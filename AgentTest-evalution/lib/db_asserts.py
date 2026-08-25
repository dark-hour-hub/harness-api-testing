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
        if not entry.get("where"):
            errors.append(f"映射 {rid}: where 条件为空（禁止全表断言）")
        if "assert_fields" not in entry:
            errors.append(f"映射 {rid}: 缺少必填键 assert_fields")
        if "schema_ref" not in entry:
            errors.append(f"映射 {rid}: 缺少必填键 schema_ref（建议形如 schema.sql#表名）")
    return errors


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
        if a.get("not_null"):
            assert_items.append({"field": field, "mode": "not_null", "ref": None, "value": None})
        else:
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