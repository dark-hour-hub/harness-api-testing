"""
UI 测试执行与报告生成脚本
逐 feature 隔离执行 pytest（pytest-bdd + pytest-playwright）→ 合并 JUnit XML → 生成含截图的 HTML 报告

用法:
    python run_ui.py --mode baseline
    python run_ui.py --mode diff
    python run_ui.py --test-path <dir> --output <dir>
    python run_ui.py --headed          # 有头模式（调试用）
    python run_ui.py -k "test_login"   # 运行特定模块
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html import escape as html_escape
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = SKILL_DIR / "template" / "ui_report_template.html"

MODE_PATHS = {
    "baseline": {
        "test_path": PROJECT_ROOT / "tests" / "baseline" / "generated" / "ui-test",
        "output_dir": PROJECT_ROOT / "tests" / "baseline" / "report" / "ui-test",
    },
    "diff": {
        "test_path": PROJECT_ROOT / "tests" / "diff" / "generated" / "ui-test",
        "output_dir": PROJECT_ROOT / "tests" / "diff" / "report" / "ui-test",
    },
}


def find_python() -> str:
    config_path = PROJECT_ROOT / "config.yaml"
    if config_path.exists():
        import yaml
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        tool_path = config.get("tools", {}).get("python", "")
        if tool_path:
            for candidate in (os.path.join(tool_path, "python.exe"), os.path.join(tool_path, "python")):
                if os.path.exists(candidate):
                    return candidate
    return shutil.which("python") or "python"


def load_frontend_url() -> str:
    config_path = PROJECT_ROOT / "config.yaml"
    if not config_path.exists():
        return ""
    try:
        import yaml
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        env_name = config.get("current_environment", "dev")
        frontends = config.get("environments", {}).get(env_name, {}).get("frontend", [])
        for fe in frontends:
            url = (fe or {}).get("url", "")
            if url:
                return url
    except Exception:
        pass
    return ""


def discover_test_files(test_dir: str) -> list:
    if os.path.isfile(test_dir):
        return [test_dir]
    return [str(f) for f in sorted(Path(test_dir).glob("test_*.py"))]


def run_pytest_file(test_file: str, junit_output: str, base_url: str, screenshot_dir: str,
                    headed: bool = False, keyword: str = None, tags: str = None) -> tuple:
    python = find_python()
    cmd = [python, "-m", "pytest", test_file, "-v", "--tb=short", "--browser", "chromium"]
    if base_url:
        cmd.extend(["--base-url", base_url])
    if headed:
        cmd.append("--headed")
    if keyword:
        cmd.extend(["-k", keyword])
    if tags:
        cmd.extend(["-m", tags])
    cmd.append(f"--junitxml={junit_output}")

    env = os.environ.copy()
    env["UI_BASE_URL"] = base_url
    env["UI_SCREENSHOT_DIR"] = screenshot_dir

    start = time.time()
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True,
                            encoding="utf-8", errors="replace", env=env)
    elapsed = round(time.time() - start, 2)
    return result.returncode, elapsed, result.stdout, result.stderr


def load_feature_scenarios(feature_dir: str) -> dict:
    """解析所有 .feature 文件：scenario 名 -> {feature, steps:[...]}

    steps 保留原始 Gherkin 步骤文本（Given/When/Then/And/But）。
    """
    scenarios = {}
    feature_dir = Path(feature_dir)
    if not feature_dir.is_dir():
        return scenarios
    for fp in sorted(feature_dir.glob("*.feature")):
        try:
            lines = fp.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        current = None
        for line in lines:
            s = line.strip()
            if not s or s.startswith("#") or s.startswith("@") \
                    or s.startswith("Feature:") or s.startswith("Background:"):
                continue
            if s.startswith("Scenario:") or s.startswith("Example:") \
                    or s.startswith("Scenario Outline:"):
                current = s.split(":", 1)[1].strip()
                scenarios[current] = {"feature": fp.name, "steps": []}
                continue
            if current and (s.startswith("Given ") or s.startswith("When ")
                            or s.startswith("Then ") or s.startswith("And ")
                            or s.startswith("But ")):
                scenarios[current]["steps"].append(s)
    return scenarios


def _ui_case_scenario_name(case_name: str) -> str:
    """'test_create_agent[chromium]' -> 'create agent'"""
    base = case_name
    if base.startswith("test_"):
        base = base[5:]
    base = base.split("[", 1)[0]
    return base.replace("_", " ")


def enrich_ui_cases(cases: list, scenarios: dict) -> None:
    """把 feature 场景名与步骤文本挂到每个 case（场景名支持「英文（中文）」双语）"""
    for case in cases:
        sc_name = _ui_case_scenario_name(case["name"])
        matched = next(
            (k for k in scenarios if k == sc_name or k.startswith(sc_name + "（")),
            sc_name,
        )
        case["scenario_name"] = matched
        case["scenario"] = scenarios.get(matched) or {}


def _step_status_map(case: dict) -> dict:
    """从 junit property bdd_steps 提取 步骤名->状态"""
    return case.get("steps_result", {})


def parse_junit_xml(xml_path: str, module_name: str = "") -> dict:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    all_tests = all_failures = all_errors = all_skipped = 0
    all_time = 0.0
    for ts in root.findall("testsuite"):
        all_tests += int(ts.attrib.get("tests", 0))
        all_failures += int(ts.attrib.get("failures", 0))
        all_errors += int(ts.attrib.get("errors", 0))
        all_skipped += int(ts.attrib.get("skipped", 0))
        all_time += float(ts.attrib.get("time", 0))

    summary = {
        "tests": all_tests,
        "failures": all_failures,
        "errors": all_errors,
        "skipped": all_skipped,
        "time": round(all_time, 2),
    }
    summary["passed"] = summary["tests"] - summary["failures"] - summary["errors"] - summary["skipped"]

    suites = []
    all_cases = []
    for ts in root.findall("testsuite"):
        suite = {
            "name": module_name or ts.attrib.get("name", "Unknown"),
            "module": module_name,
            "tests": int(ts.attrib.get("tests", 0)),
            "failures": int(ts.attrib.get("failures", 0)),
            "errors": int(ts.attrib.get("errors", 0)),
            "skipped": int(ts.attrib.get("skipped", 0)),
            "time": round(float(ts.attrib.get("time", 0)), 2),
            "cases": [],
        }
        for tc in ts.findall("testcase"):
            case = {
                "name": tc.attrib.get("name", ""),
                "time": round(float(tc.attrib.get("time", 0)), 3),
                "status": "passed",
                "message": "",
                "trace": "",
                "screenshot": "",
                "element_hits": {},
                "db_asserts": [],
                "api_syncs": [],
            }
            # 读取 screenshot property（由 conftest 自动截图 hook 写入）
            props = tc.find("properties")
            if props is not None:
                for prop in props.findall("property"):
                    if prop.attrib.get("name") == "screenshot":
                        case["screenshot"] = prop.attrib.get("value", "")
                    elif prop.attrib.get("name") == "bdd_steps":
                        try:
                            steps = json.loads(prop.attrib.get("value", "[]"))
                            case["steps_result"] = {s["name"]: s["status"] for s in steps}
                        except Exception:
                            case["steps_result"] = {}
                    elif prop.attrib.get("name") == "element_hits":
                        try:
                            case["element_hits"] = json.loads(prop.attrib.get("value", "{}"))
                        except Exception:
                            case["element_hits"] = {}
                    elif prop.attrib.get("name") == "db_asserts":
                        try:
                            case["db_asserts"] = json.loads(prop.attrib.get("value", "[]"))
                        except Exception:
                            case["db_asserts"] = []
                    elif prop.attrib.get("name") == "api_syncs":
                        try:
                            case["api_syncs"] = json.loads(prop.attrib.get("value", "[]"))
                        except Exception:
                            case["api_syncs"] = []
            failure = tc.find("failure")
            error = tc.find("error")
            skipped = tc.find("skipped")
            if failure is not None:
                case["status"] = "failed"
                case["message"] = (failure.attrib.get("message", "") or "")[:500]
                case["trace"] = (failure.text or "")[:5000]
            elif error is not None:
                case["status"] = "error"
                case["message"] = (error.attrib.get("message", "") or "")[:500]
                case["trace"] = (error.text or "")[:5000]
            elif skipped is not None:
                case["status"] = "skipped"
                case["message"] = skipped.attrib.get("message", "")

            suite["cases"].append(case)
            all_cases.append(case)
        suites.append(suite)

    return {"summary": summary, "suites": suites, "cases": all_cases}


def merge_results(all_results: list, total_elapsed: float) -> dict:
    merged_cases = []
    merged_suites = []
    totals = dict(tests=0, failures=0, errors=0, skipped=0)
    for data in all_results:
        s = data["summary"]
        totals["tests"] += s["tests"]
        totals["failures"] += s["failures"]
        totals["errors"] += s["errors"]
        totals["skipped"] += s["skipped"]
        merged_suites.extend(data["suites"])
        merged_cases.extend(data["cases"])
    summary = dict(totals, time=round(total_elapsed, 2))
    summary["passed"] = summary["tests"] - summary["failures"] - summary["errors"] - summary["skipped"]
    return {"summary": summary, "suites": merged_suites, "cases": merged_cases}


def build_summary_cards(summary: dict) -> str:
    passed, failed = summary["passed"], summary["failures"]
    errors, skipped, total = summary["errors"], summary["skipped"], summary["tests"]
    pass_rate = round(passed / total * 100, 1) if total > 0 else 0
    if pass_rate >= 90: rate_color, rate_bg = "#10b981", "#ecfdf5"
    elif pass_rate >= 70: rate_color, rate_bg = "#f59e0b", "#fffbeb"
    else: rate_color, rate_bg = "#ef4444", "#fef2f2"
    return f"""
    <div class="summary-grid">
        <div class="card total"><div class="card-icon">&#9733;</div><div class="card-value">{total}</div><div class="card-label">场景总数</div></div>
        <div class="card passed"><div class="card-icon">&#10003;</div><div class="card-value">{passed}</div><div class="card-label">通过</div></div>
        <div class="card failed"><div class="card-icon">&#10007;</div><div class="card-value">{failed}</div><div class="card-label">失败</div></div>
        <div class="card errors"><div class="card-icon">&#9888;</div><div class="card-value">{errors}</div><div class="card-label">错误</div></div>
        <div class="card skipped"><div class="card-icon">&#8212;</div><div class="card-value">{skipped}</div><div class="card-label">跳过</div></div>
        <div class="card rate" style="background:{rate_bg}; border-color:{rate_color};"><div class="card-value" style="color:{rate_color};">{pass_rate}%</div><div class="card-label">通过率</div></div>
        <div class="card time"><div class="card-icon">&#9202;</div><div class="card-value">{summary['time']}s</div><div class="card-label">总耗时</div></div>
    </div>"""


def _clean_message(message: str) -> str:
    """从失败消息中提取简洁原因，去掉 AssertionError 前缀和可访问性树 dump"""
    if not message:
        return ""
    if "Actual value:" in message:
        message = message.split("Actual value:")[0]
    message = message.replace("AssertionError:", "").strip()
    message = re.sub(r"\s+", " ", message)
    return message[:300]


def _clean_trace(trace: str) -> str:
    """过滤堆栈：跳过 site-packages 内部帧（含帧体内联代码）和可访问性树 dump"""
    if not trace:
        return ""
    lines = []
    skip_tree = False
    skip_frame_body = False
    for line in trace.split("\n"):
        stripped = line.strip()
        # 可访问性树 dump：从 "Actual value" 起跳过缩进树
        if "Actual value:" in line:
            skip_tree = True
            continue
        if skip_tree:
            if stripped and not stripped.startswith("E ") and not line.startswith((" ", "\t")):
                skip_tree = False
            else:
                continue
        # 跳过 pytest/pluggy/playwright 内部帧（帧头 + 帧体内联代码）
        if skip_frame_body:
            if stripped.startswith("E ") or (line and not line.startswith(" ")):
                skip_frame_body = False
            else:
                continue
        if "site-packages" in line and not stripped.startswith("E "):
            skip_frame_body = True
            continue
        lines.append(line)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def _build_steps_panel(case: dict) -> str:
    """生成场景步骤面板：Given=前置 / When=操作 / Then=预期断言（And 继承上一类型）"""
    steps = (case.get("scenario") or {}).get("steps", [])
    status_map = case.get("steps_result", {}) or {}
    if not steps and not status_map:
        return ""
    if not steps and status_map:
        steps = list(status_map.keys())

    parts = []
    last_kind = "When"
    for st in steps:
        text = st.strip()
        kw, _, rest = text.partition(" ")
        if kw in ("Given", "When", "Then"):
            last_kind = kw
        elif kw in ("And", "But"):
            pass
        else:
            kw = last_kind
            rest = text
        kind = last_kind
        status = status_map.get(st) or status_map.get(text) or "unknown"
        if status == "running":
            status = "failed" if case["status"] in ("failed", "error") else "passed"
        cls = f"step-{kind.lower()}" if kind in ("Given", "When", "Then") else "step-when"
        icon = {"passed": "&#10003;", "failed": "&#10007;", "unknown": "&#183;"}.get(status, "&#183;")
        parts.append(
            f'<div class="bdd-step {cls}">'
            f'<span class="step-icon step-{status}">{icon}</span>'
            f'<span class="step-kw">{html_escape(kw)}</span>'
            f'<span class="step-text">{html_escape(rest)}</span></div>')
    return f'<div class="d-section"><div class="d-title">场景步骤与预期</div>' \
           f'<div class="bdd-steps">{"".join(parts)}</div></div>'


def _build_db_assert_panel(case: dict) -> str:
    """DB 落库断言详情：SQL/参数/记录数/字段校验结果"""
    asserts = case.get("db_asserts") or []
    if not asserts:
        return ""
    parts = []
    for rec in asserts:
        rec_ok = rec.get("actual_records") == rec.get("expect_records")
        mark = "&#10003;" if rec_ok else "&#10007;"
        color = "#10b981" if rec_ok else "#ef4444"
        rows = []
        for fc in rec.get("field_checks") or []:
            f_ok = fc.get("ok")
            f_mark = "&#10003;" if f_ok else "&#10007;"
            f_color = "#10b981" if f_ok else "#ef4444"
            rows.append(
                f"<tr><td>{html_escape(str(fc['field']))}</td>"
                f"<td>{html_escape(str(fc['expected']))}</td>"
                f"<td>{html_escape(str(fc['actual']))}</td>"
                f"<td style='color:{f_color}'>{f_mark}</td></tr>")
        params_txt = ", ".join(f"{k}={v}" for k, v in (rec.get("params") or {}).items())
        parts.append(
            f'<div class="db-assert">'
            f'<div class="db-title">映射 {html_escape(str(rec.get("map_id")))} '
            f'<span style="color:{color}">{mark}</span>'
            f'<span class="db-meta">表 {html_escape(str(rec.get("table")))} | '
            f'期望 {rec.get("expect_records")} 条 / 实际 {rec.get("actual_records")} 条 | '
            f'参数 {html_escape(params_txt)}</span></div>'
            f'<div class="db-sql">SQL: {html_escape(str(rec.get("sql")))}</div>'
            f'{"<table class=\"detail-table\"><thead><tr><th>字段</th><th>期望值</th><th>实际值</th><th>结果</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>" if rows else ""}'
            f'</div>')
    return (f'<div class="d-section"><div class="d-title">DB 落库断言详情</div>'
            f'{"".join(parts)}</div>')


def _build_api_sync_panel(case: dict) -> str:
    """API 返回校验详情：操作 → 方法/路径/是否收到/状态码"""
    syncs = case.get("api_syncs") or []
    if not syncs:
        return ""
    rows = []
    for s in syncs:
        ok = s.get("received")
        mark = "&#10003;" if ok else "&#10007;"
        color = "#10b981" if ok else "#ef4444"
        status_txt = str(s.get("status")) if s.get("received") else "未收到响应"
        rows.append(
            f"<tr><td>{html_escape(str(s.get('action')))}</td>"
            f"<td>{html_escape(str(s.get('method')))}</td>"
            f"<td>{html_escape(str(s.get('path')))}</td>"
            f"<td>{html_escape(status_txt)}</td>"
            f"<td style='color:{color}'>{mark}</td></tr>")
    return (f'<div class="d-section"><div class="d-title">API 返回校验（api_sync_rules 同步结果）</div>'
            f'<table class="detail-table"><thead><tr><th>操作</th><th>方法</th><th>路径</th>'
            f'<th>状态</th><th>结果</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def build_case_rows(cases: list) -> str:
    status_cn = {"passed": "通过", "failed": "失败", "error": "错误", "skipped": "跳过"}
    rows = []
    for i, case in enumerate(cases):
        status = case["status"]
        status_text = status_cn.get(status, status)
        reason = _clean_message(case.get("message", ""))
        screenshot = case.get("screenshot", "")
        trace = _clean_trace(case.get("trace", ""))
        sc = case.get("scenario") or {}
        sc_name = case.get("scenario_name", case["name"])
        steps_panel = _build_steps_panel(case)
        has_detail = bool(steps_panel or reason or trace or screenshot)

        parts = []
        if sc.get("feature"):
            parts.append(f'<div class="d-section"><div class="d-title">来源 Feature</div>'
                         f'<div class="d-desc">{html_escape(sc["feature"])}</div></div>')
        if steps_panel:
            parts.append(steps_panel)
        db_panel = _build_db_assert_panel(case)
        if db_panel:
            parts.append(db_panel)
        api_panel = _build_api_sync_panel(case)
        if api_panel:
            parts.append(api_panel)
        if reason:
            parts.append(
                f'<div class="fail-reason"><span class="lbl">失败原因</span>'
                f'<span class="val">{html_escape(reason)}</span></div>'
            )
        if screenshot:
            shot_label = "失败截图" if status in ("failed", "error") else "场景截图"
            parts.append(
                f'<div class="shot-box"><span class="lbl">{shot_label}</span>'
                f'<img src="screenshots/{html_escape(screenshot)}" '
                f'onerror="this.style.display=\'none\'" loading="lazy" /></div>'
            )
        if trace:
            parts.append(
                f'<details class="trace-box"><summary>完整错误堆栈</summary>'
                f'<pre>{html_escape(trace)}</pre></details>'
            )
        detail_row = ""
        if has_detail:
            default_open = i == 0 and status in ("failed", "error")
            display_attr = "" if default_open else ' style="display:none;"'
            detail_row = (
                f'<tr class="detail-row"{display_attr}>'
                f'<td colspan="3"><div class="case-detail">{"".join(parts)}</div></td></tr>'
            )
        rows.append(f"""
            <tr class="case-row status-{status}" onclick="toggleDetail(this)">
                <td class="col-status"><span class="badge badge-{status}">{status_text}</span></td>
                <td class="col-name" title="{html_escape(sc_name)}">
                    <div class="case-title">{html_escape(sc_name)}</div>
                    <div class="case-sub">{html_escape(case['name'])}</div>
                </td>
                <td class="col-action">{'&#9660; 详情' if has_detail else ''}</td>
            </tr>
            {detail_row}""")
    return "\n".join(rows)


def build_element_hit_report(cases: list) -> str:
    """聚合全部用例的 element_hits：元素 → 最高命中级别；未记录 = 走回退（脆弱点）"""
    best = {}
    for case in cases:
        for name, level in (case.get("element_hits") or {}).items():
            best[name] = max(best.get(name, -1), level)
    if not best:
        return ""
    rows = []
    for name in sorted(best):
        level = best[name]
        status = "地图命中" if level >= 0 else "回退"
        color = "#10b981" if level == 0 else ("#f59e0b" if level == 1 else "#ef4444")
        rows.append(
            f"<tr><td>{html_escape(name)}</td><td style='color:{color}'>{status}</td>"
            f"<td>策略第 {level + 1} 级</td></tr>")
    return (f'<div class="d-section"><div class="d-title">元素地图命中报告（本运行）</div>'
            f'<table class="detail-table"><thead><tr><th>元素</th><th>命中方式</th><th>策略级别</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')


def build_sections(suites: list) -> str:
    sections = []
    for suite in suites:
        module = suite.get("module", suite.get("name", ""))
        passed = suite["tests"] - suite["failures"] - suite["errors"] - suite["skipped"]
        rate = round(passed / suite["tests"] * 100, 1) if suite["tests"] > 0 else 0
        if rate >= 90: badge_css = "badge-passed"
        elif rate >= 70: badge_css = "badge-failed"
        else: badge_css = "badge-error"
        status_icon = "&#10003;" if suite["failures"] == 0 and suite["errors"] == 0 else "&#10007;"
        section_class = "section-passed" if suite["failures"] == 0 and suite["errors"] == 0 else "section-failed"
        cases_html = build_case_rows(suite["cases"])
        sections.append(f"""
        <div class="module-section {section_class}" data-module="{module}">
            <div class="section-header" onclick="toggleSection(this)">
                <span class="section-icon">{status_icon}</span>
                <span class="section-title">{html_escape(module)}</span>
                <span class="section-badge"><span class="badge {badge_css}">{rate}%</span></span>
                <span class="section-stats">{suite['tests']} scenarios | {suite['time']}s
                    {f"| {suite['failures']} failed" if suite['failures'] > 0 else ""}
                    {f"| {suite['errors']} errors" if suite['errors'] > 0 else ""}
                </span>
                <span class="section-arrow">&#9660;</span>
            </div>
            <div class="section-body">
                <table class="detail-table">
                    <thead><tr><th class="col-status">状态</th><th class="col-name">场景名称</th><th class="col-action">详情</th></tr></thead>
                    <tbody>{cases_html}</tbody>
                </table>
            </div>
        </div>""")
    return "\n".join(sections)


def generate_report(data: dict, output_dir: str) -> str:
    summary = data["summary"]
    suites = data["suites"]
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"模板文件不存在: {TEMPLATE_PATH}")
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    report_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    html = template.replace("{{REPORT_TIME}}", report_time)
    html = html.replace("{{SUMMARY_CARDS}}", build_summary_cards(summary))
    html = html.replace("{{SECTIONS}}", build_sections(suites))
    html = html.replace("{{ELEMENT_HITS}}", build_element_hit_report(data.get("cases", [])))

    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(output_dir, f"report_{timestamp}.html")
    latest_path = os.path.join(output_dir, "latest.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)
    shutil.copy(report_path, latest_path)
    print(f"\n[run_ui] 报告已生成:")
    print(f"  主文件: {os.path.abspath(report_path)}")
    print(f"  快捷方式: {os.path.abspath(latest_path)}")
    return report_path


def main():
    parser = argparse.ArgumentParser(description="执行 pytest-bdd UI 测试并生成含截图的 HTML 报告")
    parser.add_argument("--mode", choices=["baseline", "diff"], default="baseline")
    parser.add_argument("--test-path", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--headed", action="store_true", help="有头模式（调试用）")
    parser.add_argument("-k", "--keyword", default=None)
    parser.add_argument("--parallel", type=int, default=2, help="并行执行的 feature 进程数（默认 2）")
    parser.add_argument("--tags", default=None, help="pytest -m 表达式（如 smoke）")
    parser.add_argument("--no-fingerprint", action="store_true", help="跳过前端版本指纹检查")
    args = parser.parse_args()

    mode_config = MODE_PATHS[args.mode]
    test_path = args.test_path if args.test_path else str(mode_config["test_path"])
    output_dir = args.output if args.output else str(mode_config["output_dir"])
    if not os.path.exists(test_path):
        print(f"[run_ui] 错误: 测试路径不存在: {test_path}")
        sys.exit(1)

    test_files = discover_test_files(test_path)
    if not test_files:
        print(f"[run_ui] 错误: 未找到 test_*.py: {test_path}")
        sys.exit(1)

    base_url = load_frontend_url()
    screenshot_dir = os.path.join(output_dir, "screenshots")
    cache_dir = os.path.join(output_dir, ".cache")
    os.makedirs(cache_dir, exist_ok=True)
    os.makedirs(screenshot_dir, exist_ok=True)

    print(f"{'=' * 60}")
    if not args.no_fingerprint:
        fp_script = PROJECT_ROOT / "scripts" / "ui_fingerprint.py"
        if fp_script.exists():
            store = os.path.join(cache_dir, "ui_fingerprint.txt")
            fp_result = subprocess.run(
                [find_python(), str(fp_script), "--store", store],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
            )
            fp_out = (fp_result.stdout or "").strip()
            if fp_result.returncode == 2:
                print(f"[run_ui] 注意: 前端已变更（{fp_out}），若元素地图失效请先跑探针/更新 ui-profile")
    print(f"[run_ui] 开始执行 UI 测试（逐 feature 隔离模式）")
    print(f"[run_ui] 浏览器: chromium | 前端地址: {base_url or '(未配置)'}")
    print(f"[run_ui] 测试目录: {test_path}")
    print(f"[run_ui] 发现 {len(test_files)} 个测试文件")
    print(f"{'=' * 60}\n")

    total_start = time.time()
    all_results = []
    crashed = []
    lock = threading.Lock()
    progress = {"done": 0}

    def _run_one(test_file):
        file_name = os.path.basename(test_file)
        junit_xml = os.path.join(cache_dir, f"results_{file_name}.xml")
        exit_code, elapsed, stdout, stderr = run_pytest_file(
            test_file, junit_xml, base_url, screenshot_dir,
            args.headed, args.keyword, args.tags,
        )
        with lock:
            progress["done"] += 1
            if os.path.exists(junit_xml):
                module_name = os.path.splitext(file_name)[0]
                if module_name.startswith("test_"):
                    module_name = module_name[5:]
                data = parse_junit_xml(junit_xml, module_name)
                s = data["summary"]
                if s["tests"] > 0:
                    all_results.append(data)
                    status = "PASS" if s["failures"] == 0 and s["errors"] == 0 else "FAIL"
                    print(f"  [{progress['done']}/{len(test_files)}] {file_name:<35} {status:>6}  "
                          f"{s['tests']:>2} scenarios | {s['failures']:>2} failed | {elapsed}s")
                    return
                print(f"  [{progress['done']}/{len(test_files)}] {file_name:<35} {'EMPTY':>6}  (无匹配场景)")
                return
            print(f"  [{progress['done']}/{len(test_files)}] {file_name:<35} {'ERROR':>6}  未生成报告 (exit={exit_code})")
            for line in (stderr or "").strip().split("\n")[-6:]:
                print(f"         {line}")
            crashed.append(file_name)

    workers = max(1, args.parallel)
    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(_run_one, test_files))

    total_elapsed = round(time.time() - total_start, 2)
    if not all_results:
        print("\n[run_ui] 错误: 所有测试文件均未产生有效结果")
        sys.exit(1)

    data = merge_results(all_results, total_elapsed)

    # 关联 feature 场景步骤（04-ui-scenarios 下的 .feature 文件）
    # test_path = .../generated/ui-test → parents[1] = .../baseline
    feature_dir = Path(test_path).resolve().parents[1] / "_workflow" / "04-ui-scenarios"
    scenarios = load_feature_scenarios(str(feature_dir))
    if scenarios:
        enrich_ui_cases(data["cases"], scenarios)
        print(f"[run_ui] 已关联 feature 场景: {len(scenarios)} 个")
    s = data["summary"]
    pass_rate = round(s["passed"] / s["tests"] * 100, 1) if s["tests"] > 0 else 0
    print(f"\n{'=' * 60}")
    print(f"[run_ui] 测试完成（聚合结果）")
    print(f"  总计: {s['tests']} | 通过: {s['passed']} | 失败: {s['failures']} | "
          f"错误: {s['errors']} | 跳过: {s['skipped']}")
    print(f"  通过率: {pass_rate}% | 总耗时: {total_elapsed}s")
    print(f"{'=' * 60}\n")

    generate_report(data, output_dir)


if __name__ == "__main__":
    main()
