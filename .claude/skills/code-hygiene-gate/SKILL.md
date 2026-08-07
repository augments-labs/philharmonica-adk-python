---
name: code-hygiene-gate
description: Run the project code-hygiene gate (ruff, ruff format, mypy, pyright, IDE diagnostics) and report pass/fail. Use before claiming work done, before requesting commit authorization, or when the user says /code-hygiene-gate.
allowed-tools: Bash(uv run *) Bash(ruff *) Bash(mypy *) Bash(pyright *) Bash(git diff *) Bash(git merge-base *)
---

# Code-Hygiene Gate

Run all five checks. ALL must be clean before work is "done".

`uv run` guarantees the locked toolchain (drop the prefix only when an
environment is already activated).

1. `uv run ruff check src/ tests/`
2. `uv run ruff format --check src/ tests/ examples/`
3. `uv run mypy -p philharmonica.adk`  (canonical)
4. Pyright **scoped to the branch's changed Python files** — seconds, NOT the
   whole package inline:

   ```
   FILES=$(git diff --name-only "$(git merge-base origin/main HEAD)" -- '*.py')
   [ -n "$FILES" ] && uv run pyright $FILES || echo "no .py changes — pyright skipped"
   ```

   (The diff against the merge-base includes uncommitted edits.) Cross-file
   regressions are still caught by full-package mypy in step 3. The full
   `pyright src/philharmonica/adk/` sweep is the NIGHTLY CI job — never run it
   inline; it can take hours.
5. IDE diagnostics via `mcp__ide__getDiagnostics`

Rules:

- Parse exit codes AND output — exit 0 alone is not "passed".
- mypy (full package) AND pyright (changed files) must BOTH be clean; they
  catch different bugs. mypy is the full cross-file/caller pass; scoped pyright
  is the fast second opinion on what you touched.
- Pre-existing errors in modified files (or files they import/call into)
  MUST be fixed regardless of pedigree — never report "pre-existing, not
  mine" and move on. Caller files outside the pyright scope surface via the
  full mypy pass (step 3).
- **Fix at source.** `isinstance` over `# type: ignore`; concrete types
  over `list[Any]`; explicit `bool` branches for `Literal[T/F]` overloads.
  A surviving suppression marker must be narrow + carry a one-line
  rationale naming the invariant the checker cannot see.

Report a per-check PASS/FAIL table and, on any FAIL, the exact errors
with file:line and the fix applied. Do not declare the gate green until
every check is clean.
