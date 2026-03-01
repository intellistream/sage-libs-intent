"""Factory helpers to build intent recognizers."""

from __future__ import annotations

from sage_libs.sage_agentic.intent.base import ChainedIntentRecognizer, IntentRecognizer
from sage_libs.sage_agentic.intent.keyword_recognizer import KeywordIntentRecognizer
from sage_libs.sage_agentic.intent.llm_recognizer import LLMIntentRecognizer


def _build_selector_recognizer() -> IntentRecognizer:
    from sage_libs.sage_agentic.intent.selector_recognizer import SelectorIntentRecognizer

    return SelectorIntentRecognizer()

RECOGNIZER_BUILDERS = {
    "llm": LLMIntentRecognizer,
    "keyword": KeywordIntentRecognizer,
    "selector": _build_selector_recognizer,
}


def build_recognizer_chain(
    primary_mode: str = "keyword",
    secondary_mode: str | None = None,
    min_confidence: float = 0.0,
) -> ChainedIntentRecognizer:
    modes = [primary_mode]
    if secondary_mode is not None:
        modes.append(secondary_mode)

    recognizers: list[IntentRecognizer] = []
    for mode in modes:
        builder = RECOGNIZER_BUILDERS.get(mode)
        if builder is None:
            raise ValueError(f"Unsupported recognizer mode: {mode}")
        recognizers.append(builder())

    if not recognizers:
        raise RuntimeError("No intent recognizer configured")

    return ChainedIntentRecognizer(recognizers=recognizers, min_confidence=min_confidence)
