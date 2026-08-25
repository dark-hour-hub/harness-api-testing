---
name: feature-to-playwright
description: 从 Gherkin .feature 场景生成 pytest-bdd + Playwright 测试脚本。为每个 feature 生成 test_{module}.py（scenarios 绑定），复制 conftest.py（含通用步骤库 + 自动截图 hook）。触发：/feature-to-playwright、Gherkin转Playwright、生成UI测试脚本、feature转pytest、生成playwright脚本、gherkin to playwright。
---

# Gherkin → Playwright 脚本生成器

读取 `.feature` 场景文件，生成 pytest-bdd + Playwright 可执行脚本。

## 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|:---:|--------|------|
| `mode` | enum | 否 | `baseline` | `baseline` = 全量；`diff` = 增量 |

路径决议（按 mode）：

| 路径变量 | `baseline` | `diff` |
|---------|----------|--------|
| `FEATURE_DIR` | `tests/baseline/_workflow/04-ui-scenarios` | `tests/diff/_workflow/02-ui-scenarios` |
| `OUTPUT_DIR` | `tests/baseline/generated/ui-test` | `tests/diff/generated/ui-test` |

## 设计原则

- **场景即脚本**：每个 feature 生成一个 `test_{module}.py`，内部用 `pytest_bdd.scenarios()` 绑定全部场景
- **通用步骤库**：`conftest.py` 内置通用 Gherkin 步骤（打开页面/登录/点击/填写/断言提示/断言表格），覆盖绝大多数 Element Plus 交互
- **自动截图**：conftest 的 `pytest_runtest_makereport` hook 在场景结束时（成功和失败）截图，写入 JUnit XML 的 `screenshot` property，供报告展示
- **配置驱动**：`base_url` 从 `config.yaml` 的 frontend url 读取，`--base-url` 可覆盖，脚本不硬编码地址

## 输出

```
${OUTPUT_DIR}/
├── conftest.py         # 通用步骤库 + base_url fixture + 自动截图 hook
├── test_login.py       # 对应 01-登录.feature
├── test_book.py        # 对应 02-图书管理.feature
└── ...
```

## 执行

```bash
# 全量模式（默认）
python .opencode/skills/feature-to-playwright/scripts/generate_playwright.py --mode baseline

# 增量模式
python .opencode/skills/feature-to-playwright/scripts/generate_playwright.py --mode diff

# 显式指定路径
python .opencode/skills/feature-to-playwright/scripts/generate_playwright.py \
  --feature-dir tests/baseline/_workflow/04-ui-scenarios \
  --output-dir tests/baseline/generated/ui-test
```

## 生成内容说明

### 生成后自检（必做，防再犯）

生成完成后立即执行（不启动浏览器，秒级暴露步骤错配）：

```bash
python -m pytest ${OUTPUT_DIR} --collect-only -q
```

- 若输出 `StepDefinitionNotFoundError`（如 `Given "点击链接 "x""`）→ **feature 文件关键字错配**
  （`And` 在 `Given` 行之后继承了 given 关键字），先修 feature 再重新生成；
- 若 `collection succeeded` 无报错 → 才进入执行阶段。

### test_{module}.py

- 用绝对路径定位 feature 文件（`Path(__file__).resolve()`），pytest 从任何目录执行都不会出错
- 调用 `scenarios(str(FEATURE_DIR / "xx.feature"))` 自动注册所有场景

### conftest.py（通用步骤库）

内置以下可复用步骤（详见 `template/conftest.py`）：

| 类型 | 步骤 | 实现 |
|------|------|------|
| Given | `打开首页 "<url>"` / `打开首页` | `page.goto` |
| Given | `以账号 "<u>" 密码 "<p>" 登录` | 填用户名/密码 + 点登录按钮 |
| When | `点击菜单 "<文本>"` | `get_by_role("menuitem")` |
| When | `点击按钮 "<文本>"` | `get_by_role("button")`，跳过 disabled |
| When | `点击链接 "<文本>"` | `get_by_role("link")` |
| When | `在 "<字段>" 输入框中输入 "<值>"` | placeholder→label→role 回退定位 |
| When | `等待 <N> 秒` | `wait_for_timeout` |
| Then | `应看到提示 "<文本>"` | `get_by_text` 可见 |
| Then | `页面应包含 "<文本>"` | `get_by_text` 可见 |
| Then | `表格应包含 "<文本>"` | `get_by_role("cell")` 可见 |
| Then | `应看到按钮 "<文本>"` | `get_by_role("button")` 可见 |

## 特殊步骤扩展

通用库覆盖不了的特殊交互（拖拽、上传、自定义组件），在 `OUTPUT_DIR` 下新建 `steps/{module}_steps.py` 定义专属步骤，并在对应 `test_{module}.py` 中 `import`。

## DB 断言生成（防假成功）

- 输入：`00-requirements/db-asserts.yaml`（缺失/为空则跳过，不影响现有场景）
- 生成期静态校验（任一失败 → 中止）：映射 id 必须存在；表/列必须存在于后端 `db/schema.sql`；场景变量必须先声明后使用
- 产物：`${OUTPUT_DIR}/db_asserts.py`（编译后的 DB_ASSERT_MAP，含 SQL 常量），运行期由 `且数据已保存到 "<id>"` 步骤查库断言
- 禁止在场景/脚本中手写物理表名与 SQL（统一走生成器编译）

## 禁止项

- 禁止在生成的脚本中硬编码 base_url（必须从 config.yaml 读）
- 禁止修改 `conftest.py`（它是模板产物，改动会被下次生成覆盖）
- 禁止生成 feature 中不存在的步骤

## 依赖

- `pytest-bdd`（Gherkin 场景解析）
- `pytest-playwright`（提供 `page` fixture）
- `playwright` + `chromium` 浏览器（`python -m playwright install chromium`）
