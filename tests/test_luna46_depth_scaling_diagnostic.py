"""Synthetic analytical tests plus a retained integrity-only check; no science run."""

from __future__ import annotations

import ast
from copy import deepcopy
import math
from pathlib import Path
import sys

import pytest

import run_luna46_depth_scaling_diagnostic as diagnostic


def synthetic_sequence(payloads, times=None, prior=0.0):
    """Mathematical observations only; no runtime/neuron/fixture generator."""
    times = times if times is not None else [float(i) for i in range(len(payloads))]
    arrivals, updates = [], []
    state = 0.0
    for index, (payload, timestamp) in enumerate(zip(payloads, times)):
        after = state * math.exp(-diagnostic.RATE * (timestamp - prior)) + payload
        arrivals.append({"event_id": f"e{index}", "queue_sequence": index,
                         "timestamp": timestamp, "payload": payload})
        updates.append({
            "event_id": f"e{index}", "queue_sequence": index, "event_type": "excursion",
            "timestamp": timestamp, "prior_clock": prior, "payload": payload,
            "z_before": state, "z_after": after, "mode_before": "N",
        })
        state, prior = after, timestamp
    return arrivals, updates


def synthetic_captures(payloads=(0.3, -0.2), times=(1.0, 2.0), source="relay", destination="destination"):
    enqueues, receptions = [], []
    for index, (payload, timestamp) in enumerate(zip(payloads, times)):
        common = {
            "event_id": f"e{index}", "queue_sequence": index, "source": source,
            "destination": destination, "event_type": "excursion", "payload": payload,
            "payload_bits": diagnostic.bits(payload), "lineage_id": index,
            "originating_emission_id": f"e{index}", "route_path": [source, destination],
            "route_depth": 1, "causal_roots": [f"root{index}"], "roots_truncated": False,
            "payload_encoding": {"decimal": repr(float(payload)), "hex": float(payload).hex()},
        }
        enqueues.append({**common, "enqueue_timestamp": timestamp - 1.0,
                         "scheduled_delivery_timestamp": timestamp})
        receptions.append({**deepcopy(common), "receiver_node": destination,
                           "reception_timestamp": timestamp, "scheduled_delivery_timestamp": timestamp,
                           "receiver_state_transition": {
                               "event_sequence": index, "processed_events_before": index,
                               "processed_events_after": index + 1}})
    return enqueues, receptions


def synthetic_destination(payloads=(0.3, 0.2), times=(1.0, 81.0)):
    enqueues, receptions = synthetic_captures(payloads, times)
    arrivals = diagnostic.reconcile(enqueues, receptions, "relay", "destination")
    _, updates = synthetic_sequence(payloads, times)
    traces, evidence = [], []
    for arrival, update in zip(arrivals, updates):
        dt = update["timestamp"] - update["prior_clock"]
        pre = update["z_before"] * math.exp(-diagnostic.RATE * dt)
        arrival["raw_reception"]["receiver_state_transition"].update(
            z_before=update["z_before"], z_after=update["z_after"])
        traces.append({
            "timestamp": update["timestamp"], "elapsed": dt, "input_value": update["payload"],
            "theta_e": 1.0, "theta_z": 1.0, "decay_rate": 1.0, "decay_rate_z": 0.0125,
            "mode_before": "N", "integrated": True, "z_before_decay": update["z_before"],
            "z_after_decay": pre, "z_after_input": update["z_after"],
            "z_post_discharge": update["z_after"], "x_after_input": update["payload"],
            "discharge_amount": 0.0,
        })
        evidence.append({
            "stream_id": "synthetic", "actual_reception": deepcopy(arrival["raw_reception"]),
            "queue_admission": deepcopy(arrival["raw_enqueue"]),
            "arrival_timestamp": update["timestamp"], "routed_contribution": update["payload"],
            "discharge_amount": 0.0, "discharge_decision": False, "discharge_sign": 0,
            "z_before_decay": update["z_before"], "elapsed": dt, "z_after_decay": pre,
            "z_after_contribution": update["z_after"], "resulting_z": update["z_after"],
        })
    return {"stream_id": "synthetic", "destination_state_trajectory": updates,
            "destination_integration_trace": traces, "destination_evidence": evidence}, arrivals


@pytest.mark.parametrize("payloads,times,expected", [
    ([], [], "NO-RECEPTIONS"),
    ([1.0], [0.0], "ALREADY-CROSSING"),
    ([-1.0], [0.0], "ALREADY-CROSSING"),
    ([0.6, 0.6], [0.0, 80.0], "TEMPORAL-RETENTION-LIMITED"),
    ([-0.6, -0.6], [0.0, 80.0], "TEMPORAL-RETENTION-LIMITED"),
    ([0.6, -0.6], [0.0, 0.0], "CANCELLATION-LIMITED"),
    ([0.2, 0.3], [0.0, 0.0], "DRIVE-LIMITED"),
    ([0.6, 0.6, -0.6], [0.0, 0.0, 0.0], "ALREADY-CROSSING"),
    ([math.nextafter(1.0, 0.0)], [0.0], "DRIVE-LIMITED"),
    ([0.5, 0.5], [0.0, 0.0], "ALREADY-CROSSING"),
    ([0.5, -0.5], [0.0, 0.0], "CANCELLATION-LIMITED"),
])
def test_exact_priority_partition(payloads, times, expected):
    arrivals, updates = synthetic_sequence(payloads, times)
    result = diagnostic.analyze_sequence("synthetic", arrivals, updates)
    assert result["category"] == expected
    assert result["signed_sum"] == sum(payloads)
    assert result["total_absolute_input"] == sum(abs(p) for p in payloads)


def test_closed_form_actual_recurrence_and_signed_zero_decay():
    arrivals, updates = synthetic_sequence([0.6, 0.6, -0.2], [0.0, 80.0, 160.0])
    result = diagnostic.analyze_sequence("synthetic", arrivals, updates)
    rows = result["recurrence_evidence"]
    assert rows[1]["rho"] == math.exp(-1)
    assert rows[1]["state_after"] == math.exp(-1) * 0.6 + 0.6
    assert rows[2]["zero_decay_state"] == 1.0
    assert rows[1]["zero_crosses"] and not rows[1]["actual_crosses"]
    assert result["first_zero_crossing"]["queue_sequence"] == 1
    for row in rows:
        assert row["recurrence"]["observed"] == row["recurrence"]["expected"]
        assert row["recurrence"]["residual"] == 0
        assert row["recurrence"]["bound"] == 64 * sys.float_info.epsilon


def test_first_interval_uses_retained_prior_not_invented_start():
    arrivals, updates = synthetic_sequence([0.3], [20.0], prior=19.0)
    result = diagnostic.analyze_sequence("synthetic", arrivals, updates)
    row = result["recurrence_evidence"][0]
    assert row["prior_clock"] == 19.0 and row["dt"] == 1.0
    assert row["rho"] == math.exp(-0.0125)
    assert row["retention_ratio"] is None
    assert result["timing"]["gaps"]["count"] == 0


def test_intervening_updates_are_kept_and_validated():
    arrivals, updates = synthetic_sequence([0.4, 0.2], [0.0, 80.0])
    state = 0.4 * math.exp(-0.5)
    intermediate = {"event_id": "error", "queue_sequence": 1, "event_type": "prediction_error",
                    "timestamp": 40.0, "prior_clock": 0.0, "z_before": 0.4, "z_after": state}
    arrivals[1]["queue_sequence"] = 2
    updates[1].update(queue_sequence=2, prior_clock=40.0, z_before=state,
                      z_after=state * math.exp(-0.5) + 0.2)
    result = diagnostic.analyze_sequence("synthetic", arrivals, [updates[0], intermediate, updates[1]])
    assert len(result["all_update_boundaries"]) == 3
    assert result["recurrence_evidence"][1]["dt"] == 40
    with pytest.raises(diagnostic.Blocked, match="intervening"):
        diagnostic.analyze_sequence("synthetic", arrivals, updates)
    intermediate["z_after"] += 0.01
    with pytest.raises(diagnostic.Blocked, match="recurrence"):
        diagnostic.analyze_sequence("synthetic", arrivals, [updates[0], intermediate, updates[1]])


@pytest.mark.parametrize("field,value", [
    ("z_after", 0.31), ("z_before", 0.1), ("timestamp", -1.0),
    ("payload", -0.3), ("event_id", "other"), ("event_type", "input"),
])
def test_recurrence_identity_mutations_block(field, value):
    arrivals, updates = synthetic_sequence([0.3], [0.0])
    updates[0][field] = value
    with pytest.raises(diagnostic.Blocked):
        diagnostic.analyze_sequence("synthetic", arrivals, updates)


def test_equation_tolerance_does_not_relax_threshold():
    epsilon_bound = 64 * sys.float_info.epsilon
    assert diagnostic.equation(0.0, epsilon_bound)["matches"]
    assert not diagnostic.equation(0.0, math.nextafter(epsilon_bound, math.inf))["matches"]
    arrivals, updates = synthetic_sequence([math.nextafter(1.0, 0.0)], [0.0])
    result = diagnostic.analyze_sequence("synthetic", arrivals, updates)
    assert not result["actual_crosses"] and not result["zero_crosses"]
    assert result["category"] == "DRIVE-LIMITED"
    updates[0]["z_after"] = 1.0
    with pytest.raises(diagnostic.Blocked, match="threshold"):
        diagnostic.analyze_sequence("synthetic", arrivals, updates)


def test_empty_singleton_and_reset_isolation():
    empty = diagnostic.analyze_sequence("empty", [], [])
    arrivals, updates = synthetic_sequence([-0.3], [10.0])
    single = diagnostic.analyze_sequence("single", arrivals, updates)
    assert empty["actual"] == {"min": 0.0, "max": 0.0, "max_abs": 0.0}
    assert single["zero_decay"] == {"min": -0.3, "max": 0.0, "max_abs": 0.3}
    assert single["timing"]["positive_gaps"]["mean"] is None
    assert diagnostic.analyze_sequence("single", arrivals, updates) == single
    assert single["rho"]["count"] == 1


def test_signed_decay_cancellation_and_overshoot_are_distinct():
    arrivals, updates = synthetic_sequence([-0.8, 0.5, 0.0, 0.9], [0.0, 80.0, 80.0, 80.0])
    result = diagnostic.analyze_sequence("signed", arrivals, updates)
    row = result["recurrence_evidence"][1]
    retained = -0.8 * math.exp(-1)
    assert row["alignment"] == "opposing"
    assert row["cancelled_magnitude"] == abs(retained)
    assert row["overshoot_magnitude"] == 0.5 - abs(retained)
    assert row["signed_decay_loss"] == -0.8 - retained
    assert row["absolute_decay_loss"] == 0.8 - abs(retained)
    assert result["alignment_counts"] == {"constructive": 1, "opposing": 1, "zero-reference": 1, "zero-input": 1}
    assert result["signed_decay_loss"] < 0
    assert result["absolute_decay_loss"] > 0
    assert result["recurrence_evidence"][3]["alignment"] == "constructive"


def test_zero_reference_and_zero_input_policies():
    arrivals, updates = synthetic_sequence([0.0, 0.2, -0.2, 0.0], [0.0] * 4)
    result = diagnostic.analyze_sequence("zeros", arrivals, updates)
    assert [r["alignment"] for r in result["recurrence_evidence"]] == [
        "zero-input", "zero-reference", "opposing", "zero-input"]
    assert result["recurrence_evidence"][-1]["retention_ratio"] is None
    assert result["timing"]["zero_payload_count"] == 2


def test_timing_ties_declared_percentiles_and_run_breaks():
    arrivals, _ = synthetic_sequence([0.2, 0.3, 0.0, -0.2, -0.1, 0.3], [0., 0., 2., 4., 8., 10.])
    stats = diagnostic.timing(arrivals)
    assert stats["gaps"]["values"] == [0.0, 2.0, 2.0, 4.0, 2.0]
    assert stats["zero_gap_count"] == 1
    assert stats["positive_gaps"]["mean"] == 2.5
    assert stats["positive_gaps"]["median"] == 2.0
    assert stats["positive_gaps"]["percentiles"]["75"] == 2.5
    assert stats["positive_gaps"]["percentiles"]["90"] == pytest.approx(3.4)
    assert [r["length"] for r in stats["constructive_runs"]] == [2, 2, 1]
    assert stats["constructive_runs"][1]["duration_over_tau"] == 4 / 80
    assert list(stats["gaps"]["percentiles"]) == ["50", "75", "90", "95", "99"]
    assert stats["run_zero_gap_count"] == 1
    assert stats["run_positive_gaps"]["values"] == [4.0]
    assert stats["run_gaps_over_tau"]["values"] == [0.0, .05]


@pytest.mark.parametrize("values", [[], [2.0], [0.0, 0.0]])
def test_distribution_empty_single_ties(values):
    result = diagnostic.distribution(values)
    assert result["count"] == len(values)
    assert result["max"] == (max(values) if values else None)
    assert result["percentiles"]["99"] == (values[0] if values else None)


def test_pooled_gaps_never_bridge_character_reset():
    a, _ = synthetic_sequence([.2, .3], [0., 10.])
    b, _ = synthetic_sequence([.2, .3], [1000., 1020.])
    pooled = diagnostic.pooled_timing([diagnostic.timing(a), diagnostic.timing(b)])
    assert pooled["gaps"]["values"] == [10., 20.]


def counts(no=0, already=0, retention=0, cancellation=0, drive=0):
    return dict(zip(diagnostic.CATEGORIES, (no, already, retention, cancellation, drive)))


@pytest.mark.parametrize("inventory,expected,n,cutoffs", [
    (counts(no=8), "BLOCKED", 0, (0, 0, 0)),
    (counts(retention=1), "SUPPORTS TEMPORAL-RETENTION BOTTLENECK", 1, (1, 1, 1)),
    (counts(drive=1), "SUPPORTS DRIVE/CANCELLATION BOTTLENECK", 1, (1, 1, 1)),
    (counts(already=1), "MIXED", 1, (1, 1, 1)),
    (counts(already=15, retention=5), "SUPPORTS TEMPORAL-RETENTION BOTTLENECK", 20, (5, 2, 15)),
    (counts(already=16, retention=4), "MIXED", 20, (5, 2, 15)),
    (counts(already=13, retention=5, drive=2), "MIXED", 20, (5, 2, 15)),
    (counts(already=14, retention=5, drive=1), "SUPPORTS TEMPORAL-RETENTION BOTTLENECK", 20, (5, 2, 15)),
    (counts(already=4, retention=1, cancellation=7, drive=8), "SUPPORTS DRIVE/CANCELLATION BOTTLENECK", 20, (5, 2, 15)),
    (counts(already=5, retention=1, drive=14), "MIXED", 20, (5, 2, 15)),
    (counts(already=3, retention=2, drive=15), "MIXED", 20, (5, 2, 15)),
    (counts(no=100, already=1, retention=1, drive=1), "MIXED", 3, (1, 1, 3)),
    (counts(already=18, retention=3), "MIXED", 21, (6, 3, 16)),
])
def test_verdict_exact_boundaries_and_denominator(inventory, expected, n, cutoffs):
    result = diagnostic.verdict(inventory)
    assert result["verdict"] == expected
    assert result["reception_bearing_N"] == n
    assert tuple(result["cutoffs"].values()) == cutoffs
    assert result["fractions"]["NO-RECEPTIONS"] is None
    if n:
        assert sum(f for f in result["fractions"].values() if f is not None) == pytest.approx(1.0)


@pytest.mark.parametrize("bad", [counts(drive=-1), {**counts(), "extra": 0}, counts(drive=True)])
def test_invalid_verdict_counts_block(bad):
    with pytest.raises(diagnostic.Blocked):
        diagnostic.verdict(bad)


def test_aggregate_metrics_keep_signed_and_absolute_and_no_receptions():
    a, u = synthetic_sequence([0.6, 0.6], [0., 80.])
    b, v = synthetic_sequence([0.6, -0.6], [0., 0.])
    rows = [diagnostic.analyze_sequence("a", a, u), diagnostic.analyze_sequence("b", b, v),
            diagnostic.analyze_sequence("empty", [], [])]
    result = diagnostic.aggregate(rows)
    assert result["reception_bearing_N"] == 2
    assert result["receptions"] == 4
    assert result["signed_sum"] == 1.2
    assert result["total_absolute_input"] == 2.4
    assert result["counts"]["NO-RECEPTIONS"] == 1
    assert result["zero_decay"]["max_abs"] == 1.2
    assert result["zero_crossing_sequences"] == 1
    assert result["actual_crossing_sequences"] == 0
    assert result["rho"]["count"] == 4


def test_reconcile_success_exact_ties_and_payload_sign():
    enqueues, receptions = synthetic_captures((0.3, -0.2), (1., 1.))
    result = diagnostic.reconcile(enqueues, receptions, "relay", "destination")
    assert [row["payload"] for row in result] == [0.3, -0.2]
    assert [row["queue_sequence"] for row in result] == [0, 1]
    assert len(result) == 2


@pytest.mark.parametrize("field,value", [
    ("event_id", "different"), ("queue_sequence", 8), ("source", "other"),
    ("destination", "relay"), ("receiver_node", "relay"), ("event_type", "input"),
    ("payload", 0.30000000000000004), ("payload_bits", "0000000000000000"),
    ("reception_timestamp", math.nextafter(1., math.inf)),
    ("scheduled_delivery_timestamp", 4.0), ("lineage_id", 100),
    ("originating_emission_id", "other"), ("route_path", ["source", "relay"]),
    ("route_depth", 2), ("causal_roots", ["wrong"]), ("roots_truncated", True),
    ("payload_encoding", {"decimal": "0.30", "hex": "0x0.0p+0"}),
])
def test_one_to_one_capture_mutations_block(field, value):
    enqueues, receptions = synthetic_captures()
    receptions[0][field] = value
    with pytest.raises(diagnostic.Blocked):
        diagnostic.reconcile(enqueues, receptions, "relay", "destination")


@pytest.mark.parametrize("mutation", ["missing-enqueue", "missing-reception", "duplicate-enqueue",
                                     "duplicate-reception", "reorder", "duplicate-emission", "truncated"])
def test_capture_missing_duplicates_order_and_truncation_block(mutation):
    enqueues, receptions = synthetic_captures()
    if mutation == "missing-enqueue":
        enqueues.pop()
    elif mutation == "missing-reception":
        receptions.pop()
    elif mutation == "duplicate-enqueue":
        enqueues.append(deepcopy(enqueues[0]))
    elif mutation == "duplicate-reception":
        receptions.append(deepcopy(receptions[0]))
    elif mutation == "reorder":
        receptions.reverse()
    elif mutation == "duplicate-emission":
        receptions[1]["event_id"] = enqueues[1]["event_id"] = enqueues[0]["event_id"]
    else:
        receptions[0]["roots_truncated"] = enqueues[0]["roots_truncated"] = True
    with pytest.raises(diagnostic.Blocked):
        diagnostic.reconcile(enqueues, receptions, "relay", "destination")


def test_raw_signed_zero_bits_are_not_normalized():
    enqueues, receptions = synthetic_captures((-0.0,), (1.,))
    receptions[0]["payload"] = 0.0
    with pytest.raises(diagnostic.Blocked):
        diagnostic.reconcile(enqueues, receptions, "relay", "destination")


def test_destination_schema_adapter_retains_observed_expected_checks_without_mutation():
    record, arrivals = synthetic_destination()
    original = diagnostic.canonical(record)
    updates = diagnostic.destination_updates(record, arrivals)
    result = diagnostic.analyze_sequence("synthetic", arrivals, updates)
    assert diagnostic.canonical(record) == original
    assert result["receptions"] == 2
    checks = result["recurrence_evidence"][1]["retained_trace_checks"]
    assert checks["trace.z_after_input"]["matches"]
    assert checks["evidence.resulting_z"]["residual"] == 0


@pytest.mark.parametrize("section,field,value", [
    ("destination_integration_trace", "decay_rate_z", 0.1),
    ("destination_integration_trace", "theta_z", 0.9),
    ("destination_integration_trace", "theta_e", 0.9),
    ("destination_integration_trace", "timestamp", 2.0),
    ("destination_integration_trace", "elapsed", 3.0),
    ("destination_integration_trace", "input_value", -0.3),
    ("destination_integration_trace", "z_after_decay", .1),
    ("destination_integration_trace", "discharge_amount", 1.0),
    ("destination_integration_trace", "integrated", False),
    ("destination_integration_trace", "mode_before", "S_PENDING"),
    ("destination_integration_trace", "x_after_input", 1.0),
    ("destination_evidence", "resulting_z", 0.31),
    ("destination_evidence", "stream_id", "other"),
    ("destination_evidence", "discharge_decision", True),
])
def test_destination_trace_config_boundaries_block(section, field, value):
    record, arrivals = synthetic_destination()
    record[section][0][field] = value
    with pytest.raises(diagnostic.Blocked):
        diagnostic.destination_updates(record, arrivals)


def test_destination_clipping_and_missing_trace_block():
    record, arrivals = synthetic_destination((4.1,), (1.,))
    with pytest.raises(diagnostic.Blocked, match="clipping"):
        diagnostic.destination_updates(record, arrivals)
    record, arrivals = synthetic_destination()
    record["destination_integration_trace"].pop()
    with pytest.raises(diagnostic.Blocked, match="inventory"):
        diagnostic.destination_updates(record, arrivals)


def sealed(body):
    return {**body, "artifact_digest": diagnostic.digest(body)}


def artifact_identity(value):
    data = diagnostic.canonical(value) + b"\n"
    return data, {"byte_length": len(data), "file_sha256": diagnostic.sha(data),
                  "artifact_digest": value["artifact_digest"]}


def test_artifact_integrity_internal_digest_and_pin_checks():
    value = sealed({"runner_revision": "pinned", "nested": {"payload": -0.5}})
    data, identity = artifact_identity(value)
    assert diagnostic.verify_artifact(data, identity, {"runner_revision": "pinned"}) == value
    with pytest.raises(diagnostic.Blocked, match="pin"):
        diagnostic.verify_artifact(data, identity, {"runner_revision": "tampered"})
    with pytest.raises(diagnostic.Blocked, match="length"):
        diagnostic.verify_artifact(data[:-1], identity, {})
    with pytest.raises(diagnostic.Blocked, match="hash"):
        diagnostic.verify_artifact(data.replace(b"pinned", b"tamped"), identity, {})
    mutated = deepcopy(value)
    mutated["nested"]["payload"] = 0.5
    changed = diagnostic.canonical(mutated)
    with pytest.raises(diagnostic.Blocked, match="internal"):
        diagnostic.verify_artifact(changed, {"byte_length": len(changed), "file_sha256": diagnostic.sha(changed)}, {})
    with pytest.raises(diagnostic.Blocked, match="catalog internal"):
        diagnostic.verify_artifact(data, {**identity, "artifact_digest": "bad"}, {})


@pytest.mark.parametrize("data", [b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}', b'[]', b'{"a":'])
def test_malformed_json_rejected(data):
    with pytest.raises(ValueError):
        diagnostic.parse(data)


def test_missing_inputs_and_catalog_tampering_fail_before_analysis(tmp_path):
    with pytest.raises(diagnostic.Blocked, match="missing"):
        diagnostic.verify_integrity(tmp_path)
    directory = tmp_path / diagnostic.L45
    directory.mkdir(parents=True)
    (directory / "artifact-integrity.json").write_bytes(b"{}")
    with pytest.raises(diagnostic.Blocked, match="catalog hash"):
        diagnostic.verify_integrity(tmp_path)


def test_real_retained_artifacts_integrity_only():
    # No sequence statistics, oracle, scientific summary or output writer invoked.
    result = diagnostic.verify_integrity()
    assert result["status"] == "PASS"
    assert len(result["inputs"]) == 33
    assert result["inputs"][str(diagnostic.L45 / "artifact-integrity.json")]["file_sha256"] == diagnostic.CATALOG_HASH
    assert result["runner44_source_identity"]["git_blob_sha256"] == diagnostic.RUNNER44_GIT_HASH
    assert result["runner44_source_identity"]["retained_execution_bytes_sha256"] != diagnostic.RUNNER44_GIT_HASH


def test_frozen_configuration_integrity_and_tampering():
    config45 = diagnostic.read_json(diagnostic.ROOT / diagnostic.L45 / "config.json")["experiment"]
    config44 = diagnostic.read_json(diagnostic.ROOT / diagnostic.L44 / "config.json")["experiment"]
    assert diagnostic.validate_config(config45, config44) == config45
    mutated = deepcopy(config45)
    mutated["structural_plasticity"] = True
    with pytest.raises(diagnostic.Blocked, match="configuration"):
        diagnostic.validate_config(mutated, config44)


def test_raw_record_inventory_digests_identity_and_replay():
    enqueues, _ = synthetic_captures()
    records = [{"stream_id": "synthetic", "routing_enqueue_events": enqueues}]
    raw = {"phase": "initial", "capture_stream": "enqueue", "arm": diagnostic.CALIBRATED,
           "per_sequence": [{"stream_id": "synthetic", "events": deepcopy(enqueues)}]}
    assert diagnostic.select_raw(raw, records, "initial", "enqueue", diagnostic.CALIBRATED) == [enqueues]
    raw["per_sequence"][0]["events"].pop()
    with pytest.raises(diagnostic.Blocked):
        diagnostic.select_raw(raw, records, "initial", "enqueue", diagnostic.CALIBRATED)


def test_phase_replay_canonical_bytes_and_digests():
    config = {"synthetic_metadata_only": True}
    initial = {"phase": "initial", "arm": "synthetic", "blocker": None,
               "records": [{"stream_id": "synthetic", "payload": -.5}], "report": {}}
    initial["phase_digest"] = diagnostic.sha(diagnostic.phase_bytes(initial, config))
    replay = {**deepcopy(initial), "phase": "replay"}
    summary = {"initial_digests": {"synthetic": initial["phase_digest"]},
               "replay_digests": {"synthetic": initial["phase_digest"]}}
    assert diagnostic.verify_phase_pair(initial, replay, config, summary, "synthetic")["canonical_bytes_equal"]
    replay["records"][0]["payload"] = .5
    with pytest.raises(diagnostic.Blocked, match="digest"):
        diagnostic.verify_phase_pair(initial, replay, config, summary, "synthetic")
    replay["phase_digest"] = diagnostic.sha(diagnostic.phase_bytes(replay, config))
    summary["replay_digests"]["synthetic"] = replay["phase_digest"]
    with pytest.raises(diagnostic.Blocked, match="bytes"):
        diagnostic.verify_phase_pair(initial, replay, config, summary, "synthetic")


def test_depth_comparison_measures_unequal_stream_statistics_and_discloses_unfairness():
    first, _ = synthetic_sequence([.2, .3, -.2], [0., 10., 20.])
    second, _ = synthetic_sequence([.4, .2], [1., 81.])
    fair = {"fixture": True, "sequence": True, "reset": True, "phase": True, "capture": True}
    result = diagnostic.depth_comparison([first], [second], fair, [100.0])
    assert result["fair"]
    assert result["first_hop"]["frequency"]["intervals_per_time"] == .1
    assert result["second_hop"]["frequency"]["intervals_per_time"] == 1 / 80
    assert result["first_hop"]["signs"]["negative"] == 1
    assert result["differences"]["receptions"] == -1
    assert result["first_hop"]["common_fixture_frequency"]["receptions_per_time"] == .03
    assert result["second_hop"]["common_fixture_frequency"]["receptions_per_time"] == .02
    assert result["first_hop"]["timing"]["gaps"] != result["second_hop"]["timing"]["gaps"]
    unfair = diagnostic.depth_comparison([first], [], {**fair, "fixture": False})
    assert not unfair["fair"] and "unfair/missing" in unfair["limitation"]
    assert unfair["second_hop"]["frequency"]["intervals_per_time"] is None


@pytest.mark.parametrize("payloads", [[.4, .4], [.4, -.4], [], [0.0], [1.0]])
def test_optional_critical_rate_not_computed_never_blocks(payloads):
    arrivals, updates = synthetic_sequence(payloads)
    result = diagnostic.analyze_sequence("synthetic", arrivals, updates)
    assert result["critical_rate"]["status"] == "NOT COMPUTED"
    assert "not implemented" in result["critical_rate"]["reason"]


def test_deterministic_bytes_and_no_label_use():
    arrivals, updates = synthetic_sequence([.3, -.2, .6], [0., 10., 30.])
    first = diagnostic.analyze_sequence("synthetic", arrivals, updates)
    for row in updates:
        row["label"] = "ignored-do-not-feed"
    second = diagnostic.analyze_sequence("synthetic", arrivals, updates)
    assert diagnostic.canonical(first) == diagnostic.canonical(second)
    assert "label" not in diagnostic.canonical(second).decode()


def test_module_has_only_standard_library_imports():
    tree = ast.parse(Path(diagnostic.__file__).read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add(node.module.split(".")[0])
    assert imported <= sys.stdlib_module_names | {"__future__"}
    assert not any(name.startswith(("tpcn", "run_luna")) for name in imported)


def test_cli_refuses_overwrite_without_loading_or_analysis(tmp_path, monkeypatch, capsys):
    path = tmp_path / "existing.json"
    path.write_bytes(b"untouched")
    def forbidden():
        pytest.fail("must not load retained analytical inputs")
    monkeypatch.setattr(diagnostic, "offline_analysis", forbidden)
    assert diagnostic.main(["--output", str(path)]) == 2
    assert path.read_bytes() == b"untouched"
    assert "refusing overwrite" in capsys.readouterr().err


def test_cli_explicit_failure_has_no_output(tmp_path, monkeypatch, capsys):
    path = tmp_path / "not-created.json"
    def blocked():
        raise diagnostic.Blocked("synthetic missing required input")
    monkeypatch.setattr(diagnostic, "offline_analysis", blocked)
    assert diagnostic.main(["--output", str(path)]) == 2
    assert not path.exists()
    assert "BLOCKED" in capsys.readouterr().err


def test_cli_n_zero_cannot_write_success(tmp_path, monkeypatch, capsys):
    result = {"verdict": "BLOCKED", "aggregate": {"reason": "N=0"}}
    monkeypatch.setattr(diagnostic, "offline_analysis", lambda: result)
    path = tmp_path / "not-created.json"
    assert diagnostic.main(["--output", str(path)]) == 2
    assert not path.exists() and "N=0" in capsys.readouterr().err


def test_synthetic_output_writer_is_exclusive_and_byte_deterministic(tmp_path):
    path = tmp_path / "synthetic-only.json"
    result = {"schema": "synthetic-test-only", "value": -.2}
    diagnostic.write_output(path, result)
    assert path.read_bytes() == diagnostic.canonical(result) + b"\n"
    with pytest.raises(diagnostic.Blocked, match="overwrite"):
        diagnostic.write_output(path, result)


def test_capacity_and_nonfinite_inputs_block():
    with pytest.raises(diagnostic.Blocked, match="capacity"):
        diagnostic.unique([{"id": i} for i in range(diagnostic.MAX_EVENTS + 1)], "id")
    with pytest.raises(diagnostic.Blocked, match="non-finite"):
        diagnostic.distribution([math.inf])


def test_successful_capture_counter_must_prove_consumption():
    enqueues, receptions = synthetic_captures()
    receptions[0]["receiver_state_transition"]["processed_events_after"] = 0
    with pytest.raises(diagnostic.Blocked, match="consumption"):
        diagnostic.reconcile(enqueues, receptions, "relay", "destination")


def test_publication_preflight_precedes_any_input_processing(monkeypatch):
    called = []
    def fake_git(*args, root=None):
        called.append(args)
        if args[0] == "rev-parse":
            return b"synthetic-implementation\n"
        if args[0] == "branch":
            return diagnostic.BRANCH.encode() + b"\n"
        if args[0] == "status":
            return b""
        if args[0] == "ls-remote":
            return b"unpublished-other-revision refs/heads/synthetic\n"
        pytest.fail("should stop at publication gate")
    monkeypatch.setattr(diagnostic, "git", fake_git)
    monkeypatch.setattr(diagnostic, "verify_integrity", lambda root: pytest.fail("must not read retained inputs"))
    with pytest.raises(diagnostic.Blocked, match="pushed"):
        diagnostic.offline_analysis()
    assert called[-1][0] == "ls-remote"


def test_all_update_difference_includes_final_decay_boundary():
    arrivals, updates = synthetic_sequence([.3], [0.])
    updates.append({"event_id": "late-error", "queue_sequence": 1, "event_type": "prediction_error",
                    "timestamp": 80., "prior_clock": 0., "z_before": .3,
                    "z_after": .3 * math.exp(-1)})
    result = diagnostic.analyze_sequence("synthetic", arrivals, updates)
    assert result["maximum_abs_difference"] == .3 - .3 * math.exp(-1)


def test_assembled_offline_schema_uses_only_synthetic_sequence_records(tmp_path, monkeypatch):
    # Frozen configuration is identity metadata, never an alternate simulation.
    config45 = diagnostic.read_json(diagnostic.ROOT / diagnostic.L45 / "config.json")["experiment"]
    config44 = diagnostic.read_json(diagnostic.ROOT / diagnostic.L44 / "config.json")["experiment"]
    records, historical = [], []
    for seed in range(5):
        for index in range(64):
            stream_id = f"c{seed:02d}-{index:03d}"
            record, arrivals = synthetic_destination((.3,), (1.,))
            record["stream_id"] = stream_id
            record["destination_evidence"][0]["stream_id"] = stream_id
            record.update({
                "arm": diagnostic.CALIBRATED, "destination_decay_rate_z": diagnostic.RATE,
                "seed": seed, "sequence_index": index, "fixture_sequence_sha256": "synthetic",
                "raw_identity": {"synthetic_only": stream_id}, "raw_identity_sha256": "synthetic",
                "input_digest": "synthetic", "point_inputs": [{"t": {"hex": 0.0.hex()}},
                                                            {"t": {"hex": 100.0.hex()}}],
                "neuron_configuration": deepcopy(config45["neuron_configurations"][diagnostic.CALIBRATED]),
                "routing_enqueue_events": [deepcopy(a["raw_enqueue"]) for a in arrivals],
                "receiver_reception_events": [deepcopy(a["raw_reception"]) for a in arrivals],
                "destination_receptions": [deepcopy(a["raw_reception"]) for a in arrivals],
                "relay_emissions": [{"event_id": "e0", "source": "relay", "timestamp": 0.,
                                     "payload": math.atanh(.3), "lineage_id": 0}],
                "settling": {"completed": True}, "relay_state_trajectory": [],
                "routing_capture_sources": {"enqueue": "synthetic", "reception": "synthetic"},
            })
            first_enqueue, first_receive = synthetic_captures((.2,), (1.,), "source", "relay")
            old = {key: deepcopy(record[key]) for key in (
                "stream_id", "seed", "sequence_index", "fixture_sequence_sha256",
                "raw_identity", "raw_identity_sha256", "input_digest",
                "settling", "relay_state_trajectory", "routing_capture_sources")}
            old.update(routing_enqueue_events=first_enqueue, receiver_reception_events=first_receive)
            old["record_digest"] = diagnostic.digest(old)
            records.append(record)
            historical.append(old)
    file_bytes, identities = {}, {}
    def store(path, body):
        artifact = sealed(body)
        data, identity = artifact_identity(artifact)
        file_bytes[tmp_path / path] = data
        identities[str(path)] = identity
    store(diagnostic.L45 / "config.json", {"experiment": config45})
    store(diagnostic.L44 / "config.json", {"experiment": config44})
    store(diagnostic.L44 / "results.json", {"runs": {"CALIBRATED": historical}})
    summary = {"status": "PASS", "verdict": "NOT SUPPORTED IN THIS SETUP",
               "replay_equal": True, "initial_blocker": None, "replay_blocker": None,
               "initial_digests": {}, "replay_digests": {}}
    for phase in ("initial", "replay"):
        for arm in ("DESTINATION_DISABLED", "DESTINATION_DEFAULT", diagnostic.CALIBRATED):
            artifact = {"arm": arm, "phase": phase, "records": records, "report": {}, "blocker": None}
            artifact["phase_digest"] = diagnostic.sha(diagnostic.phase_bytes(artifact, config45))
            summary[f"{phase}_digests"][arm] = artifact["phase_digest"]
            store(diagnostic.L45 / f"{phase}-{arm.lower()}.json", artifact)
        for stream, field in (("enqueue", "routing_enqueue_events"), ("reception", "receiver_reception_events")):
            store(diagnostic.L45 / f"{phase}-destination_calibrated-{stream}.json", {
                "phase": phase, "arm": diagnostic.CALIBRATED, "capture_stream": stream,
                "per_sequence": [{"stream_id": r["stream_id"], "events": r[field]} for r in records],
            })
            per_arm = {"CALIBRATED": [
                {"stream_id": r["stream_id"], "seed": r["seed"], "sequence_index": r["sequence_index"],
                 "capture_status": "completed", "events": r[field], "stream_digest": diagnostic.digest(r[field])}
                for r in historical]}
            store(diagnostic.L44 / f"routing-{phase}-{stream}.json", {
                "phase": phase, "capture_stream": stream, "per_arm": per_arm,
                "streams_digest": diagnostic.digest(per_arm)})
    store(diagnostic.L45 / "summary.json", summary)
    monkeypatch.setattr(diagnostic, "execution_identity", lambda root: {
        "revision": "synthetic-committed-and-published", "sha256": "synthetic", "module": "synthetic"})
    monkeypatch.setattr(diagnostic, "verify_integrity", lambda root: {"status": "PASS", "inputs": identities})
    monkeypatch.setattr(diagnostic, "read_bytes", lambda path: file_bytes[path])
    result = diagnostic.offline_analysis(tmp_path)
    assert result["schema"] == "TPCN-LUNA46-OFFLINE-1"
    assert len(result["sequences"]) == 320
    assert result["aggregate"]["counts"]["DRIVE-LIMITED"] == 320
    assert result["verdict"] == "SUPPORTS DRIVE/CANCELLATION BOTTLENECK"
    assert result["depth_comparison"]["fair"]
    assert result["depth_comparison"]["second_hop"]["common_fixture_frequency"]["exposure"] == 32000.
    assert result["replay"]["analytical_bytes_equal"]
    assert result["feedback"] == "NONE; downstream only"
    assert result["efficacy"] == "NOT EVALUATED"
    assert result["output_digest"] == diagnostic.digest({k: v for k, v in result.items() if k != "output_digest"})
    assert diagnostic.canonical(result) == diagnostic.canonical(diagnostic.offline_analysis(tmp_path))
    assert list(tmp_path.iterdir()) == []
