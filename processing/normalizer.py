"""Entity normalization utilities. Populated in Phase 2."""

from __future__ import annotations


def normalize_ein(ein: str) -> str:
    """Normalize EIN to XX-XXXXXXX format."""
    digits = "".join(c for c in ein if c.isdigit())
    if len(digits) != 9:
        raise ValueError(f"Invalid EIN: {ein!r}")
    return f"{digits[:2]}-{digits[2:]}"


def normalize_name(name: str) -> str:
    """Lowercase and strip whitespace for entity name matching."""
    return " ".join(name.lower().split())
