import unittest

import app


class AppTests(unittest.TestCase):
    def test_default_config_is_local_only(self):
        self.assertTrue(app.is_configured())

    def test_project_summary_format(self):
        summary = app.summarize_project("demo", completed_tasks=2, open_tasks=3)
        self.assertEqual(app.format_summary(summary), "demo: 2 completed, 3 open")

    def test_feature_flags_default_off(self):
        self.assertFalse(app.is_feature_enabled("experimental_summary_view"))

    def test_normalize_status(self):
        self.assertEqual(app.normalize_status(" OK "), "ok")


if __name__ == "__main__":
    unittest.main()
