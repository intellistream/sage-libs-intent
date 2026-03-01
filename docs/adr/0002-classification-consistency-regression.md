# ADR 0002: Keep intent classification enrichment consistent across recognizers

## Status

Accepted

## Date

2026-03-01

## Issue

`intellistream/sage-libs-intent#4`

## Context

After boundary cleanup in #2/#3, recognizer modes stayed explicit (`keyword`, `llm`, `selector`).
A behavior gap remained in classification enrichment:

- `keyword` and `selector` modes derive `knowledge_domains` for `knowledge_query` from the catalog (`INTENT_TOOLS`).
- `llm` mode used a hard-coded subset (`sage_docs`, `examples`).

This caused inconsistent outputs for the same intent across modes.

## Decision

1. Remove hard-coded LLM knowledge domains for `knowledge_query`.
2. Use the same catalog-based mapping (`get_intent_tool`) used by other recognizers.
3. Add regression tests that lock consistency between `keyword` and `llm` modes.

## Consequences

- `IntentResult` enrichment is now deterministic across recognizer implementations.
- Catalog is the single source of truth for intent-domain mapping.
- No fallback/shim behavior is introduced.

## Verification

- `ruff check src/sage_libs/sage_agentic/intent/llm_recognizer.py tests/test_issue4_classification_consistency.py`
- `PYTHONPATH=src pytest -q tests/test_issue4_classification_consistency.py`
