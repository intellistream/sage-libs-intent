"""Intent recognition primitives (L3: sage-libs)."""

from sage_libs.sage_agentic.intent.base import (
    ChainedIntentRecognizer,
    IntentRecognitionContext,
    IntentRecognizer,
)
from sage_libs.sage_agentic.intent.catalog import (
    INTENT_TOOLS,
    IntentTool,
    IntentToolsLoader,
    get_all_intent_keywords,
    get_intent_tool,
)

# Direct exports (no lazy loading for core components)
from sage_libs.sage_agentic.intent.classifier import IntentClassifier
from sage_libs.sage_agentic.intent.factory import build_recognizer_chain
from sage_libs.sage_agentic.intent.keyword_recognizer import KeywordIntentRecognizer
from sage_libs.sage_agentic.intent.types import (
    DOMAIN_DISPLAY_NAMES,
    INTENT_DISPLAY_NAMES,
    IntentResult,
    KnowledgeDomain,
    UserIntent,
    get_domain_display_name,
    get_intent_display_name,
)

# Conditional import for LLMIntentRecognizer (requires isagellm)
try:
    from sage_libs.sage_agentic.intent.llm_recognizer import LLMIntentRecognizer

    _llm_recognizer_available = True
except ImportError:
    LLMIntentRecognizer = None
    _llm_recognizer_available = False

__all__ = [
    "ChainedIntentRecognizer",
    "IntentRecognitionContext",
    "IntentRecognizer",
    "INTENT_TOOLS",
    "IntentTool",
    "IntentToolsLoader",
    "IntentClassifier",
    "build_recognizer_chain",
    "KeywordIntentRecognizer",
    "LLMIntentRecognizer",
    "DOMAIN_DISPLAY_NAMES",
    "INTENT_DISPLAY_NAMES",
    "IntentResult",
    "KnowledgeDomain",
    "UserIntent",
    "get_domain_display_name",
    "get_intent_display_name",
    "get_intent_tool",
    "get_all_intent_keywords",
]
