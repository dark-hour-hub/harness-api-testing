"""
API 测试执行与报告生成脚本
运行 pytest 测试 → 解析 JUnit XML → 生成 HTML 报告

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
            # 配置的是目录，拼接 python 可执行文件
            candidates = [
                os.path.join(tool_path, "python.exe"),
                os.path.join(tool_path, "python"),
            ]
            for candidate in candidates:
                if os.path.exists(candidate):
                    return candidate
    return shutil.which("python") or "python"


def run_pytest(test_path: str, junit_output: str, markers: str = None, keyword: str = None) -> int:
    """运行 pytest 并输出 JUnit XML

    Returns:
        pytest 退出码（0 = 全部通过，1 = 有失败）
    """
    python = find_python()
    cmd = [python, "-m", "pytest", test_path, "-v", "--tb=short"]

    if markers:
        cmd.extend(["-m", markers])
    if keyword:
        cmd.extend(["-k", keyword])

    cmd.extend([f"--junitxml={junit_output}"])

    print(f"[run_tests] 执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=False)

    if result.returncode not in (0, 1):
        print(f"[run_tests] pytest 执行异常，退出码: {result.returncode}")
    return result.returncode


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

    # 从所有 <testsuite> 子元素聚合（根 <testsuites> 可能无属性）
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


def build_summary_cards(summary: dict) -> str:
    """生成摘要卡片 HTML"""
    passed = summary["passed"]
    failed = summary["failures"]
    errors = summary["errors"]
    skipped = summary["skipped"]
    total = summary["tests"]
    pass_rate = round(passed / total * 100, 1) if total > 0 else 0

    # 根据通过率选颜色
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

    # 耗时 top 15
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


def generate_report(data: dict, output_dir: str) -> str:
    """生成 HTML 报告文件"""
    summary = data["summary"]
    suites = data["suites"]
    cases = data["cases"]

    # 读取模板
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"模板文件不存在: {TEMPLATE_PATH}")
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    # 填充数据
    report_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    html = template.replace("{{REPORT_TIME}}", report_time)
    html = html.replace("{{SUMMARY_CARDS}}", build_summary_cards(summary))
    html = html.replace("{{CHART_DATA}}", build_chart_data(cases))
    html = html.replace("{{MODULE_SECTIONS}}", build_module_sections(suites))

    # 写入文件
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(output_dir, f"report_{timestamp}.html")
    latest_path = os.path.join(output_dir, "latest.html")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)
    shutil.copy(report_path, latest_path)

    # 返回绝对路径
    report_abs = os.path.abspath(report_path)
    print(f"\n[run_tests] 报告已生成:")
    print(f"  主文件: {report_abs}")
    print(f"  快捷方式: {os.path.abspath(latest_path)}")
    return report_abs


def main():
    parser = argparse.ArgumentParser(description="执行 pytest 测试并生成 HTML 报告")
    parser.add_argument("--test-path", default=str(TEST_PATH), help="测试文件目录")
    parser.add_argument("-m", "--markers", default=None, help="pytest markers (如 smoke, P0)")
    parser.add_argument("-k", "--keyword", default=None, help="pytest -k 筛选表达式")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_DIR), help="报告输出目录")
    args = parser.parse_args()

    test_path = args.test_path
    if not os.path.isdir(test_path):
        print(f"[run_tests] 错误: 测试目录不存在: {test_path}")
        sys.exit(1)

    # 缓存目录
    cache_dir = os.path.join(args.output, ".cache")
    os.makedirs(cache_dir, exist_ok=True)
    junit_xml = os.path.join(cache_dir, "results.xml")

    # Step 1: 运行 pytest
    print(f"\n{'=' * 60}")
    print(f"[run_tests] 开始执行 API 测试")
    print(f"[run_tests] 测试路径: {test_path}")
    print(f"{'=' * 60}\n")

    start_time = time.time()
    exit_code = run_pytest(test_path, junit_xml, args.markers, args.keyword)
    elapsed = round(time.time() - start_time, 2)

    # Step 2: 解析结果
    if not os.path.exists(junit_xml):
        print(f"[run_tests] 错误: JUnit XML 未生成，pytest 可能未正常执行")
        sys.exit(1)

    data = parse_junit_xml(junit_xml)
    data["summary"]["time"] = elapsed  # 用实际耗时覆盖

    # Step 3: 打印摘要
    s = data["summary"]
    print(f"\n{'=' * 60}")
    print(f"[run_tests] 测试完成")
    print(f"  总计: {s['tests']} | 通过: {s['passed']} | 失败: {s['failures']} | 错误: {s['errors']} | 跳过: {s['skipped']}")
    print(f"  耗时: {elapsed}s | 退出码: {exit_code}")
    print(f"{'=' * 60}\n")

    # Step 4: 生成报告
    report_path = generate_report(data, args.output)
    return report_path


if __name__ == "__main__":
    main()
