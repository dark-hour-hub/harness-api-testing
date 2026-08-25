# -*- coding: utf-8 -*-
"""lib/db_asserts.py 单元测试：db-asserts.yaml 加载与结构校验（无外部依赖）"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))

from db_asserts import load_db_asserts, structural_errors  # noqa: E402

VALID_YAML = """\
db_asserts:
  - id: AGENT_CREATE_001
    ui_action: 保存新增智能体表单
    table: agent_config
    expect_records: 1
    where:
      - { field: agent_code, from: var, ref: $code }
    assert_fields:
      - { field: agent_name, from: var, ref: $name }
      - { field: enabled, equals: 1 }
    sync: { api: "POST /api/agents", status: 200 }
    schema_ref: schema.sql#agent_config
"""


def test_load_db_asserts_parses_yaml(tmp_path):
    p = tmp_path / "db-asserts.yaml"
    p.write_text(VALID_YAML, encoding="utf-8")
    asserts = load_db_asserts(p)
    assert list(asserts.keys()) == ["AGENT_CREATE_001"]
    assert asserts["AGENT_CREATE_001"]["table"] == "agent_config"
    assert asserts["AGENT_CREATE_001"]["where"][0] == {"field": "agent_code", "from": "var", "ref": "$code"}


def test_load_db_asserts_missing_file(tmp_path):
    assert load_db_asserts(tmp_path / "nope.yaml") == {}


def test_load_db_asserts_empty_file(tmp_path):
    p = tmp_path / "db-asserts.yaml"
    p.write_text("", encoding="utf-8")
    assert load_db_asserts(p) == {}


def test_structural_errors_ok(tmp_path):
    p = tmp_path / "db-asserts.yaml"
    p.write_text(VALID_YAML, encoding="utf-8")
    assert structural_errors(load_db_asserts(p)) == []


def test_structural_errors_missing_required_keys(tmp_path):
    p = tmp_path / "db-asserts.yaml"
    p.write_text(
        "db_asserts:\n  - id: X\n    where: []\n",
        encoding="utf-8",
    )
    errors = structural_errors(load_db_asserts(p))
    assert any("table" in e for e in errors)
    assert any("where" in e for e in errors)