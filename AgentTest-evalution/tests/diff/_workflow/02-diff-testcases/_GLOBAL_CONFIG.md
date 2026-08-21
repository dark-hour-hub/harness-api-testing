# 全局配置与生成规则（api-doc-to-testcases 共享）

> 本文件由主会话生成，供各模块 Agent 直接读取并遵守。请勿修改其中 `headers_config` / `auth_setup` / `global_variables`。

base_url: "http://localhost:8080"

## 一、headers_config（所有模块共用，直接照抄）

```yaml
headers_config:
  public_headers:
    - name: "Content-Type"
      value: "application/json"
  auth_headers:
    - name: "Authorization"
      value: "${auth.token_prefix} ${auth.token}"
    - name: "clientid"
      value: "${auth.params.admin.clientId}"
```

## 二、auth_setup（所有模块共用，直接照抄）

```yaml
auth_setup:
  type: bearer_token
  login_endpoint: "/auth/login"
  token_prefix: "Bearer "
  params:
    admin:
      clientId: "e5cd7e4891bf95d1d19206ce24a7b32e"
      grantType: "password"
      tenantId: "000000"
    visitor:
      clientId: "e5cd7e4891bf95d1d19206ce24a7b32e"
      grantType: "password"
      tenantId: "000000"
  accounts:
    admin:
      username: "admin"
      password: "admin123"
    visitor:
      username: "test"
      password: "666666"
  extracts:
    token: "$.data.access_token"
```

## 三、global_variables（所有模块共用，直接照抄）

```yaml
global_variables:
  default_page_size: 10
```

## 四、字段名强制规则（违反即校验失败）

- `request.body` 的 key 必须是 **JSON 键名**（从实体文档「注解转义说明」/「字段定义」表的「JSON 键名」列确认），不是 Java 字段名。
- `expected.data_exists` 的字段名也必须是 **JSON 键名**。
- 注意转义：例如 `access_token`（非 `accessToken`）、`client_id`（非 `clientId`）、`dept_id` 等，以实体文档为准。
- 登录请求体 JSON 键名：`username`、`password`、`clientId`、`grantType`、`tenantId`（与 Java 字段名一致）。

## 五、用例生成规则

1. 每个接口生成 **2 条用例**：1 条正向（P0，tags `[正常, 回归]`，核心接口加 `[冒烟]`）+ 1 条反向（P1，tags `[异常, 回归]`）。
2. **跳过**不生成用例的接口：文件导出/下载（`response_type: void`，如 `*/export`、`*/download`、`*/batchGenCode`、`/resource/oss/download` 等）；静态资源/重定向。
3. 正向用例：`auth.required` 与文档「认证方式」一致；填合法必填字段；断言 `status_code: 200`、`business_code: 200`、仅 1-2 个关键 `data_exists`（分页接口断言 `rows`）；不填 `data_equals`。
4. 反向用例：优先从文档「业务规则」表选 1 条典型违规（覆盖不到时回退「错误响应」表，选最有代表性的 1 条，如必填缺失/用户名已存在）；断言 `status_code: 200`、`business_code: 500`、不填 `data_exists`。
5. 数据安全：**禁止**对 `auth_setup.accounts` 中的账号（admin / test）生成增/删/改用例；**禁止**对 `auth_setup.params` 中的 clientId/grantType/tenantId 资源生成删/改用例。需要增删改时，先 POST 新建数据，再对新数据操作，认证始终用 admin。
6. 变量引用：
   - `${auth.token}`（跳过 extracts 层级）
   - `${auth.token_prefix}`、`${auth.params.admin.clientId}`、`${auth.accounts.admin.username}`、`${global_variables.default_page_size}`
   - 响应 JSONPath 以 `$` 开头，如 `$.data.id`
7. `auth` 段：`required: true`/`false` 与文档一致；`account` 必须在 accounts 中存在（默认 `admin`）。
8. **认证头禁止手写在 `request.headers`**：`Authorization` 与 `clientid` 已通过 `auth_headers` 在 `required:true` 时自动注入。
9. 用例间依赖：若需先创建数据再操作，用 `extracts` + `depends_on` + `${TC_XXX.extracts.xxx}`。
10. ID 格式：`TC_{MODULE}_{三位数字}`，从 001 递增，正反连续。标题：`{METHOD} {路径}_{条件}_{预期}`。
11. 401 共性错误：仅在认证模块对某个需认证接口生成 1 条（未带 token → 401）；403/权限不足：仅选 1 个代表性接口生成 1 条，不重复。

## 六、YAML 格式约束

- 缩进 2 空格；字符串用双引号；布尔 `true`/`false` 小写无引号；数字不加引号；列表项 `- ` 开头。
- 顶层字段：`module`、`module_name`、`base_url`、`headers_config`、`auth_setup`、`testcases`（非空 list）、可选 `global_variables`。
- `module`：纯字母数字下划线（取自文件名英文标识，如 `auth`、`system_part1`、`monitor`、`resource`、`tool`、`workflow_part1`）。
- `module_name`：中文名（如 `认证模块`、`系统管理模块-part1`）。
- 每个 `expected`：`status_code`(int) + `response_type`(json/html) 必填；json 时 `business_code`(int) + `data_exists`(list) 必填；html 时 `body_contains`(list) 必填。

## 七、实体文档读取

- 实体文档目录：`entities/`（相对模块文档目录）。
- 只读本模块用到的实体（请求体 DTO / 响应体 VO）。不要预读全量。
- 请求体字段与 `data_exists` 字段名均取自其实体文档的 JSON 键名。
