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
from sage_libs.sage_agentic.intent.types import (
    DOMAIN_DISPLAY_NAMES,
    INTENT_DISPLAY_NAMES,
    IntentResult,
    KnowledgeDomain,
    UserIntent,
    get_domain_display_name,
    get_intent_display_name,
)
from sage_libs.sage_agentic.intent.keyword_recognizer import KeywordIntentRecognizer

# Lazy imports for optional dependencies
def _get_intent_classifier():
    """Lazy import IntentClassifier to avoid immediate LLM dependency."""
    from sage_libs.sage_agentic.intent.classifier import IntentClassifier
    return IntentClassifier

def _get_llm_recognizer():
    """Lazy import LLMIntentRecognizer (requires isagellm)."""
    from sage_libs.sage_agentic.intent.llm_recognizer import LLMIntentRecognizer
    return LLMIntentRecognizer

def _get_recognizer_chain_builder():
    """Lazy import build_recognizer_chain."""
    from sage_libs.sage_agentic.intent.factory import build_recognizer_chain
    return build_recognizer_chain

# Export lazy-loaded classes
IntentClassifier = None  # Will be imported on demand
LLMIntentRecognizer = None
build_recognizer_chain = None

def __getattr__(name):
    """Lazy attribute access for optional dependencies."""
    global IntentClassifier, LLMIntentRecognizer, build_recognizer_chain
    
    if name == "IntentClassifier":
        if IntentClassifier is None:
            IntentClassifier = _get_intent_classifier()
        return IntentClassifier
    elif name == "LLMIntentRecognizer":
        if LLMIntentRecognizer is None:
            LLMIntentRecognizer = _get_llm_recognizer()
        return LLMIntentRecognizer
    elif name == "build_recognizer_chain":
        if build_recognizer_chain is None:
            build_recognizer_chain = _get_recognizer_chain_builder()
        return build_recognizer_chain
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

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
