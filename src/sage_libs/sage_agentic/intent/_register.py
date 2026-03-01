"""Register sage-libs-intent implementations with sage.libs.agentic factory.

Adapters bridge between:
- sage.libs.agentic.interface.base.IntentRecognizer  (sync recognize())
- sage.libs.agentic.interface.base.IntentClassifier  (sync classify())

and the local async implementations.
"""

from __future__ import annotations

import asyncio
import concurrent.futures
import logging
from typing import Any

from sage.libs.agentic.interface.base import Intent
from sage.libs.agentic.interface.base import IntentClassifier as SageIntentClassifier
from sage.libs.agentic.interface.base import IntentRecognizer as SageIntentRecognizer
from sage.libs.agentic.interface.factory import (
    list_intent_classifiers,
    list_intent_recognizers,
    register_intent_classifier,
    register_intent_recognizer,
)

from sage_libs.sage_agentic.intent.base import IntentRecognitionContext
from sage_libs.sage_agentic.intent.classifier import IntentClassifier
from sage_libs.sage_agentic.intent.keyword_recognizer import KeywordIntentRecognizer
from sage_libs.sage_agentic.intent.llm_recognizer import LLMIntentRecognizer
from sage_libs.sage_agentic.intent.types import IntentResult

logger = logging.getLogger(__name__)


# ==================== Async → Sync bridge ====================


def _run_async(coro: Any) -> Any:
    """Run a coroutine synchronously, even inside a running event loop."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        # No event loop running — safe to call asyncio.run directly.
        return asyncio.run(coro)
    else:
        # Event loop already running (e.g. in a Jupyter environment).
        # Delegate to a thread that creates its own event loop.
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(asyncio.run, coro)
            return future.result()


# ==================== IntentResult → sage.libs Intent ====================


def _to_sage_intent(result: IntentResult) -> Intent:
    metadata: dict[str, Any] = {
        "matched_keywords": result.matched_keywords,
        "trace": result.trace,
    }
    if result.knowledge_domains:
        metadata["knowledge_domains"] = [d.value for d in result.knowledge_domains]
    return Intent(
        name=result.intent.value,
        confidence=result.confidence,
        slots={},
        metadata=metadata,
    )


# ==================== Adapters ====================


class KeywordIntentRecognizerAdapter(SageIntentRecognizer):
    """Wraps KeywordIntentRecognizer for sage.libs registry."""

    def __init__(self) -> None:
        self._recognizer = KeywordIntentRecognizer()

    def recognize(self, text: str, context: dict[str, Any] | None = None) -> Intent:
        ctx = IntentRecognitionContext(message=text, extra=context)
        result: IntentResult = _run_async(self._recognizer.classify(ctx))
        return _to_sage_intent(result)


class LLMIntentRecognizerAdapter(SageIntentRecognizer):
    """Wraps LLMIntentRecognizer for sage.libs registry."""

    def __init__(self, control_plane_url: str | None = None) -> None:
        self._recognizer = LLMIntentRecognizer(control_plane_url=control_plane_url)

    def recognize(self, text: str, context: dict[str, Any] | None = None) -> Intent:
        ctx = IntentRecognitionContext(message=text, extra=context)
        result: IntentResult = _run_async(self._recognizer.classify(ctx))
        return _to_sage_intent(result)


class IntentClassifierAdapter(SageIntentClassifier):
    """Wraps local IntentClassifier for sage.libs registry."""

    def __init__(self, mode: str = "keyword") -> None:
        self._classifier = IntentClassifier(mode=mode)

    def classify(self, text: str) -> list[Intent]:
        result: IntentResult = _run_async(self._classifier.classify(message=text))
        return [_to_sage_intent(result)]


# ==================== Register with sage.libs factory ====================

def _register_if_absent(name: str, cls: Any, registry_fn: Any, list_fn: Any) -> None:
    if name not in list_fn():
        registry_fn(name, cls)
    else:
        logger.debug("sage-libs-intent: '%s' already registered, skipping.", name)


_register_if_absent("keyword", KeywordIntentRecognizerAdapter, register_intent_recognizer, list_intent_recognizers)
_register_if_absent("llm", LLMIntentRecognizerAdapter, register_intent_recognizer, list_intent_recognizers)
_register_if_absent("keyword_classifier", IntentClassifierAdapter, register_intent_classifier, list_intent_classifiers)

logger.debug(
    "sage-libs-intent: registered intent recognizers %s",
    list_intent_recognizers(),
)
