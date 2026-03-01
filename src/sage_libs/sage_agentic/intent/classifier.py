"""Default IntentClassifier for L3 reuse."""

from __future__ import annotations

from sage_libs.sage_agentic.intent.base import IntentRecognitionContext
from sage_libs.sage_agentic.intent.factory import build_recognizer_chain
from sage_libs.sage_agentic.intent.types import IntentResult


class IntentClassifier:
    """Default classifier backed by a recognizer chain."""

    def __init__(
        self,
        mode: str = "keyword",
        embedding_model: str | None = None,
        secondary_mode: str | None = None,
    ) -> None:
        self.mode = mode
        self.embedding_model = embedding_model
        self._recognizer = build_recognizer_chain(
            primary_mode=mode,
            secondary_mode=secondary_mode,
            min_confidence=0.0,
        )
        self._initialized = True

    async def classify(
        self,
        message: str,
        history: list[dict[str, str]] | None = None,
        context: str | None = None,
    ) -> IntentResult:
        ctx = IntentRecognitionContext(message=message, history=history, extra={"context": context})
        return await self._recognizer.classify(ctx)

    @property
    def is_initialized(self) -> bool:
        return self._initialized


__all__ = [
    "IntentClassifier",
]
