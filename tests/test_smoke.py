"""Smoke tests for sage-libs-intent."""


def test_import_intent_module() -> None:
    from sage_libs.sage_agentic import intent

    assert intent.IntentClassifier is not None


def test_build_recognizer_chain() -> None:
    from sage_libs.sage_agentic.intent import build_recognizer_chain

    chain = build_recognizer_chain(primary_mode="keyword")
    assert chain is not None
