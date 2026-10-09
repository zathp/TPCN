from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess

import pytest

from experiments.luna54 import run as luna54
from experiments.luna55 import run as luna55


ROOT = Path(__file__).resolve().parents[1]


def test_luna55_retained_phase_pins_and_population_partition():
    selection, categories, retained = luna55._phase_pins_and_populations()
    compatibility = luna55._verify_phase_compatibility(selection, retained)

    assert len(categories) == 320
    assert len(luna55.TARGET_IDS) == 16
    assert compatibility["passed"]
    assert compatibility["phase_checks"]["initial"]["matched_arrivals"] == 235
    assert compatibility["phase_checks"]["replay"]["matched_historical_destination_traces"] == 235


def test_luna55_reauthenticates_stale_luna46_file_pin_without_mutating_history():
    sources, _protocol, _config, _frozen, note = (
        luna55._load_verified_luna54_sources()
    )

    assert note["git_object_and_checkout_match"]
    assert note["semantic_digest_passed"]
    assert note["legacy_helper_identity_verified"]
    assert note["legacy_helper_expected_length"] == 2_337_377
    assert note["observed_length"] == 2_337_377
    assert note["legacy_helper_sha256"] == note["checkout_sha256"]
    assert sources["l46_identity"]["git_blob"] == luna55.LUNA46_EXPECTED_BLOB


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write_fixture_checkout(tmp_path, monkeypatch, content: bytes) -> str:
    monkeypatch.setattr(luna55.luna53, "ROOT", tmp_path)
    relative = "fixture/same-path.json"
    checkout = tmp_path / relative
    checkout.parent.mkdir(parents=True, exist_ok=True)
    checkout.write_bytes(content)
    return relative


def test_luna55_exact_lf_and_crlf_checkouts_and_materialized_hashes(tmp_path, monkeypatch):
    canonical = b'{"value": 1}\n'
    crlf = canonical.replace(b"\n", b"\r\n")
    relative = _write_fixture_checkout(tmp_path, monkeypatch, canonical)
    raw_lf, identity_lf = luna55._read_verified_checkout(
        relative, _sha256(canonical), canonical
    )
    assert raw_lf == canonical
    assert identity_lf["checkout_sha256"] == _sha256(canonical)

    (tmp_path / relative).write_bytes(crlf)
    raw_crlf, identity_crlf = luna55._read_verified_checkout(
        relative, _sha256(canonical), canonical
    )
    assert raw_crlf == crlf
    assert identity_crlf["checkout_materialization"] == (
        "exact-Git-LF-to-CRLF-checkout"
    )

    # The same recorded CRLF identity is valid whether today's checkout is LF
    # (different current SHA) or CRLF (equal current and historical SHA).
    (tmp_path / relative).write_bytes(canonical)
    _raw, lf_identity = luna55._read_verified_checkout(
        relative, _sha256(crlf), canonical, expected_length=len(crlf)
    )
    assert lf_identity["checkout_sha256"] != _sha256(crlf)
    (tmp_path / relative).write_bytes(crlf)
    _raw, crlf_identity = luna55._read_verified_checkout(
        relative, _sha256(crlf), canonical, expected_length=len(crlf)
    )
    assert crlf_identity["checkout_sha256"] == _sha256(crlf)


@pytest.mark.parametrize(
    "mutate",
    [
        lambda data: data.replace(b"value", b"Value", 1),
        lambda data: data.replace(b"1", b"2", 1),
        lambda data: data.replace(b": ", b":", 1),
        lambda data: data.replace(b":", b": ", 1),
        lambda data: data.replace(b"value", b"valu", 1),
        lambda data: data.replace(b"\n", b"x\n", 1),
        lambda data: data + b" ",
        lambda data: data[:-1],
        lambda data: data + b"\n",
        lambda data: data.replace(b"\n", b"\r\n", 1) + b"\n",
        lambda data: data.replace(b"\n", b"\r", 1),
    ],
    ids=[
        "changed-character",
        "changed-number",
        "removed-space",
        "added-space",
        "removed-character",
        "added-character",
        "added-content",
        "removed-final-lf",
        "invalid-extra-eof-lf",
        "mixed-lf-crlf",
        "lone-cr",
    ],
)
def test_luna55_checkout_rejects_changed_or_malformed_materializations(
    tmp_path, monkeypatch, mutate
):
    canonical = b'{"value": 1}\n'
    substituted = mutate(canonical)
    assert substituted != canonical
    relative = _write_fixture_checkout(tmp_path, monkeypatch, substituted)

    # The file remains at the same path; only its bytes have been substituted.
    with pytest.raises(luna55.GateError, match="checkout verification failed"):
        luna55._read_verified_checkout(relative, _sha256(canonical), canonical)


def test_luna55_rejects_substituted_content_at_the_pinned_checkout_path(
    tmp_path, monkeypatch
):
    canonical = b'{"value": 1}\n'
    relative = _write_fixture_checkout(tmp_path, monkeypatch, canonical)
    (tmp_path / relative).write_bytes(b'{"value": 2}\n')

    with pytest.raises(luna55.GateError, match="checkout verification failed"):
        luna55._read_verified_checkout(relative, _sha256(canonical), canonical)


def test_luna55_rejects_wrong_revision_or_blob_and_missing_historical_object(
    monkeypatch,
):
    with pytest.raises(luna55.GateError, match="revision differs"):
        luna55._historical_blob_bytes(
            "HEAD", luna55.LUNA46_PATH, luna55.LUNA46_EXPECTED_BLOB
        )
    with pytest.raises(luna55.GateError, match="Git blob mismatch"):
        luna55._historical_blob_bytes(
            luna55.AUTHORIZATION_REVISION, luna55.LUNA46_PATH, "0" * 40
        )

    def missing_object_git(*args, binary=False):
        if args[0] == "rev-parse":
            return luna55.LUNA46_EXPECTED_BLOB
        if args[0] == "cat-file":
            raise subprocess.CalledProcessError(1, ["git", *args])
        raise AssertionError(f"unexpected Git call: {args}")

    monkeypatch.setattr(luna55, "_git", missing_object_git)
    with pytest.raises(luna55.GateError, match="missing pinned historical Git object"):
        luna55._historical_blob_bytes(
            luna55.AUTHORIZATION_REVISION,
            luna55.LUNA46_PATH,
            luna55.LUNA46_EXPECTED_BLOB,
        )


def test_luna55_rejects_missing_current_checkout_file(tmp_path, monkeypatch):
    monkeypatch.setattr(luna55.luna53, "ROOT", tmp_path)
    with pytest.raises(luna55.GateError, match="checkout verification failed"):
        luna55._read_verified_checkout(
            "missing/current-file.json", _sha256(b'{"value":1}\n'), b'{"value":1}\n'
        )


def test_luna55_rejects_unrelated_historical_hash_or_length(tmp_path, monkeypatch):
    canonical = b'{"value":1}\n'
    relative = _write_fixture_checkout(tmp_path, monkeypatch, canonical)

    with pytest.raises(luna55.GateError, match="historical SHA-256"):
        luna55._read_verified_checkout(relative, "0" * 64, canonical)
    with pytest.raises(luna55.GateError, match="canonical byte length"):
        luna55._read_verified_checkout(
            relative,
            _sha256(canonical),
            canonical,
            expected_length=len(canonical) + 1,
        )


def test_luna55_has_only_two_frozen_factorial_settings():
    selection = json.loads(
        (ROOT / "experiments/luna55/config.json").read_text(encoding="utf-8")
    )
    frozen = json.loads(
        (ROOT / "artifacts/luna45-depth2-frozen-config-20261006-r2/config.json").read_text(
            encoding="utf-8"
        )
    )
    nodes = frozen["neuron_configurations"]["DESTINATION_CALIBRATED"]
    expected = {
        "HH": (0.0125, 0.0125, []),
        "RH": (0.00125, 0.0125, ["relay.integration.decay_rate_z"]),
        "HR": (0.0125, 0.00125, ["destination.integration.decay_rate_z"]),
        "RR": (
            0.00125,
            0.00125,
            ["destination.integration.decay_rate_z", "relay.integration.decay_rate_z"],
        ),
    }
    for arm, (relay_rate, destination_rate, changed_paths) in expected.items():
        relay, destination, _ = luna55._make_configs(
            frozen, selection["conditions"][arm]
        )
        relay_record = luna54.jsonable(relay)
        destination_record = luna54.jsonable(destination)
        baseline = {"relay": nodes["relay"], "destination": nodes["destination"]}
        actual = {"relay": relay_record, "destination": destination_record}
        assert relay.integration.decay_rate_z == relay_rate
        assert destination.integration.decay_rate_z == destination_rate
        assert luna54._diff_paths(baseline, actual) == changed_paths


def test_destination_response_requires_linked_emission_and_complete_roots():
    row = {
        "destination_integration_traces": [
            {"discharge_amount": 1.0, "emission_id": "destination:1"}
        ],
        "destination_emissions": [{"event_id": "destination:1"}],
        "destination_discharge_count": 1,
        "route_lineage_authenticated": True,
        "route_links_complete": True,
        "destination_receptions": [{"roots_truncated": False}],
    }

    assert luna55._response_l54(row)
    truncated = deepcopy(row)
    truncated["destination_receptions"][0]["roots_truncated"] = True
    assert not luna55._response_l54(truncated)
    unlinked = deepcopy(row)
    unlinked["destination_emissions"] = []
    assert not luna55._response_l54(unlinked)


def test_destination_only_response_requires_linked_emission_and_matched_roots():
    row = {
        "integration_traces": [
            {"discharge_amount": 1.0, "emission_id": "destination:1"}
        ],
        "emissions": [{"event_id": "destination:1"}],
        "discharge_count": 1,
        "root_lineage_complete": True,
    }
    assert luna55._response_l53(row)
    assert not luna55._response_l53({**row, "root_lineage_complete": False})


def test_composed_rr_preserves_relay_route_identity_from_rh():
    selection, _categories, retained = luna55._phase_pins_and_populations()
    rr = luna55._json(luna55.OUTPUT / "rr-initial.json")
    relay_only = luna55._phase_arm_rows("RH", "initial", retained, rr)
    composed = luna55._phase_arm_rows("RR", "initial", retained, rr)
    relay_by_id = {row["stream_id"]: row for row in relay_only}
    composed_by_id = {row["stream_id"]: row for row in composed}

    assert set(relay_by_id) == set(composed_by_id) == {
        row["stream_id"] for row in selection["streams"]
    }
    assert all(
        relay_by_id[stream_id]["route_signature"]
        == composed_by_id[stream_id]["route_signature"]
        for stream_id in relay_by_id
    )
