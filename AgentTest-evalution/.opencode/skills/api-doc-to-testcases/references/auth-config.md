# 认证配置构建规则

如何从 `auth-analysis.md`、主文档和 `_manifest.yaml` 构建 `auth_setup` 和 `headers_config`。

---

## 数据来源映射

| auth_setup 字段 | 数据来源 | 提取方式                                               |
|----------------|---------|----------------------------------------------------|
| `type` | auth-analysis.md → 认证方式表 | Sa-Token JWT → `bearer_token`，Session → `basic`    |
| `login_endpoint` | auth-analysis.md → 登录接口表 | 取「接口路径」列，如 `/auth/login`（纯路径）                      |
| `token_prefix` | auth-analysis.md → 认证方式表 | Token 名为 `Authorization`，前缀 `Bearer` → `"Bearer "` |
| `params` | 登录接口的请求体实体文档 | 从实体文档「字段定义」表的「JSON 键名」列提取参数名，值从 `_manifest.yaml` 的 `test_accounts` 获取 |
| `accounts` | `_manifest.yaml` → `test_accounts` | 复制 username、password，可补充其他参数                       |
| `extracts` | auth-analysis.md → 登录响应字段表 | 用 **JSON key** 列的值，不是 Java 字段名                     |

---

## type 判定规则

| auth-analysis.md 认证类型 | YAML type |
|--------------------------|-----------|
| Sa-Token + JWT | `bearer_token` |
| Sa-Token（非 JWT） | `bearer_token` |
| Spring Security Session | `basic` |
| OAuth2 / 第三方 | `oauth2` |
| API Key | `apikey` |
| 无认证 | `none` |

---

## extracts 字段名规则

`auth_setup.extracts` 的 key 可以自由命名，但 value（JSONPath）中的最后一段必须使用 **JSON key**（即 API 实际返回的字段名）。

从 auth-analysis.md 的「登录响应字段」表读取：

| Java 字段名     | JSON key | 说明 |
|--------------|---------|------|
| token        | `token` | ← extracts 中用 `token` |

生成的 extracts：
```yaml
extracts:
  token: "$.data.token"        # JSON key
```

---

## headers_config 照抄规则

### public_headers

直接从主文档「公开接口（无需认证）」的请求头表格逐行照抄：

```markdown
| 头名称 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|:---:|------|--------|
| Content-Type | String | 是 | ... | `application/json` |
```

→

```yaml
public_headers:
  - name: "Content-Type"
    value: "application/json"
```

### auth_headers

直接从主文档「认证接口（需要认证）」的请求头表格逐行照抄。Token 头的 `value` 用 `${auth.token_prefix} ${auth.token}`，其他头的值用 `${auth.params.xxx}` 引用：

```markdown
| Authorization | String | 是 | `Bearer {token}` | `Bearer eyJhbG...` |
| other | String | 是 | 客户端 ID | `sdgsadgsdfghsgdsg` |
```

→

```yaml
auth_headers:
  - name: "Authorization"
    value: "${auth.token_prefix} ${auth.token}"
  - name: "other"
    value: "${auth.params.admin.other}"
```

---

## params 字段名规则

`auth_setup.params` 的 key 必须使用**登录请求体实体文档**中「字段定义」表的「JSON 键名」列的值。

> 注意：登录请求体实体和登录响应体实体是**两个不同的实体文档**。请求体实体的 JSON 键名可能与响应体实体的 JSON 键名不同（例如请求体无转义而响应体有 `@JsonProperty` 转义）。`params` 用于构造登录请求体，因此必须以**请求体**实体文档的 JSON 键名为准。

从登录接口的请求体实体文档读取：

| 实体文档字段 | JSON 键名 | 说明 |
|------------|----------|------|
| Java 字段 | 实体文档「JSON 键名」列 | ← params 中用 JSON 键名 |

若实体文档标注"Java 字段名与 JSON 键名一致"，则 JSON 键名就是 Java 字段名本身。

生成的 params：
```yaml
params:
  admin:
    <json_key_1>: "<value>"
    <json_key_2>: "<value>"
```

---

## params 结构设计

`auth_setup.params` 的结构与 `auth_headers` 中的引用对齐即可，格式不固定。

场景1 — 单账号，参数少：
```yaml
params:
  id: "asdfdasfasfasf"
```
引用：`${auth.params.id}`

场景2 — 多账号，参数有差异：
```yaml
params:
  admin:
    id: "adfasfsdgfsdg"
  visitor:
    id: "dasgaaggagg"
```
引用：`${auth.params.admin.id}`

---

## accounts 规则

从 `_manifest.yaml` 的 `test_accounts` 提取：

```yaml
# manifest 中:
test_accounts:
  - role: admin
    username: admin
    password: admin123
    id: sfasdfasdfasfasf
```

→

```yaml
accounts:
  admin:
    username: "admin"
    password: "admin123"
```

最小字段集：`username` + `password`。可补充更多字段供 `auth_headers` 引用。

---

## 校验清单

生成 `auth_setup` 和 `headers_config` 后，确认以下一致性：

1. `auth_headers` 中每个 `${auth.xxx}` 引用都能在 `auth_setup` 中解析
2. `extracts` 的 JSONPath 中最后一段是 JSON key（不是 Java 字段名）
3. `login_endpoint` 是纯路径（以 `/` 开头，不含 HTTP 方法）
4. `accounts` 中的账号名与用例中的 `auth.account` 引用一致
5. `token_prefix` 尾部空格正确（如 `"Bearer "` 有空格，`"Token "` 有空格，`""` 无空格）
6. `params` 中的 key 名与登录请求体实体文档的「JSON 键名」列一致（不是响应体实体的 JSON 键名）
