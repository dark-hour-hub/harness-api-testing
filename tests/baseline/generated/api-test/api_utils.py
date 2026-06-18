"""
api_utils.py — API 请求工具类和通用辅助函数
"""
import time
import re
import requests
from pathlib import Path
from conftest import PROJECT_ROOT, load_yaml, resolve_variables, test_context_vars


def load_testcases(yaml_path: str, tags: list = None) -> list:
    """从 YAML 文件加载测试用例，可选按标签筛选

    Args:
        yaml_path: YAML 文件相对于项目根目录的路径
        tags: 筛选标签列表，None 表示全部加载

    Returns:
        测试用例列表，每项包含 YAML 中定义的完整字段
    """
    data = load_yaml(yaml_path)
    cases = data.get("testcases", [])
    if tags:
        cases = [c for c in cases if any(t in c.get("tags", []) for t in tags)]
    return cases


def build_request(case: dict, context: dict) -> dict:
    """根据用例构造 requests 参数

    Returns:
        {"method": "GET", "url": "http://...", ...}
    """
    req = case["request"]
    return {
        "method": req["method"],
        "url": resolve_variables(req["path"], context),
        "headers": resolve_variables(req.get("headers", {}), context),
        "params": resolve_variables(req.get("params", {}), context),
        "json": resolve_variables(req.get("body"), context) if req.get("body") else None,
    }


def _eval_assert_expr(expr: str, response: requests.Response, context: dict):
    """求值断言表达式，如 "response.status_code" 或 "response.json()['data']['id']"

    支持的路径前缀:
        response.status_code          → HTTP 状态码
        response.json()['key']...     → JSON body 路径
    """
    if expr.startswith("response.status_code"):
        return response.status_code

    if expr.startswith("response.json()"):
        path_match = re.findall(r"\[['\"]([^'\"]+)['\"]\]", expr)
        val = response.json()
        for key in path_match:
            if isinstance(val, dict):
                val = val.get(key)
            else:
                raise KeyError(f"Cannot access '{key}' on {type(val)}")
        return val

    return resolve_variables(expr, context)


def execute_assertions(response, case: dict, context: dict):
    """执行 YAML 用例中定义的所有断言

    断言分层（参考 .claude/rules/testPoint-interface.md）：
    1. 协议层 — HTTP 状态码
    2. 业务层 — business_code (response.json()['code'])
    3. 数据层 — message / data 字段

    支持的断言表达式：
        assert_equal      — 严格相等
        assert_not_equal  — 不相等
        assert_exists     — JSON 路径存在
        assert_not_empty  — 值非空（truthy）
        assert_contains   — 字符串包含
        assert_in         — 值在列表中
        assert_is_type    — 类型检查
    """
    import pytest as _pytest

    assertions = case.get("assertions", [])
    for item in assertions:
        for assert_type, args in item.items():
            if assert_type == "description":
                continue

            desc = item.get("description", f"{assert_type}: {args}")

            if assert_type == "assert_equal":
                left = _eval_assert_expr(args[0], response, context)
                right = resolve_variables(args[1], context)
                assert left == right, f"[{desc}] 期望 {right!r}, 实际 {left!r}"

            elif assert_type == "assert_not_equal":
                left = _eval_assert_expr(args[0], response, context)
                right = resolve_variables(args[1], context)
                assert left != right, f"[{desc}] 期望不等于 {right!r}, 实际 {left!r}"

            elif assert_type == "assert_exists":
                try:
                    _eval_assert_expr(args[0], response, context)
                except (KeyError, IndexError, TypeError):
                    _pytest.fail(f"[{desc}] 字段不存在: {args[0]}")

            elif assert_type == "assert_not_empty":
                val = _eval_assert_expr(args[0], response, context)
                assert val, f"[{desc}] 值为空: {args[0]}"

            elif assert_type == "assert_contains":
                haystack = _eval_assert_expr(args[0], response, context)
                needle = resolve_variables(args[1], context)
                assert needle in str(haystack), f"[{desc}] '{needle}' 不在 '{haystack}' 中"

            elif assert_type == "assert_in":
                val = _eval_assert_expr(args[0], response, context)
                expected_list = args[1]
                assert val in expected_list, f"[{desc}] {val!r} 不在 {expected_list}"

            elif assert_type == "assert_is_type":
                val = _eval_assert_expr(args[0], response, context)
                type_map = {
                    "str": str, "string": str,
                    "int": int, "integer": int,
                    "list": list, "array": list,
                    "dict": dict, "object": dict,
                    "bool": bool, "float": float,
                }
                expected = type_map.get(args[1], args[1])
                assert isinstance(val, expected), f"[{desc}] 类型不匹配: 期望 {expected}, 实际 {type(val)}"


def sort_cases_by_execution_order(cases: list) -> list:
    """按 execution_order 排序用例：cleanup 用例排在最后，其余保持原序"""
    normal = [c for c in cases if c.get("execution_order") != "cleanup"]
    cleanup = [c for c in cases if c.get("execution_order") == "cleanup"]
    return normal + cleanup


def get_token(base_url: str, username: str, password: str) -> str:
    """获取认证 Token"""
    resp = requests.post(
        f"{base_url}/admin/login",
        json={"username": username, "password": password},
        timeout=30,
    )
    assert resp.status_code == 200, f"获取Token失败 HTTP {resp.status_code}"
    body = resp.json()
    assert body.get("code") == 200, f"获取Token失败: {body.get('message')}"
    return body["data"]["token"]
