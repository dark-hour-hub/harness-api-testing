---
name: api-doc-discover
description: API 接口发现与模块分组。从后端源码扫描所有路由，按 URL 前缀分组为模块，输出结构化清单 _manifest.yaml 和主文档骨架。触发：api-doc 全流程的第一步、/api-doc-discover、发现API接口。
---

# API 接口发现与分组

扫描后端源码，发现所有 API 路由，按模块分组，输出结构化清单和主文档骨架。

## 前置输入

并行读取：

1. `config.yaml` — source.backend[].path（源码路径）、environments.${current_environment}.backend[]（base_url、测试账号）
2. `tests/baseline/_workflow/02-analysis-plan/auth-analysis.md` — 认证机制，白名单、请求头
3. `tests/baseline/_workflow/02-analysis-plan/framework-analysis.md` — 框架、技术栈

## 输出产物

```
tests/baseline/_workflow/03-api-docs/
├── _manifest.yaml              # 结构化清单（下游 Skill 的输入合约）
└── API接口文档.md    # 主文档骨架（模块概览和已知问题留空）
```

_manifest.yaml 详细格式定义见 [references/_manifest-format.md](references/_manifest-format.md)
接口文档 详细格式定义见 [.claude/references/API接口文档模板.md](../../references/API接口文档模板.md)

---

## 流程

### Step 1 — 读取输入 + 确认响应包装

并行读 3 个前置文件。然后用 `codegraph_explore` 一次性确认 R 类和 TableDataInfo 的字段名：

```
codegraph_explore query="R TableDataInfo"
```

从源码中提取：`code` 字段名、`msg`/`message` 字段名、`rows`/`total` 字段名、`R.ok()` 的默认 code 值。

### Step 2 — 全量路由发现

用 `codegraph_search kind="route"` 搜索全部 HTTP 方法路由：

```
GET limit=200 | POST limit=200 | PUT limit=200 | DELETE limit=200 | PATCH limit=200
```

5 次搜索可并行发出。

### Step 3 — 排除非业务路由

排除以下路由：
- `/actuator/**` — 监控端点
- `/swagger-ui/**`, `/v3/api-docs/**` — API 文档
- `/static/**`, `/public/**` — 静态资源
- 返回类型为 `SseEmitter` 或路径含 `sse` 的 — SSE 推送
- `/demo/**` — 演示模块（除非 config 明确需要）
- `/*.html`, `/*.css`, `/*.js`, `/favicon.ico`, `/error` — 静态文件

### Step 4 — 批量读取 Controller 源码

收集 Step 3 保留的所有路由涉及的 Controller 类名（去重）。用 `codegraph_explore` 批量读取所有 Controller 源码（1-2 次调用，每次 15-20 个类）。

从源码中逐条提取：

| 信息 | 来源 |
|------|------|
| HTTP 方法 | 方法上的 `@XxxMapping` 注解（不以方法名推断） |
| 完整路径 | 类级 `@RequestMapping` + 方法级 `@XxxMapping` |
| 接口说明 | 方法注释 / Swagger 注解 / 方法名语义 |
| 认证方式 | `@SaIgnore` 类/方法级 → 无需认证；否则需要认证 |
| 权限要求 | `@SaCheckPermission("xxx")` / `@SaCheckRole("xxx")` → 权限标识；无则 `null` |
| 请求体 DTO | `@RequestBody` 参数的全限定类型名 |
| 路径参数 | `@PathVariable` 参数名和类型 |
| 返回类型 | 方法返回类型的泛型参数 |
| 特殊属性 | `@RepeatSubmit` / `@RateLimiter` / `@ApiEncrypt` 等 |

### Step 5 — 按模块分组

以 URL 路径第一段为模块标识：
- `/auth/login` → `auth`
- `/system/user/list` → `system`
- `/workflow/...` → `workflow`
- `/tool/gen/...` → `tool`
- `/resource/...` → `resource`
- `/monitor/...` → `monitor`
- 仅有一级路径的（如 `/`）→ `common`

同前缀但业务含义不同的，按 URL 第二段进一步细分（如 `/system/user` 和 `/system/role` 可合入 `system` 模块，也可按接口数量拆开）。

**模块排序**：认证模块最先，系统管理其次，其他按字母排列。

### Step 6 — 模块大小评估

统计每个模块的接口数：
- ≤ 15：单文件输出
- 16-30：拆为 2 个子文件
- > 30：拆为 N 个，每约 15 个一组

在 manifest 的 `split_plan` 字段记录拆分方案。

### Step 7 — 收集 DTO/VO 清单

从所有路由提取：
- `all_dtos`：`@RequestBody` 参数的全限定类型名（去重）
- `all_vos`：返回类型泛型中的 VO 全限定名（去重）

按模块分组，写入 manifest。

### Step 8 — 写入输出

1. 创建 `tests/baseline/_workflow/03-api-docs/` 目录
2. 写入 `_manifest.yaml`（格式见 [references/_manifest-format.md](references/_manifest-format.md)）
3. 写入主文档骨架（填充项目信息、测试账号、响应包装、权限体系；模块概览和已知问题留空）

---

## 禁止

- 不生成实体文件（由 `api-doc-entities` 负责）
- 不生成模块文档（由 `api-doc-module` 负责）
- 不回填主文档模块概览（由 `api-doc-assemble` 负责）
- 不逐条 `codegraph_node`——用 `codegraph_explore` 批量读
- 不凭方法名推断 HTTP 方法
- 不凭类名推断路径前缀
