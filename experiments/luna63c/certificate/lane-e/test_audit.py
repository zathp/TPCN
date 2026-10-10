from __future__ import annotations

import json
import unittest

import audit


class LaneEAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix, cls.manifest = audit.build_outputs()
        matrix_bytes = audit.canonical_json(cls.matrix).encode("utf-8")
        cls.manifest["owned_files"]["coverage_matrix.json"] = audit.sha256(matrix_bytes)

    def test_w_and_t_publication_totals(self) -> None:
        counts = self.manifest["counts"]
        self.assertEqual(counts["w_rows"], 100)
        self.assertEqual(counts["t_events"], 191)
        self.assertEqual(counts["t_certified"], 9)
        self.assertEqual(counts["t_blocked"], 182)
        self.assertEqual(counts["t_c7_ids"], 119)
        self.assertEqual(counts["observation_rows"], 15)

    def test_every_w_checkpoint_has_applicable_a_rows(self) -> None:
        rows = [row for row in self.matrix["rows"] if row["domain"] == "fixture_checkpoint"]
        self.assertEqual({row["row_id"] for row in rows}, {
            row["row_id"] for row in audit.read_json(audit.W_DIR / "coverage_matrix.json")["rows"]
        })
        for obligation in audit.A_OBLIGATIONS:
            relevant = [row for row in rows if row["obligation"] == obligation]
            self.assertGreater(len(relevant), 0)
            self.assertTrue(all(row["status"] == "PASS" for row in relevant))

    def test_t_identity_coverage_preserves_all_blockers(self) -> None:
        events = [row for row in self.matrix["rows"] if row["domain"] == "scheduled_event"]
        b7 = [row for row in events if row["obligation"] == "N4-B7"]
        self.assertEqual(len(b7), 191)
        self.assertEqual(sum(row["status"] == "PASS" for row in b7), 9)
        self.assertEqual(sum(row["status"] == "BLOCKED" for row in b7), 182)
        blocked = [row for row in b7 if row["status"] == "BLOCKED"]
        self.assertTrue(all(row["blocked_reasons"] for row in blocked))
        self.assertEqual(
            {row["row_id"] for row in blocked},
            set(self.matrix["audit_summary"]["blocked_event_ids"]),
        )

    def test_only_nine_t_rows_receive_numeric_conversion_passes(self) -> None:
        events = [row for row in self.matrix["rows"] if row["domain"] == "scheduled_event"]
        passing_ids = {
            row["row_id"] for row in events
            if row["obligation"] == "N4-B2" and row["status"] == "PASS"
        }
        self.assertEqual(passing_ids, audit.EXPECTED_CERTIFIED_T)
        self.assertIn("N4-B", self.matrix["disposition"])
        self.assertIn("incomplete", self.matrix["disposition"].lower())

    def test_serialized_matrix_and_manifest_are_deterministic(self) -> None:
        matrix_bytes = audit.canonical_json(self.matrix).encode("utf-8")
        manifest_bytes = audit.canonical_json(self.manifest).encode("utf-8")
        self.assertEqual(audit.OUT_MATRIX.read_bytes(), matrix_bytes)
        self.assertEqual(audit.OUT_MANIFEST.read_bytes(), manifest_bytes)
        self.assertEqual(json.loads(matrix_bytes), self.matrix)


if __name__ == "__main__":
    unittest.main()
