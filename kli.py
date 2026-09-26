"""Klipper Logging Interface (KLI).

This module exposes a very small subset of a Klipper event bus that can be
subscribed to by external Python code.  It is intentionally minimal – the
full Klipper API is large and tightly coupled – but it demonstrates how the
ASC component can receive telemetry without needing to modify the core
Klipper code.

Usage example::

    from kli import Kli
    kl = Kli()
    kl.subscribe("event_name", lambda data: print(data))
    kl.publish("event_name", {"value": 42})
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable, Dict, List


class Kli:
    """Very small in‑process event bus.

    The real Klipper implementation would communicate over IPC or a
    socket.  For the purposes of the ASC demo we keep everything in
    memory and expose the API used by the adaptive loop.
    """

    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable[[Any], None]]] = defaultdict(list)

    def subscribe(self, event: str, handler: Callable[[Any], None]) -> None:
        """Register *handler* to be called when *event* is published."""
        self._subscribers[event].append(handler)

    def publish(self, event: str, data: Any) -> None:
        """Invoke all handlers for *event* with *data*.

        If there are no subscribers the call is a no‑op.
        """
        for handler in self._subscribers.get(event, []):
            handler(data)

    def clear(self) -> None:
        """Remove all registered subscribers."""
        self._subscribers.clear()
