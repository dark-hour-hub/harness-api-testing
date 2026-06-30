# 安全框架与认证分析

确定所有 API 请求必须携带的请求头，写入 `global_headers` 和 `auth` 配置。

## 常见遗漏场景（速查）

执行分析前先过一遍此表——以下场景最容易漏检，且漏检后果严重（全量用例认证失败）：

| 遗漏类型 | 代码位置 | 为什么容易漏 |
|---------|---------|------------|
| 跨模块的交叉校验 | common-security 模块的 SecurityConfig | 只在安全框架模块（如 common-satoken）搜索 |
| Lambda 内的 getHeader | `addInterceptors(handler -> {...})` 内部 | AST 索引无法发现 lambda 内的调用 |
| WebSocket 拦截器 | PlusWebSocketInterceptor | 不经过 MVC 拦截器链，容易被忽略 |
| 参数来源的校验 | `request.getParameter(K)` 参与比较 | 只关注了 header 来源，忽略了 parameter |

## 步骤一：识别安全框架

在源码中搜索特征：

| 特征 | 框架 |
|------|------|
| `SecurityFilterChain`, `@EnableWebSecurity` | Spring Security |
| `ShiroFilterFactoryBean`, `AuthorizingRealm` | Apache Shiro |
| `StpUtil`, `SaTokenConfig`, `SaInterceptor` | Sa-Token |
| `implements Filter`, `extends OncePerRequestFilter` | 自定义 Servlet Filter |
| `implements HandlerInterceptor`, `addInterceptors` | Spring Interceptor |

## 步骤二：搜索所有请求读取点

用 **Grep**（非 CodeGraph）对**项目根目录全量搜索，不限定子目录**——Lambda 和匿名类内的调用无法被 AST 索引发现：

```
Grep pattern="getHeader\(" path="<source.backend[].path>"
Grep pattern="getParameter\(" path="<source.backend[].path>"
```

**禁止限定到安全框架所在模块**（如 `<project>-common-satoken`）。原因：安全拦截器的注册入口（`SecurityConfig implements WebMvcConfigurer`）常位于独立的通用安全模块（如 `common-security`），与认证框架配置类不在同一模块。限定子目录会导致跨模块的交叉校验代码漏检。

**批量读取**：收集 Grep 命中结果中所有涉及的 Java 文件名（去重），用 `codegraph_explore` 一次性批量读取这些安全相关文件源码，审查调用点上下文：

```
codegraph_explore query="<file1> <file2> <file3> ..."
```

不要对每个命中文件逐个 Read。

## 步骤三：确定主认证头

在认证入口方法中（`doFilter`/`preHandle`/`attemptAuthentication`/SaInterceptor lambda）：
1. 找到 `request.getHeader("X")` 调用
2. "X" 即为认证 header 名
3. 从安全配置读取 token 前缀（如 `token-prefix: Bearer`）

## 步骤四：检查跨字段校验

**判定规则**：若 `getHeader(X)` / `getParameter(X)` 的返回值参与了与认证会话数据的**比较运算**（`equals`/`equalsAny`/`==`/`StringUtils.equalsAny`），且失败分支抛出认证异常 → `X` 是必填 header。

**发现路径（按优先级搜索）**：

1. **所有 `WebMvcConfigurer` 实现类的 `addInterceptors()` 方法** → Grep `implements WebMvcConfigurer` 找到所有实现类，逐个检查 `addInterceptors()` 中的 lambda/匿名类
2. **所有 `HandlerInterceptor` 实现类的 `preHandle()` 方法** → Grep `implements HandlerInterceptor`
3. **所有 `Filter` 实现类的 `doFilter()` 方法** → Grep `implements Filter|extends OncePerRequestFilter`
4. **对步骤二的 Grep 结果**，筛选同时包含 `getHeader` 和 `getExtra`（或等效 token 数据读取方法）的文件，逐文件检查比较逻辑

```java
// 示例模式 1：header 值与 token extra 比较
headerVal = request.getHeader("X-Extra-Id");
tokenVal = tokenGetExtra("extraId");
if (!headerVal.equals(tokenVal)) throw new AuthException();

// 示例模式 2：多来源取值后与 token 比较（任一匹配即可）
headerVal = request.getHeader("extraId");
paramVal = ServletUtils.getParameter("extraId");
extraVal = tokenUtil.getExtra("extraId").toString();
if (!StringUtils.equalsAny(extraVal, headerVal, paramVal)) throw AuthException(...);
```

**模式 2 的关键含义**：header 和 parameter 的值都是可选的（任一匹配 token 即通过），但两者都缺失时 `equalsAny(X, null, null)` → `false` → 抛出异常。因此 `global_headers` **至少需要覆盖其中一个来源**，优先选择 header。

跨字段校验 header 的值来源：
- 登录响应 → `auth.fixture_extracts` 定义提取
- 全局常量 → 直接写入 global_headers

## 步骤四补充：批量读取登录 VO 和安全文件

在确定登录接口后，用 `codegraph_explore` 一次性读取登录 VO + 安全配置类 + 拦截器实现类：

```
codegraph_explore query="LoginVo SecurityConfig <InterceptorImpl> ..."
```

从登录 VO 源码中按 @JsonProperty 注解确定 JSON 键名。**禁止用 codegraph_node 结构摘要中的 Java 字段名直接当 JSON 键名。**

## 步骤五：汇总输出

### auth 配置

```yaml
auth:
  type: <框架类型>
  login_endpoint: <登录接口路径（仅路径，不含 HTTP 方法前缀），如 /auth/login>
  token_header: <主认证 header 名>
  token_prefix: "<前缀>"          # 从安全配置读取，无则 ""
  token_response_path: <token 在登录响应中的 JSONPath。⚠️ 字段名必须 Read 登录响应 VO 源码，按 @JsonProperty 注解确定，非 Java 字段名。例如 LoginVo 中 @JsonProperty("access_token") private String accessToken → $.data.access_token>
  response_msg_field: <包装类消息字段的 Java 字段名>
  fixture_extracts:              # 交叉校验字段提取。⚠️ JSON 键名必须 Read 登录响应 VO 源码，按 @JsonProperty 注解确定（codegraph_node 结构摘要只显示 Java 字段名，不含注解）
    <变量名>: "$.data.<JSON键名（从 VO 源码 @JsonProperty 确定，非 Java 字段名）>"
  accounts:                      # 从 config.yaml 原样复制
    <role>:
      <key>: <value>
```

### global_headers

```yaml
global_headers:
  # 认证头 — value 必须拼接 token_prefix
  - name: <认证 header 名>
    value: "<token_prefix>${token}"
    required: true
    description: "认证 Token"

  # 交叉校验头（若有）
  - name: <header 名>
    value: "${<变量名>}"
    required: true
    description: "与 token 中的 <字段> 比较"
```

### accounts 的用途

`auth.accounts` 中的字段在生成测试用例时**直接内联为具体值**，不使用 `${account.xxx}` 引用。

例如：生成 `account: admin` 的用例时，`request.body` 中的 `username` 字段直接写入 `accounts.admin.username` 的具体值，而非 `${account.username}`。

原因：账号配置是生成时的已知常量，不需要运行时解析。只有 `fixture_extracts`（从登录响应动态提取）的值才使用 `${变量名}` 引用。

## 步骤六：认证有效性探测

在完成以上分析后，对每个模块实际发一次无 token 请求，验证认证是否生效。

### 探测方法

对 Phase A2 产出的每个模块，选取 1-2 条标记为 `auth_required: true` 的路由，用 curl 或 Python 发送无 token 请求：

```python
import requests
resp = requests.get("http://localhost:8080/{module}/xxx")
probe_code = resp.json().get("code")
```

### 结果判定与记录

| 探测结果 | 含义 | 写入 auth_probe_code |
|---------|------|---------------------|
| probe_code === auth_fail.business_code | 认证生效 | 写入实际值 |
| probe_code === 200 | 接口不校验认证 | 写入 200 |
| probe_code 为其他值 | 认证行为与预期不符 | 写入实际值 |

将探测结果写入 shared-context.yaml §7 每条路由的 `auth_probe_code` 字段。

### 影响

- `auth_probe_code === 401`（或 auth_fail.code）→ Phase B 按正常无认证用例生成
- `auth_probe_code === 200` → Phase B 在标题注明"无认证但未拦截"，预期改为 200
- 其他值 → Phase B 按探测结果调整预期

## 步骤七：global_headers 验证清单（强制步骤，全部通过后方可进入下一阶段）

- [ ] Grep 结果中**每个** `getHeader("X")` / `getParameter("X")` 调用点都已审查（不限子目录）
- [ ] 跨模块搜索已完成——不仅搜索了安全框架模块，还搜索了 common-security、common-websocket 等通用模块
- [ ] 所有参与比较运算的 header/parameter 已标记并写入 `global_headers`
- [ ] 每个交叉校验 header 的 `value` 有明确数据来源（fixture_extracts / 全局常量）
- [ ] 若 value 来自登录响应，已在 `auth.fixture_extracts` 中定义提取路径，JSONPath 字段名已经 codegraph_explore 批量读取登录响应 VO 源码 + @JsonProperty 注解验证（非 codegraph_node 结构摘要中的 Java 字段名）
- [ ] 认证头 `value` 已拼接 `auth.token_prefix`（格式：`"<prefix>${token}"`）
- [ ] `login_endpoint` 为纯路径（如 `/auth/login`），不含 HTTP 方法前缀（如 `POST `）
- [ ] `token_response_path` 中的 JSON 键名已经 codegraph_explore 读取登录响应 VO 源码，按 @JsonProperty 注解验证
- [ ] `fixture_extracts` 中每个 JSON 键名已经 codegraph_explore 读取登录响应 VO 源码，按 @JsonProperty 注解验证

## 禁止

- 禁止凭框架名称猜测 header 名
- 禁止复制其他项目的 header 配置
- 禁止遗漏跨字段校验 header
- 禁止 global_headers 认证头 value 不拼接 token_prefix
