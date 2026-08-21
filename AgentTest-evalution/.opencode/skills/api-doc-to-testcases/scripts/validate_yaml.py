#!/usr/bin/env python3
"""
YAML 测试用例格式校验脚本（v2 — headers_config + auth_setup 格式）。

用法:
  python validate_yaml.py <yaml文件或目录>

校验规则:
  1. YAML 语法有效
  2. 所有必填字段存在
  3. 枚举字段值在允许范围内
  4. login_endpoint 为纯路径（不含 HTTP 方法）
  5. data_exists 使用 JSON 键名格式
  6. auth_setup 结构完整
  7. 用例 ID 格式正确且无重复
  8. method 值为有效 HTTP 方法
  9. response_type 与断言字段一致性
  10. 变量引用一致性（auth_headers 中的 ${auth.xxx} 能从 auth_setup 解析）

退出码: 0=通过, 1=校验失败, 2=脚本异常
"""

import sys
import os
import re
import argparse
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML 未安装，请执行: pip install pyyaml")
    sys.exit(2)

# ── 枚举定义 ──

VALID_AUTH_TYPES = {"bearer_token", "basic", "apikey", "oauth2", "none"}
VALID_PRIORITIES = {"P0", "P1", "P2"}
VALID_TAGS = {"正常", "异常", "回归", "冒烟", "兼容性", "用户体验"}
VALID_HTTP_METHODS = {"GET", "POST", "PUT", "DELETE", "PATCH"}
VALID_RESPONSE_TYPES = {"json", "html"}

# login_endpoint 应为纯路径
LOGIN_ENDPOINT_PATTERN = re.compile(r'^(/[a-zA-Z0-9_\-{}]+)*$')
# 用例 ID 格式: TC_<MODULE>_<三位数字>
CASE_ID_PATTERN = re.compile(r'^TC_[A-Z][A-Z0-9_]*_\d{3}$')
# JSONPath 格式
JSONPATH_PATTERN = re.compile(r'^\$(\.[a-zA-Z_][a-zA-Z0-9_]*|\[\d+\])+$')
# 变量引用格式 ${xxx}
VAR_REF_PATTERN = re.compile(r'\$\{([^}]+)\}')

ERRORS = []
WARNINGS = []


def error(msg: str):
    ERRORS.append(msg)


def warn(msg: str):
    WARNINGS.append(msg)


# ── 校验函数 ──

def validate_required(data, key, parent=""):
    """检查必填字段存在且非空"""
    path = f"{parent}.{key}" if parent else key
    if key not in data:
        error(f"缺失必填字段: {path}")
        return False
    if data[key] is None or (isinstance(data[key], str) and data[key].strip() == ""):
        error(f"必填字段为空: {path}")
        return False
    return True


def validate_enum(data, key, valid_values, parent=""):
    """检查字段值在枚举范围内"""
    path = f"{parent}.{key}" if parent else key
    if key not in data:
        return
    value = data[key]
    if isinstance(value, list):
        for v in value:
            if v not in valid_values:
                error(f"{path}: 无效标签 '{v}'，允许值: {sorted(valid_values)}")
    else:
        if value not in valid_values:
            error(f"{path}: 无效值 '{value}'，允许值: {sorted(valid_values)}")


def validate_pattern(data, key, pattern, desc, parent=""):
    """检查字段值匹配正则"""
    path = f"{parent}.{key}" if parent else key
    if key not in data or not data[key]:
        return
    if not pattern.match(str(data[key])):
        error(f"{path}: 格式错误 ({desc})，当前值: '{data[key]}'")


def validate_headers_list(headers, parent, label):
    """校验 headers 列表格式"""
    if not isinstance(headers, list):
        error(f"{parent}: {label} 必须是列表")
        return
    for i, h in enumerate(headers):
        if isinstance(h, str):
            error(f"{parent}[{i}]: {label} 条目必须是 {{name, value}} 字典，不能是纯字符串")
        elif isinstance(h, dict):
            if "name" not in h:
                error(f"{parent}[{i}]: 缺少 name 字段")
            if "value" not in h:
                error(f"{parent}[{i}]: 缺少 value 字段")


def resolve_auth_ref(ref_path, auth_setup):
    """
    解析 ${auth.xxx} 引用路径是否在 auth_setup 中存在。
    支持 extracts 跳过规则: ${auth.token} 直接查 auth_setup.extracts.token。
    返回 (exists: bool, resolved_path: str)
    """
    parts = ref_path.split(".")
    if parts[0] != "auth":
        return False, ref_path

    if len(parts) == 1:
        return False, ref_path

    # ${auth.xxx} 或 ${auth.xxx.yyy...}
    current = auth_setup

    # 第一层
    first = parts[1]

    # extracts 跳过规则: ${auth.xxx} 且 xxx 在 auth_setup.extracts 中
    if len(parts) == 2:
        extracts = auth_setup.get("extracts", {})
        if first in extracts:
            return True, f"auth_setup.extracts.{first}"
        # 也检查顶层字段
        if first in auth_setup:
            return True, f"auth_setup.{first}"
        # 检查 params
        params = auth_setup.get("params", {})
        if first in params:
            return True, f"auth_setup.params.{first}"
        return False, ref_path

    # 多层级: ${auth.xxx.yyy.zzz...}
    if first == "extracts":
        warn(f"变量引用 '${{auth.extracts.{'.'.join(parts[2:])}}}' 应跳过 extracts 层级，"
             f"建议使用 '${{auth.{'.'.join(parts[2:])}}}'")

    # 遍历路径
    if first in auth_setup:
        current = auth_setup[first]
    elif first == "extracts":
        current = auth_setup.get("extracts", {})
    elif first == "params":
        current = auth_setup.get("params", {})
    elif first == "accounts":
        current = auth_setup.get("accounts", {})
    else:
        return False, ref_path

    for part in parts[2:]:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return False, ref_path

    return True, ref_path


def validate_yaml_structure(data, filepath):
    """校验单个 YAML 文件的完整结构"""

    # ── 顶层字段 ──
    for key in ["module", "module_name", "base_url", "testcases"]:
        validate_required(data, key)
    validate_required(data, "headers_config")
    validate_required(data, "auth_setup")

    # ── headers_config ──
    hc = data.get("headers_config", {})
    if isinstance(hc, dict):
        if "public_headers" in hc:
            validate_headers_list(hc["public_headers"], "headers_config.public_headers", "public_headers")
        if "auth_headers" in hc:
            validate_headers_list(hc["auth_headers"], "headers_config.auth_headers", "auth_headers")

    # ── auth_setup ──
    auth_setup = data.get("auth_setup", {})
    validate_required(auth_setup, "type", "auth_setup")
    validate_enum(auth_setup, "type", VALID_AUTH_TYPES, "auth_setup")

    auth_type = auth_setup.get("type", "")
    is_no_auth = (auth_type == "none")

    # login_endpoint: 无认证时可为空
    if not is_no_auth:
        validate_required(auth_setup, "login_endpoint", "auth_setup")
        validate_pattern(auth_setup, "login_endpoint", LOGIN_ENDPOINT_PATTERN,
                         "应为纯路径如 /auth/login，不含 HTTP 方法前缀", "auth_setup")

    # token_prefix: 无认证时可为空
    if not is_no_auth:
        validate_required(auth_setup, "token_prefix", "auth_setup")

    # accounts: 无认证时可为空
    accounts = auth_setup.get("accounts", {})
    if not is_no_auth:
        validate_required(auth_setup, "accounts", "auth_setup")
        if not accounts:
            error("auth_setup.accounts 至少需要一个测试账号")

    # extracts
    extracts = auth_setup.get("extracts", {})
    if not is_no_auth:
        validate_required(auth_setup, "extracts", "auth_setup")
        if isinstance(extracts, dict):
            if "token" not in extracts:
                error("auth_setup.extracts 至少需要包含 'token' 字段")

    # ── auth_headers 中的 ${auth.xxx} 引用校验 ──
    auth_headers = hc.get("auth_headers", [])
    if isinstance(auth_headers, list):
        for i, ah in enumerate(auth_headers):
            if not isinstance(ah, dict):
                continue
            ah_value = ah.get("value", "")
            if not isinstance(ah_value, str):
                continue
            refs = VAR_REF_PATTERN.findall(ah_value)
            for ref in refs:
                if ref.startswith("auth."):
                    exists, _ = resolve_auth_ref(ref, auth_setup)
                    if not exists:
                        error(f"headers_config.auth_headers[{i}].value: "
                              f"引用 '${{{ref}}}' 无法在 auth_setup 中解析")

    # ── global_variables ──
    global_vars = data.get("global_variables", {})
    if global_vars and not isinstance(global_vars, dict):
        error("global_variables 必须是字典")

    # ── testcases ──
    cases = data.get("testcases", [])
    if not isinstance(cases, list) or len(cases) == 0:
        error("testcases 必须是非空列表")
        return

    case_ids = []
    for i, case in enumerate(cases):
        if not isinstance(case, dict):
            error(f"testcases[{i}]: 必须是字典类型")
            continue

        prefix = f"testcases[{i}]"

        # 必填字段
        for key in ["id", "title", "priority", "method", "path"]:
            validate_required(case, key, prefix)

        # 枚举校验
        validate_enum(case, "priority", VALID_PRIORITIES, prefix)
        validate_enum(case, "tags", VALID_TAGS, prefix)
        validate_enum(case, "method", VALID_HTTP_METHODS, prefix)

        # 用例 ID
        case_id = case.get("id", "")
        if case_id:
            validate_pattern(case, "id", CASE_ID_PATTERN,
                           "格式: TC_<MODULE>_<三位数字>，如 TC_AUTH_001", prefix)
            if case_id in case_ids:
                error(f"{prefix}.id: 重复的用例 ID '{case_id}'")
            case_ids.append(case_id)

        # path 应为 / 开头
        if case.get("path") and not str(case["path"]).startswith("/"):
            error(f"{prefix}.path: 应以 / 开头，当前值: '{case['path']}'")

        # ── auth 段（用例级认证声明）──
        case_auth = case.get("auth", {})
        if isinstance(case_auth, dict):
            if "required" in case_auth:
                if not isinstance(case_auth["required"], bool):
                    error(f"{prefix}.auth.required: 必须是布尔值 (true/false)")
            else:
                warn(f"{prefix}.auth: 建议显式声明 auth.required")

            account_name = case_auth.get("account", "")
            if account_name:
                if account_name not in accounts:
                    error(f"{prefix}.auth.account: 账号 '{account_name}' 未在 auth_setup.accounts 中定义，"
                          f"可用账号: {list(accounts.keys())}")

        # 认证接口不应在 request.headers 中手写认证头
        if case_auth.get("required"):
            ah_names = set()
            if isinstance(auth_headers, list):
                for ah in auth_headers:
                    if isinstance(ah, dict):
                        ah_names.add(ah.get("name", "").lower())
            case_headers = case.get("request", {}).get("headers", [])
            if isinstance(case_headers, list):
                for h in case_headers:
                    if isinstance(h, dict) and h.get("name", "").lower() in ah_names:
                        warn(f"{prefix}.request.headers: 手写了已在 headers_config.auth_headers 中"
                              f"声明的头，已通过 auth.required=true 自动注入")

        # ── request 段 ──
        request = case.get("request", {})
        if request and isinstance(request, dict):
            req_prefix = f"{prefix}.request"
            if "headers" in request:
                validate_headers_list(request["headers"], f"{req_prefix}.headers", "headers")

        # ── expected 段 ──
        expected = case.get("expected", {})
        if not isinstance(expected, dict):
            error(f"{prefix}.expected: 必须是字典类型")
            continue

        exp_prefix = f"{prefix}.expected"
        validate_required(expected, "status_code", exp_prefix)
        validate_required(expected, "response_type", exp_prefix)
        validate_enum(expected, "response_type", VALID_RESPONSE_TYPES, exp_prefix)

        rt = expected.get("response_type")

        if rt == "json":
            if "business_code" not in expected:
                error(f"{exp_prefix}: response_type=json 时 business_code 必填")
            if "data_exists" not in expected:
                error(f"{exp_prefix}: response_type=json 时 data_exists 必填")
            else:
                de = expected["data_exists"]
                if not isinstance(de, list):
                    error(f"{exp_prefix}.data_exists: 必须是列表")

        elif rt == "html":
            if "body_contains" not in expected:
                error(f"{exp_prefix}: response_type=html 时 body_contains 必填")
            elif not isinstance(expected["body_contains"], list):
                error(f"{exp_prefix}.body_contains: 必须是列表")

        # ── extracts ──
        if "extracts" in case:
            case_extracts = case["extracts"]
            if isinstance(case_extracts, dict):
                for ek, ev in case_extracts.items():
                    if isinstance(ev, str) and not ev.startswith("$"):
                        error(f"{prefix}.extracts.{ek}: JSONPath 必须以 $ 开头，当前值: '{ev}'")

        # ── depends_on ──
        if "depends_on" in case:
            deps = case["depends_on"]
            if isinstance(deps, list):
                for dep in deps:
                    if dep not in case_ids:
                        warn(f"{prefix}.depends_on: 依赖的用例 '{dep}' 未在当前文件中找到"
                             f"（可能在其他模块中，请人工确认）")


def validate_file(filepath: str) -> int:
    """校验单个 YAML 文件，返回错误数"""
    global ERRORS, WARNINGS
    ERRORS = []
    WARNINGS = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        error(f"YAML 语法错误: {e}")
        return len(ERRORS)
    except Exception as e:
        error(f"读取文件失败: {e}")
        return len(ERRORS)

    if data is None:
        error("YAML 文件为空或仅含注释")
        return len(ERRORS)

    validate_yaml_structure(data, filepath)

    basename = os.path.basename(filepath)
    if ERRORS:
        print(f"\n{'='*60}")
        print(f"  FAIL: {basename}")
        print(f"{'='*60}")
        for e in ERRORS:
            print(f"  [ERROR] {e}")
    else:
        print(f"  PASS: {basename}")

    if WARNINGS:
        for w in WARNINGS:
            print(f"  [WARN]  {w}")

    return len(ERRORS)


def main():
    parser = argparse.ArgumentParser(description="YAML 测试用例格式校验")
    parser.add_argument("path", help="YAML 文件或包含 .yaml 文件的目录")
    parser.add_argument("--strict", action="store_true", help="将 WARNING 视为 ERROR")
    args = parser.parse_args()

    target = Path(args.path)
    if not target.exists():
        print(f"ERROR: 路径不存在: {args.path}")
        sys.exit(2)

    files = []
    if target.is_file():
        if target.suffix in (".yaml", ".yml"):
            files = [str(target)]
    else:
        files = sorted(str(p) for p in target.glob("*.yaml"))
        if not files:
            print(f"WARNING: 目录中未找到 .yaml 文件: {args.path}")

    if not files:
        print("没有文件需要校验")
        sys.exit(0)

    print(f"校验 {len(files)} 个文件...\n")

    total_errors = 0
    for f in files:
        errs = validate_file(f)
        total_errors += errs

    print(f"\n{'='*60}")
    print(f"  汇总: {len(files)} 文件, {total_errors} 错误")
    if WARNINGS:
        print(f"        {len(WARNINGS)} 警告")
    print(f"{'='*60}")

    if args.strict and WARNINGS:
        total_errors += len(WARNINGS)

    sys.exit(0 if total_errors == 0 else 1)


if __name__ == "__main__":
    main()
