"""
从 YAML 测试用例生成可独立执行的 pytest 脚本。

输入: tests/baseline/_workflow/03-testcases/*.yaml
输出: tests/baseline/generated/api-test/
  ├── api_utils.py     - 工具函数（JSONPath、变量解析、请求构建、断言）
  ├── conftest.py      - pytest fixtures（认证、变量池、执行上下文）
  ├── test_{module}.py - 每个 YAML 一个测试模块，每用例一个 def
  └── pytest.ini       - markers 配置

用法:
    python generate_pytest.py
    python generate_pytest.py --input tests/baseline/_workflow/03-testcases
    python generate_pytest.py --output tests/baseline/generated/api-test
"""

import argparse
import os
import re
import sys
from pathlib import Path

# Windows 控制台 UTF-8 支持
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Run: pip install pyyaml")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
DEFAULT_INPUT = PROJECT_ROOT / "tests" / "baseline" / "_workflow" / "03-testcases"
DEFAULT_OUTPUT = PROJECT_ROOT / "tests" / "baseline" / "generated" / "api-test"


# ──────────────────────────────────────────────
# 代码生成工具
# ──────────────────────────────────────────────

def _safe_func_name(text):
    """从文本生成合法的 Python 函数名片段（仅小写字母、数字、下划线）"""
    # 移除非 ASCII 和特殊字符，转为小写
    text = text.lower().replace(" ", "_").replace("/", "_").replace("-", "_")
    text = re.sub(r"[^a-z0-9_]", "", text)
    # 压缩连续下划线
    text = re.sub(r"_+", "_", text)
    return text.strip("_")


def _make_test_func_name(case_id, title):
    """从用例 ID 和标题生成测试函数名。

    TC_AUTH_001 + "POST /auth/login_完整有效参数_登录成功"
    → test_tc_auth_001_post_auth_login
    """
    case_part = _safe_func_name(case_id)
    # 从标题提取 HTTP 方法 + 路径部分
    method_path = title.split("_")[0] if "_" in title else title[:30]
    method_path = method_path.replace(" ", "_").replace("/", "_").lower()
    method_path = re.sub(r"[^a-z0-9_]", "", method_path)
    method_path = re.sub(r"_+", "_", method_path).strip("_")
    # 限制长度
    name = f"test_{case_part}_{method_path}"[:80]
    return name


PYTHON_KEYWORDS = frozenset({
    "False", "None", "True", "and", "as", "assert", "async", "await",
    "break", "class", "continue", "def", "del", "elif", "else", "except",
    "finally", "for", "from", "global", "if", "import", "in", "is",
    "lambda", "nonlocal", "not", "or", "pass", "raise", "return",
    "try", "while", "with", "yield",
})


def _safe_marker_name(name):
    """将标签名转为安全的 pytest marker 名，避免 Python 关键字冲突"""
    cleaned = re.sub(r"[^a-zA-Z0-9一-鿿]", "_", name)
    if cleaned in PYTHON_KEYWORDS:
        cleaned = f"tag_{cleaned}"
    return cleaned


def _parse_case_priority(case):
    """将优先级的 P0/P1/P2 映射到 pytest marker 装饰器"""
    priority = case.get("priority", "P2")
    tags = case.get("tags", [])
    markers = [f"@pytest.mark.{priority}"]
    for tag in tags:
        markers.append(f"@pytest.mark.{_safe_marker_name(tag)}")
    return "\n".join(markers)


# ──────────────────────────────────────────────
# 文件生成函数
# ──────────────────────────────────────────────

API_UTILS_TEMPLATE = '''"""
API 测试工具函数 — 与 pytest 无关，可独立使用。

提供:
- JSONPath 求值 ($.data.field)
- 变量解析 (${var})
- HTTP 请求构建与发送
- 响应断言（协议层 + 业务层 + 数据层）
"""

import json
import os
import re
import time
from pathlib import Path

import requests


# ── JSONPath ──────────────────────────────────

def evaluate_jsonpath(data, path):
    """求值简单 JSONPath 表达式，如 $.data.accessToken、$.data。

    支持: $.a.b.c 形式，仅支持 dict 键访问。
    返回: 提取的值，不存在时返回 None。
    """
    if not path or not path.startswith("$."):
        return None
    parts = path[2:].split(".")
    current = data
    for part in parts:
        if isinstance(current, dict):
            current = current.get(part)
        elif isinstance(current, list):
            try:
                current = current[int(part)]
            except (IndexError, ValueError):
                return None
        else:
            return None
    return current


# ── 变量解析 ──────────────────────────────────

def generate_timestamp():
    """生成毫秒时间戳，用于构造唯一测试数据（如用户名后缀）"""
    return str(int(time.time() * 1000))


_VAR_PATTERN = re.compile(r"\\$\\{([^}]+)\\}")


def resolve_vars(obj, context):
    """递归解析对象中的 ${var} 变量引用。

    context 字典提供变量值映射。支持:
    - ${token}       → context["token"]
    - ${clientId}    → context["clientId"]
    - ${timestamp}   → 自动生成时间戳
    - ${var_name}    → context 中任意键

    对字符串、列表、字典递归处理，不修改原对象。
    """
    if isinstance(obj, str):
        # 如果整个字符串就是一个 ${var}，则返回原始类型
        m = _VAR_PATTERN.fullmatch(obj.strip())
        if m:
            var_name = m.group(1)
            if var_name == "timestamp":
                return generate_timestamp()
            if var_name in context:
                val = context[var_name]
                # 如果提取的值是字符串且看起来像 JSONPath，则求值
                # （这种情况发生在 extract 的变量被引用时）
                return val
            return obj
        return _VAR_PATTERN.sub(lambda m: _resolve_single(m.group(1), context), obj)

    elif isinstance(obj, dict):
        return {k: resolve_vars(v, context) for k, v in obj.items()}

    elif isinstance(obj, list):
        return [resolve_vars(item, context) for item in obj]

    return obj


def _resolve_single(var_name, context):
    """解析单个变量名为字符串"""
    if var_name == "timestamp":
        return generate_timestamp()
    val = context.get(var_name, f"${{{var_name}}}")
    if not isinstance(val, str):
        val = str(val)
    return val


# ── HTTP 请求构建 ──────────────────────────────

def build_headers(global_headers, case_headers, context):
    """构建请求头：解析全局头中的变量 → 用例特定头覆盖。

    Args:
        global_headers: YAML 中的 global_headers 列表
        case_headers: 用例 request.headers 列表
        context: 变量上下文（包含 token, clientId 等）

    Returns:
        dict: 最终请求头
    """
    headers = {}

    # 1. 构建全局头
    if global_headers:
        for h in global_headers:
            resolved_value = resolve_vars(h["value"], context)
            # 跳过值为空的头（表示不需要传递）
            if resolved_value:
                headers[h["name"]] = resolved_value

    # 2. 用例特定头覆盖
    if case_headers:
        for h in case_headers:
            # 空字符串表示显式移除
            if h.get("value") == "":
                headers.pop(h["name"], None)
            else:
                headers[h["name"]] = resolve_vars(h["value"], context)

    return headers


def send_request(method, path, base_url, case_request, headers):
    """构建并发送 HTTP 请求。

    Args:
        method: HTTP 方法
        path: 请求路径
        base_url: 基础 URL
        case_request: 用例的 request 字段（含 params/body/files）
        headers: 已解析的请求头

    Returns:
        requests.Response
    """
    url = f"{base_url}{path}"
    kwargs = {"headers": headers, "timeout": 30}

    params = case_request.get("params", {}) if case_request else {}
    body = case_request.get("body", {}) if case_request else {}

    method_upper = method.upper()

    if method_upper in ("GET", "DELETE"):
        if params:
            kwargs["params"] = params
    elif method_upper in ("POST", "PUT", "PATCH"):
        if body is not None:
            kwargs["json"] = body
        if params:
            kwargs["params"] = params

    return requests.request(method_upper, url, **kwargs)


# ── 响应断言 ──────────────────────────────────

class ApiAssertionError(Exception):
    """测试断言错误，包含清晰的失败信息"""
    pass


def assert_response(response, expected, msg_field="msg"):
    """对 HTTP 响应执行三层断言。

    1. 协议层: HTTP 状态码
    2. 业务层: 业务状态码 + 业务消息（支持 exact/contains/skip 模式）
    3. 数据层: 响应字段存在性

    Args:
        response: requests.Response 对象
        expected: YAML 中的 expected 字典
        msg_field: 业务消息在响应 JSON 中的字段名（默认 "msg"）

    Raises:
        ApiAssertionError: 断言失败时抛出
    """
    # 尝试解析 JSON 响应体
    try:
        body = response.json()
    except Exception:
        body = {}

    # ── 协议层 ──
    exp_status = expected.get("status_code")
    if exp_status is not None:
        if response.status_code != exp_status:
            raise ApiAssertionError(
                f"HTTP 状态码不匹配: 期望 {exp_status}, 实际 {response.status_code}\\n"
                f"响应体: {json.dumps(body, ensure_ascii=False)[:500]}"
            )

    # ── 业务层 ──
    exp_code = expected.get("business_code")
    if exp_code is not None:
        actual_code = body.get("code")
        if actual_code != exp_code:
            raise ApiAssertionError(
                f"业务状态码不匹配: 期望 {exp_code}, 实际 {actual_code}\\n"
                f"响应体: {json.dumps(body, ensure_ascii=False)[:500]}"
            )

    exp_msg = expected.get("business_message")
    msg_mode = expected.get("business_message_mode", "exact")
    if exp_msg is not None:
        actual_msg = body.get(msg_field, body.get("msg", ""))
        if msg_mode == "skip":
            pass
        elif msg_mode == "contains":
            if actual_msg and exp_msg not in actual_msg:
                raise ApiAssertionError(
                    f"业务消息不匹配: 期望包含 '{exp_msg}', 实际 '{actual_msg}'"
                )
        else:  # "exact"（默认）
            if actual_msg and actual_msg != exp_msg:
                raise ApiAssertionError(
                    f"业务消息不匹配: 期望 '{exp_msg}', 实际 '{actual_msg}'"
                )

    # ── 数据层 ──
    data_exists = expected.get("data_exists")
    if data_exists:
        data = body.get("data")
        if data is None:
            data = {}
        missing = [f for f in data_exists if f not in data]
        if missing:
            raise ApiAssertionError(
                f"响应 data 中缺少字段: {missing}\\n"
                f"实际 data: {json.dumps(data, ensure_ascii=False)[:300]}"
            )


def extract_from_response(response, extract_map, context):
    """从 HTTP 响应中提取变量并存入 context。

    Args:
        response: requests.Response 对象
        extract_map: YAML extract 字典 {var_name: "$.data.path"}
        context: 可变上下文字典（直接修改）
    """
    if not extract_map:
        return
    try:
        body = response.json()
    except Exception:
        return
    for var_name, jsonpath in extract_map.items():
        value = evaluate_jsonpath(body, jsonpath)
        if value is not None:
            context[var_name] = value
'''

CONFTEST_TEMPLATE = '''"""
pytest conftest — 提供认证、变量池、测试执行上下文 fixtures。

每个测试模块（test_{module}.py）自动加载对应的 YAML 数据文件。
Token 按账号缓存，同模块内复用。提取的变量存入模块级变量池。
"""

import os
import sys
from pathlib import Path

import pytest
import requests
import yaml

# 将当前目录加入 path
sys.path.insert(0, os.path.dirname(__file__))

from api_utils import (
    ApiAssertionError,
    assert_response,
    build_headers,
    evaluate_jsonpath,
    extract_from_response,
    generate_timestamp,
    resolve_vars,
    send_request,
)


# ── YAML 加载 ─────────────────────────────────

_WORKFLOW_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "_workflow", "03-testcases")
)
_yaml_cache = {}


def _get_yaml_for_module(module_name):
    """test_auth → auth-testcases.yaml"""
    if module_name.startswith("test_"):
        module_name = module_name[5:]
    return os.path.join(_WORKFLOW_DIR, f"{module_name}-testcases.yaml")


def _load_yaml(module_name):
    if module_name not in _yaml_cache:
        path = _get_yaml_for_module(module_name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"YAML 文件不存在: {path}")
        with open(path, "r", encoding="utf-8") as f:
            _yaml_cache[module_name] = yaml.safe_load(f)
    return _yaml_cache[module_name]


# ── 认证 ──────────────────────────────────────

class AuthManager:
    """管理账号登录和 token 缓存"""

    def __init__(self, yaml_data):
        auth = yaml_data.get("auth", {})
        self.auth = auth
        self.base_url = yaml_data.get("base_url", "http://localhost:8080")
        self.token_cache = {}  # account_name → token
        self.fixture_vars = {}  # account_name → {var: value}

    def login(self, account_name="admin"):
        """登录指定账号，返回 (token, fixture_vars)。缓存结果。"""
        if account_name in self.token_cache:
            return self.token_cache[account_name], self.fixture_vars.get(account_name, {})

        accounts = self.auth.get("accounts", {})
        if account_name not in accounts:
            available = list(accounts.keys())
            if not available:
                raise RuntimeError("YAML 中未定义任何账号")
            account_name = available[0]

        acc = accounts[account_name]
        login_endpoint = self.auth.get("login_endpoint", "/auth/login")
        url = f"{self.base_url}{login_endpoint}"

        login_data = {
            "clientId": acc.get("clientId", ""),
            "grantType": acc.get("grantType", "password"),
            "tenantId": acc.get("tenantId", "000000"),
            "username": acc.get("username", ""),
            "password": acc.get("password", ""),
        }

        response = requests.post(url, json=login_data, timeout=30)

        if response.status_code != 200:
            raise RuntimeError(
                f"登录失败 ({account_name}): HTTP {response.status_code}\\n"
                f"请求 URL: {url}\\n"
                f"响应: {response.text[:500]}"
            )

        body = response.json()
        token_path = self.auth.get("token_response_path", "$.data.accessToken")
        token = evaluate_jsonpath(body, token_path)

        if not token:
            raise RuntimeError(
                f"无法从登录响应提取 token (path={token_path})\\n"
                f"响应: {response.text[:500]}"
            )

        # 提取 fixture 变量
        extracted = {}
        for var_name, jsonpath in self.auth.get("fixture_extracts", {}).items():
            value = evaluate_jsonpath(body, jsonpath)
            if value is not None:
                extracted[var_name] = value

        self.token_cache[account_name] = token
        self.fixture_vars[account_name] = extracted
        return token, extracted


# ── 测试执行上下文 ─────────────────────────────

class ApiCaseContext:
    """每个测试用例的执行上下文。

    提供 run(case_id) 方法，自动完成:
    查找用例 → 解析 depends_on 依赖 → 解析变量 → 登录认证 → 构建请求 → 发送 → 断言 → 提取变量
    """

    def __init__(self, yaml_data, var_store, auth_manager):
        self.yaml_data = yaml_data
        self.var_store = var_store
        self.auth = auth_manager
        self.base_url = yaml_data.get("base_url", "http://localhost:8080")
        self.global_headers = yaml_data.get("global_headers", [])
        self._executed = set()  # 记录已执行的用例 ID，防止 depends_on 重复执行

    def run(self, case_id):
        """执行指定 ID 的测试用例"""
        # 查找用例
        case = self._find_case(case_id)
        if not case:
            pytest.fail(f"未找到测试用例: {case_id}")

        # ── 自动解析 depends_on 依赖 ──
        depends_on = case.get("depends_on", [])
        for dep_id in depends_on:
            if dep_id not in self._executed:
                self.run(dep_id)

        # 认证
        account_name = case.get("account", "admin")
        token, fixture_vars = self.auth.login(account_name)

        # 构建变量上下文
        context = {**fixture_vars, **self.var_store}
        context["token"] = token

        # 解析请求数据中的变量
        case_request = case.get("request", {})
        resolved_request = resolve_vars(case_request, context)

        # 构建请求头
        case_headers = resolved_request.pop("headers", None)
        # 还原 pop — 需要保留原始结构用于 send_request
        headers = build_headers(self.global_headers, case_headers, context)

        # 发送请求
        try:
            response = send_request(
                method=case["method"],
                path=case["path"],
                base_url=self.base_url,
                case_request=resolved_request,
                headers=headers,
            )
        except Exception as e:
            pytest.fail(f"请求发送失败 [{case_id}]: {e}")

        # 断言
        msg_field = self.yaml_data.get("auth", {}).get("response_msg_field", "msg")
        try:
            assert_response(response, case.get("expected", {}), msg_field=msg_field)
        except ApiAssertionError as e:
            pytest.fail(str(e))

        # 提取变量
        if "extract" in case:
            extract_from_response(response, case["extract"], self.var_store)

        # 标记已执行（用于 depends_on 防重复）
        self._executed.add(case_id)
        return response

    def _find_case(self, case_id):
        for tc in self.yaml_data.get("testcases", []):
            if tc.get("id") == case_id:
                return tc
        return None


# ── Fixtures ──────────────────────────────────

@pytest.fixture(scope="module")
def yaml_data(request):
    """模块级 fixture: 加载当前测试模块对应的 YAML 数据"""
    module_name = request.module.__name__
    return _load_yaml(module_name)


@pytest.fixture(scope="module")
def var_store():
    """模块级 fixture: 跨用例变量池（存储 extract 提取的值）"""
    return {}


@pytest.fixture(scope="module")
def auth_manager(yaml_data):
    """模块级 fixture: 认证管理器"""
    return AuthManager(yaml_data)


@pytest.fixture
def api_case(yaml_data, var_store, auth_manager):
    """函数级 fixture: 测试执行上下文"""
    return ApiCaseContext(yaml_data, var_store, auth_manager)
'''

def _build_pytest_ini(all_tags):
    """动态构建 pytest.ini，包含所有实际使用的 markers"""
    base_markers = {
        "P0": "核心路径 / 冒烟测试",
        "P1": "主要功能",
        "P2": "非关键细节",
        "正常": "正常业务流程用例",
        "异常": "异常/错误处理用例",
        "回归": "回归测试用例",
        "冒烟": "冒烟测试用例 (同 P0)",
        "兼容性": "兼容性测试",
        "用户体验": "用户体验测试",
    }
    # 合并 YAML 中的自定义标签（去重）
    for tag in sorted(all_tags):
        if tag not in base_markers:
            base_markers[tag] = f"{tag} 标签用例"

    markers_lines = "\n".join(f"    {k}: {v}" for k, v in base_markers.items())
    return f"""[pytest]
testpaths = .
python_files = test_*.py
python_functions = test_*
addopts = -v --tb=short -p no:warnings
markers =
{markers_lines}
"""


# ──────────────────────────────────────────────
# 主生成逻辑
# ──────────────────────────────────────────────

def generate_test_module(module_name, testcases, output_dir):
    """为一个模块生成 test_{module}.py 文件

    Args:
        module_name: 模块名（如 "auth"）
        testcases: YAML 中的 testcases 列表
        output_dir: 输出目录路径

    Returns:
        str: 生成的文件路径
    """
    lines = [
        '"""',
        f'{module_name} 模块 — API 接口测试',
        '',
        '自动生成，请勿手动编辑。',
        '修改测试数据请编辑对应的 YAML 文件，然后重新运行本脚本或直接执行 pytest。',
        '"""',
        '',
        'import pytest',
        '',
        '',
    ]

    for case in testcases:
        case_id = case["id"]
        title = case.get("title", case_id)
        func_name = _make_test_func_name(case_id, title)
        markers = _parse_case_priority(case)
        description = case.get("description", title)

        func_code = f'''
{markers}
def {func_name}(api_case):
    """{case_id}: {title}
    {description}
    """
    api_case.run("{case_id}")
'''
        lines.append(func_code)

    file_path = os.path.join(output_dir, f"test_{module_name}.py")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return file_path


def generate_shared_files(output_dir, all_tags=None):
    """生成共享文件: api_utils.py, conftest.py, pytest.ini

    Args:
        output_dir: 输出目录路径
        all_tags: 所有 YAML 中收集到的标签集合（用于动态注册 markers）

    Returns:
        list: 生成的文件路径列表
    """
    files = []

    # api_utils.py
    path = os.path.join(output_dir, "api_utils.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write(API_UTILS_TEMPLATE)
    files.append(path)

    # conftest.py
    path = os.path.join(output_dir, "conftest.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write(CONFTEST_TEMPLATE)
    files.append(path)

    # pytest.ini — 动态生成 markers 列表
    path = os.path.join(output_dir, "pytest.ini")
    with open(path, "w", encoding="utf-8") as f:
        f.write(_build_pytest_ini(all_tags or set()))
    files.append(path)

    return files


def main():
    parser = argparse.ArgumentParser(
        description="从 YAML 测试用例生成可独立执行的 pytest 脚本"
    )
    parser.add_argument(
        "--input", "-i",
        default=str(DEFAULT_INPUT),
        help=f"YAML 测试用例目录（默认: {DEFAULT_INPUT}）",
    )
    parser.add_argument(
        "--output", "-o",
        default=str(DEFAULT_OUTPUT),
        help=f"pytest 脚本输出目录（默认: {DEFAULT_OUTPUT}）",
    )
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)

    if not input_dir.is_dir():
        print(f"Error: input dir not found: {input_dir}")
        sys.exit(1)

    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)

    # 发现所有 YAML 文件
    yaml_files = sorted(input_dir.glob("*-testcases.yaml"))
    if not yaml_files:
        print(f"Error: no *-testcases.yaml files found in {input_dir}")
        sys.exit(1)

    print(f"Input: {input_dir}")
    print(f"Output: {output_dir}")
    print(f"Found {len(yaml_files)} YAML files")
    print("=" * 60)

    total_cases = 0
    generated_modules = []
    all_tags = set()

    for yf in yaml_files:
        with open(yf, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        module_name = data.get("module", yf.stem.replace("-testcases", ""))
        testcases = data.get("testcases", [])
        if not testcases:
            print(f"  Skip {yf.name}: no test cases")
            continue

        # 收集所有标签用于 pytest.ini markers 注册
        for case in testcases:
            for tag in case.get("tags", []):
                all_tags.add(_safe_marker_name(tag))

        file_path = generate_test_module(module_name, testcases, str(output_dir))
        generated_modules.append(module_name)
        total_cases += len(testcases)
        print(f"  [OK] test_{module_name}.py - {len(testcases)} cases")

    # 生成共享文件
    print("-" * 60)
    shared = generate_shared_files(str(output_dir), all_tags)
    for f in shared:
        print(f"  [OK] {os.path.basename(f)}")

    print("=" * 60)
    print(f"Done: {len(generated_modules)} modules, {total_cases} test cases")
    print(f"Output: {output_dir}")

    # 验证语法
    print()
    print("Syntax check...")
    errors = []
    for py_file in sorted(output_dir.glob("*.py")):
        try:
            compile(py_file.read_text(encoding="utf-8"), str(py_file), "exec")
            print(f"  [OK] {py_file.name}")
        except SyntaxError as e:
            print(f"  [FAIL] {py_file.name}: {e}")
            errors.append(str(py_file))
    if errors:
        print(f"\nWarning: {len(errors)} files have syntax errors")
        sys.exit(1)
    else:
        print("All files pass syntax check")


if __name__ == "__main__":
    main()