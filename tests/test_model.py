import unittest

from src.model import FakeModel


class ModelTests(unittest.TestCase):
    def test_fake_model_is_deterministic_and_records_prompt(self):
        model = FakeModel("local answer")

        answer = model.generate("Explain tool calling")

        self.assertEqual(answer, "local answer")
        self.assertEqual(model.prompts, ["Explain tool calling"])


if __name__ == "__main__":
    unittest.main()
