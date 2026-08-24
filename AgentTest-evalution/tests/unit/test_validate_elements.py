# -*- coding: utf-8 -*-
"""scripts/validate_elements.py 单元测试"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from validate_elements import validate  # noqa: E402

GOOD = """elements:
  新增智能体:
    strategies:
      - { type: role, role: button, name: "新增智能体" }
  风险等级:
    strategies:
      - { type: data-testid, value: agent-risk-tier }
"""


def test_valid_map_no_errors(tmp_path):
    p = tmp_path / "elements.yaml"
    p.write_text(GOOD, encoding="utf-8")
    assert validate(p) == []


def test_unknown_strategy_type(tmp_path):
    p = tmp_path / "elements.yaml"
    p.write_text(
        "elements:\n  x:\n    strategies:\n      - { type: nope, value: a }\n",
        encoding="utf-8",
    )
    errors = validate(p)
    assert len(errors) == 1 and "nope" in errors[0]


def test_missing_strategies(tmp_path):
    p = tmp_path / "elements.yaml"
    p.write_text("elements:\n  x:\n    strategies: []\n", encoding="utf-8")
    errors = validate(p)
    assert len(errors) == 1 and "strategies" in errors[0]


def test_role_strategy_needs_name(tmp_path):
    p = tmp_path / "elements.yaml"
    p.write_text(
        "elements:\n  x:\n    strategies:\n      - { type: role, role: button }\n",
        encoding="utf-8",
    )
    errors = validate(p)
    assert len(errors) == 1 and "name" in errors[0]


def test_duplicate_keys(tmp_path):
    p = tmp_path / "elements.yaml"
    p.write_text(
        "elements:\n  a:\n    strategies:\n      - { type: text, value: a }\n"
        "  a:\n    strategies:\n      - { type: text, value: b }\n",
        encoding="utf-8",
    )
    errors = validate(p)
    assert len(errors) == 1 and errors[0].startswith("元素 key 重复")


def test_nested_duplicate_keys(tmp_path):
    p = tmp_path / "elements.yaml"
    p.write_text(
        "elements:\n  a:\n    strategies:\n      - { type: text, value: a }\n"
        "  b:\n    x: 1\n    x: 2\n",
        encoding="utf-8",
    )
    errors = validate(p)
    assert len(errors) == 1 and errors[0].startswith("元素 key 重复")


def test_missing_file(tmp_path):
    assert validate(tmp_path / "not-exists.yaml") == []
