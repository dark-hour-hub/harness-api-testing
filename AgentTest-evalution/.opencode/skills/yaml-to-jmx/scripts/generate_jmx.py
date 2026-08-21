#!/usr/bin/env python3
"""
性能场景 YAML -> JMeter .jmx 脚本生成器

从 perf-scenario.yaml 目录读取性能场景，每个场景生成一个独立 .jmx（单 ThreadGroup），
便于执行端逐场景串行压测（避免不同并发互相干扰）。同时输出 _scenarios.json 清单，
供 perf-runner 读取 thresholds / load 元信息。

认证场景自动生成「OnceOnlyController + 登录请求 + JSON Extractor 提取 token」，
主请求通过 ${token} 引用。

支持两种模式:
  --mode baseline  → 全量模式（默认）
  --mode diff      → 增量模式

用法:
  python generate_jmx.py --mode baseline
  python generate_jmx.py --mode diff
  python generate_jmx.py --yaml-dir <dir> --output-dir <dir>
"""

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML 未安装，请执行: pip install pyyaml")
    sys.exit(2)

# jmx_fragments.py 位于 template/ 目录
_TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "template"
sys.path.insert(0, str(_TEMPLATE_DIR))
import jmx_fragments as frag  # noqa: E402

# 项目根目录（scripts/ 向上 4 级）
_PROJECT_ROOT = Path(__file__).resolve().parents[4]

MODE_PATHS = {
    "baseline": {
        "yaml_dir": "tests/baseline/_workflow/05-perf-scenarios",
        "output_dir": "tests/baseline/generated/api-perf",
    },
    "diff": {
        "yaml_dir": "tests/diff/_workflow/03-diff-perf-scenarios",
        "output_dir": "tests/diff/generated/api-perf",
    },
}

LOGIN_LABEL = "login"  # 登录请求在 .jtl 中的固定 label，统计时排除


# ═══════════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════════

def parse_base_url(base_url: str) -> tuple:
    """解析 base_url → (protocol, domain, port)"""
    parsed = urlparse(base_url)
    protocol = parsed.scheme or "http"
    domain = parsed.hostname or ""
    if parsed.port:
        port = str(parsed.port)
    else:
        port = "443" if protocol == "https" else "80"
    return protocol, domain, port


def _headers_to_list(headers) -> list:
    """YAML headers 列表 → [(name, value)]，跳过缺字段的条目"""
    result = []
    for h in headers or []:
        if isinstance(h, dict) and h.get("name"):
            result.append((h["name"], h.get("value", "")))
    return result


def _apply_path_params(path: str, path_params: dict) -> str:
    for k, v in (path_params or {}).items():
        path = path.replace("{" + str(k) + "}", str(v))
    return path


def _dump_json(obj) -> str:
    if obj is None:
        return None
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


# ═══════════════════════════════════════════════════════════════
# 单个场景 → 完整 jmx
# ═══════════════════════════════════════════════════════════════

def build_single_jmx(scenario: dict, module_name: str, source_file: str,
                     public_headers, auth_headers, auth_setup: dict,
                     protocol, domain, port) -> str:
    """生成单个场景的完整 jmx 文档字符串"""
    sc_id = scenario.get("id", "scenario")
    title = scenario.get("title", sc_id)
    method = scenario.get("method", "GET").upper()
    path = _apply_path_params(scenario.get("path", ""),
                              scenario.get("request", {}).get("path_params"))
    request = scenario.get("request", {})
    load = scenario.get("load", {})
    auth = scenario.get("auth", {}) or {}
    auth_required = bool(auth.get("required", False))

    users = int(load.get("users", 1))
    duration = int(load.get("duration", 60))
    ramp_up = int(load.get("ramp_up", max(1, users // 10)))
    loops = int(load.get("loops", -1))

    body = None
    query = None
    if method in ("POST", "PUT", "PATCH"):
        body = _dump_json(request.get("body"))
    else:
        query = request.get("query", {})
        if not isinstance(query, dict):
            query = {}

    # 场景特有头（同名覆盖全局 public_headers）
    extra_headers = _headers_to_list(request.get("headers"))
    merged_public = dict(public_headers)
    for name, value in extra_headers:
        merged_public[name] = value

    parts = []
    parts.append(frag.header())
    parts.append(frag.test_plan(f"{module_name} - {title}", comment=f"来源: {source_file}"))
    parts.append(frag.thread_group(title, users, ramp_up, duration, loops))

    # 公共请求头（作用整个 ThreadGroup）
    parts.append(frag.header_manager("公共请求头", list(merged_public.items())))

    # 认证：每个线程登录一次 + 提取 token
    if auth_required:
        login_body = _dump_json(auth_setup.get("login_body"))
        login_headers = _headers_to_list(auth_setup.get("login_headers"))

        parts.append(frag.once_only_controller("登录（每线程一次）"))
        if login_headers:
            parts.append(frag.header_manager("登录请求头", login_headers))
        parts.append(frag.http_sampler(
            LOGIN_LABEL, protocol, domain, port,
            str(auth_setup.get("login_endpoint", "")),
            auth_setup.get("login_method", "POST").upper(),
            body=login_body,
        ))
        parts.append(frag.json_extractor(
            "提取token", "token",
            str(auth_setup.get("token_jsonpath", "$.data.token")),
            str(auth_setup.get("token_default", "NOT_FOUND")),
        ))
        parts.append(frag.close_tree(6))  # 关闭登录 sampler hashTree
        parts.append(frag.close_tree(6))  # 关闭 once_only hashTree

    # 主请求（testname = scenario id，作为 .jtl 的 label）
    parts.append(frag.http_sampler(sc_id, protocol, domain, port, path, method,
                                  body=body, query=query))
    if auth_required and auth_headers:
        parts.append(frag.header_manager("认证请求头", auth_headers))
    parts.append(frag.close_tree(6))  # 关闭主请求 sampler hashTree
    parts.append(frag.close_tree(6))  # 关闭 ThreadGroup hashTree
    parts.append(frag.close_tree(4))  # 关闭 TestPlan hashTree
    parts.append(frag.footer())

    return "".join(parts)


def validate_jmx(jmx_path: Path) -> bool:
    try:
        ET.parse(str(jmx_path))
        return True
    except ET.ParseError as e:
        print(f"  [FAIL] {jmx_path.name}: XML 解析失败: {e}")
        return False


def generate_jmx(yaml_path: Path, output_dir: Path, manifest: list) -> int:
    """从单个 YAML 生成多个 .jmx（每场景一个），写入 manifest 清单，返回场景数"""
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    module = data.get("module", yaml_path.stem)
    module_name = data.get("module_name", module)
    base_url = data.get("base_url", "")
    headers_config = data.get("headers_config", {})
    auth_setup = data.get("auth_setup", {}) or {}
    scenarios = data.get("scenarios", [])

    if not scenarios:
        print(f"  SKIP: {yaml_path.name} --- 无性能场景")
        return 0

    protocol, domain, port = parse_base_url(base_url)
    public_headers = _headers_to_list(headers_config.get("public_headers"))
    auth_headers = _headers_to_list(headers_config.get("auth_headers"))

    output_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for sc in scenarios:
        sc_id = sc.get("id")
        if not sc_id:
            print(f"  WARN: {yaml_path.name} --- 存在缺少 id 的场景，已跳过")
            continue
        jmx_content = build_single_jmx(
            sc, module_name, yaml_path.name,
            public_headers, auth_headers, auth_setup,
            protocol, domain, port,
        )
        jmx_name = f"{sc_id.lower()}.jmx"
        (output_dir / jmx_name).write_text(jmx_content, encoding="utf-8")

        manifest.append({
            "jmx": jmx_name,
            "id": sc_id,
            "title": sc.get("title", sc_id),
            "description": sc.get("description", ""),
            "module": module,
            "module_name": module_name,
            "method": sc.get("method", "").upper(),
            "path": sc.get("path", ""),
            "request": sc.get("request", {}),
            "load": sc.get("load", {}),
            "thresholds": sc.get("thresholds", {}),
        })
        count += 1

    return count


def write_manifest(manifest: list, output_dir: Path) -> Path:
    manifest_path = output_dir / "_scenarios.json"
    manifest_path.write_text(
        json.dumps({"scenarios": manifest}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return manifest_path


def main():
    parser = argparse.ArgumentParser(description="性能场景 YAML -> JMeter .jmx 生成器")
    parser.add_argument("--mode", choices=["baseline", "diff"], default="baseline",
                        help="baseline=全量模式（默认）, diff=增量模式")
    parser.add_argument("--yaml-dir", default=None, help="YAML 场景目录（覆盖 --mode）")
    parser.add_argument("--output-dir", default=None, help="输出目录（覆盖 --mode）")
    parser.add_argument("--no-verify", action="store_true", help="跳过 XML 校验")
    args = parser.parse_args()

    mode_config = MODE_PATHS[args.mode]
    yaml_dir_rel = args.yaml_dir if args.yaml_dir else mode_config["yaml_dir"]
    output_dir_rel = args.output_dir if args.output_dir else mode_config["output_dir"]

    yaml_dir = _PROJECT_ROOT / yaml_dir_rel
    output_dir = _PROJECT_ROOT / output_dir_rel

    if not yaml_dir.exists():
        print(f"ERROR: YAML 场景目录不存在: {yaml_dir}")
        sys.exit(1)

    yaml_files = sorted(yaml_dir.glob("*.yaml"))
    if not yaml_files:
        print(f"WARNING: 目录中无 .yaml 文件: {yaml_dir}")
        sys.exit(0)

    print(f"YAML 场景目录: {yaml_dir}")
    print(f"输出目录: {output_dir}")
    print(f"发现 {len(yaml_files)} 个 YAML 文件\n")

    manifest = []
    total_scenarios = 0
    failed = 0
    for yf in yaml_files:
        n = generate_jmx(yf, output_dir, manifest)
        total_scenarios += n
        print(f"  [OK] {yf.name} --- {n} 个场景 -> {n} 个 jmx")

    if not args.no_verify:
        print("\nXML 校验...")
        for jmx in sorted(output_dir.glob("*.jmx")):
            if not validate_jmx(jmx):
                failed += 1

    manifest_path = write_manifest(manifest, output_dir)
    print(f"\n清单已写入: {manifest_path.name} ({len(manifest)} 个场景)")
    print(f"生成完成: {total_scenarios} 个场景 / {len(manifest)} 个 jmx")
    if failed:
        print(f"!!! {failed} 个 jmx 文件 XML 校验失败 !!!")
        sys.exit(1)


if __name__ == "__main__":
    main()
