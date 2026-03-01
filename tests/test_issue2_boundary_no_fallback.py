from __future__ import annotations

import builtins

import pytest

from sage_libs.sage_agentic.intent import build_recognizer_chain


@pytest.fixture
def block_tool_selection_import(monkeypatch: pytest.MonkeyPatch):
    original_import = builtins.__import__

    def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name.startswith("sage_libs.sage_agentic.agents.action.tool_selection"):
            raise ImportError("blocked for test")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", guarded_import)


def test_selector_mode_fails_fast_without_dependency(block_tool_selection_import) -> None:
    with pytest.raises(ModuleNotFoundError, match="requires isage-agentic tool_selection modules"):
        build_recognizer_chain(primary_mode="selector")


def test_selector_secondary_mode_never_silent_fallback(block_tool_selection_import) -> None:
    with pytest.raises(ModuleNotFoundError, match="requires isage-agentic tool_selection modules"):
        build_recognizer_chain(primary_mode="keyword", secondary_mode="selector")


def test_secondary_mode_validated_explicitly() -> None:
    with pytest.raises(ValueError, match="Unsupported recognizer mode"):
        build_recognizer_chain(primary_mode="keyword", secondary_mode="unknown")
