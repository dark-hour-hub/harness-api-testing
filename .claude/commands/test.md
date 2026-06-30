# 接口测试全流程

全程串联执行：配置检查 → 源码分析 → 用例设计 → 脚本生成 → 用例执行。每步产出物作为下一步输入。

- 遵循规则: [测试用例编写标准](../rules/testCase-standards.md)
- 遵循规则: [接口测试要点规范](../rules/testPoint-interface.md)


### 01 · 配置检查（自动）

```
python scripts/check_env_deps.py
```

**行为**：执行 `scripts/check_env_deps.py`，检查运行环境配置（Python 版本、依赖包、浏览器驱动等）。

**产物**：`tests/baseline/_workflow/01-config/output.json`

**产物即证据**：阶段完成后脚本自动验证 `output.json` 存在性，缺失则流程中止。


### 02 · 分析规划（AI 介入）

调用 `analyze-source` skill，完成源码分析。

**产物**：
- `tests/baseline/_workflow/02-analysis-plan/generation-plan.md`
- `tests/baseline/_workflow/02-analysis-plan/apis.json`

**产物即证据**：阶段完成后自动验证 `generation-plan.md` 存在性，缺失则流程中止。


### 03 · 用例设计（AI 介入）

调用 `testcase-generator` skill，读取 02 阶段的接口分析产物，结合源码验证字段、错误码，生成参数化测试用例 YAML。

**输入**：`config.yaml`

**产物**：`tests/baseline/_workflow/03-testcases/{module}-testcases.yaml`

**产物即证据**：阶段完成后自动验证 `03-testcases/` 目录存在且包含至少一个 YAML 文件，缺失则流程中止。


### 04 · 脚本生成（AI 介入）

调用 `pytest-generator` skill，读取 03 阶段的 YAML 测试用例定义，生成可执行的 pytest 测试脚本。

**输入**：`tests/baseline/_workflow/03-testcases/*.yaml`

**产物**：
- `tests/baseline/generated/api-test/test_{module}.py`
- `tests/baseline/generated/api-test/conftest.py`
- `tests/baseline/generated/api-test/pytest.ini`

**产物即证据**：阶段完成后自动验证 `generated/api-test/` 目录存在且包含测试脚本，缺失则流程中止。


### 05 · 用例执行（自动）

调用 `test-runner` skill，执行 04 阶段生成的 pytest 测试脚本并生成 HTML 报告。**此阶段只执行不修复：禁止分析失败原因、修改用例、重新执行。**

**输入**：`tests/baseline/generated/api-test/`

**产物**：`tests/baseline/report/api-test/*.html`

**产物即证据**：阶段完成后自动验证报告文件存在，缺失则流程中止。


### 05 · 用例执行结果分析（自动）

调用 `error-analyzer` skill，分析用例执行结果

**输入**：`tests/baseline/report/api-test/*`、`tests/baseline/generated/api-test/test_*.py`、

**产物**：`tests/baseline/_workflow/04-results/error-analysis.md`、`tests/baseline/_workflow/04-results/repair.md`

**产物即证据**：阶段完成后自动验证报告文件存在，缺失则流程中止。
