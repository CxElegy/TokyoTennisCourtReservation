from __future__ import annotations

from .base import Site


def get_site(name: str) -> Site:
    if name == "edogawa":
        from .edogawa import EdogawaSite

        return EdogawaSite()
    raise ValueError(f"unknown site: {name}")
