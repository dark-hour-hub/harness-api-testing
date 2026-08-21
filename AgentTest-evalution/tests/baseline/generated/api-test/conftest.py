"""
conftest.py — 由 yaml-to-pytest skill 自动生成，请勿手动修改

提供所有测试文件共享的基础设施：
- 变量解析（${auth.xxx} / ${global_variables.xxx} / ${TC_XXX.extracts.xxx}）
- JSONPath 提取
- 请求头构建
- HTTP 请求执行 + 断言
- Fixtures: module_context, auth_values, request_helper
"""
import pytest
import requests
import re
import json


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """把用例实际响应报文写入 junit property，供报告展示"""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        rh = getattr(item, "funcargs", {}).get("request_helper", None)
        last = getattr(rh, "last_response", None)
        if last:
            payload = json.dumps(last, ensure_ascii=False)
            item.user_properties.append(("api_response", payload[:4000]))


# ═══════════════════════════════════════════════════════════════
# 变量解析引擎
# ═══════════════════════════════════════════════════════════════

VAR_REF = re.compile(r"\$\{([^}]+)\}")


class ModuleContext:
    """模块级共享上下文，存储用例 extracts 结果供跨用例引用"""

    def __init__(self):
        self.vars = {}  # {case_id: {key: value}}


def _dig(data, path_parts):
    """沿路径从嵌套字典中取值"""
    cur = data
    for p in path_parts:
        if isinstance(cur, dict):
            cur = cur.get(p)
        else:
            return None
    return cur


def _resolve_auth_ref(parts, auth_setup, auth_values, ctx):
    """解析 ${auth.xxx.yyy} 引用，支持 extracts 跳过规则"""
    first = parts[0]

    # ── 单层引用: ${auth.xxx} ──
    if len(parts) == 1:
        if first == "token_prefix":
            return str(auth_setup.get("token_prefix", ""))

        # 从 auto-login 结果取
        if first in auth_values and auth_values[first] is not None:
            return str(auth_values[first])

        # 从 module_context.__auth__ 取（测试用例登录提取的 token）
        auth_ctx = ctx.vars.get("__auth__", {})
        if first in auth_ctx:
            return str(auth_ctx[first])

        # 从 auth_setup.params 顶层取（非 dict 值）
        params = auth_setup.get("params", {})
        if first in params and not isinstance(params[first], dict):
            return str(params[first])

        # 从 auth_setup 顶层取（非容器字段）
        if first in auth_setup and first not in (
            "params", "accounts", "extracts", "type", "login_endpoint", "token_prefix"
        ):
            val = auth_setup[first]
            return str(val) if not isinstance(val, dict) else ""

        return ""

    # ── 多层级引用 ──
    if first == "params":
        cur = auth_setup.get("params", {})
    elif first == "accounts":
        cur = auth_setup.get("accounts", {})
    elif first == "extracts":
        # 跳过 extracts 层级: ${auth.extracts.token} → 直接从 auth_values 或 __auth__ 取
        if len(parts) >= 2:
            key = parts[1]
            if key in auth_values and auth_values[key] is not None:
                return str(auth_values[key])
            auth_ctx = ctx.vars.get("__auth__", {})
            if key in auth_ctx:
                return str(auth_ctx[key])
        return ""
    elif first in auth_setup:
        cur = auth_setup[first]
        if not isinstance(cur, dict):
            return str(cur)
    else:
        return ""

    for p in parts[1:]:
        if isinstance(cur, dict):
            cur = cur.get(p)
        else:
            return ""
    return str(cur) if cur is not None and not isinstance(cur, dict) else ""


def _resolve_case_ref(parts, ctx):
    """解析 ${TC_XXX.extracts.xxx} 跨用例引用；无法解析时返回哨兵供依赖中断检测"""
    if len(parts) >= 2 and parts[1] == "extracts":
        case_id = parts[0]
        var_name = parts[2] if len(parts) >= 3 else ""
        val = ctx.vars.get(case_id, {}).get(var_name)
        if val is not None:
            return str(val)
        return f"__UNRESOLVED_DEP:{case_id}:{var_name}__"
    return ""


def _resolve_single_ref(ref, auth_setup, auth_values, global_vars, ctx):
    """解析单个 ${...} 引用"""
    parts = ref.split(".")
    root = parts[0]

    if root == "auth":
        return _resolve_auth_ref(parts[1:], auth_setup, auth_values, ctx)
    elif root == "global_variables":
        val = _dig(global_vars, parts[1:])
        return str(val) if val is not None else ""
    elif root.startswith("TC_"):
        return _resolve_case_ref(parts, ctx)

    return "${" + ref + "}"


def resolve_vars(value, auth_setup, auth_values, global_vars, ctx):
    """递归解析值中的 ${...} 变量引用"""
    if isinstance(value, str):
        # 整个字符串是单个引用 → 保留原始类型（数字、布尔等）
        m = VAR_REF.fullmatch(value)
        if m:
            result = _resolve_single_ref(m.group(1), auth_setup, auth_values, global_vars, ctx)
            # 尝试转换数字
            if result.isdigit() and not result.startswith("0"):
                return int(result)
            return result
        return VAR_REF.sub(
            lambda m: _resolve_single_ref(m.group(1), auth_setup, auth_values, global_vars, ctx),
            value,
        )
    elif isinstance(value, dict):
        return {k: resolve_vars(v, auth_setup, auth_values, global_vars, ctx) for k, v in value.items()}
    elif isinstance(value, list):
        return [resolve_vars(v, auth_setup, auth_values, global_vars, ctx) for v in value]
    return value


# ═══════════════════════════════════════════════════════════════
# JSONPath 提取
# ═══════════════════════════════════════════════════════════════

def jsonpath_extract(data, expr):
    """简单的 JSONPath 提取，支持 $.data.xxx 和 $.data.list[0].xxx"""
    if not expr or not expr.startswith("$"):
        return None
    path = expr.lstrip("$").lstrip(".")
    if not path:
        return data
    cur = data
    for seg in path.split("."):
        if not seg or cur is None:
            continue
        if "[" in seg:
            key, rest = seg.split("[", 1)
            idx_str = rest.rstrip("]")
            if key:
                cur = cur.get(key) if isinstance(cur, dict) else None
            if cur is not None and isinstance(cur, list):
                try:
                    cur = cur[int(idx_str)]
                except (ValueError, IndexError):
                    return None
        else:
            cur = cur.get(seg) if isinstance(cur, dict) else None
    return cur


# ═══════════════════════════════════════════════════════════════
# 请求头构建
# ═══════════════════════════════════════════════════════════════

def build_headers(case, auth_setup, auth_values, global_vars, ctx, public_tmpl, auth_tmpl):
    """构建最终请求头: public + auth(如需) + case 特有，后覆盖前"""
    headers = {}

    for h in public_tmpl:
        name = resolve_vars(h.get("name", ""), auth_setup, auth_values, global_vars, ctx)
        value = resolve_vars(h.get("value", ""), auth_setup, auth_values, global_vars, ctx)
        if name:
            headers[name] = value

    if case.get("auth", {}).get("required"):
        for h in auth_tmpl:
            name = resolve_vars(h.get("name", ""), auth_setup, auth_values, global_vars, ctx)
            value = resolve_vars(h.get("value", ""), auth_setup, auth_values, global_vars, ctx)
            if name:
                headers[name] = value

    for h in case.get("request", {}).get("headers", []):
        name = resolve_vars(h.get("name", ""), auth_setup, auth_values, global_vars, ctx)
        value = resolve_vars(h.get("value", ""), auth_setup, auth_values, global_vars, ctx)
        if name:
            headers[name] = value

    return headers


# ═══════════════════════════════════════════════════════════════
# 认证
# ═══════════════════════════════════════════════════════════════

def _find_login_body_template(module_data, auth_setup, yaml_dir=None):
    """在模块的 testcases 中找匹配 login_endpoint 的 POST 用例作为登录请求体模板。
    如果当前模块没有，则搜索同目录下的其他 YAML 文件。"""
    login_path = auth_setup.get("login_endpoint", "")
    if not login_path:
        return None

    # 先查当前模块
    for tc in module_data.get("testcases", []):
        if tc.get("path") == login_path and tc.get("method") == "POST":
            return tc.get("request", {}).get("body", {})

    # 再查同目录下其他 YAML 文件
    if yaml_dir and yaml_dir.exists():
        import yaml as _yaml
        for yf in sorted(yaml_dir.glob("*.yaml")):
            try:
                with open(yf, "r", encoding="utf-8") as _f:
                    other_data = _yaml.safe_load(_f)
                for tc in other_data.get("testcases", []):
                    if tc.get("path") == login_path and tc.get("method") == "POST":
                        return tc.get("request", {}).get("body", {})
            except Exception:
                pass

    return None


def _build_fallback_login_body(auth_setup):
    """从 accounts + params 拼接默认登录请求体"""
    accounts = auth_setup.get("accounts", {})
    params = auth_setup.get("params", {})
    account_names = list(accounts.keys())
    if not account_names:
        return {}
    default_account = account_names[0]
    account = accounts.get(default_account, {})
    body = {}
    account_params = params.get(default_account, {})
    if isinstance(account_params, dict):
        for k, v in account_params.items():
            body[k] = v
    body.update(account)
    return body


def _do_login(base_url, auth_setup, global_vars, module_data, yaml_dir=None):
    """执行登录，返回 token 字典"""
    login_path = auth_setup.get("login_endpoint", "")
    if not login_path:
        return {}

    url = f"{base_url}{login_path}"
    headers = {"Content-Type": "application/json"}

    login_body = _find_login_body_template(module_data, auth_setup, yaml_dir)
    if login_body is None:
        login_body = _build_fallback_login_body(auth_setup)

    empty_ctx = ModuleContext()
    body = resolve_vars(login_body, auth_setup, {}, global_vars, empty_ctx)

    resp = requests.post(url, json=body, headers=headers, timeout=30)

    extracts = auth_setup.get("extracts", {})
    result = {}
    if resp.headers.get("Content-Type", "").startswith("application/json"):
        try:
            resp_data = resp.json()
            for key, expr in extracts.items():
                val = jsonpath_extract(resp_data, expr)
                if val is not None:
                    result[key] = val
        except Exception:
            pass

    return result


# ═══════════════════════════════════════════════════════════════
# 请求执行 + 断言
# ═══════════════════════════════════════════════════════════════

def _format_failure_context(method, url, req_body, resp, parsed_data):
    """格式化断言失败时的完整请求/响应上下文"""
    lines = [
        "",
        "-" * 60,
        "[完整请求/响应上下文]",
        f"  请求: {method} {url}",
    ]
    if req_body:
        body_str = json.dumps(req_body, indent=2, ensure_ascii=False)
        lines.append(f"  请求体: {body_str}")
    lines.append(f"  响应状态码: {resp.status_code}")
    if parsed_data is not None:
        lines.append("  响应体:")
        lines.append(json.dumps(parsed_data, indent=2, ensure_ascii=False))
    elif resp.text:
        # 尝试解析 JSON 以便格式化输出
        try:
            fallback_data = json.loads(resp.text)
            lines.append("  响应体:")
            lines.append(json.dumps(fallback_data, indent=2, ensure_ascii=False))
        except (json.JSONDecodeError, ValueError):
            lines.append("  响应体 (非JSON):")
            lines.append(resp.text[:2000])
    lines.append("-" * 60)
    return "\n".join(lines)


def execute_request(case, base_url, auth_setup, auth_values, global_vars, ctx,
                    public_h, auth_h):
    """构建并发送 HTTP 请求，执行断言，返回 (response, parsed_data)"""
    method = case.get("method", "GET").upper()
    path_tmpl = case.get("path", "")
    request_def = case.get("request", {})
    expected = case.get("expected", {})

    # 解析变量
    path = resolve_vars(path_tmpl, auth_setup, auth_values, global_vars, ctx)
    query = resolve_vars(request_def.get("query", {}), auth_setup, auth_values, global_vars, ctx)
    body = resolve_vars(request_def.get("body", {}), auth_setup, auth_values, global_vars, ctx)
    path_params = resolve_vars(request_def.get("path_params", {}), auth_setup, auth_values, global_vars, ctx)

    # 替换路径参数 {key} → resolved_value（同时兼容 ${key} 写法，避免生成 $1 畸形占位）
    for k, v in path_params.items():
        path = path.replace("${" + k + "}", str(v)).replace("{" + k + "}", str(v))

    # 依赖中断检测：前置用例未成功执行（extracts 缺失）时跳过而非发送残缺请求
    unresolved = re.findall(r"__UNRESOLVED_DEP:([\w]+):[\w]+__", path)
    if unresolved:
        pytest.skip(f"依赖用例 {unresolved[0]} 未成功执行，跳过（避免发送残缺 URL）")
    body_str = json.dumps(body, ensure_ascii=False) if body else ""
    if "__UNRESOLVED_DEP:" in body_str:
        unresolved_body = re.findall(r"__UNRESOLVED_DEP:([\w]+):[\w]+__", body_str)
        pytest.skip(f"依赖用例 {unresolved_body[0]} 未成功执行，跳过（请求体含未解析引用）")

    # 构建请求头
    headers = build_headers(case, auth_setup, auth_values, global_vars, ctx, public_h, auth_h)

    # 构建 URL
    url = f"{base_url}{path}"

    # 判断请求体编码方式
    ct = headers.get("Content-Type", "").lower()
    use_json = "json" in ct and "form" not in ct and "x-www-form-urlencoded" not in ct

    # 发送请求
    if method == "GET":
        resp = requests.get(url, params=query, headers=headers, timeout=30)
    elif method == "POST":
        if use_json:
            resp = requests.post(url, params=query, json=body, headers=headers, timeout=30)
        else:
            resp = requests.post(url, params=query, data=body, headers=headers, timeout=30)
    elif method == "PUT":
        if use_json:
            resp = requests.put(url, params=query, json=body, headers=headers, timeout=30)
        else:
            resp = requests.put(url, params=query, data=body, headers=headers, timeout=30)
    elif method == "DELETE":
        resp = requests.delete(url, params=query, headers=headers, timeout=30)
    elif method == "PATCH":
        if use_json:
            resp = requests.patch(url, params=query, json=body, headers=headers, timeout=30)
        else:
            resp = requests.patch(url, params=query, data=body, headers=headers, timeout=30)
    else:
        raise ValueError(f"不支持的 HTTP 方法: {method}")

    # ── 断言 ──
    data = None  # 确保 except 中 data 始终可用
    try:
        status_code = expected.get("status_code")
        assert resp.status_code == status_code, (
            f"HTTP 状态码不匹配: 期望 {status_code}, 实际 {resp.status_code}"
        )

        response_type = expected.get("response_type", "json")
        if response_type == "json":
            try:
                data = resp.json()
            except Exception:
                data = None

            # 检测是否为包装响应（有 code 字段）还是原始 JSON
            is_wrapped = isinstance(data, dict) and "code" in data

            business_code = expected.get("business_code")
            if business_code is not None and is_wrapped:
                assert data is not None, "期望 JSON 响应但解析失败"
                actual_code = data.get("code")
                assert actual_code == business_code, (
                    f"业务状态码不匹配: 期望 {business_code}, 实际 {actual_code}"
                )
            business_message = expected.get("business_message")
            if business_message and is_wrapped:
                # msg_field 兼容：优先 msg，其次 message（由 _manifest.yaml response_wrapper.msg_field 决定）
                actual_msg = data.get("msg", data.get("message", ""))
                assert actual_msg == business_message, (
                    f"业务消息不匹配: 期望 '{business_message}', 实际 '{actual_msg}'"
                )
            # 无包装 JSON：仅校验 HTTP 状态码即视为业务成功
            data_exists = expected.get("data_exists", [])
            if is_wrapped:
                resp_data_section = data.get("data") if data else None
            else:
                resp_data_section = data  # 根级查找
            for key in data_exists:
                if isinstance(resp_data_section, dict):
                    assert key in resp_data_section, (
                        f"响应中缺少字段: {key}"
                    )
                elif isinstance(resp_data_section, list) and key == "":
                    pass  # 允许空列表占位
            data_equals = expected.get("data_equals", {})
            for jsonpath_key, expected_val in data_equals.items():
                actual_val = jsonpath_extract(data, jsonpath_key)
                assert actual_val == expected_val, (
                    f"字段 {jsonpath_key} 值不匹配: 期望 {expected_val}, 实际 {actual_val}"
                )
        elif response_type == "html":
            data = resp.text
            body_contains = expected.get("body_contains", [])
            for fragment in body_contains:
                assert fragment in resp.text, (
                    f"响应体不包含预期文本: '{fragment}'"
                )
        else:
            data = resp.text
    except AssertionError as e:
        context = _format_failure_context(method, url, body, resp, data)
        raise AssertionError(f"{e}\n{context}") from None

    return resp, data


# ═══════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════

@pytest.fixture(scope="module")
def module_context():
    """模块级共享上下文"""
    return ModuleContext()


@pytest.fixture(scope="session")
def module_data():
    """由各 test_{module}.py 覆盖，返回本模块的 YAML 数据"""
    return {}


@pytest.fixture(scope="session")
def yaml_dir():
    """由各 test_{module}.py 覆盖，返回 YAML 文件所在目录"""
    return None


@pytest.fixture(scope="session")
def auth_values(module_data, yaml_dir):
    """Session 级登录，获取 token 等认证信息"""
    auth_setup = module_data.get("auth_setup", {})
    if auth_setup.get("type", "none") == "none":
        return {}

    base_url = module_data.get("base_url", "")
    global_vars = module_data.get("global_variables", {})
    return _do_login(base_url, auth_setup, global_vars, module_data, yaml_dir)


class RequestHelper:
    """封装请求执行逻辑，减少测试函数中重复参数传递"""

    def __init__(self, base_url, auth_setup, auth_values, global_vars, module_context, public_h, auth_h):
        self.base_url = base_url
        self.auth_setup = auth_setup
        self.auth_values = auth_values
        self.global_vars = global_vars
        self.module_context = module_context
        self.public_h = public_h
        self.auth_h = auth_h

    def execute(self, case):
        resp, data = execute_request(
            case, self.base_url, self.auth_setup, self.auth_values,
            self.global_vars, self.module_context, self.public_h, self.auth_h
        )
        # 记录实际响应报文，供报告展示（由 makereport hook 写入 junit property）
        try:
            body_text = getattr(resp, "text", "") or ""
        except Exception:
            body_text = ""
        self.last_response = {
            "status_code": getattr(resp, "status_code", None),
            "body": body_text[:4000],
        }
        return resp, data

    def resolve(self, value):
        return resolve_vars(
            value, self.auth_setup, self.auth_values,
            self.global_vars, self.module_context
        )

    def store_extracts(self, case_id, case, data):
        """存储用例的 extracts 到 module_context，同时同步 __auth__"""
        extracts_def = case.get("extracts", {})
        if not extracts_def or data is None:
            return
        self.module_context.vars.setdefault(case_id, {})
        auth_extracts_def = self.auth_setup.get("extracts", {})
        for key, jsonpath in extracts_def.items():
            val = jsonpath_extract(data, jsonpath)
            if val is not None:
                self.module_context.vars[case_id][key] = val
                # 匹配 auth_setup.extracts：先按 key 名，再按 JSONPath
                auth_key = key if key in auth_extracts_def else None
                if auth_key is None:
                    for auth_k, auth_path in auth_extracts_def.items():
                        if auth_path == jsonpath:
                            auth_key = auth_k
                            break
                if auth_key is not None:
                    self.module_context.vars.setdefault("__auth__", {})[auth_key] = val


@pytest.fixture(scope="module")
def request_helper(module_data, auth_values, module_context):
    base_url = module_data.get("base_url", "")
    auth_setup = module_data.get("auth_setup", {})
    global_vars = module_data.get("global_variables", {})
    public_h = module_data.get("headers_config", {}).get("public_headers", [])
    auth_h = module_data.get("headers_config", {}).get("auth_headers", [])
    return RequestHelper(base_url, auth_setup, auth_values, global_vars, module_context, public_h, auth_h)
