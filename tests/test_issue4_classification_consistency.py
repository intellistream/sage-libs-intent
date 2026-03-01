from __future__ import annotations

from types import SimpleNamespace

import pytest

from sage_libs.sage_agentic.intent.base import IntentRecognitionContext
from sage_libs.sage_agentic.intent.catalog import get_intent_tool
from sage_libs.sage_agentic.intent.keyword_recognizer import KeywordIntentRecognizer
from sage_libs.sage_agentic.intent.llm_recognizer import LLMIntentRecognizer
from sage_libs.sage_agentic.intent.types import KnowledgeDomain, UserIntent


class _FakeCompletions:
    def __init__(self, content: str) -> None:
        self._content = content

    def create(self, **kwargs):
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=self._content))]
        )


@pytest.mark.asyncio
async def test_llm_knowledge_query_domains_match_catalog() -> None:
    recognizer = LLMIntentRecognizer(control_plane_url="http://localhost:8080/v1")
    recognizer._client = SimpleNamespace(  # noqa: SLF001
        chat=SimpleNamespace(completions=_FakeCompletions("knowledge_query"))
    )

    result = await recognizer.classify(
        IntentRecognitionContext(message="SAGE 安装文档在哪里")
    )

    assert result.intent == UserIntent.KNOWLEDGE_QUERY
    tool = get_intent_tool(UserIntent.KNOWLEDGE_QUERY)
    assert tool is not None
    expected_domains = [KnowledgeDomain(domain) for domain in tool.knowledge_domains]
    assert result.knowledge_domains == expected_domains


@pytest.mark.asyncio
async def test_keyword_and_llm_knowledge_domains_are_consistent() -> None:
    keyword_result = await KeywordIntentRecognizer().classify(
        IntentRecognitionContext(message="请给我 SAGE 安装教程")
    )

    llm = LLMIntentRecognizer(control_plane_url="http://localhost:8080/v1")
    llm._client = SimpleNamespace(  # noqa: SLF001
        chat=SimpleNamespace(completions=_FakeCompletions("knowledge_query"))
    )
    llm_result = await llm.classify(
        IntentRecognitionContext(message="请给我 SAGE 安装教程")
    )

    assert keyword_result.intent == UserIntent.KNOWLEDGE_QUERY
    assert llm_result.intent == UserIntent.KNOWLEDGE_QUERY
    assert keyword_result.knowledge_domains == llm_result.knowledge_domains


@pytest.mark.asyncio
async def test_llm_unknown_output_falls_back_to_general_chat() -> None:
    recognizer = LLMIntentRecognizer(control_plane_url="http://localhost:8080/v1")
    recognizer._client = SimpleNamespace(  # noqa: SLF001
        chat=SimpleNamespace(completions=_FakeCompletions("something_else"))
    )

    result = await recognizer.classify(
        IntentRecognitionContext(message="随便聊聊")
    )

    assert result.intent == UserIntent.GENERAL_CHAT
    assert result.confidence == 0.3
