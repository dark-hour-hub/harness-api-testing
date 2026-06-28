---
name: testcase-generator
description: 从后端源码生成按模块组织的 YAML 接口测试用例。触发：/testcase-generator、生成测试用例、生成testcase、生成接口测试用例。读取 config.yaml 获取源码路径和环境配置，使用 CodeGraph 分析后端代码，输出数据与脚本分离的 YAML 定义，修改 YAML 后无需重新生成 pytest 脚本即可执行。
---

# 接口测试用例生成器

从后端源码全量分析接口，按 URL 前缀模块生成 YAML 测试用例。数据与脚本分离——修改 YAML 后无需重新生成 pytest 脚本。

## 总体架构

```
Phase A（主会话）                         Phase B（多 Agent，并行）         Phase C（主会话）
┌────────────────────────────┐     ┌──────────────────────┐     ┌──────────────────┐
│ A1 配置读取                 │     │ auth 模块 Agent       │     │ 响应包装器一致性    │
│ A2 API 全量发现(batch)      │     │ system 模块 Agent     │     │ fixture_extracts  │
│ A3 值溯源 + DTO 字段预索引   │ ──▶ │ resource 模块 Agent   │ ──▶ │ 覆盖率检查         │
│ A4 认证分析 ─┐              │     │ monitor 模块 Agent    │     │ 问题修复           │
│ A5 错误+i18n ┘(并行 Agent)  │     │ tool 模块 Agent       │     │                    │
│ A6 → 写入 shared-context    │     │ workflow 模块 Agent   │     │                    │
└────────────────────────────┘     └──────────────────────┘     └──────────────────┘
  产出：shared-context.yaml          产出：{module}-testcases.yaml    产出：修正后的 YAML
  (含 DTO 字段索引)
```

## ⛔ 铁律

1. **Phase A 关键分析在主会话完成。** A1-A3 和 A6 必须由主会话执行。A4（认证分析）和 A5（错误路径+i18n）可并行派给 2 个 Agent 执行，结果回传主会话填入 shared-context。
2. **Phase B 禁止重复 Phase A 的分析。** Agent prompt 内联共享上下文，Agent 不得重新搜索安全框架、R 类、i18n 文件。
3. **shared-context.yaml 写入磁盘是进入 Phase B 的硬性前提。** 文件不存在 → 禁止派 Agent。
4. **Phase B Agent 必须读完自己模块的所有 DTO/VO 源码再写断言。** 禁止猜测字段名。使用 `codegraph_explore` 批量读取——先收集模块所有 DTO/VO 类名，再 1-2 次 explore 调用全部取出，禁止逐条 `codegraph_node`。

---

## Phase A：共享分析（主会话执行，A4/A5 可并行 Agent）

### A1. 读取配置

读 `config.yaml`：`source.backend[]`（项目路径）、`current_environment`（环境名）、`environments.${env}.backend[]`（base_url + accounts）。

→ `references/config-reading.md`

### A2. API 全量发现

**步骤 1**：对每个后端项目，用 CodeGraph 对 GET/POST/PUT/DELETE/PATCH 各执行 `codegraph_search kind="route"`（limit=200），按 URL 路径第一段分组为模块。

排除：Actuator、Swagger、SSE、静态资源、Demo 模块。

**步骤 2**：收集步骤 1 中所有路由涉及的 **Controller 类名**（去重），用 `codegraph_explore` 批量读取所有 Controller 源码（1-2 次调用，一次传全部类名）。从源码中提取每条路由的 HTTP 方法、完整路径、返回类型、认证要求。

**步骤 3**：收集所有路由涉及到的 **DTO 全限定名**（`@RequestBody` 参数类型）和 **VO 全限定名**（返回类型泛型），去重后列入 `all_dtos` 和 `all_vos` 集合，传递给 A3b 做字段预索引。

**禁止**：对每条路由逐个调用 `codegraph_node`——这会产生 N 次串行 MCP 往返。

**关键**：每条路由标注返回类型是 `R<T>` 还是 `TableDataInfo<T>` 还是 `void`。这决定 Phase B 的 `business_message` 断言值。

→ `references/api-discovery.md`

### A3. 值溯源 + DTO 字段预索引

#### A3a. 值溯源

从 Controller return → R 包装类静态方法 → 构造器 → 常量/枚举，追踪正向 `business_code` 和 `business_message`。

从 Service 异常抛出点 → 全局异常处理器，追踪反向 code/message。

**必须确认**：
- `R.ok()` 的 code 和 message
- `R.fail()` / `R.fail(code, msg)` 的 code 和 message
- `TableDataInfo` 构建时的 message 值（通常为 "查询成功"）
- `@ResponseStatus` 注解的 HTTP 状态码

**使用 `codegraph_explore` 一次性读取** R.java、TableDataInfo.java 和全局异常处理器源码——不要逐个 codegraph_node。

→ `references/value-resolution.md`

#### A3b. DTO 字段预索引（关键性能优化）

对 A2 步骤 3 收集的**所有 DTO 和 VO**（全项目去重），用 `codegraph_explore` 批量读取源码（按包路径前缀分组，每次传 15-20 个类名，2-4 次调用覆盖全量）。

对每个 DTO/VO，按 `references/field-resolution.md` 优先级链提取：
- Java 字段名 → JSON 键名
- 校验注解（`@NotBlank` / `@NotNull` / `@NotEmpty` / `@Size` / `@Length` / `@Email` 等）
- 必填/可选标记

结果写入 `shared-context.yaml` 的 `dto_index` 字段，按模块组织：

```yaml
dto_index:
  <module>:
    dtos:
      <DTO简名>:
        full_name: "<全限定名>"
        fields:
          - { java: "userName", json: "userName", required: true, constraints: "@NotBlank @Length(min=2,max=30)" }
    vos:
      <VO简名>:
        fields: [...]
```

**目的**：Phase B Agent 直接从 shared-context 获取 DTO/VO 字段信息，不再重复读取源码。只有 shared-context 中未覆盖的 DTO（如服务间调用的嵌套类型）才需要 Agent 自行读取。

### A4. 认证分析（可与 A5 并行）

**步骤**：
1. 识别安全框架 → Grep 认证框架特征类（如 `StpUtil`/`SecurityFilterChain`/`ShiroFilterFactoryBean` 等，详见 `references/auth-analysis.md` 特征表）
2. Grep 全项目 `getHeader(` 和 `getParameter(` 调用（不限子目录）
3. 确定主认证头和 token_prefix
4. 检查跨字段校验逻辑（header/param 与 token extra 的比较运算）
5. 汇总 `global_headers`
6. **读取登录响应 VO 源码** → 用 `codegraph_explore` 批量读取登录 VO + 安全配置类 + 拦截器源码，按 `references/field-resolution.md` 优先级链（@JsonProperty > @JsonNaming > 默认）确定 accessToken、clientId 等字段的 JSON 键名，写入 `token_response_path` 和 `fixture_extracts`。**禁止用 codegraph_node 结构摘要中的 Java 字段名直接当 JSON 键名。**

**⛔ 检查点**：执行 `references/auth-analysis.md` 的六项验证清单，**全部通过后方可继续**。

→ `references/auth-analysis.md` + `references/field-resolution.md`

### A5. 错误路径追踪 + i18n 解析（可与 A4 并行）

**步骤**：
1. 定位全局异常处理器（`@RestControllerAdvice`）→ 用 `codegraph_explore` 一次读取异常处理器 + 所有异常类源码
2. 识别格式化模式（原样透传/字段名拼接/固定兜底/i18n 解析）
3. 搜索 properties 文件：`messages*.properties`、`ValidationMessages.properties`
4. 用 `codegraph_explore` 批量读取所有 DTO 源码中包含 i18n key 的校验注解，解析所有 i18n key → 翻译文本，写入 `i18n_map`

**重要**：校验注解的 `message` 和业务异常中的 i18n key 必须通过 properties 文件解析为最终翻译文本。

→ `references/error-tracing.md` + `references/i18n-resolution.md`

### A4/A5 并行执行策略

A4 和 A5 无依赖关系。A3 完成后，可同时派发 2 个 Agent：
- **Agent A4**：按 `references/auth-analysis.md` 执行认证分析，返回 `auth` + `global_headers` + `fixture_extracts` 三个 section 的 YAML 片段
- **Agent A5**：按 `references/error-tracing.md` + `references/i18n-resolution.md` 执行错误+i18n 分析，返回 `error_codes` + `i18n_map` 两个 section 的 YAML 片段

两个 Agent 的 prompt 中内联 A3 的相关输出（R 类名、异常处理器位置），避免重复搜索。

主会话收到两个 Agent 结果后，在 A6 中组装完整的 shared-context.yaml。

### A6. 输出共享上下文工件

将 A1-A5 的分析结果按 `template/shared-context.yaml` 模板填入，写入：

```
tests/baseline/_workflow/02-analysis-plan/shared-context.yaml
```

**此文件写入磁盘是进入 Phase B 的硬性前提。**

验证清单：
- [ ] 所有占位符已替换为实际值
- [ ] `accounts` 包含 config.yaml 中的全部字段（原样）
- [ ] `dto_index` 已按模块组织，覆盖所有模块的 DTO 和 VO（JSON 键名已按 @JsonProperty 验证）
- [ ] `i18n_map` 至少覆盖 properties 文件中出现在 DTO 注解里的 key
- [ ] `error_codes` 中每个条目都有 `status_code` + `business_code` + `business_message`
- [ ] `global_headers` 中认证头 value 已拼接 token_prefix
- [ ] `login_endpoint` 为纯路径（如 `/auth/login`），不含 HTTP 方法前缀（如 `POST `）
- [ ] `token_response_path` 的 JSON 键名已经 codegraph_explore 读取登录 VO 源码，按 @JsonProperty 注解验证
- [ ] `fixture_extracts` 中每个 JSON 键名已经 codegraph_explore 读取登录 VO 源码，按 @JsonProperty 注解验证
- [ ] 模块路由清单已填入 `modules` 字段

---

## Phase B：按模块并行生成（Agent 并行执行）

> ⛔ **前置条件**：`shared-context.yaml` 已写入且通过 Phase A6 验证清单。文件不存在 → **禁止进入 Phase B**。

### Agent 派发规则

1. 对 Phase A2 产出的**每个模块**，并行派发一个 Agent
2. 每个 Agent 的 prompt 必须：
   - 使用 `template/module-agent-prompt.md` 模板
   - 将模板中 `{SHARED_CONTEXT}` 替换为 `shared-context.yaml` 的**完整内联内容**
   - 将 `{MODULE}` / `{MODULE_NAME}` / `{BASE_URL}` / `{MODULE_ROUTES}` / `{SOURCE_PATH}` / `{OUTPUT_PATH}` 替换为实际值
3. Agent 的 `description` 参数格式：`Generate {MODULE} module YAML`

### Agent 工作内容（每个 Agent 独立完成）

#### B1. 字段溯源

**优先查 shared-context.yaml §dto_index**——Phase A 已预索引所有 DTO/VO 的字段信息（JSON 键名、校验注解、必填/可选）。大部分 DTO/VO 无需再读源码。

**仅当 dto_index 中未覆盖时**，才用 `codegraph_explore` 批量读取缺失的 DTO/VO（一次传全部缺失类名，不要逐个 codegraph_node）。

→ `references/field-resolution.md`

#### B2. 生成用例

为每个 API 生成正向用例（至少 1 条完整参数）+ 按特征选反向用例（缺参数/格式错/越界/无认证/权限不足/资源不存在）。分配 P0/P1/P2 优先级和标签。

**断言消息直接使用共享上下文**——不要重新判断用 "操作成功" 还是 "查询成功"。

**变量写入原则**：静态值直接内联（账号字段从共享上下文 §5 取具体值），动态值使用 `${}`。

→ `references/case-design.md` + `references/data-safety.md`

#### B3. 输出 YAML

按模块输出到 `tests/baseline/_workflow/03-testcases/{module}-testcases.yaml`。

→ `references/yaml-schema.md`，模板：`template/module-testcase.yaml`

### Agent 提交前自检

Agent 在返回前必须确认：
- [ ] 每条路由至少 1 条正向用例
- [ ] 每个 @NotBlank/@NotNull/@NotEmpty 字段有对应反向用例
- [ ] 所有 `business_message` 正确区分 TableDataInfo 和 R（值来自 shared-context.yaml §1）
- [ ] `fixture_extracts` 中每个值都是 JSONPath（`$.data.xxx`），非硬编码常量
- [ ] `global_headers` 中引用 fixture_extracts 变量的 header，value = `${变量名}`（变量引用）
- [ ] 账号字段 = 从 shared-context.yaml §5 取的 literal 值，非 `${account.xxx}`
- [ ] 唯一标识含 `${timestamp}`
- [ ] YAML 合法

---

## Phase C：交叉验证（主会话执行）

所有模块 Agent 完成后，主会话对全部 YAML 做交叉验证。

### C1. 响应包装器一致性检查

对每个 `data_exists: ["rows", "total"]` 的用例，验证 `business_message` 为 `shared-context.yaml` 中 `TableDataInfo.success_message` 的值。
对每个 `data_exists` 包含业务字段（非 rows/total）的用例，验证 `business_message` 为 `shared-context.yaml` 中 `R.success_message` 的值。

**修复**：发现不一致 → 直接用 Edit 工具修复 YAML 文件。

### C2. fixture_extracts 一致性检查

检查所有 YAML 的 `auth.fixture_extracts` 中的每个值：
- JSONPath 格式（`$.data.xxx`）→ 正确，进入下一步
- JSONPath 字段名 → 与 `shared-context.yaml` §4 中 Phase A 已验证的值比对，不一致则修复为 shared-context 中的值
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

---

## 模板文件

| 文件 | 用途 |
|------|------|
| `template/shared-context.yaml` | Phase A 产出工件，Phase B Agent 共享上下文 |
| `template/module-agent-prompt.md` | Phase B Agent 标准 prompt 模板 |
| `template/module-testcase.yaml` | 单模块 YAML 输出模板 |

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
