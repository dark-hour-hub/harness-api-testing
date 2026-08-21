# Agent 派发 Prompt 模板

向每个模块 Agent 派发时使用此模板。`{PLACEHOLDER}` 由主会话替换。

---

## 任务

你是一个测试用例生成器。根据以下模块 API 文档生成 YAML 格式的接口测试用例。

## 全局配置（所有模块共享）

以下 `headers_config`、`auth_setup`、`global_variables` 已从主文档和认证分析报告中提取，直接使用，**不要修改**：

```yaml
{HEADERS_CONFIG_YAML}

{AUTH_SETUP_YAML}

{GLOBAL_VARIABLES_YAML}
```

base_url: `{BASE_URL}`

## 模块文档

以下是要生成用例的模块文档全文：

```markdown
{MODULE_DOC_CONTENT}
```

## 模块路由清单

从 `_manifest.yaml` 提取的本模块路由：

```yaml
{MODULE_ROUTES_YAML}
```

## 引用的实体文档

本模块接口引用的实体文档，按需读取 `{ENTITY_PATH}` 下的文件。

**不要预读全量实体文件**，只读取本模块用到的实体。

- 请求体引用的实体（如 `SysUserBo`）→ 读取 `entities/SysUserBo.md` 获取 JSON 字段和校验规则
- 响应体引用的实体（如 `SysUserVo`）→ 读取 `entities/SysUserVo.md` 获取 `data_exists` 候选字段

## 输出要求

将生成的 YAML 写入 `{OUTPUT_PATH}/{MODULE_FILE_NAME}.yaml`。

## 生成规则摘要

### 基本规则
- 每个接口生成 1 条正向用例（P0）+ 1 条反向用例（P1）
- 文件导出/下载接口（response_type: void）跳过，不生成用例

### 正向用例
- 填合法必填字段，断言 `status_code` + `business_code` + 1-2 个 `data_exists`
- 不填 `data_equals`
- tags: `[正常, 回归]`，核心接口加 `[冒烟]`

### 反向用例
- 从错误响应表中选 1 个最有代表性的触发条件
- 优先必填参数缺失或典型业务错误
- tags: `[异常, 回归]`

### 数据安全
- **禁止**对 `auth_setup.accounts` 中列出的账号生成增/删/改用例
- **禁止**对 `auth_setup.params` 中的资源生成删/改用例
- 需要增删改测试时，先 POST 新建数据，再对新建数据操作
- 认证永远使用提供的账号

### 字段名
- `request.body` 和 `data_exists` 的字段名必须是 **JSON 键名**（从实体文档确认）
- 不是 Java 字段名

### 变量引用
- `${auth.token}` — 跳过 extracts 层级
- `${auth.params.admin.xxx}` — 认证参数
- `${auth.accounts.admin.xxx}` — 账号信息
- `${global_variables.xxx}` — 全局变量
- `$.data.xxx` — 响应 JSONPath

### method 校验
- 必须是 `GET` / `POST` / `PUT` / `DELETE` / `PATCH` 之一
- 从文档「请求方式」提取后校验

### auth 校验
- `auth.required` 与文档「认证方式」一致
- `auth.account` 必须在 `auth_setup.accounts` 中存在

### 401/403 共性错误
- 不随每个模块重复生成
- 仅在认证模块生成 1 条 401 用例
- 仅在 1 个代表性接口生成 1 条权限不足用例

### ID 和标题
- ID: `TC_{MODULE}_{NNN}`
- 标题: `{METHOD} {路径}_{条件}_{预期}`

## 参考规则

完整规则文件见 skill 的 references/ 目录：
- `yaml-schema.md` — YAML 字段定义与约束
- `case-design.md` — 用例设计原则
- `doc-mapping.md` — 文档→YAML 映射
- `variable-reference.md` — 变量引用规范
- `generation-rules.md` — 生成约束

### 业务规则

- 若模块文档包含「业务规则」表，逐条解析规则的触发条件和预期行为
- **反向用例条件优先从业务规则中选取**（优先于错误响应表）
- 正向用例的请求参数不得违反业务规则
- 业务规则中的校验逻辑（如"用户名不能重复"、"金额必须大于0"）→ 转化为反向用例的触发条件

### 断言参照（diff 模式）

- 若文档接口已声明预期断言（status_code、business_code、data_exists），**直接使用文档断言值**
- 不自行修改或推断文档已给出的断言
- 仅当文档缺少断言信息时，才回退到默认推断规则
- 文档断言格式为表格 → 提取值填入 YAML expected 块

直接开始生成，不需要确认。
