"""LLM-based intent recognizer."""

from __future__ import annotations

import asyncio
import logging

import openai
from sage.common.config.ports import SagePorts

from sage_libs.sage_agentic.intent.base import IntentRecognitionContext, IntentRecognizer
from sage_libs.sage_agentic.intent.catalog import get_intent_tool
from sage_libs.sage_agentic.intent.types import IntentResult, KnowledgeDomain, UserIntent

logger = logging.getLogger(__name__)


class LLMIntentRecognizer(IntentRecognizer):
    def __init__(self, control_plane_url: str | None = None) -> None:
        self._client = None
        self._control_plane_url = (
            control_plane_url or f"http://localhost:{SagePorts.GATEWAY_DEFAULT}/v1"
        )
        self._initialize_client()

    def _initialize_client(self) -> None:
        self._client = openai.OpenAI(
            base_url=self._control_plane_url,
            api_key="dummy",  # Gateway doesn't require real API key
            timeout=30.0,  # 30 second timeout to prevent hanging
            max_retries=0,  # Disable retries for faster failure
        )
        logger.info("LLM Intent client initialized with Gateway: %s", self._control_plane_url)

    async def classify(self, ctx: IntentRecognitionContext) -> IntentResult:
        prompt = (
            "You are an intent classifier for the SAGE AI framework.\n"
            "Classify the user's message into one of the following intents.\n\n"
            "Available intents:\n"
            "- knowledge_query: Questions requiring knowledge base search (SAGE docs, research papers, examples)\n"
            "- sage_coding: SAGE framework programming tasks (pipeline generation, debugging, API usage)\n"
            "- system_operation: System management (start/stop services, check status)\n"
            "- general_chat: General conversation or unrelated topics\n\n"
            f"User message: \"{ctx.message}\"\n\n"
            "Return ONLY the intent name in lowercase (e.g., knowledge_query). Do not return numbers or explanations."
        )

        loop = asyncio.get_running_loop()

        def _call_llm():
            response = self._client.chat.completions.create(
                model="",  # Gateway routes automatically
                messages=[{"role": "user", "content": prompt}],
                max_tokens=50,
                temperature=0.01,  # Min positive value (Gateway requires > 0)
            )
            return response.choices[0].message.content

        response = await loop.run_in_executor(None, _call_llm)

        content = response.strip().lower()
        normalized = content.replace(" ", "_")

        # **Diagnostic logging**
        logger.info(f"[LLM Intent] Raw LLM output: '{response}'")
        logger.info(f"[LLM Intent] Normalized: '{normalized}'")

        for intent in UserIntent:
            if intent.value in content or intent.value in normalized:
                knowledge_domains = None
                if intent == UserIntent.KNOWLEDGE_QUERY:
                    tool = get_intent_tool(intent)
                    if tool and tool.knowledge_domains:
                        knowledge_domains = [KnowledgeDomain(domain) for domain in tool.knowledge_domains]
                return IntentResult(
                    intent=intent,
                    confidence=0.9,
                    knowledge_domains=knowledge_domains,
                    matched_keywords=[],
                )

        logger.warning("LLM output '%s' did not match known intents", content)
        return IntentResult(intent=UserIntent.GENERAL_CHAT, confidence=0.3)
