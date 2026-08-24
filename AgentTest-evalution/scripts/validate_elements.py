# -*- coding: utf-8 -*-
"""
validate_elements.py — 校验 ui-profile/elements.yaml 结构与策略类型

供 ui-element-map skill 生成后与人工确认前调用；返回错误清单（空 = 通过）。
"""
from pathlib import Path

import yaml
from yaml.constructor import ConstructorError

KNOWN_TYPES = {"data-testid", "placeholder", "label", "role", "combobox", "css", "text"}


class _DuplicateKeyError(ConstructorError):
    """标记 YAML 映射重复 key，区别于其它构造错误（如未知 tag）。"""


def _construct_mapping_no_duplicate(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise _DuplicateKeyError(
                "while constructing a mapping",
                node.start_mark,
                str(key),
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


class _NoDuplicateSafeLoader(yaml.SafeLoader):
    pass


_NoDuplicateSafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping_no_duplicate,
)


def validate(path: Path) -> list:
    """返回错误信息列表；文件不存在返回空（最小绑定合法）。"""
    path = Path(path)
    if not path.exists():
        return []
    errors = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=_NoDuplicateSafeLoader) or {}
    except _DuplicateKeyError as e:
        return [f"元素 key 重复: {e.problem}"]
    except yaml.YAMLError as e:
        return [f"YAML 解析失败: {e}"]

    elements = data.get("elements") or {}
    for key, entry in elements.items():
        if not key or not str(key).strip():
            errors.append("存在空 key")
        strategies = (entry or {}).get("strategies") or []
        if not strategies:
            errors.append(f"元素「{key}」无 strategies")
        for s in strategies:
            stype = s.get("type")
            if stype not in KNOWN_TYPES:
                errors.append(f"元素「{key}」未知策略类型: {stype}")
            if stype == "role" and not s.get("name"):
                errors.append(f"元素「{key}」role 策略缺 name")
    return errors


if __name__ == "__main__":
    import sys
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "ui-profile" / "elements.yaml"
    if not target.exists():
        print(f"[validate_elements] 目标不存在: {target}")
        sys.exit(1)
    errs = validate(target)
    if errs:
        print(f"[validate_elements] 校验失败: {target}")
        for e in errs:
            print(f"  - {e}")
        sys.exit(1)
    print(f"[validate_elements] 校验通过: {target}")
