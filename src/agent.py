"""A tiny, dependency-free agent loop for learning purposes."""

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class AgentResult:
    """The agent's answer and the action it selected."""

    answer: str
    action: str


def run_agent(
    request: str,
    tools: dict[str, Callable[[], str]],
    trace: list[dict[str, str]] | None = None,
) -> AgentResult:
    """Route a request to a safe read-only tool or answer directly.

    This is deliberately rule-based. Later, an LLM can replace the routing
    decision, while the tool boundary remains explicit and testable.
    """
    normalized = request.strip().lower()

    if "status" in normalized or "health" in normalized:
        if "read_status" not in tools:
            result = AgentResult(
                answer="Status checks are not enabled for this agent.",
                action="tool_unavailable",
            )
            _record(trace, result.action, "blocked")
            return result

        evidence = tools["read_status"]()
        result = AgentResult(
            answer=f"System status: {evidence}",
            action="read_status",
        )
        _record(trace, result.action, "completed")
        return result

    result = AgentResult(
        answer=(
            "I can currently answer simple questions or check system status. "
            "No infrastructure-changing actions are available."
        ),
        action="direct_answer",
    )
    _record(trace, result.action, "completed")
    return result


def _record(
    trace: list[dict[str, str]] | None,
    action: str,
    outcome: str,
) -> None:
    """Record safe metadata without storing the user's full request."""
    if trace is not None:
        trace.append({"action": action, "outcome": outcome})


if __name__ == "__main__":
    result = run_agent("What is the system status?", {"read_status": lambda: "healthy"})
    print(result.answer)
