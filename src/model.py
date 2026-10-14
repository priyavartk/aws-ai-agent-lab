"""Model boundary used by the agent application."""

from typing import Protocol


class TextModel(Protocol):
    """The smallest interface our agent needs from a language model."""

    def generate(self, prompt: str) -> str:
        """Generate text from a prompt."""


class FakeModel:
    """Deterministic local model for tests and cheap development."""

    def __init__(self, response: str = "This is a local model response.") -> None:
        self.response = response
        self.prompts: list[str] = []

    def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.response
