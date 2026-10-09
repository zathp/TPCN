from __future__ import annotations

import hashlib
import inspect
import json
from pathlib import Path
import subprocess

import pytest
from experiments.luna53 import run as luna53


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "artifacts" / "luna53"
LUNA46_PIN_REVISION = "04305a2917195888cbbcccf378eba7971551e9b5"
LUNA46_PIN_PATH = "artifacts/luna46-depth-scaling-diagnostic-corrective-20261006.json"
LUNA46_PIN_BLOB = "9506369d97babf7bc0ef15ed52efb738dcdcd549"
LUNA46_PIN_LF_SHA256 = "54220205537184dadc26eba3c59f7e9b36f01db579fd895339728e089e313d51"
LUNA46_PIN_CRLF_SHA256 = "0d32926f6f72a77a5b34eb054e1e46e9ece95cef3d6145e7892957cf3727722e"


def test_luna56_luna53_pin_verifies_historical_object_and_exact_materialization(
    tmp_path,
    monkeypatch,
):
    actual_blob = subprocess.check_output(
        ["git", "rev-parse", f"{LUNA46_PIN_REVISION}:{LUNA46_PIN_PATH}"],
        cwd=ROOT,
        text=True,
    ).strip()
    assert actual_blob == LUNA46_PIN_BLOB
    canonical = subprocess.check_output(
        ["git", "show", f"{LUNA46_PIN_REVISION}:{LUNA46_PIN_PATH}"],
        cwd=ROOT,
    )
    crlf = canonical.replace(b"\n", b"\r\n")
    assert hashlib.sha256(canonical).hexdigest() == LUNA46_PIN_LF_SHA256
    assert hashlib.sha256(crlf).hexdigest() == LUNA46_PIN_CRLF_SHA256
    monkeypatch.setattr(luna53, "ROOT", tmp_path)
    checkout = tmp_path / LUNA46_PIN_PATH
    checkout.parent.mkdir(parents=True)

    checkout.write_bytes(canonical)
    _, lf_identity = luna53._verified_file(
        LUNA46_PIN_PATH,
        LUNA46_PIN_CRLF_SHA256,
        canonical_bytes=canonical,
    )
    assert lf_identity["checkout_materialization"] == "exact"

    checkout.write_bytes(crlf)
    _, crlf_identity = luna53._verified_file(
        LUNA46_PIN_PATH,
        LUNA46_PIN_CRLF_SHA256,
        canonical_bytes=canonical,
    )
    assert crlf_identity["checkout_materialization"] == (
        "exact-Git-LF-to-CRLF-checkout"
    )

    mutations = (
        canonical.replace(b'"schema"', b"'schema'", 1),
        canonical.replace(b"320", b"321", 1),
        canonical + b" ",
        canonical.replace(b" ", b"", 1),
        canonical.replace(b'"sequences"', b'\r\n"sequences"', 1),
        canonical.replace(b"\n", b"\r", 1),
        canonical[:-1],
    )
    for mutation in mutations:
        assert mutation != canonical
        checkout.write_bytes(mutation)
        with pytest.raises(luna53.GateError, match="beyond exact Git line-ending"):
            luna53._verified_file(
                LUNA46_PIN_PATH,
                LUNA46_PIN_CRLF_SHA256,
                canonical_bytes=canonical,
            )

    monkeypatch.setattr(luna53, "ROOT", ROOT)
    with pytest.raises(luna53.GateError, match="Git blob mismatch"):
        luna53._historical_blob_bytes(
            LUNA46_PIN_REVISION,
            LUNA46_PIN_PATH,
            "0" * 40,
        )
    with pytest.raises(luna53.GateError, match="missing pinned historical object"):
        luna53._historical_blob_bytes(
            "missing-historical-revision",
            LUNA46_PIN_PATH,
            LUNA46_PIN_BLOB,
        )


def _synthetic_arrivals() -> list[dict]:
    # A unit mechanism fixture only; it is not part of Luna-53 retained evidence.
    return [
        {
            "event_id": "synthetic:1",
            "source_queue_sequence": 4,
            "timestamp": 0.0,
            "payload": 0.6,
            "payload_bits": luna53.float_bits(0.6),
            "source": "relay",
            "destination": "destination",
            "event_type": "excursion",
            "lineage_id": 1,
            "route_path": ["relay", "destination"],
            "route_depth": 1,
        },
        {
            "event_id": "synthetic:2",
            "source_queue_sequence": 9,
            "timestamp": 80.0,
            "payload": 0.6,
            "payload_bits": luna53.float_bits(0.6),
            "source": "relay",
            "destination": "destination",
            "event_type": "excursion",
            "lineage_id": 2,
            "route_path": ["relay", "destination"],
            "route_depth": 1,
        },
    ]


def test_pinned_inputs_reconcile_without_running_neurons():
    identities, data = luna53.verify_provenance()

    assert identities["authorization_revision"] == luna53.AUTHORIZATION_REVISION
    assert identities["phase_reconciliation"]["initial"]["stream_count"] == 320
    assert identities["phase_reconciliation"]["replay"]["stream_count"] == 320
    assert identities["phase_reconciliation"]["initial"]["destination_reception_count"] == 235
    assert identities["phase_reconciliation"]["replay"]["destination_reception_count"] == 235
    assert data["phase_streams"]["initial"] == data["phase_streams"]["replay"]


def test_intervention_changes_only_destination_slow_decay():
    config = json.loads((ROOT / luna53.CONFIG_PATH).read_text(encoding="utf-8"))
    historical = config["historical_destination"]
    control = dict(historical)
    treatment = dict(historical)
    control["integration"] = dict(historical["integration"])
    treatment["integration"] = dict(historical["integration"])
    control["integration"]["decay_rate_z"] = 0.0125
    treatment["integration"]["decay_rate_z"] = 0.00125

    assert luna53._diff_paths(control, treatment) == ["integration.decay_rate_z"]
    assert luna53._make_destination_config(config, "control").event_budget == 4096
    assert luna53._make_destination_config(config, "intervention").integration.decay_rate_z == 0.00125


def test_e2_runtime_and_independent_recurrence_link_discharge_to_emission():
    config_json = json.loads((ROOT / luna53.CONFIG_PATH).read_text(encoding="utf-8"))
    control = luna53.run_stream(
        _synthetic_arrivals(),
        luna53._make_destination_config(config_json, "control"),
    )
    intervention = luna53.run_stream(
        _synthetic_arrivals(),
        luna53._make_destination_config(config_json, "intervention"),
    )

    assert control["recurrence_oracle"]["passed"]
    assert control["discharge_count"] == 0
    assert control["canonical_emission_count"] == 0
    assert intervention["recurrence_oracle"]["passed"]
    assert intervention["discharge_count"] == 1
    assert intervention["canonical_emission_count"] == 1
    assert intervention["linked_integration_emissions"][0]["emission_linked"]
    assert intervention["linked_integration_emissions"][0]["canonical_emission"]["event_id"]
    assert intervention["execution"]["completed"]
    assert intervention["execution"]["pending_event_count"] == 0


def test_neuron_runner_interface_does_not_accept_evaluation_class():
    parameters = inspect.signature(luna53.run_stream).parameters
    assert set(parameters) == {"arrivals", "config"}
    assert "category" not in parameters


def test_scientific_replay_digest_ignores_only_phase_metadata():
    config = json.loads((ROOT / luna53.CONFIG_PATH).read_text(encoding="utf-8"))
    summary = {"condition": "control", "classes": {}}
    initial = [{
        "stream_id": "s1",
        "phase": "initial",
        "reset_identity": "initial:control:s1",
        "events": [{"event_id": "e1", "payload": 0.6}],
    }]
    replay = [{
        **initial[0],
        "phase": "replay",
        "reset_identity": "replay:control:s1",
        "events": [{"event_id": "e1", "payload": 0.6}],
    }]

    initial_payload = luna53._scientific_payload("control", config, summary, initial)
    replay_payload = luna53._scientific_payload("control", config, summary, replay)
    assert luna53.digest(initial_payload) == luna53.digest(replay_payload)

    replay[0]["events"][0]["payload"] = 0.7
    changed_payload = luna53._scientific_payload("control", config, summary, replay)
    assert luna53.digest(initial_payload) != luna53.digest(changed_payload)


def test_saved_run_artifacts_are_complete_and_replay_exact():
    summary = luna53.summarize_outputs()
    saved_summary = json.loads((OUTPUTS / "summary.json").read_bytes())
    assert saved_summary == summary
    assert luna53._artifact_payload_digest(saved_summary)
    assert summary["retained_initial_replay_exact"]
    assert summary["no_reception_invariant"] == "PASS"
    assert summary["paired_causal_class_summary"]["classes"][
        "TEMPORAL-RETENTION-LIMITED"
    ]["n"] == 33
    assert summary["paired_causal_class_summary"]["classes"]["DRIVE-LIMITED"]["n"] == 75
    assert summary["paired_causal_class_summary"]["classes"]["NO-RECEPTIONS"]["n"] == 212
    assert luna53._artifact_payload_digest(summary)

    for relative_path, identity in summary["phase_condition_executions"].items():
        artifact_path = ROOT / relative_path
        assert artifact_path.stat().st_size == identity["bytes"]
        assert luna53.sha256(artifact_path.read_bytes()) == identity["sha256"]

    for condition in ("control", "intervention"):
        for phase in ("initial", "replay"):
            path = OUTPUTS / f"luna53-{condition}-{phase}.json"
            record = json.loads(path.read_bytes())
            assert record["fresh_process_execution"]
            assert record["labels_entered_runtime"] is False
            assert record["upstream_route_executed"] is False
            assert record["destination_outputs_rerouted"] is False
            assert record["baseline_compatibility"]["passed"]
