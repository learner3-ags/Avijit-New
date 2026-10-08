# Copilot instructions — MP1 multi-agent maintenance guard

- Treat `work-items/MP1.md` as the source of truth.
- Inspect before editing; keep changes minimal and scoped.
- The **Implementation** agent is the parent implementation role. It may dynamically delegate focused analysis to the eligible specialists based on runtime evidence.
- Use **Test Fixer** for failing pytest/Playwright evidence, **API Specialist** for API/status/contract changes, and **Security Reviewer** for privileged/security-sensitive concerns.
- Subagents return findings to the parent; they do not replace the parent implementation stage.
- Final stage transitions use configured handoffs: Standard Code Review, Security Review, or Re-plan Change.
- Never weaken or delete a valid test merely to obtain green.
- The Implementation agent's Stop hook is the completion gate; do not try to bypass it.
- Stop before merge/deployment; a human reviews the diff and evidence.
