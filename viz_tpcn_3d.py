"""Interactive replay viewer for Luna-12C TPCV artifacts."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from tpcn.cpu_visualization import ReplaySequence, ReplaySequenceError
from tpcn.viewer_3d import VisualizationScene


def _run_window(scene: VisualizationScene, width: int, height: int) -> int:
    try:
        import pygame
        from pygame.locals import DOUBLEBUF, OPENGL
        from OpenGL.GL import (GL_BLEND, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_LINES,
                               GL_MODELVIEW, GL_ONE_MINUS_SRC_ALPHA, GL_POINTS, GL_PROJECTION, GL_SRC_ALPHA,
                               glBegin, glBlendFunc, glClear, glClearColor, glColor4f, glEnable, glEnd,
                       glDisable, glEnable, glLoadIdentity, glMatrixMode, glPointSize, glVertex3f, glLineWidth,
                       GL_DEPTH_TEST, glWindowPos2d, glDrawPixels, GL_RGBA, GL_UNSIGNED_BYTE)
        from OpenGL.GLU import gluLookAt, gluPerspective
    except ImportError as error:
        print(f"Interactive viewer requires pygame and PyOpenGL: {error}")
        return 2
    pygame.init()
    pygame.display.set_caption("TPCN TPCV-1 temporal viewer")
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    clock = pygame.time.Clock()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClearColor(0.025, 0.035, 0.05, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(55.0, width / max(height, 1), 0.1, 200.0)
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
        scene.tick(elapsed)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        yaw, pitch = math.radians(scene.camera.yaw), math.radians(scene.camera.pitch)
        distance = scene.camera.distance
        eye = (distance * math.cos(pitch) * math.sin(yaw), distance * math.sin(pitch), distance * math.cos(pitch) * math.cos(yaw))
        gluLookAt(*eye, *scene.camera.target, 0.0, 1.0, 0.0)
        glLineWidth(1.0)
        glBegin(GL_LINES)
        for edge in scene.edges():
            glColor4f(1.0, 0.25, 0.15, 0.85) if edge.kind == "pruned" else glColor4f(0.2, 0.7, 1.0, 0.35)
            glVertex3f(*scene.positions[edge.source])
            glVertex3f(*scene.positions[edge.destination])
        glEnd()
        glPointSize(7.0)
        glBegin(GL_POINTS)
        for node in scene.nodes():
            intensity = min(1.0, abs(node.activation))
            glColor4f(1.0 if node.selected else 0.25 + intensity * 0.7,
                      0.75 if node.active else 0.2, 0.2 if node.active else 0.35, 1.0)
            glVertex3f(*node.position)
        glEnd()
        font = pygame.font.SysFont("consolas", 16)
        summary = scene.summary()
        metric = scene.metrics or {}
        lines = (
            f"TPCV-1  snapshot {scene.snapshot_index + 1}/{len(scene.replay.snapshots)}  epoch {scene.snapshot.epoch}",
            f"nodes active {summary['nodes_active']}/{summary['node_count']}  edges {summary['connections']}  +{summary['added']} -{summary['removed']}",
            f"accuracy {metric.get('accuracy', 'unavailable')}  loss {metric.get('prediction_loss', 'unavailable')}  reward {metric.get('reward', 'unavailable')}  energy {metric.get('energy', 'unavailable')}  utility {metric.get('utility', 'unavailable')}",
            f"mode {scene.filters.mode}  active-only {scene.filters.active_only}  changed-only {scene.filters.changed_only}  coordinates {scene.coordinate_source}",
            "space play/pause  arrows step  home/end jump  +/- speed  f fit  r reset  a/c filters  o/t/s/m modes  1-9 select  esc quit",
        )
        glDisable(GL_DEPTH_TEST)
        for line_index, line in enumerate(lines):
            surface = font.render(line, True, (220, 230, 240))
            rgba = pygame.image.tostring(surface, "RGBA", True)
            glWindowPos2d(12, height - 24 - line_index * 20)
            glDrawPixels(surface.get_width(), surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, rgba)
        glEnable(GL_DEPTH_TEST)
        pygame.display.flip()
    pygame.quit()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("replay", type=Path)
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=800)
    parser.add_argument("--inspect-only", action="store_true", help="Validate and print the first scene summary")
    args = parser.parse_args()
    try:
        scene = VisualizationScene(ReplaySequence.load(args.replay))
    except (ReplaySequenceError, OSError, ValueError) as error:
        parser.error(str(error))
    if args.inspect_only:
        print(scene.summary())
        return 0
    return _run_window(scene, args.width, args.height)


if __name__ == "__main__":
    raise SystemExit(main())