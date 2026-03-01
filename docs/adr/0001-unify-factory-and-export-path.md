# ADR 0001: Unify factory and export path

## Status

Accepted

## Context

Issue `intellistream/sage-libs-intent#3` requires removing duplicate classifier entrypoints and legacy alias metadata.

Problems identified:

- `classifier.py` re-exported many symbols that were already exported by package root, creating duplicate public entrypoints;
- `pyproject.toml` still pointed to legacy `sage-intent` repository URLs.

## Decision

1. Keep package root `sage_libs.sage_agentic.intent` as the only aggregate export path.
2. Restrict `classifier.py` public surface to `IntentClassifier` only.
3. Keep factory fail-fast semantics for unsupported modes (no fallback/shim).
4. Update project URLs to `sage-libs-intent` canonical repository.

## Consequences

- Public API surface is explicit and non-duplicated.
- Alias-style metadata and duplicate entrypoints are removed.
- Callers get deterministic failures for unsupported recognizer modes.

## Verification

- `ruff check src/sage_libs/sage_agentic/intent/classifier.py tests/test_issue3_unify_exports.py`
- `PYTHONPATH=src pytest -q tests/test_issue3_unify_exports.py`
