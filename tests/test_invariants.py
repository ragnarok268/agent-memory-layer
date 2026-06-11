import unittest

from grand_challenges_library.invariants import list_invariants


class InvariantTests(unittest.TestCase):
    def test_list_invariants_returns_all_starter_invariants(self) -> None:
        invariants = list_invariants()

        self.assertEqual(len(invariants), 14)

    def test_list_invariants_can_filter_by_challenge(self) -> None:
        invariants = list_invariants("memory")
        statements = [item.statement for item in invariants]

        self.assertEqual(len(invariants), 2)
        self.assertIn("Memory must distinguish canonical facts from temporary assumptions.", statements)
        self.assertIn("Memory reuse must check whether state has been superseded.", statements)


if __name__ == "__main__":
    unittest.main()
