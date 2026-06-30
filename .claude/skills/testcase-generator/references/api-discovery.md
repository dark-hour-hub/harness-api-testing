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
| response_structure | 从返回类型判定：`TableDataInfo<T>` → `paginated`；`R<List<T>>` → `list`；`R<T>`（T 非 List） → `single`；`void`/`R<Void>` → `empty` |
| 认证要求 | 类/方法上的认证注解、安全配置白名单 |

### 4. 收集 DTO/VO 全限定名

从步骤 3 的补全结果中，提取所有 `request_body_dto`（@RequestBody 参数类型）和返回类型泛型 VO，去重后生成两个集合：

- `all_dtos`：所有 DTO 全限定名
- `all_vos`：所有 VO 全限定名

传递给 Phase A3b 做字段预索引。

### 4b. response_structure 判定规则

从 Controller 方法返回类型提取响应数据结构类型：

| 返回类型 | response_structure | 说明 |
|---------|-------------------|------|
| `TableDataInfo<T>` | `paginated` | 分页结构，data 中包含 rows 和 total |
| `R<List<T>>` | `list` | 列表结构，data 是数组 |
| `R<T>`（T 为非 List 的单个类型） | `single` | 单对象结构，data 是单个对象 |
| `R<Void>` 或 `void` | `empty` | 无响应体或无 data 字段 |
| `R<PageResult<T>>` 等自定义分页 | `paginated` | 自定义分页包装，需在 shared-context 中注明 structure |

此值写入 shared-context.yaml §7 的 `response_structure` 字段，Phase B Agent 据此决定 `data_exists` 断言内容。

### 4c. 场景链识别

从步骤 3 补全的路由清单中，识别同一 Controller 内"同一资源"的 CRUD 路由组，标记为场景链。

**识别规则**（按优先级）：

1. **同 Controller + 同路径前缀**：同一 Controller 中路径去掉变量部分后相同的一组路由。例如 `SysPostController` 中的 `GET /system/post/list`、`POST /system/post`、`PUT /system/post`、`DELETE /system/post/{postIds}` → 链 ID: `system-post`
2. **返回类型有 extract 价值**：POST 路由返回 `R<XxxVo>`（data 含 ID）→ 标记为 `type: "create"`
3. **返回 void/R<Void>**：POST 返回空 → 标记 `type: "create"` 但注明 `extractable: false`，该链不生成 PUT/DELETE 正向用例

**输出格式**（写入 shared-context.yaml §6 每条路由的 `scene_chain` 字段）：

```yaml
# POST 创建
scene_chain:
  type: "create"
  chain_id: "system-post"
  extractable: true              # R<XxxVo> 包含 ID

# PUT 修改
scene_chain:
  type: "update"
  chain_id: "system-post"
  depends_on_create: true

# DELETE 删除
scene_chain:
  type: "delete"
  chain_id: "system-post"
  depends_on_create: true

# 无场景链
scene_chain: null
```

**注意**：同一链中 `depends_on_create: true` 的路由，其 expected.min_positive 应设为 0（正向用例依赖 create 的 extract，create 失败则全链失败）。Phase D 会验证链的完整性。

### 4d. response_structure 验证（供 Phase C6 使用）

步骤 3 提取的 `response_structure` 需要在后续 Phase C6 做二次验证。验证规则：

1. 对每条 `return_type: TableDataInfo` 的路由，用 `codegraph_explore` 读取 Controller 方法源码
2. 检查方法签名中的实际返回类型：
   - `public TableDataInfo<T> list(...)` → 正确，JSON 结构为 `{code, msg, total, rows}`（顶层平铺）
   - `public R<TableDataInfo<T>> list(...)` → **误判**，JSON 结构为 `{code, msg, data: {code, msg, total, rows}}`（嵌套在 R 的 data 内）
   - `public R<List<T>> list(...)` → **误判**，应标记为 `return_type: R, response_structure: list`
3. 同样验证标记为 `return_type: R` 的路由——确认不返回 `TableDataInfo`

验证在 Phase C6 执行，而非 A2 阶段。A2 阶段只需记录推断值，C6 做最终修正。

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
