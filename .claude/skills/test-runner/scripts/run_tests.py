"""
API 测试执行与报告生成脚本
逐文件隔离执行 pytest 测试 → 合并 JUnit XML → 生成 HTML 报告

每个 test_*.py 独立启动 pytest 进程，避免 session 级 token 被登出/修改密码等
破坏性用例失效，确保模块间完全隔离。

用法:
    python run_tests.py                           # 默认运行所有测试
    python run_tests.py -m smoke                  # 只运行冒烟测试
    python run_tests.py -k "test_ums"             # 运行特定模块
    python run_tests.py --output report/api-test  # 指定输出目录
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
SKILL_DIR = Path(__file__).resolve().parent.parent
TEST_PATH = PROJECT_ROOT / "tests" / "baseline" / "generated" / "api-test"
TEMPLATE_PATH = SKILL_DIR / "template" / "report_template.html"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "tests" / "baseline" / "report" / "api-test"


def find_python() -> str:
    """查找 Python 解释器路径"""
    config_path = PROJECT_ROOT / "config.yaml"
    if config_path.exists():
        import yaml
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        tool_path = config.get("tools", {}).get("python", "")
        if tool_path:
            candidates = [
                os.path.join(tool_path, "python.exe"),
                os.path.join(tool_path, "python"),
            ]
            for candidate in candidates:
                if os.path.exists(candidate):
                    return candidate
    return shutil.which("python") or "python"


def discover_test_files(test_dir: str) -> list:
    """发现测试目录下所有 test_*.py 文件，按文件名排序"""
    if os.path.isfile(test_dir):
        return [test_dir]
    files = sorted(Path(test_dir).glob("test_*.py"))
    return [str(f) for f in files]


def run_pytest_file(test_file: str, junit_output: str, markers: str = None, keyword: str = None) -> tuple:
    """对单个测试文件运行 pytest

    Returns:
        (exit_code: int, elapsed: float, stdout: str, stderr: str)
    """
    python = find_python()
    cmd = [python, "-m", "pytest", test_file, "-v", "--tb=short"]

    if markers:
        cmd.extend(["-m", markers])
    if keyword:
        cmd.extend(["-k", keyword])

    cmd.extend([f"--junitxml={junit_output}"])

    start = time.time()
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True)
    elapsed = round(time.time() - start, 2)

    return result.returncode, elapsed, result.stdout, result.stderr


def parse_junit_xml(xml_path: str) -> dict:
    """解析 JUnit XML 为结构化数据

    Returns:
        {
            "summary": {"tests": 25, "passed": 20, "failures": 3, "errors": 1, "skipped": 1, "time": 45.2},
            "suites": [...],
            "cases": [...]
        }
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    all_tests = 0
    all_failures = 0
    all_errors = 0
    all_skipped = 0
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
            "name": ts.attrib.get("name", "Unknown"),
            "tests": int(ts.attrib.get("tests", 0)),
            "failures": int(ts.attrib.get("failures", 0)),
            "errors": int(ts.attrib.get("errors", 0)),
            "skipped": int(ts.attrib.get("skipped", 0)),
            "time": round(float(ts.attrib.get("time", 0)), 2),
            "cases": [],
        }

        for tc in ts.findall("testcase"):
            case = {
                "classname": tc.attrib.get("classname", ""),
                "name": tc.attrib.get("name", ""),
                "time": round(float(tc.attrib.get("time", 0)), 3),
                "status": "passed",
                "message": "",
                "trace": "",
            }

            failure = tc.find("failure")
            error = tc.find("error")
            skipped = tc.find("skipped")

            if failure is not None:
                case["status"] = "failed"
                msg = failure.attrib.get("message", "")
                case["message"] = msg[:200]
                case["trace"] = (failure.text or "")[:2000]
            elif error is not None:
                case["status"] = "error"
                msg = error.attrib.get("message", "")
                case["message"] = msg[:200]
                case["trace"] = (error.text or "")[:2000]
            elif skipped is not None:
                case["status"] = "skipped"
                case["message"] = skipped.attrib.get("message", "")

            suite["cases"].append(case)
            all_cases.append(case)

        suites.append(suite)

    return {"summary": summary, "suites": suites, "cases": all_cases}


def merge_results(all_results: list, total_elapsed: float) -> dict:
    """合并多个文件的独立解析结果为一个聚合数据结构"""
    merged_cases = []
    merged_suites = []
    all_tests = 0
    all_failures = 0
    all_errors = 0
    all_skipped = 0

    for data in all_results:
        s = data["summary"]
        all_tests += s["tests"]
        all_failures += s["failures"]
        all_errors += s["errors"]
        all_skipped += s["skipped"]
        merged_suites.extend(data["suites"])
        merged_cases.extend(data["cases"])

    summary = {
        "tests": all_tests,
        "failures": all_failures,
        "errors": all_errors,
        "skipped": all_skipped,
        "time": round(total_elapsed, 2),
    }
    summary["passed"] = summary["tests"] - summary["failures"] - summary["errors"] - summary["skipped"]

    return {"summary": summary, "suites": merged_suites, "cases": merged_cases}


def build_summary_cards(summary: dict) -> str:
    """生成摘要卡片 HTML"""
    passed = summary["passed"]
    failed = summary["failures"]
    errors = summary["errors"]
    skipped = summary["skipped"]
    total = summary["tests"]
    pass_rate = round(passed / total * 100, 1) if total > 0 else 0

    if pass_rate >= 90:
        rate_color, rate_bg = "#10b981", "#ecfdf5"
    elif pass_rate >= 70:
        rate_color, rate_bg = "#f59e0b", "#fffbeb"
    else:
        rate_color, rate_bg = "#ef4444", "#fef2f2"

    return f"""
    <div class="summary-grid">
        <div class="card total">
            <div class="card-icon">&#9733;</div>
            <div class="card-value">{total}</div>
            <div class="card-label">总计用例</div>
        </div>
        <div class="card passed">
            <div class="card-icon">&#10003;</div>
            <div class="card-value">{passed}</div>
            <div class="card-label">通过</div>
        </div>
        <div class="card failed">
            <div class="card-icon">&#10007;</div>
            <div class="card-value">{failed}</div>
            <div class="card-label">失败</div>
        </div>
        <div class="card errors">
            <div class="card-icon">&#9888;</div>
            <div class="card-value">{errors}</div>
            <div class="card-label">错误</div>
        </div>
        <div class="card skipped">
            <div class="card-icon">&#8212;</div>
            <div class="card-value">{skipped}</div>
            <div class="card-label">跳过</div>
        </div>
        <div class="card rate" style="background:{rate_bg}; border-color:{rate_color};">
            <div class="card-value" style="color:{rate_color};">{pass_rate}%</div>
            <div class="card-label">通过率</div>
        </div>
        <div class="card time">
            <div class="card-icon">&#9202;</div>
            <div class="card-value">{summary["time"]}s</div>
            <div class="card-label">总耗时</div>
        </div>
    </div>"""


def build_chart_data(cases: list[dict]) -> str:
    """生成 Chart.js 图表 JSON 数据"""
    passed = sum(1 for c in cases if c["status"] == "passed")
    failed = sum(1 for c in cases if c["status"] == "failed")
    errors = sum(1 for c in cases if c["status"] == "error")
    skipped = sum(1 for c in cases if c["status"] == "skipped")

    sorted_by_time = sorted(cases, key=lambda c: c["time"], reverse=True)[:15]
    time_labels = [c["name"][:40] for c in sorted_by_time]
    time_data = [c["time"] for c in sorted_by_time]

    return json.dumps({
        "pie": {
            "labels": ["通过", "失败", "错误", "跳过"],
            "data": [passed, failed, errors, skipped],
            "colors": ["#10b981", "#ef4444", "#f59e0b", "#94a3b8"],
        },
        "time": {
            "labels": time_labels,
            "data": time_data,
        },
    }, ensure_ascii=False)


def build_detail_rows(cases: list[dict]) -> str:
    """生成详细结果表格行 HTML"""
    rows = []
    for i, case in enumerate(cases):
        status_cn = {"passed": "通过", "failed": "失败", "error": "错误", "skipped": "跳过"}
        status = case["status"]
        status_text = status_cn.get(status, status)
        module_name = case["classname"].split(".")[-1] if case["classname"] else "-"

        trace_html = ""
        if case["trace"]:
            trace_html = f"""
            <tr class="trace-row" id="trace-{i}" style="display:none;">
                <td colspan="5">
                    <div class="trace-box">
                        <strong>{case['message']}</strong>
                        <pre>{case['trace']}</pre>
                    </div>
                </td>
            </tr>"""

        rows.append(f"""
            <tr class="case-row status-{status}" onclick="toggleTrace({i})">
                <td class="col-status"><span class="badge badge-{status}">{status_text}</span></td>
                <td class="col-name" title="{case['name']}">{case['name'][:80]}</td>
                <td class="col-module">{module_name}</td>
                <td class="col-time">{case['time']:.2f}s</td>
                <td class="col-action">{"&#9660; 详情" if case['trace'] else ""}</td>
            </tr>
            {trace_html}""")

    return "\n".join(rows)


def build_module_sections(suites: list[dict]) -> str:
    """按测试套件（模块）分组生成 sections"""
    sections = []
    for suite in suites:
        cases_html = build_detail_rows(suite["cases"])
        status_icon = "&#10003;" if suite["failures"] == 0 and suite["errors"] == 0 else "&#10007;"
        section_class = "section-passed" if suite["failures"] == 0 and suite["errors"] == 0 else "section-failed"

        sections.append(f"""
        <div class="module-section {section_class}">
            <div class="section-header" onclick="toggleSection(this)">
                <span class="section-icon">{status_icon}</span>
                <span class="section-title">{suite['name']}</span>
                <span class="section-stats">
                    {suite['tests']} tests | {suite['time']}s
                    {f"| {suite['failures']} failed" if suite['failures'] > 0 else ""}
                    {f"| {suite['errors']} errors" if suite['errors'] > 0 else ""}
                </span>
                <span class="section-arrow">&#9660;</span>
            </div>
            <div class="section-body">
                <table class="detail-table">
                    <thead>
                        <tr>
                            <th class="col-status">状态</th>
                            <th class="col-name">用例名称</th>
                            <th class="col-module">模块</th>
                            <th class="col-time">耗时</th>
                            <th class="col-action">详情</th>
                        </tr>
                    </thead>
                    <tbody>{cases_html}</tbody>
                </table>
            </div>
        </div>""")

    return "\n".join(sections)


def build_failure_analysis(suites: list[dict]) -> dict:
    """分析失败原因，按错误类型分类统计

    Returns:
        {"categories": [{"reason": str, "count": int, "cases": [str]}], "total_failed": int}
    """
    RULES = [
        ("认证/权限失败", [
            "认证失败，无法访问系统资源",
            "没有访问权限",
            "客户端ID与Token不匹配",
            "NotLoginException", "NotPermissionException", "NotRoleException",
        ]),
        ("登录失败", [
            "login failed",
        ]),
        ("参数校验错误", [
            "不能为空", "格式不正确", "长度必须", "长度不能超过",
            "已在", "已存在",
        ]),
        ("资源不存在/无权限访问", [
            "不存在", "没有权限访问",
        ]),
        ("连接/网络错误", [
            "Connection", "ConnectionError", "Timeout", "timeout",
            "MaxRetryError", "RemoteDisconnected",
        ]),
        ("HTTP 状态码不匹配", [
            "status_code:", "expected",
        ]),
        ("业务状态码错误", [
            "business_code:", "business_message",
        ]),
        ("服务端错误 (500)", [
            "发生未知异常", "发生系统异常", "请联系管理员",
        ]),
    ]

    categories = {}
    uncategorized = []

    for suite in suites:
        for case in suite.get("cases", []):
            if case["status"] != "failed" and case["status"] != "error":
                continue
            msg = case.get("message", "")
            trace = case.get("trace", "")
            full = msg + "\n" + trace

            matched = None
            for category, keywords in RULES:
                for kw in keywords:
                    if kw in full:
                        matched = category
                        break
                if matched:
                    break

            if matched:
                if matched not in categories:
                    categories[matched] = {"count": 0, "cases": []}
                categories[matched]["count"] += 1
                categories[matched]["cases"].append(case["name"][:80])
            else:
                uncategorized.append({"name": case["name"][:80], "message": msg[:100]})

    result = []
    for cat, data in sorted(categories.items(), key=lambda x: -x[1]["count"]):
        result.append({"reason": cat, "count": data["count"], "cases": data["cases"]})

    if uncategorized:
        result.append({"reason": "其他/未分类", "count": len(uncategorized),
                       "cases": [u["name"] for u in uncategorized]})

    total = sum(d["count"] for d in result)
    return {"categories": result, "total_failed": total}


def build_failure_html(analysis: dict) -> str:
    """生成失败原因分析 HTML"""
    categories = analysis.get("categories", [])
    total = analysis.get("total_failed", 0)

    if total == 0:
        return """
        <div class="failure-section">
            <h2 class="section-heading">失败原因分析</h2>
            <div class="no-results">&#127881; 所有用例均通过，无失败分析</div>
        </div>"""

    max_count = max(c["count"] for c in categories) if categories else 1
    rows = []
    for i, cat in enumerate(categories):
        pct = round(cat["count"] / total * 100, 1) if total > 0 else 0
        bar_width = round(cat["count"] / max_count * 100)
        case_list = ", ".join(cat["cases"][:5])
        more = f" (+{len(cat['cases']) - 5}条)" if len(cat["cases"]) > 5 else ""

        colors = ["#ff4d6a", "#f0a040", "#4da8ff", "#a78bfa", "#22d695", "#64748b"]
        color = colors[i % len(colors)]

        rows.append(f"""
        <div class="failure-cat">
            <div class="failure-cat-header">
                <span class="failure-cat-name" style="color:{color};">{cat['reason']}</span>
                <span class="failure-cat-count">{cat['count']} 条 ({pct}%)</span>
            </div>
            <div class="failure-bar-wrap">
                <div class="failure-bar" style="width:{bar_width}%; background:{color};"></div>
            </div>
            <div class="failure-cases" title="{case_list}{more}">{case_list}{more}</div>
        </div>""")

    return f"""
    <div class="failure-section">
        <h2 class="section-heading">失败原因分析</h2>
        <div class="failure-total">共 {total} 条失败/错误，分为 {len(categories)} 类</div>
        <div class="failure-grid">{''.join(rows)}</div>
    </div>"""


def generate_report(data: dict, output_dir: str) -> str:
    """生成 HTML 报告文件"""
    summary = data["summary"]
    suites = data["suites"]
    cases = data["cases"]

    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"模板文件不存在: {TEMPLATE_PATH}")
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    report_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    failure_analysis = build_failure_analysis(suites)
    html = template.replace("{{REPORT_TIME}}", report_time)
    html = html.replace("{{FAILURE_ANALYSIS}}", build_failure_html(failure_analysis))
    html = html.replace("{{SUMMARY_CARDS}}", build_summary_cards(summary))
    html = html.replace("{{CHART_DATA}}", build_chart_data(cases))
    html = html.replace("{{MODULE_SECTIONS}}", build_module_sections(suites))

    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(output_dir, f"report_{timestamp}.html")
    latest_path = os.path.join(output_dir, "latest.html")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)
    shutil.copy(report_path, latest_path)

    report_abs = os.path.abspath(report_path)
    print(f"\n[run_tests] 报告已生成:")
    print(f"  主文件: {report_abs}")
    print(f"  快捷方式: {os.path.abspath(latest_path)}")
    return report_abs


def main():
    parser = argparse.ArgumentParser(description="执行 pytest 测试并生成 HTML 报告（逐文件隔离执行）")
    parser.add_argument("--test-path", default=str(TEST_PATH), help="测试文件目录或单个文件")
    parser.add_argument("-m", "--markers", default=None, help="pytest markers (如 smoke, P0)")
    parser.add_argument("-k", "--keyword", default=None, help="pytest -k 筛选表达式")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_DIR), help="报告输出目录")
    args = parser.parse_args()

    test_path = args.test_path
    if not os.path.exists(test_path):
        print(f"[run_tests] 错误: 测试路径不存在: {test_path}")
        sys.exit(1)

    # 发现测试文件
    test_files = discover_test_files(test_path)
    if not test_files:
        print(f"[run_tests] 错误: 未找到 test_*.py 测试文件: {test_path}")
        sys.exit(1)

    # 缓存目录
    cache_dir = os.path.join(args.output, ".cache")
    os.makedirs(cache_dir, exist_ok=True)

    # ── Step 1: 逐文件执行 pytest ──────────────────────────
    print(f"\n{'=' * 60}")
    print(f"[run_tests] 开始执行 API 测试（逐文件隔离模式）")
    print(f"[run_tests] 测试目录: {test_path}")
    print(f"[run_tests] 发现 {len(test_files)} 个测试文件")
    print(f"{'=' * 60}\n")

    total_start = time.time()
    all_results = []
    crashed_files = []

    for i, test_file in enumerate(test_files):
        file_name = os.path.basename(test_file)
        junit_xml = os.path.join(cache_dir, f"results_{file_name}.xml")

        exit_code, elapsed, stdout, stderr = run_pytest_file(
            test_file, junit_xml, args.markers, args.keyword
        )

        if os.path.exists(junit_xml):
            data = parse_junit_xml(junit_xml)
            s = data["summary"]
            if s["tests"] > 0:
                all_results.append(data)
                status = "PASS" if s["failures"] == 0 and s["errors"] == 0 else "FAIL"
                print(f"  [{i+1}/{len(test_files)}] {file_name:<35} {status:>6}  "
                      f"{s['tests']:>3} tests | {s['failures']:>2} failed | {elapsed}s")
            else:
                print(f"  [{i+1}/{len(test_files)}] {file_name:<35} {'EMPTY':>6}  "
                      f"(无匹配用例)")
        else:
            print(f"  [{i+1}/{len(test_files)}] {file_name:<35} {'ERROR':>6}  "
                  f"未生成报告 (exit={exit_code})")
            if stderr:
                for line in stderr.strip().split("\n")[-5:]:
                    print(f"         {line}")
            crashed_files.append(file_name)

    total_elapsed = round(time.time() - total_start, 2)

    if not all_results:
        print(f"\n[run_tests] 错误: 所有测试文件均未产生有效结果")
        sys.exit(1)

    # ── Step 2: 合并结果 ──────────────────────────────────
    data = merge_results(all_results, total_elapsed)

    # ── Step 3: 打印聚合摘要 ──────────────────────────────
    s = data["summary"]
    pass_rate = round(s["passed"] / s["tests"] * 100, 1) if s["tests"] > 0 else 0
    print(f"\n{'=' * 60}")
    print(f"[run_tests] 测试完成（聚合结果）")
    print(f"  文件数: {len(test_files)} | 有效: {len(all_results)}", end="")
    if crashed_files:
        print(f" | 异常: {len(crashed_files)} ({', '.join(crashed_files)})", end="")
    print()
    print(f"  总计: {s['tests']} | 通过: {s['passed']} | "
          f"失败: {s['failures']} | 错误: {s['errors']} | 跳过: {s['skipped']}")
    print(f"  通过率: {pass_rate}% | 总耗时: {total_elapsed}s")
    print(f"{'=' * 60}\n")

    # ── Step 4: 生成报告 ──────────────────────────────────
    report_path = generate_report(data, args.output)
    return report_path


if __name__ == "__main__":
    main()
