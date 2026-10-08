const { execSync } = require('node:child_process');

let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
  const event = JSON.parse(input || '{}');

  function run(command) {
    try {
      const output = execSync(command, {
        encoding: 'utf8',
        stdio: ['ignore', 'pipe', 'pipe'],
        env: process.env
      });
      return { ok: true, output };
    } catch (error) {
      return {
        ok: false,
        output: (error.stdout && error.stdout.toString()) ||
                (error.stderr && error.stderr.toString()) ||
                error.message
      };
    }
  }

  const py = run('python -m pytest -q');
  const ui = py.ok ? run('npm run test:ui') : { ok: false, output: 'Skipped because pytest failed.' };

  if (py.ok && ui.ok) {
    process.stdout.write(JSON.stringify({
      systemMessage: 'Implementation completion gate passed: pytest and Playwright are green.'
    }));
    return;
  }

  // A Stop hook can force another model turn. Prevent an unbounded loop.
  if (event.stop_hook_active) {
    process.stdout.write(JSON.stringify({
      continue: false,
      stopReason: 'Verification is still failing after the automatic continuation. Escalate to the human reviewer.'
    }));
    return;
  }

  const evidence = [
    py.ok ? 'pytest: PASS' : `pytest: FAIL\n${py.output}`,
    ui.ok ? 'Playwright: PASS' : `Playwright: FAIL/SKIPPED\n${ui.output}`
  ].join('\n\n');

  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: 'Stop',
      decision: 'block',
      reason: `You may not finish the Implementation agent yet. Verification is not green.\n\n${evidence}\n\nDiagnose the failure. Invoke Test Fixer if appropriate, correct the issue, and rerun verification.`
    }
  }));
});
