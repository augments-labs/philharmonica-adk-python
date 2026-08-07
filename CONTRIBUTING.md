# Contributing

<!--include-from-here-->

Welcome! This guide covers everything an outside contributor needs
to land a change.

## Quick start

```bash
# Clone
git clone https://github.com/augments-labs/philharmonica-adk-python.git
cd philharmonica-adk-python

# Build .venv from the committed lockfile
uv sync --extra dev

# Verify
uv run python -c "from philharmonica.adk import Agent, Runner; print('OK')"
```

The `dev` extra brings the full set of tools — tests, lint, typecheck.
`uv sync` resolves from `uv.lock`, so your environment matches CI exactly;
`uv run <cmd>` runs anything inside it without activating a shell.
`make sync` is the same thing if you prefer the Makefile.

Conda works too, if you prefer it:

```bash
conda env create -f environment.yaml   # also runs pip install -e '.[dev]'
conda activate philharmonica-adk-python
```

Every command below is written with the `uv run` prefix; drop it when you
have an environment activated. The `make` targets take `RUN=` for the same
reason (`make typecheck-fast RUN=`).

## How we work — spec → plan → execute → review

Every non-trivial change goes through four phases:

1. **Spec** — write down what you're building and why. One-page is
   often enough. Discuss before coding if the shape is unclear.
2. **Plan** — turn the spec into a concrete, bite-sized task list with
   exact file paths. The plan should be executable by someone unfamiliar
   with the code.
3. **Execute** — follow the plan task by task. Commit at logical
   checkpoints.
4. **Review** — the maintainer runs the project's multi-agent review
   pass before merging.

Bug fixes can skip steps 1 and 2 if the fix is small and the test
makes the change self-evident.

## The five-check hygiene gate

Before declaring any change "done" — and before every commit — run
all five checks:

```bash
uv run ruff check src tests examples
uv run ruff format --check src tests examples
uv run mypy src
uv run pyright src
# + your IDE's diagnostics (no red squigglies anywhere you touched)
```

**All five must be clean.** Fix at source — don't suppress. The only
acceptable suppressions are `# type: ignore[<rule>]` lines for
verified provider-SDK or third-party false positives, with a
one-line justification comment.

## Conventions

- **No version language in shipped code.** No `v1`/`v2`/`Phase N`/
  `*_SCHEMA_VERSION` markers in `src/`, `tests/`, `docs/`, `examples/`,
  or `README.md`. Persisted formats evolve via tolerant loaders; hard
  breaks rename the loader. `CHANGELOG.md` and `pyproject.toml` are
  sanctioned exceptions.
- **No implicit framework-added tokens.** Every token the framework
  adds to a prompt is opt-in. Cost-conservative defaults
  (off / smallest / bounded) everywhere.
- **Named parameters.** Prefer explicit named parameters over `**kwargs`
  for core APIs. Avoid `_NON_LITELLM_FIELDS`-style hidden allow-lists.
- **Three-layer types.** Layer 1 (`LLMInputContentItem`) and Layer 3
  (`RunItem`) are developer-facing. Layer 2 wire `TypedDict`s live
  inside `src/philharmonica/adk/llms/<provider>/` and never escape.
- **No `print()`** — always `logging`. The codebase uses
  `logger = logging.getLogger(__name__)` per module.
- **No `if x:` truthiness** on non-booleans. Use explicit `len(x) > 0`
  or `x is None`.

## Tests + coverage

Run the test suite:

```bash
uv run pytest
```

Run with coverage:

```bash
uv run pytest --cov=src/philharmonica --cov-report=html --cov-report=term-missing
```

The HTML report lands at `.coverage/html/index.html`.

**Coverage today:** 83% line, 86% branch.

**Goal:** 95% line + branch coverage. The goal is documented to focus
where new tests are most useful; it is not a hard gate (no CI
enforcement today). New code should aim for high coverage from the
start; raising the project baseline is gradual.

## Documentation

Documentation is plain Markdown under [`docs/`](https://github.com/augments-labs/philharmonica-adk-python/tree/main/docs).
There is no build step and no generated site in this repository — the
pages are the source, and [augmentslabs.com](https://augmentslabs.com)
renders them.

When you ship code, update the page that covers the surface you changed
and keep the code samples runnable against the current API.

## Commits + PRs

- `git add` and `git commit` are pre-approved — commit at logical
  checkpoints. **Do not** use `--no-verify`.
- `git push` is the maintainer's call — open a PR description that
  includes a one-paragraph summary and a bulleted test plan.
- Conventional Commits are encouraged but not required.
- Sign your commits if your workflow supports it (`git commit -S`).

## Licensing & contributions

Philharmonica ADK is open source under the [MIT License](https://github.com/augments-labs/philharmonica-adk-python/blob/main/LICENSE).

By contributing, you agree that your contributions are licensed under the
same MIT License that covers the project (inbound = outbound). You keep the
copyright in what you write. No Contributor License Agreement is required —
opening a pull request is enough.

## Reporting issues

For bug reports:

1. Minimal reproducer (a small script that reproduces the bug).
2. Environment info (Python version, `pip freeze | head -20`).
3. Expected vs. actual behaviour.
4. Stack trace if one was emitted.

For feature requests: describe the use case and the smallest change
that would unblock you. Pointing at a similar feature in another
agent framework is fine; the request should still articulate the
need in this codebase's terms.

## Acknowledgements

See the [Acknowledgements section](https://github.com/augments-labs/philharmonica-adk-python/blob/main/README.md#acknowledgements) in the
README for prior art and ongoing influences.
