# -*- coding: utf-8 -*-
"""lib/ui_profile.py 运行期 DB 断言与场景变量展开单元测试（FakeConn 注入，无真实 DB）"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))

from ui_profile import resolve_vars, run_db_assert  # noqa: E402


class FakeConn:
    """鸭子类型连接：记录执行参数，返回预设行"""

    def __init__(self, rows):
        self.rows = rows
        self.executed = None

    def cursor(self):
        return self

    def execute(self, sql, params=None):
        self.executed = (sql, params)

    def fetchall(self):
        return self.rows


COMPILED = {
    "id": "AGENT_CREATE_001",
    "table": "agent_config",
    "expect_records": 1,
    "sql": "SELECT agent_name, enabled FROM agent_config WHERE agent_code = %(p0)s",
    "params": [{"key": "p0", "mode": "var", "ref": "$code", "value": None}],
    "asserts": [
        {"field": "agent_name", "mode": "var", "ref": "$name", "value": None},
        {"field": "enabled", "mode": "literal", "ref": None, "value": 1},
    ],
    "schema_ref": "schema.sql#agent_config",
}


def test_resolve_vars_basic():
    assert resolve_vars("AGT_$code", {"code": "AGT_UI_123"}) == "AGT_AGT_UI_123"
    assert resolve_vars("$code", {"code": "X"}) == "X"


def test_resolve_vars_ignores_dynamic_placeholders():
    assert resolve_vars("${ts}", {"ts": "x"}) == "${ts}"


def test_resolve_vars_ignores_json_path():
    assert resolve_vars("$.answer", {"answer": "y"}) == "$.answer"


def test_resolve_vars_unknown_var_kept():
    assert resolve_vars("$ghost", {"code": "X"}) == "$ghost"


def test_resolve_vars_non_string():
    assert resolve_vars(123, {"a": "b"}) == 123


def test_run_db_assert_pass():
    conn = FakeConn([{"agent_name": "UI测试智能体_1", "enabled": 1}])
    run_db_assert(conn, COMPILED, {"code": "AGT_UI_1", "name": "UI测试智能体_1"})
    assert conn.executed[0] == COMPILED["sql"]
    assert conn.executed[1] == {"p0": "AGT_UI_1"}


def test_run_db_assert_record_count_mismatch():
    conn = FakeConn([])
    with pytest.raises(AssertionError, match="期望 1 条记录，实际 0 条"):
        run_db_assert(conn, COMPILED, {"code": "X", "name": "Y"})


def test_run_db_assert_field_mismatch():
    conn = FakeConn([{"agent_name": "OTHER", "enabled": 1}])
    with pytest.raises(AssertionError, match="字段 agent_name"):
        run_db_assert(conn, COMPILED, {"code": "X", "name": "Y"})


def test_run_db_assert_missing_var():
    conn = FakeConn([{"agent_name": "Y", "enabled": 1}])
    with pytest.raises(AssertionError, match="场景变量未定义: \\$code"):
        run_db_assert(conn, COMPILED, {"name": "Y"})


def test_run_db_assert_tuple_rows():
    conn = FakeConn([("Y", 1)])
    run_db_assert(conn, COMPILED, {"code": "X", "name": "Y"})