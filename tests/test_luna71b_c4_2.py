from __future__ import annotations

import ast
import json
import hashlib
import importlib.util
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch
import struct
import sys
import threading
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "experiments" / "luna71b_c4_2"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.luna71b_c4_2.ppc11.compare import _p11_stop_alignment, _branch_observations, _shape_gaps, _parameter_manifest_digest, compare_pair
from experiments.luna71b_c4_2.ppc11.capture import SourceCapture
from experiments.luna71b_c4_2.ppc11.driver import (
    FIXTURE_MANIFEST_SCHEMA,
    PLAN_SHA256,
    PreflightError,
    _source_revision,
    _validate_fixture_manifest,
    run_authorized_pair,
    verify_preflight,
)
from experiments.luna71b_c4_2.ppc11.pairing import PairEventGate
from experiments.luna71b_c4_2.ppc11.schema import BRANCHES, RECORDS, encode_payload, f64, validate_record
from experiments.luna71b_c4_2.ppc11.trace import TraceWriter, read_trace

ARTIFACTS = EXPERIMENT / "test-artifacts"


def _payloads(mismatch_drive: bool = False) -> list[tuple[str, dict]]:
    enc = encode_payload
    anchor = {key: value for key, value in (
        ("exposure_id", "seed17:A:train:example-1"), ("event_id", "event-1"),
        ("source", "input:A"), ("destination", "sequence"), ("event_type", "input"),
    )}
    event = {"kind": "input", "value": "A"}
    queue_fields = {"anchor": anchor, "event_type": "input", "payload": event,
                    "timestamp": 0.25, "queue_sequence": 0,
                    "priority_key": [0.25, 0], "admission_outcome": "ADMITTED",
                    "occupancy_before": 0, "occupancy_after": 1}
    records: list[tuple[str, dict]] = [
        ("input_event", {"event_type": "input", "payload": event, "payload_type": "dict",
                          "timestamp": 0.25, "input_order": 0, "channel_id": "input:A", "event_id": "event-1"}),
        ("enqueue", {**queue_fields, "enqueue_order": 0}),
        ("schedule", {"anchor": anchor, "event_type": "input", "payload": event,
                       "timestamp": 0.25, "queue_sequence": 0, "priority_key": [0.25, 0],
                       "tie_break_cause": "timestamp_then_assigned_sequence"}),
        ("dequeue", {"anchor": anchor, "event_type": "input", "payload": event,
                      "timestamp": 0.25, "queue_sequence": 0, "priority_key": [0.25, 0],
                      "dequeue_order": 0, "tie_break_cause": "timestamp_then_assigned_sequence"}),
        ("process", {"anchor": anchor, "event_type": "input", "payload": event,
                      "timestamp": 0.25, "queue_sequence": 0, "process_order": 0}),
        ("prediction_create", {"prediction_id": "p1", "expected_symbol": "A", "created_at": 0.25,
                               "due_at": 1.0, "expires_at": 1.5}),
        ("prediction_match", {"prediction_id": "p1", "observed_symbol": "A", "matched_at": 1.0, "outcome": "matched"}),
        ("omission_resolve", {"prediction_id": "p1", "omitted_symbol": "B", "omission_at": 1.0, "outcome": "resolved"}),
        ("omission_route", {"prediction_id": "p1", "route": ["sequence", "readout"], "payload": event,
                             "event_id": "omit-1", "routed_at": 1.0}),
        ("omission_delivery", {"prediction_id": "p1", "route": ["sequence", "readout"], "payload": event,
                                "event_id": "omit-1", "delivered_at": 1.1, "outcome": "delivered"}),
        ("readout_feature", {"decision_id": "d1", "decision_at": 1.1, "feature": 0.0}),
        ("readout_drive", {"decision_id": "d1", "class_index": 0, "weight": 1.0, "bias": 0.0,
                            "feature": 0.0, "drive": -0.0 if mismatch_drive else 0.0}),
        ("readout_activation", {"decision_id": "d1", "class_index": 0, "pre_transfer": 0.0, "post_transfer": 0.0}),
        ("readout_decision", {"decision_id": "d1", "winner": 0, "tie_set": [0],
                               "tie_break_order": [0, 1, 2, 3], "tie_break_result": 0}),
        ("eligibility_create", {"trace_id": "t1", "owner": "ledger", "trace_kind": "weight", "value": 1.0,
                                 "created_at": 1.0, "expires_at": 2.0}),
        ("eligibility_expire", {"trace_id": "t1", "owner": "ledger", "expired_at": 2.0,
                                 "expiry_boundary": "strictly_after", "value": 1.0}),
        ("eligibility_consume", {"trace_id": "t1", "owner": "ledger", "consumed_at": 1.5,
                                  "value": 1.0, "outcome": "matched"}),
        ("eligibility_admission", {"trace_id": "t1", "owner": "ledger", "capacity": 4,
                                    "occupancy_before": 0, "decision": "ADMITTED", "reason": "capacity_available"}),
        ("feedback_schedule", {"feedback_id": "f1", "origin_id": "p1", "due_at": 2.0,
                                "scheduled_at": 1.0, "sign": 1, "magnitude": 1.0}),
        ("feedback_apply", {"feedback_id": "f1", "origin_id": "p1", "due_at": 2.0,
                             "applied_at": 2.0, "application_order": 4, "sign": 1, "magnitude": 1.0}),
        ("feedback_reject", {"feedback_id": "f1", "origin_id": "p1", "rejected_at": 2.0,
                              "reason": "duplicate", "duplicate": True}),
        ("parameter_initial", {"manifest_sha256": "c" * 64, "parameters": {"w": 0.0}}),
        ("parameter_transition", {"parameter_id": "w0", "parameter_kind": "weight", "old_value": 0.0,
                                   "new_value": 1.0, "cause": "reward", "transition_order": 0, "timestamp": 2.0}),
        ("parameter_final", {"manifest_sha256": "d" * 64, "parameters": {"w": 1.0}}),
        ("classification_output", {"predicted_class": 0, "output_at": 1.2,
                                    "emissions": [{"event_id": "out-1", "timestamp": 1.2}]}),
        ("queue_state", {"occupancy": 1, "capacity": 8, "pending": [{"event_id": "event-1", "priority": [0.25, 0]}]}),
        ("admission_decision", {"anchor": anchor, "admission_outcome": "ADMITTED",
                                 "occupancy_before": 0, "occupancy_after": 1, "queue_sequence": 0}),
        ("event_processed", {"event_id": "event-1", "processed_at": 0.25, "process_order": 0, "processed_count": 1}),
    ]
    index = next(i for i, (kind, _) in enumerate(records) if kind == "readout_decision")
    extras = []
    for class_index in range(1, 4):
        extras.extend([
            ("readout_drive", {"decision_id": "d1", "class_index": class_index,
                               "weight": 1.0, "bias": 0.0, "feature": 0.0, "drive": 0.0}),
            ("readout_activation", {"decision_id": "d1", "class_index": class_index,
                                    "pre_transfer": 0.0, "post_transfer": 0.0}),
        ])
    records[index:index] = extras
    return [(kind, enc(payload)) for kind, payload in records]


def _identity(side: str) -> dict:
    return {"side": side, "run_id": f"run-{side}",
            "source_revision": "11b6f52e9aa6725af69bcd3cd098bb2c62e78b76+sha256:" + ("a" if side == "original" else "b") * 64,
            "runtime_manifest_sha256": ("a" if side == "original" else "b") * 64,
            "seed": 17, "arm": "A", "split": "train", "example_id": "example-1",
            "exposure_id": "seed17:A:train:example-1"}


def _write(path: Path, side: str, *, mismatch: bool = False,
           reorder: bool = False, omit: str | None = None,
           positive_branch: str | None = None,
           missing_branch: str | None = None) -> None:
    with TraceWriter(path, identity=_identity(side)) as writer:
        records = _payloads(mismatch and side == "instrumented")
        if omit is not None and side == "instrumented":
            records = [record for record in records if record[0] != omit]
        if reorder and side == "instrumented":
            records[0], records[1] = records[1], records[0]
        if positive_branch == "duplicate_feedback" and side == "instrumented":
            records = [(kind, p) for kind, p in records if kind != "feedback_reject"]
        if len(records) + len(BRANCHES) > 100:
            raise AssertionError("synthetic fixture exceeded the 100-record test bound")
        for kind, payload in records:
            comparison, _ = RECORDS[kind]
            writer.record(comparison, kind, payload)
        for branch in BRANCHES:
            if branch == missing_branch and side == "instrumented":
                continue
            observations = _branch_observations(
                [{"record_type": kind, "payload": p} for kind, p in records], branch)
            writer.record("BRANCH", "branch_state", {
                "branch_name": branch,
                "evidence_state": "MEASURED_POSITIVE" if observations else "COMPLETE_UNEXERCISED",
                "occurrence_count": {"kind": "pyint", "decimal": str(len(observations))} if observations else None,
                "occurrences": observations if observations else None,
            })
    aggregate_bytes = sum(path.stat().st_size for path in ARTIFACTS.glob("*") if path.is_file())
    if aggregate_bytes > 8 * 1024 * 1024:
        raise AssertionError("synthetic test artifacts exceeded 8 MiB")


class Luna71BC42TraceTests(unittest.TestCase):
    def setUp(self) -> None:
        ARTIFACTS.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        if ARTIFACTS.exists():
            self.assertLessEqual(
                sum(path.stat().st_size for path in ARTIFACTS.iterdir() if path.is_file()),
                8 * 1024 * 1024,
            )
            for path in ARTIFACTS.iterdir():
                if path.is_file():
                    path.unlink()
        if ARTIFACTS.exists() and not any(ARTIFACTS.iterdir()):
            ARTIFACTS.rmdir()

    def test_float_encoding_preserves_signed_zero_and_nan_payload(self) -> None:
        self.assertEqual(f64(-0.0)["bits_be_hex"], "8000000000000000")
        raw_nan = bytes.fromhex("7ff8000000000042")
        value = struct.unpack(">d", raw_nan)[0]
        self.assertEqual(f64(value)["bits_be_hex"], "7ff8000000000042")

    def test_writer_parser_round_trip_and_unknown_field_rejection(self) -> None:
        path = ARTIFACTS / "one.jsonl"
        with TraceWriter(path, identity=_identity("original")) as writer:
            payload = encode_payload({"event_type": "input", "payload": "A", "payload_type": "str",
                                      "timestamp": 0.25, "input_order": 0, "channel_id": "input:A", "event_id": "event-1"})
            writer.record("P01", "input_event", payload)
        rows, digest, size = read_trace(path, expected_side="original")
        self.assertEqual(len(rows), 1)
        self.assertEqual(len(digest), 64)
        self.assertEqual(size, path.stat().st_size)
        self.assertLessEqual(size, 8 * 1024 * 1024)
        bad = dict(rows[0], extra="forbidden")
        with self.assertRaisesRegex(ValueError, "envelope"):
            validate_record(bad)

    def test_exact_comparator_reports_first_bit_level_mismatch(self) -> None:
        original = ARTIFACTS / "original.jsonl"
        instrumented = ARTIFACTS / "instrumented.jsonl"
        _write(original, "original")
        _write(instrumented, "instrumented", mismatch=True)
        expected = {
            "original": {"source_revision": _identity("original")["source_revision"],
                         "runtime_manifest_sha256": _identity("original")["runtime_manifest_sha256"]},
            "instrumented": {"source_revision": _identity("instrumented")["source_revision"],
                              "runtime_manifest_sha256": _identity("instrumented")["runtime_manifest_sha256"]},
            "seed": 17, "arm": "A", "split": "train", "example_id": "example-1",
            "exposure_id": "seed17:A:train:example-1", "fixture_sha256": "e" * 64,
            "initial_parameter_sha256": "c" * 64,
        }
        report = compare_pair(original, instrumented, expected=expected)
        self.assertEqual(report.item_status["P06"], "CONTRADICTED")
        self.assertEqual(report.first_mismatch.comparison_id, "P06")
        self.assertIn("drive", report.first_mismatch.field_path)
        self.assertEqual(report.overall_status, "CONTRADICTED")

    def test_global_record_order_is_compared_across_requirement_families(self) -> None:
        original = ARTIFACTS / "original.jsonl"
        instrumented = ARTIFACTS / "instrumented.jsonl"
        _write(original, "original")
        _write(instrumented, "instrumented", reorder=True)
        report = compare_pair(original, instrumented, expected=self._expected())
        self.assertEqual(report.overall_status, "CONTRADICTED")
        self.assertEqual(report.first_mismatch.field_path, "record_type")

    def test_missing_record_is_incomplete_not_missing_as_zero(self) -> None:
        original = ARTIFACTS / "original.jsonl"
        instrumented = ARTIFACTS / "instrumented.jsonl"
        _write(original, "original")
        _write(instrumented, "instrumented", omit="schedule")
        report = compare_pair(original, instrumented, expected=self._expected())
        self.assertEqual(report.item_status["P02"], "INCOMPLETE")
        self.assertEqual(report.overall_status, "INCOMPLETE")

    def test_one_sided_positive_branch_is_contradicted(self) -> None:
        original = ARTIFACTS / "original.jsonl"
        instrumented = ARTIFACTS / "instrumented.jsonl"
        _write(original, "original", positive_branch="duplicate_feedback")
        _write(instrumented, "instrumented", positive_branch="duplicate_feedback")
        report = compare_pair(original, instrumented, expected=self._expected())
        self.assertEqual(report.branch_status["duplicate_feedback"]["pair_outcome"], "ONE_SIDED_OCCURRENCE")
        self.assertEqual(report.item_status["P08"], "CONTRADICTED")
        self.assertEqual(report.overall_status, "CONTRADICTED")

    def test_missing_branch_state_is_incomplete_not_unexercised(self) -> None:
        original = ARTIFACTS / "original.jsonl"
        instrumented = ARTIFACTS / "instrumented.jsonl"
        _write(original, "original")
        _write(instrumented, "instrumented", missing_branch="prediction_expiration")
        report = compare_pair(original, instrumented, expected=self._expected())
        self.assertEqual(report.branch_status["prediction_expiration"]["pair_outcome"], "EVIDENCE_UNAVAILABLE")
        self.assertEqual(report.item_status["P03"], "INCOMPLETE")
        self.assertEqual(report.overall_status, "INCOMPLETE")

    @staticmethod
    def _expected() -> dict:
        return {
            "original": {"source_revision": _identity("original")["source_revision"],
                         "runtime_manifest_sha256": _identity("original")["runtime_manifest_sha256"]},
            "instrumented": {"source_revision": _identity("instrumented")["source_revision"],
                              "runtime_manifest_sha256": _identity("instrumented")["runtime_manifest_sha256"]},
            "seed": 17, "arm": "A", "split": "train", "example_id": "example-1",
            "exposure_id": "seed17:A:train:example-1", "fixture_sha256": "e" * 64,
            "initial_parameter_sha256": "c" * 64,
        }

    def test_driver_fails_closed_before_calling_execution_adapter(self) -> None:
        called = []
        with self.assertRaisesRegex(PreflightError, "fixture-payload manifest is missing"):
            run_authorized_pair(
                root=EXPERIMENT, source_manifest_path="reports/source-manifest.json",
                fixture_manifest_path="fixture-payload-manifest.json",
                authorization_path="execution-authorization.json",
                initial_parameters={}, execute_side=lambda **kwargs: called.append(kwargs),
            )
        self.assertEqual(called, [])
        self.assertFalse(any(name == "tpcn" or name.startswith("tpcn.") for name in sys.modules))

    def test_driver_rejects_mismatched_source_identity(self) -> None:
        source = json.loads((EXPERIMENT / "reports" / "source-manifest.json").read_text(encoding="utf-8"))
        source["variants"]["original"][0]["sha256"] = "0" * 64
        bad_manifest = ARTIFACTS / "bad-source-manifest.json"
        bad_manifest.write_text(json.dumps(source), encoding="utf-8")
        with self.assertRaisesRegex(PreflightError, "source identity mismatch"):
            verify_preflight(
                EXPERIMENT,
                source_manifest_path="test-artifacts/bad-source-manifest.json",
                fixture_manifest_path="fixture-payload-manifest.json",
            )

    def test_driver_rejects_mismatched_implementation_identity(self) -> None:
        source = json.loads((EXPERIMENT / "reports" / "source-manifest.json").read_text(encoding="utf-8"))
        source["implementation"][0]["sha256"] = "0" * 64
        bad_manifest = ARTIFACTS / "bad-implementation-manifest.json"
        bad_manifest.write_text(json.dumps(source), encoding="utf-8")
        with self.assertRaisesRegex(PreflightError, "implementation identity mismatch"):
            verify_preflight(
                EXPERIMENT,
                source_manifest_path="test-artifacts/bad-implementation-manifest.json",
                fixture_manifest_path="fixture-payload-manifest.json",
            )


    def test_pair_gate_stops_both_sides_before_next_event(self) -> None:
        gate = PairEventGate()
        rendezvous = threading.Barrier(3)
        stopped = threading.Event()
        result: dict[str, bool] = {}

        def worker(side: str) -> None:
            gate.begin_exposure(side, "paired-exposure")
            self.assertTrue(gate.before_event(side, "paired-exposure", {"event_id": "e1"}))
            rendezvous.wait(timeout=2)
            self.assertTrue(stopped.wait(timeout=2))
            gate.after_event(side)
            result[side] = gate.before_event(side, "paired-exposure", {"event_id": "e2"})
            gate.finish_exposure(side)
            gate.finish(side)

        with ThreadPoolExecutor(max_workers=2) as pool:
            left = pool.submit(worker, "original")
            right = pool.submit(worker, "instrumented")
            rendezvous.wait(timeout=2)
            gate.stop("original", "synthetic P11 trigger", None)
            stopped.set()
            left.result(timeout=2)
            right.result(timeout=2)
        self.assertEqual(result, {"original": False, "instrumented": False})

    def test_pair_gate_rejects_mismatched_exposure_identities(self) -> None:
        gate = PairEventGate()
        gate.begin_exposure("original", "exposure-original")
        with self.assertRaisesRegex(RuntimeError, "identities differ"):
            gate.begin_exposure("instrumented", "exposure-instrumented")
        self.assertTrue(gate.stopped)

    def test_p11_alignment_requires_exact_pre_stop_admitted_anchor(self) -> None:
        anchor = {"exposure_id": "paired-exposure", "event_id": "e9",
                  "source": "source", "destination": "destination", "event_type": "input"}
        failure = {"record_type": "queue_failure", "record_index": 4,
                   "payload": {"anchor": anchor}}
        failed_terminal = {"record_type": "terminal_state", "record_index": 5, "payload": {}}
        peer_admission = {"record_type": "enqueue", "record_index": 6,
                          "payload": {"anchor": anchor, "admission_outcome": "ADMITTED"}}
        peer_terminal = {"record_type": "terminal_state", "record_index": 7, "payload": {}}
        aligned = _p11_stop_alignment(
            [failure, failed_terminal],
            [peer_admission, peer_terminal],
        )
        unaligned = _p11_stop_alignment(
            [failure, failed_terminal],
            [peer_terminal],
        )
        self.assertTrue(aligned["aligned"])
        self.assertFalse(unaligned["aligned"])

    def test_synthetic_fixture_budget_is_bounded(self) -> None:
        self.assertLess(len(_payloads()) + len(BRANCHES), 100)

    def test_schema_rejects_wrong_family_types_and_branch_counts(self) -> None:
        path = ARTIFACTS / "types.jsonl"
        _write(path, "original")
        rows, _, _ = read_trace(path)
        cases = [
            ("input_event", "timestamp", "0.25"),
            ("input_event", "input_order", "0"),
            ("input_event", "channel_id", True),
            ("input_event", "payload_type", "str"),
            ("enqueue", "payload", {"not": "a tagged source map"}),
            ("readout_drive", "weight", "1.0"),
            ("readout_drive", "class_index", f64(0.0)),
            ("feedback_reject", "duplicate", "true"),
            ("queue_state", "pending", "empty"),
            ("branch_state", "occurrence_count", {"kind": "pyint", "decimal": "9"}),
        ]
        for kind, field, value in cases:
            row = next(r for r in rows if r["record_type"] == kind
                       and (kind != "branch_state" or r["payload"]["evidence_state"] == "MEASURED_POSITIVE"))
            with self.subTest(kind=kind, field=field), self.assertRaises(ValueError):
                validate_record({**row, "payload": {**row["payload"], field: value}})
        row = next(r for r in rows if r["record_type"] == "input_event")
        payload = {**row["payload"], "input_order": {"kind": "u32", "bits_be_hex": "00000000"}}
        validate_record({**row, "payload": payload})
        payload["input_order"] = {"kind": "u32", "bits_be_hex": "0000000g"}
        with self.assertRaises(ValueError):
            validate_record({**row, "payload": payload})

    def test_preflight_source_revision_is_valid_trace_identity(self) -> None:
        revision = _source_revision([{"path": "module.py", "sha256": "a" * 64}])
        row = {
            "schema_version": "ppc11-paired-trace-1",
            **_identity("original"),
            "source_revision": revision,
            "record_index": 0,
            "comparison_id": "P01",
            "record_type": "input_event",
            "payload": _payloads()[0][1],
        }
        validate_record(row, expected_side="original")
        self.assertRegex(revision, r"^[0-9a-f]{40}\+sha256:[0-9a-f]{64}$")

    def test_fixture_manifest_rejects_unsupported_schema_tag(self) -> None:
        manifest = {
            "schema": "unsupported-fixture-manifest",
            "plan_sha256": PLAN_SHA256,
            "splits": {"train": {}, "validation": {}, "test": {}},
        }
        with self.assertRaisesRegex(PreflightError, "schema or frozen plan identity"):
            _validate_fixture_manifest(manifest)
        manifest["schema"] = FIXTURE_MANIFEST_SCHEMA
        self.assertIs(_validate_fixture_manifest(manifest), manifest)

    def test_feedback_application_order_is_a_distinct_application_ordinal(self) -> None:
        path = ARTIFACTS / "feedback-order.jsonl"
        with TraceWriter(path, identity=_identity("original")) as writer:
            capture = SourceCapture(writer)
            capture.feedback_applied("f1", "origin", 1.0, 1, 0.5, 1.0)
            capture.feedback_applied("f2", "origin", 1.0, (1, -1, 1, -1), 1.0, 1.0)
        rows, _, _ = read_trace(path, expected_side="original")
        orders = [row["payload"]["application_order"] for row in rows]
        self.assertEqual(orders, [
            {"kind": "pyint", "decimal": "0"},
            {"kind": "pyint", "decimal": "1"},
        ])
        self.assertEqual(rows[1]["payload"]["sign"], [
            {"kind": "pyint", "decimal": "1"},
            {"kind": "pyint", "decimal": "-1"},
            {"kind": "pyint", "decimal": "1"},
            {"kind": "pyint", "decimal": "-1"},
        ])
        invalid_vector = dict(rows[1])
        invalid_vector["payload"] = dict(rows[1]["payload"], sign=rows[1]["payload"]["sign"][:3])
        with self.assertRaisesRegex(ValueError, "four class values"):
            validate_record(invalid_vector, expected_side="original")
        for side in ("original", "instrumented"):
            source_path = EXPERIMENT / "variants" / side / "tpcn" / "luna70_readout_learning.py"
            tree = ast.parse(source_path.read_text(encoding="utf-8"))
            direct_applications = [
                node for node in ast.walk(tree)
                if isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "emit"
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and node.args[0].value == "feedback_apply"
            ]
            helper_applications = [
                node for node in ast.walk(tree)
                if isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "feedback_applied"
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "ppc11_capture"
            ]
            self.assertEqual(direct_applications, [])
            self.assertEqual(len(helper_applications), 2)

    @staticmethod
    def _eligibility_module(side: str):
        package_name = f"synthetic_c42_eligibility_{side}"
        package = types.ModuleType(package_name)
        package.__path__ = []
        sys.modules[package_name] = package

        runtime = types.ModuleType(f"{package_name}.event_runtime")
        runtime.Event = type("Event", (), {})

        class LocalClock:
            def __init__(self) -> None:
                self.timestamp = 0.0

            def advance_to(self, timestamp: float) -> float:
                elapsed = timestamp - self.timestamp
                self.timestamp = timestamp
                return elapsed

        runtime.LocalClock = LocalClock
        predictive = types.ModuleType(f"{package_name}.predictive_coding")
        predictive.PredictionError = type("PredictionError", (), {})
        sys.modules[runtime.__name__] = runtime
        sys.modules[predictive.__name__] = predictive
        path = EXPERIMENT / "variants" / side / "tpcn" / "eligibility.py"
        spec = importlib.util.spec_from_file_location(f"{package_name}.eligibility", path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module.__name__] = module
        spec.loader.exec_module(module)
        return module, (module.__name__, runtime.__name__, predictive.__name__, package_name)

    def test_eligibility_admission_uses_trace_identity_not_total_occupancy(self) -> None:
        from types import SimpleNamespace

        for side in ("original", "instrumented"):
            module, loaded_modules = self._eligibility_module(side)
            try:
                ledger = module.EligibilityLedger(
                    "ledger", max_traces=4, decay_time_constant=10.0)

                def admit(trace_id: str, timestamp: float):
                    event = SimpleNamespace(
                        destination="ledger",
                        payload=module.EligibilityActivity(trace_id, 1.0),
                        timestamp=timestamp,
                    )
                    return ledger.record_activity_with_admission(event)

                _, existed, occupancy = admit("trace-1", 1.0)
                self.assertFalse(existed)
                self.assertEqual(occupancy, 0)
                _, existed, occupancy = admit("trace-2", 2.0)
                self.assertFalse(existed)
                self.assertEqual(occupancy, 1)
                _, existed, occupancy = admit("trace-1", 3.0)
                self.assertTrue(existed)
                self.assertEqual(occupancy, 2)

                source_path = EXPERIMENT / "variants" / side / "tpcn" / "luna70_readout_learning.py"
                source = source_path.read_text(encoding="utf-8")
                self.assertEqual(source.count("record_activity_with_admission(event)"), 2)
                self.assertEqual(
                    source.count('reason="existing_trace" if existing_trace else "capacity_available"'),
                    2,
                )

                expiring = module.EligibilityLedger(
                    "ledger", max_traces=2, decay_time_constant=10.0, expiry=0.5)
                first = SimpleNamespace(
                    destination="ledger",
                    payload=module.EligibilityActivity("expired-id", 1.0),
                    timestamp=1.0,
                )
                expiring.record_activity_with_admission(first)
                expired_reuse = SimpleNamespace(
                    destination="ledger",
                    payload=module.EligibilityActivity("expired-id", 1.0),
                    timestamp=2.0,
                )
                _, existed, occupancy = expiring.record_activity_with_admission(expired_reuse)
                self.assertFalse(existed)
                self.assertEqual(occupancy, 0)
            finally:
                for name in loaded_modules:
                    sys.modules.pop(name, None)

    def test_completion_marker_rejects_missing_altered_and_clean_truncation(self) -> None:
        for mode in ("missing", "altered", "truncated"):
            path = ARTIFACTS / f"{mode}.jsonl"
            _write(path, "original")
            marker = path.with_suffix(".jsonl.complete.json")
            if mode == "missing":
                marker.unlink()
            elif mode == "altered":
                data = json.loads(marker.read_bytes())
                data["record_count"] += 1
                marker.write_text(json.dumps(data), encoding="utf-8")
            else:
                path.write_bytes(b"".join(path.read_bytes().splitlines(keepends=True)[:-1]))
            with self.subTest(mode=mode), self.assertRaisesRegex(ValueError, "completion"):
                read_trace(path)

    def test_exceptional_writer_exit_does_not_certify_completion(self) -> None:
        path = ARTIFACTS / "aborted.jsonl"
        with self.assertRaises(RuntimeError):
            with TraceWriter(path, identity=_identity("original")) as writer:
                writer.record("P01", "input_event", _payloads()[0][1])
                raise RuntimeError("synthetic failure")
        with self.assertRaisesRegex(ValueError, "completion"):
            read_trace(path)

    def test_caught_record_failure_cannot_certify_a_valid_prefix(self) -> None:
        path = ARTIFACTS / "caught-failure.jsonl"
        with TraceWriter(path, identity=_identity("original")) as writer:
            writer.record("P01", "input_event", _payloads()[0][1])
            with self.assertRaises(ValueError):
                writer.record("P01", "input_event", {})
        with self.assertRaisesRegex(ValueError, "completion"):
            read_trace(path)

    def test_four_class_cardinality_and_orphan_decision_are_incomplete(self) -> None:
        records = [{"record_type": kind, "payload": payload, "record_index": index}
                   for index, (kind, payload) in enumerate(_payloads())]
        self.assertFalse([g for g in _shape_gaps(records, "original") if g["comparison_id"] == "P06"])
        records = [r for r in records if not (r["record_type"] == "readout_drive"
                   and r["payload"]["class_index"]["decimal"] == "3")]
        self.assertTrue(any("four_class_cardinality" in g["field_path"] for g in _shape_gaps(records, "original")))
        records.append({"record_type": "readout_drive", "payload": {
            **next(r["payload"] for r in records if r["record_type"] == "readout_drive"),
            "decision_id": "orphan"}})
        self.assertTrue(any("orphan" in g["field_path"] for g in _shape_gaps(records, "original")))

    def test_unbound_fixture_and_unverified_parameter_digest_remain_incomplete(self) -> None:
        original, instrumented = ARTIFACTS / "original.jsonl", ARTIFACTS / "instrumented.jsonl"
        _write(original, "original")
        _write(instrumented, "instrumented")
        report = compare_pair(original, instrumented, expected=self._expected())
        self.assertEqual(report.overall_status, "INCOMPLETE")
        self.assertEqual(report.item_status["P01"], "INCOMPLETE")
        self.assertEqual(report.item_status["P09"], "INCOMPLETE")
        self.assertTrue(any("captured_manifest_identity" in g["field_path"] for g in report.missing_evidence))
        expected = {**self._expected(), "fixture_sha256": "truthy"}
        with self.assertRaisesRegex(ValueError, "fixture identity"):
            compare_pair(original, instrumented, expected=expected)

    def test_branch_claim_must_match_actual_occurrence_records(self) -> None:
        original, instrumented = ARTIFACTS / "original.jsonl", ARTIFACTS / "instrumented.jsonl"
        for side, path in (("original", original), ("instrumented", instrumented)):
            with TraceWriter(path, identity=_identity(side)) as writer:
                for kind, payload in _payloads():
                    writer.record(RECORDS[kind][0], kind, payload)
                for branch in BRANCHES:
                    writer.record("BRANCH", "branch_state", encode_payload({
                        "branch_name": branch, "evidence_state": "MEASURED_POSITIVE",
                        "occurrence_count": 1, "occurrences": [{"invented": "not-source-evidence"}],
                    }))
        report = compare_pair(original, instrumented, expected=self._expected())
        self.assertEqual(report.overall_status, "INCOMPLETE")
        self.assertTrue(all(s["pair_outcome"] == "EVIDENCE_UNAVAILABLE" for s in report.branch_status.values()))

    def test_parameter_manifest_hash_is_recomputed_from_captured_source_bits(self) -> None:
        parameters = {"weight": -0.0, "bias": [1.0, 0.5], "order": 1}
        captured = encode_payload({"parameters": parameters})["parameters"]
        expected = hashlib.sha256(json.dumps(parameters, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()
        self.assertEqual(_parameter_manifest_digest(captured), expected)
        parameters["weight"] = 0.0
        altered = encode_payload({"parameters": parameters})["parameters"]
        self.assertNotEqual(_parameter_manifest_digest(altered), expected)

    def test_missing_class_and_input_scheduler_link_are_incomplete_in_comparator(self) -> None:
        original, instrumented = ARTIFACTS / "original.jsonl", ARTIFACTS / "instrumented.jsonl"
        for side, path in (("original", original), ("instrumented", instrumented)):
            with TraceWriter(path, identity=_identity(side)) as writer:
                for kind, payload in _payloads():
                    if kind == "readout_drive" and payload["class_index"]["decimal"] == "3":
                        continue
                    if kind == "input_event":
                        payload = {**payload, "event_id": "not-enqueued"}
                    writer.record(RECORDS[kind][0], kind, payload)
        report = compare_pair(original, instrumented, expected=self._expected())
        self.assertEqual(report.item_status["P06"], "INCOMPLETE")
        self.assertTrue(any("four_class_cardinality" in g["field_path"] for g in report.missing_evidence))
        self.assertTrue(any("enqueue_link" in g["field_path"] for g in report.missing_evidence))

    def test_gate_event_identity_mismatch_releases_both_threads(self) -> None:
        gate = PairEventGate()
        for side in ("original", "instrumented"):
            gate.begin_exposure(side, "exposure")
        results = {}
        def worker(side: str) -> None:
            results[side] = gate.before_event(side, "exposure", {"event_id": side})
        threads = [threading.Thread(target=worker, args=(side,), daemon=True)
                   for side in ("original", "instrumented")]
        for thread in threads:
            thread.start()
        try:
            for thread in threads:
                thread.join(timeout=2)
            self.assertTrue(all(not t.is_alive() for t in threads))
            self.assertEqual(results, {"original": False, "instrumented": False})
            self.assertIn("identity mismatch", gate.stop_evidence["reason"])
        finally:
            gate.stop("original", "test cleanup", None)

    def test_gate_peer_completion_never_releases_unmatched_event(self) -> None:
        for finish_method in ("finish_exposure", "finish"):
            gate = PairEventGate()
            for side in ("original", "instrumented"):
                gate.begin_exposure(side, "exposure")
            results = {}
            def next_event() -> None:
                results["allowed"] = gate.before_event("original", "exposure", {"event_id": "e1"})
            def finish_peer() -> None:
                getattr(gate, finish_method)("instrumented")
            threads = [threading.Thread(target=f, daemon=True) for f in (next_event, finish_peer)]
            for thread in threads:
                thread.start()
            try:
                for thread in threads:
                    thread.join(timeout=2)
                self.assertTrue(all(not t.is_alive() for t in threads))
                self.assertFalse(results["allowed"])
                self.assertTrue(gate.stopped)
            finally:
                gate.stop("original", "test cleanup", None)

    def test_driver_never_dispatches_arbitrary_callbacks_even_after_preflight(self) -> None:
        from types import SimpleNamespace
        from experiments.luna71b_c4_2.ppc11 import driver
        called = []
        params = {"w": 0.0}
        digest = driver._canonical_digest(params)
        fixture = ARTIFACTS / "synthetic-manifest.json"
        fixture.write_text("{}", encoding="utf-8")
        preflight = SimpleNamespace(source_manifest_sha256="a" * 64, root=EXPERIMENT,
                                    initial_parameter_sha256=digest)
        grant = {"source_manifest_sha256": "a" * 64,
                 "fixture_manifest_sha256": hashlib.sha256(fixture.read_bytes()).hexdigest()}
        with patch.object(driver, "verify_preflight", return_value=preflight), patch.object(
            driver, "require_execution_authorization", return_value=grant
        ), self.assertRaisesRegex(PreflightError, "dispatch is unimplemented"):
            run_authorized_pair(root=EXPERIMENT, source_manifest_path="unused",
                                fixture_manifest_path=fixture, authorization_path="unused",
                                initial_parameters={"original": params, "instrumented": params},
                                execute_side=lambda **kwargs: called.append(kwargs))
        self.assertEqual(called, [])

    @staticmethod
    def _runtime(side: str):
        name = f"synthetic_c42_event_runtime_{side}"
        spec = importlib.util.spec_from_file_location(
            name, EXPERIMENT / "variants" / side / "tpcn" / "event_runtime.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module

    def test_disabled_capture_skips_tie_metadata_and_enabled_policy_is_observed(self) -> None:
        for side in ("original", "instrumented"):
            runtime = self._runtime(side)
            internal = runtime.Event(1.0, "s", "d", runtime.EventType.INTERNAL, None, event_id="i")
            external = runtime.Event(1.0, "s", "d", runtime.EventType.INPUT, None, event_id="e")
            queue = runtime.EventQueue(4)
            queue._tie_break_cause = lambda event: self.fail("disabled tie metadata computed")
            queue._snapshot = lambda: self.fail("disabled queue snapshot computed")
            queue.push(internal)
            queue.push(external)
            self.assertEqual(queue.pop_ready(1.0).event_id, "e")
            self.assertEqual(queue.pop_ready(1.0).event_id, "i")
            observed = []
            from types import SimpleNamespace
            observer = SimpleNamespace(queue_transition=lambda operation, **data: observed.append((operation, data)))
            queue = runtime.EventQueue(4, observer=observer)
            queue.push(internal)
            queue.push(external)
            queue.pop_ready(1.0)
            queue.pop_ready(1.0)
            causes = [data["tie_break_cause"] for op, data in observed if op == "dequeue"]
            self.assertEqual(causes, ["external_before_internal_same_destination_same_timestamp",
                                      "timestamp_then_assigned_sequence"])

    def test_failed_handler_and_queue_failure_preserve_last_completed_operation(self) -> None:
        for side in ("original", "instrumented"):
            runtime = self._runtime(side)
            for failure in ("handler", "queue"):
                path = ARTIFACTS / f"{side}-{failure}.jsonl"
                with TraceWriter(path, identity=_identity(side)) as writer:
                    capture = SourceCapture(writer)
                    queue = runtime.EventQueue(1, observer=capture)
                    queue.push(runtime.Event(1.0, "s", "d", "input", "A", event_id="e1"))
                    def handler(event, pending):
                        if failure == "queue":
                            pending.push(runtime.Event(9.0, "s", "d", "input", "B", event_id="e2"))
                            pending.push(runtime.Event(10.0, "s", "d", "input", "C", event_id="e3"))
                        raise RuntimeError("synthetic handler failed")
                    with self.assertRaises((RuntimeError, runtime.QueueCapacityError)):
                        runtime.execute_bounded(queue, handler, event_budget=2)
                rows, _, _ = read_trace(path)
                self.assertFalse(any(r["record_type"] in {"process", "event_processed"} for r in rows))
                terminals = [r["payload"] for r in rows if r["record_type"] == "terminal_state"]
                self.assertEqual(len(terminals), 1)
                self.assertEqual(terminals[0]["last_operation"], "dequeue" if failure == "handler" else "enqueue")
                self.assertEqual(terminals[0]["timestamp"], f64(1.0))
                schedules = [r["payload"] for r in rows if r["record_type"] == "schedule"]
                self.assertTrue(all(p["tie_break_cause"] is None for p in schedules))

    def test_successful_handler_is_counted_only_after_return(self) -> None:
        runtime = self._runtime("original")
        path = ARTIFACTS / "success.jsonl"
        with TraceWriter(path, identity=_identity("original")) as writer:
            queue = runtime.EventQueue(1, observer=SourceCapture(writer))
            queue.push(runtime.Event(1.0, "s", "d", "input", "A", event_id="e1"))
            def handler(event, pending):
                self.assertNotIn(b'"record_type":"event_processed"', path.read_bytes())
            result = runtime.execute_bounded(queue, handler, event_budget=1)
        self.assertEqual(result.processed_event_count, 1)
        rows, _, _ = read_trace(path)
        self.assertEqual(sum(r["record_type"] == "event_processed" for r in rows), 1)

    def test_unequal_synthetic_queues_stop_before_extra_event_with_bilateral_terminals(self) -> None:
        runtime = self._runtime("original")
        gate = PairEventGate()
        processed = {"original": [], "instrumented": []}
        writers = {side: TraceWriter(ARTIFACTS / f"{side}.jsonl", identity=_identity(side))
                   for side in processed}
        queues = {side: runtime.EventQueue(3, observer=SourceCapture(writer, pair_gate=gate))
                  for side, writer in writers.items()}
        for queue in queues.values():
            queue.push(runtime.Event(1.0, "s", "d", "input", "A", event_id="e1"))
        queues["original"].push(runtime.Event(2.0, "s", "d", "input", "B", event_id="e2"))
        errors = []
        results = {}
        def worker(side):
            try:
                results[side] = runtime.execute_bounded(queues[side],
                    lambda event, queue: processed[side].append(event.event_id), event_budget=3)
            except BaseException as error:
                errors.append(error)
        threads = [threading.Thread(target=worker, args=(side,), daemon=True) for side in processed]
        for thread in threads:
            thread.start()
        try:
            for thread in threads:
                thread.join(timeout=2)
            self.assertTrue(all(not t.is_alive() for t in threads))
            self.assertEqual(errors, [])
            self.assertEqual(processed, {"original": ["e1"], "instrumented": ["e1"]})
            self.assertTrue(all(not result.completed and result.termination_reason == "paired_stop"
                                for result in results.values()))
        finally:
            gate.stop("original", "test cleanup", None)
            for thread in threads:
                thread.join(timeout=2)
            for writer in writers.values():
                writer.close()
        for side in processed:
            rows, _, _ = read_trace(ARTIFACTS / f"{side}.jsonl")
            terminals = [r for r in rows if r["record_type"] == "terminal_state"]
            self.assertEqual(len(terminals), 1)
            self.assertEqual(terminals[0]["payload"]["timestamp"], f64(1.0))


if __name__ == "__main__":
    unittest.main()
