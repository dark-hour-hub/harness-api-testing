# API 发现与枚举

## 步骤

### 1. 全量路由搜索

对每种 HTTP 方法执行 CodeGraph 搜索，limit 设为 200 确保覆盖：

```
codegraph_search kind="route" query="GET" limit=200
codegraph_search kind="route" query="POST" limit=200
codegraph_search kind="route" query="PUT" limit=200
codegraph_search kind="route" query="DELETE" limit=200
codegraph_search kind="route" query="PATCH" limit=200
```

### 2. 分组为模块

以 URL 路径第一段为模块标识。例：`/system/user/list` → `system`，`/auth/login` → `auth`。仅有一级路径的（如 `/login`）归入 `common`。

### 3. 批量读取 Controller 源码（关键：禁止逐条 codegraph_node）

收集步骤 1 中所有路由涉及的 **Controller 类名**（去重），使用 `codegraph_explore` 一次性批量读取所有 Controller 源码：

```
codegraph_explore query="<Controller1> <Controller2> <Controller3> ..."
```

一次 explore 调用可读取多个 Controller。若 Controller 数量超过单次 explore 容量，按 15-20 个一组分批，2-3 次调用覆盖全量。

从批量读取的源码中逐条补全：

| 信息 | 来源 |
|------|------|
| HTTP 方法 | 方法上的 `@XxxMapping` 注解，**不以方法名推断** |
| 完整路径 | 类级 `@RequestMapping` 值 + 方法级 `@XxxMapping` 值。无类级注解则直接取方法路径 |
| 请求体 | `@RequestBody` 参数的类型（DTO 全限定名） |
| 查询参数 | `@RequestParam` 参数名和类型 |
| 路径变量 | `@PathVariable` 参数名 |
| 业务 header | `@RequestHeader` 参数名 |
| 返回类型 | 方法返回类型的泛型参数（如 `R<XxxVo>` → `XxxVo`） |
| 认证要求 | 类/方法上的认证注解、安全配置白名单 |

### 4. 收集 DTO/VO 全限定名

从步骤 3 的补全结果中，提取所有 `request_body_dto`（@RequestBody 参数类型）和返回类型泛型 VO，去重后生成两个集合：

- `all_dtos`：所有 DTO 全限定名
- `all_vos`：所有 VO 全限定名

传递给 Phase A3b 做字段预索引。

### 5. 排除

| 排除类型 | 示例 |
|----------|------|
| Actuator | `/actuator/**` |
| API 文档 | `/swagger-ui/**`, `/v3/api-docs/**` |
| 静态资源 | `/static/**`, `/public/**` |
| SSE | 返回类型为 `SseEmitter` 或 `Flux<ServerSentEvent>` |

排除的接口需记录数量和原因。

## 禁止

- 禁止根据类名推断路径前缀（`XxxController` ≠ 路径以 `/xxx/` 开头）
- 禁止根据方法名推断 HTTP 方法（`delete()` ≠ `@DeleteMapping`）
- 禁止跳过模块（即使"不重要"）
- 禁止因数量多而只选部分
- **禁止对每条路由逐个调用 `codegraph_node`**——必须用 `codegraph_explore` 批量读取
