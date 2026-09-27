"""Downstream temporal analysis for detached TPCV replay sequences."""

from __future__ import annotations

from collections import Counter, defaultdict
from statistics import mean, median
from typing import Iterable, Mapping

from .cpu_visualization import ReplaySequence, ReplaySequenceError


USAGE_UNAVAILABLE = "unavailable: TPCV-1 records topology existence, not per-edge event paths"
_METRICS = ("accuracy", "prediction_loss", "reward", "utility", "energy")
_REJECTION_KEYS = (
    "duplicate", "fan_in_full", "fan_out_full", "edge_capacity", "nonlocal",
    "candidate_capacity", "invalid_candidate", "no_valid_candidate", "pruning_interaction", "other",
)


def _values(metrics: Iterable[Mapping[str, object]], name: str) -> list[float]:
    return [float(item[name]) for item in metrics if isinstance(item.get(name), (int, float)) and not isinstance(item.get(name), bool)]


def _flat(values: list[float]) -> dict[str, object]:
    if not values:
        return {"available": False, "flat": None, "values": [], "min": None, "max": None, "range": None}
    low, high = min(values), max(values)
    return {"available": True, "flat": low == high, "values": values, "min": low, "max": high, "range": high - low}


def _inactive_span(active: list[bool]) -> int:
    longest = current = 0
    for value in active:
        current = 0 if value else current + 1
        longest = max(longest, current)
    return longest


def _node_statistics(sequence: ReplaySequence) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    by_id: dict[str, list[tuple[int, object]]] = defaultdict(list)
    for index, snapshot in enumerate(sequence.snapshots):
        for neuron in snapshot.neurons:
            by_id[neuron.neuron_id].append((index, neuron))
    records = []
    for neuron_id in sorted(by_id):
        samples = by_id[neuron_id]
        active = [bool(neuron.active) for _, neuron in samples]
        processed = [int(neuron.processed_events) for _, neuron in samples]
        active_indices = [index for index, value in enumerate(active) if value]
        received = processed[-1] if processed else 0
        records.append({
            "neuron_id": neuron_id,
            "first_active_snapshot": active_indices[0] if active_indices else None,
            "last_active_snapshot": active_indices[-1] if active_indices else None,
            "active_snapshot_count": sum(active),
            "activity_fraction": sum(active) / len(active) if active else 0.0,
            "event_count_over_time": received,
            "received_event_count": received,
            "received_event_delta": sum(max(0, current - previous) for previous, current in zip(processed, processed[1:])),
            "emitted_event_count": None,
            "longest_inactive_span": _inactive_span(active),
            "permanently_inactive": not any(active),
            "emitted_event_evidence": "unavailable: snapshots do not encode emitted-event identity",
        })
    return records, [{
        "snapshot": index,
        "epoch": snapshot.epoch,
        "active_neuron_count": sum(neuron.active for neuron in snapshot.neurons),
        "neuron_count": len(snapshot.neurons),
        "active_neuron_fraction": sum(neuron.active for neuron in snapshot.neurons) / len(snapshot.neurons)
        if snapshot.neurons else 0.0,
        "event_count": sum(neuron.processed_events for neuron in snapshot.neurons),
        "activation_count": sum(neuron.active for neuron in snapshot.neurons),
    } for index, snapshot in enumerate(sequence.snapshots)]


def _edge_statistics(sequence: ReplaySequence) -> tuple[list[dict[str, object]], dict[str, object]]:
    appearances: dict[tuple[str, str], list[int]] = defaultdict(list)
    delays: dict[tuple[str, str], float] = {}
    edge_sets = []
    for index, snapshot in enumerate(sequence.snapshots):
        current = set()
        for edge in snapshot.connections:
            key = (edge.source, edge.destination)
            current.add(key)
            appearances[key].append(index)
            delays[key] = edge.propagation_delay
        edge_sets.append(current)
    records = []
    for source, destination in sorted(appearances):
        indices = appearances[(source, destination)]
        runs = 1 + sum(current != previous + 1 for previous, current in zip(indices, indices[1:]))
        removed = sum(key in edge_sets[index - 1] and key not in edge_sets[index] for index in range(1, len(edge_sets)))
        records.append({
            "source": source, "destination": destination, "propagation_delay": delays[(source, destination)],
            "first_appearance_snapshot": indices[0], "last_appearance_snapshot": indices[-1],
            "lifetime_snapshots": len(indices), "lifetime_span_snapshots": indices[-1] - indices[0] + 1,
            "reappearance_count": max(0, runs - 1), "added_count": runs, "removed_count": removed,
            "persisted_to_final_snapshot": indices[-1] == len(edge_sets) - 1,
            "usage": USAGE_UNAVAILABLE, "used_recently": None, "used_frequently": None,
        })
    additions = [len(edge_sets[index] - edge_sets[index - 1]) for index in range(1, len(edge_sets))]
    removals = [len(edge_sets[index - 1] - edge_sets[index]) for index in range(1, len(edge_sets))]
    lifetimes = [item["lifetime_snapshots"] for item in records]
    return records, {
        "total_unique_edges_seen": len(records), "persistent_edge_count": sum(item["persisted_to_final_snapshot"] for item in records),
        "transient_edge_count": sum(not item["persisted_to_final_snapshot"] for item in records),
        "mean_edge_lifetime": mean(lifetimes) if lifetimes else 0.0,
        "median_edge_lifetime": median(lifetimes) if lifetimes else 0.0,
        "total_additions": sum(additions), "total_removals": sum(removals),
        "additions_per_transition": additions, "removals_per_transition": removals,
        "churn_rate": (sum(additions) + sum(removals)) / max(1, len(edge_sets) - 1),
        "final_graph_size": len(edge_sets[-1]) if edge_sets else 0,
        "edge_use_evidence": "unavailable",
    }


def _rejections(metrics: Iterable[Mapping[str, object]]) -> dict[str, int | str]:
    counts: Counter[str] = Counter()
    observed = False
    for metric in metrics:
        raw = metric.get("mutation_rejection_reasons", ())
        if isinstance(raw, Mapping):
            observed = True
            counts.update({str(key): int(value) for key, value in raw.items()})
        elif isinstance(raw, (list, tuple)):
            observed = True
            counts.update({str(item[0]): int(item[1]) for item in raw if isinstance(item, (list, tuple)) and len(item) == 2})
        else:
            for item in metric.get("mutation_history", ()) if isinstance(metric.get("mutation_history"), (list, tuple)) else ():
                if isinstance(item, (list, tuple)) and item and item[0] == "duplicate":
                    counts["duplicate"] += 1
    result = {key: counts.get(key, 0) for key in _REJECTION_KEYS}
    result["growth_attempts"] = sum(result[key] for key in _REJECTION_KEYS) + sum(int(metric.get("accepted_additions", 0)) for metric in metrics)
    result["accepted"] = sum(int(metric.get("accepted_additions", 0)) for metric in metrics)
    result["evidence"] = "recorded" if observed else "partial: older TPCV metrics do not preserve all rejection reasons"
    return result


def _timeline(sequence: ReplaySequence, node_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    metrics_by_epoch = {int(item["epoch"]): item for item in sequence.metrics if "epoch" in item}
    rows = []
    for index, snapshot in enumerate(sequence.snapshots):
        metric = dict(metrics_by_epoch.get(snapshot.epoch, {}))
        previous = rows[-1]["metrics"] if rows else {}
        rows.append({
            "snapshot": index, "epoch": snapshot.epoch,
            "connection_count": len(snapshot.connections),
            "additions": len(set((edge.source, edge.destination) for edge in snapshot.connections) -
                             (set((edge.source, edge.destination) for edge in sequence.snapshots[index - 1].connections) if index else set())),
            "removals": len((set((edge.source, edge.destination) for edge in sequence.snapshots[index - 1].connections) if index else set()) -
                            set((edge.source, edge.destination) for edge in snapshot.connections)),
            "active_neuron_fraction": node_rows[index]["active_neuron_fraction"],
            "event_count": node_rows[index]["event_count"], "activation_count": node_rows[index]["activation_count"],
            "metrics": metric,
            "metric_deltas": {name: float(metric[name]) - float(previous[name]) for name in _METRICS
                              if name in metric and name in previous},
        })
    return rows


def _classification(edge_summary: Mapping[str, object], flat: Mapping[str, Mapping[str, object]], timeline: list[dict[str, object]]) -> str:
    changed = bool(edge_summary.get("total_additions", 0) or edge_summary.get("total_removals", 0))
    active_values = [float(item["active_neuron_fraction"]) for item in timeline]
    active = bool(active_values and max(active_values) > 0.0)
    functional = [flat[name] for name in ("accuracy", "prediction_loss", "reward", "utility") if flat[name]["available"]]
    flat_functional = bool(functional) and all(item["flat"] for item in functional)
    if not changed:
        return "stable topology / active behavior" if active else "stable topology / inactive behavior"
    if flat_functional:
        return "persistent churn / no functional response"
    metric = flat.get("accuracy", {})
    values = metric.get("values", [])
    direction = "improving" if len(values) > 1 and values[-1] > values[0] else "degrading" if len(values) > 1 and values[-1] < values[0] else "flat"
    return f"changing topology / {direction} behavior"


def analyze_replay(sequence: ReplaySequence) -> dict[str, object]:
    """Return deterministic, JSON-compatible analysis without mutating replay."""
    if not isinstance(sequence, ReplaySequence):
        raise TypeError("sequence must be a ReplaySequence")
    nodes, node_timeline = _node_statistics(sequence)
    edges, edge_summary = _edge_statistics(sequence)
    timeline = _timeline(sequence, node_timeline)
    flat = {name: _flat(_values(sequence.metrics, name)) for name in _METRICS}
    functional_flat = bool(flat["accuracy"]["available"]) and all(flat[name]["flat"] for name in _METRICS if flat[name]["available"])
    active_fractions = [float(row["active_neuron_fraction"]) for row in node_timeline]
    activity_fractions = [float(row["activity_fraction"]) for row in nodes]
    result = {
        "schema_version": 1, "digest": sequence.digest, "snapshot_count": len(sequence.snapshots),
        "node_statistics": nodes, "edge_statistics": edges, "edge_summary": edge_summary,
        "snapshot_metrics": timeline, "flat_metrics": flat,
        "mutation_rejections": _rejections(sequence.metrics),
        "activity_summary": {
            "never_active_neuron_count": sum(item["permanently_inactive"] for item in nodes),
            "always_active_neuron_count": sum(item["activity_fraction"] == 1.0 for item in nodes),
            "mean_activity_fraction": mean(activity_fractions) if activity_fractions else 0.0,
            "median_activity_fraction": median(activity_fractions) if activity_fractions else 0.0,
            "active_neuron_fraction_per_snapshot": active_fractions,
        },
        "functional_metric_response_observed": not functional_flat,
        "topology_changes_with_flat_functional_metrics": bool((edge_summary["total_additions"] or edge_summary["total_removals"]) and functional_flat),
        "classification": _classification(edge_summary, flat, timeline),
        "limitations": [USAGE_UNAVAILABLE, "TPCV-1 does not encode per-neuron emitted-event identity or mutation candidates rejected before metric capture."],
    }
    return result


def compare_replays(left: ReplaySequence, right: ReplaySequence) -> dict[str, object]:
    """Compare two analyses descriptively; no superiority claim is made."""
    first, second = analyze_replay(left), analyze_replay(right)
    def final_metric(analysis: Mapping[str, object], name: str) -> float | None:
        rows = analysis["snapshot_metrics"]
        return rows[-1]["metrics"].get(name) if rows else None
    return {"left_digest": left.digest, "right_digest": right.digest, "metrics": {
        name: {"left": final_metric(first, name), "right": final_metric(second, name),
               "delta_right_minus_left": (final_metric(second, name) - final_metric(first, name))
               if final_metric(first, name) is not None and final_metric(second, name) is not None else None}
        for name in ("accuracy", "prediction_loss", "reward", "utility", "energy")
    }, "topology": {
        "left_churn_rate": first["edge_summary"]["churn_rate"], "right_churn_rate": second["edge_summary"]["churn_rate"],
        "left_final_connection_count": first["edge_summary"]["final_graph_size"], "right_final_connection_count": second["edge_summary"]["final_graph_size"],
    }, "active_neuron_fraction": {
        "left": first["activity_summary"]["active_neuron_fraction_per_snapshot"],
        "right": second["activity_summary"]["active_neuron_fraction_per_snapshot"],
    }}


def summarize_analysis(analysis: Mapping[str, object]) -> str:
    """Format a concise terminal summary from an analysis artifact."""
    edges = analysis["edge_summary"]
    activity = analysis["activity_summary"]
    rejection = analysis["mutation_rejections"]
    return (f"classification: {analysis['classification']}\n"
            f"snapshots: {analysis['snapshot_count']} | final edges: {edges['final_graph_size']} | "
            f"unique edges: {edges['total_unique_edges_seen']} | churn rate: {edges['churn_rate']:.4f}\n"
            f"inactive neurons: {activity['never_active_neuron_count']} | "
            f"persistent edges: {edges['persistent_edge_count']} | transient edges: {edges['transient_edge_count']}\n"
            f"growth attempts: {rejection['growth_attempts']} | accepted: {rejection['accepted']} | "
            f"rejection evidence: {rejection['evidence']}\n"
            f"edge-use evidence: {edges['edge_use_evidence']}")


__all__ = ["ReplaySequenceError", "USAGE_UNAVAILABLE", "analyze_replay", "compare_replays", "summarize_analysis"]
