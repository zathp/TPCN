"""Synthetic analytical tests plus a retained integrity-only check; no science run."""

from __future__ import annotations

import ast
from copy import deepcopy
import math
import os
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
                         "timestamp": timestamp, "payload": payload,
                         "causal_roots": [f"root{index}"], "roots_truncated": False})
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
                                     "duplicate-reception", "reorder", "duplicate-emission"])
def test_capture_missing_duplicates_and_order_block(mutation):
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
    with pytest.raises(diagnostic.Blocked):
        diagnostic.reconcile(enqueues, receptions, "relay", "destination")


def test_matching_true_roots_metadata_preserved_and_reported_without_changing_oracles():
    record, arrivals = synthetic_destination()
    unflagged = diagnostic.analyze_sequence(
        "synthetic", arrivals, diagnostic.destination_updates(record, arrivals))
    enqueue = [deepcopy(row["raw_enqueue"]) for row in arrivals]
    received = [deepcopy(row["raw_reception"]) for row in arrivals]
    enqueue[0]["roots_truncated"] = received[0]["roots_truncated"] = True
    before = diagnostic.canonical([enqueue, received])
    flagged = diagnostic.reconcile(enqueue, received, "relay", "destination")
    assert diagnostic.canonical([enqueue, received]) == before
    assert [row["roots_truncated"] for row in flagged] == [True, False]
    assert flagged[0]["causal_roots"] == enqueue[0]["causal_roots"]
    result = diagnostic.analyze_sequence("synthetic", flagged, record["destination_state_trajectory"])
    assert result["roots_truncated_metadata"]["true_count"] == 1
    assert result["roots_truncated_metadata"]["false_count"] == 1
    assert result["roots_truncated_metadata"]["true_fraction"] == .5
    assert result["recurrence_evidence"][0]["roots_truncated"] is True
    assert result["recurrence_evidence"][0]["causal_roots"] == enqueue[0]["causal_roots"]
    for key in ("actual", "zero_decay", "category", "actual_crosses", "zero_crosses"):
        assert result[key] == unflagged[key]
    combined = diagnostic.aggregate([result, diagnostic.analyze_sequence("empty", [], [])])
    assert combined["roots_truncated_metadata"]["true_count"] == 1
    assert combined["roots_truncated_metadata"]["false_count"] == 1
    assert combined["roots_truncated_metadata"]["true_fraction"] == .5
    assert combined["sequences_with_roots_truncated"] == 1
    assert diagnostic.analyze_sequence("empty", [], [])["roots_truncated_metadata"]["true_fraction"] is None
    assert diagnostic.stream_metrics([flagged])["roots_truncated_metadata"]["true_count"] == 1


@pytest.mark.parametrize("enqueue_flag,reception_flag", [(True, False), (False, True)])
def test_roots_truncated_capture_site_mismatch_blocks(enqueue_flag, reception_flag):
    enqueues, receptions = synthetic_captures()
    enqueues[0]["roots_truncated"] = enqueue_flag
    receptions[0]["roots_truncated"] = reception_flag
    with pytest.raises(diagnostic.Blocked, match="raw capture identity differs: roots_truncated"):
        diagnostic.reconcile(enqueues, receptions, "relay", "destination")


@pytest.mark.parametrize("invalid", [0, 1, None, "true"])
def test_matching_nonboolean_roots_metadata_blocks(invalid):
    enqueues, receptions = synthetic_captures()
    enqueues[0]["roots_truncated"] = receptions[0]["roots_truncated"] = invalid
    with pytest.raises(diagnostic.Blocked, match="invalid roots_truncated"):
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


def test_luna51_catalog_identity_is_pinned_to_the_expected_git_object():
    canonical_bytes = diagnostic.git(
        "show",
        f"{diagnostic.CATALOG_REVISION}:{diagnostic.CATALOG_GIT_PATH}",
    )
    checkout = diagnostic.read_bytes(diagnostic.ROOT / diagnostic.CATALOG_PATH)

    catalog, identity = diagnostic.verify_catalog_identity(
        diagnostic.ROOT, checkout
    )

    assert catalog["file_count"] == 22
    assert identity["git_revision"] == diagnostic.CATALOG_REVISION
    assert identity["git_blob"] == diagnostic.CATALOG_GIT_BLOB
    assert identity["file_sha256"] == diagnostic.CATALOG_HASH
    assert identity["checkout_materialization"] in {
        "exact",
        "exact-Git-LF-to-CRLF-checkout",
    }
    crlf_catalog, crlf_identity = diagnostic.verify_catalog_identity(
        diagnostic.ROOT,
        canonical_bytes.replace(b"\n", b"\r\n"),
    )
    assert crlf_catalog == catalog
    assert crlf_identity["checkout_materialization"] == (
        "exact-Git-LF-to-CRLF-checkout"
    )
    assert diagnostic.verify_catalog_checkout(
        canonical_bytes, canonical_bytes
    ) == "exact"
    assert diagnostic.verify_catalog_checkout(
        canonical_bytes.replace(b"\n", b"\r\n"), canonical_bytes
    ) == "exact-Git-LF-to-CRLF-checkout"

    with pytest.raises(diagnostic.Blocked, match="revision differs"):
        diagnostic.verify_catalog_identity(
            diagnostic.ROOT,
            checkout,
            revision="HEAD",
        )
    with pytest.raises(diagnostic.Blocked, match="Git object differs"):
        diagnostic.verify_catalog_identity(
            diagnostic.ROOT,
            checkout,
            expected_blob="0" * 40,
        )


@pytest.mark.parametrize(
    "mutate",
    [
        lambda data: data.replace(b'"file_count":22', b'"file_count":23', 1),
        lambda data: data + b" ",
        lambda data: data[:-2] + b"\n",
        lambda data: data.replace(b"\n", b"\r\n") + b"\n",
        lambda data: data.rstrip(b"\n"),
    ],
    ids=[
        "changed-content",
        "added-whitespace",
        "removed-content",
        "extra-newline-at-eof",
        "newline-at-eof",
    ],
)
def test_luna51_catalog_checkout_rejects_every_nonexact_mutation(mutate):
    canonical_bytes = diagnostic.git(
        "show",
        f"{diagnostic.CATALOG_REVISION}:{diagnostic.CATALOG_GIT_PATH}",
    )

    with pytest.raises(diagnostic.Blocked, match="beyond line endings"):
        diagnostic.verify_catalog_checkout(mutate(canonical_bytes), canonical_bytes)


def test_luna51_catalog_checkout_rejects_mixed_line_endings():
    canonical_bytes = b'{\n  "key": 1\n}\n'
    mixed = b'{\r\n  "key": 1\n}\r\n'

    with pytest.raises(diagnostic.Blocked, match="beyond line endings"):
        diagnostic.verify_catalog_checkout(mixed, canonical_bytes)


def test_luna51_exact_intentional_crlf_object_is_not_rewritten():
    canonical_bytes = b'{\r\n  "key": 1\r\n}\r\n'

    assert diagnostic.verify_git_text_checkout(
        canonical_bytes, canonical_bytes, "synthetic content differs"
    ) == "exact"
    with pytest.raises(diagnostic.Blocked, match="canonical LF text"):
        diagnostic.verify_git_text_checkout(
            canonical_bytes.replace(b"\r\n", b"\n"),
            canonical_bytes,
            "synthetic content differs",
        )


def test_luna51_catalog_entries_accept_only_their_exact_checkout_transform():
    body = {"schema": "synthetic", "payload": "historical"}
    value = {**body, "artifact_digest": diagnostic.digest(body)}
    canonical_bytes = diagnostic.canonical(value) + b"\n"
    identity = {
        "byte_length": len(canonical_bytes),
        "file_sha256": diagnostic.sha(canonical_bytes),
    }

    assert diagnostic.verify_artifact(
        canonical_bytes.replace(b"\n", b"\r\n"),
        identity,
        {},
        canonical_bytes=canonical_bytes,
    ) == value
    with pytest.raises(diagnostic.Blocked, match="artifact checkout bytes differ"):
        diagnostic.verify_artifact(
            canonical_bytes.replace(b"historical", b"substituted"),
            identity,
            {},
            canonical_bytes=canonical_bytes,
        )


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
    first_intervals = result["first_hop"]["interval_statistics"]
    second_intervals = result["second_hop"]["interval_statistics"]
    assert first_intervals["interval_count"] == 2
    assert first_intervals["observed_duration"] == 20.
    assert first_intervals["mean_interval_duration"] == 10.
    assert first_intervals["reciprocal_mean_interval"] == .1
    assert first_intervals["reciprocal_mean_interval_units"] == "intervals per retained logical-time unit"
    assert "not an event rate" in first_intervals["definition"]
    assert second_intervals["interval_count"] == 1
    assert second_intervals["observed_duration"] == 80.
    assert second_intervals["mean_interval_duration"] == 80.
    assert second_intervals["reciprocal_mean_interval"] == 1 / 80
    tied, _ = synthetic_sequence([.2, .3], [5., 5.])
    tied_intervals = diagnostic.stream_metrics([tied])["interval_statistics"]
    assert tied_intervals["interval_count"] == 1
    assert tied_intervals["observed_duration"] == 0.
    assert tied_intervals["mean_interval_duration"] == 0.
    assert tied_intervals["reciprocal_mean_interval"] is None
    singleton, _ = synthetic_sequence([.2], [5.])
    singleton_intervals = diagnostic.stream_metrics([singleton])["interval_statistics"]
    assert singleton_intervals["interval_count"] == 0
    assert singleton_intervals["mean_interval_duration"] is None
    assert singleton_intervals["reciprocal_mean_interval"] is None
    assert result["first_hop"]["signs"]["negative"] == 1
    assert result["differences"]["receptions"] == -1
    first_event_rate = result["first_hop"]["common_fixture_event_rate"]
    second_event_rate = result["second_hop"]["common_fixture_event_rate"]
    assert first_event_rate["event_count"] == 3
    assert first_event_rate["observation_window_duration"] == 100.
    assert first_event_rate["events_per_time_unit"] == .03
    assert first_event_rate["units"] == "routed receptions per retained logical-time unit"
    assert "reception count /" in first_event_rate["definition"]
    assert second_event_rate["event_count"] == 2
    assert second_event_rate["observation_window_duration"] == 100.
    assert second_event_rate["events_per_time_unit"] == .02
    assert result["first_hop"]["timing"]["gaps"] != result["second_hop"]["timing"]["gaps"]
    unfair = diagnostic.depth_comparison([first], [], {**fair, "fixture": False})
    assert not unfair["fair"] and "unfair/missing" in unfair["limitation"]
    assert unfair["second_hop"]["interval_statistics"]["reciprocal_mean_interval"] is None
    assert unfair["second_hop"]["common_fixture_event_rate"]["events_per_time_unit"] is None


# Contract-to-test matrix (luna-46.agent.md critical-rate clause and checklist):
# A unique finite (same-sign, verified bisection); B drive-limited/no crossing at any
# rate; C already-crossing; D zero-decay endpoint; E non-monotone/multiple (mixed sign,
# no root selected); F signed cancellation (no zero-decay root); G singleton/no recurrence.
CRITICAL_MATRIX = [
    ("A-unique", [0.6, 0.6], [0.0, 80.0], "TEMPORAL-RETENTION-LIMITED", "UNIQUE"),
    ("B-drive", [0.2, 0.3], [0.0, 80.0], "DRIVE-LIMITED", "ABSENT: NO CROSSING AT ANY NONNEGATIVE RATE"),
    ("B-drive-mixed", [0.2, -0.3], [0.0, 80.0], "DRIVE-LIMITED", "ABSENT: NO CROSSING AT ANY NONNEGATIVE RATE"),
    ("C-already", [0.5, 0.5], [0.0, 0.0], "ALREADY-CROSSING", "NOT APPLICABLE: ALREADY-CROSSING"),
    ("D-zero-boundary", [0.5, 0.5], [0.0, 80.0], "TEMPORAL-RETENTION-LIMITED", "ZERO-BOUNDARY"),
    ("E-non-monotone", [0.6, -0.1, 0.6], [0.0, 40.0, 80.0], "TEMPORAL-RETENTION-LIMITED",
     "NOT COMPUTED: NON-MONOTONE SIGNED"),
    ("F-cancellation", [0.6, -0.6], [0.0, 0.0], "CANCELLATION-LIMITED", "NOT APPLICABLE: NO ZERO-DECAY CROSSING"),
    ("G-singleton", [0.3], [0.0], "DRIVE-LIMITED", "NO FINITE CRITICAL RATE: SINGLETON"),
    ("G-singleton-zero", [0.0], [0.0], "DRIVE-LIMITED", "NO FINITE CRITICAL RATE: SINGLETON"),
    ("G-no-receptions", [], [], "NO-RECEPTIONS", "NOT APPLICABLE: NO RECEPTIONS"),
]


@pytest.mark.parametrize("case,payloads,times,category,status", CRITICAL_MATRIX,
                         ids=[row[0] for row in CRITICAL_MATRIX])
def test_critical_rate_contract_matrix(case, payloads, times, category, status):
    arrivals, updates = synthetic_sequence(payloads, times)
    result = diagnostic.analyze_sequence("synthetic", arrivals, updates)
    assert result["category"] == category  # classification unchanged by critical-rate analysis
    critical = result["critical_rate"]
    assert critical["status"] == status
    assert critical["status"] in diagnostic.CRITICAL_RATE_POLICY["statuses"]
    if status == "UNIQUE":
        assert 0 < critical["critical_rate"] < diagnostic.RATE
    elif status == "ZERO-BOUNDARY":
        assert critical["critical_rate"] == 0.0 and critical["F_zero"] == 1.0
    else:
        assert critical["critical_rate"] is None  # never fabricated


def test_critical_rate_a_unique_matches_closed_form_and_predeclared_verification():
    arrivals, updates = synthetic_sequence([0.6, 0.6], [0.0, 80.0])
    critical = diagnostic.analyze_sequence("synthetic", arrivals, updates)["critical_rate"]
    tolerance = diagnostic.CRITICAL_SOLVER_TOLERANCE
    assert tolerance == 64 * sys.float_info.epsilon * diagnostic.RATE
    root = critical["critical_rate"]
    assert root == pytest.approx(math.log(1.5) / 80, rel=1e-12, abs=0)
    checks = critical["verification"]
    assert checks["iterations"] <= diagnostic.CRITICAL_SOLVER_ITERATIONS
    lo, hi = checks["bracket"]
    assert lo == root and hi - lo <= tolerance
    assert checks["residual"]["matches"] and checks["residual"]["expected"] == 1.0
    assert checks["below"]["rate"] == root - tolerance and checks["below"]["crosses"]
    assert checks["above"]["rate"] == root + tolerance and not checks["above"]["crosses"]
    steps = [(0.0, 0.6), (80.0, 0.6)]
    assert diagnostic.signed_maximum(steps, 0.0) == 1.2
    assert diagnostic.signed_maximum(steps, diagnostic.RATE) == 0.6 * math.exp(-1) + 0.6


def test_critical_rate_unique_with_intervening_update_uses_all_retained_boundaries():
    arrivals, updates = synthetic_sequence([0.4, 0.2, 0.5], [0.0, 30.0, 80.0])
    result = diagnostic.analyze_sequence("synthetic", arrivals, updates)
    assert result["category"] == "TEMPORAL-RETENTION-LIMITED"
    assert result["critical_rate"]["status"] == "UNIQUE"
    root = result["critical_rate"]["critical_rate"]
    steps = [(0.0, 0.4), (30.0, 0.2), (50.0, 0.5)]
    assert diagnostic.signed_maximum(steps, root) >= 1.0 > diagnostic.signed_maximum(
        steps, root + diagnostic.CRITICAL_SOLVER_TOLERANCE)


@pytest.mark.parametrize("case", ["B-drive", "C-already", "E-non-monotone", "F-cancellation",
                                  "G-singleton", "G-no-receptions"])
def test_critical_rate_non_unique_cases_never_evaluate_or_select_a_root(case, monkeypatch):
    _, payloads, times, _, _ = next(row for row in CRITICAL_MATRIX if row[0] == case)
    arrivals, updates = synthetic_sequence(payloads, times)
    monkeypatch.setattr(diagnostic, "signed_maximum",
                        lambda steps, rate: pytest.fail("no solver for non-unique/absent cases"))
    assert diagnostic.analyze_sequence("synthetic", arrivals, updates)["critical_rate"]["critical_rate"] is None


def test_critical_rate_inconsistent_bracket_reports_failure_not_estimate():
    steps = [(0.0, 0.3), (80.0, 0.3)]  # zero-decay does not cross: bracket invalid
    critical = diagnostic.critical_rate("TEMPORAL-RETENTION-LIMITED", steps, [0.3, 0.3])
    assert critical["status"] == "NOT COMPUTED: VERIFICATION FAILED"
    assert critical["critical_rate"] is None
    with pytest.raises(diagnostic.Blocked):
        diagnostic.critical_rate("UNKNOWN", steps, [0.3, 0.3])


def test_critical_rate_policy_is_analytical_only_and_aggregated():
    policy = diagnostic.POLICY["critical_rate"]
    assert policy is diagnostic.CRITICAL_RATE_POLICY
    assert "ANALYTICAL ONLY" in policy["scope"] and "not production tuning" in policy["scope"]
    rows = [diagnostic.analyze_sequence(case, *synthetic_sequence(p, t)) for case, p, t, _, _ in CRITICAL_MATRIX]
    counts = diagnostic.aggregate(rows)["critical_rate_status_counts"]
    assert counts["UNIQUE"] == 1 and counts["ABSENT: NO CROSSING AT ANY NONNEGATIVE RATE"] == 2
    assert sum(counts.values()) == len(CRITICAL_MATRIX)


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
    # Sole non-stdlib import: the authoritative fixture path constant from the verifier.
    assert imported <= sys.stdlib_module_names | {"__future__", "scripts"}
    assert not any(name.startswith(("tpcn", "run_luna")) for name in imported)
    from scripts import verify_luna44_canonical_fixture as verifier
    verifier_tree = ast.parse(Path(verifier.__file__).read_text(encoding="utf-8"))
    verifier_imports = {alias.name.split(".")[0] for node in ast.walk(verifier_tree)
                        if isinstance(node, ast.Import) for alias in node.names}
    verifier_imports |= {node.module.split(".")[0] for node in ast.walk(verifier_tree)
                         if isinstance(node, ast.ImportFrom)}
    assert verifier_imports <= sys.stdlib_module_names | {"__future__"}
    assert diagnostic.FIXTURE_ROOT == Path(verifier.EXPECTED_FIXTURE_PATH).parent


def guard_root(tmp_path):
    """Synthetic repository layout; never touches the real artifacts tree."""
    fixture = tmp_path / diagnostic.FIXTURE_ROOT
    fixture.mkdir(parents=True)
    (fixture / "fixture.json").write_bytes(b"frozen")
    namespace = tmp_path / "artifacts" / "luna46-test"
    namespace.mkdir()
    return fixture, namespace


@pytest.mark.parametrize("relative", [
    "artifacts/luna44-canonical-fixture",                         # exact
    "artifacts/luna44-canonical-fixture/fixture.json",            # child (existing file)
    "artifacts/luna44-canonical-fixture/new.json",                # child
    "artifacts/luna44-canonical-fixture/a/b/new.json",            # nested
    "artifacts/luna46-test/../luna44-canonical-fixture/new.json", # '..' escape
    "artifacts/luna46-test/./../luna44-canonical-fixture",        # '..' exact
    "artifacts",                                                  # broad parent (inverse)
    ".",                                                          # repository root (inverse)
    "artifacts/luna45-acp0008-depth2-destination-integration-20261006/new.json",
    "artifacts/luna44-acp0008-independent-routing-rerun-20261005/new.json",
    "artifacts/luna45-corrective-verification-20261006-r1/new.json",
])
def test_output_guard_rejects_fixture_and_evidence_overlap(tmp_path, relative):
    guard_root(tmp_path)
    with pytest.raises(diagnostic.Blocked, match="overlaps"):
        diagnostic.validate_output_path(tmp_path / relative, tmp_path)


def test_output_guard_rejects_relative_alias_from_cwd(tmp_path, monkeypatch):
    guard_root(tmp_path)
    monkeypatch.chdir(tmp_path / "artifacts" / "luna46-test")
    with pytest.raises(diagnostic.Blocked, match="frozen Luna44 fixture"):
        diagnostic.validate_output_path(Path("../luna44-canonical-fixture/new.json"), tmp_path)
    accepted = diagnostic.validate_output_path(Path("new.json"), tmp_path)
    assert accepted == (tmp_path / "artifacts" / "luna46-test" / "new.json").resolve()


@pytest.mark.parametrize("relative", ["outside.json", "artifacts/new.json", "artifacts/luna47-x/new.json",
                                      "artifacts/xluna46-x.json", "artifacts/luna46-test/../new.json",
                                      "artifacts-luna46-x/new.json"])
def test_output_guard_requires_luna46_namespace(tmp_path, relative):
    guard_root(tmp_path)
    with pytest.raises(diagnostic.Blocked, match="outside artifacts/luna46-"):
        diagnostic.validate_output_path(tmp_path / relative, tmp_path)


@pytest.mark.parametrize("relative", ["artifacts/luna46-test/out.json", "artifacts/luna46-new.json",
                                      "artifacts/luna46-test/nested/out.json"])
def test_output_guard_accepts_canonical_namespace(tmp_path, relative):
    guard_root(tmp_path)
    assert diagnostic.validate_output_path(tmp_path / relative, tmp_path) == (tmp_path / relative).resolve()


def test_output_guard_temporary_directory_outside_namespace_rejected(tmp_path, tmp_path_factory):
    guard_root(tmp_path)
    elsewhere = tmp_path_factory.mktemp("elsewhere") / "out.json"
    with pytest.raises(diagnostic.Blocked, match="outside"):
        diagnostic.validate_output_path(elsewhere, tmp_path)


def make_directory_alias(link, target, kind):
    if kind == "symlink":
        try:
            os.symlink(target, link, target_is_directory=True)
        except (OSError, NotImplementedError) as error:
            pytest.skip(f"directory symlink unsupported: {error}")
    else:
        try:
            import _winapi
            _winapi.CreateJunction(str(target), str(link))
        except (ImportError, AttributeError, OSError) as error:
            pytest.skip(f"junction unsupported: {error}")


@pytest.mark.parametrize("kind", ["symlink", "junction"])
def test_output_guard_resolves_directory_aliases_to_fixture(tmp_path, kind):
    fixture, _ = guard_root(tmp_path)
    alias = tmp_path / "artifacts" / "luna46-alias"
    make_directory_alias(alias, fixture, kind)
    assert (alias / "fixture.json").read_bytes() == b"frozen"
    with pytest.raises(diagnostic.Blocked, match="frozen Luna44 fixture"):
        diagnostic.validate_output_path(alias / "new.json", tmp_path)
    with pytest.raises(diagnostic.Blocked, match="frozen Luna44 fixture"):
        diagnostic.validate_output_path(alias, tmp_path)
    outer = tmp_path / "outer-alias"
    make_directory_alias(outer, tmp_path / "artifacts", kind)
    with pytest.raises(diagnostic.Blocked, match="frozen Luna44 fixture"):
        diagnostic.validate_output_path(outer / "luna44-canonical-fixture" / "x.json", tmp_path)
    assert (fixture / "fixture.json").read_bytes() == b"frozen"


def test_output_guard_on_real_repository_layout_without_writing():
    root = diagnostic.ROOT
    before = sorted(p.name for p in (root / "artifacts").iterdir())
    accepted = root / "artifacts" / "luna46-test" / "never-written.json"
    assert diagnostic.validate_output_path(accepted) == accepted.resolve()
    for path in (root / diagnostic.FIXTURE_ROOT, root / diagnostic.FIXTURE_ROOT / "fixture.json",
                 root / "artifacts", root):
        with pytest.raises(diagnostic.Blocked, match="overlaps"):
            diagnostic.validate_output_path(path)
    assert sorted(p.name for p in (root / "artifacts").iterdir()) == before


def cli_namespace(tmp_path, monkeypatch):
    _, namespace = guard_root(tmp_path)
    monkeypatch.setattr(diagnostic, "ROOT", tmp_path)
    return namespace


def test_cli_refuses_overwrite_without_loading_or_analysis(tmp_path, monkeypatch, capsys):
    path = cli_namespace(tmp_path, monkeypatch) / "existing.json"
    path.write_bytes(b"untouched")
    def forbidden():
        pytest.fail("must not load retained analytical inputs")
    monkeypatch.setattr(diagnostic, "offline_analysis", forbidden)
    assert diagnostic.main(["--output", str(path)]) == 2
    assert path.read_bytes() == b"untouched"
    assert "refusing overwrite" in capsys.readouterr().err


def test_cli_refuses_retained_luna46_output_without_analysis(monkeypatch, capsys):
    retained = diagnostic.ROOT / "artifacts" / "luna46-depth-scaling-diagnostic-20261006.json"
    before = retained.read_bytes()
    monkeypatch.setattr(diagnostic, "offline_analysis", lambda: pytest.fail("no analysis"))
    assert diagnostic.main(["--output", str(retained)]) == 2
    assert retained.read_bytes() == before
    assert "refusing overwrite" in capsys.readouterr().err


@pytest.mark.parametrize("relative", ["artifacts/luna44-canonical-fixture/new.json",
                                      "artifacts/luna46-test/../luna44-canonical-fixture/new.json",
                                      "outside.json"])
def test_cli_output_guard_blocks_before_analysis(tmp_path, monkeypatch, capsys, relative):
    cli_namespace(tmp_path, monkeypatch)
    monkeypatch.setattr(diagnostic, "offline_analysis", lambda: pytest.fail("no analysis"))
    assert diagnostic.main(["--output", str(tmp_path / relative)]) == 2
    assert not (tmp_path / relative).exists()
    assert sorted(p.name for p in (tmp_path / diagnostic.FIXTURE_ROOT).iterdir()) == ["fixture.json"]
    assert "BLOCKED" in capsys.readouterr().err


def test_cli_missing_output_parent_blocks(tmp_path, monkeypatch, capsys):
    namespace = cli_namespace(tmp_path, monkeypatch)
    monkeypatch.setattr(diagnostic, "offline_analysis", lambda: pytest.fail("no analysis"))
    assert diagnostic.main(["--output", str(namespace / "missing" / "out.json")]) == 2
    assert "parent directory missing" in capsys.readouterr().err


def test_cli_explicit_failure_has_no_output(tmp_path, monkeypatch, capsys):
    path = cli_namespace(tmp_path, monkeypatch) / "not-created.json"
    def blocked():
        raise diagnostic.Blocked("synthetic missing required input")
    monkeypatch.setattr(diagnostic, "offline_analysis", blocked)
    assert diagnostic.main(["--output", str(path)]) == 2
    assert not path.exists()
    assert "BLOCKED" in capsys.readouterr().err


def test_cli_n_zero_cannot_write_success(tmp_path, monkeypatch, capsys):
    result = {"verdict": "BLOCKED", "aggregate": {"reason": "N=0"}}
    monkeypatch.setattr(diagnostic, "offline_analysis", lambda: result)
    path = cli_namespace(tmp_path, monkeypatch) / "not-created.json"
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
    second_hop = result["depth_comparison"]["second_hop"]
    assert second_hop["common_fixture_event_rate"]["observation_window_duration"] == 32000.
    assert second_hop["common_fixture_event_rate"]["event_count"] == 320
    assert second_hop["common_fixture_event_rate"]["events_per_time_unit"] == .01
    assert second_hop["interval_statistics"]["interval_count"] == 0
    assert second_hop["interval_statistics"]["reciprocal_mean_interval"] is None
    assert result["replay"]["analytical_bytes_equal"]
    assert result["feedback"] == "NONE; downstream only"
    assert result["efficacy"] == "NOT EVALUATED"
    assert result["output_digest"] == diagnostic.digest({k: v for k, v in result.items() if k != "output_digest"})
    assert diagnostic.canonical(result) == diagnostic.canonical(diagnostic.offline_analysis(tmp_path))
    assert list(tmp_path.iterdir()) == []
