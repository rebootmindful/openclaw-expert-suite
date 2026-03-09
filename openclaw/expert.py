"""
Forward-chaining expert system engine.
"""
from __future__ import annotations

from typing import Iterable

from openclaw.rules import Fact, FactBase, Rule


class ExpertEngine:
    """A simple forward-chaining inference engine.

    Rules are evaluated in descending priority order.  Each rule fires at
    most once per :meth:`run` cycle unless *allow_refiring* is set to
    *True* or :meth:`reset` is called between cycles.

    Example::

        engine = ExpertEngine()
        engine.declare(Fact("temperature", 42))

        engine.add_rule(Rule(
            name="high-temp",
            condition=lambda fb: fb.has("temperature") and fb.get("temperature").value > 40,
            action=lambda fb: fb.declare(Fact("alert", "HIGH TEMPERATURE")),
            priority=10,
        ))

        engine.run()
        print(engine.facts.get("alert").value)  # HIGH TEMPERATURE
    """

    def __init__(self, *, allow_refiring: bool = False) -> None:
        self._rules: list[Rule] = []
        self._facts = FactBase()
        self._allow_refiring = allow_refiring

    # ------------------------------------------------------------------
    # Rule management
    # ------------------------------------------------------------------

    def add_rule(self, rule: Rule) -> None:
        """Register a rule with the engine."""
        self._rules.append(rule)
        self._sort_rules()

    def add_rules(self, rules: Iterable[Rule]) -> None:
        """Register multiple rules at once."""
        self._rules.extend(rules)
        self._sort_rules()

    def remove_rule(self, name: str) -> None:
        """Unregister a rule by name.  No-op if the name is unknown."""
        self._rules = [r for r in self._rules if r.name != name]

    def _sort_rules(self) -> None:
        self._rules.sort(key=lambda r: r.priority, reverse=True)

    # ------------------------------------------------------------------
    # Fact management
    # ------------------------------------------------------------------

    def declare(self, fact: Fact) -> None:
        """Assert a fact into the engine's knowledge base."""
        self._facts.declare(fact)

    def retract(self, name: str) -> None:
        """Remove a fact from the knowledge base by name."""
        self._facts.retract(name)

    @property
    def facts(self) -> FactBase:
        """The engine's current fact base (read-only reference)."""
        return self._facts

    # ------------------------------------------------------------------
    # Inference
    # ------------------------------------------------------------------

    def run(self, max_cycles: int = 100) -> int:
        """Execute the forward-chaining inference loop.

        The engine repeatedly scans all rules, fires those whose conditions
        are satisfied, and continues until no new rules fire or *max_cycles*
        is reached.

        Args:
            max_cycles: Safety limit on the number of agenda cycles.

        Returns:
            The total number of rules that fired during this run.
        """
        total_fired = 0
        for _ in range(max_cycles):
            cycle_fired = 0
            for rule in self._rules:
                if not self._allow_refiring and rule.has_fired():
                    continue
                if rule.matches(self._facts):
                    rule.fire(self._facts)
                    cycle_fired += 1
                    total_fired += 1
            if cycle_fired == 0:
                break
        return total_fired

    def reset(self) -> None:
        """Clear all facts and reset all rule fired-flags."""
        self._facts = FactBase()
        for rule in self._rules:
            rule.reset()

    def __repr__(self) -> str:
        return (
            f"ExpertEngine(rules={len(self._rules)}, "
            f"facts={len(self._facts)}, "
            f"allow_refiring={self._allow_refiring})"
        )
