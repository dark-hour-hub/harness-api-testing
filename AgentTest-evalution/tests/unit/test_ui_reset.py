# -*- coding: utf-8 -*-
"""scripts/ui_reset.py 单元测试"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from ui_reset import build_plan, parse_confirmation  # noqa: E402

SQL = """-- 智能体评测平台 UI 测试清理模板（FK 逆序）
-- 运行期数据判定：created_by 为 ui-test 或 code 以 AGT_UI_/TC_UI_/SCHEME_UI_ 开头
DELETE FROM agent WHERE code LIKE 'AGT_UI_%' OR code LIKE 'AGT_SEED_%';
DELETE FROM indicator WHERE code LIKE 'IND_UI_%';
"""


def test_build_plan(tmp_path):
    p = tmp_path / "cleanup_template.sql"
    p.write_text(SQL, encoding="utf-8")
    plan = build_plan(p)
    assert len(plan["statements"]) == 2
    assert "agent" in plan["tables"]
    assert "indicator" in plan["tables"]


def test_build_plan_missing_file(tmp_path):
    plan = build_plan(tmp_path / "nope.sql")
    assert plan["statements"] == [] and plan["tables"] == []


def test_parse_confirmation():
    assert parse_confirmation("yes") is True
    assert parse_confirmation("y") is True
    assert parse_confirmation("no") is False
    assert parse_confirmation("") is False
