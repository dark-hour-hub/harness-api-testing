# 模块分析报告：agent-evaluation-platform-backend

**生成时间**: 2026-08-19
**分析方式**: CodeGraph 深度源码分析（索引 252 文件 / 4,992 节点）

## 技术栈

- 后端：Java 17 + Spring Boot 3.5.16（Spring MVC REST + WebFlux WebClient 出站调用）
- 架构：六边形/DDD，包根 `com.czbank.aicgs.evaluation`，各域按 agent/indicator/testcase/scheme/task/execution/scoring/report/measurement 划分
- ORM：MyBatis-Plus 3.5.17（MySQL 分页插件）
- 数据库：MySQL（dev: `jdbc:mysql://localhost:3306/agent_evaluation`，用户名 root，口令 dev 配置为明文）
- 校验：spring-boot-starter-validation（Hibernate Validator）
- API 文档：springdoc-openapi 2.8.17（/swagger-ui.html、/v3/api-docs）
- Excel：Apache POI 5.2.5（测试用例导入）
- 前端：Vue（本次任务不分析前端，仅后端）

## 微服务

| 服务名 | 端口 | 描述 |
|--------|------|------|
| agent-evaluation-platform-backend | 8080 | 智能体评测平台后端（单服务，无注册中心/网关） |

## 响应包装结构

所有 JSON 接口统一返回 `ApiResponse<T>`（`com.czbank.aicgs.evaluation.common.api.ApiResponse`）：

| 字段 | 类型 | 说明 |
|------|------|------|
| code | string | 成功固定 `"200"`；失败为 ErrorCode 枚举名（如 `COMMON_400_VALIDATION`、`COMMON_404_RESOURCE`、`COMMON_409_CONFLICT`、`TASK_503_EXECUTOR`） |
| message | string | 成功固定 `"success"`；失败为 ErrorCode.defaultMessage 英文文案 |
| data | T | 业务数据；部分接口为 null（如 DELETE /api/agents/{id}） |
| traceId | string | 链路追踪 ID：取 X-Trace-Id 请求头或服务端生成的 32 位小写十六进制 UUID |

分页数据统一为 `PageResult<T>`（`common/api/PageResult.java`）：

| 字段 | 类型 | 说明 |
|------|------|------|
| items | array | 当前页数据列表 |
| page | integer | 当前页码（从 1 开始） |
| pageSize | integer | 页大小（1-100） |
| total | integer | 记录总数 |

## API 端点

共 42 个业务接口（GET 21 / POST 15 / PUT 3 / DELETE 3），按模块分组：

| 模块 | 方法 | 路径 | 描述 | 权限 |
|------|------|------|------|------|
| agents | GET | /api/agents | 分页查询 Agent 配置 | 无 |
| agents | POST | /api/agents | 创建 Agent 配置 | 无 |
| agents | GET | /api/agents/{id} | 查询 Agent 配置详情 | 无 |
| agents | PUT | /api/agents/{id} | 更新 Agent 配置 | 无 |
| agents | DELETE | /api/agents/{id} | 禁用/删除 Agent 配置 | 无 |
| indicators | GET | /api/indicator-dimensions | 指标维度列表 | 无 |
| indicators | GET | /api/indicator-categories | 指标分类列表 | 无 |
| indicators | GET | /api/indicators | 分页查询指标 | 无 |
| indicators | GET | /api/indicators/{id} | 查询指标详情 | 无 |
| indicators | GET | /api/indicator-catalog-versions | 指标目录版本列表 | 无 |
| test-cases | GET | /api/test-cases | 分页查询测试用例 | 无 |
| test-cases | POST | /api/test-cases | 创建测试用例 | 无 |
| test-cases | GET | /api/test-cases/{id} | 查询测试用例 | 无 |
| test-cases | PUT | /api/test-cases/{id} | 更新测试用例 | 无 |
| test-cases | DELETE | /api/test-cases/{id} | 软删除测试用例 | 无 |
| test-cases | POST | /api/test-cases/import | 批量导入测试用例（JSON） | 无 |
| test-cases | POST | /api/test-cases/import/excel | Excel 导入测试用例（multipart） | 无 |
| test-cases | GET | /api/test-cases/import/template | 下载 Excel 导入模板（二进制） | 无 |
| evaluation-tasks | POST | /api/evaluation-tasks | 创建评估任务（快照，不执行） | 无 |
| evaluation-tasks | POST | /api/evaluation-tasks/ad-hoc | 创建临场评估任务 | 无 |
| evaluation-tasks | GET | /api/evaluation-tasks | 分页查询任务 | 无 |
| evaluation-tasks | GET | /api/evaluation-tasks/{id} | 查询任务详情 | 无 |
| evaluation-tasks | GET | /api/evaluation-tasks/{id}/progress | 查询任务进度 | 无 |
| evaluation-tasks | POST | /api/evaluation-tasks/{id}/run | 启动任务执行（HTTP 202） | 无 |
| evaluation-schemes | GET | /api/evaluation-schemes | 分页查询评测方案 | 无 |
| evaluation-schemes | POST | /api/evaluation-schemes | 创建方案草稿 | 无 |
| evaluation-schemes | GET | /api/evaluation-schemes/{id} | 查询方案详情 | 无 |
| evaluation-schemes | PUT | /api/evaluation-schemes/{id} | 更新方案草稿 | 无 |
| evaluation-schemes | DELETE | /api/evaluation-schemes/{id} | 删除方案（物理删除/归档） | 无 |
| evaluation-schemes | GET | /api/evaluation-schemes/{id}/deletion-impact | 预览删除影响 | 无 |
| evaluation-schemes | POST | /api/evaluation-schemes/{id}/validate | 校验方案草稿 | 无 |
| evaluation-schemes | POST | /api/evaluation-schemes/{id}/publish | 发布方案 | 无 |
| evaluation-schemes | POST | /api/evaluation-schemes/{id}/clone | 克隆方案为草稿 | 无 |
| evaluation-schemes | POST | /api/evaluation-schemes/{id}/archive | 归档方案 | 无 |
| results | POST | /api/evaluation-tasks/{id}/finalize | 重算不完整任务的评分 | 无 |
| results | GET | /api/evaluation-tasks/{id}/results | 任务评测结果汇总 | 无 |
| results | GET | /api/evaluation-tasks/{id}/results/indicators | 分页查询指标结果 | 无 |
| results | GET | /api/evaluation-tasks/{id}/case-results | 分页查询用例判定结果 | 无 |
| results | GET | /api/evaluation-tasks/{id}/calls | 分页查询 Agent 调用记录（脱敏） | 无 |
| results | GET | /api/evaluation-tasks/{id}/report | 查询评测报告 | 无 |
| measurements | POST | /api/evaluation-tasks/{taskId}/measurements | 提交指标测量草稿证据 | 无 |
| measurements | POST | /api/evaluation-tasks/{taskId}/measurements/{measurementId}/confirm | 确认测量证据 | 无 |

## 前端页面

| 路径 | 组件 | 描述 |
|------|------|------|
| - | - | 本任务仅分析后端；前端 `agent-evaluation-platform-frontend`（Vue 3 + Vite，localhost:5173）留待 UI 分析流水线处理 |

## 认证机制

- 类型：无（`none`）
- Token 过期时间：无（无 Token）
- 唯一 Filter：TraceIdFilter（@Order(HIGHEST_PRECEDENCE)），仅做 X-Trace-Id 链路追踪，与认证无关
- 无登录接口、无权限注解、无拦截器（详见 `_workflow/02-analysis-plan/auth-analysis.md`）

## 拦截器/请求头

| 拦截器 | 路径前缀 | 必填 Header | 可选 Header |
|--------|----------|-------------|-------------|
| TraceIdFilter (OncePerRequestFilter) | 所有路径 | - | X-Trace-Id（缺失自动生成；透传至响应头与响应体 traceId） |

## 错误码速查

| ErrorCode | HTTP | 默认 message | 典型触发场景 |
|-----------|------|--------------|--------------|
| COMMON_400_VALIDATION | 400 | Validation failed | Bean 校验失败、请求体不可读、分页/枚举/布尔参数非法、测量数据非法 |
| COMMON_404_RESOURCE | 404 | Resource not found | Agent/指标/任务/测量记录不存在 |
| COMMON_409_CONFLICT | 409 | Resource conflict | Agent code 重复、用例 code 重复、测量状态冲突 |
| AGENT_400_CONFIG | 400 | Invalid agent configuration | Agent 配置非法（endpoint 无 host） |
| TEST_CASE_400_RULE | 400 | Invalid test case rule | 用例判定规则非法 |
| TEST_CASE_NOT_FOUND | 404 | Test case not found | 用例不存在 |
| SCHEME_400_INVALID | 400 | Invalid evaluation scheme | 方案校验失败（validate 接口 data 带错误列表） |
| SCHEME_409_STATUS | 409 | Evaluation scheme status conflict | 方案状态冲突（非草稿发布/更新等） |
| SCHEME_NOT_FOUND | 404 | Evaluation scheme not found | 方案不存在 |
| SCHEME_ALREADY_ARCHIVED | 409 | Evaluation scheme is already archived | 重复归档 |
| DRAFT_SCHEME_REFERENCED | 409 | Draft evaluation scheme is referenced | 被引用的草稿删除冲突 |
| SCHEME_DELETE_CONFLICT | 409 | Evaluation scheme deletion conflict | 删除冲突 |
| TASK_409_SCHEME_STATUS | 409 | Evaluation scheme is not available for this task | 用非发布方案建任务 |
| TASK_409_STATUS | 409 | Evaluation task status conflict | 重复 run/finalize 等 |
| TASK_409_SNAPSHOT_UNSUPPORTED | 409 | Evaluation task snapshot is not supported | 快照类型不支持 |
| TASK_409_RESULT_NOT_READY | 409 | Evaluation result is not ready | 结果/报告未就绪 |
| TASK_500_RESULT_INCONSISTENT | 500 | Persisted evaluation result is inconsistent | 持久化结果不一致 |
| TASK_503_EXECUTOR | 503 | Evaluation executor unavailable | 执行器队列不可用 |
| COMMON_500_INTERNAL | 500 | Internal server error | 未处理异常（响应不泄露堆栈） |

## 数据流要点（供测试用例设计参考）

1. **任务执行主链路**：`POST /api/evaluation-tasks`（或 ad-hoc）→ `POST /api/evaluation-tasks/{id}/run`（202 Accepted）→ `GET .../progress` 轮询 → `GET .../results` / `.../case-results` / `.../calls` / `.../report`。run 会真实调用外部 Agent 端点与 Dify AI 判分服务（dev 配置 base-url http://180.76.180.32/v1），测试环境网络不通时执行会失败，建议准备可控的 Agent 端点或仅测试到 run 之前的环节。
2. **方案生命周期**：`POST /api/evaluation-schemes`（DRAFT）→ `validate` → `publish`（PUBLISHED）→ 创建任务引用 → 删除已发布方案自动归档（PHYSICALLY_DELETED 仅限未引用草稿）。
3. **measurement 证据流**：`POST .../measurements`（DRAFT）→ `POST .../measurements/{id}/confirm`（CONFIRMED）；重复 confirm 返回 409。
4. **Excel 导入**：`GET /api/test-cases/import/template` 取模板 → 填写 → `POST /api/test-cases/import/excel`（multipart，参数名 file/indicatorId）；空文件返回 400 + ImportError 列表。
5. **分页与过滤参数均为字符串手工解析**：page/pageSize 非法（<1、非数字、pageSize>100）返回 400；枚举参数非法值返回 400；status 白名单（results 模块 16 个值）外返回 400。
