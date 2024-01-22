from __future__ import annotations

__version__ = "0.4.0"


def __getattr__(name: str):
    if name in {"CalloutsExtension", "makeExtension"}:
        from . import callouts

        return getattr(callouts, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
