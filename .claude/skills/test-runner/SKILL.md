---
name: test-runner
description: 执行 generated/api-test/ 下的 pytest 测试脚本并生成 HTML 报告。触发方式：/test-runner、运行API测试、执行接口测试、生成测试报告、pytest api test、run api tests and generate report、跑接口测试、执行pytest测试。每次用户提到运行测试、执行测试脚本、生成测试报告时使用此 skill。
---

# API 测试执行与报告生成

执行 `tests/baseline/generated/api-test/` 下的 pytest 测试脚本，将结果输出为精美的 HTML 报告。

## 执行模式：逐文件隔离

每个 `test_*.py` 文件以**独立 pytest 进程**执行，确保：

- **Token 隔离**：每个模块独立登录获取 token，登出/改密码等破坏性用例不会影响其他模块
- **进程隔离**：单个文件 crash 或超时不影响其他文件继续执行
- **模块边界清晰**：报告按文件分组，一目了然

所有文件执行完毕后，自动合并各模块的 JUnit XML 结果，生成一份聚合 HTML 报告。

## 执行步骤

直接执行脚本并生成报告：

```bash
python .claude/skills/test-runner/scripts/run_tests.py
```

可选参数：
```bash
python .claude/skills/test-runner/scripts/run_tests.py -m smoke        # 只运行冒烟测试
python .claude/skills/test-runner/scripts/run_tests.py -k "test_auth"  # 运行特定模块
```

报告生成到 `tests/baseline/report/api-test/`，命名格式：`report_<YYYYMMDD_HHMMSS>.html`，同时更新 `latest.html` 指向最新报告。

## 报告内容

生成的 HTML 报告包含：

- **摘要卡片**：总计、通过、失败、错误、跳过、通过率、总耗时
- **失败原因分析**：自动按错误类型（认证失败、参数校验、连接错误等）分类统计
- **通过率饼图**：Chart.js 环形图展示通过/失败/错误分布
- **耗时分布图**：Chart.js 柱状图展示 Top 15 耗时用例
- **详细结果表**：每条用例的名称、状态标签、耗时、失败时的错误信息和堆栈（可折叠展开）
- **筛选功能**：按钮切换查看全部/通过/失败/错误用例
- **按模块分组**：每个 test_*.py 文件为一个 section，显示该模块的统计信息
- **分页**：每个模块 section 内支持分页切换（10/20/50条/全部）

## 报告模板

报告样式定义在 `template/report_template.html`，使用内联 CSS + Chart.js CDN。

模板中的占位符：
- `{{REPORT_TIME}}` — 报告生成时间
- `{{SUMMARY_CARDS}}` — 摘要卡片 HTML
- `{{FAILURE_ANALYSIS}}` — 失败原因分析 HTML
- `{{CHART_DATA}}` — Chart.js 图表 JSON 数据
- `{{MODULE_SECTIONS}}` — 按模块分组的详细结果

## 输出文件


| 文件 | 路径                                              | 说明 |
|------|-------------------------------------------------|------|
| 测试报告 | `tests/baseline/report/api-test/report_<timestamp>.html` | 带时间戳的聚合报告 |
| 最新报告 | `tests/baseline/report/api-test/latest.html`    | 始终指向最新报告 |
| JUnit 缓存 | `tests/baseline/report/api-test/.cache/results_<module>.xml` | 各模块独立 XML（临时） |

## 行为约束

执行结束后，无论用例通过率多少，**禁止以下所有行为**：

- 禁止分析失败用例的根因
- 禁止修改 03 阶段的 YAML 测试用例定义
- 禁止修改 04 阶段生成的 pytest 测试脚本
- 禁止向用户建议修复方案
- 禁止重新执行测试

**唯一允许的动作**：输出统计摘要（总计/通过/失败/耗时）和报告文件路径，然后结束。
