# 框架分析报告

**生成时间**: 2026-07-14
**分析项目数**: 1

---

## 项目：RuoYi-Vue-Plus

### 一、基本信息

| 属性 | 值 |
|------|-----|
| 项目路径 | `D:/java/project/RuoYi-Vue-Plus` |
| Spring Boot | 3.5.15 |
| Java | 21 |
| 项目类型 | 多模块（4 个顶级模块，24 个 common 子模块） |
| 构建工具 | Maven |
| 版本号 | 5.6.2 |

**模块结构**：
- `ruoyi-admin` — 主应用入口（8080端口）
- `ruoyi-common` — 24 个通用子模块（core、web、security、satoken、redis、mybatis、encrypt 等）
- `ruoyi-extend` — 扩展模块（monitor-admin、snailjob-server）
- `ruoyi-modules` — 业务模块（system、generator、demo、job、workflow）

### 二、技术栈总览

| 类别 | 框架 | 版本 | 说明 |
|------|------|------|------|
| 基础框架 | Spring Boot | 3.5.15 | 继承自 spring-boot-dependencies |
| 基础框架 | Spring MVC (WebMVC) | — | spring-boot-starter-web |
| 安全/认证 | Sa-Token | 1.45.0 | sa-token-spring-boot3-starter |
| 安全/认证 | Sa-Token JWT | 1.45.0 | sa-token-jwt（简单模式） |
| ORM | MyBatis-Plus | 3.5.16 | mybatis-plus-spring-boot3-starter |
| ORM | MyBatis | 3.5.19 | 底层 ORM |
| 数据库 | MySQL Connector | — | mysql-connector-j |
| 连接池 | HikariCP + Druid | — | dynamic-datasource 多数据源 |
| SQL 分析 | p6spy | 3.9.1 | SQL 性能分析 |
| 缓存 | Spring Data Redis | — | Redis 客户端 |
| 缓存 | Redisson | 3.52.0 | 分布式锁/缓存 |
| 缓存 | Caffeine | — | 本地缓存（Sa-Token 二级缓存） |
| 校验 | Hibernate Validator | — | JSR-380 Bean Validation |
| 工具库 | Lombok | 1.18.44 | 代码生成 |
| 工具库 | Hutool | 5.8.43 | Java 工具集 |
| 工具库 | MapStruct Plus | 1.5.0 | 对象映射 |
| 工具库 | Fastjson | 1.2.83 | JSON 序列化 |
| 模板引擎 | Apache Velocity | 2.3 | 代码生成模板 |
| 监控 | Spring Boot Admin | 3.5.8 | 客户端 + 服务端 |
| API 文档 | SpringDoc OpenAPI | 2.8.17 | Swagger 3 / OpenAPI 3 |
| 任务调度 | SnailJob | 1.10.0 | 分布式任务调度 |
| 分布式锁 | Lock4j | 2.2.7 | 基于 Redisson |
| 工作流 | Warm-Flow | 1.8.5 | 国产工作流引擎 |
| 对象存储 | AWS SDK 2.x | 2.28.22 | S3 对象存储 |
| 短信 | SMS4J | 3.3.5 | 多厂商短信 |
| 社交登录 | JustAuth | 1.16.7 | 第三方登录集成 |
| 加密 | BouncyCastle | 1.83 | 加密算法库 |
| Excel | FastExcel | 1.3.0 | Excel 导入导出 |
| IP 定位 | ip2region | 3.3.7 | 离线 IP 地址定位 |

> 未使用的类别：消息队列（RocketMQ/Kafka/RabbitMQ 未引入）、RPC 框架（Dubbo 未引入）。

### 三、关键配置

| 配置项 | 值 | 来源 |
|--------|-----|------|
| server.port | 8080 | application.yml |
| spring.profiles.active | dev（默认） | pom.xml profiles |
| spring.datasource.url | jdbc:mysql://180.76.180.32:3306/ry-vue | application-dev.yml |
| spring.datasource.username | root | application-dev.yml |
| spring.datasource.password | \*\*\*\*\*\*\* | application-dev.yml（已脱敏） |
| spring.data.redis.host | 180.76.180.32 | application-dev.yml |
| spring.data.redis.port | 6379 | application-dev.yml |
| spring.data.redis.password | \*\*\*\*\*\* | application-dev.yml（已脱敏） |
| sa-token.token-name | Authorization | application.yml |
| sa-token.token-prefix | Bearer | common-satoken.yml |
| sa-token.jwt-secret-key | \*\*\*\*\*\*\*\*\*\* | application.yml（已脱敏） |
| captcha.enable | false | application.yml |
| tenant.enable | true | application.yml |
| xss.enabled | true | application.yml |
| api-decrypt.enabled | false | application.yml |
| mybatis-encryptor.enable | false | application.yml |
| spring.boot.admin.client.url | http://localhost:9090/admin | application-dev.yml |
| snail-job.server.host | 127.0.0.1:17888 | application-dev.yml |

### 四、建议与注意事项

#### 框架版本提示
- Spring Boot 3.5.15 为当前较新版本，生态兼容性良好。
- Sa-Token 1.45.0 为稳定版本，与 Spring Boot 3.x 兼容。
- Fastjson 版本 1.2.83 较旧且存在已知安全漏洞，建议评估是否可迁移至 Fastjson2 或 Jackson。
- 项目通过 `sa-token-jwt` 使用简单模式 JWT，密钥硬编码在 application.yml 中（`jwt-secret-key: abcdefghijklmnopqrstuvwxyz`），**强烈建议生产环境更换为安全的随机密钥并通过环境变量注入**。

#### 其他
- 多租户功能已开启（`tenant.enable: true`），数据隔离通过 MyBatis-Plus 拦截器实现。
- 验证码默认关闭（`captcha.enable: false`），登录接口无需验证码。
- 接口加密默认关闭（`api-decrypt.enabled: false`），但登录接口通过 `@ApiEncrypt` 注解独立开启了请求体加密。
- XSS 过滤默认开启，排除路径包括 `/system/notice` 和 `/warm-flow/save-json`。
- 项目使用虚拟线程（JDK 21 特性），当前关闭（`spring.threads.virtual.enabled: false`）。
