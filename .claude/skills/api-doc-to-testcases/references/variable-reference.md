# 变量引用规范

YAML 中所有变量引用的格式、作用域和校验规则。

---

## 引用格式一览

| 引用格式 | 作用域 | 说明 | 示例 |
|---------|--------|------|------|
| `${auth.token}` | auth_setup.extracts | 登录提取的变量，跳过 extracts 层级 | `${auth.token}` |
| `${auth.token_prefix}` | auth_setup 顶层 | auth_setup 的直接字段 | `${auth.token_prefix}` |
| `${auth.params.xxx}` | auth_setup.params | 认证参数 | `${auth.params.admin.tenant_id}` |
| `${auth.accounts.xxx}` | auth_setup.accounts | 账号信息 | `${auth.accounts.admin.username}` |
| `${global_variables.xxx}` | global_variables | 全局变量 | `${global_variables.default_page_size}` |
| `${TC_XXX.extracts.xxx}` | 前置用例 extracts | 跨用例变量传递 | `${TC_USER_001.extracts.user_id}` |
| `$.xx.xx` | 当前响应体 | JSONPath 提取 | `$.data.id` |

---

## extracts 跳过规则（核心）

`auth_setup.extracts` 中定义的变量，引用时**跳过 `extracts` 层级**。

```yaml
auth_setup:
  extracts:
    token: "$.data.access_token"
    refresh_token: "$.data.refresh_token"
```

- 正确：`${auth.token}`、`${auth.refresh_token}`
- 错误：`${auth.extracts.token}`

**为什么**：extracts 是"容器"，引用的目标是容器中的变量，不引用容器本身。这是唯一可以跳过层级的地方。

**其他所有字段必须严格按照层级路径引用**：

- `${auth.accounts.admin.username}` — 不能跳过 accounts
- `${auth.params.admin.client_id}` — 不能跳过 params
- `${global_variables.default_page_size}` — 不能跳过 global_variables

---

## 请求头中的变量引用

`headers_config.auth_headers` 的 `value` 支持 `${auth.xxx}` 引用，运行时替换：

```yaml
auth_headers:
  - name: "Authorization"
    value: "${auth.token_prefix} ${auth.token}"    # 运行时 → "Bearer eyJhbG..."
  - name: "clientid"
    value: "${auth.params.admin.client_id}"         # 运行时 → "e5cd7e4891bf95d1d19206ce24a7b32e"
```

多个变量可拼接在一个 value 中。

---

## 用例间变量引用

用例通过 `extracts` 将响应字段存入上下文，后续用例通过 `${TC_XXX.extracts.xxx}` 引用：

```yaml
# 用例 A — 提取
- id: TC_USER_001
  extracts:
    created_user_id: "$.data.userId"

# 用例 B — 引用
- id: TC_USER_002
  path: "/system/user/${TC_USER_001.extracts.created_user_id}"
  depends_on:
    - "TC_USER_001"
```

`depends_on` 声明依赖关系，确保执行顺序。

---

## JSONPath 规范（`$.xx.xx`）

用于 `extracts` 和 `data_equals` 中定位响应字段。

| JSONPath | 含义 |
|----------|------|
| `$.data.id` | 响应体 data.id |
| `$.data.access_token` | 响应体 data.access_token（JSON key） |
| `$.data.list[0].id` | 响应体 data.list 数组第一个元素的 id |

- JSONPath 必须以 `$` 开头
- 路径段使用 **JSON key**（不是 Java 字段名）
- 数组索引用 `[n]`

---

## 校验规则

生成 YAML 后验证所有变量引用：

1. `${auth.xxx}` — `xxx` 必须在 `auth_setup` 中可解析（extracts 跳过层级后）
2. `${auth.params.xxx.yyy}` — 路径必须在 `auth_setup.params` 中存在
3. `${auth.accounts.xxx.yyy}` — 账号名和字段必须在 `auth_setup.accounts` 中存在
4. `${global_variables.xxx}` — 变量必须在 `global_variables` 中定义
5. `${TC_XXX.extracts.xxx}` — 前置用例 ID 必须存在且该用例定义了对应 extracts
6. `$.xx.xx` — JSONPath 格式正确（以 `$` 开头）
