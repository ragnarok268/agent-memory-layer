import json
import unittest
from pathlib import Path

from grand_challenges_library.catalog import load_catalog
from grand_challenges_library.export import export_catalog
from grand_challenges_library.validate import validate_catalog


class CatalogTests(unittest.TestCase):
    def test_load_catalog_contains_expected_challenges(self) -> None:
        catalog = load_catalog()
        challenge_ids = [challenge.id for challenge in catalog]

        self.assertEqual(
            challenge_ids,
            [
                "memory",
                "efficiency",
                "reasoning_correctness",
                "context_retrieval",
                "agent_architecture",
                "sparse_compute",
                "program_bug_system_truth",
            ],
        )

    def test_validation_has_no_errors(self) -> None:
        self.assertEqual(validate_catalog(), [])

    def test_export_catalog_writes_json(self) -> None:
        output_dir = Path("outputs_test")
        output_path = export_catalog(output_dir=output_dir)
        data = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertEqual(output_path.name, "grand_challenges_catalog.json")
        self.assertEqual(len(data), 7)
        self.assertEqual(data[0]["id"], "memory")
        self.assertIn("invariants", data[0])

        output_path.unlink()
        output_dir.rmdir()


if __name__ == "__main__":
    unittest.main()
