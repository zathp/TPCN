from __future__ import annotations

import hashlib
import json
import unittest
from fractions import Fraction

import certificate


class LaneWCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = certificate.build_certificate()

    def test_every_w_row_has_certified_status_and_unique_identity(self) -> None:
        rows = self.matrix["rows"]
        self.assertTrue(rows)
        self.assertEqual(len(rows), len({row["row_id"] for row in rows}))
        self.assertTrue(all(row["owner"] == "W" for row in rows))
        self.assertTrue(all(row["status"] == "CERTIFIED" for row in rows))
        self.assertEqual(self.matrix["reconciliation"]["blocked_count"], 0)

    def test_c2_a1_has_both_polarities_at_all_four_checkpoints(self) -> None:
        actual = {
            (row["polarity"], row["active_time_TU"])
            for row in self.matrix["rows"]
            if row["fixture"] == "C2" and row["checkpoint"].startswith("C2.A1.")
        }
        self.assertEqual(
            actual,
            {
                (1, "0"),
                (1, "1/2"),
                (1, "1"),
                (1, "2"),
                (-1, "0"),
                (-1, "1/2"),
                (-1, "1"),
                (-1, "2"),
            },
        )
        for row in self.matrix["rows"]:
            if row["fixture"] == "C2" and row["checkpoint"].startswith("C2.A1."):
                self.assertIn("oracle_state_enclosures", row)
                self.assertEqual(row["candidate_comparison"], "NOT PERFORMED — no Stage-B candidate evaluation in Lane W.")

    def test_tangency_is_exact_and_never_a_crossing(self) -> None:
        tangent = [row for row in self.matrix["rows"] if ".A2_TANGENT." in row["row_id"]]
        self.assertEqual(len(tangent), 2)
        self.assertTrue(all(row["evidence_class"] == "EXACT_SYMBOLIC" for row in tangent))
        self.assertTrue(all("tangent" in row["claim"].lower() for row in tangent))

    def test_roots_resolve_with_overlap_and_within_bisection_cap(self) -> None:
        evidence = self.matrix["evidence"]
        for root_set in (evidence["roots_A4"], evidence["roots_C6_independent"]):
            for root in root_set.values():
                self.assertEqual(root["bisections_total"], 128)
                self.assertLessEqual(root["bisections_total"], 128)
                left256, right256 = root["precision_runs"]["256"]["bracket"]
                left512, right512 = root["precision_runs"]["512"]["bracket"]
                self.assertLessEqual(Fraction(left256), Fraction(right512))
                self.assertLessEqual(Fraction(left512), Fraction(right256))
                for precision in ("256", "512"):
                    endpoints = root["precision_runs"][precision]["endpoint_surface_enclosures"]
                    self.assertIn("lower_exact", endpoints["left"])
                    self.assertIn("upper_exact", endpoints["right"])

    def test_t_e_work_is_explicitly_separate_and_blocked(self) -> None:
        blockers = self.matrix["deferred_not_w_lane"]
        self.assertTrue(blockers)
        self.assertTrue(all(item["status"] == "BLOCKED" for item in blockers))
        self.assertTrue(all("T/E" in item["owner"] for item in blockers))
        self.assertFalse(self.matrix["evidence"]["arithmetic_profile"]["active_time_or_event_clock_conversion_performed"])

    def test_frozen_fixture_inventory_reconciles_to_all_lane_w_categories(self) -> None:
        inventory = self.matrix["source_inventory"]
        self.assertEqual(inventory["fixture_ids"], [f"C{i}" for i in range(8)])
        self.assertEqual(inventory["c2_case_count"], 7)
        self.assertEqual(inventory["c2_a1_polarity_checkpoint_count"], 8)
        self.assertEqual(inventory["c3_hold_duration_count"], 3)
        self.assertEqual(inventory["c5_hold_instance_count"], 3)
        self.assertEqual(inventory["c7_subcase_count"], 14)
        self.assertEqual(inventory["c7_timestamp_invalid_instance_count"], 4)
        self.assertEqual(len(self.matrix["reconciliation"]["c7_subcase_coverage"]), 14)
        self.assertEqual(self.matrix["reconciliation"]["planned_total"], 100)
        self.assertEqual(
            self.matrix["reconciliation"]["row_counts_by_fixture"],
            {"C0": 1, "C1": 2, "C2": 22, "C3": 5, "C4": 8, "C5": 18, "C6": 8, "C7": 36},
        )

    def test_json_serialization_is_deterministic(self) -> None:
        encoded = certificate.canonical_json(self.matrix)
        self.assertEqual(encoded, certificate.canonical_json(json.loads(encoded)))
        self.assertEqual(
            hashlib.sha256(encoded).hexdigest().upper(),
            hashlib.sha256(certificate.canonical_json(self.matrix)).hexdigest().upper(),
        )
        matrix_path = certificate.LANE_DIR / "coverage_matrix.json"
        manifest_path = certificate.LANE_DIR / "manifest.json"
        self.assertTrue(matrix_path.is_file())
        self.assertTrue(manifest_path.is_file())
        self.assertEqual(matrix_path.read_bytes(), encoded)
        expected_manifest = certificate.canonical_json(
            certificate.make_manifest(self.matrix, encoded)
        )
        self.assertEqual(manifest_path.read_bytes(), expected_manifest)


if __name__ == "__main__":
    unittest.main()
