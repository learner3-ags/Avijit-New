# MP1 — Maintenance-mode guard for disruptive reset actions

Add a maintenance-mode control to API and UI.

## Acceptance criteria

1. `ForceOff` and `GracefulRestart` return HTTP 409 unless maintenance mode is enabled.
2. `On` remains allowed.
3. Add an API operation to enable/disable maintenance mode.
4. The UI lets an operator enable/disable maintenance mode and clearly shows rejection of disruptive reset actions when maintenance is off.
5. Generate/update Python API tests and Playwright UI tests.
6. Existing baseline behavior remains green where not intentionally changed.
7. Do not merge automatically.

## Agent-workflow requirement

During implementation, demonstrate runtime specialist delegation:
- failing verification → **Test Fixer**
- API/status/contract question → **API Specialist**
- security/privileged-operation concern → **Security Reviewer**

After verification, choose one of the configured final handoffs: Standard Code Review, Security Review, or Re-plan Change.
