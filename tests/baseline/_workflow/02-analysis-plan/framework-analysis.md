# 框架分析报告

**生成时间**: 2026-07-10
**分析项目数**: 1

---

## 项目：spring-petclinic

### 一、基本信息

| 属性 | 值 |
|------|-----|
| 项目路径 | `D:\java\project\spring-petclinic` |
| Spring Boot | 4.1.0 |
| Java | 17 |
| 项目类型 | 单模块 |
| 构建工具 | Maven |

### 二、技术栈总览

| 类别 | 框架 | 版本 | 说明 |
|------|------|------|------|
| 基础框架 | Spring MVC (WebMVC) | 继承自父 pom | `spring-boot-starter-webmvc` |
| 基础框架 | Spring Boot Actuator | 继承自父 pom | 监控端点 |
| ORM | Spring Data JPA | 继承自父 pom | JPA + Hibernate |
| 数据库 | H2 | 继承自父 pom | 默认数据库，内存模式，重启后数据重置 |
| 数据库 | MySQL Connector | 继承自父 pom | `runtime` scope |
| 数据库 | PostgreSQL Driver | 继承自父 pom | `runtime` scope |
| 缓存 | Spring Cache | 继承自父 pom | 缓存抽象层 |
| 缓存 | Caffeine | 继承自父 pom | 本地缓存，`runtime` scope |
| 缓存 | JCache API | 继承自父 pom | `javax.cache:cache-api` |
| 校验 | Bean Validation | 继承自父 pom | JSR-380 校验 |
| 模板引擎 | Thymeleaf | 继承自父 pom | 服务端模板 |
| 工具库 | WebJars Locator | 1.1.3 | 静态资源版本管理 |
| 工具库 | Bootstrap (WebJars) | 5.3.8 | 前端 UI 框架 |
| 工具库 | Font Awesome (WebJars) | 4.7.0 | 图标库 |
| 测试 | Spring Boot Test Starters | 继承自父 pom | webmvc-test, data-jpa-test, actuator-test 等 |
| 测试 | Testcontainers | 继承自父 pom | 集成测试容器（MySQL） |
| DevTools | spring-boot-devtools | 继承自父 pom | 热重载（optional） |

> 未使用类别：安全/认证、消息队列、RPC/HTTP 客户端、微服务/注册中心、调度/异步。

### 三、关键配置

| 配置项 | 值 | 来源 |
|--------|-----|------|
| server.port | 8080（默认值，未显式配置） | 未配置 |
| spring.datasource (default) | H2 内存数据库 | application.properties |
| spring.datasource (mysql) | `jdbc:mysql://localhost/petclinic`（通过 `${MYSQL_URL}` 环境变量覆盖） | application-mysql.properties |
| spring.datasource (postgres) | `jdbc:postgresql://localhost/petclinic`（通过 `${POSTGRES_URL}` 环境变量覆盖） | application-postgres.properties |
| spring.profiles.active | 未显式设置（使用默认 profile = H2） | application.properties |
| spring.jpa.ddl-auto | none | application.properties |
| management.endpoints.web.exposure.include | *（所有 Actuator 端点公开） | application.properties |
| spring.cache | Caffeine（通过 classpath 自动检测） | 自动配置 |

### 四、建议与注意事项

#### 框架版本提示
- Spring Boot 4.1.0 为较新版本，兼容性良好，无明显已知漏洞。
- Java 17 为 LTS 版本，持续受支持。

#### 其他
- 默认使用 H2 内存数据库，重启后所有数据重置。如需持久化，切换至 MySQL 或 PostgreSQL profile（`--spring.profiles.active=mysql`）。
- Actuator 所有端点已公开（`management.endpoints.web.exposure.include=*`），生产环境应限制为仅健康检查。
- 项目无任何认证/安全框架依赖，所有接口公开访问（详见认证机制分析报告）。
