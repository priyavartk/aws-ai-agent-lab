import unittest

from src.policy import ActionPolicy


class PolicyTests(unittest.TestCase):
    def test_read_only_policy_allows_status_only(self):
        policy = ActionPolicy.read_only()

        self.assertTrue(policy.allows("read_status"))
        self.assertFalse(policy.allows("deploy"))


if __name__ == "__main__":
    unittest.main()
