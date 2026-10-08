## Common first 15 minutes — start with a fresh GitHub repo

1. Go to **https://github.com/new** and create a new **private** repository. Do not initialize it with a README.
2. Unzip this starter locally and push it:

```bash
git init
git add .
git commit -m "lab: starter application"
git branch -M main
git remote add origin <YOUR-NEW-REPO-URL>
git push -u origin main
```

3. Open the folder in VS Code, sign in to GitHub Copilot, and **Trust the workspace**.
4. Use the **Local** agent harness/session target. Hooks in this lab use VS Code Local-hook events.
5. Create the environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
npm install
npx playwright install chromium
```

6. Run `pytest -q` and `npm run test:ui`. The starter must be green.
7. Read `work-items/MP1.md` before changing code.

# Mini-project 1 — Multi-Agent Maintenance Guard

**Spotlight:** custom agents, dynamic subagent selection, multiple handoffs, isolated context, tool scoping, an agent-scoped `Stop` hook, UI + Playwright.

## What you are learning

This lab deliberately separates two orchestration patterns:

- **Dynamic subagent selection:** the Implementation parent chooses temporary specialists at runtime based on test results and the type of files/contract changed. Specialist findings return to Implementation.
- **Handoff:** when the implementation stage is complete, control moves to another top-level agent. The available handoffs are static choices: Standard Code Review, Security Review, or Re-plan Change.

The Implementation agent also has an **agent-scoped Stop hook**. If it attempts to finish while pytest or Playwright is red, the hook blocks completion and feeds the failure back into the agent loop.

## Phase 1 — inspect the agent envelopes (20 min)

The starter already contains the agents under `.github/agents/` so you can focus on using them. Inspect:

- `Planner`
- `Codebase Researcher`
- `Implementation`
- `Test Fixer`
- `Security Reviewer`
- `API Specialist`
- `Reviewer`

Identify which ones can edit files and which are read-only.

## Phase 2 — Planner → Researcher → human approval (30 min)

Select **Planner** and give it MP1. Require it to delegate repository investigation to **Codebase Researcher**.

Expected pattern:

`Planner → Researcher subagent → findings return → Planner plan → human approval`

Do not implement until the plan is acceptable. Then click **Start Implementation**.

## Phase 3 — Implementation with runtime specialist selection (70 min)

Implementation must add the maintenance-mode API/UI behavior and tests.

During the work, observe which specialists it chooses:

1. **Test Fixer** — when pytest/Playwright evidence is red.
2. **API Specialist** — when routes, status codes, request/response shape, or Redfish-style contract behavior changes.
3. **Security Reviewer** — if you introduce a security-sensitive variant or if privileged-operation handling warrants independent security review.
4. **Codebase Researcher** — when existing patterns need discovery.

### Instructor/learner injection: force at least two different specialist paths

After the first implementation attempt, choose two of these prompts/evidence injections:

- **Test path:** introduce or surface a failing UI/API test and ask Implementation to continue.
- **API path:** ask whether returning HTTP `409` and the new maintenance-mode endpoint are contract-consistent; Implementation should delegate to API Specialist.
- **Security path:** ask whether enabling maintenance mode should be treated as a privileged action; Implementation should delegate to Security Reviewer before final transition.

The parent Implementation agent must remain in control and incorporate the returned findings.

## Phase 4 — demonstrate the Stop hook (20 min)

Before all tests are green, ask Implementation to summarize and finish. The agent-scoped `Stop` hook should run:

- `python -m pytest -q`
- `npm run test:ui`

If either fails, completion is blocked and the evidence is returned to Copilot. Let the agent diagnose/correct once. The hook contains a loop guard so repeated failure escalates rather than running forever.

## Phase 5 — multiple handoffs (25 min)

When all verification is green, inspect the three handoff choices:

- **Standard Code Review** → `Reviewer`
- **Security Review** → `Security Reviewer`
- **Re-plan Change** → `Planner`

Choose the transition that matches the actual runtime evidence. This selection is intentionally a workflow/HITL decision; the YAML handoffs themselves do not contain LangGraph-style dynamic conditions.

The Reviewer also has **Fix Review Findings**, which hands control back to Implementation if blockers are found.

## Phase 6 — PR and debrief (25 min)

Rerun tests, inspect `git diff`, commit, push, and open a PR. Do not merge automatically.

Be ready to explain:

1. Why Test Fixer was a **subagent** rather than a handoff.
2. Why final review was a **handoff**.
3. Which parts were LLM-driven vs deterministically enforced by the Stop hook.
4. Why multiple handoffs are still predefined transitions, while dynamic specialist choice happens inside the parent-agent reasoning loop.
