from __future__ import annotations

import time
import unittest
from pathlib import Path
from uuid import uuid4
import shutil
import os
from dataclasses import replace

from mindfreak.authority import AuthorityLayer
from mindfreak.checkpoint import CheckpointLayer
from mindfreak.constants import LIFECYCLE_ORDER
from mindfreak.memory_graph import MemoryGraph
from mindfreak.models import Receipt
from mindfreak.receipts import ReceiptLog
from mindfreak.robustness import (
    generated_memory,
    corruption_scenarios,
    deterministic_run_hash,
    run_generated_simulation,
    write_stress_results,
)
from mindfreak.replay import verify_replay


class MindfreakStressTests(unittest.TestCase):
    def test_100_memory_simulation(self) -> None:
        result = run_generated_simulation(100)
        self.assertTrue(result["replay"].passed)
        for receipt in result["receipt_objects"]:
            if receipt.score_breakdown is None:
                continue
            self.assertGreaterEqual(receipt.score_breakdown["final_score"], 0.0)
            self.assertLessEqual(receipt.score_breakdown["final_score"], 1.0)
        for state in result["final_state"].values():
            self.assertIn(state["lifecycle_state"], LIFECYCLE_ORDER)

    def test_1000_memory_simulation(self) -> None:
        started = time.perf_counter()
        result = run_generated_simulation(1000)
        elapsed = time.perf_counter() - started
        self.assertTrue(result["replay"].passed)
        self.assertFalse(result["duplicate_memory_ids"])
        self.assertLess(elapsed, 10.0)

    def test_corrupted_receipt_replay_fails_safely(self) -> None:
        result = corruption_scenarios()["corrupted_receipt"]["verification"]
        self.assertFalse(result.passed)
        self.assertIn("failure", result.mismatch_reason.lower())

    def test_missing_receipt_detection(self) -> None:
        result = corruption_scenarios()["missing_receipt"]["verification"]
        self.assertFalse(result.passed)

    def test_duplicate_receipt_detection(self) -> None:
        result = corruption_scenarios()["duplicate_receipt"]["verification"]
        self.assertFalse(result.passed)
        self.assertIn("Duplicate receipt id detected", result.mismatch_reason)

    def test_out_of_order_receipt_handling(self) -> None:
        result = corruption_scenarios()["out_of_order_receipt"]["verification"]
        self.assertTrue(result.passed)
        self.assertTrue(result.used_sorted_receipts)

    def test_invalid_schema_blocked(self) -> None:
        authority = AuthorityLayer(graph=MemoryGraph(), receipt_log=ReceiptLog(), checkpoint_layer=CheckpointLayer())
        with self.assertRaises(ValueError):
            authority.register_memory(replace(generated_memory(1), confidence=2.0), step=1)
        result = run_generated_simulation(5)
        receipts = result["receipt_objects"]
        bad_receipt = Receipt(
            receipt_id="bad-receipt",
            step=999,
            action="bad",
            memory_id="bad-memory",
            before_state=None,
            after_state={
                "id": "bad-memory",
                "text": "bad",
                "tags": [],
                "evidence": [],
                "confidence": 2.0,
                "explicit_importance": 0.0,
                "recurrence": 0.0,
                "outcome_reinforcement": 0.0,
                "recent_utility": 0.0,
                "causal_connectedness": 0.0,
                "decay": 0.0,
                "contradiction": 0.0,
                "redundancy": 0.0,
                "noise": 0.0,
                "created_step": 1,
                "last_used_step": 1,
                "lifecycle_state": "KEEP",
                "causal_links": [],
            },
            score_breakdown={"final_score": 0.0},
            authority_decision="APPROVED",
            reason="bad",
        )
        verification = verify_replay(receipts + [bad_receipt], result["final_state"])
        self.assertFalse(verification.passed)

    def test_deterministic_repeated_run_hash(self) -> None:
        result = deterministic_run_hash(100)
        self.assertTrue(result["matched"])

    def test_stress_results_artifact_generated(self) -> None:
        temp_dir = Path(os.getcwd()) / f"test_stress_{uuid4().hex}"
        temp_dir.mkdir()
        try:
            result = write_stress_results(temp_dir / "artifacts")
            self.assertTrue(Path(result["path"]).is_file())
            contents = Path(result["path"]).read_text(encoding="utf-8")
            self.assertIn("1,000-memory simulation", contents)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
