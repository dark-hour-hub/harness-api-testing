---
name: perf-runner
description: 执行 JMeter .jmx 压测脚本并生成性能测试 HTML 报告。触发：/perf-runner、运行性能测试、执行压测、生成性能报告、run jmeter、跑压测、执行性能测试。每次用户提到运行压测、执行性能测试、生成性能报告时使用此 skill。
---

# 性能压测执行与报告生成

逐场景串行执行 JMeter `.jmx` 压测脚本，解析 `.jtl` 结果，与阈值比对，生成 HTML 报告。

## 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|:---:|--------|------|
| `mode` | enum | 否 | `baseline` | `baseline` = 全量模式；`diff` = 增量模式 |

路径决议（按 mode）：

| 路径变量 | `baseline` | `diff` |
|---------|----------|--------|
| `JMX_DIR` | `tests/baseline/generated/api-perf` | `tests/diff/generated/api-perf` |
| `REPORT_DIR` | `tests/baseline/report/api-perf` | `tests/diff/report/api-perf` |

## 范围

此 skill 仅做两件事：**执行** JMeter 压测 + **生成** HTML 报告。不分析、不修复、不重跑。

## 执行步骤

```bash
# 全量模式（默认）
python .opencode/skills/perf-runner/scripts/run_perf.py --mode baseline

# 增量模式
python .opencode/skills/perf-runner/scripts/run_perf.py --mode diff

# 只跑指定场景
python .opencode/skills/perf-runner/scripts/run_perf.py -k "perf_auth_001"

# 显式指定路径（优先级高于 --mode）
python .opencode/skills/perf-runner/scripts/run_perf.py --jmx-dir <dir> --output <dir>
```

## 执行流程

1. 从 `config.yaml` 的 `tools.jmeter` 定位 `jmeter.bat`（Windows）/ `jmeter`（Unix）
2. 读取 `_scenarios.json` 清单（jmx → id/thresholds/load）
3. 逐场景串行执行（每个 `.jmx` 独立 jmeter 进程，避免不同并发互相干扰）：
   ```bash
   jmeter -n -t <场景>.jmx -l <缓存>/result_<id>.jtl \
     -Jjmeter.save.saveservice.print_field_names=true \
     -Jjmeter.save.saveservice.output_format=csv
   ```
4. 解析 `.jtl`（主请求 label = scenario id，`login` 样本排除），统计：
   samples / avg / min / max / p50 / p90 / p95 / p99 / error_rate / rps
5. 与 `thresholds` 比对，任一超限即标记「不达标」
6. 生成聚合 HTML 报告

## 报告内容

- 摘要卡片：场景数、达标数、总请求数、平均 P95、平均错误率、达标率
- 场景明细表：每个场景的完整指标 + 阈值对比 + 达标/不达标标记
- 图表：各场景 P95 柱状图（达标绿/不达标红）、各场景 RPS 柱状图

报告命名格式：`report_<YYYYMMDD_HHMMSS>.html`，同时更新 `latest.html`。

## 输出文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 性能报告 | `${REPORT_DIR}/report_<timestamp>.html` | 带时间戳的聚合报告 |
| 最新报告 | `${REPORT_DIR}/latest.html` | 始终指向最新报告 |
| JTL 缓存 | `${REPORT_DIR}/.cache/result_<id>.jtl` | 各场景原始结果 CSV |

## 报告后的经验沉淀钩子（重要）

本 skill 只负责执行 + 报告，**不分析未达标根因**（铁律见上）。但报告已产出：
- 若全部达标：正常结束，无需后续动作。
- 若存在不达标：**在输出统计与报告路径后，主动询问用户是否分析本次不达标场景**（调用 `post-run-analysis` skill），例如：

  > 本次压测有 N 个不达标场景。是否分析失败原因并沉淀为项目级/企业级经验？（注意区分：被测系统性能问题 vs 压测数据污染/客户端限制/脚本问题）

  由用户决定；用户同意后，分析、归类、确认、回写等流程交给 `post-run-analysis` skill 执行，本 skill 不再参与。

- 前置检查（可选增强）：执行前可先读 `D:\AI-Test\AIHarness\experience-library\ENTERPRISE-KNOWN-ISSUES.md` 对照已知的企业级坑（如 JMeter 唯一编码用 `__RandomString`、Windows 子进程编码、先读后写防污染、端口耗尽）。

## 铁律

执行结束后，无论达标率多少，**禁止**以下行为：

- 禁止分析未达标场景的根因
- 禁止修改 YAML 性能场景定义或 `.jmx` 脚本
- 禁止重新执行测试
- 禁止向用户建议性能调优方案

唯一允许的动作：输出统计摘要和报告路径；若存在不达标场景，追加一句"是否分析本次不达标场景"的询问（后续交给 `post-run-analysis` skill），然后结束。

## 输出模板

执行完成后严格按此格式输出：

```
**性能压测执行完成**

| 场景 | 并发 | 样本 | Avg | P95 | P99 | RPS | 错误率 | 结果 |
|------|------|------|-----|-----|-----|-----|--------|------|
| PERF_xxx_001 | 100 | N | Xms | Xms | Xms | X | X% | 达标/不达标 |

**合计**: N 场景 / M 达标 (X%)
**报告**: `${REPORT_DIR}/report_<timestamp>.html`
```

最后一行"报告"之后不再输出任何内容。存在不达标场景时仅可追加"是否分析本次不达标场景"的一句询问（交给 `post-run-analysis` skill）。
