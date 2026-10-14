import unittest

from src.agent import run_agent


class AgentTests(unittest.TestCase):
    def test_status_request_uses_read_only_tool(self):
        calls = []

        def status_tool():
            calls.append("called")
            return "healthy"

        result = run_agent("Can you check the service status?", {"read_status": status_tool})

        self.assertEqual(result.action, "read_status")
        self.assertEqual(result.answer, "System status: healthy")
        self.assertEqual(calls, ["called"])

    def test_unknown_request_does_not_call_tool(self):
        result = run_agent("Deploy the application", {"read_status": lambda: self.fail("called")})

        self.assertEqual(result.action, "direct_answer")
        self.assertIn("No infrastructure-changing actions", result.answer)

    def test_status_tool_can_be_disabled(self):
        result = run_agent("Check the service status", {})

        self.assertEqual(result.action, "tool_unavailable")
        self.assertEqual(result.answer, "Status checks are not enabled for this agent.")


if __name__ == "__main__":
    unittest.main()
