# 性能场景 YAML 字段规范

每个模块性能场景文件的完整字段定义、类型、约束。

> 本文件是 `api-doc-to-perf` 生成物与 `yaml-to-jmx` 生成器的契约。所有字段名、枚举值必须严格一致。

---

## 顶层字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `module` | string | 是 | 模块标识，纯字母数字下划线，如 `auth`、`system_user` |
| `module_name` | string | 是 | 模块中文名，如 `"认证模块"` |
| `base_url` | string | 是 | 服务端 Base URL，含协议与端口，如 `"http://localhost:8080"` |
| `headers_config` | dict | 是 | 全局请求头配置 |
| `auth_setup` | dict | 否 | 认证统一配置（无需认证时可省略） |
| `scenarios` | list | 是 | 性能场景列表，非空 |

---

## `headers_config`

### `headers_config.public_headers`

所有请求默认携带的公共请求头。

```yaml
headers_config:
  public_headers:
    - name: "Content-Type"
      value: "application/json"
```

### `headers_config.auth_headers`

仅当场景 `auth.required: true` 时注入的认证请求头。Token 用 **JMeter 变量** `${token}` 引用（生成器会自动生成"登录 + 提取 token"逻辑）。

```yaml
  auth_headers:
    - name: "Authorization"
      value: "Bearer ${token}"
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `name` | string | 是 | 请求头名称 |
| `value` | string | 是 | 请求头值，支持 `${token}` 及 JMeter `${__P(...)}` 属性引用 |

---

## `auth_setup`

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `login_endpoint` | string | 是 | 登录接口纯路径，如 `"/auth/login"` |
| `login_method` | enum | 否 | 登录 HTTP 方法，默认 `POST` |
| `login_headers` | list | 否 | 登录请求特有头（合并到 public_headers 之上） |
| `login_body` | dict | 是 | 登录请求体（JSON 键名），账号密码可直接写死或占位 |
| `token_jsonpath` | string | 是 | 从登录响应提取 token 的 JSONPath，如 `"$.data.token"` |
| `token_default` | string | 否 | 提取失败时的默认值，默认 `"NOT_FOUND"` |

```yaml
auth_setup:
  login_endpoint: "/auth/login"
  login_method: POST
  login_body:
    clientId: "e5cd7e4891bf95d1d19206ce24a7b32e"
    grantType: "password"
    username: "admin"
    password: "admin123"
    tenantId: "000000"
  token_jsonpath: "$.data.token"
```

---

## `scenarios` 条目

### 顶层字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `id` | string | 是 | 唯一标识，格式 `PERF_{MODULE}_{序号}`，如 `PERF_AUTH_001` |
| `title` | string | 是 | 格式 `{METHOD} {路径}_{并发}并发_{时长}s` |
| `priority` | enum | 否 | `P0` / `P1` / `P2`，默认 `P1` |
| `method` | enum | 是 | `GET` / `POST` / `PUT` / `DELETE` / `PATCH` |
| `path` | string | 是 | 接口纯路径（不含 base_url 与查询参数） |
| `description` | string | 否 | 压测目的简述 |
| `auth` | dict | 否 | 权限声明，默认 `{required: false}` |
| `request` | dict | 否 | 请求定义（GET 可省略 body） |
| `load` | dict | 是 | 负载配置 |
| `thresholds` | dict | 是 | 性能阈值（达标判定） |

### `auth`

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `required` | bool | 是 | `true` = 每个并发用户先登录一次再压主接口；`false` = 仅 public_headers |

### `request`

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `headers` | list | 否 | 场景特有头（同名覆盖全局），支持 `${token}` |
| `path_params` | dict | 否 | 路径参数，如 `{id: "1"}` |
| `query` | dict | 否 | 查询参数（GET 请求） |
| `body` | dict | 否 | 请求体，字段名必须是 JSON 键名 |

### `load`

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `users` | int | 是 | 并发用户数（→ JMeter `ThreadGroup.num_threads`） |
| `ramp_up` | int | 否 | 爬坡时间秒（→ `ThreadGroup.ramp_time`），默认 `users` 的 1/10（最少 1） |
| `duration` | int | 是 | 压测持续时间秒（→ 通过 `ThreadGroup.duration` + `scheduler=true` 控制） |
| `loops` | int | 否 | 循环次数，默认 `-1`（无限，由 duration 终止） |

### `thresholds`

| 字段 | 类型 | 必填 | 说明 | 单位 |
|------|------|:---:|------|------|
| `avg` | number | 否 | 平均响应时间上限 | ms |
| `p50` | number | 否 | 中位数响应时间上限 | ms |
| `p90` | number | 否 | P90 响应时间上限 | ms |
| `p95` | number | 否 | P95 响应时间上限 | ms |
| `p99` | number | 否 | P99 响应时间上限 | ms |
| `error_rate` | number | 否 | 错误率上限（0~1，如 `0.01` = 1%） | 比例 |
| `min_rps` | number | 否 | 最低吞吐（每秒请求数）下限 | req/s |

> `thresholds` 至少含一项。任一指标超限即该场景判定「不达标」。

---

## 完整示例

> 以下示例中的 `clientId`/`grantType`/`tenantId` 等字段为**示例值**，必须按被测项目登录接口实际请求体替换。

```yaml
module: auth
module_name: "认证模块"
base_url: "http://localhost:8080"

headers_config:
  public_headers:
    - name: "Content-Type"
      value: "application/json"
  auth_headers:
    - name: "Authorization"
      value: "Bearer ${token}"

auth_setup:
  login_endpoint: "/auth/login"
  login_method: POST
  login_body:
    clientId: "e5cd7e4891bf95d1d19206ce24a7b32e"
    grantType: "password"
    username: "admin"
    password: "admin123"
    tenantId: "000000"
  token_jsonpath: "$.data.token"

scenarios:
  - id: PERF_AUTH_001
    title: "POST /auth/login_100并发_60s"
    priority: P0
    method: POST
    path: "/auth/login"
    description: "验证登录接口在 100 并发下的响应时间与吞吐"
    auth:
      required: false
    request:
      body:
        clientId: "e5cd7e4891bf95d1d19206ce24a7b32e"
        grantType: "password"
        username: "admin"
        password: "admin123"
        tenantId: "000000"
    load:
      users: 100
      ramp_up: 10
      duration: 60
    thresholds:
      p95: 800
      p99: 1500
      avg: 500
      error_rate: 0.01
      min_rps: 50

  - id: PERF_USER_001
    title: "GET /system/user/list_50并发_60s"
    priority: P1
    method: GET
    path: "/system/user/list"
    description: "验证用户列表查询在 50 并发下的性能"
    auth:
      required: true
    request:
      query:
        pageNum: 1
        pageSize: 10
    load:
      users: 50
      ramp_up: 5
      duration: 60
    thresholds:
      p95: 1200
      error_rate: 0.02
      min_rps: 30
```

---

## 变量引用

| 引用格式 | 说明 |
|---------|------|
| `${token}` | JMeter 线程级变量，由登录 JSON Extractor 注入，供 `auth_headers` 使用 |
| `${__P(name, default)}` | JMeter 属性引用，可在命令行 `-Jname=value` 覆盖 |
