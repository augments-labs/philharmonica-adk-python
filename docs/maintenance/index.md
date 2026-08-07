# Maintenance

What to update in `docs/` when you ship code. The pages here are plain
Markdown with no build step — edit them and the change is done.

## Did you add a new public API symbol?

Add or extend the matching guide under `docs/guides/<topic>.md`. Keep
prose short; show one minimal example. Add the symbol to the matching
page under `docs/references/api/` so the public surface stays complete.

## Did you change a major architectural decision?

Update or extend the relevant page under `docs/architecture/` to
reflect the new design. If the change is wide-reaching, update
`docs/architecture/overview.md` as well.

## Did you change persisted-format / tolerance behaviour?

Add an entry under `CHANGELOG.md` `[Unreleased]` → `Changed` (or
`Fixed` if it's a bug fix that user code may need to be aware of).

## Did you add a new module under `src/philharmonica/adk/`?

Add a `docs/guides/<module>.md` (or expand a relevant
`docs/architecture/<page>.md`).

## Did you touch a public class signature?

The docstring is the reference — make sure it is current, and check
that the symbol is still listed on its `docs/references/api/` page.

## Did you change `pyproject.toml` deps?

Update the install instructions in `CONTRIBUTING.md` if a contributor
will need to re-install.

## Before claiming docs are done

Check that every code sample you touched still runs against the
current API, and that relative links resolve. The hygiene gate
(`ruff` / `mypy` / `pyright` / IDE diagnostics) will not have anything
to say about pure doc changes, but run it anyway for habit.
