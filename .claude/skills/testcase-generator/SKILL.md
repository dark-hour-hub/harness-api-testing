---
name: testcase-generator
description: 从后端源码生成按模块组织的 YAML 接口测试用例。触发：/testcase-generator、生成测试用例、生成testcase、生成接口测试用例。读取 config.yaml 获取源码路径和环境配置，使用 CodeGraph 分析后端代码，输出数据与脚本分离的 YAML 定义，修改 YAML 后无需重新生成 pytest 脚本即可执行。
---

# 接口测试用例生成器

从后端源码全量分析接口，按 URL 前缀模块生成 YAML 测试用例。数据与脚本分离——修改 YAML 后无需重新生成 pytest 脚本。

## 总体架构

- **Phase A**（主会话）→ 共享分析，产出 `shared-context.yaml`（含 DTO 字段索引 + 预期用例数）
- **Phase B**（并行 Agent）→ 每模块一个 Agent，按预期用例数目标产出 `{module}-testcases.yaml`
- **Phase C**（主会话）→ 交叉验证 + YAML 结构校验，修复问题
- **Phase D**（主会话）→ 覆盖度评估。不达标则自动派 Agent 补齐，最多重试 2 轮

## ⛔ 铁律

1. **Phase A 关键分析在主会话完成。** A1-A3 和 A6 必须由主会话执行。A4（认证分析）和 A5（错误路径+i18n）可并行派给 2 个 Agent 执行，结果回传主会话填入 shared-context。
2. **Phase B 禁止重复 Phase A 的分析。** Agent prompt 内联共享上下文，Agent 不得重新搜索安全框架、R 类、i18n 文件。必须优先使用 dto_index 中的字段信息，缺失时才用 `codegraph_explore` 批量补充（禁止逐条 `codegraph_node`）。

---

## Phase A：共享分析（主会话执行，A4/A5 可并行 Agent）

### A1. 读取配置

读 `config.yaml`：`source.backend[]`（项目路径）、`current_environment`（环境名）、`environments.${env}.backend[]`（base_url + accounts）。

→ `references/config-reading.md`

### A2. API 全量发现

1. 对每个后端项目，用 CodeGraph 对各 HTTP 方法执行 `codegraph_search kind="route"`（limit=200），按 URL 路径第一段分组为模块。排除 Actuator、Swagger、SSE、静态资源、Demo 模块。
2. 收集所有路由涉及的 Controller 类名（去重），用 `codegraph_explore` 批量读取全部 Controller 源码（1-2 次调用）。提取每条路由的 HTTP 方法、完整路径、返回类型、认证要求、**response_structure**（`TableDataInfo`→`paginated` / `R<List>`→`list` / `R<T>`→`single` / `void`→`empty`）。写入 shared-context.yaml §6。
3. 收集所有路由的 DTO（`@RequestBody` 参数类型）和 VO（返回类型泛型）全限定名，去重后传递给 A3b。
4. **（新增）为每条路由预计算预期用例数**：在 A3b 完成 DTO 字段索引后，按 `references/coverage-rules.md` 公式计算每条路由的 `expected_minimum`（最低预期）和 `expected_ideal`（理想预期），写入 shared-context.yaml §6 每条路由的 `expected` 字段。Phase B Agent 将此作为硬性数量目标。
5. **（新增）识别场景链**：扫描同一 Controller 内的路由，识别"同一资源"的 CRUD 链（POST /xxx → GET /xxx/{id} → PUT /xxx → DELETE /xxx/{ids}），标记为场景链组。对每条链中的 POST 路由标记 `scene_chain: {type: "create", chain_id: "<module>-<resource>"}`，PUT/DELETE 路由标记 `scene_chain: {type: "update/delete", chain_id: "...", depends_on_create: true}`。写入 shared-context.yaml §6 路由的 `scene_chain` 字段。Phase B Agent 据此自动生成 extract + depends_on 链，避免遗漏。

→ `references/api-discovery.md`

### A2.6 认证有效性探测

在 A4 完成后，对每个模块取 1-2 条 `auth_required: true` 的路由发无 token 请求，对比返回的 `business_code` 与 `error_codes.auth_fail.business_code`：一致则写入该值，返回 200 则写入 200。结果写入 shared-context.yaml §6 每条路由的 `auth_probe_code`。此步骤依赖 A4/A5 结果，应在 A6 写入前执行。

→ `references/auth-analysis.md`

### A3. 值溯源 + DTO 字段预索引

#### A3a. 值溯源

追踪正向 code/message：Controller return → R 包装类静态方法 → 构造器。追踪反向 code/message：Service 异常抛出点 → 全局异常处理器。用 `codegraph_explore` 一次性读取 R.java、TableDataInfo.java 和全局异常处理器源码。

→ `references/value-resolution.md`

#### A3b. DTO 字段预索引

对 A2 收集的所有 DTO/VO（全项目去重），用 `codegraph_explore` 批量读取源码（每次 15-20 个类名，2-4 次覆盖全量）。按 `references/field-resolution.md` 优先级链提取 Java 字段名→JSON 键名、校验注解、必填标记。结果按模块写入 `dto_index`（结构见 `template/shared-context.yaml` §7）。Phase B Agent 优先从此索引获取字段信息，仅缺失时才自行读取。

### A4. 认证分析（可与 A5 并行）

1. 识别安全框架 → Grep 特征类（详见 `references/auth-analysis.md` 特征表）
2. Grep 全项目 `getHeader(` / `getParameter(` 调用，确定主认证头、token_prefix
3. 检查跨字段校验逻辑，汇总 `global_headers`
4. 用 `codegraph_explore` 批量读取登录 VO + 安全配置类 + 拦截器源码，按 `@JsonProperty > @JsonNaming > 默认` 优先级确定 JSON 键名，写入 `token_response_path` 和 `fixture_extracts`（禁止用 Java 字段名直接当 JSON 键名）

**⛔ 检查点**：通过 `references/auth-analysis.md` 六项验证清单后方可继续。

→ `references/auth-analysis.md` + `references/field-resolution.md`

### A5. 错误路径追踪 + i18n 解析（可与 A4 并行）

1. 定位全局异常处理器（`@RestControllerAdvice`），用 `codegraph_explore` 一次读取异常处理器 + 所有异常类源码
2. 识别格式化模式（原样透传/字段名拼接/固定兜底/i18n 解析），确定 `validation_message_mode`（遍历拼接→`concatenated` / 取首错误→`single`），写入 shared-context.yaml §1
3. 搜索 `messages*.properties`，解析所有 DTO 校验注解中的 i18n key → 翻译文本，写入 `i18n_map`

→ `references/error-tracing.md` + `references/i18n-resolution.md`

### A4/A5 并行策略

A3 完成后，并行派 2 个 Agent 执行 A4 和 A5，结果回传主会话在 A6 组装。

### A6. 输出共享上下文

将 A1-A5 的分析结果按 `template/shared-context.yaml` 模板填入，写入：

```
tests/baseline/_workflow/02-analysis-plan/shared-context.yaml
```

**此文件写入磁盘是进入 Phase B 的硬性前提。**

### A7. 环境能力探测

对路由清单中依赖外部服务（SMS/Email/OSS/Workflow 等）的接口发试探请求：返回 500 → 不可用，200 → 可用。结果写入 shared-context.yaml §8 `environment.capabilities`。

### A8. A6 验证清单

- [ ] 占位符已替换；accounts 字段完整；dto_index 覆盖全部模块
- [ ] i18n_map 覆盖 DTO 注解中出现的 key；error_codes 条目完整
- [ ] global_headers 认证头已拼接 token_prefix；login_endpoint 为纯路径
- [ ] token_response_path / fixture_extracts 的 JSON 键名已经 @JsonProperty 验证
- [ ] 路由清单含 response_structure + auth_probe_code；environment.capabilities 已填入

---

## Phase B：按模块并行生成（Agent 并行执行）

> ⛔ **前置条件**：`shared-context.yaml` 已写入且通过 Phase A6 验证清单。文件不存在 → **禁止进入 Phase B**。

### Agent 派发规则

1. 对 Phase A2 产出的**每个模块**，并行派发一个 Agent
2. 每个 Agent 的 prompt 必须：
   - 使用 `template/module-agent-prompt.md` 模板
   - 将模板中 `{SHARED_CONTEXT}` 替换为 `shared-context.yaml` 的**完整内联内容**
   - 将 `{MODULE}` / `{MODULE_NAME}` / `{BASE_URL}` / `{MODULE_ROUTES}` / `{SOURCE_PATH}` / `{OUTPUT_PATH}` 替换为实际值
   - 将 `{EXPECTED_MIN_TOTAL}` / `{EXPECTED_MIN_POSITIVE}` / `{EXPECTED_MIN_NEGATIVE}` 替换为 D1 预计算的模块汇总值
3. Agent 的 `description` 参数格式：`Generate {MODULE} module YAML`

### Agent 工作内容

Agent 按 `template/module-agent-prompt.md` 模板执行以下步骤（模板中 §3.0-§3.4 有完整说明）：

1. 评估 dto_index 覆盖率，优先使用共享上下文字段信息
2. 缺失 DTO/VO 用 `codegraph_explore` 批量补充
3. 生成正向 + 反向用例（按 `references/case-design.md` + `references/data-safety.md`）
4. 按 `references/yaml-schema.md` 格式输出 YAML

**Agent 必须通过 `template/module-agent-prompt.md` §6 全部检查清单后方可返回。**

---

## Phase C：交叉验证（主会话执行）

所有模块 Agent 完成后，主会话对全部 YAML 做交叉验证。

### C1. 断言值一致性检查

- **business_message**：`data_exists: [rows, total]` 的用例 → 验证为 `TableDataInfo.success_message`；含业务字段的用例 → 验证为 `R.success_message`
- **business_message_mode**：`validation_message_mode === "concatenated"` 的校验失败用例 → 验证设置了 `contains`；实际为单一消息的 → 改回 `exact`
- **data_exists 结构**：`response_structure === "paginated"` → 必须含 `rows` 和 `total`；`list` → 不应含 `rows`/`total`，应含 VO 实际字段

**修复**：发现不一致 → 用 Edit 工具直接修复 YAML。

### C2. fixture_extracts 一致性检查

检查所有 YAML 的 `auth.fixture_extracts` 中的每个值：
- JSONPath 格式（`$.data.xxx`）→ 正确，进入下一步
- JSONPath 字段名 → 与 `shared-context.yaml` §2 `auth.fixture_extracts` 中 Phase A 已验证的值比对，不一致则修复为 shared-context 中的值
- 硬编码值（具体字符串或数字）→ 错误，修复为对应的 JSONPath

**修复**：用 Edit 工具将错误值替换为 shared-context.yaml 中的正确 JSONPath。

### C3. 覆盖率检查

Phase A2 发现的每个模块每条路由，在对应 YAML 中至少有一条正向用例。

缺失的 API → 派修复 Agent 或手动补充。

### C4. 跨文件一致性

- 所有 YAML 的 `auth.type` 一致
- 所有 YAML 的 `auth.token_prefix` 一致（与 shared-context.yaml 中的值匹配，无首尾空格）
- 所有 YAML 的 `auth.login_endpoint` 一致（纯路径格式，无 HTTP 方法前缀）
- 所有 YAML 的 `global_headers` 结构一致

### C5. YAML 结构校验

对所有模块 YAML 执行数据结构类型检查：

1. **headers 条目类型**：遍历 `global_headers` 和每个用例的 `request.headers`，确认每个条目是 `{name, value}` 字典——若为纯字符串则报错并修复
2. **fixture_extracts 位置**：确认 `fixture_extracts` 在 `auth` 段内——若出现在 YAML 顶层则移入 `auth` 段
3. **token_response_path 必填**：确认每个模块 YAML 的 `auth.token_response_path` 不为空——若缺失则从 shared-context.yaml §2 补入
4. **硬编码系统 ID 扫描**：扫描所有 PUT/DELETE 路径——若路径段为纯数字 1-999 且非 `${变量}` 引用，输出 warning 并评估是否可替换为 extract 变量引用

**修复**：发现结构错误 → 用 Edit 工具直接修复 YAML。

### C6. response_structure 源码交叉验证

对 shared-context.yaml §6 中标记为 `return_type: TableDataInfo` 的路由，用 `codegraph_explore` 批量读取 Controller 方法签名，验证实际返回类型。`R<TableDataInfo<T>>` 被误判为 `TableDataInfo` 时需修正（JSON 结构不同：前者 data 内嵌 total/rows，后者顶层平铺）。发现不一致 → 先修 shared-context.yaml §6，再修对应 YAML 断言。

→ `references/api-discovery.md` §4d

---

## Phase D：覆盖度评估（主会话执行）

Phase C 完成后，对所有模块 YAML 做量化覆盖度评估。计算规则详见 `references/coverage-rules.md`。

**评分**：`正向覆盖率 × 0.5 + 反向覆盖率 × 0.5`。≥1.0 通过，0.7-0.99 警告，<0.7 不通过。两条硬性红线（路由缺正向、必填字段覆盖<50%）直接不通过。

**返工**：不通过时精准派单模块 Agent 补齐缺口（缺正向/缺反向/缺特定类型），最多循环 2 次。2 次后仍不通过 → 标注"人工介入"。

**报告**：生成 `tests/baseline/_workflow/03-testcases/coverage-report.md`，含模块评分表和缺失详情。

---

## 模板文件

| 文件 | 用途 |
|------|------|
| `template/shared-context.yaml` | Phase A 产出工件，Phase B Agent 共享上下文 |
| `template/module-agent-prompt.md` | Phase B Agent 标准 prompt 模板 |
| `template/module-testcase.yaml` | 单模块 YAML 输出模板 |
| `template/coverage-report.md` | Phase D 覆盖度报告模板 |

## 参考文档

| 文件 | 内容 |
|------|------|
| `references/config-reading.md` | config.yaml 读取规则 |
| `references/api-discovery.md` | API 发现与枚举 |
| `references/field-resolution.md` | 字段名解析（DTO/VO → JSON 键名） |
| `references/value-resolution.md` | 值溯源（R 包装类、异常响应） |
| `references/auth-analysis.md` | 安全框架与认证分析（含六项验证清单） |
| `references/error-tracing.md` | 错误路径追踪 |
| `references/i18n-resolution.md` | i18n 消息解析 |
| `references/case-design.md` | 用例设计规则 |
| `references/data-safety.md` | 数据安全规则 |
| `references/yaml-schema.md` | YAML 输出格式规范 |
| `references/coverage-rules.md` | Phase D 覆盖度计算规则与判定矩阵 |
