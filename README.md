# AWS AI Agent Lab

A hands-on project for learning how to build a read-only AI agent on AWS.

## Learning goals

1. Call a model safely.
2. Structure an agent’s instructions and responses.
3. Add read-only tools.
4. Ground answers in evidence.
5. Add tests, evaluation, and observability.
6. Deploy only after the local design is understood.

## Safety and budget principles

- Never commit secrets, access keys, tokens, or sensitive logs.
- Use IAM roles and temporary credentials.
- Start with local mocks before paid AWS API calls.
- Add an AWS Budget alert before using billable services.
- Keep the initial agent read-only.

## Project status

Repository created. Safety foundations are in place.
