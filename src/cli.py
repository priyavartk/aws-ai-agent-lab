"""Command-line entry point for the local learning agent."""

import argparse

from .agent import run_agent


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local read-only agent")
    parser.add_argument(
        "--request",
        required=True,
        help="The request to send to the agent",
    )
    args = parser.parse_args()

    trace: list[dict[str, str]] = []
    result = run_agent(
        args.request,
        {"read_status": lambda: "healthy"},
        trace,
    )

    print(f"Action: {result.action}")
    print(f"Answer: {result.answer}")
    print(f"Trace: {trace}")


if __name__ == "__main__":
    main()
