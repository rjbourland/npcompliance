"""Unit tests for processing.normalizer."""

from __future__ import annotations

import pytest

from processing.normalizer import normalize_ein, normalize_name


def test_normalize_ein_with_dashes():
    assert normalize_ein("12-3456789") == "12-3456789"


def test_normalize_ein_without_dashes():
    assert normalize_ein("123456789") == "12-3456789"


def test_normalize_ein_invalid():
    with pytest.raises(ValueError):
        normalize_ein("1234")


def test_normalize_name():
    assert normalize_name("  American Red   Cross  ") == "american red cross"


def test_normalize_name_already_clean():
    assert normalize_name("united way") == "united way"
