---
name: framework-analyzer
description: 从 config.yaml 读取后端项目路径，解析 pom.xml 识别技术框架，深度分析认证机制（Shiro/Spring Security/自定义拦截器/WebConfig），提取必填请求头和字段，输出框架分析报告到 02-analysis-plan。触发：/framework-analyzer、分析框架、分析pom、分析认证机制、分析项目用了什么框架、分析技术栈。
---

# 框架分析器

解析 pom.xml 识别技术栈，深度分析认证机制，输出 Markdown 分析报告。

## 执行流程

### 1. 读取配置

读取 `config.yaml`，提取 `source.backend[]` 中 `enabled: true` 的项目路径列表。

### 2. pom.xml 依赖分析

对每个项目路径：
1. 读取项目根目录的 `pom.xml`
2. 检测是否为多模块项目（`<modules>` 标签），若是则递归读取子模块 `pom.xml`
3. 提取所有 `<dependency>`，按 `references/pom-analysis.md` 中的分类规则归类
4. 提取 Spring Boot 版本（从 `<parent>` 中的 `spring-boot-starter-parent`）

### 3. 认证机制分析（核心）

对每个项目，按以下步骤层层下钻：

#### 3.1 pom 层初判

根据 pom.xml 依赖快速判断认证体系，详见 `references/auth-detection.md`。

#### 3.2 代码特征搜索

对每个项目目录，**并行**执行以下 Grep 搜索（均为 `files_with_matches` 模式）：

| 搜索内容 | 目标 |
|---------|------|
| `SecurityFilterChain\|@EnableWebSecurity\|WebSecurityConfigurerAdapter` | Spring Security |
| `ShiroFilterFactoryBean\|AuthorizingRealm` | Apache Shiro |
| `SaTokenConfig\|StpLogic\|@SaCheckLogin` | Sa-Token |
| `extends OncePerRequestFilter\|implements Filter.*\{` | 自定义 Filter |
| `implements HandlerInterceptor` | 自定义拦截器 |
| `addInterceptors` | WebMvcConfigurer 配置 |
| `@WebFilter` | Servlet Filter 注册 |
| `Jwts\|JJWT\|TokenProvider\|TokenService` | JWT 令牌 |
| `@EnableOAuth2Sso\|spring-security-oauth2` | OAuth2 |
| `@PreAuthorize\|@PostAuthorize\|@Secured` | 方法级权限注解 |
| `getHeader\(` | 请求头读取 |

#### 3.3 认证组件源码分析

对 3.2 搜索结果中的关键文件，用 `codegraph_explore` 批量读取源码（1-2 次调用），提取：

- **必填请求头**：所有 `request.getHeader("...")` → 头名称、是否可空、用途
- **Token 来源**：Header（`Authorization: Bearer xxx`）/ Cookie（`JSESSIONID`）/ 请求参数
- **登录接口**：`/login`、`/auth/login` 等 → 请求方法、请求体字段、必填项
- **拦截路径**：`addInterceptors()` / `addPathPatterns()` → 被拦截的 URL 模式
- **白名单路径**：`excludePathPatterns()` → 免认证 URL

**注意**：若 Grep 未搜索到任何认证特征 → 项目无认证机制，报告中标注 `type: none`。

#### 3.4 认证流程描述

基于源码分析结果，用文字描述请求经过的 Filter → Interceptor → Controller 链条顺序，标注每层的认证动作。

### 4. 关键配置提取

对每个项目，搜索 `application.yml` / `application.properties` / `application-{env}.yml`，提取：
- `server.port` — 服务端口
- `spring.datasource.*` — 数据库连接（脱敏：隐藏密码）
- `spring.redis.*` — Redis 配置（脱敏）
- `spring.profiles.active` — 当前 profile
- 认证相关自定义配置（如 `jwt.secret`、`token.expire` 等）

### 5. 输出报告（拆分为两个文件）

按 `references/output-format.md` 模板，输出两个独立文件：

#### 文件 1：框架分析报告

```
tests/baseline/_workflow/02-analysis-plan/framework-analysis.md
```

内容：项目概览 + 技术栈总览（pom 依赖分类矩阵）+ 关键配置 + 框架版本建议。

#### 文件 2：认证机制分析报告

```
tests/baseline/_workflow/02-analysis-plan/auth-analysis.md
```

内容：认证方式 + 请求头要求 + 登录接口 + 拦截器/过滤器链 + 权限模型 + 白名单路径。

**无论是否有认证机制，都必须输出此文件。** 无认证时，认证类型标注 `none`，各章节写明"无"，并在建议中说明"该项目无认证机制，所有接口公开访问"。

两个文件均按项目分开填写，多项目时共享同一文件、按 `## 项目：{name}` 分隔。

### 6. 建议与注意事项

分析完成后，基于发现给出建议，写入对应报告：

- **框架分析报告**：框架版本冲突、已知漏洞版本、依赖升级建议
- **认证分析报告**：测试建议（是否需要先登录获取 token、token 过期时间）、安全风险（无认证、硬编码密钥、Token 无过期）、必填字段清单

## 参考文档

| 文件 | 内容 |
|------|------|
| `references/pom-analysis.md` | pom.xml 依赖分类规则 |
| `references/auth-detection.md` | 认证机制检测特征表与搜索模式 |
| `references/output-format.md` | 分析报告 Markdown 模板 |
