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

from pathlib import Path
from typing import Optional

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