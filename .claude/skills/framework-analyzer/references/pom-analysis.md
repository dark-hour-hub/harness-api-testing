# pom.xml 依赖分类规则

## 分类映射表

解析 `<dependency>` 时，按 `groupId:artifactId` 前缀匹配以下分类。

### 基础框架

| 依赖特征 | 框架名 | 说明 |
|---------|--------|------|
| `spring-boot-starter-webmvc` | Spring MVC (WebMVC) | 同步 Web 框架 |
| `spring-boot-starter-webflux` | Spring WebFlux | 响应式 Web 框架 |
| `spring-boot-starter` | Spring Boot | 基础 starter |
| `spring-boot-starter-web` | Spring MVC | 旧版命名（含 webmvc） |

### 安全/认证

| 依赖特征 | 框架名 | 说明 |
|---------|--------|------|
| `spring-boot-starter-security` | Spring Security | 安全框架 |
| `spring-security-oauth2` | Spring Security OAuth2 | OAuth2 支持 |
| `spring-security-cas` | Spring Security CAS | CAS 单点登录 |
| `shiro-spring` | Apache Shiro | 安全框架 |
| `shiro-core` | Apache Shiro Core | Shiro 核心 |
| `sa-token-spring-boot-starter` | Sa-Token | 轻量认证框架 |
| `sa-token-reactor-spring-boot-starter` | Sa-Token (WebFlux) | 响应式支持 |
| `jjwt` | JJWT | JWT 生成/解析 |
| `java-jwt` | java-jwt (Auth0) | JWT 库 |
| `nimbus-jose-jwt` | Nimbus JOSE+JWT | JWT/OAuth2 库 |

### ORM / 数据库

| 依赖特征 | 框架名 | 说明 |
|---------|--------|------|
| `spring-boot-starter-data-jpa` | Spring Data JPA | JPA + Hibernate |
| `mybatis-spring-boot-starter` | MyBatis | ORM 框架 |
| `mybatis-plus-boot-starter` | MyBatis-Plus | MyBatis 增强 |
| `mysql-connector-j` | MySQL Connector | MySQL 驱动 |
| `postgresql` | PostgreSQL Driver | PG 驱动 |
| `h2` | H2 Database | 内存数据库 |
| `druid-spring-boot-starter` | Druid | 连接池 |

### 缓存

| 依赖特征 | 框架名 | 说明 |
|---------|--------|------|
| `spring-boot-starter-cache` | Spring Cache | 缓存抽象 |
| `spring-boot-starter-data-redis` | Spring Data Redis | Redis 客户端 |
| `redisson` | Redisson | Redis 分布式客户端 |
| `caffeine` | Caffeine | 本地缓存 |
| `ehcache` | Ehcache | 本地缓存 |

### 消息队列

| 依赖特征 | 框架名 | 说明 |
|---------|--------|------|
| `rocketmq-spring-boot-starter` | RocketMQ | 阿里 MQ |
| `spring-kafka` | Kafka | 消息队列 |
| `spring-boot-starter-amqp` | RabbitMQ | 消息队列 |

### RPC / HTTP 客户端

| 依赖特征 | 框架名 | 说明 |
|---------|--------|------|
| `dubbo-spring-boot-starter` | Apache Dubbo | RPC 框架 |
| `spring-cloud-starter-openfeign` | OpenFeign | HTTP 客户端 |
| `spring-boot-starter-web-services` | Spring Web Services | SOAP 服务 |

### 校验

| 依赖特征 | 框架名 | 说明 |
|---------|--------|------|
| `spring-boot-starter-validation` | Bean Validation | JSR-380 校验 |
| `hibernate-validator` | Hibernate Validator | 校验实现 |

### 工具库

| 依赖特征 | 框架名 | 说明 |
|---------|--------|------|
| `lombok` | Lombok | 代码生成 |
| `hutool-all` | Hutool | 工具集 |
| `guava` | Guava | Google 工具库 |
| `mapstruct` | MapStruct | 对象映射 |
| `commons-lang3` | Commons Lang3 | Apache 工具库 |
| `jackson` | Jackson | JSON 序列化 |
| `fastjson` | Fastjson | JSON 序列化 |
| `gson` | Gson | JSON 序列化 |

### 微服务/注册中心

| 依赖特征 | 框架名 | 说明 |
|---------|--------|------|
| `spring-cloud-starter-gateway` | Spring Cloud Gateway | 网关 |
| `spring-cloud-starter-netflix-eureka-client` | Eureka Client | 注册中心 |
| `spring-cloud-starter-alibaba-nacos-discovery` | Nacos | 注册/配置中心 |
| `spring-cloud-starter-alibaba-nacos-config` | Nacos Config | 配置中心 |
| `spring-cloud-starter-sentinel` | Sentinel | 流量控制 |

### 模板引擎

| 依赖特征 | 框架名 | 说明 |
|---------|--------|------|
| `spring-boot-starter-thymeleaf` | Thymeleaf | 服务端模板 |
| `spring-boot-starter-freemarker` | FreeMarker | 服务端模板 |

### 调度/异步

| 依赖特征 | 框架名 | 说明 |
|---------|--------|------|
| `spring-boot-starter-quartz` | Quartz | 任务调度 |
| `xxl-job-core` | XXL-Job | 分布式调度 |

## 分类优先级

一个依赖匹配多个分类时取第一个匹配（如 `spring-boot-starter-data-redis` 优先匹配缓存类而非通用 data 类）。

## 版本提取规则

- **Spring Boot 版本**：从 `<parent>` → `spring-boot-starter-parent` 的 `<version>` 提取
- **Java 版本**：从 `<properties>` → `<java.version>` 提取
- **其他依赖版本**：从自身 `<version>` 或父 pom `<dependencyManagement>` 推断（标注为 "继承自父 pom"）
