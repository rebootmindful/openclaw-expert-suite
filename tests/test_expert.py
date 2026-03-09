"""Tests for openclaw.expert (ExpertEngine)."""
import pytest

from openclaw.expert import ExpertEngine
from openclaw.rules import Fact, Rule


class TestExpertEngine:
    def test_repr(self):
        engine = ExpertEngine()
        assert "ExpertEngine" in repr(engine)

    def test_declare_and_facts(self):
        engine = ExpertEngine()
        engine.declare(Fact("x", 10))
        assert engine.facts.has("x")
        assert engine.facts.get("x").value == 10

    def test_retract(self):
        engine = ExpertEngine()
        engine.declare(Fact("x", 10))
        engine.retract("x")
        assert not engine.facts.has("x")

    # ------------------------------------------------------------------
    # Rule registration
    # ------------------------------------------------------------------

    def test_add_rule(self):
        engine = ExpertEngine()
        rule = Rule("r", lambda fb: True, lambda fb: None)
        engine.add_rule(rule)
        assert len(engine._rules) == 1

    def test_add_rules_multiple(self):
        engine = ExpertEngine()
        rules = [
            Rule("r1", lambda fb: True, lambda fb: None),
            Rule("r2", lambda fb: True, lambda fb: None),
        ]
        engine.add_rules(rules)
        assert len(engine._rules) == 2

    def test_remove_rule(self):
        engine = ExpertEngine()
        engine.add_rule(Rule("r", lambda fb: True, lambda fb: None))
        engine.remove_rule("r")
        assert engine._rules == []

    def test_remove_nonexistent_noop(self):
        engine = ExpertEngine()
        engine.remove_rule("ghost")  # should not raise

    def test_rules_sorted_by_priority(self):
        engine = ExpertEngine()
        engine.add_rule(Rule("low", lambda fb: True, lambda fb: None, priority=1))
        engine.add_rule(Rule("high", lambda fb: True, lambda fb: None, priority=10))
        assert engine._rules[0].name == "high"

    # ------------------------------------------------------------------
    # Inference
    # ------------------------------------------------------------------

    def test_run_fires_matching_rule(self):
        engine = ExpertEngine()
        engine.declare(Fact("trigger", True))
        fired = []
        engine.add_rule(
            Rule(
                "r",
                lambda fb: fb.has("trigger"),
                lambda fb: fired.append(1),
            )
        )
        total = engine.run()
        assert total == 1
        assert fired == [1]

    def test_run_does_not_fire_non_matching_rule(self):
        engine = ExpertEngine()
        fired = []
        engine.add_rule(
            Rule(
                "r",
                lambda fb: fb.has("missing"),
                lambda fb: fired.append(1),
            )
        )
        engine.run()
        assert fired == []

    def test_rule_fires_at_most_once_by_default(self):
        engine = ExpertEngine()
        engine.declare(Fact("x", 1))
        fired = []
        engine.add_rule(
            Rule("r", lambda fb: fb.has("x"), lambda fb: fired.append(1))
        )
        engine.run()
        assert len(fired) == 1

    def test_allow_refiring(self):
        """With allow_refiring=True a rule can fire every cycle."""
        engine = ExpertEngine(allow_refiring=True)
        engine.declare(Fact("x", 1))
        fired = []

        def action(fb):
            fired.append(1)
            # Remove fact after first fire to stop infinite loop
            if len(fired) >= 3:
                fb.retract("x")

        engine.add_rule(Rule("r", lambda fb: fb.has("x"), action))
        engine.run(max_cycles=10)
        assert len(fired) == 3

    def test_chained_rules(self):
        """One rule's action can trigger a second rule."""
        engine = ExpertEngine()
        engine.declare(Fact("start", True))

        engine.add_rule(
            Rule(
                "step1",
                lambda fb: fb.has("start") and not fb.has("middle"),
                lambda fb: fb.declare(Fact("middle", True)),
            )
        )
        engine.add_rule(
            Rule(
                "step2",
                lambda fb: fb.has("middle") and not fb.has("end"),
                lambda fb: fb.declare(Fact("end", True)),
            )
        )

        engine.run()
        assert engine.facts.has("end")

    def test_run_returns_fired_count(self):
        engine = ExpertEngine()
        engine.declare(Fact("a", 1))
        engine.declare(Fact("b", 2))
        engine.add_rule(Rule("r1", lambda fb: fb.has("a"), lambda fb: None))
        engine.add_rule(Rule("r2", lambda fb: fb.has("b"), lambda fb: None))
        count = engine.run()
        assert count == 2

    def test_max_cycles_limits_execution(self):
        engine = ExpertEngine(allow_refiring=True)
        engine.declare(Fact("loop", True))
        fired = []
        engine.add_rule(
            Rule("r", lambda fb: fb.has("loop"), lambda fb: fired.append(1))
        )
        engine.run(max_cycles=5)
        assert len(fired) == 5

    def test_reset_clears_facts_and_rules(self):
        engine = ExpertEngine()
        engine.declare(Fact("x", 1))
        rule = Rule("r", lambda fb: True, lambda fb: None)
        engine.add_rule(rule)
        rule.fire(engine.facts)  # manually fire to set _fired flag
        engine.reset()
        assert not engine.facts.has("x")
        assert not engine._rules[0].has_fired()
