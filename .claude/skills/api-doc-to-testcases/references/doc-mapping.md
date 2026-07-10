# 文档→YAML 字段映射

如何从各类文档中提取信息并映射到 YAML 字段。

---

## 主文档 → 全局配置

| YAML 字段 | 主文档来源 | 提取方式 |
|-----------|-----------|---------|
| `base_url` | 项目信息表 → Base URL | 直接取值，如 `http://localhost:8080` |
| `module_name` | 模块概览表 → 模块名 | 直接取值 |
| `headers_config.public_headers` | 全局默认请求头 → 公开接口表格 | 逐行照抄 name + value |
| `headers_config.auth_headers` | 全局默认请求头 → 认证接口表格 | 逐行照抄，Token 值用 `${auth.token_prefix} ${auth.token}` |
| `global_variables` | 项目信息 + 响应包装 | 提取默认分页大小、默认 tenantId 等常量 |

---

## auth-analysis.md → auth_setup

| YAML 字段 | auth-analysis.md 来源 |
|-----------|----------------------|
| `type` | 认证方式表 → 认证类型 |
| `login_endpoint` | 登录接口表 → 接口路径 |
| `token_prefix` | 认证方式表 → Token 名前缀 |
| `extracts` | 登录响应字段表 → JSON key 列 |
| `params` | 测试建议区的 clientId、tenantId |
| `accounts` | 测试建议区 → 登录示例的 username、password |

---

## _manifest.yaml → 路由信息

manifest 的 `modules[].routes[]` 提供每个接口的基本元数据：

| manifest 字段 | YAML 字段 | 说明 |
|--------------|-----------|------|
| `method` | `method` | 直接映射，需校验合法性 |
| `path` | `path` | 直接映射 |
| `summary` | `description` | 接口摘要作为描述基础 |
| `auth` | `auth.required` | `true` → `required: true`，`false` → `required: false` |
| `request_body` | 请求体实体名 | 去 `entities/` 读取对应实体文档 |
| `response_type` | 响应结构 | `R<XxxVo>` → type 为 XxxVo，去 entities 读字段 |
| `response_structure` | 响应类型判断 | `page` → 分页响应，`single` → 单对象，`list` → 列表 |

---

## 模块文档 → 用例

每个接口以 `### N 接口名称` 开头。

| YAML 字段 | 模块文档来源 |
|-----------|------------|
| `method` | 属性表 → 「请求方式」 |
| `path` | 属性表 → 「接口路径」 |
| `description` | 属性表 → 「接口说明」 |
| `auth.required` | 属性表 → 「认证方式」（"需要认证" → true，"无需认证" → false） |
| `request.query` | 「查询参数」表 |
| `request.path_params` | 「路径参数」表 |
| `request.body` | 「请求体」引用 → 去 entities/ 读取实体文档获取 JSON 字段 |
| `expected.status_code` | 「成功响应」→ HTTP 状态码 |
| `expected.business_code` | 「成功响应」→ R.code 值 |
| 反向用例条件 | 「错误响应」表 + 「业务规则」表 |
| `tags` 是否加 `[冒烟]` | 属性表 → 「标签」（含"冒烟测试"则加） |

---

## 实体文档 → 请求体 / 响应断言字段

实体文档位于 `entities/{ClassName}.md`。

### 读取 JSON 键名

从实体文档的「注解转义说明」表确定 JSON 键名：

- 如果有转义：取「JSON 键名」列
- 如果无转义（"Java 字段名与 JSON 键名一致"）：使用「字段定义」表的「JSON 键名」列（即 Java 字段名本身）

**关键**：`request.body` 和 `data_exists` 的字段名**必须是 JSON 键名**，不是 Java 字段名。

### 读取校验规则

从「字段定义」表的「约束/校验规则」列获取：
- `@NotBlank` → 必填，缺失时会报错（反向用例候选）
- `@NotNull` → 必填
- `@Email` → 格式校验
- `@Length(min=X, max=Y)` → 长度约束
- 无注解 → 可选字段

### 构建请求体示例

正向用例的 `request.body` 从实体文档的「JSON 示例」段获取参考值。

---

## 响应结构判断

| response_structure | 断言要点 |
|-------------------|---------|
| `single` (R\<T\>) | `data_exists` 断言 T 的字段 |
| `page` (TableDataInfo\<T\>) | `data_exists` 断言 `rows`，可选断言 `total` |
| `list` (R\<List\<T\>\>) | `data_exists` 断言数组字段 |
| `null` (R\<Void\>) | 不填 `data_exists`（data 为 null） |
| `void` (无响应体/文件下载) | `response_type: html` 或不填 |
