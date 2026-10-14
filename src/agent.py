"""A tiny, dependency-free agent loop for learning purposes."""

from dataclasses import dataclass
from typing import Callable

from .policy import ActionPolicy


@dataclass(frozen=True)
class AgentResult:
    """The agent's answer and the action it selected."""

    answer: str
    action: str


def run_agent(
    request: str,
    tools: dict[str, Callable[[], str]],
    trace: list[dict[str, str]] | None = None,
    policy: ActionPolicy | None = None,
) -> AgentResult:
    """Route a request to a safe read-only tool or answer directly.

    This is deliberately rule-based. Later, an LLM can replace the routing
    decision, while the tool boundary remains explicit and testable.
    """
    policy = policy or ActionPolicy.read_only()
    normalized = request.strip().lower()

    if "status" in normalized or "health" in normalized:
        return _run_tool_action(
            action="read_status",
            unavailable_answer="Status checks are not enabled for this agent.",
            tools=tools,
            policy=policy,
            trace=trace,
            answer_prefix="System status: ",
        )

    if "deploy" in normalized and "deploy" in tools:
        return _run_tool_action(
            action="deploy",
            unavailable_answer="Deployment actions are not enabled for this agent.",
            tools=tools,
            policy=policy,
            trace=trace,
            answer_prefix="Deployment result: ",
        )

    result = AgentResult(
        answer=(
            "I can currently answer simple questions or check system status. "
            "No infrastructure-changing actions are available."
        ),
        action="direct_answer",
    )
    _record(trace, result.action, "completed")
    return result


def _run_tool_action(
    action: str,
    unavailable_answer: str,
    tools: dict[str, Callable[[], str]],
    policy: ActionPolicy,
    trace: list[dict[str, str]] | None,
    answer_prefix: str,
) -> AgentResult:
    if action not in tools:
        result = AgentResult(answer=unavailable_answer, action="tool_unavailable")
        _record(trace, result.action, "blocked")
        return result

    if not policy.allows(action):
        result = AgentResult(
            answer=f"Action '{action}' is blocked by policy.",
            action="policy_blocked",
        )
        _record(trace, result.action, "blocked")
        return result

    result = AgentResult(
        answer=f"{answer_prefix}{tools[action]()}",
        action=action,
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
