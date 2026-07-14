# YAML 字段规范

每个模块 YAML 文件的完整字段定义、类型、约束和枚举值。

---

## 顶层字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `module` | string | 是 | 模块标识，纯字母数字下划线，如 `auth`、`system_user` |
| `module_name` | string | 是 | 模块中文名，如 `"认证模块"` |
| `base_url` | string | 是 | 服务端 Base URL，不含尾部斜杠，如 `"http://localhost:8080"` |
| `global_variables` | dict | 否 | 全局变量，供 `${global_variables.xxx}` 引用 |
| `headers_config` | dict | 是 | 全局请求头配置 |
| `auth_setup` | dict | 是 | 认证统一配置 |
| `testcases` | list | 是 | 测试用例列表，非空 |

---

## `global_variables`

供全局 `${global_variables.xxx}` 引用的键值对，存放会被大量公用的变量，减少重复内容。

```yaml
global_variables:
  default_page_size: 10
  default_id: "000000"
```

- key 为合法标识符（字母/数字/下划线）
- value 可以是字符串、数字、布尔值

---

## `headers_config`

### `headers_config.public_headers`

所有接口默认携带的公共请求头（无论公开还是认证接口）。直接从主文档「公开接口」请求头表格照抄。

```yaml
headers_config:
  public_headers:
    - name: "Content-Type"
      value: "application/json"
```

**条目字段**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `name` | string | 是 | 请求头名称 |
| `value` | string | 是 | 请求头值，支持 `${}` 变量引用 |

### `headers_config.auth_headers`

仅当用例 `auth.required: true` 时注入的认证请求头。直接从主文档「认证接口」请求头表格照抄。Token 类字段的值用 `${auth.xxx}` 引用。

```yaml
  auth_headers:
    - name: "Authorization"
      value: "${auth.token_prefix} ${auth.token}"
    - name: "xx"
      value: "${auth.params.admin.xx}"
```

> **禁止**在 `request.headers` 中手写此处已声明的头。

---

## `auth_setup`

### `auth_setup.type`

认证类型，枚举值：

| 值 | 说明 |
|----|------|
| `bearer_token` | Bearer Token 认证（JWT/Token），最常见 |
| `basic` | HTTP Basic Auth |
| `apikey` | API Key Header |
| `oauth2` | OAuth2 认证 |
| `none` | 无认证 |

### `auth_setup.login_endpoint`

登录接口路径，**纯路径**（不含 HTTP 方法前缀）。

- 正确：`"/auth/login"`
- 错误：`"POST /auth/login"`

### `auth_setup.token_prefix`

Token 前缀，无则填空字符串 `""`。示例：`"Bearer "`（注意尾部空格）。

### `auth_setup.params`

其他认证参数，格式灵活，与 `auth_headers` 中的引用对齐。

```yaml
params:
  admin:
    param_key: "<value>"
```
- 结构可自定义，不强制 `params.admin.xx`
- direct `params.xx` 也是合法的（如 `params.param_key`）
- 引用时写全路径：`${auth.params.admin.param_key}` 或 `${auth.params.param_key}`

### `auth_setup.accounts`

登录账号池，供用例 `auth.account` 选择。

```yaml
accounts:
  admin:
    username: "admin"
    password: "admin123"
  readonly:
    username: "test"
    password: "666666"
```

每个账号至少包含登录所需字段（通常为 `username` + `password`）。可扩展更多字段`供 `auth_headers` 引用。

### `auth_setup.extracts`

从登录响应中提取的变量，供 `auth_headers` 通过 `${auth.xxx}` 引用。字段名必须使用 **JSON key**（从登录响应体实体文档的「注解转义说明」表或「字段定义」表的「JSON 键名」列确认）。

```yaml
extracts:
  token: "$.data.<json_key>"       # 用响应体实体的 JSON 键名，不是 Java 字段名
```

**跳过规则**：`extracts` 中定义的变量，引用时写 `${auth.变量名}`，**跳过 `extracts` 层级**。

- 正确：`${auth.token}`（跳过 extracts）
- 错误：`${auth.extracts.token}`
- 正确：其他字段严格按完整路径，如 `${auth.accounts.admin.username}`

---

## `testcases` 条目

### 顶层字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `id` | string | 是 | 唯一标识，格式 `TC_{MODULE}_{序号}`，如 `TC_AUTH_001` |
| `title` | string | 是 | 格式 `{METHOD} {路径}_{条件}_{预期}` |
| `priority` | enum | 是 | `P0` / `P1` / `P2` |
| `tags` | list[enum] | 是 | 见下方标签枚举 |
| `method` | enum | 是 | `GET` / `POST` / `PUT` / `DELETE` / `PATCH` |
| `path` | string | 是 | 接口路径（纯路径，不含 base_url 和查询参数） |
| `description` | string | 是 | 简要说明测试目的 |
| `auth` | dict | 是 | 权限声明 |
| `request` | dict | 否 | 请求定义（GET 可省略 body） |
| `extracts` | dict | 否 | 从响应提取变量到上下文 |
| `expected` | dict | 是 | 预期断言 |
| `depends_on` | list | 否 | 依赖的前置用例 id 列表 |

### 标签枚举

| 标签 | 说明 |
|------|------|
| `正常` | 正向功能验证 |
| `异常` | 反向/错误处理 |
| `回归` | 回归测试（建议所有用例都带） |
| `冒烟` | 冒烟测试（核心流程快速验证） |
| `兼容性` | 版本/环境兼容性 |
| `用户体验` | UI/交互体验 |

### `auth`

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `required` | bool | 是 | `true`=注入 `auth_headers`，`false`=仅 `public_headers` |
| `account` | string | 否 | 指定使用的账号，必须存在于 `auth_setup.accounts` 中。默认 `"admin"` |

### `request`

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `headers` | list | 否 | 接口特有头（不在 `headers_config` 中的），同名会覆盖 |
| `path_params` | dict | 否 | 路径参数，如 `{id: "${userId}"}` |
| `query` | dict | 否 | 查询参数（GET 请求） |
| `body` | dict | 否 | 请求体，字段名必须是 **JSON 键名**（从实体文档获取） |

### `expected`

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `status_code` | int | 是 | HTTP 状态码，如 `200`、`401`、`500` |
| `response_type` | enum | 是 | `json` / `html` |
| `business_code` | int | json 时必填 | 业务状态码（从 `R.code` 取值），如 `200` |
| `business_message` | string | 否 | 业务消息（从 `R.msg` 取值） |
| `data_exists` | list | json 时必填 | 断言 data 中存在的 JSON 键名（仅 1-2 个关键字段） |
| `data_equals` | dict | 否 | 具体的字段值断言（尽量少用） |
| `body_contains` | list | html 时必填 | 断言响应体中包含的文本 |

### `depends_on`

依赖的前置用例 id 列表，用于声明用例执行顺序。

```yaml
depends_on:
  - "TC_USER_001"
```
