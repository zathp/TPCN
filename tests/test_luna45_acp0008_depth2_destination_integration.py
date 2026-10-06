from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
from dataclasses import asdict

import pytest

import run_luna45_acp0008_depth2_destination_integration as luna45
from tpcn.excursion_neuron import E1Config, IntegrationConfig, MultiExcursionNeuron
from tpcn.event_runtime import Event, EventType


def sequence(values=((0.0, 3.8, 0.0),)):
    points = []
    batch = -1
    prior = None
    for index, (timestamp, x, y) in enumerate(values):
        if prior is None or timestamp != prior:
            batch += 1
        points.append({
            "seed": 0, "sequence_index": 0, "stream_id": "c00-000",
            "point_index": index, "batch_ordinal": batch,
            "x": luna45.reference._float_record(x),
            "y": luna45.reference._float_record(y),
            "t": luna45.reference._float_record(timestamp),
            "audit_x_plus_y": luna45.reference._float_record(x + y),
        })
        prior = timestamp
    result = {
        "seed": 0, "sequence_index": 0, "stream_id": "c00-000",
        "point_count": len(points), "points": points,
    }
    result["source_sha256"] = luna45.digest(luna45.reference._sequence_raw_rows(result))
    return result


@pytest.fixture(scope="module")
def simple_runs():
    return {arm: [luna45.run_character(arm, sequence())] for arm in luna45.ARMS}


@pytest.fixture(scope="module")
def integrated_record():
    # Unit mechanism stimulus, not a retained task experiment or calibration.
    stimulus = sequence(tuple((6.0 * index, 3.8, 0.0) for index in range(10)))
    record = luna45.run_character(luna45.ARMS[2], stimulus)
    luna45.destination_evidence(record)
    return record


def history_of(record):
    result = deepcopy(record)
    result["record_digest"] = "unit-history"
    return result


def test_config_only_varies_destination_and_freezes_all_bounds():
    config = luna45.experiment_config()
    assert config["gate_order"] == ["G1", "G2", "G3", "G4", "DESTINATION", "REPLAY"]
    assert not config["structural_plasticity"]
    nodes = config["neuron_configurations"]
    for arm in luna45.ARMS:
        assert nodes[arm]["source"]["integration"] is None
        assert nodes[arm]["relay"]["integration"]["decay_rate_z"] == 0.0125
        assert nodes[arm]["destination"]["theta_e"] == 1.0
        stripped = deepcopy(nodes[arm])
        stripped["destination"]["integration"] = None
        baseline = deepcopy(nodes[luna45.ARMS[0]])
        assert stripped == baseline
    assert nodes[luna45.ARMS[0]]["destination"]["integration"] is None
    assert nodes[luna45.ARMS[1]]["destination"]["integration"]["decay_rate_z"] == 0.1
    assert nodes[luna45.ARMS[2]]["destination"]["integration"]["decay_rate_z"] == 0.0125
    assert config["runtime"] == {
        "neuron_event_budget": 4096, "queue_capacity": 128,
        "runtime_event_budget": 1024, "max_activity_events": 1024,
        "settling_horizon": 4.0, "prediction_capacity": 8,
        "prediction_expiry": 4.0, "eligibility_capacity_per_ledger": 1024,
        "neutral_reward": 0.0,
    }
    assert config["topology"]["edges"] == [
        {"source": "source", "destination": "relay", "delay": 1.0, "w": 1.0, "d": 1.0, "r": 0.0},
        {"source": "relay", "destination": "destination", "delay": 1.0, "w": 1.0, "d": 1.0, "r": 0.0},
    ]


def test_frozen_inputs_forbid_generation_calls_but_allow_transitive_benchmark_import():
    fixture, manifest = luna45.load_inputs()
    assert len(fixture["sequences"]) == 320
    assert sum(item["point_count"] for item in fixture["sequences"]) == 5164
    assert manifest["fixture_byte_length"] == 3451453
    assert luna45.file_hash(luna45.reference.FIXTURE_PATH) == luna45.reference.FIXTURE_FILE_SHA256
    assert len(manifest["source_files"]) == 4
    # Production package imports are allowed; scientific generation is not.
    code = """
import importlib.abc
import sys
from unittest import mock
import run_luna45_acp0008_depth2_destination_integration as r
import tpcn
import tpcn.spiral_benchmark as benchmark

dedicated = ('run_luna34_excursion_v1_multi_emitter_bridge',
             'scripts.build_luna44_canonical_fixture')
class NoDedicatedGeneratorImport(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname in dedicated:
            raise AssertionError('dedicated generator import: ' + fullname)
        return None

def forbidden(*args, **kwargs):
    raise AssertionError('generation entrypoint called')

entrypoints = ('generate_spiral', 'make_spiral_dataset', 'generate_matched_pair',
              'generate_traversal_pair', 'generate_variant')
originals = {getattr(benchmark, name) for name in entrypoints}
sys.meta_path.insert(0, NoDedicatedGeneratorImport())
from contextlib import ExitStack
with ExitStack() as stack:
    for module in tuple(sys.modules.values()):
        if module is None:
            continue
        for name, value in tuple(vars(module).items()):
            if any(value is function for function in originals):
                stack.enter_context(mock.patch.object(module, name, forbidden))
    for module_name, names in (
        (dedicated[0], ('_training_point_sequences',)),
        (dedicated[1], ('_build_fixture', '_materialize_worker',
                        'materialize_independently', 'main')),
    ):
        module = sys.modules.get(module_name)
        if module is not None:
            for name in names:
                if hasattr(module, name):
                    stack.enter_context(mock.patch.object(module, name, forbidden))
    fixture, manifest = r.load_inputs()
    assert r.file_hash(r.reference.FIXTURE_PATH) == r.reference.FIXTURE_FILE_SHA256
    assert r.digest([row for s in fixture['sequences']
                     for row in r.reference._sequence_raw_rows(s)]) == r.reference.FIXTURE_SHA256
    synthetic = {'seed': 0, 'sequence_index': 0, 'stream_id': 'c00-000',
                 'point_count': 1, 'points': [{
        'seed': 0, 'sequence_index': 0, 'stream_id': 'c00-000',
        'point_index': 0, 'batch_ordinal': 0,
        'x': r.reference._float_record(3.8), 'y': r.reference._float_record(0.0),
        't': r.reference._float_record(0.0),
        'audit_x_plus_y': r.reference._float_record(3.8)}]}
    synthetic['source_sha256'] = r.digest(r.reference._sequence_raw_rows(synthetic))
    for arm in r.ARMS:
        record = r.run_character(arm, synthetic)
        assert record['raw_identity_sha256'] == synthetic['source_sha256']
    assert all(name not in sys.modules for name in dedicated)
    for name in entrypoints:
        assert getattr(benchmark, name) is forbidden
"""
    completed = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_frozen_loader_rejects_byte_length_mismatch(monkeypatch):
    monkeypatch.setattr(Path, "stat", lambda self: type("Stat", (), {"st_size": 1})())
    with pytest.raises(luna45.Blocker, match="byte length"):
        luna45.load_inputs()


def test_authorization_handoff_checkout_and_git_blob_have_separate_exact_pins():
    working = luna45.HANDOFF.read_bytes()
    committed = subprocess.run(
        ["git", "show", f"{luna45.BASELINE}:{luna45.HANDOFF.as_posix()}"],
        check=True, capture_output=True,
    ).stdout
    assert hashlib.sha256(working).hexdigest() == luna45.HANDOFF_SHA256
    assert hashlib.sha256(committed).hexdigest() == luna45.HANDOFF_COMMITTED_SHA256
    assert working != committed
    assert working.replace(b"\r\n", b"\n") == committed


def test_historical_evidence_identity_and_actual_capture_files():
    records, identity = luna45.load_history()
    assert len(records) == identity["records"] == 320
    assert sum(len(item["source_emissions"]) for item in records) == 1715
    assert sum(len(item["relay_emissions"]) for item in records) == 235
    assert identity["runner_revision"] == luna45.HISTORY_REVISION
    assert identity["files"] == luna45.HISTORY_FILES


def test_history_pin_failure_is_blocking(monkeypatch):
    monkeypatch.setattr(luna45, "file_hash", lambda path: "wrong")
    with pytest.raises(luna45.Blocker, match="historical file pin"):
        luna45.load_history()


def test_float_policy_does_not_waive_exact_fields():
    check = luna45.compare_historical({"payload": 0.5}, {"payload": math.nextafter(0.5, 1.0)})[0]
    assert check["matches"]
    assert check["bound"] == 64 * sys.float_info.epsilon
    for key in ("elapsed", "prior_clock", "theta_e", "decay_rate_z"):
        assert not luna45.compare_historical({key: 0.5}, {key: math.nextafter(0.5, 1.0)})[0]["matches"]
    assert not luna45.compare_historical({"source": "source"}, {"source": "mutated"})[0]["matches"]
    assert not luna45.compare_historical({"timestamp": 0.5}, {"timestamp": math.nextafter(0.5, 1.0)})[0]["matches"]


def test_exact_upstream_invariance_and_ordered_gates(simple_runs):
    runs = deepcopy(simple_runs)
    history = [history_of(runs[luna45.ARMS[2]][0])]
    gates = luna45.run_gates(runs, history)
    assert list(gates) == ["G1", "G2", "G3", "G4"]
    for arm in luna45.ARMS:
        assert luna45.upstream(runs[arm][0]) == luna45.upstream(runs[luna45.ARMS[2]][0])
        assert runs[arm][0]["luna45_bounds"]["matches"]


@pytest.mark.parametrize("field", [
    "source_emissions", "relay_state_trajectory", "relay_integration_trace",
    "routing_enqueue_events", "receiver_reception_events",
])
def test_g1_rejects_each_upstream_history_mismatch(simple_runs, field):
    runs = deepcopy(simple_runs)
    old = history_of(runs[luna45.ARMS[2]][0])
    old[field][0]["event_id"] = "historical-mutation"
    with pytest.raises(luna45.Blocker) as failure:
        luna45.run_gates(runs, [old])
    assert failure.value.gate == "G1"
    assert "G2" not in failure.value.detail["checks"]


def test_g2_exact_float_drift_is_not_tolerated(simple_runs):
    runs = deepcopy(simple_runs)
    old = history_of(runs[luna45.ARMS[2]][0])
    runs[luna45.ARMS[0]][0]["source_emissions"][0]["payload"] = math.nextafter(
        runs[luna45.ARMS[0]][0]["source_emissions"][0]["payload"], 1.0
    )
    with pytest.raises(luna45.Blocker) as failure:
        luna45.run_gates(runs, [old])
    assert failure.value.gate == "G2"
    assert "G3" not in failure.value.detail["checks"]


def test_route_reconciliation_rejects_source_mutation_with_details(simple_runs):
    record = simple_runs[luna45.ARMS[0]][0]
    enqueue = deepcopy(record["routing_enqueue_events"])
    receive = deepcopy(record["receiver_reception_events"])
    receive[0]["source"] = "mutated-source-only"
    report = luna45.reconcile(enqueue, receive)
    assert not report["reconciles"]
    assert report["source_mismatch_count"] == 1
    assert report["payload_mismatch_count"] == 0
    assert report["unmatched_enqueue_count"] == report["unmatched_reception_count"] == 1
    assert report["checks"][0]["enqueue_source"] != report["checks"][0]["reception_source"]


@pytest.mark.parametrize("field,value,counter", [
    ("destination", "mutated", "destination_mismatch_count"),
    ("event_id", "mutated", "event_id_mismatch_count"),
    ("payload_bits", "0000000000000000", "payload_mismatch_count"),
    ("reception_timestamp", 99.0, "timing_mismatch_count"),
    ("route_path", ["relay", "source"], "route_path_mismatch_count"),
    ("route_depth", 9, "route_path_mismatch_count"),
    ("causal_roots", ["mutated"], "provenance_mismatch_count"),
    ("originating_emission_id", "mutated", "provenance_mismatch_count"),
    ("roots_truncated", True, "provenance_mismatch_count"),
])
def test_route_mismatch_categories(simple_runs, field, value, counter):
    record = simple_runs[luna45.ARMS[0]][0]
    receive = deepcopy(record["receiver_reception_events"])
    receive[0][field] = value
    report = luna45.reconcile(record["routing_enqueue_events"], receive)
    assert not report["reconciles"]
    assert report[counter] == 1


def test_missing_duplicate_and_orphan_captures(simple_runs):
    record = simple_runs[luna45.ARMS[0]][0]
    enqueue, receive = record["routing_enqueue_events"], record["receiver_reception_events"]
    missing = luna45.reconcile(enqueue, [])
    assert not missing["reconciles"] and missing["unmatched_enqueue_count"] == 1
    orphan = luna45.reconcile([], receive)
    assert not orphan["reconciles"] and orphan["orphan_reception_count"] == 1
    for first, second, key in (
        (enqueue + enqueue, receive, "duplicate_enqueue_count"),
        (enqueue, receive + receive, "duplicate_reception_count"),
    ):
        report = luna45.reconcile(first, second)
        assert not report["reconciles"] and report[key] == 1


def test_both_capture_sites_retain_state_and_exact_payload(integrated_record):
    record = integrated_record
    for source, destination in (("source", "relay"), ("relay", "destination")):
        enqueues = [item for item in record["routing_enqueue_events"] if item["source"] == source]
        receives = [item for item in record["receiver_reception_events"] if item["destination"] == destination]
        assert enqueues and receives
        assert luna45.reconcile(enqueues, receives)["reconciles"]
        for admission, reception in zip(enqueues, receives):
            assert admission is not reception
            assert admission["source"] == reception["source"]
            assert admission["payload_encoding"] == reception["payload_encoding"]
            state = reception["receiver_state_transition"]
            assert state["processed_events_after"] == state["processed_events_before"] + 1


@pytest.mark.parametrize("field,value", [
    ("queue_peak", 129), ("processed_events", 1025), ("activity_high_water", 1025),
    ("prediction_peak", 9), ("pending_events", 1), ("prediction_expiry", 5.0),
    ("topology_edge_peak", 3), ("topology_fan_in_peak", 3),
])
def test_hard_bounds_fail_exactly(simple_runs, field, value):
    record = deepcopy(simple_runs[luna45.ARMS[0]][0])
    record["resource_high_water"][field] = value
    assert not luna45.bounds_check(record)["matches"]


def test_destination_oracle_verifies_genuine_integrated_chain(integrated_record):
    emitted = [item for item in integrated_record["destination_evidence"]
               if item["canonical_emission"] is not None]
    assert emitted
    assert all(item["classification"] == "integration-mediated" for item in emitted)
    for item in emitted:
        assert item["genuine_chain"]["verified"]
        assert item["discharge_decision"]
        assert item["discharge_amount"] == item["discharge_sign"] == 1
        assert item["oracle"]["dt"]["exact_match"]
        assert item["oracle"]["classification_matches"]
        assert item["contributing_receptions"]
        assert len(item["genuine_chain"]["upstream_links"]) == len(item["contributing_receptions"])
    report = luna45.arm_report([integrated_record])
    assert report["genuine_integrated_emissions"] == len(emitted)
    assert report["maximum_abs_z_location"]["event_id"] is not None
    assert all(item["contributing_reception_count"] > 1
               for item in report["emission_timing_and_contributing_receptions"])


def _destination_chain_and_link(record, relay_emission_id):
    destination = next(
        item for item in record["destination_evidence"]
        if item["canonical_emission"] is not None
        and any(
            link["relay_canonical_emission"]["event_id"] == relay_emission_id
            for link in item["genuine_chain"]["upstream_links"]
        )
    )
    link = next(
        item for item in destination["genuine_chain"]["upstream_links"]
        if item["relay_canonical_emission"]["event_id"] == relay_emission_id
    )
    return destination, link


def _add_unrelated_source_route(record, *, event_id, root, timestamp):
    source = deepcopy(record["source_emissions"][0])
    source.update(event_id=event_id, lineage_id=9001, timestamp=timestamp)
    record["source_emissions"].append(source)
    runtime_emission = deepcopy(next(
        item for item in record["runtime_events"]
        if item["event_type"] == "excursion_emission" and item["source"] == "source"
    ))
    runtime_emission.update(
        event_id=event_id, lineage_id=9001, timestamp=timestamp,
        causal_roots=[root], sequence=9001,
    )
    record["runtime_events"].append(runtime_emission)
    enqueue = deepcopy(next(
        item for item in record["routing_enqueue_events"]
        if item["source"] == "source"
    ))
    enqueue.update(
        event_id=event_id, originating_emission_id=event_id, lineage_id=9001,
        causal_roots=[root], queue_sequence=9001,
        enqueue_timestamp=timestamp - 1.0,
        scheduled_delivery_timestamp=timestamp, timestamp=timestamp,
    )
    record["routing_enqueue_events"].append(enqueue)
    reception = deepcopy(next(
        item for item in record["source_to_relay_receptions"]
    ))
    reception.update(
        event_id=event_id, originating_emission_id=event_id, lineage_id=9001,
        causal_roots=[root], queue_sequence=9001,
        reception_timestamp=timestamp, scheduled_delivery_timestamp=timestamp,
    )
    record["source_to_relay_receptions"].append(reception)


def test_chain_includes_only_exact_provenance_roots(integrated_record):
    record = deepcopy(integrated_record)
    destination, link = _destination_chain_and_link(record, "relay:excursion:2")
    assert link["relay_causal_roots"] == ["c00-000:input:2"]
    assert [
        item["source_inputs"][0]["point_index"]
        for item in link["canonical_source_links"]
    ] == [2]
    assert luna45.reconstruct_chain(record, destination)["verified"]


def test_chain_includes_each_second_valid_root(integrated_record):
    link = next(
        link for item in integrated_record["destination_evidence"]
        for link in item.get("genuine_chain", {}).get("upstream_links", [])
        if link["relay_canonical_emission"]["event_id"] == "relay:excursion:1"
    )
    assert link["relay_causal_roots"] == [
        "c00-000:input:0", "c00-000:input:1",
    ]
    assert [
        item["source_inputs"][0]["point_index"]
        for item in link["canonical_source_links"]
    ] == [0, 1]


def test_two_earlier_source_events_outside_declared_roots_are_excluded(integrated_record):
    record = deepcopy(integrated_record)
    destination, link = _destination_chain_and_link(record, "relay:excursion:2")
    check_time = link["relay_recurrence"]["timestamp"]
    earlier = [
        item for item in record["source_to_relay_receptions"]
        if item["reception_timestamp"] <= check_time
        and item["event_id"] != "source:excursion:3"
    ]
    assert len(earlier) >= 2
    assert [
        item["source_canonical_emission"]["event_id"]
        for item in link["canonical_source_links"]
    ] == ["source:excursion:3"]
    assert luna45.reconstruct_chain(record, destination)["verified"]


def test_nearby_earlier_event_outside_provenance_is_excluded(integrated_record):
    record = deepcopy(integrated_record)
    destination, link = _destination_chain_and_link(record, "relay:excursion:2")
    check_time = link["relay_recurrence"]["timestamp"]
    _add_unrelated_source_route(
        record, event_id="source:unrelated-nearby",
        root="c00-000:input:9", timestamp=check_time - 1.01,
    )
    rebuilt = luna45.reconstruct_chain(record, destination)
    linked_ids = {
        item["source_canonical_emission"]["event_id"]
        for item in rebuilt["upstream_links"][1]["canonical_source_links"]
    }
    assert "source:unrelated-nearby" not in linked_ids


def test_unknown_declared_root_blocks_chain(integrated_record):
    record = deepcopy(integrated_record)
    destination, _ = _destination_chain_and_link(record, "relay:excursion:2")
    emission = next(
        item for item in record["runtime_events"]
        if item["event_id"] == "relay:excursion:2"
    )
    emission["causal_roots"] = ["unknown:input"]
    with pytest.raises(luna45.Blocker, match="unknown input root"):
        luna45.reconstruct_chain(record, destination)


def test_extra_reconstructed_root_blocks_chain(integrated_record):
    record = deepcopy(integrated_record)
    destination, link = _destination_chain_and_link(record, "relay:excursion:2")
    source_link = link["canonical_source_links"][0]
    source_id = source_link["source_canonical_emission"]["event_id"]
    extra = "c00-000:input:9"
    source_link["relay_actual_reception"]["causal_roots"].append(extra)
    source_link["source_queue_admission"]["causal_roots"].append(extra)
    source_trace = next(
        item for item in record["runtime_events"] if item["event_id"] == source_id
    )
    source_trace["causal_roots"].append(extra)
    with pytest.raises(luna45.Blocker, match="provenance link absent"):
        luna45.reconstruct_chain(record, destination)


def test_missing_reconstructed_root_blocks_chain(integrated_record):
    record = deepcopy(integrated_record)
    destination, _ = _destination_chain_and_link(record, "relay:excursion:2")
    record["source_to_relay_receptions"] = [
        item for item in record["source_to_relay_receptions"]
        if item["event_id"] != "source:excursion:3"
    ]
    with pytest.raises(luna45.Blocker, match="do not exactly match"):
        luna45.reconstruct_chain(record, destination)


def test_duplicate_root_blocks_under_production_deduplication_contract(integrated_record):
    record = deepcopy(integrated_record)
    destination, _ = _destination_chain_and_link(record, "relay:excursion:2")
    emission = next(
        item for item in record["runtime_events"]
        if item["event_id"] == "relay:excursion:2"
    )
    emission["causal_roots"] *= 2
    with pytest.raises(luna45.Blocker, match="duplicate"):
        luna45.reconstruct_chain(record, destination)


def test_lineage_provenance_mutation_blocks_chain(integrated_record):
    record = deepcopy(integrated_record)
    destination, link = _destination_chain_and_link(record, "relay:excursion:2")
    link["canonical_source_links"][0]["relay_actual_reception"]["lineage_id"] += 1
    with pytest.raises(luna45.Blocker, match="provenance link absent"):
        luna45.reconstruct_chain(record, destination)


def test_multi_hop_chain_roots_match_both_route_receivers(integrated_record):
    record = deepcopy(integrated_record)
    destination = next(
        item for item in record["destination_evidence"]
        if item["canonical_emission"] is not None
    )
    chain = luna45.reconstruct_chain(record, destination)
    assert chain["verified"]
    for link in chain["upstream_links"]:
        roots = link["relay_causal_roots"]
        assert link["relay_queue_admission"]["causal_roots"] == roots
        assert link["destination_actual_reception"]["causal_roots"] == roots
        assert [
            root
            for source_link in link["canonical_source_links"]
            for root in source_link["relay_actual_reception"]["causal_roots"]
        ] == roots


@pytest.mark.parametrize("field,value", [
    ("elapsed", 0.125), ("z_after_input", 99.0),
    ("discharge_amount", -1.0), ("classification", "direct"),
    ("theta_e", 0.5), ("emission_id", "forged"),
])
def test_destination_mutations_block_not_support(integrated_record, field, value):
    record = deepcopy(integrated_record)
    entry = next(item for item in record["destination_integration_trace"]
                 if item["emission_id"] is not None)
    entry[field] = value
    with pytest.raises(luna45.Blocker):
        luna45.destination_evidence(record)


def test_unreconstructable_chain_blocks(integrated_record):
    record = deepcopy(integrated_record)
    record["source_emissions"].clear()
    with pytest.raises(luna45.Blocker, match="source/admission/reception"):
        luna45.destination_evidence(record)


def test_disabled_destination_has_no_slow_state_and_no_precursor_scan(simple_runs):
    record = deepcopy(simple_runs[luna45.ARMS[0]][0])
    luna45.destination_evidence(record)
    assert not record["destination_integration_trace"]
    assert not record["candidate_opportunity_precursors"]["scan_performed"]
    assert luna45.arm_report([record])["maximum_abs_z"] == 0.0


def test_precursors_use_source_not_relay_and_exact_window():
    record = {
        "stream_id": "unit", "source_emissions": [
            {"event_id": "source-equal", "timestamp": 4.0},
            {"event_id": "source-boundary", "timestamp": 0.0},
            {"event_id": "source-too-old", "timestamp": -0.0001},
            {"event_id": "source-future", "timestamp": 5.0},
        ], "relay_emissions": [{"event_id": "never-endpoint", "timestamp": 3.0}],
        "destination_emissions": [{"event_id": "destination-1", "timestamp": 4.0}],
    }
    result = luna45.precursor_scan(record)
    assert result["label"] == "candidate-opportunity precursors"
    assert result["count"] == result["unique_characters"] == 1
    pair = result["pairs"][0]
    assert pair["source_canonical_emission_id"] == "source-boundary"
    assert pair["destination_canonical_emission_id"] == "destination-1"
    assert pair["elapsed"] == 4.0
    assert not result["candidate_instantiation"]


def test_default_only_and_direct_only_never_support():
    reports = {arm: {"genuine_integrated_emissions": 0} for arm in luna45.ARMS}
    reports[luna45.ARMS[1]]["genuine_integrated_emissions"] = 1
    assert luna45.decide(True, reports) == ("PASS", "NOT SUPPORTED IN THIS SETUP")
    reports[luna45.ARMS[2]]["direct_emissions"] = 10
    assert luna45.decide(True, reports) == ("PASS", "NOT SUPPORTED IN THIS SETUP")
    reports[luna45.ARMS[2]]["genuine_integrated_emissions"] = 1
    assert luna45.decide(True, reports) == ("PASS", "SUPPORTED")
    assert luna45.decide(False, reports) == ("BLOCKED", "BLOCKED")


def test_replay_digest_detects_one_bit_and_capture_changes(simple_runs):
    records = deepcopy(simple_runs[luna45.ARMS[0]])
    for record in records:
        luna45.destination_evidence(record)
    report = luna45.arm_report(records)
    original = luna45.phase_digest(records, report)
    assert original == luna45.phase_digest(deepcopy(records), deepcopy(report))
    records[0]["source_emissions"][0]["payload"] = math.nextafter(records[0]["source_emissions"][0]["payload"], 1.0)
    assert original != luna45.phase_digest(records, report)


def test_replay_canonical_bytes_match_for_identical_material(simple_runs):
    records = deepcopy(simple_runs[luna45.ARMS[0]])
    for record in records:
        luna45.destination_evidence(record)
    report = luna45.arm_report(records)
    compared = luna45.compare_phase_replay(
        records, report, deepcopy(records), deepcopy(report),
    )
    assert compared["matches"]
    assert compared["canonical_bytes_equal"]
    assert compared["digests_equal"]
    assert compared["initial_byte_length"] == compared["replay_byte_length"]
    assert compared["initial_sha256"] == compared["replay_sha256"]
    assert compared["first_byte_difference"] is None


def test_replay_canonical_bytes_sort_object_keys():
    initial = {"records": [{"source": "source", "lineage_id": 3}], "report": {"count": 1}}
    reordered = {
        "report": {"count": 1},
        "records": [{"lineage_id": 3, "source": "source"}],
    }
    initial_bytes = luna45.reference._canonical_bytes(initial)
    replay_bytes = luna45.reference._canonical_bytes(reordered)
    assert initial_bytes == replay_bytes


@pytest.mark.parametrize("mutator", [
    lambda row: row.pop("source"),
    lambda row: row.update(mandatory_extension="extra"),
    lambda row: row.update(payload=math.nextafter(row["payload"], 1.0)),
    lambda row: row.update(event_id="different-source-event"),
    lambda row: row.update(causal_roots=["different:root"]),
])
def test_replay_canonical_bytes_reject_material_mutations(mutator):
    initial = [{"source": "source", "event_id": "source:excursion:1",
                "payload": 0.25, "causal_roots": ["c00-000:input:0"]}]
    replay = deepcopy(initial)
    mutator(replay[0])
    comparison = luna45.compare_phase_replay(
        initial, {"count": 1}, replay, {"count": 1},
    )
    assert not comparison["matches"]
    assert not comparison["canonical_bytes_equal"]
    assert comparison["initial_sha256"] != comparison["replay_sha256"]
    assert comparison["first_byte_difference"]["offset"] >= 0


def test_equal_digest_cannot_override_unequal_canonical_bytes():
    assert not luna45.replay_content_matches(b"initial", b"replay", "same", "same")
    assert not luna45.replay_content_matches(b"same", b"same", "initial-hash", "replay-hash")


def test_replay_accepts_only_equal_canonical_bytes_and_digests():
    encoded = luna45.phase_canonical_bytes(
        [{"source": "source", "payload": 0.25}], {"count": 1},
    )
    digest = hashlib.sha256(encoded).hexdigest()
    assert luna45.replay_content_matches(encoded, bytes(encoded), digest, digest)
    assert not luna45.replay_content_matches(encoded, encoded + b" ", digest, digest)


def test_replay_comparison_records_first_differing_byte():
    initial = [{"value": "before"}]
    replay = [{"value": "after"}]
    compared = luna45.compare_phase_replay(initial, {}, replay, {})
    difference = compared["first_byte_difference"]
    assert difference is not None
    assert difference["initial_byte"] != difference["replay_byte"]
    assert difference["initial_context_hex"]
    assert difference["replay_context_hex"]


def mock_startup(monkeypatch):
    metadata = {
        "execution_revision": "unit-revision", "runner_revision": "unit-revision",
        "runner_sha256": luna45.file_hash(Path(luna45.__file__)),
        "config_digest": luna45.digest(luna45.experiment_config()),
    }
    monkeypatch.setattr(luna45, "collect_provenance", lambda: metadata.copy())
    monkeypatch.setattr(luna45, "load_inputs", lambda: ({"sequences": []}, {}))
    monkeypatch.setattr(luna45, "load_history", lambda: ([], {}))
    monkeypatch.setattr(luna45.reference, "_git_output", lambda *args: "unit-revision")
    return metadata


def empty_phase(blocker=None):
    runs = {arm: [] for arm in luna45.ARMS}
    reports = {arm: luna45.arm_report([]) for arm in luna45.ARMS}
    return runs, reports, {}, blocker


def test_initial_blocker_has_no_science_digest_or_replay(tmp_path, monkeypatch):
    mock_startup(monkeypatch)
    calls = []
    def initial(*args):
        calls.append(1)
        return empty_phase({"gate": "G1", "reason": "unit blocker"})
    monkeypatch.setattr(luna45, "execute_phase", initial)
    output = tmp_path / "blocked"
    result = luna45.run_experiment(output)
    assert len(calls) == 1
    assert result["status"] == "BLOCKED" and result["replay_not_run"]
    assert result["summary_digest"] is None
    assert all(value is None for value in result["initial_digests"].values())
    assert all(value is None for value in result["replay_digests"].values())
    assert not list(output.glob("replay-*.json"))
    with pytest.raises(FileExistsError):
        luna45.run_experiment(output)


def test_replay_blocker_preserves_initial_artifacts_and_digest(tmp_path, monkeypatch):
    mock_startup(monkeypatch)
    calls = []
    saved = {}
    output = tmp_path / "replay-blocker"
    def phase(*args):
        calls.append(1)
        if len(calls) == 1:
            return empty_phase()
        for path in output.glob("initial-*.json"):
            saved[path.name] = path.read_bytes()
        return empty_phase({"gate": "G4", "reason": "unit replay capacity failure"})
    monkeypatch.setattr(luna45, "execute_phase", phase)
    result = luna45.run_experiment(output)
    assert result["status"] == "BLOCKED" and not result["replay_not_run"]
    assert result["initial_blocker"] is None
    assert result["replay_blocker"]["gate"] == "G4"
    assert all(value is not None for value in result["initial_digests"].values())
    assert all(value is None for value in result["replay_digests"].values())
    assert saved
    for name, payload in saved.items():
        assert (output / name).read_bytes() == payload
    for artifact in output.glob("*.json"):
        value = json.loads(artifact.read_bytes())
        assert value["artifact_digest"] == luna45.reference._artifact_digest(value)


def test_execution_exception_retains_raw_capture_before_failure(monkeypatch):
    original = luna45.reference._run_character
    def fail_after_character(**kwargs):
        original(**kwargs)
        raise RuntimeError("unit post-runtime failure")
    monkeypatch.setattr(luna45.reference, "_run_character", fail_after_character)
    with pytest.raises(luna45.Blocker) as failure:
        luna45.run_character(luna45.ARMS[0], sequence())
    detail = failure.value.detail
    assert not detail["completed"]
    assert detail["routing_enqueue_events"] and detail["receiver_reception_events"]
    assert detail["snapshots"]
    assert "unit post-runtime failure" in detail["reason"]


@pytest.mark.parametrize("value,expected", [
    (1.2, "direct"), (0.4, "none"), (-1.2, "direct"), (-0.4, "none"),
])
def test_oracle_direct_admission_is_distinct_from_subthreshold_integration(value, expected):
    config = E1Config(integration=IntegrationConfig(decay_rate_z=0.0125))
    neuron = MultiExcursionNeuron("destination", config=config)
    neuron.receive_event(Event(0.0, "relay", "destination", EventType.EXCURSION, value, event_id="unit"))
    captured = {
        "timestamp": 0.0, "prior_clock": 0.0, "event_id": "unit",
        "event_type": EventType.EXCURSION.value, "payload": value,
        "x_before": 0.0, "z_before": 0.0, "mode_before": "N",
    }
    checks = luna45.reference._relay_recurrence_checks(
        luna45.reference._jsonable(neuron.integration_trace), [captured], config,
    )
    assert checks[0]["matches"]
    assert checks[0]["expected_classification"] == expected
    assert checks[0]["discharge_amount"]["expected"] == 0.0


def test_execution_blocker_persists_separate_failed_raw_records(tmp_path, monkeypatch, simple_runs):
    mock_startup(monkeypatch)
    record = simple_runs[luna45.ARMS[0]][0]
    blocker = {
        "gate": "EXECUTION", "reason": "unit capacity failure", "arm": luna45.ARMS[0],
        "stream_id": record["stream_id"],
        "routing_enqueue_events": record["routing_enqueue_events"],
        "receiver_reception_events": record["receiver_reception_events"],
    }
    monkeypatch.setattr(luna45, "execute_phase", lambda *args: empty_phase(blocker))
    output = tmp_path / "capacity"
    result = luna45.run_experiment(output)
    assert result["replay_not_run"]
    assert json.loads((output / "initial-failed-enqueue.json").read_bytes())["events"]
    assert json.loads((output / "initial-failed-reception.json").read_bytes())["events"]
    assert json.loads((output / "initial-failed-character.json").read_bytes())["failed_character"] == blocker


def test_write_artifact_is_no_overwrite_and_digest_bound(tmp_path):
    result = luna45.write_artifact(tmp_path, "unit.json", {"execution_revision": "unit"}, {"records": []})
    payload = (tmp_path / "unit.json").read_bytes()
    assert result["file_sha256"] == hashlib.sha256(payload).hexdigest()
    assert result["byte_length"] == len(payload)
    with pytest.raises(FileExistsError):
        luna45.write_artifact(tmp_path, "unit.json", {}, {})
