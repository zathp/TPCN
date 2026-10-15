r"""Open one read-only TPCV replay in the local 3D topology viewer.

Launch with ``python viz_tpcn_3d.py artifacts\cpu-tpcv-12b\manifest.json``.
Space toggles playback; arrows step; home/end seek; click the bar to scrub.
Left-drag orbits, right-drag pans, and the wheel zooms. Click a node or edge
to inspect it. Green/red edges show additions/removals between snapshots,
not causal evidence of a specific plasticity or pruning mechanism.
No training, artifact discovery, or replay bundling is performed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

from tpcn.cpu_visualization import MAX_METRIC_BYTES, MANIFEST_NAME, ReplaySequence, ReplaySequenceError
from tpcn.viewer_3d import VisualizationScene


def load_single_replay(path: str | Path) -> tuple[ReplaySequence, dict[str, str]]:
    """Load exactly one manifest-listed replay and return its immutable identity."""
    selected = Path(path).expanduser()
    if selected.is_dir():
        selected = selected / MANIFEST_NAME
    if selected.name != MANIFEST_NAME:
        raise ReplaySequenceError(f"select one {MANIFEST_NAME} file or its containing run directory")
    try:
        manifest_path = selected.resolve(strict=True)
    except FileNotFoundError as error:
        raise ReplaySequenceError("selected replay manifest is missing") from error
    if not manifest_path.is_file():
        raise ReplaySequenceError("selected replay manifest is not a regular file")

    def read_bounded_manifest() -> bytes:
        with manifest_path.open("rb") as manifest_file:
            content = manifest_file.read(MAX_METRIC_BYTES + 1)
        if len(content) > MAX_METRIC_BYTES:
            raise ReplaySequenceError("replay manifest exceeds the bounded limit")
        return content

    try:
        manifest_bytes = read_bounded_manifest()
        before_hash = hashlib.sha256(manifest_bytes).hexdigest()
        sequence = ReplaySequence.load(manifest_path.parent)
        after_hash = hashlib.sha256(read_bounded_manifest()).hexdigest()
    except ReplaySequenceError:
        raise
    except OSError as error:
        raise ReplaySequenceError("selected replay cannot be read") from error
    if before_hash != after_hash:
        raise ReplaySequenceError("selected replay manifest changed while it was being loaded")
    identity = {
        "source_artifact_id": manifest_path.parent.name,
        "manifest_path": str(manifest_path),
        "manifest_sha256": before_hash,
        "replay_digest": sequence.digest,
        "snapshot_count": str(len(sequence.snapshots)),
    }
    return sequence, identity


def _camera_eye(scene: VisualizationScene) -> tuple[float, float, float]:
    yaw, pitch = math.radians(scene.camera.yaw), math.radians(scene.camera.pitch)
    distance = scene.camera.distance
    return (scene.camera.target[0] + distance * math.cos(pitch) * math.sin(yaw),
            scene.camera.target[1] + distance * math.sin(pitch),
            scene.camera.target[2] + distance * math.cos(pitch) * math.cos(yaw))


def _project(scene: VisualizationScene, point: tuple[float, float, float],
             width: int, height: int) -> tuple[float, float] | None:
    eye = _camera_eye(scene)
    forward = tuple(scene.camera.target[i] - eye[i] for i in range(3))

    def unit(vector: tuple[float, float, float]) -> tuple[float, float, float]:
        length = math.sqrt(sum(value * value for value in vector))
        return tuple(value / length for value in vector)

    forward = unit(forward)
    right = unit((-forward[2], 0.0, forward[0]))
    up = (right[1] * forward[2] - right[2] * forward[1],
          right[2] * forward[0] - right[0] * forward[2],
          right[0] * forward[1] - right[1] * forward[0])
    relative = tuple(point[i] - eye[i] for i in range(3))
    depth = sum(relative[i] * forward[i] for i in range(3))
    if depth <= 0.1:
        return None
    fov_scale = math.tan(math.radians(55.0) / 2.0)
    x = sum(relative[i] * right[i] for i in range(3))
    y = sum(relative[i] * up[i] for i in range(3))
    aspect = width / max(height, 1)
    return (width * (0.5 + x / (2.0 * depth * fov_scale * aspect)),
            height * (0.5 - y / (2.0 * depth * fov_scale)))


def _point_segment_distance(point: tuple[float, float], start: tuple[float, float],
                            end: tuple[float, float]) -> float:
    dx, dy = end[0] - start[0], end[1] - start[1]
    length_squared = dx * dx + dy * dy
    fraction = 0.0 if length_squared == 0.0 else max(
        0.0, min(1.0, ((point[0] - start[0]) * dx + (point[1] - start[1]) * dy) / length_squared))
    return math.hypot(point[0] - start[0] - fraction * dx,
                      point[1] - start[1] - fraction * dy)


def _slider_index(x: int, width: int, snapshot_count: int) -> int:
    fraction = max(0.0, min(1.0, (x - 350) / max(width - 368, 1)))
    return round(fraction * max(snapshot_count - 1, 0))


def _transport_button(x: int, screen_y: int, height: int) -> int | None:
    if 42 <= height - screen_y <= 72:
        for index, (left, right) in enumerate(((12, 68), (76, 124), (132, 220),
                                               (228, 276), (284, 340))):
            if left <= x <= right:
                return index
    return None


def _pick(scene: VisualizationScene, position: tuple[int, int], width: int,
          height: int) -> tuple[str, Any] | None:
    """Pick a projected node first, then a directed edge; render state is read-only."""
    cursor = (float(position[0]), float(position[1]))
    projected_nodes = [(node.neuron_id, _project(scene, node.position, width, height))
                       for node in scene.nodes()]
    visible_nodes = [(identifier, point) for identifier, point in projected_nodes if point is not None]
    nearby = [(math.dist(cursor, point), identifier) for identifier, point in visible_nodes]
    if nearby:
        distance, identifier = min(nearby)
        if distance <= 16.0:
            return "neuron", identifier
    projected = {identifier: point for identifier, point in visible_nodes}
    candidates = []
    for edge in scene.edges():
        start, end = projected.get(edge.source), projected.get(edge.destination)
        if start is not None and end is not None:
            candidates.append((_point_segment_distance(cursor, start, end), (edge.source, edge.destination)))
    if candidates:
        distance, edge = min(candidates)
        if distance <= 8.0:
            return "edge", edge
    return None


def _draw_window(scene: VisualizationScene, identity: dict[str, str], width: int, height: int) -> int:
    try:
        import pygame
        from pygame.locals import DOUBLEBUF, OPENGL
        from OpenGL.GL import (
            GL_BLEND, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_LINES, GL_MODELVIEW,
            GL_ONE_MINUS_SRC_ALPHA, GL_POINTS, GL_PROJECTION, GL_QUADS, GL_SRC_ALPHA, GL_TRIANGLES,
            glBegin, glBlendFunc, glClear, glClearColor, glColor4f, glDisable, glEnable, glEnd,
            glDrawPixels, glLineWidth, glLoadIdentity, glMatrixMode, glOrtho, glPointSize,
            glPopMatrix, glPushMatrix, glVertex2f, glVertex3f, glWindowPos2d, GL_RGBA, GL_UNSIGNED_BYTE,
        )
        from OpenGL.GLU import gluLookAt, gluPerspective
    except ImportError as error:
        print(f"Interactive viewer requires pygame and PyOpenGL: {error}")
        return 2

    pygame.init()
    pygame.display.set_caption(f"TPCV replay — {identity['source_artifact_id']} (read-only)")
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 13)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClearColor(0.025, 0.035, 0.05, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(55.0, width / max(height, 1), 0.1, 200.0)
    drag: tuple[int, int, int, int, int] | None = None
    scrubbing = False
    running = True
    while running:
        elapsed = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    scene.playing = not scene.playing
                elif event.key in (pygame.K_RIGHT, pygame.K_n):
                    scene.step()
                elif event.key in (pygame.K_LEFT, pygame.K_p):
                    scene.step(-1)
                elif event.key == pygame.K_HOME:
                    scene.first()
                elif event.key == pygame.K_END:
                    scene.last()
                elif event.key in (pygame.K_EQUALS, pygame.K_PLUS):
                    scene.playback_speed = min(32.0, scene.playback_speed * 2.0)
                elif event.key == pygame.K_MINUS:
                    scene.playback_speed = max(0.25, scene.playback_speed / 2.0)
                elif event.key == pygame.K_r:
                    scene.camera.reset()
                elif event.key == pygame.K_f:
                    scene.fit()
                elif event.key == pygame.K_a:
                    scene.filters.active_only = not scene.filters.active_only
                elif event.key == pygame.K_c:
                    scene.filters.changed_only = not scene.filters.changed_only
                elif event.key == pygame.K_o:
                    scene.set_mode("overview")
                elif event.key == pygame.K_t:
                    scene.set_mode("activity")
                elif event.key == pygame.K_s:
                    scene.set_mode("structural")
                elif event.key == pygame.K_m:
                    scene.set_mode("neighborhood" if scene.selected_neuron else "overview")
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    nodes = scene.snapshot.neurons
                    ordinal = event.key - pygame.K_1
                    scene.select(nodes[ordinal].neuron_id if ordinal < len(nodes) else None)
            elif event.type == pygame.MOUSEWHEEL:
                scene.zoom(-event.y * 1.0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, screen_y = event.pos
                y = height - screen_y
                if event.button in (4, 5):
                    scene.zoom(1.0 if event.button == 4 else -1.0)
                elif screen_y >= height - 76:
                    button = _transport_button(x, screen_y, height)
                    if event.button == 1 and button is not None:
                        if button == 0:
                            scene.first()
                        elif button == 1:
                            scene.step(-1)
                        elif button == 2:
                            scene.playing = not scene.playing
                        elif button == 3:
                            scene.step(1)
                        elif button == 4:
                            scene.last()
                    elif event.button == 1 and x >= 350 and y <= 30:
                        scrubbing = True
                        scene.seek(_slider_index(x, width, len(scene.replay.snapshots)))
                elif event.button in (1, 2, 3):
                    drag = (x, screen_y, event.button, x, screen_y)
            elif event.type == pygame.MOUSEMOTION and scrubbing:
                scene.seek(_slider_index(event.pos[0], width, len(scene.replay.snapshots)))
            elif event.type == pygame.MOUSEMOTION and drag is not None:
                x, screen_y = event.pos
                dx, dy = x - drag[3], screen_y - drag[4]
                if drag[2] == 1:
                    scene.orbit(dx * 0.5, -dy * 0.5)
                else:
                    scale = scene.camera.distance * 0.002
                    scene.pan(-dx * scale, dy * scale)
                drag = (drag[0], drag[1], drag[2], x, screen_y)
            elif event.type == pygame.MOUSEBUTTONUP:
                if scrubbing and event.button == 1:
                    scene.seek(_slider_index(event.pos[0], width, len(scene.replay.snapshots)))
                    scrubbing = False
                elif drag is not None and drag[2] == 1 and event.button == 1:
                    moved = math.dist(event.pos, drag[:2])
                    if moved < 4 and event.pos[1] < height - 76:
                        picked = _pick(scene, event.pos, width, height)
                        if picked is None:
                            scene.select(None)
                            scene.select_edge(None)
                        elif picked[0] == "neuron":
                            scene.select(str(picked[1]))
                        else:
                            scene.select_edge(picked[1])
                drag = None

        scene.tick(elapsed)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        eye = _camera_eye(scene)
        gluLookAt(*eye, *scene.camera.target, 0.0, 1.0, 0.0)
        glLineWidth(1.5)
        glBegin(GL_LINES)
        for edge in scene.edges():
            if edge.kind == "pruned":
                glColor4f(1.0, 0.23, 0.18, 0.95)
            elif edge.kind == "added":
                glColor4f(0.3, 1.0, 0.48, 0.95)
            elif scene.selected_edge == (edge.source, edge.destination):
                glColor4f(1.0, 0.85, 0.15, 1.0)
            else:
                glColor4f(0.24, 0.68, 0.9, 0.48)
            start, end = scene.positions[edge.source], scene.positions[edge.destination]
            glVertex3f(*start)
            glVertex3f(*end)
        glEnd()
        # Small arrowheads encode the direction of every currently existing edge.
        glBegin(GL_TRIANGLES)
        for edge in scene.edges():
            if edge.kind == "pruned":
                continue
            if edge.kind == "added":
                glColor4f(0.3, 1.0, 0.48, 0.95)
            elif scene.selected_edge == (edge.source, edge.destination):
                glColor4f(1.0, 0.85, 0.15, 1.0)
            else:
                glColor4f(0.24, 0.68, 0.9, 0.65)
            start, end = scene.positions[edge.source], scene.positions[edge.destination]
            direction = tuple(end[i] - start[i] for i in range(3))
            length = math.sqrt(sum(value * value for value in direction))
            if length == 0.0:
                continue
            direction = tuple(value / length for value in direction)
            reference = (0.0, 1.0, 0.0) if abs(direction[1]) < 0.9 else (1.0, 0.0, 0.0)
            side = (direction[1] * reference[2] - direction[2] * reference[1],
                    direction[2] * reference[0] - direction[0] * reference[2],
                    direction[0] * reference[1] - direction[1] * reference[0])
            side_length = math.sqrt(sum(value * value for value in side))
            side = tuple(value / side_length * 0.13 for value in side)
            tip = tuple(end[i] - direction[i] * 0.35 for i in range(3))
            base = tuple(tip[i] - direction[i] * 0.35 for i in range(3))
            glVertex3f(*tip)
            glVertex3f(*(base[i] + side[i] for i in range(3)))
            glVertex3f(*(base[i] - side[i] for i in range(3)))
        glEnd()
        glPointSize(12.0)
        glBegin(GL_POINTS)
        for node in scene.nodes():
            if node.selected:
                glColor4f(1.0, 1.0, 1.0, 1.0)
            elif node.changed:
                glColor4f(1.0, 0.72, 0.12, 1.0)
            elif node.active:
                glColor4f(0.2, 0.9, 0.48, 1.0)
            else:
                glColor4f(0.45, 0.55, 0.68, 0.9)
            glVertex3f(*node.position)
        glEnd()

        summary = scene.summary()
        metrics = scene.metrics or {}
        snapshot = scene.snapshot
        if scene.selected_edge is not None:
            inspect = scene.inspect_edge() or {}
            selection = (f"EDGE {inspect.get('source')} -> {inspect.get('destination')}  "
                         f"status={inspect.get('status')}  delay={inspect.get('propagation_delay', 'unavailable')}")
        else:
            inspect = scene.inspect()
            selection = "selection: click a neuron or an edge to inspect"
            if inspect is not None:
                selection = (f"NEURON {inspect['neuron_id']} state={inspect['state']:.5g} "
                             f"active={inspect['active']} activation={inspect['activation'] if inspect['activation'] is not None else 'unavailable'} "
                             f"events={inspect['processed_events']} fan-in/out={inspect['fan_in']}/{inspect['fan_out']} "
                             f"topology-deltas={len(inspect['topology_changes'])}")
        lines = (
            f"ARTIFACT {identity['source_artifact_id']} | read-only single replay",
            f"MANIFEST {identity['manifest_path']}",
            f"MANIFEST SHA-256 {identity['manifest_sha256']}",
            f"SNAPSHOT {scene.snapshot_index + 1}/{len(scene.replay.snapshots)}  time={snapshot.timestamp:g}  epoch={snapshot.epoch}  layout={scene.coordinate_source} (diagnostic positions are visualization-only)",
            f"nodes active={summary['nodes_active']}/{summary['node_count']}  edges={summary['connections']}  added={summary['added']}  removed(snapshot diff only)={summary['removed']}  changed nodes={len(scene.diff.changed_neurons)}  rejected mutations={metrics.get('rejected_mutations', 'unavailable')}",
            f"accuracy={metrics.get('accuracy', 'unavailable')}  loss={metrics.get('prediction_loss', 'unavailable')}  reward={metrics.get('reward', 'unavailable')}  energy={metrics.get('energy', 'unavailable')}  utility={metrics.get('utility', 'unavailable')}",
            selection,
            "Persistent edges blue; added edges green; removed snapshot-diff edges red; changed nodes gold. No event-by-event propagation timing is recorded.",
            f"space play/pause | arrows step | home/end | +/- speed ({scene.playback_speed:g} snapshots/s) | drag left orbit/right pan | wheel zoom | f fit | r reset | a active | c changed | 1-9 select | esc quit",
        )
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glColor4f(0.025, 0.035, 0.05, 0.92)
        glBegin(GL_QUADS)
        glVertex2f(0, height - 174)
        glVertex2f(width, height - 174)
        glVertex2f(width, height)
        glVertex2f(0, height)
        glVertex2f(0, 0)
        glVertex2f(width, 0)
        glVertex2f(width, 82)
        glVertex2f(0, 82)
        glEnd()
        buttons = ((12, 68, "FIRST"), (76, 124, "PREV"), (132, 220, "PAUSE" if scene.playing else "PLAY"),
                   (228, 276, "NEXT"), (284, 340, "LAST"))
        for left, right, _ in buttons:
            glBegin(GL_QUADS)
            glColor4f(0.12, 0.2, 0.3, 1.0)
            glVertex2f(left, 42)
            glVertex2f(right, 42)
            glVertex2f(right, 72)
            glVertex2f(left, 72)
            glEnd()
        slider_left, slider_right = 350, width - 18
        slider_y = 20
        glBegin(GL_LINES)
        glColor4f(0.42, 0.52, 0.64, 1.0)
        glVertex2f(slider_left, slider_y)
        glVertex2f(slider_right, slider_y)
        progress = scene.snapshot_index / max(len(scene.replay.snapshots) - 1, 1)
        glColor4f(0.25, 0.9, 0.52, 1.0)
        glVertex2f(slider_left, slider_y)
        glVertex2f(slider_left + (slider_right - slider_left) * progress, slider_y)
        glEnd()
        for index, line in enumerate(lines):
            surface = font.render(line, True, (225, 234, 245))
            rgba = pygame.image.tostring(surface, "RGBA", True)
            glWindowPos2d(12, height - 22 - index * 18)
            glDrawPixels(surface.get_width(), surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, rgba)
        for left, _, label in buttons:
            surface = font.render(label, True, (240, 245, 250))
            rgba = pygame.image.tostring(surface, "RGBA", True)
            glWindowPos2d(left + 6, 51)
            glDrawPixels(surface.get_width(), surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, rgba)
        timeline = font.render(f"SNAPSHOT {scene.snapshot_index + 1} / {len(scene.replay.snapshots)} — click bar to scrub", True, (220, 230, 240))
        glWindowPos2d(slider_left, 27)
        glDrawPixels(timeline.get_width(), timeline.get_height(), GL_RGBA, GL_UNSIGNED_BYTE,
                     pygame.image.tostring(timeline, "RGBA", True))
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        pygame.display.flip()
    pygame.quit()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("replay", type=Path, help="one run directory or its exact manifest.json")
    parser.add_argument("--width", type=int, default=1440)
    parser.add_argument("--height", type=int, default=900)
    parser.add_argument("--inspect-only", action="store_true", help="validate one replay and print identity/summary")
    args = parser.parse_args()
    if args.width < 640 or args.height < 480:
        parser.error("window dimensions must be at least 640 by 480")
    try:
        sequence, identity = load_single_replay(args.replay)
        scene = VisualizationScene(sequence)
    except (ReplaySequenceError, OSError, ValueError) as error:
        parser.error(str(error))
    if args.inspect_only:
        report = dict(identity)
        report["snapshot_count"] = len(sequence.snapshots)
        report["summary"] = scene.summary()
        report["unsupported_fields"] = [
            "canonical 3D coordinates (uses diagnostic layout when no positions are recorded)",
            "event-by-event propagation timing",
            "per-edge traffic",
            "per-neuron energy and utility",
        ]
        print(json.dumps(report, indent=2, sort_keys=True, default=str))
        return 0
    return _draw_window(scene, identity, args.width, args.height)


if __name__ == "__main__":
    raise SystemExit(main())
