# 生成约束与校验规则

Agent 生成 YAML 时必须遵守的约束和自检规则。

---

## 文件级约束

- 每个模块文档 → **1 个 YAML 文件**（不是每个接口 1 个文件）
- 文件名与模块文档一致，仅扩展名改为 `.yaml`
  - `01-认证模块.md` → `01-认证模块.yaml`
  - `03-系统管理-part1-用户管理.md` → `03-系统管理-part1-用户管理.yaml`
- `module` 字段取文件名中的英文标识（`auth`、`system_user`、`system_role` 等）
- `module_name` 取文件名中的中文名（`认证模块`、`用户管理` 等）

---

## 用例 ID 生成

```
TC_{MODULE}_{NNN}
```

- MODULE 取文档文件名的大写英文缩写，如：
  - `01-认证模块.md` → `AUTH`
  - `03-系统管理-part1-用户管理.md` → `USER`
  - `03-系统管理-part2-角色管理.md` → `ROLE`
  - `06-工作流管理-part1-SPEL与流程分类.md` → `WF_SPEL` 或 `WF_CATEGORY`
- NNN：三位数字，从 001 递增
- 每个接口生成正反两条用例，ID 连续

---

## method 校验

`method` 必须为以下值之一，不能乱填：

`GET` | `POST` | `PUT` | `DELETE` | `PATCH`

- 从模块文档的「请求方式」字段直接提取
- 提取后必须校验是否在合法值集合中
- 如果文档中写的是小写（如 `get`），转大写（`GET`）

---

## auth 校验

- `auth.required`：与文档「认证方式」一致（"需要认证" → `true`，"无需认证" → `false`）
- `auth.account`：引用的账号名必须在 `auth_setup.accounts` 中存在
- 认证接口（`required: true`）不在 `request.headers` 中手写已在 `headers_config.auth_headers` 中声明的头
- 测试"未认证访问"场景：设 `auth.required: false`，不手写 Authorization

---

## 请求体字段校验

- `request.body` 的 key 必须是 **JSON 键名**（从实体文档确认，不是 Java 字段名）
- 字段类型与实体文档一致（字符串用引号，数字不加引号，数组用 `[]`）
- 正向用例：必填字段都给值，可选字段选填
- 反向用例：故意缺失 1 个必填字段或给 1 个非法值

---

## 断言字段校验

- `data_exists` 的字段名必须是 **JSON 键名**
- 正向用例 `data_exists` 仅 1-2 个关键字段，不过度断言
- `data_equals` 尽量不填
- `response_type: json` → 必填 `business_code` + `data_exists`
- `response_type: html` → 必填 `body_contains`，不填 `business_code`
- 分页响应 → `data_exists` 断言 `rows`，可选加 `total`

---

## 变量引用校验

生成后自检所有变量引用：

1. `${auth.xxx}`（跳过 extracts 层级）— xxx 在 `auth_setup.extracts` 或 `auth_setup` 顶层有定义
2. `${auth.params.xxx.yyy}` — 路径存在
3. `${auth.accounts.admin.xxx}` — 账号和字段存在
4. `${global_variables.xxx}` — 变量已定义
5. `${TC_XXX.extracts.xxx}` — 前置用例 ID 存在且定义了对应 extracts
6. `$.xx.xx` — JSONPath 以 `$` 开头，路径段正确

---

## 数据安全约束

- `auth_setup.accounts` 中的账号：**不生成增/删/改用例**，仅可查询
- `auth_setup.params` 中的参数对应资源：**不生成删/改用例**
- 需要增删改测试 → 新建数据来操作，认证始终用提供的账号
- 新建数据在测试后不要求清理（由测试环境负责）

---

## 禁止生成的用例

以下情况**跳过**，不生成用例：
- 接口为文件导出/下载，且 `response_type: void`（如 `/system/user/export`）— 跳过，不生成用例
- 接口为静态资源或健康检查（如 `/error`、`/*.html`）— 跳过
- 接口仅返回页面重定向 — 跳过

---

## YAML 格式约束

- 缩进使用 2 空格（不使用 Tab）
- 字符串值使用双引号（除非值本身不含特殊字符）
- 列表项以 `- ` 开头
- 多行字符串不使用 `|` 或 `>`（保持简单）
- 布尔值写 `true` / `false`（小写，不带引号）
- 数字不加引号

---

## 业务规则约束

- 若模块文档有「业务规则」表，**反向用例必须从中选取至少 1 条规则**作为测试条件
- 不得在有业务规则的情况下仅依赖「错误响应」表生成反向用例
- 正向用例的请求参数必须通过所有业务规则的校验

---

## 断言参照约束（diff 模式）

- **文档断言优先**：diff 文档中已有的断言值不得被 Agent 自行修改或覆盖
- 若文档断言与默认推断规则冲突，以文档断言为准
- 若文档未提供断言信息，回退到默认推断规则
- 生成后自检：对比文档断言与 YAML expected 块，确保文档声明的字段均已覆盖

---

## 登录接口用例（diff 模式）

- diff 模式下，必须额外生成一份含登录接口用例的 YAML 文件
- 登录用例从 `${BASELINE_YAML_DIR}` 目录的已有 YAML 中提取，不重新生成
- 筛选条件：`path` 等于 `auth_setup.login_endpoint` 且 `method: POST` 的用例
- 提取正向和反向各 1 条，写入 `${OUTPUT_DIR}` 下的新 YAML 文件
- 新文件使用 Step 1 构建的 `headers_config`、`auth_setup`、`global_variables`
- 此文件为 yaml-to-pytest 脚本的 `_do_login()` 提供正确的登录请求体模板
- 若 `${OUTPUT_DIR}` 已有文件包含登录用例则跳过此步骤
