### 01 · 配置检查（自动）

```
python scripts/check_env_deps.py
```

**行为**：
- 执行python脚本`scripts/check_env_deps.py`，检查运行环境配置（Python 版本、依赖包、浏览器驱动等）

**产物**：`tests/baseline/_workflow/01-config/output.json`

**产物即证据**：阶段完成后脚本自动验证 `output.json` 存在性，缺失则流程中止。


### 02 · 分析规划（AI 介入）

调用 `analyze-source` skill，完成源码分析

**产物**：`tests/baseline/_workflow/02-analysis-plan/generation-plan.md`

**产物即证据**：AI 阶段完成后脚本自动验证 `generation-plan.md` 存在性，缺失则流程中止。


### 03 · 用例生成（AI 介入）

调用 `api-test-generator` skill，完成用例脚本生成，脚本生成需要遵循

[测试用例编写标准]: ../rules/testCase-standards.md

**产物**：`tests/baseline/generated/api-test/*.py`

### 04 · 用例执行（AI 介入）
调用 `test-runner` skill，执行用例

**产物**：`tests/baseline/report/api-test/*.html`

