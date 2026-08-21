#!/usr/bin/env python3
"""
JMeter 压测执行与性能报告生成脚本

逐场景串行执行 .jmx → 解析 .jtl 结果 → 与 thresholds 比对 → 生成 HTML 报告。

每个场景（.jmx）独立启动一次 jmeter 进程，避免不同并发/时长场景互相干扰，
保证各场景指标独立准确。

用法:
    python run_perf.py --mode baseline           # 全量模式（默认）
    python run_perf.py --mode diff               # 增量模式
    python run_perf.py -k "perf_auth_001"        # 只跑指定场景
    python run_perf.py --jmx-dir <dir> --output <dir>  # 显式指定路径
"""
import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = SKILL_DIR / "template" / "perf_report_template.html"

MODE_PATHS = {
    "baseline": {
        "jmx_dir": PROJECT_ROOT / "tests" / "baseline" / "generated" / "api-perf",
        "output_dir": PROJECT_ROOT / "tests" / "baseline" / "report" / "api-perf",
    },
    "diff": {
        "jmx_dir": PROJECT_ROOT / "tests" / "diff" / "generated" / "api-perf",
        "output_dir": PROJECT_ROOT / "tests" / "diff" / "report" / "api-perf",
    },
}

LOGIN_LABEL = "login"


# ═══════════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════════

def find_jmeter() -> str:
    config_path = PROJECT_ROOT / "config.yaml"
    if config_path.exists():
        import yaml
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        tool_path = config.get("tools", {}).get("jmeter", "")
        if tool_path:
            candidates = [
                os.path.join(tool_path, "jmeter.bat"),
                os.path.join(tool_path, "jmeter.cmd"),
                os.path.join(tool_path, "jmeter"),
            ]
            for c in candidates:
                if os.path.exists(c):
                    return c
    return shutil.which("jmeter") or "jmeter"


def load_manifest(jmx_dir: str) -> dict:
    manifest_path = os.path.join(jmx_dir, "_scenarios.json")
    if not os.path.exists(manifest_path):
        return {}
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    result = {}
    for sc in data.get("scenarios", []):
        result[sc["jmx"]] = sc
    return result


def discover_jmx_files(jmx_dir: str) -> list:
    files = sorted(Path(jmx_dir).glob("*.jmx"))
    return [f.name for f in files]


def _extract_sc_id_from_jmx(jmx_path) -> str:
    """从 jmx 中提取主请求 HTTPSamplerProxy 的 testname 作为场景 id"""
    import xml.etree.ElementTree as ET
    try:
        tree = ET.parse(jmx_path)
    except Exception:
        return None
    for sampler in tree.iter("HTTPSamplerProxy"):
        name = (sampler.get("testname") or "").strip()
        if name and name.lower() not in ("login", LOGIN_LABEL):
            return name
    return None


def percentile(sorted_vals, p):
    """线性插值百分位数"""
    if not sorted_vals:
        return 0.0
    k = (len(sorted_vals) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(sorted_vals) - 1)
    if f == c:
        return float(sorted_vals[f])
    return float(sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f))


def run_jmeter(jmeter: str, jmx_path: str, jtl_path: str, timeout: int) -> tuple:
    cmd = [
        jmeter, "-n",
        "-t", jmx_path,
        "-l", jtl_path,
        "-Jjmeter.save.saveservice.print_field_names=true",
        "-Jjmeter.save.saveservice.output_format=csv",
    ]
    start = time.time()
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True,
                            timeout=timeout, encoding="utf-8", errors="replace")
    elapsed = round(time.time() - start, 2)
    return result.returncode, elapsed, result.stdout, result.stderr


def parse_jtl(jtl_path: str, scenario_id: str) -> dict:
    """解析 .jtl，统计主请求（label == scenario_id）样本指标"""
    if not os.path.exists(jtl_path):
        return None

    elapsed_list = []
    success_count = 0
    samples = 0
    time_stamps = []

    with open(jtl_path, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return None

        idx = {}
        for i, col in enumerate(header):
            idx[col.strip()] = i
        if "elapsed" not in idx or "label" not in idx or "success" not in idx:
            return None

        for row in reader:
            if len(row) <= idx["label"]:
                continue
            label = row[idx["label"]].strip()
            if label != scenario_id:
                continue
            samples += 1
            try:
                elapsed_list.append(float(row[idx["elapsed"]]))
            except (ValueError, IndexError):
                pass
            try:
                if row[idx["success"]].strip().lower() == "true":
                    success_count += 1
            except IndexError:
                pass
            if "timeStamp" in idx:
                try:
                    time_stamps.append(float(row[idx["timeStamp"]]))
                except (ValueError, IndexError):
                    pass

    if samples == 0:
        return None

    sorted_elapsed = sorted(elapsed_list)
    actual_duration = 0.0
    if len(time_stamps) >= 2:
        actual_duration = (max(time_stamps) - min(time_stamps)) / 1000.0

    return {
        "samples": samples,
        "avg": round(sum(sorted_elapsed) / len(sorted_elapsed), 2),
        "min": round(sorted_elapsed[0], 2),
        "max": round(sorted_elapsed[-1], 2),
        "p50": round(percentile(sorted_elapsed, 50), 2),
        "p90": round(percentile(sorted_elapsed, 90), 2),
        "p95": round(percentile(sorted_elapsed, 95), 2),
        "p99": round(percentile(sorted_elapsed, 99), 2),
        "error_rate": round(1 - success_count / samples, 4),
        "rps": round(samples / actual_duration, 2) if actual_duration > 0 else 0.0,
    }


def check_thresholds(metrics: dict, thresholds: dict) -> list:
    """比对阈值，返回未达标项列表"""
    violations = []
    rules = [
        ("avg", "avg", "ms", False),
        ("p50", "p50", "ms", False),
        ("p90", "p90", "ms", False),
        ("p95", "p95", "ms", False),
        ("p99", "p99", "ms", False),
        ("min", "min", "ms", False),
        ("max", "max", "ms", False),
        ("error_rate", "error_rate", "", False),
        ("min_rps", "rps", "req/s", True),  # True = 实际须 >= 阈值
    ]
    for th_key, metric_key, unit, is_lower_bound in rules:
        if th_key not in thresholds or thresholds[th_key] is None:
            continue
        threshold = float(thresholds[th_key])
        actual = metrics.get(metric_key, 0.0)
        if is_lower_bound:
            if actual < threshold:
                violations.append({"metric": th_key, "threshold": threshold,
                                   "actual": actual, "unit": unit})
        else:
            if actual > threshold:
                violations.append({"metric": th_key, "threshold": threshold,
                                   "actual": actual, "unit": unit})
    return violations


# ═══════════════════════════════════════════════════════════════
# 报告生成
# ═══════════════════════════════════════════════════════════════

def build_summary_cards(results: list) -> str:
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "pass")
    failed = total - passed
    total_samples = sum(r["metrics"]["samples"] for r in results if r.get("metrics"))
    avg_p95 = 0.0
    avg_error = 0.0
    cnt = 0
    for r in results:
        if r.get("metrics"):
            avg_p95 += r["metrics"]["p95"]
            avg_error += r["metrics"]["error_rate"]
            cnt += 1
    if cnt:
        avg_p95 /= cnt
        avg_error /= cnt
    pass_rate = round(passed / total * 100, 1) if total else 0

    return f"""
    <div class="summary-grid">
        <div class="card total"><div class="card-icon">&#9733;</div>
            <div class="card-value">{total}</div><div class="card-label">场景数</div></div>
        <div class="card passed"><div class="card-icon">&#10003;</div>
            <div class="card-value">{passed}</div><div class="card-label">达标</div></div>
        <div class="card failed"><div class="card-icon">&#10007;</div>
            <div class="card-value">{failed}</div><div class="card-label">不达标</div></div>
        <div class="card total"><div class="card-icon">&#8644;</div>
            <div class="card-value">{total_samples}</div><div class="card-label">总请求数</div></div>
        <div class="card time"><div class="card-icon">&#9203;</div>
            <div class="card-value">{avg_p95:.0f}ms</div><div class="card-label">平均 P95</div></div>
        <div class="card errors"><div class="card-icon">&#9888;</div>
            <div class="card-value">{avg_error * 100:.2f}%</div><div class="card-label">平均错误率</div></div>
        <div class="card rate"><div class="card-icon">&#128200;</div>
            <div class="card-value">{pass_rate}%</div><div class="card-label">达标率</div></div>
    </div>"""


def _fmt_ms(v) -> str:
    return f"{v:.0f}ms"


def _esc(text) -> str:
    return (str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;").replace("'", "&#39;"))


def _pretty(obj) -> str:
    try:
        return json.dumps(obj, ensure_ascii=False, indent=2)
    except Exception:
        return str(obj)


def _meta_fields(meta: dict, sc_id: str) -> dict:
    """从 manifest 元数据提取报告展示字段"""
    return {
        "title": meta.get("title", sc_id),
        "description": meta.get("description", ""),
        "method": meta.get("method", ""),
        "path": meta.get("path", ""),
        "request": meta.get("request", {}),
        "thresholds": meta.get("thresholds", {}),
    }


def _build_perf_detail_html(r: dict) -> str:
    """场景详情面板：说明 / 请求 / 负载配置 / 阈值对比 / 未达标项"""
    parts = []
    desc = r.get("description", "")
    if desc:
        parts.append(f'<div class="d-section"><div class="d-title">场景说明</div>'
                     f'<div class="d-desc">{_esc(desc)}</div></div>')

    req = r.get("request") or {}
    step_items = []
    method = r.get("method", "")
    path = r.get("path", "")
    if method or path:
        step_items.append(f'<li><b class="d-req">{_esc(method)}</b> {_esc(path)}</li>')
    if req.get("path_params"):
        step_items.append(f'<li>路径参数<pre>{_esc(_pretty(req["path_params"]))}</pre></li>')
    if req.get("query"):
        step_items.append(f'<li>Query 参数<pre>{_esc(_pretty(req["query"]))}</pre></li>')
    if req.get("headers"):
        step_items.append(f'<li>请求头<pre>{_esc(_pretty(req["headers"]))}</pre></li>')
    if req.get("body"):
        step_items.append(f'<li>请求体<pre>{_esc(_pretty(req["body"]))}</pre></li>')
    if step_items:
        parts.append(f'<div class="d-section"><div class="d-title">请求</div>'
                     f'<ul class="d-steps">{"".join(step_items)}</ul></div>')

    load = r.get("load") or {}
    if load:
        parts.append(f'<div class="d-section"><div class="d-title">负载配置</div>'
                     f'<pre>{_esc(_pretty(load))}</pre></div>')

    m = r.get("metrics") or {}
    thresholds = r.get("thresholds") or {}
    if thresholds:
        mapping = (
            ("p95", "P95", f"{m.get('p95', '-')}ms" if m else "-"),
            ("error_rate", "错误率", f"{m['error_rate'] * 100:.2f}%" if m else "-"),
            ("min_rps", "RPS", f"{m.get('rps', '-')}" if m else "-"),
        )
        rows_html = []
        for key, label, actual in mapping:
            if key not in thresholds:
                continue
            limit = thresholds[key]
            op = ">=" if key == "min_rps" else "<="
            try:
                actual_num = float(str(actual).rstrip("ms%"))
            except Exception:
                actual_num = None
            ok = None
            if actual_num is not None:
                ok = actual_num >= limit if key == "min_rps" else actual_num <= limit
            mark = ("<span class='t-pass'>&#10003; 达标</span>" if ok
                    else "<span class='t-fail'>&#10007; 超限</span>" if ok is False else "—")
            rows_html.append(
                f'<tr><td class="d-k">{_esc(label)}</td>'
                f'<td>阈值 {op} {_esc(limit)}</td>'
                f'<td>实际 {_esc(actual)}</td><td>{mark}</td></tr>')
        if rows_html:
            parts.append(f'<div class="d-section"><div class="d-title">阈值对比</div>'
                         f'<table class="d-table">{"".join(rows_html)}</table></div>')

    if r.get("violations"):
        v_text = "；".join(
            f"{v['metric']}={v['actual']}{v['unit']}"
            f"(阈值{'>=' if v['metric'] == 'min_rps' else '<='}{v['threshold']})"
            for v in r["violations"])
        parts.append(f'<div class="d-section"><div class="d-title">未达标项</div>'
                     f'<div class="d-desc fail-text">{_esc(v_text)}</div></div>')

    return "".join(parts)


def build_scenario_rows(results: list) -> str:
    rows = []
    for r in results:
        m = r.get("metrics") or {}
        load = r.get("load", {})
        status = r["status"]
        status_text = "达标" if status == "pass" else "不达标"
        badge = "badge-passed" if status == "pass" else "badge-failed"

        violations = r.get("violations", [])
        v_text = "；".join(
            f"{v['metric']}={v['actual']}{v['unit']}(阈值{'>=' if v['metric']=='min_rps' else '<='}{v['threshold']})"
            for v in violations
        ) if violations else "—"

        if m:
            cells = (
                f"<td class=\"num\">{load.get('users', '-')}</td>"
                f"<td class=\"num\">{load.get('duration', '-')}s</td>"
                f"<td class=\"num\">{m['samples']}</td>"
                f"<td class=\"num\">{_fmt_ms(m['avg'])}</td>"
                f"<td class=\"num\">{_fmt_ms(m['min'])}</td>"
                f"<td class=\"num\">{_fmt_ms(m['max'])}</td>"
                f"<td class=\"num\">{_fmt_ms(m['p90'])}</td>"
                f"<td class=\"num\">{_fmt_ms(m['p95'])}</td>"
                f"<td class=\"num\">{_fmt_ms(m['p99'])}</td>"
                f"<td class=\"num\">{m['rps']}</td>"
                f"<td class=\"num\">{m['error_rate'] * 100:.2f}%</td>"
            )
        else:
            cells = f"<td colspan=\"11\" class=\"num\">无样本数据（执行失败）</td>"

        detail = _build_perf_detail_html(r)

        rows.append(f"""
        <tr class="row-{status}" onclick="togglePerfDetail(this)">
            <td class="id">{r['id']}</td>
            <td class="title" title="{_esc(r['title'])}">
                <div class="case-title">{_esc(r['title'])}</div>
            </td>
            <td class="method">{r.get('method', '')}</td>
            {cells}
            <td><span class="badge {badge}">{status_text}</span></td>
            <td class="vio" title="{_esc(v_text)}">{_esc(v_text[:60])}</td>
        </tr>
        <tr class="perf-detail-row" style="display:none;">
            <td colspan="16"><div class="perf-detail">{detail}</div></td>
        </tr>""")

    return "\n".join(rows)


def build_chart_data(results: list) -> str:
    labels = []
    p95 = []
    rps = []
    err = []
    colors = []
    for r in results:
        if not r.get("metrics"):
            continue
        labels.append(r["id"][-7:])
        p95.append(r["metrics"]["p95"])
        rps.append(r["metrics"]["rps"])
        err.append(round(r["metrics"]["error_rate"] * 100, 2))
        colors.append("#22d695" if r["status"] == "pass" else "#ff4d6a")
    return json.dumps({
        "labels": labels,
        "p95": {"data": p95, "colors": colors},
        "rps": rps,
        "error_rate": err,
    }, ensure_ascii=False)


def generate_report(results: list, output_dir: str, jmx_dir: str) -> str:
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"模板文件不存在: {TEMPLATE_PATH}")
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = template.replace("{{REPORT_TIME}}", report_time)
    html = html.replace("{{SUMMARY_CARDS}}", build_summary_cards(results))
    html = html.replace("{{SCENARIO_TABLE}}", build_scenario_rows(results))
    html = html.replace("{{CHART_DATA}}", build_chart_data(results))
    html = html.replace("{{SCENARIO_COUNT}}", str(len(results)))

    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(output_dir, f"report_{timestamp}.html")
    latest_path = os.path.join(output_dir, "latest.html")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)
    shutil.copy(report_path, latest_path)

    return os.path.abspath(report_path)


# ═══════════════════════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════════════════════

def check_windows_ports():
    """Windows 下检查 TCP 动态端口范围，不足时警告（高并发短连接易 BindException）"""
    if sys.platform != "win32":
        return
    try:
        out = subprocess.run(
            ["netsh", "int", "ipv4", "show", "dynamicport", "tcp"],
            capture_output=True, text=True, timeout=10,
        ).stdout
        m = re.search(r"Number of Ports\s*:\s*(\d+)", out)
        if m and int(m.group(1)) < 20000:
            print("[run_perf] 警告: TCP 动态端口数过少 "
                  f"({m.group(1)} < 20000)，高并发压测易出现 "
                  "BindException: Address already in use")
            print("[run_perf]         建议（管理员）: "
                  "netsh int ipv4 set dynamicport tcp start=1025 num=64510")
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description="JMeter 压测执行与报告生成")
    parser.add_argument("--mode", choices=["baseline", "diff"], default="baseline",
                        help="模式: baseline=全量, diff=增量 (默认: baseline)")
    parser.add_argument("--jmx-dir", default=None, help="jmx 目录（优先级高于 --mode）")
    parser.add_argument("-k", "--keyword", default=None, help="只运行 jmx 文件名含关键字的场景")
    parser.add_argument("--output", default=None, help="报告输出目录（优先级高于 --mode）")
    parser.add_argument("--report-only", action="store_true",
                        help="仅用输出目录 .cache 下已有 jtl 重新生成报告，不执行压测")
    args = parser.parse_args()

    mode_config = MODE_PATHS[args.mode]
    jmx_dir = args.jmx_dir if args.jmx_dir else str(mode_config["jmx_dir"])
    output_dir = args.output if args.output else str(mode_config["output_dir"])

    if not os.path.isdir(jmx_dir):
        print(f"[run_perf] 错误: jmx 目录不存在: {jmx_dir}")
        sys.exit(1)

    check_windows_ports()

    jmeter = find_jmeter()
    manifest = load_manifest(jmx_dir)
    jmx_files = discover_jmx_files(jmx_dir)

    if args.keyword:
        jmx_files = [f for f in jmx_files if args.keyword in f]

    if not jmx_files:
        print(f"[run_perf] 错误: 未找到 .jmx 文件: {jmx_dir}")
        sys.exit(1)

    cache_dir = os.path.join(output_dir, ".cache")
    os.makedirs(cache_dir, exist_ok=True)


    if args.report_only:
        print(f"\n{'=' * 60}")
        print(f"[run_perf] 报告重建模式（--report-only，不执行压测）")
        print(f"[run_perf] jmx 目录: {jmx_dir} | jtl 缓存: {cache_dir}")
        print(f"{'=' * 60}\n")
        results = []
        for jmx_file in jmx_files:
            meta = manifest.get(jmx_file, {})
            sc_id = meta.get("id") or _extract_sc_id_from_jmx(os.path.join(jmx_dir, jmx_file)) \
                or os.path.splitext(jmx_file)[0]
            jtl_path = os.path.join(cache_dir, f"result_{sc_id}.jtl")
            metrics = parse_jtl(jtl_path, sc_id)
            thresholds = meta.get("thresholds", {})
            violations = check_thresholds(metrics, thresholds) if metrics else []
            status = "pass" if metrics and not violations else "fail"
            rec = {"jmx": jmx_file, "id": sc_id, "status": status,
                   "metrics": metrics, "violations": violations,
                   "load": meta.get("load", {}), **_meta_fields(meta, sc_id)}
            results.append(rec)
            if metrics:
                print(f"  [{sc_id}] samples={metrics['samples']} p95={metrics['p95']}ms "
                      f"rps={metrics['rps']} err={metrics['error_rate'] * 100:.2f}% -> "
                      f"{'达标' if status == 'pass' else '不达标 (' + str(len(violations)) + '项)'}")
            else:
                print(f"  [{sc_id}] 无 jtl 缓存，跳过")
        report_path = generate_report(results, output_dir, jmx_dir)
        print(f"[run_perf] 报告已生成:")
        print(f"  主文件: {report_path}")
        print(f"  快捷方式: {os.path.join(os.path.abspath(output_dir), 'latest.html')}")
        return report_path

    print(f"\n{'=' * 60}")
    print(f"[run_perf] 开始执行性能压测（逐场景串行）")
    print(f"[run_perf] JMeter: {jmeter}")
    print(f"[run_perf] jmx 目录: {jmx_dir}")
    print(f"[run_perf] 发现 {len(jmx_files)} 个场景")
    print(f"{'=' * 60}\n")

    results = []
    total_start = time.time()

    for i, jmx_file in enumerate(jmx_files):
        meta = manifest.get(jmx_file, {})
        sc_id = meta.get("id") or _extract_sc_id_from_jmx(os.path.join(jmx_dir, jmx_file)) \
            or os.path.splitext(jmx_file)[0]
        load = meta.get("load", {})
        duration = int(load.get("duration", 60)) if isinstance(load.get("duration"), int) else 60
        ramp_up = int(load.get("ramp_up", 10)) if isinstance(load.get("ramp_up"), int) else 10
        timeout = duration + ramp_up + 120

        jmx_path = os.path.join(jmx_dir, jmx_file)
        jtl_path = os.path.join(cache_dir, f"result_{sc_id}.jtl")

        print(f"  [{i + 1}/{len(jmx_files)}] {jmx_file} ({sc_id}) "
              f"users={load.get('users')} duration={duration}s ...")

        try:
            code, elapsed, stdout, stderr = run_jmeter(jmeter, jmx_path, jtl_path, timeout)
        except subprocess.TimeoutExpired:
            print(f"        超时（>{timeout}s）")
            results.append({"jmx": jmx_file, "id": sc_id, "status": "error",
                            "metrics": None, "violations": [],
                            "load": load, **_meta_fields(meta, sc_id)})
            continue

        metrics = parse_jtl(jtl_path, sc_id)
        if metrics is None:
            print(f"        jmeter exit={code}, 无有效样本")
            if stderr:
                for line in stderr.strip().split("\n")[-3:]:
                    print(f"         {line}")
            results.append({"jmx": jmx_file, "id": sc_id, "status": "error",
                            "metrics": None, "violations": [],
                            "load": load, **_meta_fields(meta, sc_id)})
            continue

        thresholds = meta.get("thresholds", {})
        violations = check_thresholds(metrics, thresholds)
        status = "pass" if not violations else "fail"
        m = metrics
        print(f"        samples={m['samples']} avg={m['avg']}ms p95={m['p95']}ms "
              f"rps={m['rps']} err={m['error_rate'] * 100:.2f}% -> "
              f"{'达标' if status == 'pass' else '不达标 (' + str(len(violations)) + '项)'}")

        results.append({"jmx": jmx_file, "id": sc_id, "status": status,
                        "metrics": metrics, "violations": violations,
                        "load": load, **_meta_fields(meta, sc_id)})

    total_elapsed = round(time.time() - total_start, 2)

    print(f"\n{'=' * 60}")
    passed = sum(1 for r in results if r["status"] == "pass")
    print(f"[run_perf] 压测完成: {len(results)} 个场景, {passed} 达标, "
          f"{len(results) - passed} 不达标 | 总耗时 {total_elapsed}s")
    print(f"{'=' * 60}\n")

    report_path = generate_report(results, output_dir, jmx_dir)
    print(f"[run_perf] 报告已生成:")
    print(f"  主文件: {report_path}")
    print(f"  快捷方式: {os.path.join(os.path.abspath(output_dir), 'latest.html')}")
    return report_path


if __name__ == "__main__":
    main()
