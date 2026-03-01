# sage-libs-intent

L3 intent recognition package for SAGE agentic workflows.

- PyPI: `isage-libs-intent`
- Import path: `sage_libs.sage_agentic.intent`

## Scope

This package only provides intent recognition logic and data structures.

- `KeywordIntentRecognizer`: keyword and heuristic intent classification
- `LLMIntentRecognizer`: LLM-based intent classification
- `selector` mode: explicit integration with `isage-agentic` KeywordSelector
- `IntentClassifier`: chain wrapper over recognizers
- Intent catalog and typed intent/domain results

## Boundary

- Intent package does not depend on tool-selection internals.
- Recognizer build path is explicit and deterministic.
- Package exports are explicit and fail-fast.

## Recognizer Modes

- `keyword`: built-in keyword and heuristic recognizer
- `llm`: LLM recognizer via OpenAI-compatible gateway
- `selector`: explicit bridge to `isage-agentic` `KeywordSelector`

`selector` mode has no fallback behavior. If `isage-agentic` tool-selection modules are not available,
construction fails immediately with `ModuleNotFoundError`.

## Installation

```bash
pip install isage-libs-intent
```

## Quick Start

```python
import asyncio

from sage_libs.sage_agentic.intent import IntentClassifier


async def main() -> None:
    classifier = IntentClassifier(mode="keyword")
    result = await classifier.classify("请帮我找一下 SAGE 的安装文档")
    print(result.intent.value, result.confidence)


asyncio.run(main())
```

## LLM Recognizer Example

```python
import asyncio

from sage_libs.sage_agentic.intent import LLMIntentRecognizer, IntentRecognitionContext


async def main() -> None:
    recognizer = LLMIntentRecognizer(control_plane_url="http://localhost:8080/v1")
    result = await recognizer.classify(IntentRecognitionContext(message="Explain SAGE pipeline API"))
    print(result.intent.value, result.confidence)


asyncio.run(main())
```

## License

MIT
