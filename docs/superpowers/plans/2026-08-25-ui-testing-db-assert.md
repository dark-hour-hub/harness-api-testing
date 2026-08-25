# UI 测试 DB 断言机制实施计划（需求文档驱动 + 确定性编译）

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 UI 测试链路加入「防假成功」DB 断言：业务按 5 节模板提供操作→表→字段映射 → AI 翻译成 `db-asserts.yaml` → 生成器编译为确定性断言代码 → 场景变量 + `且数据已保存到 <id>` 步骤运行期查库验证。

**Architecture:** 新增 `lib/db_asserts.py`（生成期纯函数：yaml 加载/结构校验/schema 解析/SQL 编译/feature 校验/模块源码生成，无浏览器无 DB 依赖，可单测）；扩展 `lib/ui_profile.py`（运行期纯函数：场景变量展开 `resolve_vars` + DB 断言执行器 `run_db_assert`，连接鸭子类型注入可单测）；`generate_playwright.py` 在生成期校验映射引用并产出 `db_asserts.py` 编译模块；`template/conftest.py` 新增 `令 $var = "..."` 与 `且数据已保存到 "<id>"` 两个步骤，DB 连接配置进 `ui-profile/business.yaml` 的 `db:` 段。

**Tech Stack:** Python 3.12、pytest、pytest-bdd + Playwright（沿用现状）、PyYAML、pymysql（新增运行时依赖）。

**依赖上游设计:** `docs/superpowers/specs/2026-08-25-ui-testing-db-assert-design.md`。

**关键路径事实（已勘察）:**
- 后端 schema：`D:\AI评测\智能体评测平台\agent-evaluation-platform-backend\db\schema.sql`（表 `agent_config`，列含 `agent_code/agent_name/risk_tier/enabled`）
- DB 连接：`application-dev.yml` 为 `jdbc:mysql://localhost:3306/agent_evaluation`
- 现有运行时同步：`business.yaml` 的 `api_sync_rules`（保存 → `POST /api/agents`），`_click_enabled_with_sync` 已实现 busy + API 同步
- 现有动态值：`lib/ui_profile.py` 的 `expand_vars`（`${ts}/${rand:8}` 等）
- 单测目录：`tests/unit/`（`test_ui_profile.py`、`test_vars_seed.py` 先例，`sys.path.insert` 引 `lib/`）

---

### Task 1: `lib/db_asserts.py` — yaml 加载与结构校验（TDD）

**Files:**
- Create: `AgentTest-evalution/tests/unit/test_db_asserts.py`
- Create: `AgentTest-evalution/lib/db_asserts.py`

- [ ] **Step 1: 编写失败测试**

```python
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
```

- [ ] **Step 2: 运行测试确认失败**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/unit/test_db_asserts.py -v`
Expected: `ModuleNotFoundError: No module named 'db_asserts'`

- [ ] **Step 3: 最小实现**

```python
# -*- coding: utf-8 -*-
"""
db_asserts.py — db-asserts.yaml 加载/校验/编译（生成期纯函数，无浏览器无 DB 依赖）

职责：
- 加载 00-requirements/db-asserts.yaml（业务映射，AI 从需求文档翻译 + 人工确认）
- 结构校验、对照后端 schema.sql 校验表/列存在性
- 编译为运行期断言结构（SQL 常量 + 参数声明），供 generate_playwright.py 产出 db_asserts.py
"""
from __future__ import annotations

from pathlib import Path
import re
from typing import Optional

import yaml


def load_db_asserts(path) -> dict:
    """加载 db-asserts.yaml → {id: entry}；缺失/空文件 → {}"""
    path = Path(path)
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return {}
    data = yaml.safe_load(text) or {}
    asserts = data.get("db_asserts") or []
    return {a["id"]: a for a in asserts if isinstance(a, dict) and a.get("id")}


_REQUIRED_KEYS = ("table", "where", "expect_records")


def structural_errors(asserts: dict) -> list:
    """结构校验：必填键缺失 → 错误清单（不抛异常，便于一次报全）"""
    errors = []
    for rid, entry in asserts.items():
        for key in _REQUIRED_KEYS:
            if key not in entry:
                errors.append(f"映射 {rid}: 缺少必填键 {key}")
        if "assert_fields" not in entry:
            errors.append(f"映射 {rid}: 缺少必填键 assert_fields")
        if "schema_ref" not in entry:
            errors.append(f"映射 {rid}: 缺少必填键 schema_ref（建议形如 schema.sql#表名）")
    return errors
```

- [ ] **Step 4: 运行测试确认通过**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/unit/test_db_asserts.py -v`
Expected: 5 passed

- [ ] **Step 5: 提交**

```bash
git add tests/unit/test_db_asserts.py lib/db_asserts.py
git commit -m "feat(ui): db_asserts.py 加载与结构校验（db-asserts.yaml）"
```

---

### Task 2: `lib/db_asserts.py` — schema 解析 + 映射编译（TDD）

**Files:**
- Modify: `AgentTest-evalution/tests/unit/test_db_asserts.py`
- Modify: `AgentTest-evalution/lib/db_asserts.py`

- [ ] **Step 1: 追加失败测试**

```python
from db_asserts import (  # noqa: E402
    load_db_asserts, structural_errors,
    parse_schema_columns, compile_assert, build_module_source,
)

SCHEMA_SAMPLE = """\
CREATE TABLE agent_config (
    id BIGINT NOT NULL AUTO_INCREMENT,
    agent_code VARCHAR(64) NOT NULL,
    agent_name VARCHAR(200) NOT NULL,
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
```

> 注意：`RISK_CHECK` 的 where 用 `risk_tier`，但 SCHEMA_SAMPLE 里没有该列——测试会失败。将 SCHEMA_SAMPLE 的 `agent_config` 定义补充 `risk_tier VARCHAR(8) NOT NULL,` 一行后再跑。

- [ ] **Step 2: 运行测试确认失败**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/unit/test_db_asserts.py -v`
Expected: 新增用例失败（`parse_schema_columns` 等函数不存在）

- [ ] **Step 3: 实现（追加到 `lib/db_asserts.py`）**

```python
_CREATE_TABLE_RE = re.compile(
    r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?`?(\w+)`?\s*\((.*?)\)\s*(?:ENGINE|DEFAULT|;|$)",
    re.IGNORECASE | re.DOTALL,
)

_SKIP_COL_LINES = ("PRIMARY", "UNIQUE", "KEY", "INDEX", "CONSTRAINT", "FOREIGN", "CHECK")


def parse_schema_columns(sql_text: str) -> dict:
    """解析 CREATE TABLE 语句 → {表名: set(列名)}（纯文本，无 DB 依赖）"""
    tables = {}
    for m in _CREATE_TABLE_RE.finditer(sql_text):
        name = m.group(1)
        cols = set()
        for line in m.group(2).splitlines():
            line = line.strip().rstrip(",")
            if not line or line.startswith(_SKIP_COL_LINES):
                continue
            col = re.match(r"`?(\w+)`?\s", line)
            if col:
                cols.add(col.group(1))
        tables[name] = cols
    return tables


def compile_assert(entry: dict, schema_columns: dict) -> dict:
    """把单条映射编译为运行期结构；表/列不存在或 where 为空 → ValueError。

    where 值来源：{ field, value: 固定值 } 或 { field, from: var, ref: $x }
    assert_fields 值来源：{ field, equals: 固定值 } 或 { field, from: var, ref: $x }
    """
    rid = entry["id"]
    table = entry["table"]
    if table not in schema_columns:
        raise ValueError(f"映射 {rid}: 表 {table} 不在 schema.sql 中")
    cols = schema_columns[table]

    where = entry.get("where") or []
    if not where:
        raise ValueError(f"映射 {rid}: where 条件为空（禁止全表断言）")
    conds, params = [], []
    for i, w in enumerate(where):
        field = w["field"]
        if field not in cols:
            raise ValueError(f"映射 {rid}: 列 {table}.{field} 不在 schema.sql 中")
        key = f"p{i}"
        conds.append(f"{field} = %({key})s")
        params.append({
            "key": key,
            "mode": "var" if w.get("from") == "var" else "literal",
            "ref": w.get("ref"),
            "value": w.get("value"),
        })

    assert_cols, assert_items = [], []
    for a in entry.get("assert_fields") or []:
        field = a["field"]
        if field not in cols:
            raise ValueError(f"映射 {rid}: 列 {table}.{field} 不在 schema.sql 中")
        assert_cols.append(field)
        assert_items.append({
            "field": field,
            "mode": "var" if a.get("from") == "var" else "literal",
            "ref": a.get("ref"),
            "value": a.get("equals"),
        })

    sql = f"SELECT {', '.join(assert_cols) or '1'} FROM {table} WHERE {' AND '.join(conds)}"
    return {
        "id": rid,
        "table": table,
        "expect_records": int(entry.get("expect_records", 1)),
        "sql": sql,
        "params": params,
        "asserts": assert_items,
        "schema_ref": entry.get("schema_ref", f"schema.sql#{table}"),
    }


def build_module_source(compiled_map: dict) -> str:
    """生成 db_asserts.py 模块源码文本（含 DB_ASSERT_MAP 常量）"""
    header = (
        "# -*- coding: utf-8 -*-\n"
        "# 由 feature-to-playwright skill 自动生成，请勿手动修改\n"
        "# DB 断言编译产物：来自 00-requirements/db-asserts.yaml + 后端 schema.sql 校验\n"
        "DB_ASSERT_MAP = {\n"
    )
    body = "".join(f"    {k!r}: {v!r},\n" for k, v in sorted(compiled_map.items()))
    return header + body + "}\n"
```

- [ ] **Step 4: 运行测试确认通过**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/unit/test_db_asserts.py -v`
Expected: 全部通过（含 Task 1 的 5 个）

- [ ] **Step 5: 提交**

```bash
git add tests/unit/test_db_asserts.py lib/db_asserts.py
git commit -m "feat(ui): db_asserts.py schema 解析与映射编译（SQL 常量生成）"
```

---

### Task 3: `lib/db_asserts.py` — feature 解析 + 引用校验（TDD）

**Files:**
- Modify: `AgentTest-evalution/tests/unit/test_db_asserts.py`
- Modify: `AgentTest-evalution/lib/db_asserts.py`

- [ ] **Step 1: 追加失败测试**

```python
from db_asserts import (  # noqa: E402
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


def test_validate_feature_undeclared_var():
    feature = FEATURE_SAMPLE.replace('输入 "$code"', '输入 "$ghost"')
    assert any("未声明的场景变量" in e for e in
               validate_feature(feature, {"AGENT_CREATE_001": {"id": "AGENT_CREATE_001"}},
                                parse_schema_columns(SCHEMA_SAMPLE)))


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
```

- [ ] **Step 2: 运行测试确认失败**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/unit/test_db_asserts.py -v`
Expected: 新增用例失败（函数不存在）

- [ ] **Step 3: 实现（追加到 `lib/db_asserts.py`）**

```python
_DECL_RE = re.compile(r'令 \$(\w+) = "([^"]*)"')
_REF_RE = re.compile(r'且数据已保存到 "([^"]+)"')
_VAR_USE_RE = re.compile(r"(?<!\$)\$([A-Za-z_]\w*)")


def extract_declarations(feature_text: str) -> list:
    """提取场景变量声明（保持出现顺序）→ [(var, value), ...]"""
    return [(m.group(1), m.group(2)) for m in _DECL_RE.finditer(feature_text)]


def extract_assert_refs(feature_text: str) -> list:
    """提取 DB 断言映射引用 → [map_id, ...]"""
    return [m.group(1) for m in _REF_RE.finditer(feature_text)]


def _line_no(text: str, pos: int) -> int:
    return text[:pos].count("\n") + 1


def validate_feature(feature_text: str, asserts: dict, schema_columns: dict) -> list:
    """feature 引用完整性校验 → 错误清单（空 = 通过）。

    校验项：映射 id 存在、表/列在 schema 中存在（经 compile_assert）、
    场景变量已声明、先声明后使用。${...} 动态值与 $.answer 之类不参与。
    """
    errors = []
    declared_pos = {}
    for var, _value in extract_declarations(feature_text):
        pos = feature_text.find(f"令 ${var} =")
        declared_pos[var] = pos if pos != -1 else 0

    for m in _VAR_USE_RE.finditer(feature_text):
        var = m.group(1)
        if var not in declared_pos:
            errors.append(f"未声明的场景变量: ${var}（行 {_line_no(feature_text, m.start())}）")
        elif m.start() < declared_pos[var]:
            errors.append(f"场景变量 ${var} 先使用后声明（行 {_line_no(feature_text, m.start())}）")

    for rid in extract_assert_refs(feature_text):
        if rid not in asserts:
            errors.append(f"db-asserts.yaml 中不存在映射 id: {rid}")
            continue
        try:
            compile_assert(asserts[rid], schema_columns)
        except ValueError as e:
            errors.append(str(e))
    return errors
```

- [ ] **Step 4: 运行测试确认通过**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/unit/test_db_asserts.py -v`
Expected: 全部通过

- [ ] **Step 5: 提交**

```bash
git add tests/unit/test_db_asserts.py lib/db_asserts.py
git commit -m "feat(ui): db_asserts.py feature 解析与映射引用校验"
```

---

### Task 4: `lib/ui_profile.py` — 场景变量展开 + 运行期断言执行器（TDD）

**Files:**
- Create: `AgentTest-evalution/tests/unit/test_db_assert_runtime.py`
- Modify: `AgentTest-evalution/lib/ui_profile.py`

- [ ] **Step 1: 编写失败测试**

```python
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
```

- [ ] **Step 2: 运行测试确认失败**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/unit/test_db_assert_runtime.py -v`
Expected: `ImportError: cannot import name 'resolve_vars'`

- [ ] **Step 3: 实现（追加到 `lib/ui_profile.py`）**

```python
_VAR_REF_RE = re.compile(r"(?<!\$)\$([A-Za-z_]\w*)")


def resolve_vars(value, vars):
    """场景变量引用展开：$name → vars[name]（${...} 动态值占位符与 $.answer 不动）"""
    if not isinstance(value, str) or not vars:
        return value
    return _VAR_REF_RE.sub(lambda m: str(vars.get(m.group(1), m.group(0))), value)


def run_db_assert(conn, compiled, scenario_vars):
    """执行编译后的 DB 断言（conn 鸭子类型：cursor()/execute/fetchall）。

    compiled 结构由 generate_playwright.py 从 db-asserts.yaml 编译产出
    （见 lib/db_asserts.py::compile_assert）。失败抛 AssertionError 含追溯信息。
    """
    params = {}
    for p in compiled.get("params", []):
        if p["mode"] == "var":
            if p["ref"] not in scenario_vars:
                raise AssertionError(f"场景变量未定义: {p['ref']}")
            params[p["key"]] = scenario_vars[p["ref"]]
        else:
            params[p["key"]] = p["value"]
    cur = conn.cursor()
    cur.execute(compiled["sql"], params)
    rows = cur.fetchall()
    expected = compiled["expect_records"]
    if len(rows) != expected:
        raise AssertionError(
            f"DB 断言失败[{compiled['schema_ref']}]: {compiled['table']} "
            f"期望 {expected} 条记录，实际 {len(rows)} 条（sql: {compiled['sql']}, params: {params}）")
    for a in compiled.get("asserts", []):
        want = a["value"]
        if a["mode"] == "var":
            if a["ref"] not in scenario_vars:
                raise AssertionError(f"场景变量未定义: {a['ref']}")
            want = scenario_vars[a["ref"]]
        row = rows[0]
        actual = row.get(a["field"]) if isinstance(row, dict) else row[a["field"]]
        if str(actual) != str(want):
            raise AssertionError(
                f"DB 断言失败[{compiled['schema_ref']}]: 字段 {a['field']} "
                f"期望 {want!r}，实际 {actual!r}")
```

- [ ] **Step 4: 运行测试确认通过**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/unit/test_db_assert_runtime.py tests/unit/test_vars_seed.py -v`
Expected: 全部通过（含原有动态值测试不回归）

- [ ] **Step 5: 提交**

```bash
git add tests/unit/test_db_assert_runtime.py lib/ui_profile.py
git commit -m "feat(ui): ui_profile.py 场景变量展开与 DB 断言执行器"
```

---

### Task 5: `generate_playwright.py` — 生成期校验 + db_asserts.py 产物

**Files:**
- Modify: `AgentTest-evalution/.opencode/skills/feature-to-playwright/scripts/generate_playwright.py`

- [ ] **Step 1: 修改 MODE_PATHS 与新增辅助函数**

在 `MODE_PATHS` 的 baseline/diff 中新增 `db_asserts` 键，并在 `import` 区加 `import yaml`、`from lib.db_asserts import ...`（需 `sys.path` 处理，见下）：

```python
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "lib"))

from db_asserts import (  # noqa: E402
    load_db_asserts, structural_errors, parse_schema_columns,
    compile_assert, validate_feature, build_module_source,
)
```

```python
MODE_PATHS = {
    "baseline": {
        "feature_dir": PROJECT_ROOT / "tests" / "baseline" / "_workflow" / "04-ui-scenarios",
        "output_dir": PROJECT_ROOT / "tests" / "baseline" / "generated" / "ui-test",
        "db_asserts": PROJECT_ROOT / "tests" / "baseline" / "_workflow" / "00-requirements" / "db-asserts.yaml",
    },
    "diff": {
        "feature_dir": PROJECT_ROOT / "tests" / "diff" / "_workflow" / "02-ui-scenarios",
        "output_dir": PROJECT_ROOT / "tests" / "diff" / "generated" / "ui-test",
        "db_asserts": PROJECT_ROOT / "tests" / "diff" / "_workflow" / "00-requirements" / "db-asserts.yaml",
    },
}
```

在 `slug_module` 后新增：

```python
def resolve_schema_path(config: dict):
    """从 config.yaml source.backend[].path 定位后端 db/schema.sql；找不到返回 None"""
    for be in config.get("source", {}).get("backend", []):
        root = Path(be.get("path", ""))
        cand = root / "db" / "schema.sql"
        if cand.exists():
            return cand
        for cand in root.rglob("schema.sql"):
            return cand
    return None


def validate_and_compile(db_asserts_path, schema_path, features):
    """生成期静态校验 + 编译。返回 (compiled_map, errors)：
    - db-asserts.yaml 缺失/空 → ({}, [])（跳过 DB 断言）
    - 有映射但 schema 缺失 → errors
    - 表/列/id/变量问题 → errors（含行号）
    """
    asserts = load_db_asserts(db_asserts_path)
    if not asserts:
        return {}, []
    if schema_path is None:
        return {}, ["db-asserts.yaml 存在但未找到后端 db/schema.sql（检查 config.yaml source.backend[].path）"]
    schema_columns = parse_schema_columns(schema_path.read_text(encoding="utf-8"))
    errors = list(structural_errors(asserts))
    for feature in features:
        errors.extend(validate_feature(feature.read_text(encoding="utf-8"), asserts, schema_columns))
    compiled = {}
    for rid, entry in asserts.items():
        try:
            compiled[rid] = compile_assert(entry, schema_columns)
        except ValueError as e:
            errors.append(str(e))
    return compiled, errors
```

- [ ] **Step 2: 修改 main() 集成校验与产物写入**

在 `features` 检查后、`output_dir.mkdir` 前插入；在 `print(f"[generate_playwright] 生成完成...")` 前插入：

```python
    # —— DB 断言：生成期静态校验 + 编译产物 ——
    db_asserts_path = Path(args.db_asserts) if args.db_asserts else mode_config["db_asserts"]
    config = {}
    config_path = PROJECT_ROOT / "config.yaml"
    if config_path.exists():
        try:
            config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        except Exception:
            config = {}
    compiled_map, errors = validate_and_compile(db_asserts_path, resolve_schema_path(config), features)
    if errors:
        print("[generate_playwright] DB 断言校验失败：")
        for e in errors:
            print(f"  [ERROR] {e}")
        sys.exit(1)
    if compiled_map:
        (output_dir / "db_asserts.py").write_text(
            build_module_source(compiled_map), encoding="utf-8")
        print(f"[generate_playwright] [OK] db_asserts.py 已生成（{len(compiled_map)} 条映射）")
    else:
        print("[generate_playwright] 未找到 db-asserts.yaml，跳过 DB 断言")
```

并在 `parser.add_argument` 区新增参数：

```python
    parser.add_argument("--db-asserts", default=None, help="db-asserts.yaml 路径（默认按 mode 决议）")
```

- [ ] **Step 3: 语法检查 + 全量生成自检**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m py_compile .opencode/skills/feature-to-playwright/scripts/generate_playwright.py`
Expected: 无输出（编译通过）

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe .opencode/skills/feature-to-playwright/scripts/generate_playwright.py --mode baseline`
Expected: 输出含 `未找到 db-asserts.yaml，跳过 DB 断言`，生成完成；`db_asserts.py` 不存在于输出目录

- [ ] **Step 4: 提交**

```bash
git add .opencode/skills/feature-to-playwright/scripts/generate_playwright.py
git commit -m "feat(ui): 生成器集成 DB 断言校验与 db_asserts.py 编译产物"
```

---

### Task 6: `template/conftest.py` — 场景变量 + DB 断言步骤

**Files:**
- Modify: `AgentTest-evalution/.opencode/skills/feature-to-playwright/template/conftest.py`

- [ ] **Step 1: 扩展 ui_profile 导入与兜底**

把模板第 44 行 `from ui_profile import ...` 改为：

```python
    from ui_profile import (
        load_profile, resolve_element, expand_vars, seed_protected,
        resolve_vars, run_db_assert,
    )
```

兜底块（第 46-56 行区域）追加：

```python
    def resolve_vars(v, s):
        return v

    def run_db_assert(*_a, **_k):
        raise AssertionError("ui_profile.py 缺少 run_db_assert（请重新生成测试目录）")
```

- [ ] **Step 2: 新增 DB 连接与步骤辅助（放在 `_retry_count` 之后）**

```python
# ═══════════════════════════════════════════════════════════════
# 场景变量 + DB 断言（db-asserts）
# ═══════════════════════════════════════════════════════════════


def _scenario_vars(request) -> dict:
    if request.node.stash.get("_scenario_vars") is None:
        request.node.stash["_scenario_vars"] = {}
    return request.node.stash["_scenario_vars"]


def _db_conn():
    if PROFILE is None:
        raise AssertionError("未配置 ui-profile/business.yaml 的 db 段，无法执行 DB 断言")
    db = PROFILE["business"].get("db") or {}
    if not db.get("database"):
        raise AssertionError("ui-profile/business.yaml 缺少 db.database 配置，无法执行 DB 断言")
    import pymysql
    return pymysql.connect(
        host=db.get("host", "localhost"),
        port=int(db.get("port", 3306)),
        user=db.get("user", "root"),
        password=db.get("password", ""),
        database=db["database"],
        charset=db.get("charset", "utf8mb4"),
        cursorclass=pymysql.cursors.DictCursor,
    )
```

- [ ] **Step 3: 新增 `令 $var = "..."` 与 `且数据已保存到 "<id>"` 步骤**

在 When 步骤区末尾（`fill_date` 之后）追加：

```python
@given(parsers.re(r'令 \$(\w+) = "([^"]*)"'))
@when(parsers.re(r'令 \$(\w+) = "([^"]*)"'))
def declare_scenario_var(request, var, value):
    _scenario_vars(request)[var] = expand_vars(value)


@then(parsers.parse('且数据已保存到 "{map_id}"'))
def db_assert_saved(request, map_id):
    try:
        from db_asserts import DB_ASSERT_MAP
    except ImportError:
        raise AssertionError(
            "未找到生成的 db_asserts.py（请重新运行 generate_playwright.py）") from None
    compiled = DB_ASSERT_MAP.get(map_id)
    if compiled is None:
        raise AssertionError(f"db_asserts.py 中不存在映射 id: {map_id}")
    conn = _db_conn()
    try:
        run_db_assert(conn, compiled, _scenario_vars(request))
    finally:
        conn.close()
```

- [ ] **Step 4: fill 步骤支持变量引用**

把 `fill_field` 与 `fill_date` 步骤函数改为注入 `request` 并先展开变量：

```python
@given(parsers.parse('在 "{field}" 输入框中输入 "{value}"'))
@when(parsers.parse('在 "{field}" 输入框中输入 "{value}"'))
def fill_field(page, request, field, value):
    _fill_input(page, field, expand_vars(resolve_vars(value, _scenario_vars(request))))


@when(parsers.parse('在 "{field}" 选择日期 "{value}"'))
def fill_date(page, request, field, value):
    _fill_input(page, field, expand_vars(resolve_vars(value, _scenario_vars(request))))
```

- [ ] **Step 5: 同步到已生成的测试目录并自检**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe .opencode/skills/feature-to-playwright/scripts/generate_playwright.py --mode baseline`
Expected: 生成完成（conftest.py 被覆盖为最新模板）

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/baseline/generated/ui-test --collect-only -q`
Expected: `collection succeeded` 无 `StepDefinitionNotFoundError`

- [ ] **Step 6: 提交**

```bash
git add .opencode/skills/feature-to-playwright/template/conftest.py
git commit -m "feat(ui): conftest 模板新增场景变量与 DB 断言步骤"
```

---

### Task 7: 配置层 — business.yaml db 段 + 环境检查 + 模板同步

**Files:**
- Modify: `AgentTest-evalution/ui-profile/business.yaml`
- Modify: `AgentTest-evalution/ui-profile-template/business.yaml`
- Create: `AgentTest-evalution/ui-profile-template/db-asserts.yaml`
- Modify: `AgentTest-evalution/scripts/check_ui_env.py`

- [ ] **Step 1: 确认后端 DB 账号并写入 business.yaml**

先读 `D:\AI评测\智能体评测平台\agent-evaluation-platform-backend\evaluation-platform-backend\src\main\resources\application-dev.yml` 的 `datasource` 段（username/password），然后向 `ui-profile/business.yaml` 末尾追加（值以读到的为准）：

```yaml
db:
  host: localhost
  port: 3306
  user: <application-dev.yml 的 username>
  password: <application-dev.yml 的 password>
  database: agent_evaluation
  charset: utf8mb4
```

- [ ] **Step 2: 同步模板 `ui-profile-template/business.yaml`**

追加（注释态，供新项目绑定参考）：

```yaml
# db:                    # DB 断言连接配置（阶段启用）
#   host: localhost
#   port: 3306
#   user: root
#   password: ""
#   database: <测试库名>
#   charset: utf8mb4
```

- [ ] **Step 3: 创建 `ui-profile-template/db-asserts.yaml` 模板**

```yaml
# db-asserts.yaml —— 操作→表→字段映射（AI 从需求文档 5 节模板翻译 + 人工确认）
# 约定：
#   - id：场景中 `且数据已保存到 "<id>"` 引用；生成器校验引用完整性
#   - table / where.field / assert_fields.field 必须存在于后端 schema.sql
#   - where 值来源：{ field, value: 固定值 } 或 { field, from: var, ref: $x }
#   - assert_fields 值来源：{ field, equals: 固定值 } 或 { field, from: var, ref: $x }
#   - where 禁止为空（防止全表断言）
db_asserts:
  # - id: BOOK_CREATE_001
  #   ui_action: 保存新增图书表单
  #   table: books
  #   expect_records: 1
  #   where:
  #     - { field: isbn, from: var, ref: $isbn }
  #   assert_fields:
  #     - { field: stock, equals: 0 }
  #   sync: { api: "POST /api/books", status: 200 }
  #   schema_ref: schema.sql#books
```

- [ ] **Step 4: `check_ui_env.py` 增加 pymysql 依赖检查**

把 `for dep in ("playwright", "pytest", "pytest-bdd", "pytest-playwright"):` 改为：

```python
    for dep in ("playwright", "pytest", "pytest-bdd", "pytest-playwright", "pymysql"):
```

同时把 `fix_hint` 列表追加 `f"{python} -m pip install pymysql"`。

- [ ] **Step 5: 验证环境检查**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe scripts/check_ui_env.py`
Expected: `dependencies.pymysql.installed = true`（若未安装，先 `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pip install pymysql` 再跑）

- [ ] **Step 6: 提交**

```bash
git add ui-profile/business.yaml ui-profile-template/business.yaml ui-profile-template/db-asserts.yaml scripts/check_ui_env.py
git commit -m "feat(ui): DB 断言配置层（business.yaml db 段 + 模板 + pymysql 环境检查）"
```

---

### Task 8: 文档 — gherkin-guide / SKILL.md / 需求文档模板

**Files:**
- Modify: `AgentTest-evalution/.opencode/skills/ui-scenario-design/references/gherkin-guide.md`
- Modify: `AgentTest-evalution/.opencode/skills/ui-scenario-design/SKILL.md`
- Modify: `AgentTest-evalution/.opencode/skills/feature-to-playwright/SKILL.md`
- Create: `AgentTest-evalution/tests/baseline/_workflow/00-requirements/ui-requirements-TEMPLATE.md`

- [ ] **Step 1: gherkin-guide.md 追加 DSL 说明**

在「场景结构模板」代码块后新增小节：

```markdown
## 场景变量与 DB 断言（防假成功）

关键写操作（创建/编辑/删除）除 UI 提示断言外，用场景变量 + DB 断言证明数据真实落库：

```gherkin
Scenario: create book
  Given 打开首页
  When 点击按钮 "新增图书"
  And 令 $isbn = "978-7-111-${ts}"
  And 在 "如 978-7-111-12345-8" 输入框中输入 "$isbn"
  And 点击按钮 "保存"
  Then 应看到提示 "新增成功"
  And 且数据已保存到 "BOOK_CREATE_001"
```

| 元素 | 示例 | 说明 |
|------|------|------|
| 场景变量 | `令 $isbn = "978-7-111-${ts}"` | 声明变量（值可含 `${ts}` 动态值，声明时展开）；仅当前 Scenario 作用域 |
| 值引用 | `在 "..." 输入框中输入 "$isbn"` | 输入/日期步骤支持 `$变量` 引用；`${...}` 与 `$.answer` 不受影响 |
| DB 断言 | `且数据已保存到 "BOOK_CREATE_001"` | 映射 id 来自 db-asserts.yaml；生成器校验 id/表/列/变量 |

规则：
1. **先声明后使用**（生成器会校验，违反则生成中止）
2. 映射由 AI 从需求文档「数据变更映射」表翻译 + 测试工程师确认，业务不写 yaml
3. 断言时机：操作步骤已完成 busy + API 同步（api_sync_rules）后自动查库
4. 需求文档无映射的操作 → 不用 DB 断言，保持 UI 提示断言
```

- [ ] **Step 2: ui-scenario-design/SKILL.md 补充产物与流程**

在「输出」区追加：

```markdown
- 00-requirements/db-asserts.yaml（可选，AI 从需求文档「数据变更映射」表翻译 + 测试工程师确认；
  场景关键写操作引用其 id；无映射时省略）
```

在「设计流程」第 5 步后追加：

```markdown
6. **翻译数据映射**：需求文档若有「数据变更映射」表，AI 对照后端 `db/schema.sql` 校验表/列存在性后产出 `00-requirements/db-asserts.yaml` 草稿，输出「业务命名 vs 物理命名」差异表；对不上时**不静默猜测**，由人工裁决后确认入库
```

- [ ] **Step 3: feature-to-playwright/SKILL.md 补充生成行为**

在「执行」区后追加小节：

```markdown
## DB 断言生成（防假成功）

- 输入：`00-requirements/db-asserts.yaml`（缺失/为空则跳过，不影响现有场景）
- 生成期静态校验（任一失败 → 中止）：映射 id 必须存在；表/列必须存在于后端 `db/schema.sql`；场景变量必须先声明后使用
- 产物：`${OUTPUT_DIR}/db_asserts.py`（编译后的 DB_ASSERT_MAP，含 SQL 常量），运行期由 `且数据已保存到 "<id>"` 步骤查库断言
- 禁止在场景/脚本中手写物理表名与 SQL（统一走生成器编译）
```

- [ ] **Step 4: 创建需求文档模板**

```markdown
# UI 测试需求文档

## 1. 模块与版本
| 模块名 | 版本 | 业务负责人 | 日期 |
|--------|------|-----------|------|

## 2. 业务流程（叙述，每流程一段）
[业务用自然语言描述用户操作路径与预期结果]

## 3. 数据变更映射（必填）
| 业务操作 | 涉及表（业务命名） | 变更类型 | 数据变化描述 | 关键字段与取值 |
|---------|------------------|---------|-------------|---------------|
| 新增图书 | 图书表 | 新增 | 新增 1 条记录 | 标题=表单"书名"；库存=0；状态=启用 |
| 借出图书 | 图书表 / 借阅表 | 修改+新增 | 图书表库存-1；借阅表+1 条 | 库存=原值-1；借阅状态=进行中 |

## 4. 字段明细（复杂场景补充）
- 图书表
  - `标题`：来自表单"书名"输入框，新增必填
  - `库存`：新增初始 0；借出时减 1
  - `状态`：枚举{启用,停用}

## 5. 数据约束（可选）
- 唯一约束：图书编码不可重复
- 种子依赖：删除需先停用（复用已有种子数据）
```

- [ ] **Step 5: 提交**

```bash
git add .opencode/skills/ui-scenario-design/references/gherkin-guide.md .opencode/skills/ui-scenario-design/SKILL.md .opencode/skills/feature-to-playwright/SKILL.md tests/baseline/_workflow/00-requirements/ui-requirements-TEMPLATE.md
git commit -m "docs(ui): DB 断言 DSL/流程文档与需求文档 5 节模板"
```

---

### Task 9: 演示落地 — create agent 场景接入 DB 断言（端到端验证）

**Files:**
- Create: `AgentTest-evalution/tests/baseline/_workflow/00-requirements/db-asserts.yaml`
- Modify: `AgentTest-evalution/tests/baseline/_workflow/04-ui-scenarios/02-agent-projects.feature`

- [ ] **Step 1: 创建 db-asserts.yaml（AI 从需求翻译 + 人工确认的示例）**

```yaml
# 来源: ui-requirements.md「数据变更映射」→ agent_config（schema.sql#agent_config）
# 确认: 业务命名「智能体配置表」= 物理表 agent_config；「编码/名称」= agent_code/agent_name
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
```

- [ ] **Step 2: 改造 create agent 场景使用场景变量 + DB 断言**

`02-agent-projects.feature` 的 `Scenario: create agent` 改为（其余场景不动）：

```gherkin
  Scenario: create agent
    Given 打开首页
    When 点击链接 "评测项目"
    When 点击按钮 "新增智能体"
    And 令 $code = "AGT_UI_${ts}"
    And 令 $name = "UI测试智能体_${ts}"
    And 在 "智能体编码" 输入框中输入 "$code"
    And 在 "请输入智能体名称" 输入框中输入 "$name"
    And 在 "例如：CUSTOMER_SERVICE" 输入框中输入 "TEST"
    And 选择下拉框 "风险等级" 的选项 "较低风险等级 D（D）"
    And 在 "请输入所属部门" 输入框中输入 "测试部"
    And 在 "例如：1.0.0" 输入框中输入 "1.0.0"
    And 在 "例如：CHAT" 输入框中输入 "CHAT"
    And 选择下拉框 "适配器类型" 的选项 "通用 HTTP JSON（GENERIC_HTTP_JSON）"
    And 选择下拉框 "HTTP 方法" 的选项 "POST"
    And 在 "https://host/path" 输入框中输入 "http://localhost:8080/mock"
    And 在 "100 - 120000" 输入框中输入 "60000"
    And 在 "$.answer" 输入框中输入 "$.answer"
    And 点击按钮 "保存"
    Then 应看到提示 "智能体已新增"
    And 页面应包含 "UI测试智能体"
    And 且数据已保存到 "AGENT_CREATE_001"
```

> 注意：`And 令 $code = ...` 继承 When 关键字（前一行是 When），模板已注册 given/when 双形态；`$.answer` 不触发变量校验（设计验证过）。

- [ ] **Step 3: 重新生成 + 自检（生成期校验应通过）**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe .opencode/skills/feature-to-playwright/scripts/generate_playwright.py --mode baseline`
Expected: 输出含 `[OK] db_asserts.py 已生成（1 条映射）`

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/baseline/generated/ui-test --collect-only -q`
Expected: `collection succeeded`，且 `db_asserts.py` 存在于 `tests/baseline/generated/ui-test/`

- [ ] **Step 4: 校验失败路径（可选抽查）：临时改错映射 id 应中止**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe .opencode/skills/feature-to-playwright/scripts/generate_playwright.py --mode baseline --db-asserts <不存在的路径>`
Expected: 跳过 DB 断言（不报错）；恢复后重新生成一次

- [ ] **Step 5: 运行 create agent 场景（需前端 localhost:5173 + MySQL 就绪）**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/baseline/generated/ui-test/test_agent-projects.py -k "create_agent and not missing" -v`
Expected: PASS（`DB 断言`步骤通过说明 `agent_config` 表确有 `agent_code=$code` 且 `agent_name=$name`、`enabled=1` 的记录）

- [ ] **Step 6: 提交**

```bash
git add tests/baseline/_workflow/00-requirements/db-asserts.yaml tests/baseline/_workflow/04-ui-scenarios/02-agent-projects.feature tests/baseline/generated/ui-test/
git commit -m "feat(ui): create agent 场景接入 DB 断言（AGENT_CREATE_001 演示落地）"
```

---

## 自检

**1. Spec 覆盖：**
- 四、需求模板 → Task 8 Step 4
- 五、db-asserts.yaml + 校验 → Task 1/2/7 Step 3
- 六、DSL（变量/引用/值引用）→ Task 3/4/6
- 七、生成器编译 + 静态校验 → Task 2（compile）+ Task 5
- 八、断言时机（busy+API 同步后查）→ 复用现有 `_click_enabled_with_sync`/`_wait_busy_gone`，Task 6 无重复实现
- 九、失败追溯（映射 id + schema_ref）→ `run_db_assert` 错误信息
- 十、人工确认模型 → Task 9 Step 1 注释 + Task 8 Step 2（AI 翻译 + 人工确认）
- 降级链（无映射 → 跳过）→ Task 5 `validate_and_compile` 空返回

**2. 占位符扫描：** 无 TBD/TODO；Task 7 Step 1 的 `<application-dev.yml 的 username>` 是执行期读取的动作指令（含明确读取命令），非占位。

**3. 类型一致性：** `compile_assert` 产出的 params/asserts 结构与 `run_db_assert` 消费的字段（key/mode/ref/value、field）一致；`build_module_source` 产出 `DB_ASSERT_MAP` 与 conftest `from db_asserts import DB_ASSERT_MAP` 一致；`VALID_YAML` 在 Task 1 定义、Task 2/3 复用（同文件追加）；`SCHEMA_SAMPLE` 在 Task 2 定义、Task 3 复用；Task 2 Step 1 注释明确 `risk_tier` 需补列（`test_compile_assert_literal_where` 依赖）。

**4. 与现有设施兼容：** `$.answer` 输入不触发变量校验（`_VAR_USE_RE` 排除）；`${ts}` 动态值在声明时展开一次；未声明变量保持原文不静默报错于 UI 步骤（DB 断言缺失变量才报错）。