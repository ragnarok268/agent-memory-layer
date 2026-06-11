from __future__ import annotations

import os
from pathlib import Path
import shutil
import unittest
from uuid import uuid4
from dataclasses import FrozenInstanceError, replace

from mindfreak.authority import AuthorityLayer
from mindfreak.checkpoint import CheckpointLayer
from mindfreak.consolidation import ConsolidationLayer
from mindfreak.constants import LIFECYCLE_COMPRESS, LIFECYCLE_FORGET, LIFECYCLE_KEEP, LIFECYCLE_PROMOTE
from mindfreak.demos.simulate_weeks import run_simulation
from mindfreak.inspection import generate_inspection_bundle
from mindfreak.memory_graph import MemoryGraph, UnauthorizedMutationError
from mindfreak.models import MemoryObject
from mindfreak.receipts import ReceiptLog
from mindfreak.reporting import generate_report_artifacts
from mindfreak.replay import verify_replay
from mindfreak.weights import clamp, decide_lifecycle, score_memory


def make_memory(**overrides: object) -> MemoryObject:
    base = MemoryObject(
        id="memory-1",
        text="Baseline memory",
        tags=(),
        evidence=("note",),
        confidence=0.60,
        explicit_importance=0.60,
        recurrence=0.50,
        outcome_reinforcement=0.60,
        recent_utility=0.50,
        causal_connectedness=0.50,
        decay=0.10,
        contradiction=0.00,
        redundancy=0.05,
        noise=0.05,
        created_step=1,
        last_used_step=1,
        lifecycle_state=LIFECYCLE_KEEP,
        causal_links=(),
    )
    return replace(base, **overrides)


class MindfreakTests(unittest.TestCase):
    def test_scoring_is_deterministic(self) -> None:
        memory = make_memory()
        self.assertEqual(score_memory(memory), score_memory(memory))

    def test_score_outputs_are_clamped(self) -> None:
        high = make_memory(
            explicit_importance=1.0,
            recurrence=1.0,
            outcome_reinforcement=1.0,
            recent_utility=1.0,
            causal_connectedness=1.0,
            confidence=1.0,
            decay=0.0,
            contradiction=0.0,
            redundancy=0.0,
            noise=0.0,
        )
        low = make_memory(
            explicit_importance=0.0,
            recurrence=0.0,
            outcome_reinforcement=0.0,
            recent_utility=0.0,
            causal_connectedness=0.0,
            confidence=0.0,
            decay=1.0,
            contradiction=1.0,
            redundancy=1.0,
            noise=1.0,
        )
        self.assertEqual(score_memory(high).final_score, clamp(score_memory(high).raw_score))
        self.assertEqual(score_memory(low).final_score, 0.0)

    def test_exact_threshold_boundaries_work(self) -> None:
        self.assertEqual(decide_lifecycle(0.80), LIFECYCLE_PROMOTE)
        self.assertEqual(decide_lifecycle(0.79), LIFECYCLE_KEEP)
        self.assertEqual(decide_lifecycle(0.50), LIFECYCLE_KEEP)
        self.assertEqual(decide_lifecycle(0.49), LIFECYCLE_COMPRESS)
        self.assertEqual(decide_lifecycle(0.25), LIFECYCLE_COMPRESS)
        self.assertEqual(decide_lifecycle(0.24), LIFECYCLE_FORGET)

    def test_contradiction_reduces_score(self) -> None:
        memory = make_memory(contradiction=0.0)
        contradicted = make_memory(contradiction=0.8)
        self.assertGreater(score_memory(memory).final_score, score_memory(contradicted).final_score)

    def test_stale_noisy_memory_forgets(self) -> None:
        graph = MemoryGraph()
        authority = AuthorityLayer(graph=graph, receipt_log=ReceiptLog(), checkpoint_layer=CheckpointLayer())
        memory = make_memory(
            id="stale",
            evidence=("old note",),
            explicit_importance=0.05,
            recurrence=0.05,
            outcome_reinforcement=0.0,
            recent_utility=0.0,
            causal_connectedness=0.0,
            confidence=0.10,
            decay=0.80,
            contradiction=0.10,
            redundancy=0.20,
            noise=0.90,
        )
        authority.register_memory(memory, step=1)
        self.assertEqual(graph.get_memory("stale").lifecycle_state, LIFECYCLE_FORGET)

    def test_high_causal_important_memory_promotes(self) -> None:
        graph = MemoryGraph()
        authority = AuthorityLayer(graph=graph, receipt_log=ReceiptLog(), checkpoint_layer=CheckpointLayer())
        memory = make_memory(
            id="promote",
            tags=("global_assumption",),
            evidence=("spec",),
            confidence=1.00,
            explicit_importance=1.00,
            recurrence=1.00,
            outcome_reinforcement=1.00,
            recent_utility=1.00,
            causal_connectedness=1.00,
            decay=0.00,
            contradiction=0.00,
            redundancy=0.00,
            noise=0.00,
        )
        authority.register_memory(memory, step=2)
        self.assertEqual(graph.get_memory("promote").lifecycle_state, LIFECYCLE_PROMOTE)

    def test_promote_without_evidence_is_blocked(self) -> None:
        graph = MemoryGraph()
        receipts = ReceiptLog()
        authority = AuthorityLayer(graph=graph, receipt_log=receipts, checkpoint_layer=CheckpointLayer())
        memory = make_memory(
            id="blocked",
            evidence=(),
            confidence=1.00,
            explicit_importance=1.00,
            recurrence=1.00,
            outcome_reinforcement=1.00,
            recent_utility=1.00,
            causal_connectedness=1.00,
            decay=0.00,
            contradiction=0.00,
            redundancy=0.00,
            noise=0.00,
        )
        receipt = authority.register_memory(memory, step=2)
        self.assertEqual(receipt.authority_decision, "BLOCKED")
        self.assertIsNone(graph.get_memory("blocked"))

    def test_unauthorized_mutation_is_impossible(self) -> None:
        graph = MemoryGraph()
        with self.assertRaises(UnauthorizedMutationError):
            graph.apply_authorized_change(make_memory(), token=object())  # type: ignore[arg-type]

        authority = AuthorityLayer(graph=graph, receipt_log=ReceiptLog(), checkpoint_layer=CheckpointLayer())
        authority.register_memory(make_memory(id="frozen"), step=1)
        frozen_memory = graph.get_memory("frozen")
        with self.assertRaises(FrozenInstanceError):
            frozen_memory.text = "mutated"  # type: ignore[misc]

    def test_checkpoint_triggers_only_under_locked_rule(self) -> None:
        checkpoints = CheckpointLayer()
        authority = AuthorityLayer(graph=MemoryGraph(), receipt_log=ReceiptLog(), checkpoint_layer=checkpoints)
        authority.register_memory(
            make_memory(
                id="no-checkpoint",
                tags=("misc",),
                evidence=("spec",),
                confidence=0.95,
                explicit_importance=0.90,
                recurrence=0.90,
                outcome_reinforcement=0.90,
                recent_utility=0.90,
                causal_connectedness=0.90,
                decay=0.01,
                contradiction=0.00,
                redundancy=0.00,
                noise=0.00,
            ),
            step=1,
        )
        authority.register_memory(
            make_memory(
                id="checkpoint",
                tags=("project_structure",),
                evidence=("spec",),
                confidence=0.95,
                explicit_importance=0.90,
                recurrence=0.90,
                outcome_reinforcement=0.90,
                recent_utility=0.90,
                causal_connectedness=0.90,
                decay=0.01,
                contradiction=0.00,
                redundancy=0.00,
                noise=0.00,
            ),
            step=2,
        )
        self.assertEqual(len(checkpoints.list_checkpoints()), 1)
        self.assertEqual(checkpoints.list_checkpoints()[0].memory_id, "checkpoint")

    def test_replay_rebuilds_same_final_state(self) -> None:
        graph = MemoryGraph()
        receipts = ReceiptLog()
        authority = AuthorityLayer(graph=graph, receipt_log=receipts, checkpoint_layer=CheckpointLayer())
        consolidation = ConsolidationLayer()
        authority.register_memory(make_memory(id="a"), step=1)
        authority.register_memory(make_memory(id="b", causal_links=("a",), tags=("project_structure",)), step=1)
        consolidation.reinforce_memory(authority, "a", step=2)
        result = verify_replay(receipts.list_receipts(), graph.final_state())
        self.assertTrue(result.passed)

    def test_consolidation_preserves_evidence_links(self) -> None:
        graph = MemoryGraph()
        receipts = ReceiptLog()
        authority = AuthorityLayer(graph=graph, receipt_log=receipts, checkpoint_layer=CheckpointLayer())
        consolidation = ConsolidationLayer()
        authority.register_memory(make_memory(id="primary", evidence=("e1",), causal_links=("x",)), step=1)
        authority.register_memory(
            make_memory(
                id="duplicate",
                evidence=("e2",),
                causal_links=("y",),
                recurrence=0.20,
                outcome_reinforcement=0.10,
                recent_utility=0.10,
                explicit_importance=0.20,
            ),
            step=1,
        )
        consolidation.consolidate_pair(authority, primary_id="primary", duplicate_id="duplicate", step=2)
        primary = graph.get_memory("primary")
        duplicate = graph.get_memory("duplicate")
        self.assertEqual(primary.evidence, ("e1", "e2"))
        self.assertEqual(primary.causal_links, ("x", "y"))
        self.assertEqual(duplicate.evidence, ("e1", "e2"))

    def test_report_artifacts_are_generated(self) -> None:
        temp_dir = Path(os.getcwd()) / f"test_artifacts_{uuid4().hex}"
        temp_dir.mkdir()
        try:
            artifact_root = temp_dir / "artifacts"
            result = run_simulation(artifact_root=artifact_root)
            artifact_paths = generate_report_artifacts(result, artifact_root=artifact_root)
            self.assertTrue(os.path.isdir(artifact_paths["case_cards"]))
            self.assertTrue(os.path.isfile(artifact_paths["timeline"]))
            self.assertTrue(os.path.isfile(artifact_paths["report"]))
            case_cards = [name for name in os.listdir(artifact_paths["case_cards"]) if name.endswith(".md")]
            self.assertEqual(len(case_cards), result["receipts_written"])
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_report_artifacts_include_expected_content(self) -> None:
        temp_dir = Path(os.getcwd()) / f"test_artifacts_{uuid4().hex}"
        temp_dir.mkdir()
        try:
            artifact_root = temp_dir / "artifacts"
            result = run_simulation(artifact_root=artifact_root)
            artifact_paths = generate_report_artifacts(result, artifact_root=artifact_root)
            timeline_text = Path(artifact_paths["timeline"]).read_text(encoding="utf-8")
            report_text = Path(artifact_paths["report"]).read_text(encoding="utf-8")
            self.assertIn("Week 1", timeline_text)
            self.assertIn("Replay: `PASS`", report_text)
            self.assertIn("Lifecycle Counts", report_text)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_inspection_artifacts_are_generated(self) -> None:
        temp_dir = Path(os.getcwd()) / f"test_artifacts_{uuid4().hex}"
        temp_dir.mkdir()
        try:
            inspection = generate_inspection_bundle(artifact_root=temp_dir / "artifacts", run_tests=False)
            for path in inspection["paths"]:
                self.assertTrue(Path(path).is_file())
            self.assertTrue((temp_dir / "artifacts" / "inspection" / "stress_results.md").is_file())
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_replay_inspection_contains_pass(self) -> None:
        temp_dir = Path(os.getcwd()) / f"test_artifacts_{uuid4().hex}"
        temp_dir.mkdir()
        try:
            inspection = generate_inspection_bundle(artifact_root=temp_dir / "artifacts", run_tests=False)
            replay_text = Path(inspection["paths"][1]).read_text(encoding="utf-8")
            self.assertIn("Replay status: `PASS`", replay_text)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_algorithm_audit_contains_exact_weights(self) -> None:
        temp_dir = Path(os.getcwd()) / f"test_artifacts_{uuid4().hex}"
        temp_dir.mkdir()
        try:
            inspection = generate_inspection_bundle(artifact_root=temp_dir / "artifacts", run_tests=False)
            audit_text = Path(inspection["paths"][3]).read_text(encoding="utf-8")
            self.assertIn("`explicit_importance`: `0.18`", audit_text)
            self.assertIn("`contradiction`: `0.18`", audit_text)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_lifecycle_analysis_contains_all_lifecycle_states(self) -> None:
        temp_dir = Path(os.getcwd()) / f"test_artifacts_{uuid4().hex}"
        temp_dir.mkdir()
        try:
            inspection = generate_inspection_bundle(artifact_root=temp_dir / "artifacts", run_tests=False)
            lifecycle_text = Path(inspection["paths"][2]).read_text(encoding="utf-8")
            self.assertIn("## PROMOTE", lifecycle_text)
            self.assertIn("## KEEP", lifecycle_text)
            self.assertIn("## COMPRESS", lifecycle_text)
            self.assertIn("## FORGET", lifecycle_text)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
