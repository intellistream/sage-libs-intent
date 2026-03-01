from __future__ import annotations

import pytest

from sage_libs.sage_agentic.intent import IntentClassifier, build_recognizer_chain


def test_classifier_module_exports_only_classifier_symbol() -> None:
    from sage_libs.sage_agentic.intent import classifier

    assert classifier.__all__ == ["IntentClassifier"]


def test_factory_rejects_unsupported_mode() -> None:
    with pytest.raises(ValueError, match="Unsupported recognizer mode"):
        build_recognizer_chain(primary_mode="unknown-mode")


def test_canonical_import_path_for_classifier() -> None:
    classifier = IntentClassifier(mode="keyword")
    assert classifier.is_initialized is True
