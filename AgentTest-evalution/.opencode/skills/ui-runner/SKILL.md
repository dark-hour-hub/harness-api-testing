---
name: ui-runner
description: 执行 generated/ui-test/ 下的 pytest-bdd UI 测试脚本（chromium 无头浏览器），成功/失败自动截图，生成含截图的 HTML 报告。触发：/ui-runner、运行UI测试、执行界面测试、生成UI测试报告、run ui test、跑UI测试、执行playwright测试。
---

# UI 测试执行与报告生成

执行 pytest-bdd + Playwright 测试脚本，成功/失败自动截图，生成含截图的 HTML 报告。

## 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|:---:|--------|------|
| `mode` | enum | 否 | `baseline` | `baseline` = 全量；`diff` = 增量 |
| `--headed` | flag | 否 | 无 | 有头模式（调试用） |

路径决议（按 mode）：

| 路径变量 | `baseline` | `diff` |
|---------|----------|--------|
| `TEST_DIR` | `tests/baseline/generated/ui-test` | `tests/diff/generated/ui-test` |
| `REPORT_DIR` | `tests/baseline/report/ui-test` | `tests/diff/report/ui-test` |

## 范围

此 skill 只做两件事：**执行** UI 测试 + **生成** HTML 报告（含截图）。不分析、不修复、不重跑。

## 铁律

执行结束后，无论通过率多少，**严格禁止**以下行为：

- 禁止分析失败场景的根因（即使失败率很高）
- 禁止查看失败场景的截图或错误堆栈
- 禁止修改 `.feature` 场景定义或生成的脚本
- 禁止向用户建议修复方案
- 禁止重新执行测试（即使只改了一个定位器）

**唯一允许的动作**：按下方输出模板输出统计摘要和报告路径；若存在失败场景，追加一句"是否分析本次失败场景"的询问（后续交给 `post-run-analysis` skill），然后结束。

## 输出模板

```
**UI 测试执行完成**

| 文件 | 场景数 | 通过 | 失败 | 错误 | 耗时 |
|------|--------|------|------|------|------|
| test_xxx.py | N | N | N | N | Xs |

**合计**: N 通过 / M 总计 (X%)
**报告**: `${REPORT_DIR}/report_<timestamp>.html`
**截图**: `${REPORT_DIR}/screenshots/`
```

最后一行"截图"之后不再输出任何内容。存在失败场景时仅可追加"是否分析本次失败场景"的一句询问（交给 `post-run-analysis` skill），不追加分析建议。

## 执行步骤

```bash
# 全量模式（默认）
python .opencode/skills/ui-runner/scripts/run_ui.py --mode baseline

# 有头模式（调试）
python .opencode/skills/ui-runner/scripts/run_ui.py --mode baseline --headed

# 运行特定模块
python .opencode/skills/ui-runner/scripts/run_ui.py -k "test_login"
```

报告命名：`report_<YYYYMMDD_HHMMSS>.html`，同时更新 `latest.html`。

## 执行细节

- **浏览器**：chromium 无头模式（`--headed` 切换有头）
- **逐 feature 隔离**：每个 `test_*.py` 独立 pytest 进程，浏览器上下文互不污染
- **base_url**：从 `config.yaml` 的 `environments.<env>.frontend[].url` 读取
- **截图**：成功和失败场景均自动截全页，存 `${REPORT_DIR}/screenshots/`，报告内嵌展示

## 报告内容

HTML 报告含摘要卡片（场景总数/通过/失败/错误/通过率/耗时）、按 feature 分组的分区（可折叠）、失败场景的**失败截图 + 错误堆栈**、通过场景的**场景截图**。样式定义在 `template/ui_report_template.html`。

## 输出文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 测试报告 | `${REPORT_DIR}/report_<timestamp>.html` | 带时间戳报告 |
| 最新报告 | `${REPORT_DIR}/latest.html` | 指向最新报告 |
| 截图 | `${REPORT_DIR}/screenshots/*.png` | 成功/失败场景截图 |
| JUnit 缓存 | `${REPORT_DIR}/.cache/results_<module>.xml` | 临时 |

## 报告后的经验沉淀钩子（重要）

本 skill 只负责执行 + 报告，**不分析失败**（铁律见上）。但报告已产出：
- 若本次执行 **0 失败**：正常结束，无需后续动作。
- 若存在失败：**在输出统计与报告路径后，主动询问用户是否分析本次失败用例**（调用 `post-run-analysis` skill），例如：

  > 本次 UI 测试有 N 个失败场景（截图已存 screenshots/）。是否分析失败原因并沉淀为项目级/企业级经验？

  由用户决定；用户同意后，分析、归类、确认、回写等流程交给 `post-run-analysis` skill 执行，本 skill 不再参与。

- 前置检查（可选增强）：执行前可先读 `experience-library/ENTERPRISE-KNOWN-ISSUES.md`（仓库根）对照已知的企业级坑（如 pytest-bdd 步骤注册机制、UI 定位规范、文案取真实值）。
