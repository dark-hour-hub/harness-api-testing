# -*- coding: utf-8 -*-
"""
ui_profile.py — ui-profile 配置加载与元素定位解析（确定性执行层）

职责：
- 加载 ui-profile/ 目录（elements.yaml + business.yaml）
- 按策略链解析元素 → Playwright locator（按序尝试，命中即止）
- 供 generated/ui-test/conftest.py（副本）与单元测试共用

依赖：pyyaml；playwright 仅在 resolve_element 的 page 参数上鸭子类型使用，
加载层本身不依赖浏览器。
"""
from __future__ import annotations

import datetime
import fnmatch
from pathlib import Path
import random
import re
import string
from typing import Optional
import uuid

import yaml


class ElementMap:
    """元素地图：文案即 key → 定位策略链"""

    def __init__(self, elements: Optional[dict] = None):
        self.elements = elements or {}

    @classmethod
    def load(cls, path: Path) -> "ElementMap":
        if not path.exists():
            return cls()
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return cls(elements=data.get("elements"))

    def lookup(self, key: str) -> Optional[dict]:
        """按业务文案查元素定义；未命中返回 None"""
        return self.elements.get(key)


def load_profile(profile_dir: Path) -> dict:
    """加载 profile 目录，返回 {"map": ElementMap, "business": dict}。

    文件缺失时返回空 map / 空 business，保证最小绑定也能跑（回退文本直搜）。
    """
    profile_dir = Path(profile_dir)
    element_map = ElementMap.load(profile_dir / "elements.yaml")
    business: dict = {}
    business_path = profile_dir / "business.yaml"
    if business_path.exists():
        with open(business_path, "r", encoding="utf-8") as f:
            business = yaml.safe_load(f) or {}
    return {"map": element_map, "business": business}


def _build_locator(page, strategy: dict):
    """按策略类型构造 locator；未知类型返回 None。

    兼容两种 YAML 写法：
    - 嵌套：{ type: role, value: { role: textbox, name: "xx" } }
    - 扁平：{ type: role, role: textbox, name: "xx" } / { type: combobox, name: "xx" }
    """
    stype = strategy.get("type")
    value = strategy.get("value")
    if stype == "data-testid":
        return page.get_by_test_id(value)
    if stype == "placeholder":
        return page.get_by_placeholder(value)
    if stype == "label":
        return page.get_by_label(value)
    if stype == "role":
        if isinstance(value, dict):
            return page.get_by_role(value.get("role", "button"), name=value.get("name"))
        return page.get_by_role(strategy.get("role", "button"), name=strategy.get("name"))
    if stype == "combobox":
        name = value if isinstance(value, str) else strategy.get("name")
        return page.get_by_role("combobox", name=name)
    if stype == "css":
        return page.locator(value)
    if stype == "text":
        return page.get_by_text(value)
    return None


def resolve_element(page, element_def: dict, timeout_ms: int = 5000):
    """按策略链解析元素（确定性：按序尝试，命中即止）。

    返回 (locator, strategy_index)：命中返回首个 attach 成功的 locator 与策略序号；
    全部失败返回 (None, -1)。
    """
    for idx, strategy in enumerate(element_def.get("strategies", [])):
        locator = _build_locator(page, strategy)
        if locator is None:
            continue
        try:
            locator.first.wait_for(state="attached", timeout=timeout_ms)
            return locator, idx
        except Exception:
            continue
    return None, -1


_VAR_RE = re.compile(r"\$\{(rand|uuid|ts|date)(?::([^}]*))?\}")


def expand_vars(value, base_time=None):
    """场景值中的动态值占位符展开（确定性执行层）：

    - ${rand:8}    N 位随机大写字母数字（默认 8）
    - ${uuid}      UUID 前 12 位大写（去连字符）
    - ${ts}        13 位毫秒时间戳
    - ${date:+Nd}  相对日期 yyyy-MM-dd（+N/-N 天，可省略）
    """
    if not isinstance(value, str):
        return value
    base = base_time or datetime.datetime.now()

    def _repl(m):
        kind, arg = m.group(1), m.group(2)
        if kind == "rand":
            n = int(arg) if arg and arg.isdigit() else 8
            return "".join(random.choices(string.ascii_uppercase + string.digits, k=n))
        if kind == "uuid":
            return str(uuid.uuid4()).replace("-", "")[:12].upper()
        if kind == "ts":
            return str(int(base.timestamp() * 1000))
        if kind == "date":
            days = 0
            if arg and arg[0] in "+-" and arg[1:].rstrip("dD").isdigit():
                days = int(arg.rstrip("dD"))
            return (base + datetime.timedelta(days=days)).strftime("%Y-%m-%d")
        return m.group(0)

    return _VAR_RE.sub(_repl, value)


def seed_protected(value, protected_seeds):
    """值命中种子保护清单（支持 fnmatch 通配）→ True"""
    if not protected_seeds or not isinstance(value, str):
        return False
    return any(fnmatch.fnmatch(value, p) or value == p for p in protected_seeds)