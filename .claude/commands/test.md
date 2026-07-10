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


### 03 · 框架分析（AI 介入）

调用 `framework-analyzer` skill，完成框架和认证机制分析。

**产物**：
- `tests/baseline/_workflow/02-analysis-plan/framework-analysis.md`

**产物即证据**：阶段完成后自动验证 `framework-analysis.md` 存在性，缺失则流程中止。


### 04 · 接口发现（AI 介入）

调用 `api-doc-discover` skill，扫描后端源码发现所有 API 路由，按模块分组，输出结构化清单和主文档骨架。

**输入**：`config.yaml`、`tests/baseline/_workflow/02-analysis-plan/auth-analysis.md`、`tests/baseline/_workflow/02-analysis-plan/framework-analysis.md`

**产物**：
- `tests/baseline/_workflow/03-api-docs/_manifest.yaml`
- `tests/baseline/_workflow/03-api-docs/API接口文档.md`

**产物即证据**：阶段完成后自动验证 `_manifest.yaml` 和 `API接口文档.md` 存在，缺失则流程中止。


### 05 · 实体文档生成（AI 介入）

调用 `api-doc-entities` skill，读取 `_manifest.yaml` 中的 DTO/VO 清单，按模块并行生成实体类文档。

**输入**：`tests/baseline/_workflow/03-api-docs/_manifest.yaml`

**产物**：
- `tests/baseline/_workflow/03-api-docs/entities/{ClassName}.md`
- `tests/baseline/_workflow/03-api-docs/entities/_index.yaml`

**产物即证据**：阶段完成后自动验证 `entities/` 目录存在且包含 `_index.yaml` 和至少一个实体 md 文件，缺失则流程中止。


### 06 · 模块文档生成（AI 介入）

调用 `api-doc-module` skill，读取 `_manifest.yaml` 路由清单，按模块并行生成接口明细文档。

**输入**：`tests/baseline/_workflow/03-api-docs/_manifest.yaml`、`tests/baseline/_workflow/03-api-docs/API接口文档.md`、`tests/baseline/_workflow/03-api-docs/entities/`

**产物**：`tests/baseline/_workflow/03-api-docs/modules/{模块}.md`

**产物即证据**：阶段完成后自动验证 `modules/` 目录存在且包含至少一个 md 文件，缺失则流程中止。


### 07 · 文档组装（AI 介入）

调用 `api-doc-assemble` skill，回填主文档模块概览表、汇总已知问题、校验模块文档完整性。

**输入**：`tests/baseline/_workflow/03-api-docs/API接口文档.md`、`tests/baseline/_workflow/03-api-docs/_manifest.yaml`、`tests/baseline/_workflow/03-api-docs/modules/`、`tests/baseline/_workflow/03-api-docs/entities/_index.yaml`

**产物**：
- `tests/baseline/_workflow/03-api-docs/API接口文档.md`（更新：回填模块概览 + 已知问题）
- `tests/baseline/_workflow/03-api-docs/_manifest.yaml`（更新：回写实际接口数）

**产物即证据**：阶段完成后自动验证 `API接口文档.md` 中"模块概览"表已填充，缺失则流程中止。


### 08 · 用例生成（AI 介入）

调用 `api-doc-to-testcases` skill，读取模块文档和实体文档，结合认证分析报告，按模块生成 YAML 格式接口测试用例。

**输入**：`tests/baseline/_workflow/03-api-docs/API接口文档.md`、`tests/baseline/_workflow/03-api-docs/_manifest.yaml`、`tests/baseline/_workflow/03-api-docs/modules/*.md`、`tests/baseline/_workflow/02-analysis-plan/auth-analysis.md`

**产物**：`tests/baseline/_workflow/04-testcases/{模块}.yaml`

**产物即证据**：阶段完成后自动验证 `04-testcases/` 目录存在且包含 YAML 文件，缺失则流程中止。


### 09 · 脚本生成（AI 介入）

调用 `yaml-to-pytest` skill，读取 YAML 测试用例，生成可执行的 pytest 脚本和 conftest.py。

**输入**：`tests/baseline/_workflow/04-testcases/*.yaml`

**产物**：
- `tests/baseline/generated/api-test/test_{module}.py`
- `tests/baseline/generated/api-test/conftest.py`

**产物即证据**：阶段完成后自动验证 `generated/api-test/` 目录存在且包含测试脚本和 conftest.py，缺失则流程中止。


### 10 · 用例执行（自动）

调用 `test-runner` skill，执行 pytest 测试脚本并生成 HTML 报告。**此阶段只执行不修复：禁止分析失败原因、修改用例、重新执行。**

**输入**：`tests/baseline/generated/api-test/`

**产物**：`tests/baseline/report/api-test/*.html`

**产物即证据**：阶段完成后自动验证报告文件存在，缺失则流程中止。

