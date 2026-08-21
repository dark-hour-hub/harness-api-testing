# agent-evaluation-platform（智能体评测平台） API 接口文档

## 项目信息

| 属性 | 值 |
|------|-----|
| **系统名称** | agent-evaluation-platform（智能体评测平台） |
| **Base URL** | `http://localhost:8080`（dev 环境；所有业务接口位于 `/api` 前缀下） |
| **框架** | Spring Boot 3.5.16 / Java 17 / 六边形(DDD)架构 / 无安全框架 |
| **数据库** | MySQL 8.0 + MyBatis-Plus 3.5.17（`agent_evaluation` 库，PaginationInnerInterceptor 分页） |
| **缓存** | 无 |
| **API 文档** | SpringDoc OpenAPI 2.8.17（`/swagger-ui.html`、`/v3/api-docs`） |
| **认证方式** | 无认证（`none`），所有接口公开访问 |
| **接口加密** | 无 |
| **文档版本** | v1.0 |
| **生成日期** | 2026-08-19 |

---

## 测试账号

| 角色 | 用户名 | 密码 | 权限范围 |
|------|--------|------|----------|
| 无 | - | - | 系统无认证机制、无账号体系，所有接口可直接调用，无登录/token 前置依赖 |

---

## 全局默认请求头

### 公开接口（无需认证，本系统全部接口均为公开接口）

| 头名称 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|:---:|------|--------|
| Content-Type | String | ✅ | 请求体格式，JSON 接口使用 `application/json`；`POST /api/test-cases/import/excel` 使用 `multipart/form-data` | `application/json` |
| X-Trace-Id | String | ❌ | 链路追踪 ID，可选；TraceIdFilter 原样透传并回写响应头，缺失时服务端自动生成 32 位十六进制 UUID | `test-case-001` |

> 适用于：全部接口（`/api/**`）。

### 认证接口（需要认证）

本系统无认证机制，无认证请求头。

> 后续各模块文档中，"请求头: [公开]" 引用上述公开请求头模板。

---

## 响应包装说明

所有接口响应均经过统一的包装类处理，以下为框架级定义。

### ApiResponse\<T\> — 非分页响应

| 字段路径 | 类型 | 可空 | 说明 | 示例值 |
|----------|------|:---:|------|--------|
| code | String | 否 | 业务状态码，成功固定 `"200"`；失败为 ErrorCode 枚举名（如 `COMMON_400_VALIDATION`） | `"200"` |
| message | String | 否 | 业务消息，成功固定 `"success"`；失败为枚举默认消息 | `"success"` |
| data | T | 是 | 业务数据（泛型），无数据时为 `null` | `{...}` |
| traceId | String | 否 | 链路追踪 ID（取自 X-Trace-Id 或服务端生成） | `a1b2c3...` |

### PageResult\<T\> — 分页响应

分页接口的 `data` 为该结构：

| 字段路径 | 类型 | 可空 | 说明 | 示例值 |
|----------|------|:---:|------|--------|
| items | List\<T\> | 否 | 当前页数据列表 | `[{...}]` |
| page | Long | 否 | 当前页码（从 1 开始） | `1` |
| pageSize | Long | 否 | 页大小（1-100，上限 100） | `20` |
| total | Long | 否 | 总记录数 | `100` |

> 说明：`page`/`pageSize` 以字符串形式接收并手工解析，非法值统一返回 400 `COMMON_400_VALIDATION`；`pageSize` 上限 100。时间字段序列化为 ISO8601（`yyyy-MM-dd'T'HH:mm:ssXXX`），Instant 字段带时区后缀。

---

## 权限体系

- **权限模型**: 无（`none`）
- **超级管理员**: 无
- **权限标识格式**: 无
- **数据权限**: 无
- 全项目无任何权限注解（@PreAuthorize/@SaCheckPermission 等）与角色控制，所有接口无鉴权、无租户隔离，`createdBy`/`submittedBy` 等字段为前端可信传入。

---

## 错误码速查

错误响应：HTTP 状态码 = ErrorCode 对应的 HttpStatus；响应体 `code` = 枚举名，`message` = 枚举默认消息（GlobalExceptionHandler 统一输出）。

| 错误码 | HTTP 状态 | 默认消息 | 触发场景 |
|--------|:---:|------|------|
| COMMON_400_VALIDATION | 400 | Validation failed | 参数校验失败（含分页/枚举/布尔手工解析失败、请求体不可读） |
| COMMON_404_RESOURCE | 404 | Resource not found | 资源不存在（Agent 等） |
| COMMON_409_CONFLICT | 409 | Resource conflict | 资源冲突（用例编码重复等） |
| COMMON_500_INTERNAL | 500 | Internal server error | 未预期异常 |
| AGENT_400_CONFIG | 400 | Invalid agent configuration | Agent 配置非法 |
| TEST_CASE_400_RULE | 400 | Invalid test case rule | 测试用例判定规则非法 |
| TEST_CASE_NOT_FOUND | 404 | Test case not found | 测试用例不存在 |
| SCHEME_400_INVALID | 400 | Invalid evaluation scheme | 方案校验不通过（data 含 ValidationError 列表） |
| SCHEME_409_STATUS | 409 | Evaluation scheme status conflict | 方案状态冲突（发布等） |
| SCHEME_NOT_FOUND | 404 | Evaluation scheme not found | 方案不存在 |
| SCHEME_ALREADY_ARCHIVED | 409 | Evaluation scheme is already archived | 方案已归档 |
| DRAFT_SCHEME_REFERENCED | 409 | Draft evaluation scheme is referenced | 草稿方案被引用 |
| SCHEME_DELETE_CONFLICT | 409 | Evaluation scheme deletion conflict | 方案删除冲突 |
| TASK_409_SCHEME_STATUS | 409 | Evaluation scheme is not available for this task | 方案状态不可用于建任务 |
| TASK_409_STATUS | 409 | Evaluation task status conflict | 任务状态冲突 |
| TASK_409_SNAPSHOT_UNSUPPORTED | 409 | Evaluation task snapshot is not supported | 任务快照不支持 |
| TASK_409_RESULT_NOT_READY | 409 | Evaluation result is not ready | 结果/报告未就绪 |
| TASK_500_RESULT_INCONSISTENT | 500 | Persisted evaluation result is inconsistent | 持久化结果不一致 |
| TASK_503_EXECUTOR | 503 | Evaluation executor unavailable | 执行器队列不可用 |

---

## 模块概览

| 模块 | 路由前缀 | 接口数量 | 说明 | 文档链接 |
|------|---------|:---:|------|----------|
| 智能体模块 | `/api/agents` | 5 | Agent 配置的增删改查（分页查询/创建/详情/更新/删除，删除按任务引用自动降级为禁用） | [01-智能体模块.md](modules/01-智能体模块.md) |
| 指标目录模块 | `/api/indicator-dimensions`、`/api/indicator-categories`、`/api/indicators`、`/api/indicator-catalog-versions` | 5 | 指标维度/分类/指标/目录版本查询（全部为 GET 只读接口） | [02-指标目录模块.md](modules/02-指标目录模块.md) |
| 测试用例模块 | `/api/test-cases`（含 `/import`、`/import/excel`、`/import/template`） | 8 | 测试用例 CRUD（软删除）+ JSON 批量导入 + Excel 导入/模板下载 | [03-测试用例模块.md](modules/03-测试用例模块.md) |
| 评测任务模块 | `/api/evaluation-tasks`（含 ad-hoc、progress、run、measurements、finalize、results、case-results、calls、report） | 14 | 任务生命周期（创建/启动/测量证据/终评）+ 结果、用例结果、调用记录、报告查询 | [04-评测任务模块.md](modules/04-评测任务模块.md) |
| 评测方案模块 | `/api/evaluation-schemes`（含 validate、publish、clone、archive、deletion-impact） | 10 | 方案草稿 CRUD + 校验/发布/克隆/归档/删除影响预览（DRAFT→PUBLISHED→ARCHIVED 状态机） | [05-评测方案模块.md](modules/05-评测方案模块.md) |

> 合计 42 个接口。各模块的接口明细（请求参数、响应结构、错误码、业务规则）见对应模块文档。实体类定义见 `entities/` 目录。

---

## 已知问题与注意事项

| # | 问题 | 影响接口/模块 | 说明 | 建议 |
|---|------|---------|------|------|
| 1 | 无认证机制 | 全部 42 接口 | 系统无登录/token 体系，所有 `/api/**` 接口公开访问；创建任务、发布方案等写操作无鉴权，`createdBy`/`submittedBy`/`confirmedBy` 等身份字段由前端可信传入 | 接入网关/统一认证（OAuth2/JWT 等），写操作至少做接口级鉴权，身份字段由服务端注入 |
| 2 | 目录版本接口返回全状态版本 | 指标目录模块 `GET /api/indicator-catalog-versions` | SQL 无 status 过滤，返回含 DRAFT/RETIRED 的全部版本，与接口说明"已发布版本"语义存在出入 | 修正 SQL 增加 `status='PUBLISHED'` 过滤，或修正文档/接口语义声明 |
| 3 | SubmitMeasurementRequest/ConfirmMeasurementRequest 无校验注解 | 评测任务模块 `POST /api/evaluation-tasks/{taskId}/measurements`、`/api/evaluation-tasks/{taskId}/measurements/{measurementId}/confirm` | DTO 无 `@Valid` 注解、字段均可选，必填/格式校验全部散落在 Service 层手工实现（measurementType/unit 与快照比对、period 成对、payload JSON 等），校验语义与接口文档易脱节 | 为 DTO 补充 Bean Validation 注解前置必填/格式校验，Service 层仅保留跨字段业务校验 |
| 4 | AgentRequest 无 @Valid 注解 | 智能体模块 `POST /api/agents`、`PUT /api/agents/{id}` | 必填与格式校验由 Controller/Service 手工完成（失败报 AGENT_400_CONFIG/COMMON_400_VALIDATION），规则与接口实现绑定，不利于维护与复用 | 为 DTO 补充 Bean Validation 注解，Service 层保留配置类业务校验 |
| 5 | evaluationType/thresholdLevel 字段已弃用 | 评测方案模块（创建/更新/查询）、评测任务模块（ad-hoc 创建、任务实体） | 遗留字段：`evaluationType` 已标注"已弃用"但仍接受输入（非法值报 400）；`thresholdLevel` 保留在请求/响应实体中，示例均为 null、未参与计算 | 后续版本移除字段或明确标注 deprecated 语义，避免调用方误用并预留兼容处理 |
| 6 | 明文数据库口令与 Dify API Key | 部署配置（影响全部接口） | `application-dev.yml` 含明文数据库口令（root/root）与 Dify API Key（`app-*`，framework-analysis.md 已脱敏标注）；沿用 dev profile 部署存在泄露风险 | 改用环境变量注入（local 环境已支持 DB_URL/DB_USERNAME/DB_PASSWORD/DIFY_AI_JUDGE_API_KEY），同时轮换已泄露密钥 |
| 7 | 硬编码错误消息，无 i18n | 全部模块 | 错误消息来自 ErrorCode 枚举 `defaultMessage`（如 `"Validation failed"`），未发现 messages*.properties，无法按语言/环境定制提示 | 引入 i18n 资源文件，GlobalExceptionHandler 按 Locale 输出对应文案 |

---

*文档基于后端源码 CodeGraph 分析生成 · v1.0 · 2026-08-19*
