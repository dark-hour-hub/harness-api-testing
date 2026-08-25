---
name: analyze-source
description: 分析源码结构，识别 Controller、API 接口、Vue 页面，支持技术栈检测和微服务分析
allowed-tools: Read, Glob, Grep, Bash
triggers:
  - 执行 /test 命令
  - 用户说"分析源码"、"分析项目"
---

# 源码分析技能

## 执行步骤

### 1. 读取配置

读取 `config.yaml`，获取源码路径配置：
- `source.backend[].path` - 后端源码路径
- `source.frontend[].path` - 前端源码路径

### 2. 初始化 CodeGraph

对于 `config.yaml` 中配置的每个源码路径（`source.backend[].path` 和 `source.frontend[].path`）：

1. 检查项目目录下是否存在 `.codegraph/` 文件夹
2. 如果不存在，执行 `codegraph init -i` 初始化索引
3. 如果已存在，检查 CodeGraph 状态，确认索引可用

### 3. 结合 CodeGraph 分析代码

结合上一步生成的 CodeGraph 索引进行深度分析。

**CodeGraph 可用工具**（通过 MCP 或 CLI）：

| 工具 | 用途 |
|------|------|
| `codegraph_status` | 检查索引状态和统计 |
| `codegraph_search` | 按名称查找符号（类/函数/方法/路由） |
| `codegraph_context` | 获取符号的完整上下文（调用者+被调用者） |
| `codegraph_explore` | 查看多个相关符号的源码（一次性返回） |
| `codegraph_trace` | 追踪两个符号之间的调用路径 |
| `codegraph_impact` | 分析变更符号的影响半径 |
| `codegraph_files` | 获取项目文件结构树 |
| `codegraph_callers` | 查找调用某个符号的所有位置 |
| `codegraph_callees` | 查找某个符号调用的所有位置 |

**优先使用 CodeGraph 的场景**：
- 查找符号（类/函数/方法）的位置和定义 → 用 `codegraph_search`
- 理解某个类的调用/被调用关系 → 用 `codegraph_context`
- 追踪数据流（如 "请求如何到达数据库"）→ 用 `codegraph_trace`
- **追踪错误路径（如 "错误密码 → Asserts.fail → GlobalExceptionHandler"）→ 用 `codegraph_trace` 或 `codegraph_callees`**
- 查找"修改这个函数会影响哪些代码" → 用 `codegraph_impact`
- 快速了解项目结构 → 用 `codegraph_files`
- **验证反向用例的真实 code/message → 用 `codegraph_trace` 从 Controller 方法到 Service 方法，找到异常抛出点**
- **验证 API 的 HTTP 方法和完整路径 → 用 `codegraph_search kind="route"` 搜索路由索引**

### 4. 技术栈检测

自动检测项目使用的技术框架：

#### 后端框架检测

| 框架 | 检测方式 |
|------|---------|
| Spring MVC | `pom.xml` + `@RestController` |
| Spring WebFlux | `RouterFunction` |
| Flask | `requirements.txt` + `@app.route` |
| Express | `package.json` + `app.get` |

#### 前端框架检测

| 框架 | 检测方式 |
|------|---------|
| Vue 2/3 | `package.json` + `.vue` 文件 |
| React | `package.json` + `.jsx` 文件 |
| Element Plus | `el-input`, `el-button` |

### 5. 认证与安全分析（粗判，深析由 framework-analyzer 承接）

请求到达 Controller 前会经过 Filter/拦截器/安全框架。**本 skill 只做粗判**（供 `apis.json` 的 `requires_auth` 字段标注）；深度分析（必填请求头、Token 来源、拦截/白名单路径、认证流程）由 `framework-analyzer` skill（test 命令阶段 03）承接，产出 `framework-analysis.md` 与 `auth-analysis.md`，本 skill 不重复产出。

粗判方法：

#### 5.1 检测安全框架

| 框架 | 检测方式 |
|------|---------|
| Shiro | `ShiroFilterFactoryBean`，pom 中有 `shiro-core` |
| Spring Security | `SecurityFilterChain`，pom 中有 `spring-security-core` |
| Sa-Token | `SaTokenConfig` / `StpLogic` / `@SaCheckLogin` |
| 自定义 Filter | `javax.servlet.Filter` + `@Component` |
| HandlerInterceptor | `implements HandlerInterceptor` + `addInterceptors()` |
| 无认证 | 以上特征均无 |

#### 5.2 标注 requires_auth

对每个 API 标注 `requires_auth`：
- 命中免认证注解（如 `@SaIgnore` / `@PermitAll` / `@Anonymous`，以源码实际为准）→ `false`
- 否则 → `true`（检测到无认证框架时全部 `false`）

### 6. 分析后端源码

#### 5.1 提取 Controller API

找出所有 Controller 类，提取 API 定义：
1. 识别 HTTP 方法注解（`@GetMapping`, `@PostMapping` 等）
2. 解析路径、参数来源（`@RequestBody`、`@PathVariable`、`@RequestParam`）
3. 解析权限注解（`@PreAuthorize` 等）

**5.1.1 路径拼接规则（禁止从类名推断前缀）**

API 的完整路径由以下规则确定：

```
完整路径 = 类级 @RequestMapping 的值（若有） + 方法级 Mapping 的值
```

| 情况 | 类注解 | 方法注解 | 完整路径 | 说明 |
|------|--------|---------|---------|------|
| 有类级前缀 | `@RequestMapping("/auth")` | `@PostMapping("/login")` | `/auth/login` | 直接拼接 |
| 有类级前缀 | `@RequestMapping("/system/user")` | `@GetMapping("/list")` | `/system/user/list` | 直接拼接 |
| 无类级前缀 | 无 | `@GetMapping("/auth/code")` | `/auth/code` | 就是方法路径 |
| 无类级前缀 | 无 | `@GetMapping("/resource/sms/code")` | `/resource/sms/code` | 就是方法路径 |

**禁止规则**：
- **禁止**根据 Controller 类名推断路径前缀（类名 `XxxController` 不等于路径以 `/xxx/` 开头；路径只取决于 `@RequestMapping` 和 `@XxxMapping` 注解的实际值）
- **禁止**根据 REST 命名惯例推断 HTTP 方法（方法名 `logout` 不等于 `DELETE`，必须看实际注解是 `@PostMapping` 还是 `@DeleteMapping` 等）
- **禁止**在没有类级 `@RequestMapping` 注解时，自行根据任何规则添加路径前缀

**5.1.2 CodeGraph 路由索引强制验证**

提取每个 API 后，必须用 CodeGraph 路由搜索验证 HTTP 方法和完整路径：

```
codegraph_search query="<HTTP方法关键词> <路径关键词>" kind="route"
```

验证项：
1. **HTTP 方法**：CodeGraph 返回的 route 前缀（GET/POST/PUT/DELETE/PATCH）必须与提取结果一致
2. **完整路径**：CodeGraph 返回的路径必须与拼接结果完全一致

如果 CodeGraph 返回的 route 与提取结果不符 → 以 CodeGraph route 的值为准。

在 apis.json 输出中为每个 API 增加验证标注字段：

```json
{
  "method": "POST",
  "path": "/auth/logout",
  "method_verified": true,
  "route_source": "CodeGraph route index"
}
```

**5.1.3 全量枚举强制规则**

**禁止人工挑选"代表性"API。** 必须对所有已发现 Controller 所在模块执行全量路由枚举，不得遗漏任何端点。

执行步骤：

1. **分 HTTP 方法全量搜索路由**：对每种 HTTP 方法，用 `codegraph_search kind="route"` 搜索，limit 设为 200，确保覆盖所有路由：

   ```
   codegraph_search kind="route" query="POST" limit=200
   codegraph_search kind="route" query="GET" limit=200
   codegraph_search kind="route" query="PUT" limit=200
   codegraph_search kind="route" query="DELETE" limit=200
   codegraph_search kind="route" query="PATCH" limit=200
   ```

2. **合并去重，按模块分组**：以 URL 路径前缀（如 `/system/`、`/auth/`、`/workflow/`）划分模块归属，将每条路由写入 `apis.json`，不得遗漏。

3. **逐条补全字段详情**：对每条路由，通过 `codegraph_node` 查看对应 Controller 方法，补全 `request_body`、`response_fields`、`requires_auth`、`permissions` 等字段。若某路由因源码缺失或依赖问题无法补全字段，在 `description` 中标注 `[字段待补全]`，而非跳过该路由。

4. **模块统计写入 generation-plan.md**：「一、分析范围」表格中必须逐模块列出 API 数量，且 `API 接口` 总数应 ≥ CodeGraph 路由总数的 80%。

**跳过规则**：以下类型的 URL 可以在 apis.json 中排除，但必须在 generation-plan.md 中明确记录排除原因和数量：

| 排除类型 | URL 示例 | 原因 |
|----------|---------|------|
| Actuator 监控端点 | `/actuator/**` | 非业务接口 |
| SSE 长连接 | `${sse.path}` | 非请求-响应模式 |
| Swagger/API 文档 | `/swagger-ui/**`, `/v3/api-docs/**` | 非业务接口 |
| 静态资源 | `/static/**`, `/assets/**` | 非 API 接口 |

**禁止行为**：
- 禁止因"API 太多写不下"而只选部分写入 apis.json
- 禁止因"某个模块不重要"而跳过整个模块
- 禁止静默跳过——任何未写入 apis.json 的模块必须在 generation-plan.md 中说明原因

#### 5.2 提取请求体定义

通过 `codegraph_search` 查找 DTO/VO 类，分析字段结构：
- 字段名、数据类型
- 必填判定（`@NotNull`、`@NotBlank`）
- 校验规则（`@Length`、`@Pattern`、`@Min`/`@Max`）

类型映射参考 `template/analysis-reference.md`。

#### 5.3 提取响应字段

解析 VO 类和 Result 包装类，获取响应数据结构。

#### 5.4 错误路径追踪原则

**原则**：Controller 返回值 ≠ 实际响应。必须追踪完整调用链。

1. 从 Controller 方法追踪到 Service 实现（`codegraph_trace`）
2. 在 Service 中定位异常抛出点（`Asserts.fail`、直接 `throw`）
3. 判断异常是否穿透到全局异常处理器，或被局部 catch
4. 从全局异常处理器获取真实 code 和 message

**禁止**仅凭 Controller return 语句推断反向用例的 code/message。

### 7. 分析前端源码

找出 `.vue` 页面，提取路径、组件名、元素选择器。

> 认证机制识别（登录流程、认证方式、Token 方案）已并入第 5 节粗判，深度分析由 `framework-analyzer` 承接，此处不再重复。

---

## 输出文件

| 文件 | 路径 | 模板 |
|------|------|------|
| 分析报告 | `tests/baseline/specs/{module}/*-analysis.md` | `template/output-formats.md` |
| 规格文件 | `tests/baseline/specs/{module}/*-spec.yaml` | `template/output-formats.md` |
| 接口文件 | `tests/baseline/_workflow/02-analysis-plan/apis.json` | `template/output-formats.md` |
| 生成计划 | `tests/baseline/_workflow/02-analysis-plan/generation-plan.md` | `template/generation-plan-template.md` |
---

---

## 支持的分析器

| 后端 | 前端 |
|------|------|
| Spring MVC (`@GetMapping` 等) | Vue 2/3 (`.vue` + v-model) |
| Spring WebFlux (`RouterFunction`) | React (`.jsx`) |
| Flask (`@app.route`) | Element Plus (`el-input`, `el-button`) |
| Express (`app.get` 等) | |

| 安全框架 | 检测方式 |
|----------|---------|
| Shiro | pom + `ShiroFilterFactoryBean` |
| Spring Security | pom + `SecurityFilterChain` |
| 自定义 Filter | `javax.servlet.Filter` |
| HandlerInterceptor | `addInterceptors()` |
