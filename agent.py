"""A tiny, dependency-free agent loop for learning purposes."""

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class AgentResult:
    """The agent's answer and the action it selected."""

    answer: str
    action: str


def run_agent(request: str, status_tool: Callable[[], str]) -> AgentResult:
    """Route a request to a safe read-only tool or answer directly.

    This is deliberately rule-based. Later, an LLM can replace the routing
    decision, while the tool boundary remains explicit and testable.
    """
    normalized = request.strip().lower()

    if "status" in normalized or "health" in normalized:
        evidence = status_tool()
        return AgentResult(
            answer=f"System status: {evidence}",
            action="read_status",
        )

    return AgentResult(
        answer=(
            "I can currently answer simple questions or check system status. "
            "No infrastructure-changing actions are available."
        ),
        action="direct_answer",
    )


if __name__ == "__main__":
    result = run_agent("What is the system status?", lambda: "healthy")
    print(result.answer)
