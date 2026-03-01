"""Selector-based intent recognizer."""

from __future__ import annotations

from sage_libs.sage_agentic.intent.base import IntentRecognitionContext, IntentRecognizer
from sage_libs.sage_agentic.intent.catalog import INTENT_TOOLS, IntentToolsLoader, get_intent_tool
from sage_libs.sage_agentic.intent.types import IntentResult, KnowledgeDomain, UserIntent


class SelectorIntentRecognizer(IntentRecognizer):
    """Intent recognizer powered by KeywordSelector from sage-agentic."""

    def __init__(self) -> None:
        try:
            from sage_libs.sage_agentic.agents.action.tool_selection import (
                KeywordSelector,
                SelectorResources,
            )
            from sage_libs.sage_agentic.agents.action.tool_selection.schemas import (
                KeywordSelectorConfig,
            )
        except ImportError as exc:
            raise ModuleNotFoundError(
                "selector mode requires isage-agentic tool_selection modules"
            ) from exc

        resources = SelectorResources(tools_loader=IntentToolsLoader(INTENT_TOOLS), embedding_client=None)
        config = KeywordSelectorConfig(
            name="intent_selector",
            top_k=1,
            min_score=0.0,
            method="tfidf",
            lowercase=True,
            remove_stopwords=False,
            ngram_range=(1, 2),
        )
        self._selector = KeywordSelector.from_config(config, resources)

    @staticmethod
    def _build_result(intent: UserIntent, confidence: float, matched_keywords: list[str]) -> IntentResult:
        knowledge_domains = None
        if intent == UserIntent.KNOWLEDGE_QUERY:
            tool = get_intent_tool(intent)
            if tool and tool.knowledge_domains:
                knowledge_domains = [KnowledgeDomain(domain) for domain in tool.knowledge_domains]

        return IntentResult(
            intent=intent,
            confidence=confidence,
            knowledge_domains=knowledge_domains,
            matched_keywords=matched_keywords,
        )

    async def classify(self, ctx: IntentRecognitionContext) -> IntentResult:
        from sage_libs.sage_agentic.agents.action.tool_selection.schemas import ToolSelectionQuery

        query = ToolSelectionQuery(
            sample_id="intent_selector",
            instruction=ctx.message,
            context={"history": ctx.history} if ctx.history else {},
            candidate_tools=[tool.tool_id for tool in INTENT_TOOLS],
        )
        predictions = self._selector.select(query, top_k=1)
        if not predictions:
            return IntentResult(intent=UserIntent.GENERAL_CHAT, confidence=0.3)

        top_prediction = predictions[0]
        try:
            intent = UserIntent(top_prediction.tool_id)
        except ValueError:
            return IntentResult(intent=UserIntent.GENERAL_CHAT, confidence=0.3)

        metadata = top_prediction.metadata or {}
        matched_keywords = metadata.get("matched_keywords")
        if not isinstance(matched_keywords, list):
            matched_keywords = []

        result = self._build_result(intent, top_prediction.score, matched_keywords)
        result.raw_prediction = top_prediction
        return result
