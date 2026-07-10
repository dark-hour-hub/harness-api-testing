---
name: test-runner
description: 执行 generated/api-test/ 下的 pytest 测试脚本并生成 HTML 报告。触发方式：/test-runner、运行API测试、执行接口测试、生成测试报告、pytest api test、run api tests and generate report、跑接口测试、执行pytest测试。每次用户提到运行测试、执行测试脚本、生成测试报告时使用此 skill。
---

# API 测试执行与报告生成

执行 `tests/baseline/generated/api-test/` 下的 pytest 测试脚本，将结果输出为 HTML 报告。

## 范围

此 skill 仅做两件事：**执行** pytest 测试脚本 + **生成** HTML 报告。不分析、不修复、不重跑。

## ⛔ 铁律

执行结束后，无论通过率多少，**严格禁止**以下行为：

- 禁止分析失败用例的根因（即使失败率很高）
- 禁止查看失败用例的响应体或错误堆栈
- 禁止修改 YAML 测试用例定义
- 禁止修改生成的 pytest 测试脚本
- 禁止向用户建议修复方案
- 禁止重新执行测试（即使只改了一个小参数）
- 禁止说"让我验证一下"、"让我看一眼"、"再跑一次确认"

**红牌思想** — 出现以下念头时立刻停止：

| 红牌思想 | 现实 |
|---------|------|
| "失败率这么高，我看一眼原因" | 分析失败 = 违反铁律。输出摘要即结束。 |
| "改一个小参数就能全过" | 修改 YAML/脚本 = 违反铁律。 |
| "让我验证修复效果" | 验证 = error-analyzer 的事，不是 test-runner 的事。 |
| "再跑一次确认是不是偶发" | 禁止重跑。一次运行，一个报告。 |
| "这个错误很明显，我可以快速定位" | 不难也不准。结束。 |

**唯一允许的动作**：按下方输出模板输出统计摘要和报告路径，然后立即结束。

## 输出模板

执行完成后**严格按此格式**输出，不增减内容：

```
**测试执行完成**

| 文件 | 用例数 | 通过 | 失败 | 错误 | 耗时 |
|------|--------|------|------|------|------|
| test_xxx.py | N | N | N | N | Xs |

**合计**: N 通过 / M 总计 (X%)
**报告**: `tests/baseline/report/api-test/report_<timestamp>.html`
```

最后一行"报告"之后不再输出任何内容。存在失败用例时也不追加分析建议。

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

HTML 报告含摘要卡片、失败分类、通过率饼图、耗时分布图、详细结果表（含筛选/分页/按模块分组）。样式定义在 `template/report_template.html`。

## 输出文件


| 文件 | 路径                                              | 说明 |
|------|-------------------------------------------------|------|
| 测试报告 | `tests/baseline/report/api-test/report_<timestamp>.html` | 带时间戳的聚合报告 |
| 最新报告 | `tests/baseline/report/api-test/latest.html`    | 始终指向最新报告 |
| JUnit 缓存 | `tests/baseline/report/api-test/.cache/results_<module>.xml` | 各模块独立 XML（临时） |

