from __future__ import annotations

import hashlib
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


def test_topology_and_only_relay_integration_vary_by_arm():
    config = luna44.experiment_config()
    assert config["authorization_revision"] == luna44.AUTHORIZATION_REVISION
    assert config["fixture"]["revision"] == luna44.FIXTURE_REVISION
    assert config["fixture"]["canonical_sha256"] == luna44.FIXTURE_SHA256
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
