# Copilot & Agent Instructions — personal_assistant_agent

Purpose
-------
This repository contains a Python-based personal assistant agent that integrates with Gmail and Google Calendar, runs locally with Ollama for development, and can switch to Anthropic Claude for production. These instructions guide GitHub Copilot, local AI agents, and contributors so suggestions and automated edits "vibe" with the project's conventions, safety rules, and workflows.

Who should read this
---------------------
- GitHub Copilot or other code assistance tools
- AI agents used in CI or local automation (refactoring bots, PR assistants)
- New contributors who want to generate code or ask the agent to make changes

High-level goals for suggestions
--------------------------------
When producing code, Copilot/agents should prefer:
- Small, surgical changes focused on the requested feature/bug fix
- Clear test coverage where feasible (unit tests for logic-heavy code)
- Preserving security and privacy (never create or commit secrets)
- Minimal external dependencies unless necessary for the feature
- Readable, idiomatic Python (project targets Python 3.12)

Repo layout reference (short)
-----------------------------
- agent.py              — LangGraph agent and tool definitions
- main.py               — FastAPI backend (SSE streaming of agent thinking)
- gmail_tool.py         — Gmail read + draft creation
- calendar_tool.py      — Google Calendar read + create events
- client/               — React + Vite frontend (chat UI)
- requirements.txt      — Python dependencies
- test_*.py             — Tests for agent and integrations

Safety & security rules (must follow)
-------------------------------------
- Never generate or add actual API keys, tokens, credentials.json, or token.json into the repo.
- If a task requires credentials, instruct the user to add them locally and explain how (see README). Do not fabricate values.
- The agent only creates Gmail drafts; never add code that sends emails automatically without explicit human review.
- Add entries to .gitignore for token.json, credentials.json, .env, venv/ and other local secrets if creating examples.

Environment & runtime guidance
-----------------------------
- Development LLM: Ollama (llama3.1). Ollama runs locally and should be used during offline development.
  - Typical flow: ollama pull llama3.1 && ollama serve
- Production LLM: Anthropic Claude. Use only when APP_ENV=production and ANTHROPIC_API_KEY is provided by the human operator.
- Backend: FastAPI + uvicorn. Use uvicorn main:app --reload during development.
- Frontend: client/ (React + Vite). Use npm install && npm run dev inside client/.

Testing & verification
----------------------
- Run unit tests before submitting changes: python3 -m pytest -q or python3 test_agent.py for basic checks.
- When modifying agent/tool behavior, run integration checks where possible (test_gmail.py/test_calendar.py) but only with local credentials and explicit human consent.
- If adding new Python deps, add them to requirements.txt and confirm pip install -r requirements.txt completes successfully.

Coding style & static checks
---------------------------
- Use idiomatic Python. Keep functions small and single-responsibility.
- When possible prefer typing annotations for public functions and method signatures.
- Favor clear variable names; avoid single-letter names except in short loops.
- Add docstrings for new modules and public functions following the existing style.

Guidance for automated edits (PR/branch bots)
--------------------------------------------
- Create a single-purpose branch and include a short, descriptive commit message.
- Keep PRs small and focused (one feature/bug per PR). If changes are cross-cutting, explain in PR description.
- Include tests and, if changing public behavior, update README where relevant.
- Do not modify core authentication flows (OAuth) without explicit human review.

Helpful prompt patterns (for humans using Copilot/agents)
--------------------------------------------------------
Use concise prompts that set scope, constraints, and verification steps. Examples:

- "Refactor the Gmail draft creation in gmail_tool.py to extract a _build_message helper. Add unit tests for subject and recipient formatting. Keep behavior identical."
- "Add error handling to calendar_tool.py when Google API returns 429. Retry up to 3 times with exponential backoff. Add tests simulating 429 responses."
- "Explain what agent.py does in plain language and list its tool functions and side effects."
- "Create a small README section in client/ describing how the UI listens to SSE from the backend."
- "Add a unit test that mocks Gmail API and verifies the agent creates a draft but does not send."

Best practices for prompts to the agent
--------------------------------------
- Include the target file path (e.g., `gmail_tool.py`) and a short explanation of desired behavior.
- Specify "don't commit secrets" when the task touches configuration files.
- Request tests in the same PR: "Please add pytest tests that validate X".
- Request small, reversible changes: "Make this change in a new branch named feat/draft-helper and push a PR" — only if CI/automation has permission to push.

What to do if secrets are accidentally added
-------------------------------------------
- Immediately remove the file from the repo and inform maintainers.
- Use `git filter-repo` or `git filter-branch` (human operator only) to remove sensitive data from history.
- Rotate any exposed keys immediately (human operator responsibility).

Agent persona & tone
--------------------
- Helpful, concise, and safety-conscious.
- Offer brief reasoning for non-trivial suggestions (1–2 lines). Example: "Using retry with backoff because the Google API throttles bursts (429)."
- When uncertain about credential/permission operations, always ask for human confirmation.

Common developer workflows (examples)
-------------------------------------
- Local dev run (backend + Ollama + frontend):
  1. Start Ollama: `ollama pull llama3.1 && ollama serve`
  2. Activate venv and install deps: `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
  3. Start backend: `uvicorn main:app --reload`
  4. Start frontend: `cd client && npm install && npm run dev`

- Switching to Anthropic (production testing):
  - Set APP_ENV=production and ANTHROPIC_API_KEY in local environment, confirm behavior with human oversight.

Examples of allowed automated tasks
----------------------------------
- Formatting code (black/isort) if configured in repo
- Minor refactors that include tests and preserve behavior
- Adding documentation and example prompts

Examples of disallowed automated tasks
-------------------------------------
- Adding credentials or demo keys to any file
- Changing OAuth scopes, consent screens, or production deployment settings without human approval
- Enabling automatic sending of email messages (agent must create drafts only)

Where to find help
------------------
- README.md: repo overview and setup instructions.
- Tests: test_agent.py, test_gmail.py, test_calendar.py — examples of verification.
- For OAuth and Google APIs, refer to Google Cloud Console docs and the README instructions in this repo.

Footer / contact
----------------
If the agent or Copilot suggestions are unclear or risky, ask a human maintainer for confirmation before applying changes.

(End of copilot-instructions.md)
