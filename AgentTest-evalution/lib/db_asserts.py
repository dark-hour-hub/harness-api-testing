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