"""Tests for openclaw.rules (Fact, FactBase, Rule)."""
import pytest

from openclaw.rules import Fact, FactBase, Rule


# ---------------------------------------------------------------------------
# Fact
# ---------------------------------------------------------------------------


class TestFact:
    def test_name_and_value(self):
        f = Fact("temperature", 42)
        assert f.name == "temperature"
        assert f.value == 42

    def test_value_defaults_to_none(self):
        f = Fact("present")
        assert f.value is None

    def test_equality_by_name(self):
        assert Fact("x", 1) == Fact("x", 99)

    def test_inequality_different_name(self):
        assert Fact("x") != Fact("y")

    def test_hashable(self):
        s = {Fact("a"), Fact("b"), Fact("a")}
        assert len(s) == 2


# ---------------------------------------------------------------------------
# FactBase
# ---------------------------------------------------------------------------


class TestFactBase:
    def test_declare_and_get(self):
        fb = FactBase()
        fb.declare(Fact("age", 30))
        assert fb.get("age").value == 30

    def test_get_missing_returns_none(self):
        fb = FactBase()
        assert fb.get("missing") is None

    def test_has(self):
        fb = FactBase()
        fb.declare(Fact("present"))
        assert fb.has("present")
        assert not fb.has("absent")

    def test_overwrite_fact(self):
        fb = FactBase()
        fb.declare(Fact("x", 1))
        fb.declare(Fact("x", 2))
        assert fb.get("x").value == 2

    def test_retract(self):
        fb = FactBase()
        fb.declare(Fact("temp", 100))
        fb.retract("temp")
        assert not fb.has("temp")

    def test_retract_missing_noop(self):
        fb = FactBase()
        fb.retract("nonexistent")  # should not raise

    def test_all_facts(self):
        fb = FactBase()
        fb.declare(Fact("a", 1))
        fb.declare(Fact("b", 2))
        names = {f.name for f in fb.all_facts()}
        assert names == {"a", "b"}

    def test_len(self):
        fb = FactBase()
        assert len(fb) == 0
        fb.declare(Fact("x"))
        assert len(fb) == 1


# ---------------------------------------------------------------------------
# Rule
# ---------------------------------------------------------------------------


class TestRule:
    def _always_true(self, fb):
        return True

    def _always_false(self, fb):
        return False

    def _noop(self, fb):
        pass

    def test_matches_true(self):
        rule = Rule("r", self._always_true, self._noop)
        assert rule.matches(FactBase())

    def test_matches_false(self):
        rule = Rule("r", self._always_false, self._noop)
        assert not rule.matches(FactBase())

    def test_matches_exception_returns_false(self):
        def bad_cond(fb):
            raise RuntimeError("oops")

        rule = Rule("r", bad_cond, self._noop)
        assert not rule.matches(FactBase())

    def test_fire_sets_fired_flag(self):
        rule = Rule("r", self._always_true, self._noop)
        assert not rule.has_fired()
        rule.fire(FactBase())
        assert rule.has_fired()

    def test_fire_executes_action(self):
        results = []
        rule = Rule(
            "r",
            self._always_true,
            lambda fb: results.append("fired"),
        )
        rule.fire(FactBase())
        assert results == ["fired"]

    def test_reset_clears_fired(self):
        rule = Rule("r", self._always_true, self._noop)
        rule.fire(FactBase())
        rule.reset()
        assert not rule.has_fired()

    def test_priority_default(self):
        rule = Rule("r", self._always_true, self._noop)
        assert rule.priority == 0
