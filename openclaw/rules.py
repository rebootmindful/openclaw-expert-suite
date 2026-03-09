"""
Rule and Fact primitives for the openclaw expert system engine.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class Fact:
    """A named piece of information stored in the fact base.

    Attributes:
        name: Unique identifier for the fact.
        value: The value associated with the fact.
    """

    name: str
    value: Any = None

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Fact):
            return self.name == other.name
        return NotImplemented


class FactBase:
    """An in-memory store for :class:`Fact` instances."""

    def __init__(self) -> None:
        self._facts: dict[str, Fact] = {}

    # ------------------------------------------------------------------
    # Mutation helpers
    # ------------------------------------------------------------------

    def declare(self, fact: Fact) -> None:
        """Add or overwrite a fact in the knowledge base."""
        self._facts[fact.name] = fact

    def retract(self, name: str) -> None:
        """Remove a fact by name.  No-op if the fact does not exist."""
        self._facts.pop(name, None)

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------

    def get(self, name: str) -> Fact | None:
        """Return the fact with the given name, or *None* if absent."""
        return self._facts.get(name)

    def has(self, name: str) -> bool:
        """Return *True* when the fact base contains a fact named *name*."""
        return name in self._facts

    def all_facts(self) -> list[Fact]:
        """Return a snapshot of all facts currently in the base."""
        return list(self._facts.values())

    def __len__(self) -> int:
        return len(self._facts)

    def __repr__(self) -> str:
        facts = ", ".join(f"{k}={v.value!r}" for k, v in self._facts.items())
        return f"FactBase({facts})"


@dataclass
class Rule:
    """A production rule consisting of a condition and an action.

    Attributes:
        name: Human-readable rule identifier.
        condition: A callable that accepts a :class:`FactBase` and returns
            *True* when the rule should fire.
        action: A callable that accepts a :class:`FactBase` and performs
            any side-effects (e.g. asserting new facts, printing output).
        priority: Higher values cause the rule to be evaluated first.
            Defaults to ``0``.
        description: Optional free-text description of the rule.
    """

    name: str
    condition: Callable[[FactBase], bool]
    action: Callable[[FactBase], None]
    priority: int = 0
    description: str = ""
    _fired: bool = field(default=False, init=False, repr=False)

    def matches(self, facts: FactBase) -> bool:
        """Return *True* when this rule's condition is satisfied.

        Any exception raised by user-supplied condition callables (e.g.
        ``AttributeError`` when a fact is absent, ``TypeError`` on bad
        comparisons) is caught and treated as a non-match so the engine
        continues processing remaining rules uninterrupted.
        """
        try:
            return bool(self.condition(facts))
        except Exception:  # noqa: BLE001
            return False

    def fire(self, facts: FactBase) -> None:
        """Execute the rule action and mark the rule as fired."""
        self.action(facts)
        self._fired = True

    def has_fired(self) -> bool:
        """Return *True* if this rule has fired since the last :meth:`reset`."""
        return self._fired

    def reset(self) -> None:
        """Clear the *fired* flag so the rule can fire again."""
        self._fired = False
