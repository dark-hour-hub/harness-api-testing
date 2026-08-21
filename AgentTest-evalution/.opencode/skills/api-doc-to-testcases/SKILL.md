---
name: api-doc-to-testcases
description: 从 API 接口文档生成 YAML 接口测试用例。支持全量模式（baseline）和增量模式（diff）。触发：/api-doc-to-testcases、从文档生成测试用例、接口文档转用例、doc to testcases、生成YAML测试用例、接口文档生成用例。
---

# API 文档 → YAML 测试用例生成器

从模块文档和实体文档提取接口信息，结合认证分析报告，按模块生成 YAML 格式的接口测试用例。

## 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|:---:|--------|------|
| `mode` | enum | 否 | `baseline` | `baseline` = 全量模式；`diff` = 增量模式 |

路径决议（按 mode）：

| 路径变量 | `baseline` | `diff` |
|---------|----------|--------|
| `DOC_ROOT` | `tests/baseline/_workflow/03-api-docs` | `tests/diff/_workflow/01-diff-api-doc` |
| `ANALYSIS_ROOT` | `tests/baseline/_workflow/02-analysis-plan` | 同 baseline（认证/框架分析无增量概念） |
| `OUTPUT_DIR` | `tests/baseline/_workflow/04-testcases` | `tests/diff/_workflow/02-diff-testcases` |
| `BASELINE_YAML_DIR` | — | `tests/baseline/_workflow/04-testcases`（仅 diff 模式，用于提取登录接口用例） |

## 输入

| 来源 | 路径 | 用途 |
|------|------|------|
| 主文档 | `${DOC_ROOT}/API接口文档.md` | 项目信息、Base URL、请求头模板、响应包装、测试账号、权限体系 |
| 认证分析 | `${ANALYSIS_ROOT}/auth-analysis.md` | 认证类型、Token 提取路径、拦截器链、白名单 |
| 清单文件 | `${DOC_ROOT}/_manifest.yaml` | 模块路由表（method、path、auth、permission、response_type） |
| 模块文档 | `${DOC_ROOT}/modules/*.md` | 各模块接口的请求参数、响应结构、错误响应、**业务规则** |
| 文档内断言 | `${DOC_ROOT}/modules/*.md`（仅 diff 模式） | diff 文档中已有的预期断言，优先参照 |
| 实体文档 | `${DOC_ROOT}/entities/*.md` | 请求体/响应体的 JSON 字段定义、校验规则 |
| 用例规则 | `../../rules/testCase-standards.md` | 用例要素、断言规范、命名标准 |
| 接口规则 | `../../rules/testPoint-interface.md` | 参数校验要点、错误路径覆盖 |

## 输出

```
${OUTPUT_DIR}/
├── 01-认证模块.yaml
├── 02-资源管理.yaml
├── 03-系统管理-part1-用户管理.yaml
├── ...
└── 06-工作流管理-part5-任务管理.yaml
```

每个 YAML 文件对应一个模块文档，文件命名与模块文档一致（仅扩展名改为 `.yaml`）。

---

## 执行流程

### Step 0 — 读取输入

根据 `mode` 参数确定 `${DOC_ROOT}`、`${ANALYSIS_ROOT}`、`${OUTPUT_DIR}`（见上方路径决议表），然后读取以下文件（所有模块 Agent 共享）：
1. `${DOC_ROOT}/API接口文档.md` → 提取 `base_url`、`headers_config`、`global_variables`、测试账号
2. `${ANALYSIS_ROOT}/auth-analysis.md` → 提取认证类型、登录接口、Token 前缀、Token 提取路径（JSON key）
3. `${DOC_ROOT}/_manifest.yaml` → 提取每个模块的路由列表（method、path、auth、request_body、response_type）
4. `.opencode/references/testcase-example.yaml` → YAML 模板参考

详细字段提取规则见 [references/doc-mapping.md](references/doc-mapping.md)。

### Step 1 — 构建全局配置

从 Step 0 的输入构建所有模块共享的配置块。详见 [references/auth-config.md](references/auth-config.md)。

**headers_config**：
- `public_headers`：直接从主文档「公开接口」请求头表格照抄
- `auth_headers`：直接从主文档「认证接口」请求头表格照抄，Token 类字段用 `${auth.xxx}` 引用

**auth_setup**：
- `type`：从 auth-analysis.md 判定（Sa-Token JWT → `bearer_token`）
- `login_endpoint`：纯路径，从 auth-analysis.md 登录接口获取
- `token_prefix`：从 auth-analysis.md 获取（如 `Bearer `）
- `params`：读取登录接口的请求体实体文档，从「字段定义」表的「JSON 键名」列获取参数名，值从 `_manifest.yaml` 的 `test_accounts` 提取。**key 名必须与请求体实体文档的 JSON 键名一致**
- `accounts`：从 manifest 的 `test_accounts` 提取（账号名、密码）
- `extracts`：从 auth-analysis.md 登录响应表提取，**字段名用 JSON key**

**global_variables**：从主文档提取全局常量（如默认分页大小）。

**校验**：构建完成后校验所有引用一致性（auth_headers 中引用的 `${auth.xxx}` 路径必须能在 auth_setup 中解析）。

### Step 2 — 并行派发模块 Agent

对 `${DOC_ROOT}/modules/` 下每个 `.md` 文件并行派发一个 Agent。

**diff 模式前置操作**：派发模块 Agent 之前，先从 `${BASELINE_YAML_DIR}` 提取登录接口用例。遍历该目录下所有 `.yaml` 文件，查找 `path` 等于 `auth_setup.login_endpoint` 且 `method` 为 `POST` 的用例（正向+反向各 1 条）。将这些用例写入 `${OUTPUT_DIR}` 下的一个新 YAML 文件，该文件的 `headers_config`、`auth_setup`、`global_variables` 使用 Step 1 构建的全局配置，`module` 取来源 YAML 的 module 值，`module_name` 取来源 YAML 的 module_name 值，`testcases` 仅包含找到的登录接口正反用例。此文件为后续 `yaml-to-pytest` 脚本的 `_do_login()` 提供登录请求体模板。若已存在含登录用例的 YAML 则跳过。基线认证模块不在 diff 范围内时此步骤必须执行。

**优先级**：含登录接口用例的 YAML 必须最先完成，因为其他模块的 pytest 脚本依赖它提供登录请求体模板。其余模块可并行。

**Agent 输入**（每个 Agent 收到的完整上下文）：
1. 全局配置（Step 1 产物，所有 Agent 相同）
2. 本模块文档全文
3. 本模块引用的实体文档（Agent 按需从 `${DOC_ROOT}/entities/` 只读本模块用到的）

**Agent Prompt 模板**见 [template/module-agent-prompt.md](template/module-agent-prompt.md)。派发时将以下占位符替换为实际路径：
- `{ENTITY_PATH}` → `${DOC_ROOT}/entities/`
- `{OUTPUT_PATH}` → `${OUTPUT_DIR}`

**Agent 任务**：按模板生成 YAML，遵循以下规则（详见 references）：

| 规则类别 | 参考文件 |
|---------|---------|
| YAML 字段定义与约束 | [references/yaml-schema.md](references/yaml-schema.md) |
| 用例设计原则 | [references/case-design.md](references/case-design.md) |
| 文档→YAML 字段映射 | [references/doc-mapping.md](references/doc-mapping.md) |
| 变量引用规范 | [references/variable-reference.md](references/variable-reference.md) |
| 生成约束与校验 | [references/generation-rules.md](references/generation-rules.md) |
| 业务规则与断言参照 | 本文件 Step 2.5 |

### Step 2.5 — 业务规则与断言参照（Agent 内执行）

Agent 在生成用例时，额外执行以下逻辑：

#### 业务规则参照

若模块文档中包含「业务规则」表/章节，Agent 应：

1. 解析业务规则表，提取每条规则的触发条件和预期行为
2. **正向用例**：确保请求参数不违反任何业务规则
3. **反向用例**：优先从业务规则中选取 1 个典型违规场景作为测试条件，而非仅依赖「错误响应」表
4. 若业务规则与错误响应表有重叠，优先使用业务规则的描述来构造操作步骤和预期结果

#### 断言参照（仅 mode=diff）

diff 模式下，模块文档可能已包含每个接口的预期断言信息（如预期 HTTP 状态码、业务码、响应字段存在性等）。Agent 应：

1. 检查文档中每个接口是否已声明 `expected.status_code`、`expected.business_code`、`expected.data_exists` 等信息
2. **若文档有断言**：直接照搬文档断言到 YAML 的 `expected` 块，仅做格式转换（如将表格式转为 YAML 结构）
3. **若文档无断言**：回退到默认规则自行推断
4. 文档断言优先级：文档明确写的值 > Agent 推断值

### Step 3 — 校验与修复

所有 Agent 完成后，运行校验脚本：

```bash
python .opencode/skills/api-doc-to-testcases/scripts/validate_yaml.py ${OUTPUT_DIR}/
```

校验不通过的文件 → 派修复 Agent，仅修该文件的具体 ERROR，不重生成。修复后重跑校验，最多 2 轮。

---

## 禁止项

- `login_endpoint` 含 HTTP 方法前缀（如 `POST /auth/login`）→ 必须是纯路径
- `data_exists` / `request.body` 使用 Java 字段名 → 必须使用 JSON 键名（从实体文档确认）
- 在 `request.headers` 中手写已在 `headers_config.auth_headers` 中声明的认证头
- 对 `auth_setup.accounts` 中列出的账号生成增/删/改用例
- 自创模板中不存在的 YAML 字段
- Agent 预读全量实体文件（仅读本模块引用的）
- 认证接口的用例缺少 `auth.required: true`
