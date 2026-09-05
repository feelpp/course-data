"""A dirty or build-mutated source cannot qualify as a frozen candidate."""

import pytest

from tools import qualify_release


def test_dirty_checkout_fails_before_build(monkeypatch):
    monkeypatch.setattr(qualify_release, "working_tree_dirty", lambda: True)
    commands = []
    monkeypatch.setattr(qualify_release, "run", commands.append)
    with pytest.raises(RuntimeError, match="clean committed checkout"):
        qualify_release.qualify()
    assert commands == []


def test_build_mutation_cannot_be_qualified(monkeypatch):
    monkeypatch.setattr(qualify_release, "working_tree_dirty", lambda: False)
    monkeypatch.setattr(qualify_release, "run", lambda command: None)
    monkeypatch.setattr(qualify_release, "capture_release", lambda: {"working_tree_dirty": True})
    with pytest.raises(RuntimeError, match="changed the committed source"):
        qualify_release.qualify()
