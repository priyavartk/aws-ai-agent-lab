"""Simple allowlist policy for agent actions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ActionPolicy:
    """Actions the application permits the agent to execute."""

    allowed_actions: frozenset[str]

    @classmethod
    def read_only(cls) -> "ActionPolicy":
        """The safe default policy for the first version of the agent."""
        return cls(allowed_actions=frozenset({"read_status"}))

    def allows(self, action: str) -> bool:
        return action in self.allowed_actions
