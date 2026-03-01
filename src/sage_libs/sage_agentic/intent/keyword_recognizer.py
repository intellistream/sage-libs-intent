"""Keyword-based intent recognizer."""

from __future__ import annotations

from collections.abc import Iterable

from sage_libs.sage_agentic.intent.base import IntentRecognitionContext, IntentRecognizer
from sage_libs.sage_agentic.intent.catalog import INTENT_TOOLS, get_intent_tool
from sage_libs.sage_agentic.intent.types import IntentResult, KnowledgeDomain, UserIntent


class KeywordIntentRecognizer(IntentRecognizer):
    @staticmethod
    def _build_result(intent: UserIntent, confidence: float, matched_keywords: Iterable[str] = ()):  # type: ignore[type-arg]
        """Construct an IntentResult with knowledge domain enrichment when applicable."""
        knowledge_domains = None
        if intent == UserIntent.KNOWLEDGE_QUERY:
            tool = get_intent_tool(intent)
            if tool and tool.knowledge_domains:
                knowledge_domains = [KnowledgeDomain(d) for d in tool.knowledge_domains]

        return IntentResult(
            intent=intent,
            confidence=confidence,
            knowledge_domains=knowledge_domains,
            matched_keywords=list(matched_keywords),
        )

    async def classify(self, ctx: IntentRecognitionContext) -> IntentResult:
        # Heuristic boost: installation/docs/tutorial queries should map to knowledge query.
        message_lower = ctx.message.lower()
        knowledge_triggers = (
            "安装",
            "install",
            "文档",
            "docs",
            "documentation",
            "教程",
            "guide",
            "使用",
            "setup",
            "配置",
            "config",
        )
        matched_triggers = [kw for kw in knowledge_triggers if kw in message_lower]
        # If the query mentions SAGE plus any install/docs trigger, force knowledge query.
        mentions_sage = "sage" in message_lower
        if (
            matched_triggers
            or mentions_sage
            and any(kw in ctx.message for kw in knowledge_triggers)
        ):
            trigger_list = matched_triggers or [
                kw for kw in knowledge_triggers if kw in ctx.message
            ]
            return self._build_result(UserIntent.KNOWLEDGE_QUERY, 0.9, trigger_list)

        return self._classify_simple(ctx.message)

    def _classify_simple(self, message: str) -> IntentResult:
        message_lower = message.lower()
        best_intent = UserIntent.GENERAL_CHAT
        best_score = 0.0
        matched_keywords: list[str] = []

        for tool in INTENT_TOOLS:
            score = 0.0
            matches = []
            for keyword in tool.keywords:
                if keyword.lower() in message_lower:
                    score += 1.0
                    matches.append(keyword)
            normalized_score = min(score * 0.5, 1.0) if tool.keywords else 0.0
            if normalized_score > best_score:
                best_score = normalized_score
                try:
                    best_intent = UserIntent(tool.tool_id)
                except ValueError:
                    continue
                matched_keywords = matches

        return self._build_result(
            intent=best_intent,
            confidence=best_score if best_score > 0 else 0.3,
            matched_keywords=matched_keywords,
        )
