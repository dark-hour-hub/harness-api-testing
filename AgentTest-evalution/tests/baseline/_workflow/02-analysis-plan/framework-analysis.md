# 框架分析报告

**生成时间**: 2026-08-19
**分析项目数**: 1

---

## 项目：agent-evaluation-platform-backend

### 一、基本信息

| 属性 | 值 |
|------|-----|
| 项目路径 | `D:\AI评测\智能体评测平台\agent-evaluation-platform-backend` |
| 项目名称（config.yaml） | agent-test-backend |
| Spring Boot | 3.5.16（父 pom `spring-boot-starter-parent`） |
| Java | 17 |
| 项目类型 | 多模块（父 pom `evaluation-platform` + 1 个子模块 `evaluation-platform-backend`；后端实际为单应用模块） |
| 构建工具 | Maven |
| 架构风格 | 六边形/DDD（domain / application / adapter.in.web / adapter.out.persistence 分层，每个业务域独立包） |
| 包根 | `com.czbank.aicgs.evaluation` |
| 业务域 | agent、indicator、testcase、scheme、task、execution、scoring、report、measurement、invocation、aijudge、common |
| 接口风格 | REST + JSON（ApiResponse 统一包装），无消息队列、无注册中心、无网关 |

### 二、技术栈总览

| 类别 | 框架 | 版本 | 说明 |
|------|------|------|------|
| 基础框架 | Spring Boot (spring-boot-starter) | 3.5.16 | 主框架 |
| Web | Spring MVC (spring-boot-starter-web) | 3.5.16 | 同步 REST 接口（10 个 Controller） |
| Web | Spring WebFlux (spring-boot-starter-webflux) | 3.5.16 | 出站 HTTP 调用（WebClient 调用 Agent / Dify AI 判分） |
| ORM | MyBatis-Plus (`mybatis-plus-spring-boot3-starter` + `mybatis-plus-jsqlparser`) | 3.5.17 | MybatisPlusConfig 注册 PaginationInnerInterceptor(DbType.MYSQL) |
| 数据库 | MySQL（`mysql-connector-j`，runtime） | 由 Spring Boot 3.5 BOM 管理 | dev 环境 `jdbc:mysql://localhost:3306/agent_evaluation` |
| 校验 | Hibernate Validator (spring-boot-starter-validation) | 3.5.16 | @NotBlank/@NotNull/@Positive/@Size/@Pattern/@DecimalMin/@DecimalMax |
| API 文档 | springdoc-openapi-starter-webmvc-ui | 2.8.17 | OpenApiConfig 按模块分 7 组（agents/indicators/test-cases/schemes/tasks/results） |
| Excel | Apache POI (poi-ooxml) | 5.2.5 | 测试用例 Excel 导入与模板生成 |
| JSON | Jackson（内置）+ json-path（com.jayway.jsonpath） | 由 Boot BOM 管理 | 请求模板渲染、响应字段提取 |
| 监控 | 无 | - | 未引入 actuator/micrometer 依赖 |
| 缓存 | 无 | - | 未引入 Redis/Caffeine/Ehcache（pom 无缓存依赖） |
| 消息队列 | 无 | - | 未引入 MQ 依赖 |
| 微服务 | 无 | - | 无 Spring Cloud/Eureka/Nacos 依赖，单服务 |
| 安全/认证 | 无 | - | 无 spring-security/shiro/sa-token/jwt 依赖 |
| 测试 | spring-boot-starter-test + H2 + ArchUnit | 1.4.1 (ArchUnit) | 单元测试 74 个 Java 文件；ArchUnit 校验六边形架构约束 |
| 工具库 | Lombok | 由 Boot BOM 管理 | 少量使用 |

### 三、关键配置

| 配置项 | 值 | 来源 |
|--------|-----|------|
| server.port | 8080 | application.yml |
| spring.profiles.default | dev（无 `spring.profiles.active` 显式设置，默认启用 dev） | application.yml |
| spring.datasource.url | `jdbc:mysql://localhost:3306/agent_evaluation?useUnicode=true&characterEncoding=utf8&serverTimezone=Asia/Shanghai`（local 环境由 `DB_URL` 环境变量注入） | application-dev.yml / application-local.yml |
| spring.datasource.username | `root`（local：`DB_USERNAME`） | application-dev.yml / application-local.yml |
| spring.datasource.password | `******`（脱敏；dev 为明文，local 由 `DB_PASSWORD` 注入） | application-dev.yml / application-local.yml |
| spring.datasource.driver-class-name | com.mysql.cj.jdbc.Driver | application-dev.yml |
| spring.redis.host | 无（未配置 Redis） | - |
| spring.jackson.date-format | `yyyy-MM-dd'T'HH:mm:ssXXX`（时间序列化为 ISO 字符串，非时间戳） | application.yml |
| mybatis-plus.configuration.map-underscore-to-camel-case | true | application.yml |
| springdoc.swagger-ui.path | /swagger-ui.html | application.yml |
| springdoc.api-docs.path | /v3/api-docs | application.yml |
| evaluation.ai-judge.enabled | true（默认 `${DIFY_AI_JUDGE_ENABLED:true}`） | application.yml / application-dev.yml |
| evaluation.ai-judge.provider | DIFY_WORKFLOW | application.yml |
| evaluation.ai-judge.dify.base-url | `http://180.76.180.32/v1`（dev 明文；生产建议环境变量 `DIFY_AI_JUDGE_BASE_URL` 覆盖） | application-dev.yml |
| evaluation.ai-judge.dify.api-key | `******`（脱敏；dev 明文 `app-*****`，可被 `DIFY_AI_JUDGE_API_KEY` 覆盖） | application-dev.yml |
| evaluation.ai-judge.dify.timeout | 30s | application.yml |
| evaluation.ai-judge.dify.model-name | Qwen/Qwen2.5-72B-Instruct | application.yml |
| evaluation.ai-judge.dify.allow-insecure-http | true | application.yml |
| evaluation.test-case-import.* | default-case-type=SINGLE_TURN、default-version=1.0.0、default-weight=1.0、default-pass-score=60、default-combine-mode=ALL、default-rule-type=AI_SEMANTIC_SCORE | application-dev.yml（TestCaseImportProperties 绑定） |

### 四、建议与注意事项

#### 框架版本提示
- Spring Boot 3.5.16 为较新维护版本（Spring Framework 6.2 系），无已知高危 CVE 必须升级项；建议保持跟随 Patch 版本更新。
- springdoc-openapi 2.8.17 与 Boot 3.5.x 兼容良好；若后续升级 Boot 大版本，需同步升级 springdoc（其版本与 Boot 3.x 严格绑定）。
- MyBatis-Plus 3.5.17 与 Boot 3.5.x 匹配（使用 `mybatis-plus-spring-boot3-starter` 而非旧版 starter），注意 3.5.9+ 起 `mybatis-plus-jsqlparser` 拆分为独立依赖，本项目已引入，无兼容问题。
- 同时引入 `spring-boot-starter-web` 与 `spring-boot-starter-webflux`：会触发 Spring Boot 对 WebMVC/WebFlux 的自动配置互斥处理（实测项目可正常启动）。建议仅在需要 WebClient 时保留 webflux，避免引入不必要的响应式自动配置与类路径歧义；可考虑把 WebClient 相关代码收敛到 invocation 模块。

#### 其他
- **无认证机制**：pom 无任何安全依赖、代码无 SecurityConfig/Filter/Interceptor（详见 auth-analysis.md），所有接口公开可访问。
- **dev 配置含敏感信息**：`application-dev.yml` 中数据库口令（root/root）与 Dify API Key（app-QFrABtRHsV0gRHv2Mx4R98bg）均为明文；建议通过环境变量注入并在测试环境替换。
- 默认 profile 为 dev 且数据源指向本机 MySQL `agent_evaluation`，测试前需确认数据库已初始化（`db/` 目录下有建库脚本）。
- 时间格式为 `yyyy-MM-dd'T'HH:mm:ssXXX`（带时区 ISO8601），LocalDateTime 序列化输出无时区后缀；Instant 字段序列化为带时区格式——测试断言注意区分。
- 分页参数 page/pageSize 以 String 接收并手工解析（非 Spring 自动绑定），非法值统一报 400 COMMON_400_VALIDATION，pageSize 上限 100。
