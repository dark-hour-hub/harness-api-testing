---
name: api-doc-to-perf
description: 从 API 接口文档生成 JMeter 性能测试场景 YAML（perf-scenario.yaml）。触发：/api-doc-to-perf、生成性能测试用例、接口文档转性能场景、perf scenario、生成压测场景、从文档生成性能用例。
---

# API 文档 → 性能场景 YAML 生成器

从模块文档、实体文档、认证分析报告提取接口信息，按模块生成 JMeter 压测场景定义 `perf-scenario.yaml`。

## 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|:---:|--------|------|
| `mode` | enum | 否 | `baseline` | `baseline` = 全量模式；`diff` = 增量模式 |

路径决议（按 mode）：

| 路径变量 | `baseline` | `diff` |
|---------|----------|--------|
| `DOC_ROOT` | `tests/baseline/_workflow/03-api-docs` | `tests/diff/_workflow/01-diff-api-doc` |
| `ANALYSIS_ROOT` | `tests/baseline/_workflow/02-analysis-plan` | 同 baseline（认证/框架分析无增量概念） |
| `OUTPUT_DIR` | `tests/baseline/_workflow/05-perf-scenarios` | `tests/diff/_workflow/03-diff-perf-scenarios` |

## 输入

| 来源 | 路径 | 用途 |
|------|------|------|
| 主文档 | `${DOC_ROOT}/API接口文档.md` | Base URL、请求头模板、响应包装、测试账号 |
| 认证分析 | `${ANALYSIS_ROOT}/auth-analysis.md` | 登录接口、Token 提取 JSONPath |
| 清单文件 | `${DOC_ROOT}/_manifest.yaml` | 模块路由表（method、path、auth、permission） |
| 模块文档 | `${DOC_ROOT}/modules/*.md` | 各接口请求参数、响应结构、业务规则 |
| 实体文档 | `${DOC_ROOT}/entities/*.md` | 请求体 JSON 字段定义 |

## 输出

```
${OUTPUT_DIR}/
├── 01-认证模块.yaml
├── 02-资源管理.yaml
└── ...
```

每个 YAML 对应一个模块，命名与模块文档一致（扩展名 `.yaml`）。

---

## 执行流程

### Step 0 — 读取输入

读取主文档、认证分析、`_manifest.yaml`，提取：
1. `base_url`（从主文档或 `config.yaml` 的 `environments.<env>.backend[].url`）
2. 登录接口路径、登录请求体、Token JSONPath（从 `auth-analysis.md`）
3. 各模块路由清单（method、path、auth、request_body）

### Step 1 — 构建全局配置

按 [references/perf-schema.md](references/perf-schema.md) 构建所有模块共享的 `headers_config`、`auth_setup`：

- `public_headers`：从主文档「公开接口」请求头表格照抄
- `auth_headers`：从主文档「认证接口」请求头表格照抄，Token 值统一写 `${token}`
- `auth_setup.login_body`：从登录接口实体文档的「字段定义」表取 JSON 键名，值从 `_manifest.yaml` 的 `test_accounts` 或 `config.yaml` 的账号提取
- `auth_setup.token_jsonpath`：从 `auth-analysis.md` 登录响应提取路径取

### Step 2 — 并行派发模块 Agent

对 `${DOC_ROOT}/modules/` 下每个 `.md` 并行派发一个 Agent，按 [template/perf-module-agent-prompt.md](template/perf-module-agent-prompt.md) 生成 YAML。

**接口选取规则**（Agent 内执行，写进 prompt）：

1. 每个模块选取 **3~5 个核心接口**（登录、列表查询、写操作优先）
2. 并发档位按优先级：P0 接口 → `100/60s`，P1 接口 → `50/60s`，P2 接口 → `20/30s`
3. 认证接口场景 `auth.required: false`；业务接口 `auth.required: true`
4. `thresholds` 默认值：`p95: 800`、`error_rate: 0.01`、`min_rps` 按接口类型估算（查询 30、写 20、登录 50）
5. 请求体/查询参数从模块文档 + 实体文档取 JSON 键名，避免 Java 字段名

### Step 3 — 校验

```bash
python .opencode/skills/api-doc-to-perf/scripts/validate_perf.py ${OUTPUT_DIR}/
```

校验字段完整性、`token_jsonpath` 存在性、`thresholds` 非空、`load` 必填项。校验不通过 → 派修复 Agent，最多 2 轮。

---

## 禁止项

- `login_endpoint` 含 HTTP 方法前缀 → 必须是纯路径
- `request.body` / `login_body` 使用 Java 字段名 → 必须用 JSON 键名
- 在 `auth_headers` 中写 `${auth.token}` → 必须写 JMeter 变量 `${token}`
- `thresholds` 为空对象
- `load` 缺少 `users` 或 `duration`
- Agent 预读全量实体文件（仅读本模块引用的）
