# sage-libs-intent Copilot Instructions

## Scope
- Package: `isage-libs-intent`, import path `sage_libs.sage_agentic.intent`.
- Layer: **L3** — intent recognition algorithms for agentic tool-use; no L4+ dependencies.
- Purpose: Intent classification and recognition for routing agent requests to appropriate tools.

## Polyrepo Context (Important)
SAGE was restructured from a monorepo into a polyrepo. This is a **specialized L3 algorithm repo** providing intent recognition capabilities that feed into the tool-use selection pipeline. It integrates with `sage-agentic-tooluse` and the `sage-libs` interface layer.

## Critical rules
- Keep runtime/service-neutral; no L4+ dependencies.
- Do not create new local virtual environments (`venv`/`.venv`); use the existing configured Python environment.
- No fallback logic; fail fast.

## Architecture focus
- `src/sage_libs/sage_agentic/intent/` — main implementation directory.
  - `base.py` — base intent recognizer interface.
  - `factory.py` — intent recognizer factory/registry.
  - `llm_recognizer.py` — LLM-based intent recognition.
  - `classifier.py` — classifier-based intent recognition.

## Dependencies
- **Depends on**: `isage-common` (L1), `isage-libs` (L3 interfaces), `isage-agentic` (L3 base).
- **Depended on by**: `sage-agentic-tooluse`, application repos requiring intent routing.

## Workflow
1. Make minimal changes under `src/sage_libs/sage_agentic/intent/`.
2. Keep public imports stable in `__init__.py`.
3. Run `pytest tests/ -v` and update docs for behavior changes.

## Git Hooks (Mandatory)
- Never use `git commit --no-verify` or `git push --no-verify`.
- If hooks fail, fix the issue first.

## 🚫 NEVER_CREATE_DOT_VENV_MANDATORY

- 永远不要创建 `.venv` 或 `venv`（无任何例外）。
- NEVER create `.venv`/`venv` in this repository under any circumstance.
- 必须复用当前已配置的非-venv Python 环境（如现有 conda 环境）。
- If any script/task suggests creating a virtualenv, skip that step and continue with the existing environment.
