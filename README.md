# AWS AI Agent Lab

A hands-on learning project exploring how to build AI agents with practical governance controls.

The project asks a practical question:

> How can small and medium-sized enterprises keep AI agents responsible and accountable without immediately investing in complex engineering or expensive governance tooling?

## Current focus

The first implementation demonstrates:

1. **Tool registry** — which capabilities are available to the agent.
2. **Action policy** — which available capabilities are permitted.
3. **Trace recording** — what action was selected and whether it completed or was blocked.

The agent is deliberately local and mocked. It does not call Amazon Bedrock, access AWS resources or execute real infrastructure changes.

## Governance flow

```text
User request
    ↓
Agent identifies intended action
    ↓
Tool registry checks availability
    ↓
Policy checks permission and risk
    ↓
ALLOW, PAUSE, DENY or ESCALATE
    ↓
Action executes, waits for approval or is blocked
    ↓
Trace records the outcome
```

## Human control and escalation

A useful governance layer should not only answer “yes” or “no”. It should also identify when the agent needs human judgement.

```text
ALLOW       Continue automatically
PAUSE       Request human approval
DENY        Block the action
ESCALATE    Send the decision to a higher-level controller
```

The current prototype demonstrates allowed and denied actions. `PAUSE` and `ESCALATE` are planned extensions.

Examples of when human control may be appropriate:

- A change targets a production environment.
- The action is destructive or difficult to reverse.
- Required security or change approval is missing.
- The agent is uncertain about the intended outcome.
- Multiple individually valid actions create combined workflow risk.
- The requested action conflicts with a higher-priority policy.

## Assessing destructive actions

Before a potentially destructive action is executed, a policy engine should assess more than the tool name. It should consider:

- **Action:** What will happen?
- **Target:** Which resource or environment is affected?
- **Impact:** Could data, availability or security be affected?
- **Reversibility:** Can the action be safely undone?
- **Approval:** Is the required human approval present?
- **Identity:** Who or which agent requested it?
- **Context:** Does it match the original goal and workflow?

For example:

```text
Request: Delete a production database
Risk: High
Reversible: No or difficult
Approval: Missing
Decision: PAUSE or DENY
```

The agent should not be able to override this decision by itself. Any exception should require an authorised human or higher-level controller, be limited in scope and be recorded for audit.

## Example scenario

A user asks:

```text
Deploy the Terraform change to production
```

The agent may identify `deploy` as the intended action. The governance layer then checks whether deployment is available, whether the current policy permits it, whether approvals exist and whether the workflow remains aligned with the original goal.

The current read-only policy blocks deployment before the tool is executed.

```text
Tool registered?       Yes
Action allowed?        No
Result                 Blocked
Trace                  policy_blocked
```

## Repository structure

```text
aws-ai-agent-lab/
├── src/
│   ├── agent.py       # Request routing and execution flow
│   ├── cli.py         # Command-line interface
│   ├── model.py       # Model abstraction and fake model
│   └── policy.py      # Allowed-action policy
├── tests/
│   ├── test_agent.py  # Agent behavior and blocked actions
│   ├── test_model.py  # Model abstraction tests
│   └── test_policy.py # Policy tests
├── .env.example       # Non-secret configuration example
├── .gitignore         # Secret and local-file protection
└── README.md          # Project goals and learning notes
```

## Run the project

```bash
git clone -b dev https://github.com/priyavartk/aws-ai-agent-lab.git
cd aws-ai-agent-lab
python3 -m unittest discover -s tests -v
python3 -m compileall -q src tests
python3 -m src.cli --request "What is the system status?"
```

## Safety and budget principles

- Never commit AWS keys, tokens, passwords or `.env` files.
- Use IAM roles and temporary credentials.
- Start with local mocks before using paid AWS services.
- Add an AWS Budget alert before using billable services.
- Keep the first real agent read-only.
- Require human approval for high-risk or destructive actions.
- Record policy decisions and overrides for audit.

## Roadmap

1. Complete the local agent and policy demonstrations.
2. Add workflow context such as environment, identity and approval state.
3. Add destructive-action risk assessment.
4. Implement `PAUSE` and `ESCALATE` outcomes.
5. Connect a real model through the existing model interface.
6. Add Amazon Bedrock with cost controls.
7. Introduce read-only AWS operational tools.
8. Add workflow-level policy evaluation and audit correlation.

This is a learning implementation, not a production governance platform. The goal is to test the ideas incrementally and understand how agent autonomy can operate inside explicit human-controlled boundaries.
