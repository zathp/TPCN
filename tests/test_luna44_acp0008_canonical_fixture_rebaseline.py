from __future__ import annotations

import hashlib
from copy import deepcopy
from dataclasses import replace
import json
import math
from pathlib import Path
import subprocess
import sys

import pytest

import run_luna44_acp0008_canonical_fixture_rebaseline as luna44


GENERATOR_MODULE = "run_luna34_excursion_v1_multi_emitter_bridge"


def _synthetic_sequence(values: tuple[tuple[float, float, float], ...]):
    points = []
    batch_ordinal = -1
    previous = None
    for point_index, (timestamp, x, y) in enumerate(values):
        if previous is None or timestamp != previous:
            batch_ordinal += 1
        stream_id = "c00-000"
        point = {
            "seed": 0,
            "sequence_index": 0,
            "stream_id": stream_id,
            "point_index": point_index,
            "batch_ordinal": batch_ordinal,
            "x": luna44._float_record(x),
            "y": luna44._float_record(y),
            "t": luna44._float_record(timestamp),
            "audit_x_plus_y": luna44._float_record(x + y),
        }
        points.append(point)
        previous = timestamp
    sequence = {
        "seed": 0,
        "sequence_index": 0,
        "stream_id": "c00-000",
        "point_count": len(points),
        "points": points,
    }
    sequence["source_sha256"] = luna44._digest(luna44._sequence_raw_rows(sequence))
    return sequence


def _route_pair():
    return (
        {
            "event_id": "emission-1",
            "queue_sequence": 1,
            "source": "source",
            "destination": "relay",
            "event_type": "excursion",
            "enqueue_timestamp": 1.0,
            "scheduled_delivery_timestamp": 2.0,
            "payload": 0.5,
            "payload_bits": luna44._bits(0.5),
            "route_path": ["source", "relay"],
            "route_depth": 1,
            "lineage_id": "lineage-1",
            "causal_roots": ["root-1"],
            "roots_truncated": False,
            "originating_emission_id": "emission-1",
        },
        {
            "event_id": "emission-1",
            "queue_sequence": 1,
            "source": "source",
            "destination": "relay",
            "receiver_node": "relay",
            "event_type": "excursion",
            "reception_timestamp": 2.0,
            "scheduled_delivery_timestamp": 2.0,
            "payload": 0.5,
            "payload_bits": luna44._bits(0.5),
            "route_path": ["source", "relay"],
            "route_depth": 1,
            "lineage_id": "lineage-1",
            "causal_roots": ["root-1"],
            "roots_truncated": False,
            "originating_emission_id": "emission-1",
        },
    )


def test_fixture_loads_from_retained_files_without_generator_or_builder():
    fixture, provenance = luna44.load_fixture()
    assert len(fixture["sequences"]) == 5 * 64
    assert sum(item["point_count"] for item in fixture["sequences"]) == 5164
    assert provenance["canonical_fixture_sha256"] == luna44.FIXTURE_SHA256
    fixture_bytes = luna44.FIXTURE_PATH.read_bytes()
    assert hashlib.sha256(fixture_bytes).hexdigest() == provenance["fixture_json_sha256"]
    assert provenance["fixture_json_sha256"] == luna44.FIXTURE_FILE_SHA256
    assert provenance["fixture_json_sha256"] != provenance["canonical_fixture_sha256"]
    subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import sys; "
                "import run_luna44_acp0008_canonical_fixture_rebaseline as runner; "
                "runner.load_fixture(); "
                f"assert {GENERATOR_MODULE!r} not in sys.modules"
            ),
        ],
        cwd=Path(luna44.__file__).resolve().parent,
        check=True,
        capture_output=True,
        text=True,
    )


def test_fixture_loader_rejects_duplicated_or_mismatching_materializations():
    provenance = luna44.FIXTURE_PROVENANCE_PATH.read_text(encoding="utf-8")
    manifest = json.loads(provenance)
    fixture_bytes = luna44.FIXTURE_PATH.read_bytes()
    fixture = json.loads(fixture_bytes)
    rows = [
        row
        for sequence in fixture["sequences"]
        for row in luna44._sequence_raw_rows(sequence)
    ]
    manifest["materializations"][1] = manifest["materializations"][0].copy()
    with pytest.raises(ValueError, match="duplicated or not independent"):
        luna44._validate_materialization_provenance(
            manifest, fixture_bytes, fixture, rows
        )

    manifest["materializations"][1] = json.loads(provenance)["materializations"][1]
    manifest["materializations"][1]["semantic_fixture_digest"] = "0" * 64
    with pytest.raises(ValueError, match="measurements differ"):
        luna44._validate_materialization_provenance(
            manifest, fixture_bytes, fixture, rows
        )


def test_fixture_rejects_manifest_metadata_drift(tmp_path, monkeypatch):
    provenance_bytes = luna44.FIXTURE_PROVENANCE_PATH.read_bytes()
    with pytest.raises(ValueError, match="provenance path differs from the pinned path"):
        luna44.load_fixture(provenance_path=tmp_path / "wrong-path.json")
    timestamp = json.loads(provenance_bytes)["generation_timestamp_utc"]
    changed = timestamp[:-1] + ("1" if timestamp[-1] != "1" else "2")
    original_timestamp = f'"generation_timestamp_utc": "{timestamp}"'.encode()
    changed_timestamp = f'"generation_timestamp_utc": "{changed}"'.encode()
    assert len(original_timestamp) == len(changed_timestamp)
    assert original_timestamp in provenance_bytes
    mutated_manifest_path = tmp_path / "provenance.json"
    mutated_manifest_path.write_bytes(provenance_bytes.replace(original_timestamp, changed_timestamp))
    monkeypatch.setattr(luna44, "FIXTURE_PROVENANCE_PATH", mutated_manifest_path)

    with pytest.raises(ValueError, match="committed provenance-revision blob"):
        luna44.load_fixture(provenance_path=mutated_manifest_path)


def test_topology_and_only_relay_integration_vary_by_arm():
    config = luna44.experiment_config()
    assert config["authorization_revision"] == luna44.AUTHORIZATION_REVISION
    assert config["fixture"]["revision"] == luna44.FIXTURE_REVISION
    assert config["fixture"]["canonical_sha256"] == luna44.FIXTURE_SHA256
    assert config["fixture"]["provenance_manifest_path"] == (
        luna44.FIXTURE_PROVENANCE_PATH.as_posix()
    )
    assert config["fixture"]["provenance_manifest_revision"] == (
        luna44.FIXTURE_PROVENANCE_REVISION
    )
    assert config["fixture"]["provenance_manifest_sha256"] == luna44.FIXTURE_PROVENANCE_SHA256
    assert config["fixture"]["provenance_manifest_git_blob"] == (
        luna44.FIXTURE_PROVENANCE_GIT_BLOB
    )
    assert config["authorization_handoff_sha256"] == luna44.AUTHORIZATION_HANDOFF_SHA256
    for arm in luna44.ARMS:
        for node in luna44.NODES:
            node_config = config["neuron_configurations"][arm][node]
            assert set(node_config) == {
                "decay_rate",
                "x_max",
                "theta_r",
                "theta_e",
                "theta_hold",
                "theta_m",
                "emission_delay",
                "m_emit_delay",
                "m_rearm_delay",
                "delta_x_e",
                "a_min",
                "a_max",
                "provenance_capacity",
                "event_budget",
                "integration",
            }
            assert node_config["event_budget"] == 4096
            assert {
                key: value
                for key, value in node_config.items()
                if key != "integration"
            } == {
                "decay_rate": 1.0,
                "x_max": 8.0,
                "theta_r": 0.25,
                "theta_e": 1.0,
                "theta_hold": 1.5,
                "theta_m": 4.0,
                "emission_delay": 0.5,
                "m_emit_delay": 1.0,
                "m_rearm_delay": 1.0,
                "delta_x_e": 1.0,
                "a_min": 0.25,
                "a_max": 1.0,
                "provenance_capacity": 16,
                "event_budget": 4096,
            }
            if node != "relay" or arm == "DISABLED":
                assert node_config["integration"] is None
            else:
                assert node_config["integration"] == {
                    "decay_rate_z": 0.1 if arm == "DEFAULT" else 0.0125,
                    "input_gain": 1.0,
                    "discharge_quantum": 1.0,
                    "z_max": 4.0,
                }
    assert config["runtime"] == {
        "neuron_event_budget": 4096,
        "queue_capacity": 128,
        "runtime_event_budget": 1024,
        "max_activity_events": 1024,
        "settling_horizon": 4.0,
        "prediction_capacity": 8,
        "prediction_expiry": 4.0,
        "eligibility_capacity_per_ledger": 1024,
        "neutral_reward": 0.0,
    }
    topology = luna44._topology()
    assert topology.nodes == ("source", "relay", "destination")
    assert [
        (
            edge.source,
            edge.destination,
            edge.propagation_delay,
            edge.edge_weight,
            edge.divider_strength,
            edge.reference,
        )
        for edge in topology.edges
    ] == [
        ("source", "relay", 1.0, 1.0, 1.0, 0.0),
        ("relay", "destination", 1.0, 1.0, 1.0, 0.0),
    ]
    assert topology.edge_capacity == topology.routing_capacity == 3
    assert luna44._relay_integration("DISABLED") is None
    assert luna44._relay_integration("DEFAULT").decay_rate_z == 0.1
    assert luna44._relay_integration("CALIBRATED").decay_rate_z == 0.0125


def test_small_sequence_retains_exact_inputs_and_raw_identity_across_arms():
    sequence = _synthetic_sequence(
        (
            (0.0, 1.0, 1.0),
            (0.0, -0.75, 0.5),
            (12.9, 2.0, 2.0),
            (25.8, 2.0, 2.0),
            (50.0, 0.0, 0.0),
        )
    )
    records = {
        arm: luna44._run_character(arm=arm, sequence=sequence)
        for arm in luna44.ARMS
    }
    baseline = records["DISABLED"]
    assert baseline["raw_identity"] == luna44._sequence_raw_rows(sequence)
    for arm, record in records.items():
        assert record["raw_identity"] == baseline["raw_identity"]
        assert record["raw_identity_sha256"] == baseline["raw_identity_sha256"]
        assert len(record["point_inputs"]) == len(sequence["points"])
        assert record["integration_configuration"]["source"] is None
        assert record["integration_configuration"]["destination"] is None
        assert all(item["matches"] for item in record["canonical_emission_checks"]["source"])
        assert all("m_peak" in item for item in record["source_emissions"])
        for source_point, retained in zip(sequence["points"], record["point_inputs"]):
            expected = float.fromhex(source_point["x"]["hex"]) + float.fromhex(
                source_point["y"]["hex"]
            )
            actual = float.fromhex(retained["computed_source_value"]["hex"])
            assert luna44._bits(actual) == luna44._bits(expected)
            assert retained["computed_source_value"]["decimal"] == repr(expected)
            assert retained["audit_comparison"]["matches"]
            assert retained["audit_comparison"]["error"] == retained["audit_comparison"]["absolute_error"]
            assert retained["audit_comparison"]["bound"] == retained["audit_comparison"]["tolerance"]
            assert retained["audit_comparison"]["tolerance"] == (
                64
                * sys.float_info.epsilon
                * max(
                    1.0,
                    abs(expected),
                    abs(float.fromhex(source_point["audit_x_plus_y"]["hex"])),
                )
            )
        assert record["point_inputs"][1]["computed_source_value"]["decimal"] == "-0.25"
        input_events = [
            item
            for item in record["runtime_events"]
            if item["destination"] == "source" and item["event_type"] == "input"
        ]
        assert [item["event_id"] for item in input_events[:2]] == [
            "c00-000:input:0",
            "c00-000:input:1",
        ]
        for event, point in zip(input_events, sequence["points"]):
            expected = (
                float.fromhex(point["x"]["hex"])
                + float.fromhex(point["y"]["hex"])
            )
            assert luna44._bits(float(event["payload"])) == luna44._bits(expected)
    assert records["DISABLED"]["integration_configuration"]["relay"] is None
    assert records["DEFAULT"]["integration_configuration"]["relay"]["decay_rate_z"] == 0.1
    assert records["CALIBRATED"]["integration_configuration"]["relay"]["decay_rate_z"] == 0.0125


def test_small_sequence_has_deterministic_event_order_and_replay_digest():
    sequence = _synthetic_sequence(
        (
            (0.0, 2.0, 2.0),
            (12.9, 2.0, 2.0),
            (25.8, 2.0, 2.0),
            (50.0, 0.0, 0.0),
        )
    )
    first = luna44._run_character(arm="CALIBRATED", sequence=sequence)
    replay = luna44._run_character(arm="CALIBRATED", sequence=sequence)
    assert first["record_digest"] == replay["record_digest"]
    assert first["runtime_events"] == replay["runtime_events"]
    assert first["relay_state_trajectory"] == replay["relay_state_trajectory"]
    for field in ("routing_enqueue_events", "receiver_reception_events",
                  "routing_stream_digests"):
        assert first[field] == replay[field]
    input_events = [
        item for item in first["runtime_events"]
        if item["destination"] == "source" and item["event_type"] == "input"
    ]
    assert [item["event_id"] for item in input_events] == [
        "c00-000:input:0",
        "c00-000:input:1",
        "c00-000:input:2",
        "c00-000:input:3",
    ]


def test_relay_classification_onward_reconciliation_and_resource_bounds():
    sequence = _synthetic_sequence(
        (
            (0.0, 4.0, 0.0),
            (3.0, 4.0, 0.0),
            (6.0, 4.0, 0.0),
            (30.0, 0.0, 0.0),
        )
    )
    record = luna44._run_character(arm="CALIBRATED", sequence=sequence)
    assert record["causality_reconciles"]
    assert record["routing_reconciliation"]["reconciles"]
    assert record["routing_enqueue_events"]
    assert record["receiver_reception_events"]
    assert record["runtime_events"]
    for hop in ("source_to_relay", "relay_to_destination"):
        reconciliation = record["routing_reconciliation"][hop]
        assert reconciliation["reconciles"]
        assert reconciliation["enqueued_count"] == reconciliation["received_count"]
        assert reconciliation["matched_count"] == reconciliation["enqueued_count"]
        assert reconciliation["unmatched_enqueue_count"] == 0
        assert reconciliation["orphan_reception_count"] == 0
        assert reconciliation["duplicate_count"] == 0
        assert reconciliation["payload_mismatch_count"] == 0
        assert reconciliation["timing_mismatch_count"] == 0
        assert reconciliation["route_path_mismatch_count"] == 0
    for enqueue in record["routing_enqueue_events"]:
        reception = next(
            item
            for item in record["receiver_reception_events"]
            if item["event_id"] == enqueue["event_id"]
        )
        assert enqueue["payload_bits"] == reception["payload_bits"]
        assert enqueue["scheduled_delivery_timestamp"] == reception["reception_timestamp"]
        assert enqueue["route_path"] == reception["route_path"]
        assert reception["receiver_state_transition"]["processed_events_after"] == (
            reception["receiver_state_transition"]["processed_events_before"] + 1
        )
    assert record["counts"]["source_emissions"] == record["counts"]["source_to_relay_transfers"]
    assert record["counts"]["source_emissions"] == record["counts"]["source_to_relay_receptions"]
    assert record["counts"]["source_to_relay_receptions"] == len(record["source_to_relay_receptions"])
    assert record["counts"]["relay_emissions"] == record["counts"]["relay_to_destination_transfers"]
    assert all(item["matches"] for item in record["relay_onward_transfer_checks"])
    assert all(
        item["classification"] in ("direct", "integration-mediated")
        for item in record["relay_emissions"]
    )
    assert record["counts"]["relay_integrated_emissions"] > 0
    assert all("m_peak" in item for item in record["source_emissions"])
    assert all("m_peak" in item for item in record["relay_emissions"])
    assert all(item["matches"] for item in record["canonical_emission_checks"]["source"])
    assert all(item["matches"] for item in record["relay_recurrence_checks"])
    for check in record["relay_recurrence_checks"]:
        assert check["dt"]["exact_match"]
        for key in (
            "x_after_decay",
            "z_after_decay",
            "x_after_input",
            "z_after_input",
            "discharge_amount",
            "x_post_discharge",
            "z_post_discharge",
        ):
            assert check[key]["matches"]
    assert record["relay_recurrence_reconciles"]
    for transfer_check in record["transfer_checks"]:
        assert transfer_check["identity_matches"]
        assert transfer_check["strict_future"]
        assert transfer_check["arrival_timestamp_check"]["matches"]
        assert transfer_check["model_b_check"]["matches"]
        emission = next(
            candidate
            for candidate in record["source_emissions"] + record["relay_emissions"]
            if candidate["event_id"] == transfer_check["event_id"]
        )
        assert transfer_check["arrival_timestamp_expected"] == emission["timestamp"] + 1.0
    assert record["resource_high_water"]["activity_count"] <= 1024
    assert record["resource_high_water"]["activity_high_water"] == sum(
        record["counts"][name]
        for name in ("source_emissions", "relay_emissions", "destination_emissions")
    )
    assert isinstance(record["counts"]["max_relay_z"], float)
    assert isinstance(record["counts"]["max_abs_relay_z"], float)
    aggregate = luna44._aggregate_arm([record])
    assert aggregate["max_relay_z"] == record["counts"]["max_relay_z"]
    assert aggregate["max_abs_relay_z"] == record["counts"]["max_abs_relay_z"]
    high_water = record["resource_high_water"]
    assert high_water["queue_peak"] < high_water["queue_capacity"]
    assert high_water["processed_events"] <= high_water["runtime_event_budget"]
    assert high_water["prediction_peak"] <= high_water["prediction_capacity"]
    assert high_water["eligibility_peak"] < high_water["eligibility_capacity_per_ledger"]
    assert all(
        item["peak"] < item["capacity"]
        for item in high_water["eligibility_ledgers"]
    )
    assert record["settling"]["completed"]


def test_route_reconciliation_accepts_independent_matching_records():
    enqueue, reception = _route_pair()

    result = luna44._reconcile_route_events([enqueue], [reception])

    assert result["reconciles"]
    assert result["enqueued_count"] == 1
    assert result["received_count"] == 1
    assert result["matched_count"] == 1
    assert result["mismatch_count"] == 0


@pytest.mark.parametrize(
    ("mutation", "expected_count"),
    [
        (lambda enqueue, reception: reception.update(payload_bits=luna44._bits(0.75)),
         "payload_mismatch_count"),
        (lambda enqueue, reception: reception.update(event_id="different-event"),
         "event_id_mismatch_count"),
        (lambda enqueue, reception: reception.update(receiver_node="destination"),
         "identity_mismatch_count"),
        (lambda enqueue, reception: reception.update(reception_timestamp=2.5),
         "timing_mismatch_count"),
        (lambda enqueue, reception: reception.update(route_path=["source", "other"]),
         "route_path_mismatch_count"),
        (lambda enqueue, reception: reception.update(lineage_id="different-lineage"),
         "provenance_mismatch_count"),
        (lambda enqueue, reception: reception.update(destination="other"),
         "identity_mismatch_count"),
        (lambda enqueue, reception: reception.update(event_type="input"),
         "provenance_mismatch_count"),
        (lambda enqueue, reception: reception.update(route_depth=2),
         "route_path_mismatch_count"),
        (lambda enqueue, reception: reception.update(causal_roots=["other"]),
         "provenance_mismatch_count"),
        (lambda enqueue, reception: reception.update(roots_truncated=True),
         "provenance_mismatch_count"),
        (lambda enqueue, reception: reception.update(originating_emission_id="other"),
         "provenance_mismatch_count"),
        (lambda enqueue, reception: reception.update(payload=0.75),
         "payload_mismatch_count"),
        (lambda enqueue, reception: reception.update(scheduled_delivery_timestamp=2.5),
         "timing_mismatch_count"),
        (lambda enqueue, reception: enqueue.update(enqueue_timestamp=2.0),
         "timing_mismatch_count"),
        (lambda enqueue, reception: reception.update(
            reception_timestamp=math.nextafter(2.0, math.inf)),
         "timing_mismatch_count"),
        (lambda enqueue, reception: (
            enqueue.update(payload=0.0, payload_bits=luna44._bits(0.0)),
            reception.update(payload=-0.0, payload_bits=luna44._bits(-0.0))),
         "payload_mismatch_count"),
    ],
)
def test_route_reconciliation_rejects_mismatched_copies(mutation, expected_count):
    enqueue, reception = _route_pair()
    mutation(enqueue, reception)

    result = luna44._reconcile_route_events([enqueue], [reception])

    assert not result["reconciles"]
    assert result[expected_count] > 0
    assert result["matched_count"] == 0
    assert result["unmatched_enqueue_count"] == 1


def test_route_reconciliation_rejects_source_mutation_with_details():
    enqueue, reception = _route_pair()
    reception["source"] = "other"

    result = luna44._reconcile_route_events([enqueue], [reception])

    assert not result["reconciles"]
    assert result["identity_mismatch_count"] == 1
    assert result["matched_count"] == 0
    assert result["unmatched_enqueue_count"] == 1
    check = result["checks"][0]
    assert not check["matches"]
    assert not check["identity_matches"]
    assert check["enqueue_source"] == "source"
    assert check["reception_source"] == "other"
    assert check["event_id"] == check["reception_event_id"] == "emission-1"
    assert check["enqueue_route_path"] == ["source", "relay"]
    assert check["reception_route_path"] == ["source", "relay"]
    assert check["queue_sequence"] == 1


@pytest.mark.parametrize(
    ("enqueues", "receptions", "expected_count"),
    [
        (lambda item: [item], lambda item: [], "unmatched_enqueue_count"),
        (lambda item: [], lambda item: [item], "orphan_reception_count"),
        (lambda item: [item], lambda item: [item, dict(item)], "duplicate_count"),
        (lambda item: [item, dict(item)], lambda item: [item], "duplicate_enqueue_count"),
    ],
)
def test_route_reconciliation_rejects_missing_or_duplicate_events(
    enqueues,
    receptions,
    expected_count,
):
    enqueue, reception = _route_pair()

    result = luna44._reconcile_route_events(enqueues(enqueue), receptions(reception))

    assert not result["reconciles"]
    assert result[expected_count] > 0


def test_route_reconciliation_is_one_to_one_by_admission_not_emission_id():
    enqueue, reception = _route_pair()
    second_enqueue, second_reception = deepcopy(enqueue), deepcopy(reception)
    second_enqueue.update(queue_sequence=2, destination="destination",
                          route_path=["source", "destination"])
    second_reception.update(queue_sequence=2, destination="destination",
                            receiver_node="destination",
                            route_path=["source", "destination"])
    result = luna44._reconcile_route_events(
        [enqueue, second_enqueue], [second_reception, reception],
    )
    assert result["reconciles"]
    assert result["matched_count"] == 2


def test_wrong_admission_identity_is_missing_and_orphan():
    enqueue, reception = _route_pair()
    reception["queue_sequence"] = 99
    result = luna44._reconcile_route_events([enqueue], [reception])
    assert not result["reconciles"]
    assert result["unmatched_enqueue_count"] == 1
    assert result["orphan_reception_count"] == 1
    assert any(check["reason"] == "orphan reception" for check in result["checks"])


def test_capture_observes_receiver_mutation_independently(monkeypatch, tmp_path):
    original = luna44.ExcursionCharacterRuntime._process_one
    original_reconcile = luna44._reconcile_route_events
    observations = []

    def changed_delivery(runtime, event):
        if event.event_type == luna44.EventType.EXCURSION:
            event = replace(event, payload=float(event.payload) + 0.125)
        return original(runtime, event)

    def observe_reconciliation(enqueued, received):
        result = original_reconcile(enqueued, received)
        observations.append((deepcopy(enqueued), deepcopy(received), result))
        return result

    monkeypatch.setattr(luna44.ExcursionCharacterRuntime, "_process_one", changed_delivery)
    monkeypatch.setattr(luna44, "_reconcile_route_events", observe_reconciliation)
    sequence = _synthetic_sequence(((0.0, 4.0, 0.0), (30.0, 0.0, 0.0)))
    with pytest.raises(luna44.RoutingEvidenceError,
                       match="provenance did not reconcile") as failure:
        luna44._run_character(arm="CALIBRATED", sequence=sequence)
    enqueued, received, reconciliation = observations[-1]
    assert enqueued and received
    assert reconciliation["payload_mismatch_count"] > 0
    assert enqueued[0]["payload_bits"] != received[0]["payload_bits"]
    captures = {arm: [] for arm in luna44.ARMS}
    captures["CALIBRATED"].append(failure.value.capture)
    manifest = luna44._persist_routing_evidence(
        tmp_path, {}, captures, {arm: [] for arm in luna44.ARMS},
    )
    assert not manifest["replay_equal"]
    for name in ("initial_enqueue", "initial_reception"):
        artifact = json.loads(
            (tmp_path / manifest["artifacts"][name]["path"]).read_bytes()
        )
        assert artifact["per_arm"]["CALIBRATED"][0]["capture_status"] == (
            "reconciliation_failed"
        )


def test_receiver_capture_requires_actual_processing(monkeypatch):
    original_receive = luna44.MultiExcursionNeuron.receive_event

    def skip_routed_event(neuron, event, queue=None):
        if event.event_type == luna44.EventType.EXCURSION:
            return None
        return original_receive(neuron, event, queue)

    monkeypatch.setattr(luna44.MultiExcursionNeuron, "receive_event", skip_routed_event)
    sequence = _synthetic_sequence(((0.0, 4.0, 0.0), (30.0, 0.0, 0.0)))
    with pytest.raises(RuntimeError, match="receiver did not process"):
        luna44._run_character(arm="CALIBRATED", sequence=sequence)


def test_raw_stream_persistence_and_replay_verification(tmp_path):
    sequence = _synthetic_sequence(((0.0, 4.0, 0.0), (30.0, 0.0, 0.0)))
    initial = {arm: [luna44._run_character(arm=arm, sequence=sequence)]
               for arm in luna44.ARMS}
    replay = {arm: [luna44._run_character(arm=arm, sequence=sequence)]
              for arm in luna44.ARMS}
    manifest = luna44._persist_routing_evidence(tmp_path, {}, initial, replay)
    assert manifest["replay_equal"]
    assert len(manifest["artifacts"]) == 4
    second_directory = tmp_path / "fresh-replay"
    second_directory.mkdir()
    assert manifest == luna44._persist_routing_evidence(
        second_directory, {}, initial, replay,
    )
    for name, reference in manifest["artifacts"].items():
        data = (tmp_path / reference["path"]).read_bytes()
        artifact = json.loads(data)
        assert hashlib.sha256(data).hexdigest() == reference["file_sha256"]
        assert luna44._artifact_digest(artifact) == reference["artifact_digest"]
        assert luna44._digest(artifact["per_arm"]) == reference["streams_digest"]
        field = ("routing_enqueue_events" if name.endswith("_enqueue")
                 else "receiver_reception_events")
        records = initial if name.startswith("initial_") else replay
        for arm in luna44.ARMS:
            retained = artifact["per_arm"][arm][0]
            assert retained["events"] == records[arm][0][field]
            assert retained["stream_digest"] == luna44._digest(retained["events"])
    replay["CALIBRATED"][0]["receiver_reception_events"][0]["payload_bits"] = "bad"
    manifest = luna44._persist_routing_evidence(tmp_path, {}, initial, replay)
    assert not manifest["replay_equal"]
    assert manifest["streams"]["enqueue"]["equal"]
    assert not manifest["streams"]["reception"]["equal"]


def test_direct_and_integration_mediated_emission_classification():
    emissions = [
        {"event_id": "direct-emission", "payload": 0.4},
        {"event_id": "integrated-emission", "payload": 0.5},
    ]
    recurrence_checks = [
        {
            "trace_emission_id": "direct-emission",
            "expected_classification": "direct",
            "matches": True,
        },
        {
            "trace_emission_id": "integrated-emission",
            "expected_classification": "integrated_discharge",
            "matches": True,
        },
    ]
    classified = luna44._classify_relay_emissions(
        emissions,
        [],
        recurrence_checks,
        integration_enabled=True,
    )
    assert [item["classification"] for item in classified] == [
        "direct",
        "integration-mediated",
    ]
    assert classified[1]["integration_trace_check"] == recurrence_checks[1]


def test_control_distinction_includes_calibrated_and_is_omitted_when_equal():
    equal = {
        arm: {
            "relay_integrated_emissions": 4,
            "relay_direct_emissions": 2,
        }
        for arm in luna44.ARMS
    }
    assert luna44._observed_control_distinctions(equal) is None
    distinct = {
        **equal,
        "CALIBRATED": {
            "relay_integrated_emissions": 7,
            "relay_direct_emissions": 1,
        },
    }
    result = luna44._observed_control_distinctions(distinct)
    assert result is not None
    assert set(result["per_arm_counts"]) == {"DISABLED", "DEFAULT", "CALIBRATED"}
    assert result["per_arm_counts"]["CALIBRATED"] == distinct["CALIBRATED"]
    assert {
        (item["left_arm"], item["right_arm"])
        for item in result["observed_differences"]
    } == {("DEFAULT", "CALIBRATED"), ("CALIBRATED", "DISABLED")}
    assert "no difference is required" in luna44.experiment_config()[
        "control_interpretation"
    ].lower()


def test_execution_provenance_uses_ancestors_not_origin_main(monkeypatch):
    calls = []

    def fake_git(*args):
        calls.append(args)
        if args == ("branch", "--show-current"):
            return "fixture-review-branch"
        if args == ("rev-parse", "HEAD"):
            return "execution-head"
        if args == ("status", "--porcelain", "--untracked-files=all"):
            return ""
        if args == ("merge-base", luna44.AUTHORIZATION_REVISION, "execution-head"):
            return luna44.AUTHORIZATION_REVISION
        if args == ("merge-base", luna44.FIXTURE_REVISION, "execution-head"):
            return luna44.FIXTURE_REVISION
        raise AssertionError(f"unexpected git query: {args!r}")

    monkeypatch.setattr(luna44, "_git_output", fake_git)
    monkeypatch.setattr(luna44, "_runner_sha256", lambda: "runner-sha")
    provenance = luna44._collect_execution_provenance()
    assert provenance["execution_revision"] == "execution-head"
    assert provenance["authorization_merge_base"] == luna44.AUTHORIZATION_REVISION
    assert provenance["fixture_merge_base"] == luna44.FIXTURE_REVISION
    assert provenance["runner_sha256"] == "runner-sha"
    assert provenance["authorization_handoff_sha256"] == luna44.AUTHORIZATION_HANDOFF_SHA256
    assert luna44._authorization_handoff_sha256() == luna44.AUTHORIZATION_HANDOFF_SHA256
    assert all("origin/main" not in call for call in calls)


def test_blocked_provenance_keeps_actual_head_nonnull(monkeypatch):
    def fake_git(*args):
        if args == ("branch", "--show-current"):
            return "fixture-review-branch"
        if args == ("rev-parse", "HEAD"):
            return "actual-execution-head"
        if args == ("status", "--porcelain", "--untracked-files=all"):
            return ""
        if args == ("merge-base", luna44.AUTHORIZATION_REVISION, "actual-execution-head"):
            return luna44.AUTHORIZATION_REVISION
        if args == ("merge-base", luna44.FIXTURE_REVISION, "actual-execution-head"):
            return "wrong-ancestor"
        raise AssertionError(f"unexpected git query: {args!r}")

    monkeypatch.setattr(luna44, "_git_output", fake_git)
    with pytest.raises(luna44.ProvenanceError) as failure:
        luna44._collect_execution_provenance()
    assert failure.value.provenance["execution_revision"] == "actual-execution-head"
    assert failure.value.provenance["execution_revision"] is not None


def test_float_comparison_policy_rejects_values_outside_declared_tolerance():
    expected = 1.0
    within = expected + math.ulp(expected)
    outside = expected + 1e-12
    assert luna44._float_check(within, expected)["matches"]
    assert not luna44._float_check(outside, expected)["matches"]


def test_cross_platform_derived_audit_difference_uses_tolerance_and_is_retained():
    sequence = _synthetic_sequence(
        (
            (0.0, 4.0, 0.0),
            (3.0, 4.0, 0.0),
            (6.0, 4.0, 0.0),
            (30.0, 0.0, 0.0),
        )
    )
    point = sequence["points"][0]
    computed = float.fromhex(point["x"]["hex"]) + float.fromhex(point["y"]["hex"])
    audit = math.nextafter(computed, math.inf)
    point["audit_x_plus_y"] = luna44._float_record(audit)
    luna44._validate_sequence(sequence)
    record = luna44._run_character(arm="CALIBRATED", sequence=sequence)
    comparison = record["point_inputs"][0]["audit_comparison"]
    assert comparison["observed"] == computed
    assert comparison["expected"] == audit
    assert comparison["error"] == abs(computed - audit)
    assert comparison["bound"] == luna44._float_tolerance(computed, audit)
    assert comparison["matches"]


def test_primary_artifact_envelopes_have_provenance_and_self_excluding_digests():
    _, fixture_source = luna44.load_fixture()
    config_digest = luna44._digest(luna44.experiment_config())
    provenance = {
        "authorization_revision": luna44.AUTHORIZATION_REVISION,
        "authorization_handoff_sha256": luna44.AUTHORIZATION_HANDOFF_SHA256,
        "fixture_revision": luna44.FIXTURE_REVISION,
        "execution_revision": "execution-head",
        "runner_sha256": "runner-hash",
        "python": sys.version,
        "python_implementation": sys.implementation.name,
        "platform": "test-platform",
        "float_info": {"epsilon": sys.float_info.epsilon},
    }
    metadata = luna44._artifact_metadata(provenance, fixture_source, config_digest)
    schemas = ("config", "results", "summary", "replay")
    for schema in schemas:
        artifact = luna44._seal_artifact(
            {**metadata, "schema": f"test-{schema}", "payload": []}
        )
        assert artifact["authorization_revision"] == luna44.AUTHORIZATION_REVISION
        assert artifact["authorization_handoff_sha256"] == luna44.AUTHORIZATION_HANDOFF_SHA256
        assert artifact["fixture_revision"] == luna44.FIXTURE_REVISION
        assert artifact["runner_revision"] == artifact["execution_revision"] == "execution-head"
        assert artifact["fixture_source_provenance"] == fixture_source
        assert artifact["config_digest"] == config_digest
        assert artifact["environment"]["platform"] == "test-platform"
        assert artifact["artifact_digest"] == luna44._artifact_digest(artifact)
    envelope = luna44._replay_envelope_digest(["first", "second"], config_digest)
    assert envelope != luna44._replay_envelope_digest(["second", "first"], config_digest)
    assert envelope != luna44._replay_envelope_digest(["first", "second"], "other-config")


def test_run_experiment_refuses_to_overwrite_existing_artifacts(tmp_path):
    output_directory = tmp_path / "retained-run"
    output_directory.mkdir()

    with pytest.raises(FileExistsError):
        luna44.run_experiment(output_directory)

    assert list(output_directory.iterdir()) == []
