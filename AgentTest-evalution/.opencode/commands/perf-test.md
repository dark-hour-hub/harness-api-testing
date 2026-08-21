---
description: 接口性能测试全流程（性能场景生成 → jmx 脚本生成 → JMeter 压测执行与报告）
---

# 接口性能测试全流程

全程串联执行：场景生成 → 脚本生成 → 压测执行。每步产出物作为下一步输入。

> 本流程与功能测试（`test` 命令）平行独立，不复用其 skill 与产物。


### 01 · 性能场景生成（AI 介入）

调用 `api-doc-to-perf` skill，从模块文档、实体文档、认证分析报告生成性能场景 YAML。

**输入**：
- `tests/baseline/_workflow/03-api-docs/API接口文档.md`
- `tests/baseline/_workflow/03-api-docs/_manifest.yaml`
- `tests/baseline/_workflow/03-api-docs/modules/*.md`
- `tests/baseline/_workflow/02-analysis-plan/auth-analysis.md`

**产物**：`tests/baseline/_workflow/05-perf-scenarios/{模块}.yaml`

**产物即证据**：阶段完成后自动验证 `05-perf-scenarios/` 目录存在且包含 YAML 文件，缺失则流程中止。


### 02 · 压测脚本生成（自动）

调用 `yaml-to-jmx` skill，读取性能场景 YAML，生成 JMeter `.jmx` 脚本与场景清单。

**输入**：`tests/baseline/_workflow/05-perf-scenarios/*.yaml`

**产物**：
- `tests/baseline/generated/api-perf/{scenario_id}.jmx`
- `tests/baseline/generated/api-perf/_scenarios.json`

**产物即证据**：阶段完成后自动验证 `generated/api-perf/` 目录存在且包含 `.jmx` 文件与 `_scenarios.json`，缺失则流程中止。


### 03 · 压测执行与报告（自动）

调用 `perf-runner` skill，逐场景执行 JMeter 压测并生成 HTML 报告。**此阶段只执行不修复：禁止分析未达标原因、修改场景、重新执行。**

**输入**：`tests/baseline/generated/api-perf/`

**产物**：`tests/baseline/report/api-perf/report_<timestamp>.html`

**产物即证据**：阶段完成后自动验证报告文件存在，缺失则流程中止。
