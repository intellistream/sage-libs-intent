# ADR 0001: intent boundary and explicit selector mode

- Status: Accepted
- Date: 2026-03-01
- Issue: #2

## Context

`intent` subpackage had compatibility-style behavior:

- conditional imports around recognizers
- fallback-oriented recognizer construction
- selector path mixed into keyword recognizer internals

This made boundary ownership ambiguous and allowed silent behavior changes.

## Decision

1. Remove compatibility/fallback paths from intent recognizer construction.
2. Keep recognizer modes explicit: `keyword`, `llm`, `selector`.
3. Implement `selector` as a dedicated recognizer (`SelectorIntentRecognizer`).
4. `selector` mode is fail-fast: missing tool-selection dependency raises immediately.
5. Keep `keyword` recognizer focused on keyword/heuristic logic only.

## Consequences

- Construction behavior is deterministic and auditable.
- No silent downgrade when a mode is unavailable.
- If `selector` dependency is absent, callers must either install dependency or use another explicit mode.
- Boundary between intent logic and tool-selection integration is clear.
