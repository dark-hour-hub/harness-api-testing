---
name: test-runner
description: 执行 generated/api-test/ 下的 pytest 测试脚本并生成 HTML 报告。触发方式：/test-runner、运行API测试、执行接口测试、生成测试报告、pytest api test、run api tests and generate report、跑接口测试、执行pytest测试。每次用户提到运行测试、执行测试脚本、生成测试报告时使用此 skill。
---

# API 测试执行与报告生成

执行 `tests/baseline/generated/api-test/` 下的 pytest 测试脚本，将结果输出为精美的 HTML 报告。

## 执行步骤

直接执行脚本并生成报告：

```bash
python .claude/skills/test-runner/scripts/run_tests.py
```

报告生成到 `tests/baseline/report` 目录，命名格式：`report_<YYYYMMDD_HHMMSS>.html`，同时更新 `latest.html` 指向最新报告。

## 报告内容

生成的 HTML 报告包含：

- **摘要卡片**：总计、通过、失败、错误、跳过、总耗时
- **通过率饼图**：Chart.js 环形图展示通过/失败/错误分布
- **耗时分布图**：Chart.js 柱状图展示各用例耗时对比
- **详细结果表**：每条用例的名称、状态标签、耗时、失败时的错误信息和堆栈（可折叠展开）
- **筛选功能**：按钮切换查看全部/通过/失败/错误用例
- **按模块分组**：自动按测试文件（模块）分 section 展示

## 报告模板

报告样式定义在 `template/report_template.html`，使用内联 CSS + Chart.js CDN。

模板中的占位符：
- `{{REPORT_TIME}}` — 报告生成时间
- `{{SUMMARY_CARDS}}` — 摘要卡片 HTML
- `{{CHART_DATA}}` — Chart.js 图表 JSON 数据
- `{{DETAIL_ROWS}}` — 详细结果行 HTML
- `{{MODULE_SECTIONS}}` — 按模块分组的详细结果

## 输出文件


| 文件 | 路径                                              | 说明 |
|------|-------------------------------------------------|------|
| 测试报告 | `tests/baseline/report/report_<timestamp>.html` | 带时间戳的报告 |
| 最新报告 | `tests/baseline/report/api-test/latest.html`    | 始终指向最新报告 |
| JUnit XML | `tests/baseline/report/api-test/.cache/results.xml`            | 原始 pytest 输出（临时） |
