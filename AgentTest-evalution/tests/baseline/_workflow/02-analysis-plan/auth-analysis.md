# 认证机制分析报告

**生成时间**: 2026-08-19
**分析项目数**: 1

---

## 项目：agent-evaluation-platform-backend

### 一、认证方式

| 属性 | 值 |
|------|-----|
| 认证类型 | `none` |
| 认证描述 | 该项目无任何认证机制，所有接口均公开访问。pom 无 spring-security/shiro/sa-token/jjwt 依赖；代码 Grep 全量扫描未命中 `SecurityFilterChain`、`@EnableWebSecurity`、`ShiroFilterFactoryBean`、`AuthorizingRealm`、`StpUtil`、`@SaCheckLogin`、`Jwts`、`TokenProvider`、`TokenService`、`HandlerInterceptor`、`addInterceptors`、`@PreAuthorize` 等任何认证特征；Controller 上无权限注解。唯一 Filter 为链路追踪用途的 TraceIdFilter，与认证无关。 |

### 二、请求头要求

| 请求头名称 | 是否必填 | 条件 | 用途 |
|-----------|---------|------|------|
| X-Trace-Id | 否（可选） | 任意路径 | 链路追踪 ID：TraceIdFilter 读取后写入 MDC（key=traceId）并回写响应头；缺失/空白时自动生成 32 位小写十六进制 UUID，因此永远不会因此报错 |

> 无认证相关请求头。所有接口不需要任何认证请求头即可访问。

### 三、登录接口

| 属性 | 值 |
|------|-----|
| 接口路径 | 无 |
| 请求体格式 | - |

> 该项目无登录接口。（已全量扫描所有 Controller 路由清单，无 /login、/auth/** 相关端点。）

### 四、拦截器/过滤器链

请求链路（按顺序）：

```
1. TraceIdFilter (jakarta.servlet Filter，继承 OncePerRequestFilter)
   类型: Filter（@Component 注册 + @Order(Ordered.HIGHEST_PRECEDENCE)，全局最高优先级）
   路径: 所有路径（无 urlPatterns 限制，@WebFilter 未使用，通过 @Component 扫描注册）
   排除: 无
   动作: 读取请求头 X-Trace-Id（可选）→ 缺失则生成 UUID（去掉连字符）→ 写入 MDC(traceId) → 设置响应头 X-Trace-Id → 放行 → finally 清理 MDC（与认证无关，纯链路追踪）
   必填头: []
   可选头: [X-Trace-Id]
```

> 无认证 Filter/HandlerInterceptor；无 WebMvcConfigurer 注册任何拦截器；无其他 Filter。

### 五、权限模型

| 属性 | 值 |
|------|-----|
| 权限注解 | 无 |
| 权限粒度 | 无 |
| 说明 | 无 |

> 无。所有接口无角色/权限控制。

### 六、白名单路径

| 路径 | 说明 |
|------|------|
| 不适用 | 无认证机制，无白名单概念。 |

> 补充说明：springdoc 配置的 `/swagger-ui.html`、`/v3/api-docs` 为文档端点，因无认证同样公开访问。

### 七、建议与注意事项

#### 测试建议
- 所有接口可直接请求，无需登录/token 获取流程，测试前置依赖为零。
- 可选：在请求头携带自定义 `X-Trace-Id`（如 `test-<用例ID>`），可断言响应头 `X-Trace-Id` 与响应体 `traceId` 与请求一致（TraceIdFilter 会原样透传）；未携带时响应体 traceId 为服务端生成的 32 位十六进制串，可在断言中断言非空而非固定值。
- 反向用例断言应校验 HTTP 状态码 + 响应体 `code` 字段（如 400 + COMMON_400_VALIDATION），而非依赖 message 文本。

#### 安全提示
- **无认证机制，所有接口可直接访问**：包括评测方案创建/发布、任务创建/执行（会真实调用外部 Agent 并消耗资源）、测量值确认等写操作，存在数据篡改与资源滥用风险。
- **无登录、无鉴权、无租户隔离**：多用户/多环境共用一个后端时无法区分操作者；`createdBy`/`submittedBy` 等字段为前端可信传入，无服务端身份校验。
- **dev 配置明文敏感信息**：`application-dev.yml` 含数据库口令（root/root）与 Dify API Key，如部署环境沿用该 profile 存在泄露风险，建议环境变量覆盖并轮换密钥。
- **X-Trace-Id 无长度/字符限制**：用户可注入超长或任意字符的请求头回写响应头，虽无直接注入风险（Spring 会过滤 CRLF），但建议后续增加长度限制。
