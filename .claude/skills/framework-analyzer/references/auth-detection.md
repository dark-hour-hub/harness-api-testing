# 认证机制检测特征表

## 1. pom 层快速判断

| pom 中有 | 认证体系 | 后续搜索重点 |
|---------|---------|-------------|
| `spring-boot-starter-security` | Spring Security | `SecurityFilterChain`、`@EnableWebSecurity` |
| `shiro-spring` / `shiro-core` | Apache Shiro | `ShiroFilterFactoryBean`、`AuthorizingRealm` |
| `sa-token-*` | Sa-Token | `SaTokenConfig`、`StpLogic` |
| `jjwt` / `java-jwt` 但无上述框架 | 自研 JWT | 自定义 Filter/Interceptor 中的 JWT 解析 |
| 以上均无 | 无认证 或 纯自定义拦截器 | `implements HandlerInterceptor`、`extends Filter` |

## 2. 代码特征搜索模式

### Spring Security 体系

**搜索目标文件**（Grep `files_with_matches`）：
```
SecurityFilterChain
@EnableWebSecurity
@EnableGlobalMethodSecurity
WebSecurityConfigurerAdapter
@PreAuthorize
@PostAuthorize
```

**深入分析**（用 `codegraph_explore` 批量读取 SecurityConfig 类）：
- `SecurityFilterChain` Bean 定义 → 路径拦截规则、放行白名单
- `AuthenticationManager` / `AuthenticationProvider` → 认证逻辑
- `UserDetailsService` 实现 → 用户加载方式
- `PasswordEncoder` → 密码加密方式
- `@PreAuthorize("hasRole('xxx')")` / `@PreAuthorize("hasAuthority('xxx')")` → 权限粒度

**Token 提取**：
- `OncePerRequestFilter` 子类 → `request.getHeader("Authorization")`
- `SecurityContextHolder` 使用方式
- Token 生成位置（登录成功 handler）

### Shiro 体系

**搜索目标文件**：
```
ShiroFilterFactoryBean
AuthorizingRealm
@RequiresPermissions
@RequiresRoles
@RequiresAuthentication
```

**深入分析**：
- `ShiroFilterFactoryBean` → `setFilterChainDefinitionMap()` → URL 权限映射
- `AuthorizingRealm` 子类 → `doGetAuthenticationInfo()` + `doGetAuthorizationInfo()`
- `SessionManager` → Session 管理方式
- 登录接口中 `Subject.login()` 调用

**Token 提取**：
- `SecurityUtils.getSubject().getSession().getAttribute(...)`
- ShiroFilter 中 `request.getHeader(...)` 位置

### Sa-Token 体系

**搜索目标文件**：
```
SaTokenConfig
StpLogic
@SaCheckLogin
@SaCheckPermission
@SaCheckRole
```

**深入分析**：
- `SaTokenConfig` → token 名称、超时时间、是否从 cookie 读取
- 登录接口中 `StpUtil.login()` 调用
- `StpUtil.getTokenInfo()` 使用方式

### 自定义拦截器

**搜索目标文件**：
```
implements HandlerInterceptor
addInterceptors\(
WebMvcConfigurer
```

**深入分析**：
- `preHandle()` → 拦截逻辑、从何处提取认证信息
- `addPathPatterns()` → 拦截哪些 URL
- `excludePathPatterns()` → 白名单 URL
- `registry.addInterceptor()` → 拦截器注册顺序

### 自定义 Filter

**搜索目标文件**：
```
extends OncePerRequestFilter
implements Filter
@WebFilter
implements javax\.servlet\.Filter
```

**深入分析**：
- `doFilter()` / `doFilterInternal()` → 过滤逻辑
- `request.getHeader(...)` → 提取哪些请求头
- `@WebFilter(urlPatterns = ...)` → 过滤哪些 URL
- `FilterRegistrationBean` → 注册配置

## 3. 请求头/必填字段提取

对每个认证相关文件，定位以下模式：

| 模式 | 含义 |
|------|------|
| `request.getHeader("Xxx")` | 从请求头读取 "Xxx" |
| `request.getParameter("Xxx")` | 从请求参数读取 "Xxx" |
| `request.getCookies()` | 从 Cookie 读取 |
| `SecurityUtils.getSubject().getSession()` | Shiro Session 读取 |
| `SecurityContextHolder.getContext().getAuthentication()` | Spring Security 上下文 |
| `StpUtil.getLoginId()` | Sa-Token 登录 ID |

**判断必填性**：
- 读取后直接判空并抛出异常/返回错误 → **必填**
- 读取后有默认值或 null 检查后跳过 → **可选**
- 仅在某些路径下判空（如 `/admin/**`）→ **条件必填**，记录路径条件

## 4. 白名单提取

收集所有免认证路径：

| 来源 | 提取方式 |
|------|---------|
| Spring Security | `SecurityFilterChain` 中 `requestMatchers(...).permitAll()` |
| Shiro | `ShiroFilterFactoryBean.setFilterChainDefinitionMap()` 中的 `anon` |
| 自定义拦截器 | `excludePathPatterns()` |
| 自定义 Filter | `shouldNotFilter()` 方法（Spring Security）/ `@WebFilter(urlPatterns=...)` 未覆盖的路径 |

常见白名单：`/login`, `/captcha`, `/swagger-ui/**`, `/v3/api-docs/**`, `/druid/**`, `/actuator/health`, `/static/**`

## 5. 认证流程追踪

用 `codegraph_trace` 追踪关键路径：

```
# 从 Controller 追溯到认证检查点
codegraph_trace from="<LoginController>" to="<filterChain>"

# 从 token 生成追溯到存储
codegraph_trace from="<TokenService>" to="<RedisCache>"
```

## 6. 分析检查清单

- [ ] 认证框架识别正确（对照 pom 依赖 + 代码特征双重确认）
- [ ] 所有 `request.getHeader()` 调用已提取，必填/可选已标注
- [ ] Token 来源（Header/Cookie/Parameter）已确认
- [ ] Token 前缀（如 `Bearer `）已从源码提取
- [ ] 登录接口路径、方法、请求体字段已提取
- [ ] 白名单路径已完整列出
- [ ] 权限注解（`@PreAuthorize` / `@RequiresPermissions` 等）已扫描
- [ ] Filter/Interceptor 链条顺序已描述
