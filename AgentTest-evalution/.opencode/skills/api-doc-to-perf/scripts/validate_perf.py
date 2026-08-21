#!/usr/bin/env python3
"""
性能场景 YAML 格式校验脚本。

用法:
  python validate_perf.py <yaml文件或目录>

校验规则:
  1. YAML 语法有效
  2. 顶层必填字段存在（module/module_name/base_url/headers_config/scenarios）
  3. auth_setup 若存在则校验 login_endpoint（纯路径）、token_jsonpath（$ 开头）
  4. 每个 scenario 含 id/title/method/path/load/thresholds
  5. scenario.id 格式 PERF_<MODULE>_<三位数字>，且无重复
  6. load 必含 users 与 duration
  7. thresholds 非空，字段在允许范围（avg/p50/p90/p95/p99/error_rate/min_rps）
  8. auth_headers 中的 token 引用必须为 ${token}，禁止 ${auth.xxx}
  9. path 以 / 开头

退出码: 0=通过, 1=校验失败, 2=脚本异常
"""

import sys
import os
import re
import argparse
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML 未安装，请执行: pip install pyyaml")
    sys.exit(2)

# ── 枚举定义 ──

VALID_HTTP_METHODS = {"GET", "POST", "PUT", "DELETE", "PATCH"}
VALID_PRIORITIES = {"P0", "P1", "P2"}
VALID_THRESHOLD_KEYS = {"avg", "p50", "p90", "p95", "p99", "min", "max",
                        "error_rate", "min_rps", "max_rps"}

LOGIN_ENDPOINT_PATTERN = re.compile(r'^(/[a-zA-Z0-9_\-{}]+)*$')
SCENARIO_ID_PATTERN = re.compile(r'^PERF_[A-Z][A-Z0-9_]*_\d{3}$')
JSONPATH_PATTERN = re.compile(r'^\$')
VAR_REF_PATTERN = re.compile(r'\$\{([^}]+)\}')

ERRORS = []
WARNINGS = []


def error(msg: str):
    ERRORS.append(msg)


def warn(msg: str):
    WARNINGS.append(msg)


def validate_required(data, key, parent=""):
    path = f"{parent}.{key}" if parent else key
    if key not in data:
        error(f"缺失必填字段: {path}")
        return False
    if data[key] is None or (isinstance(data[key], str) and data[key].strip() == ""):
        error(f"必填字段为空: {path}")
        return False
    return True


def validate_headers_list(headers, parent, label):
    if not isinstance(headers, list):
        error(f"{parent}: {label} 必须是列表")
        return
    for i, h in enumerate(headers):
        if not isinstance(h, dict):
            error(f"{parent}[{i}]: {label} 条目必须是 {{name, value}} 字典")
            continue
        if "name" not in h:
            error(f"{parent}[{i}]: 缺少 name 字段")
        if "value" not in h:
            error(f"{parent}[{i}]: 缺少 value 字段")


def validate_no_auth_ref(headers, parent):
    """禁止在 auth_headers 中使用 ${auth.xxx} 引用（应使用 ${token}）"""
    for i, h in enumerate(headers):
        if not isinstance(h, dict):
            continue
        value = h.get("value", "")
        if not isinstance(value, str):
            continue
        refs = VAR_REF_PATTERN.findall(value)
        for ref in refs:
            if ref.startswith("auth."):
                error(f"{parent}[{i}].value: 禁止引用 '${{{ref}}}'，"
                      f"性能场景统一使用 JMeter 变量 '${{token}}'")


def validate_yaml_structure(data, filepath):
    # ── 顶层字段 ──
    for key in ["module", "module_name", "base_url", "headers_config", "scenarios"]:
        validate_required(data, key)

    # ── headers_config ──
    hc = data.get("headers_config", {})
    if isinstance(hc, dict):
        if "public_headers" in hc:
            validate_headers_list(hc["public_headers"], "headers_config.public_headers",
                                  "public_headers")
        if "auth_headers" in hc:
            validate_headers_list(hc["auth_headers"], "headers_config.auth_headers",
                                  "auth_headers")
            validate_no_auth_ref(hc["auth_headers"], "headers_config.auth_headers")

    # ── auth_setup（可选）──
    auth_setup = data.get("auth_setup", {})
    if auth_setup is not None:
        if not isinstance(auth_setup, dict):
            error("auth_setup 必须是字典")
        else:
            if "login_endpoint" in auth_setup and auth_setup["login_endpoint"]:
                if not LOGIN_ENDPOINT_PATTERN.match(str(auth_setup["login_endpoint"])):
                    error("auth_setup.login_endpoint 应为纯路径，不含 HTTP 方法前缀")
            else:
                warn("auth_setup.login_endpoint 未设置，认证场景将无法自动登录")
            if "token_jsonpath" in auth_setup and auth_setup["token_jsonpath"]:
                if not JSONPATH_PATTERN.match(str(auth_setup["token_jsonpath"])):
                    error("auth_setup.token_jsonpath 必须以 $ 开头")
            else:
                warn("auth_setup.token_jsonpath 未设置")
            if "login_body" not in auth_setup or not auth_setup.get("login_body"):
                warn("auth_setup.login_body 未设置，登录请求体将为空")

    # ── scenarios ──
    scenarios = data.get("scenarios", [])
    if not isinstance(scenarios, list) or len(scenarios) == 0:
        error("scenarios 必须是非空列表")
        return

    seen_ids = []
    for i, sc in enumerate(scenarios):
        if not isinstance(sc, dict):
            error(f"scenarios[{i}]: 必须是字典类型")
            continue

        prefix = f"scenarios[{i}]"

        for key in ["id", "title", "method", "path", "load", "thresholds"]:
            validate_required(sc, key, prefix)

        # method 枚举
        method = sc.get("method", "")
        if method and method.upper() not in VALID_HTTP_METHODS:
            error(f"{prefix}.method: 无效 HTTP 方法 '{method}'")
        if method and method != method.upper():
            warn(f"{prefix}.method: 建议大写，当前 '{method}'")

        # priority 枚举
        priority = sc.get("priority", "P1")
        if priority not in VALID_PRIORITIES:
            error(f"{prefix}.priority: 无效优先级 '{priority}'")

        # id 格式
        sc_id = sc.get("id", "")
        if sc_id:
            if not SCENARIO_ID_PATTERN.match(str(sc_id)):
                error(f"{prefix}.id: 格式应为 PERF_<MODULE>_<三位数字>，当前 '{sc_id}'")
            if sc_id in seen_ids:
                error(f"{prefix}.id: 重复的场景 ID '{sc_id}'")
            seen_ids.append(sc_id)

        # path 以 / 开头
        if sc.get("path") and not str(sc["path"]).startswith("/"):
            error(f"{prefix}.path: 应以 / 开头，当前 '{sc['path']}'")

        # auth 段
        sc_auth = sc.get("auth", {})
        if sc_auth and isinstance(sc_auth, dict):
            if "required" in sc_auth and not isinstance(sc_auth["required"], bool):
                error(f"{prefix}.auth.required: 必须是布尔值")

        # request 段
        request = sc.get("request", {})
        if request and isinstance(request, dict) and "headers" in request:
            validate_headers_list(request["headers"], f"{prefix}.request.headers", "headers")

        # ── load 段 ──
        load = sc.get("load", {})
        if not isinstance(load, dict):
            error(f"{prefix}.load: 必须是字典")
        else:
            for key in ["users", "duration"]:
                validate_required(load, key, f"{prefix}.load")
            for k in ["users", "ramp_up", "duration", "loops"]:
                if k in load and load[k] is not None and not isinstance(load[k], int):
                    error(f"{prefix}.load.{k}: 必须是整数")
            if load.get("users", 0) <= 0:
                error(f"{prefix}.load.users: 必须大于 0")
            if load.get("duration", 0) <= 0:
                error(f"{prefix}.load.duration: 必须大于 0")

        # ── thresholds 段 ──
        thresholds = sc.get("thresholds", {})
        if not isinstance(thresholds, dict):
            error(f"{prefix}.thresholds: 必须是字典")
        elif len(thresholds) == 0:
            error(f"{prefix}.thresholds: 不能为空对象，至少包含一个阈值")
        else:
            for tk, tv in thresholds.items():
                if tk not in VALID_THRESHOLD_KEYS:
                    error(f"{prefix}.thresholds.{tk}: 无效阈值字段，允许值: "
                          f"{sorted(VALID_THRESHOLD_KEYS)}")
                if not isinstance(tv, (int, float)):
                    error(f"{prefix}.thresholds.{tk}: 必须是数字")


def validate_file(filepath: str) -> int:
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
        print(f"\n{'=' * 60}")
        print(f"  FAIL: {basename}")
        print(f"{'=' * 60}")
        for e in ERRORS:
            print(f"  [ERROR] {e}")
    else:
        print(f"  PASS: {basename}")

    if WARNINGS:
        for w in WARNINGS:
            print(f"  [WARN]  {w}")

    return len(ERRORS)


def main():
    parser = argparse.ArgumentParser(description="性能场景 YAML 格式校验")
    parser.add_argument("path", help="YAML 文件或包含 .yaml 文件的目录")
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
        total_errors += validate_file(f)

    print(f"\n{'=' * 60}")
    print(f"  汇总: {len(files)} 文件, {total_errors} 错误")
    if WARNINGS:
        print(f"        {len(WARNINGS)} 警告")
    print(f"{'=' * 60}")

    sys.exit(0 if total_errors == 0 else 1)


if __name__ == "__main__":
    main()
