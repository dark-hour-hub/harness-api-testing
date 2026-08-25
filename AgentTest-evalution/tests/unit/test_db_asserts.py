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


from db_asserts import (  # noqa: E402
    load_db_asserts, structural_errors,
    parse_schema_columns, compile_assert, build_module_source,
    extract_declarations, extract_assert_refs, validate_feature,
)

FEATURE_SAMPLE = """\
Scenario: create agent
  Given 打开首页
  When 点击按钮 "新增智能体"
  And 令 $code = "AGT_UI_${ts}"
  And 令 $name = "UI测试智能体_${ts}"
  And 在 "智能体编码" 输入框中输入 "$code"
  And 点击按钮 "保存"
  Then 应看到提示 "智能体已新增"
  And 且数据已保存到 "AGENT_CREATE_001"
"""


def test_extract_declarations():
    decls = extract_declarations(FEATURE_SAMPLE)
    assert decls == [("code", "AGT_UI_${ts}"), ("name", "UI测试智能体_${ts}")]


def test_extract_assert_refs():
    assert extract_assert_refs(FEATURE_SAMPLE) == ["AGENT_CREATE_001"]


def test_validate_feature_ok(tmp_path):
    p = tmp_path / "db-asserts.yaml"
    p.write_text(VALID_YAML, encoding="utf-8")
    asserts = load_db_asserts(p)
    cols = parse_schema_columns(SCHEMA_SAMPLE)
    assert validate_feature(FEATURE_SAMPLE, asserts, cols) == []


def test_validate_feature_unknown_id():
    assert validate_feature(FEATURE_SAMPLE, {}, parse_schema_columns(SCHEMA_SAMPLE)) != []


def test_validate_feature_undeclared_var(tmp_path):
    p = tmp_path / "db-asserts.yaml"
    p.write_text(VALID_YAML, encoding="utf-8")
    asserts = load_db_asserts(p)
    feature = FEATURE_SAMPLE.replace('输入 "$code"', '输入 "$ghost"')
    assert any("未声明的场景变量" in e for e in
               validate_feature(feature, asserts, parse_schema_columns(SCHEMA_SAMPLE)))


def test_validate_feature_use_before_declare():
    feature = (
        'Scenario: x\n'
        '  When 在 "智能体编码" 输入框中输入 "$code"\n'
        '  And 令 $code = "AGT"\n'
    )
    errors = validate_feature(feature, {}, parse_schema_columns(SCHEMA_SAMPLE))
    assert any("先使用后声明" in e for e in errors)


def test_validate_feature_ignores_dollar_json_path():
    feature = 'When 在 "$.answer" 输入框中输入 "$.answer"\n'
    assert validate_feature(feature, {}, parse_schema_columns(SCHEMA_SAMPLE)) == []

SCHEMA_SAMPLE = """\
CREATE TABLE agent_config (
    id BIGINT NOT NULL AUTO_INCREMENT,
    agent_code VARCHAR(64) NOT NULL,
    agent_name VARCHAR(200) NOT NULL,
    risk_tier VARCHAR(8) NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (id),
    CONSTRAINT uk_agent_code UNIQUE (agent_code)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8mb4;

CREATE TABLE `indicator_catalog` (
    `id` BIGINT NOT NULL,
    `code` VARCHAR(32) NOT NULL,
    PRIMARY KEY (`id`)
);
"""


def test_parse_schema_columns():
    tables = parse_schema_columns(SCHEMA_SAMPLE)
    assert "agent_config" in tables
    assert {"id", "agent_code", "agent_name", "enabled"} <= tables["agent_config"]
    assert "indicator_catalog" in tables
    assert "code" in tables["indicator_catalog"]


def test_compile_assert_basic(tmp_path):
    p = tmp_path / "db-asserts.yaml"
    p.write_text(VALID_YAML, encoding="utf-8")
    compiled = compile_assert(load_db_asserts(p)["AGENT_CREATE_001"], parse_schema_columns(SCHEMA_SAMPLE))
    assert compiled["sql"] == (
        "SELECT agent_name, enabled FROM agent_config "
        "WHERE agent_code = %(p0)s"
    )
    assert compiled["params"] == [{"key": "p0", "mode": "var", "ref": "$code", "value": None}]
    assert compiled["asserts"][0] == {"field": "agent_name", "mode": "var", "ref": "$name", "value": None}
    assert compiled["asserts"][1] == {"field": "enabled", "mode": "literal", "ref": None, "value": 1}
    assert compiled["expect_records"] == 1
    assert compiled["schema_ref"] == "schema.sql#agent_config"


def test_compile_assert_unknown_table():
    import pytest as _pytest
    with _pytest.raises(ValueError, match="不在 schema"):
        compile_assert(
            {"id": "X", "table": "ghost", "where": [{"field": "id", "value": 1}],
             "assert_fields": [], "expect_records": 1, "schema_ref": "schema.sql#ghost"},
            parse_schema_columns(SCHEMA_SAMPLE),
        )


def test_compile_assert_unknown_column():
    import pytest as _pytest
    with _pytest.raises(ValueError, match="agent_config.no_such_col"):
        compile_assert(
            {"id": "X", "table": "agent_config", "where": [{"field": "no_such_col", "value": 1}],
             "assert_fields": [], "expect_records": 1, "schema_ref": "schema.sql#agent_config"},
            parse_schema_columns(SCHEMA_SAMPLE),
        )


def test_compile_assert_empty_where_forbidden():
    import pytest as _pytest
    with _pytest.raises(ValueError, match="where 条件为空"):
        compile_assert(
            {"id": "X", "table": "agent_config", "where": [],
             "assert_fields": [], "expect_records": 1, "schema_ref": "schema.sql#agent_config"},
            parse_schema_columns(SCHEMA_SAMPLE),
        )


def test_compile_assert_literal_where(tmp_path):
    p = tmp_path / "db-asserts.yaml"
    p.write_text(
        "db_asserts:\n"
        "  - id: RISK_CHECK\n"
        "    table: agent_config\n"
        "    expect_records: 1\n"
        "    where:\n"
        "      - { field: risk_tier, value: D }\n"
        "    assert_fields: []\n"
        "    schema_ref: schema.sql#agent_config\n",
        encoding="utf-8",
    )
    compiled = compile_assert(load_db_asserts(p)["RISK_CHECK"], parse_schema_columns(SCHEMA_SAMPLE))
    assert compiled["sql"] == "SELECT 1 FROM agent_config WHERE risk_tier = %(p0)s"
    assert compiled["params"][0] == {"key": "p0", "mode": "literal", "ref": None, "value": "D"}


def test_build_module_source_roundtrip():
    compiled = {
        "AGENT_CREATE_001": {
            "id": "AGENT_CREATE_001", "table": "agent_config", "expect_records": 1,
            "sql": "SELECT agent_name FROM agent_config WHERE agent_code = %(p0)s",
            "params": [{"key": "p0", "mode": "var", "ref": "$code", "value": None}],
            "asserts": [{"field": "agent_name", "mode": "var", "ref": "$name", "value": None}],
            "schema_ref": "schema.sql#agent_config",
        }
    }
    src = build_module_source(compiled)
    ns: dict = {}
    exec(src, ns)  # noqa: S102
    assert ns["DB_ASSERT_MAP"] == compiled