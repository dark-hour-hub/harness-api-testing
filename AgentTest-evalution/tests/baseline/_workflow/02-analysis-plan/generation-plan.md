# 源码分析计划

**模块**: agent-evaluation-platform-backend（智能体评测平台后端）
**生成时间**: 2026-08-19
**分析方式**: CodeGraph 深度源码分析（索引 252 文件 / 4,992 节点，CLI 版本 1.1.0）

---

## 一、分析范围

| 类型 | 数量 | 说明 |
|------|------|------|
| 后端源码 | 1 | `evaluation-platform-backend`（Maven 单子模块，父 pom `evaluation-platform`，main 源码 252 个 Java 文件，另含 test 源码 74 个 Java 文件） |
| Controller | 10 | 均位于各模块 `adapter/in/web/` 包 |
| API 接口 | 42 | 与 CodeGraph route 索引业务路由数一致（索引共 45 条，剔除 3 条测试路由） |
| DTO/VO 类 | 56 | Request/Response/Command/Query/Snapshot/View/Result/Progress 命名文件 |

### 各模块 API 数量（按 URL 前缀分组）

| 模块 | Controller | API 数量 | 路由清单 |
|------|-----------|---------|----------|
| agents | AgentController | 5 | GET/POST /api/agents、GET/PUT/DELETE /api/agents/{id} |
| indicators | IndicatorController + IndicatorCatalogVersionController | 5 | GET /api/indicators、GET /api/indicators/{id}、GET /api/indicator-dimensions、GET /api/indicator-categories、GET /api/indicator-catalog-versions |
| test-cases | TestCaseController + TestCaseExcelImportController | 8 | GET/POST /api/test-cases、GET/PUT/DELETE /api/test-cases/{id}、POST /api/test-cases/import、POST /api/test-cases/import/excel、GET /api/test-cases/import/template |
| evaluation-tasks | EvaluationTaskController + EvaluationExecutionController | 6 | GET/POST /api/evaluation-tasks、POST /api/evaluation-tasks/ad-hoc、GET /api/evaluation-tasks/{id}、GET /api/evaluation-tasks/{id}/progress、POST /api/evaluation-tasks/{id}/run |
| evaluation-schemes | EvaluationSchemeController | 10 | GET/POST /api/evaluation-schemes、GET/PUT/DELETE /api/evaluation-schemes/{id}、GET /api/evaluation-schemes/{id}/deletion-impact、POST /api/evaluation-schemes/{id}/validate、/publish、/clone、/archive |
| results | EvaluationResultController | 6 | POST /api/evaluation-tasks/{id}/finalize、GET /api/evaluation-tasks/{id}/results、GET /api/evaluation-tasks/{id}/results/indicators、GET /api/evaluation-tasks/{id}/case-results、GET /api/evaluation-tasks/{id}/calls、GET /api/evaluation-tasks/{id}/report |
| measurements | IndicatorMeasurementController | 2 | POST /api/evaluation-tasks/{taskId}/measurements、POST /api/evaluation-tasks/{taskId}/measurements/{measurementId}/confirm |

**合计**: GET 21 + POST 15 + PUT 3 + DELETE 3 = 42（PATCH 0，WebFlux RouterFunction 0）

### 排除清单（不在 apis.json 中）

| 排除类型 | 数量 | 路由 | 原因 |
|----------|------|------|------|
| 测试代码路由 | 3 | GET /unexpected、GET /not-found、POST /validation（均来自 `src/test/.../GlobalExceptionHandlerTest.java` 内嵌 TestController） | 测试专用，非业务接口，仅用于验证全局异常处理器行为 |

### HTTP 方法分布

| 方法 | 数量 | 说明 |
|------|------|------|
| GET | 21 | 查询类接口 |
| POST | 15 | 创建/操作类接口 |
| PUT | 3 | 更新类接口（agents/test-cases/evaluation-schemes） |
| DELETE | 3 | 删除类接口（agents/test-cases/evaluation-schemes） |

## 二、技术栈

| 类型 | 框架 | 说明 |
|------|------|------|
| 后端 | Spring Boot 3.5.16 | spring-boot-starter-parent，Java 17 |
| Web | Spring MVC (starter-web) + WebFlux (starter-webflux) | 同步接口 + WebClient 出站调用（Agent 调用/AI 判分） |
| ORM | MyBatis-Plus 3.5.17（spring-boot3-starter + jsqlparser） | MybatisPlusConfig 注册 MySQL 分页插件 |
| 数据库 | MySQL 8.x（mysql-connector-j，dev 配置 localhost:3306/agent_evaluation） | 连接池默认 HikariCP |
| 校验 | spring-boot-starter-validation（Hibernate Validator） | @NotBlank/@NotNull/@Positive/@Size/@Pattern/@DecimalMin/@DecimalMax |
| API 文档 | springdoc-openapi-starter-webmvc-ui 2.8.17 | OpenApiConfig 分 7 组：agents/indicators/test-cases/schemes/tasks/results |
| Excel | Apache POI 5.2.5 (poi-ooxml) | 测试用例 Excel 导入/模板下载 |
| JSON | Jackson + json-path | 请求模板渲染与响应字段提取 |
| 测试 | spring-boot-starter-test、H2、ArchUnit 1.4.1 | 单元测试 |
| 前端 | 未纳入本次分析范围 | 本任务仅分析后端（config.yaml 中 frontend.enabled=true，留给 UI 分析流水线） |
| 认证框架 | 无 | 详见 auth-analysis.md |

## 三、校验规则提取

> 规则来源：DTO 注解（Bean Validation）+ Controller 手工解析校验（parsePage/parseEnum/parseRequiredEnum 等，失败统一抛 `COMMON_400_VALIDATION`）。Agent 接口的 `AgentRequest` 未加 `@Valid`，必填性由 Controller 手工解析保证。

| 字段 | 类型 | 必填 | 校验规则 | 来源 |
|------|------|------|----------|------|
| AgentRequest.agentCode | string | true | pattern `[A-Z0-9_]{2,64}`（Schema 声明，无注解强校验）；创建/更新时非空 | @Schema + Controller 手工 |
| AgentRequest.riskTier | string(enum A/B/C/D) | true | 枚举值，缺失/非法 → COMMON_400_VALIDATION | Controller parseRequiredEnum |
| AgentRequest.adapterType | string(enum) | true | MINI_ZHEXIAOZHI / GENERIC_HTTP_JSON | Controller parseRequiredEnum |
| AgentRequest.timeoutMs | string(数字) | true | 100 ≤ n ≤ 120000（Schema 声明 min/max；代码仅校验可解析且非空） | Controller parseRequiredLong |
| AgentRequest.headerSecretRef | string | false | pattern `(?:env:[A-Za-z_]\w*\|secret:[\w./:-]+\|app-\w{6,})` | @Schema |
| TestCaseRequest.caseCode | string | true | @NotBlank | Bean Validation |
| TestCaseRequest.caseName | string | true | @NotBlank | Bean Validation |
| TestCaseRequest.indicatorId | integer | true | @NotNull @Positive（>0） | Bean Validation |
| TestCaseRequest.caseType | string(enum) | true | SINGLE_TURN/MULTI_TURN/TOOL_CALL/MANUAL_AUDIT（@NotNull） | Bean Validation |
| TestCaseRequest.weight | number | true | @NotNull @DecimalMin(value=0, inclusive=false) 即 >0 | Bean Validation |
| TestCaseRequest.passScore | number | true | @NotNull @DecimalMin(0) @DecimalMax(100) | Bean Validation |
| TestCaseRequest.version | string | true | @NotBlank | Bean Validation |
| TestCaseRequest.combineMode | string(enum) | true | ALL/ANY/WEIGHTED（@NotNull） | Bean Validation |
| TestCaseRequest.rules | array | true | @NotEmpty（至少 1 条） | Bean Validation |
| TestCaseRequest.rules[].judgeType | string(enum) | true | 11 种 JudgeType（@NotNull） | Bean Validation |
| TestCaseRequest.rules[].ruleOrder | integer | true | @NotNull @Positive | Bean Validation |
| TestCaseRequest.rules[].ruleConfig | object | true | @NotNull | Bean Validation |
| TestCaseRequest.scenarioType | string | false | 缺省 AUTO | Controller/domain 默认 |
| EvaluationSchemeRequest.schemeCode | string | true | @NotBlank | Bean Validation |
| EvaluationSchemeRequest.schemeName | string | true | @NotBlank | Bean Validation |
| EvaluationSchemeRequest.version | string | true | @NotBlank @Size(max=64) @Pattern(数字点分版本号) | Bean Validation |
| EvaluationSchemeRequest.evaluationMode | string(enum) | true | COMPREHENSIVE/SPECIAL（@NotNull） | Bean Validation |
| EvaluationSchemeRequest.riskTier | string(enum) | true | A/B/C/D（@NotNull） | Bean Validation |
| CreateEvaluationTaskRequest.agentId | integer | true | @NotNull @Positive | Bean Validation |
| CreateEvaluationTaskRequest.schemeId | integer | true | @NotNull @Positive | Bean Validation |
| CreateEvaluationTaskRequest.createdBy | string | false | @Size(max=100)，缺省 "api" | Bean Validation |
| CreateAdHocEvaluationTaskRequest.agentId | integer | true | @NotNull @Positive | Bean Validation |
| CreateAdHocEvaluationTaskRequest.indicators | array | true | @NotEmpty，元素 @Valid | Bean Validation |
| CreateAdHocEvaluationTaskRequest.testCaseIds | array | true | @NotEmpty，元素 @Positive | Bean Validation |
| AdHocIndicatorRequest.indicatorId | integer | true | @NotNull @Positive | Bean Validation |
| AdHocIndicatorRequest.weightOverride/thresholdOverride | number | false | @DecimalMin(0, exclusive) | Bean Validation |
| SubmitMeasurementRequest | object | false | 无校验注解（所有字段可选） | Controller 无 @Valid |
| ConfirmMeasurementRequest.confirmedBy | string | false | 无校验注解 | Controller 无 @Valid |
| 分页参数 page / pageSize | string(数字) | 是 | ≥1；pageSize ≤ MAX_PAGE_SIZE=100；非法值 → COMMON_400_VALIDATION | Controller 手工解析（4 个 Controller 同规则） |
| 路径变量 id | string(数字) | 是 | 必须为正整数，否则 → COMMON_400_VALIDATION | Controller 手工解析 |
| 枚举 query 参数（status/direction/caseType 等） | string | 否 | 非法枚举值 → COMMON_400_VALIDATION | Controller parseEnum |
| Query 布尔参数（enabled/passed/success） | string | 否 | 仅接受 true/false（忽略大小写） | Controller 手工解析 |
| EvaluationResultController.status | string | 否 | 白名单 16 个取值（COMPLETED/NOT_APPLICABLE/WAITING_* 等） | Controller RESULT_STATUSES |
| EvaluationResultController.errorType | string | 否 | AgentInvocationErrorType 枚举且 ≠ NONE | Controller validateErrorType |
| 测试用例导入 Excel file | file | 是 | multipart，file 必填且非空；解析失败 → 400 + ImportError 列表 | Controller + ExcelTestCaseImportService |
| DimensionWeights | object | false | 非空 Map<dimensionCode, weight>；空/null 抛 IllegalArgumentException（→ 500 COMMON_500_INTERNAL 或解析错误） | domain 构造器 |

## 四、错误消息追踪

> 所有异常统一由 `GlobalExceptionHandler`（@RestControllerAdvice）或 Controller 局部 @ExceptionHandler 处理，响应体均为 `ApiResponse`（code/message/data/traceId）。`BusinessException` 的 message 固定取 ErrorCode.defaultMessage（构造入参 context 不参与 message 拼接）。

| 场景 | HTTP | Code | Message | 追踪路径 |
|------|------|------|---------|----------|
| Bean 校验失败（@Valid @RequestBody） | 400 | COMMON_400_VALIDATION | Validation failed（data 为字段错误 Map：`{"caseCode":"must not be blank"}`） | Controller → @Valid → MethodArgumentNotValidException → GlobalExceptionHandler.handleValidation |
| 请求体 JSON 不可读/类型错误 | 400 | COMMON_400_VALIDATION | Validation failed | HttpMessageNotReadableException → Controller 局部 @ExceptionHandler（Agent/TestCase/EvaluationTask/EvaluationScheme 4 个 Controller） |
| 分页/枚举/布尔参数非法 | 400 | COMMON_400_VALIDATION | Validation failed | Controller parsePage/parseEnum → BusinessException → GlobalExceptionHandler |
| Agent code 重复（创建/更新） | 409 | COMMON_409_CONFLICT | Resource conflict | AgentController → AgentConfigService:45/66 或 MybatisAgentConfigRepository:43/57 |
| Agent 不存在 | 404 | COMMON_404_RESOURCE | Resource not found | AgentConfigService:83 |
| Agent 配置非法（如 endpoint 无 host） | 400 | AGENT_400_CONFIG | Invalid agent configuration | AgentConfigService:231 |
| TestCase 不存在 | 404 | TEST_CASE_NOT_FOUND | Test case not found | MybatisTestCaseRepository:156 |
| TestCase code 重复 | 409 | COMMON_409_CONFLICT | Resource conflict | TestCaseService:54/64 |
| TestCase 规则配置非法 | 400 | TEST_CASE_400_RULE | Invalid test case rule | TestCaseService:157 |
| 用例批量导入（含行级校验失败） | 200/400 | 行错误 code 各异 | 行级 message | TestCaseController.importCases → ImportError 列表（data=errors） |
| 导入 JSON 数组行内非法值 | 400 | COMMON_400_VALIDATION | Validation failed（data=ImportError 列表） | HttpMessageNotReadableException → TestCaseController 局部处理器 |
| Excel 为空/无法解析 | 400 | COMMON_400_VALIDATION | Excel file is required / Unable to read the Excel file | TestCaseExcelImportController.importExcel |
| Scheme 不存在 | 404 | SCHEME_NOT_FOUND | Evaluation scheme not found | EvaluationSchemeService:152/230 |
| Scheme 状态冲突（DRAFT→发布等） | 409 | SCHEME_409_STATUS | Evaluation scheme status conflict | EvaluationSchemeService 多处 |
| Scheme 校验失败（validate 接口） | 400 | SCHEME_400_INVALID | Invalid evaluation scheme（data=SchemeValidationResult） | SchemeValidator → SchemeValidationException → EvaluationSchemeController 局部处理器 |
| Scheme 已归档 | 409 | SCHEME_ALREADY_ARCHIVED | Evaluation scheme is already archived | EvaluationSchemeService:245 |
| 草稿 Scheme 被任务引用（删除） | 409 | DRAFT_SCHEME_REFERENCED | Draft evaluation scheme is referenced | EvaluationSchemeService:236 |
| 删除冲突（发布方案被引用） | 409 | SCHEME_DELETE_CONFLICT | Evaluation scheme deletion conflict | MybatisEvaluationSchemeRepository:142 |
| 创建任务时 Scheme 非发布态 | 409 | TASK_409_SCHEME_STATUS | Evaluation scheme is not available for this task | EvaluationTaskService:129/149 |
| 任务状态冲突（重复 run/finalize） | 409 | TASK_409_STATUS | Evaluation task status conflict | EvaluationTaskExecutionService:43/52、EvaluationScoringService:156/180/201/241 |
| 快照类型不支持 | 409 | TASK_409_SNAPSHOT_UNSUPPORTED | Evaluation task snapshot is not supported | EvaluationTaskExecutionService:48 |
| 结果/报告未就绪 | 409 | TASK_409_RESULT_NOT_READY | Evaluation result is not ready | EvaluationScoringService:234、EvaluationReportQueryService:175 |
| 结果数据不一致 | 500 | TASK_500_RESULT_INCONSISTENT | Persisted evaluation result is inconsistent | EvaluationReportQueryService:179/200 |
| 执行器队列不可用 | 503 | TASK_503_EXECUTOR | Evaluation executor unavailable | EvaluationTaskExecutionService:58（run 接口） |
| 任务不存在 | 404 | COMMON_404_RESOURCE | Resource not found | EvaluationTaskExecutionService:41、EvaluationScoringService:186/196/213 |
| 指标不存在 | 404 | COMMON_404_RESOURCE | Resource not found | IndicatorCatalogService:62 |
| 指标目录版本不存在 | 404 | COMMON_404_RESOURCE | Resource not found | IndicatorCatalogVersionService:53 |
| 测量任务/记录不存在 | 404 | COMMON_404_RESOURCE | Resource not found | IndicatorMeasurementService:30/61 |
| 测量状态冲突（重复确认） | 409 | COMMON_409_CONFLICT | Resource conflict | IndicatorMeasurementService:64/67 |
| 测量提交数据非法 | 400 | COMMON_400_VALIDATION | Validation failed | IndicatorMeasurementService:45 |
| 未处理异常（NPE 等） | 500 | COMMON_500_INTERNAL | Internal server error | Exception → GlobalExceptionHandler.handleUnexpectedException（日志含 traceId，响应不泄露堆栈） |

## 五、输出文件

| 文件 | 路径 |
|------|------|
| 接口清单 | tests/baseline/_workflow/02-analysis-plan/apis.json |
| 生成计划 | tests/baseline/_workflow/02-analysis-plan/generation-plan.md |
| 框架分析报告 | tests/baseline/_workflow/02-analysis-plan/framework-analysis.md |
| 认证机制分析报告 | tests/baseline/_workflow/02-analysis-plan/auth-analysis.md |
| 模块分析报告 | tests/baseline/specs/agent-evaluation-platform-backend/agent-evaluation-platform-backend-analysis.md |
| 规格文件 | tests/baseline/specs/agent-evaluation-platform-backend/agent-evaluation-platform-backend-spec.yaml |

## 六、下一步

1. 使用 `test-case-generator`（api-doc-to-testcases / yaml-to-pytest）技能，基于 apis.json 与 spec.yaml 生成 YAML 测试用例并转 pytest 脚本。
2. 注意：本项目无认证机制，接口测试无需登录/token 流程；如需校验 traceId 透传，可断言响应头 `X-Trace-Id` 与响应体 `traceId` 一致。
3. 反向用例断言建议统一校验 HTTP 状态码 + `code` 字段（枚举值见第四节），而非 message 文本。
