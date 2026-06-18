"""
ums 模块 API 测试 — 用户管理系统
从 ums-testcases.yaml 读取用例数据，运行时动态执行

生成时间: 2026-06-18T10:00:00
模块标识: ums
"""
import pytest
import requests
import time
from api_utils import (
    load_testcases, build_request, execute_assertions,
    sort_cases_by_execution_order,
)
from conftest import resolve_variables, test_context_vars

# ============================================================
# 测试数据加载
# ============================================================

YAML_FILE = "tests/baseline/_workflow/02-analysis-plan/testcases/ums-testcases.yaml"

# 加载本模块所有用例并按 execution_order 排序
ALL_CASES = sort_cases_by_execution_order(
    load_testcases(YAML_FILE)
)


# ============================================================
# 按标签筛选的用例分组（用于选择性运行）
# ============================================================

SMOKE_CASES = [c for c in ALL_CASES if "smoke" in c.get("tags", [])]
P0_CASES = [c for c in ALL_CASES if c.get("priority") == "P0"]
P1_CASES = [c for c in ALL_CASES if c.get("priority") == "P1"]
POSITIVE_CASES = [c for c in ALL_CASES if "positive" in c.get("tags", [])]
NEGATIVE_CASES = [c for c in ALL_CASES if "negative" in c.get("tags", [])]


def _resolve_expected_response(case: dict, context: dict) -> dict:
    """解析预期响应中的变量引用，处理 'exists_and_type: <type>' 标记"""
    expected = case.get("expected_response", {}).copy()

    for key, value in expected.items():
        if key in ("http_status", "business_code"):
            continue
        if isinstance(value, str) and value.startswith("exists_and_type:"):
            expected[key] = value
        elif isinstance(value, dict):
            expected[key] = resolve_variables(value, context)
        elif isinstance(value, str):
            expected[key] = resolve_variables(value, context)

    return expected


# ============================================================
# 测试执行
# ============================================================

@pytest.mark.parametrize("case", ALL_CASES, ids=[c["id"] for c in ALL_CASES])
def test_case(api_session: requests.Session, base_url: str, case: dict, test_context: dict):
    """通用测试执行器，数据驱动：从 YAML 用例读取请求和断言

    流程:
    1. 解析变量引用 (${...})
    2. 构造 HTTP 请求
    3. 发送请求
    4. 执行分层断言
    5. 将产生的变量写入 test_context_vars 供后续 cleanup 用例引用
    """
    # 合并全局上下文变量与当前测试上下文
    context = {**test_context, **test_context_vars}

    # 重新解析 timestamp（每次执行使用新的时间戳）
    context["timestamp"] = str(int(time.time()))

    # 解析请求参数中的变量
    req_kwargs = build_request(case, context)

    # 构造完整 URL
    url = base_url.rstrip("/") + "/" + req_kwargs["url"].lstrip("/")
    method = req_kwargs["method"].upper()

    # 构建请求头（合并 api_session 默认头和用例指定头）
    headers = {**api_session.headers}
    if req_kwargs.get("headers"):
        headers.update(req_kwargs["headers"])
    api_session.headers.update(headers)

    # 发送请求
    try:
        response = api_session.request(
            method=method,
            url=url,
            params=req_kwargs.get("params"),
            json=req_kwargs.get("json"),
            timeout=30,
        )
    except requests.exceptions.Timeout:
        pytest.fail(f"[{case['id']}] 请求超时: {method} {url}")
    except requests.exceptions.ConnectionError:
        pytest.fail(f"[{case['id']}] 无法连接后端服务: {base_url}")

    # 执行分层断言
    execute_assertions(response, case, context)

    # 如果用例标记了 produces，将产生的变量写入全局上下文
    produces = case.get("produces", {})
    for var_name, expr in produces.items():
        if expr.startswith("response.json()"):
            import re
            path_match = re.findall(r"\[['\"]([^'\"]+)['\"]\]", expr)
            val = response.json()
            for key in path_match:
                if isinstance(val, dict):
                    val = val.get(key)
            test_context_vars[var_name] = val


# ============================================================
# Smoke 测试快捷入口
# ============================================================

@pytest.mark.smoke
@pytest.mark.parametrize("case", SMOKE_CASES, ids=[c["id"] for c in SMOKE_CASES])
def test_smoke(api_session: requests.Session, base_url: str, case: dict, test_context: dict):
    """冒烟测试：仅执行标记 smoke 的用例"""
    test_case(api_session, base_url, case, test_context)
