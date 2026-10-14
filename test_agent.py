import unittest

from src.agent import run_agent


class AgentTests(unittest.TestCase):
    def test_status_request_uses_read_only_tool(self):
        calls = []

        def status_tool():
            calls.append("called")
            return "healthy"

        result = run_agent("Can you check the service status?", status_tool)

        self.assertEqual(result.action, "read_status")
        self.assertEqual(result.answer, "System status: healthy")
        self.assertEqual(calls, ["called"])

    def test_unknown_request_does_not_call_tool(self):
        result = run_agent("Deploy the application", lambda: self.fail("called"))

        self.assertEqual(result.action, "direct_answer")
        self.assertIn("No infrastructure-changing actions", result.answer)


if __name__ == "__main__":
    unittest.main()
