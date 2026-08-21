# UI 测试全流程

业务需求驱动：场景设计 → 脚本生成 → 执行截图出报告。每步产物作为下一步输入。

### 01 · 需求整理（AI 介入）

把业务需求沉淀为文档，作为场景设计的固定输入。

**输入**：用户提供的业务需求/业务流程描述（若 `ui-requirements.md` 已存在则直接复用，跳过录入）

**产物**：`tests/baseline/_workflow/00-requirements/ui-requirements.md`

**产物即证据**：阶段完成后验证该文件存在且包含业务模块清单，缺失则流程中止（提示用户补充需求）。

### 02 · 环境检查（自动）

检查 UI 测试运行环境：Python 依赖（pytest-bdd / pytest-playwright / playwright）、chromium 浏览器驱动、前端地址配置。

```bash
python scripts/check_ui_env.py
```

**产物**：`tests/baseline/_workflow/01-config/ui-env.json`

**产物即证据**：阶段完成后验证 `ui-env.json` 存在且 `ready=true`，否则流程中止。

### 03 · 场景设计（AI 介入）

调用 `ui-scenario-design` skill，以业务需求文档为输入，读前端源码提取定位文案，产出 Gherkin 场景。

**输入**：`tests/baseline/_workflow/00-requirements/ui-requirements.md`、`config.yaml`（前端路径 + 地址 + 账号）、前端源码

**产物**：
- `tests/baseline/_workflow/04-ui-scenarios/*.feature`
- `tests/baseline/_workflow/04-ui-scenarios/_manifest.yaml`

**产物即证据**：验证至少一个 `.feature` 文件 + `_manifest.yaml` 存在，缺失则流程中止。

### 04 · 脚本生成（自动）

调用 `feature-to-playwright` skill，读取 `.feature` 生成 pytest-bdd + Playwright 脚本。

**输入**：`tests/baseline/_workflow/04-ui-scenarios/*.feature`

**产物**：
- `tests/baseline/generated/ui-test/test_{module}.py`
- `tests/baseline/generated/ui-test/conftest.py`

**产物即证据**：验证 `generated/ui-test/` 存在 `conftest.py` 和至少一个 `test_*.py`，缺失则流程中止。

### 05 · 执行与报告（自动）

调用 `ui-runner` skill，chromium 无头执行测试，成功/失败自动截图，生成含截图的 HTML 报告。**此阶段只执行不修复：禁止分析失败原因、修改场景、重新执行。**

**输入**：`tests/baseline/generated/ui-test/`

**产物**：
- `tests/baseline/report/ui-test/report_*.html`
- `tests/baseline/report/ui-test/screenshots/*.png`

**产物即证据**：验证报告文件存在，缺失则流程中止。
