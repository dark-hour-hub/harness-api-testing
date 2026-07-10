---
name: api-doc-to-testcases
description: 从 API 接口文档（03-api-docs）生成 YAML 接口测试用例。输入为 modules/*.md 模块文档 + entities/*.md 实体文档 + 主文档 + auth-analysis.md，按模块生成 YAML 用例到 04-testcases/。触发：/api-doc-to-testcases、从文档生成测试用例、接口文档转用例、doc to testcases、生成YAML测试用例、接口文档生成用例。
---

# API 文档 → YAML 测试用例生成器

从 `tests/baseline/_workflow/03-api-docs/` 下的模块文档和实体文档提取接口信息，结合认证分析报告，按模块生成 YAML 格式的接口测试用例。

## 输入

| 来源 | 路径 | 用途 |
|------|------|------|
| 主文档 | `03-api-docs/API接口文档.md` | 项目信息、Base URL、请求头模板、响应包装、测试账号、权限体系 |
| 认证分析 | `02-analysis-plan/auth-analysis.md` | 认证类型、Token 提取路径、拦截器链、白名单 |
| 清单文件 | `03-api-docs/_manifest.yaml` | 模块路由表（method、path、auth、permission、response_type） |
| 模块文档 | `03-api-docs/modules/*.md` | 各模块接口的请求参数、响应结构、错误响应、业务规则 |
| 实体文档 | `03-api-docs/entities/*.md` | 请求体/响应体的 JSON 字段定义、校验规则 |
| 用例规则 | `../../rules/testCase-standards.md` | 用例要素、断言规范、命名标准 |
| 接口规则 | `../../rules/testPoint-interface.md` | 参数校验要点、错误路径覆盖 |

## 输出

```
tests/baseline/_workflow/04-testcases/
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

主会话读取以下文件（所有模块 Agent 共享）：
1. 主文档 → 提取 `base_url`、`headers_config`、`global_variables`、测试账号
2. `auth-analysis.md` → 提取认证类型、登录接口、Token 前缀、Token 提取路径（JSON key）
3. `_manifest.yaml` → 提取每个模块的路由列表（method、path、auth、request_body、response_type）
4. `.claude/references/testcase-example.yaml` → YAML 模板参考

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
- `params`：从主文档测试账号信息 + manifest 提取（clientId、tenantId 等）
- `accounts`：从 manifest 的 `test_accounts` 提取（账号名、密码）
- `extracts`：从 auth-analysis.md 登录响应表提取，**字段名用 JSON key**

**global_variables**：从主文档提取全局常量（如默认分页大小）。

**校验**：构建完成后校验所有引用一致性（auth_headers 中引用的 `${auth.xxx}` 路径必须能在 auth_setup 中解析）。

### Step 2 — 并行派发模块 Agent

对 `modules/` 下每个 `.md` 文件并行派发一个 Agent。

**优先级**：认证模块（`01-认证模块.md`）必须最先完成，因为其他模块需要确认 `auth_setup` 的正确性。其余模块可并行。

**Agent 输入**（每个 Agent 收到的完整上下文）：
1. 全局配置（Step 1 产物，所有 Agent 相同）
2. 本模块文档全文
3. 本模块引用的实体文档（Agent 按需从 `entities/` 只读本模块用到的）

**Agent 任务**：按模板生成 YAML，遵循以下规则（详见 references）：

| 规则类别 | 参考文件 |
|---------|---------|
| YAML 字段定义与约束 | [references/yaml-schema.md](references/yaml-schema.md) |
| 用例设计原则 | [references/case-design.md](references/case-design.md) |
| 文档→YAML 字段映射 | [references/doc-mapping.md](references/doc-mapping.md) |
| 变量引用规范 | [references/variable-reference.md](references/variable-reference.md) |
| 生成约束与校验 | [references/generation-rules.md](references/generation-rules.md) |

**Agent Prompt 模板**见 [template/module-agent-prompt.md](template/module-agent-prompt.md)。

### Step 3 — 校验与修复

所有 Agent 完成后，运行校验脚本：

```bash
python .claude/skills/api-doc-to-testcases/scripts/validate_yaml.py tests/baseline/_workflow/04-testcases/
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
