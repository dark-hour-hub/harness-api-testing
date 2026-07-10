# 分析报告 Markdown 模板

输出两个独立文件。多项目时每个项目一个独立章节、共享同一文件。

---

## 文件 1：框架分析报告

**路径**：`tests/baseline/_workflow/02-analysis-plan/framework-analysis.md`

```markdown
# 框架分析报告

**生成时间**: {YYYY-MM-DD}
**分析项目数**: {N}

---

## 项目：{project-name}

### 一、基本信息

| 属性 | 值 |
|------|-----|
| 项目路径 | `{path}` |
| Spring Boot | {version} |
| Java | {version} |
| 项目类型 | 单模块 / 多模块（{N} 个子模块） |
| 构建工具 | Maven |

### 二、技术栈总览

| 类别 | 框架 | 版本 | 说明 |
|------|------|------|------|
| 基础框架 | {framework} | {version} | {note} |
| ORM | ... | ... | ... |
| 数据库 | ... | ... | ... |
| 缓存 | ... | ... | ... |
| 校验 | ... | ... | ... |
| 工具库 | ... | ... | ... |
| 模板引擎 | ... | ... | ... |
| 监控 | ... | ... | ... |
| 测试 | ... | ... | ... |

> 只列出实际使用的类别行，未使用的类别不展示。在末尾加一行列出未使用的类别。

### 三、关键配置

| 配置项 | 值 | 来源 |
|--------|-----|------|
| server.port | {port} | application.yml |
| spring.datasource.url | {url（密码脱敏）} | application.yml |
| spring.redis.host | {host} | application.yml |
| spring.profiles.active | {profile} | application.yml |
| ... | ... | ... |

### 四、建议与注意事项

#### 框架版本提示
- {如：Spring Boot 版本较低，建议升级}
- {如：依赖 A 版本 x.x.x 与依赖 B 版本 y.y.y 存在兼容性问题}

#### 其他
- {如：默认 H2 内存数据库，重启后数据重置}

---

## 项目：{project-name-2}

（下一个项目，复用上述结构）
```

---

## 文件 2：认证机制分析报告

**路径**：`tests/baseline/_workflow/02-analysis-plan/auth-analysis.md`

**无论是否有认证机制，都必须输出此文件。**

```markdown
# 认证机制分析报告

**生成时间**: {YYYY-MM-DD}
**分析项目数**: {N}

---

## 项目：{project-name}

### 一、认证方式

| 属性 | 值 |
|------|-----|
| 认证类型 | `spring-security` / `shiro` / `sa-token` / `custom-interceptor` / `custom-filter` / `none` |
| 认证描述 | {一句话描述，如："基于 Spring Security + JWT 的无状态认证"} |

> 若为 `none`："该项目无任何认证机制，所有接口均公开访问。"

### 二、请求头要求

| 请求头名称 | 是否必填 | 条件 | 用途 |
|-----------|---------|------|------|
| Authorization | 是 | 除白名单外所有路径 | 认证令牌，格式 `Bearer {token}` |
| {header-name} | 是/条件必填/否 | {适用路径} | {说明} |

> 若无认证，写"无。所有接口不需要任何认证请求头。"

### 三、登录接口

| 属性 | 值 |
|------|-----|
| 接口路径 | `POST /auth/login` |
| 请求体格式 | JSON / Form |

**必填字段**：

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| username | string | 必填 | 用户名 |
| password | string | 必填 | 密码 |
| ... | ... | ... | ... |

> 若认证类型为 `none`，写"该项目无登录接口。"；若为自研 JWT 但未发现登录接口，写"未识别到登录接口，请人工确认。"

### 四、拦截器/过滤器链

请求链路（按顺序）：

```
{序号}. {类名} ({类型})
   类型: Filter / HandlerInterceptor
   路径: {urlPatterns}
   排除: {excludePatterns}
   动作: {认证动作描述}
   必填头: [{header-list}]
```

> 若有非认证拦截器（如 i18n、日志），单独列出并在动作中标注"与认证无关"。
> 若认证类型为 `none` 且无任何拦截器/过滤器，写"该项目无拦截器/过滤器。"。

### 五、权限模型

| 属性 | 值 |
|------|-----|
| 权限注解 | `@PreAuthorize` / `@RequiresPermissions` / `@SaCheckPermission` / 无 |
| 权限粒度 | 角色级（`hasRole`）/ 权限字符串级（`hasAuthority`）/ 无 |
| 说明 | {如 "Controller 方法上使用 @PreAuthorize(\"hasAuthority('system:user:list')\") 控制权限"} |

> 若无，三行均写"无"。

### 六、白名单路径

| 路径 | 说明 |
|------|------|
| /auth/login | 登录接口 |
| /swagger-ui/** | API 文档 |
| ... | ... |

> 若认证类型为 `none`，写"不适用（无需认证，无白名单概念）。"。
> 若认证类型非 `none` 但未发现白名单，写"未发现白名单配置（所有路径均需认证）。"。

### 七、建议与注意事项

#### 测试建议
- {如："所有接口（除白名单外）需在请求头携带 `Authorization: Bearer {token}`，测试前先调 POST /auth/login 获取 token"}
- {如："Token 有效期 30 分钟，长时间测试注意刷新"}

#### 安全提示
- {如：硬编码 JWT 密钥}
- {如：无认证机制，所有接口可直接访问}
- {如：Token 无过期时间}

---

## 项目：{project-name-2}

（下一个项目，复用上述结构）
```

---

## 多项目合并规则

1. 文件最顶层标题用 `#`（一级标题）
2. 每个项目用 `## 项目：{project-name}` 作为一级分隔
3. 项目内的章节用 `###`（三级标题）
4. 项目之间用 `---` 水平线分隔
5. 仅有一个项目时同样使用上述结构
