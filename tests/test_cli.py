"""Tests for openclaw.cli."""
import json
import tempfile
from pathlib import Path

import pytest

from openclaw.cli import build_parser, main


class TestCLI:
    def test_version_flag(self, capsys):
        rc = main(["--version"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "openclaw-expert-suite" in out

    def test_no_args_shows_help(self, capsys):
        rc = main([])
        assert rc == 0
        out = capsys.readouterr().out
        assert "openclaw" in out.lower()

    def test_run_missing_file(self, capsys):
        rc = main(["run", "/nonexistent/path/facts.json"])
        assert rc == 1
        err = capsys.readouterr().err
        assert "not found" in err

    def test_run_valid_facts(self, capsys, tmp_path):
        facts_file = tmp_path / "facts.json"
        facts_file.write_text(json.dumps({"temperature": 42, "humidity": 80}))
        rc = main(["run", str(facts_file)])
        assert rc == 0
        out = capsys.readouterr().out
        assert "temperature" in out
        assert "humidity" in out

    def test_run_invalid_json(self, capsys, tmp_path):
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("{not valid json}")
        rc = main(["run", str(bad_file)])
        assert rc == 1
        err = capsys.readouterr().err
        assert "invalid JSON" in err

    def test_run_non_object_json(self, capsys, tmp_path):
        bad_file = tmp_path / "array.json"
        bad_file.write_text(json.dumps([1, 2, 3]))
        rc = main(["run", str(bad_file)])
        assert rc == 1
        err = capsys.readouterr().err
        assert "JSON object" in err

    def test_run_empty_facts(self, capsys, tmp_path):
        facts_file = tmp_path / "empty.json"
        facts_file.write_text(json.dumps({}))
        rc = main(["run", str(facts_file)])
        assert rc == 0
        out = capsys.readouterr().out
        assert "no facts" in out
