---
name: api-doc-diff
description: 增量 API 文档生成。基于代码变更文档和全量基线 API 文档，结合 CodeGraph + git diff，仅生成变更部分的接口文档、实体文档、模块文档。触发：/api-doc-diff、增量接口文档、diff api doc、生成增量API文档、增量生成API文档。
---

# 增量 API 文档生成

基于代码变更文档和全量基线，**仅生成变更部分**的 API 文档到 `tests/diff/_workflow/01-diff-api-doc/`。

## 输入

| # | 文件 | 用途 |
|---|------|------|
| 1 | `config.yaml` | 取 `source.backend[].path`（源码路径）、`environments`（base_url） |
| 2 | `tests/diff/doc/` | 代码变更文档（模板参考 `.opencode/references/代码变更说明文档模板.md`） |
| 3 | `tests/baseline/_workflow/03-api-docs/` | 全量基线：`_manifest.yaml`、`API接口文档.md`、`entities/`、`modules/` |

## 输出

```
tests/diff/_workflow/01-diff-api-doc/
├── API接口文档.md          # 照抄基线，仅当认证/框架/账号变更时修改
├── _manifest.yaml           # 仅含受影响模块的清单
├── entities/
│   ├── _index.yaml          # 仅受影响+被引用实体
│   └── {Entity}.md          # 仅变更实体（新增/修改字段）
└── modules/
    └── {序号}-{模块}.md     # 仅受影响的模块
```

> **增量原则**：未变更的模块、实体、接口**不生成**。这是增量文档，不是全量拷贝。

---

## 流程

### Step 1 — 读输入

并行读取：

1. `config.yaml` → 提取 `source.backend` 中 `enabled: true` 的项目 path、`environments.${current_environment}.backend[].url`
2. 代码变更文档 → 遍历 `tests/diff/doc/` 下所有 `.md` 文件（可能不存在）
3. 基线 `_manifest.yaml` + `API接口文档.md`
4. 基线 `02-analysis-plan/auth-analysis.md` + `framework-analysis.md`

### Step 2 — 判变更

参考 `references/diff-rules.md` 中的详细规则。

**若代码变更文档存在**：解析"2.接口变更"和"3.实体字段变更"节，提取变更清单。

**若代码变更文档不存在**：对每个 backend 项目执行 `git diff`（工作区 vs HEAD），用 CodeGraph 追踪变更的 Controller 方法 → 映射到具体 API 路径，生成精简变更清单（测试要点留空，后续模块文档生成时补充）。

对照基线 `_manifest.yaml`，将每个变更 API 归类为 `added` / `modified` / `deleted`。

### Step 3 — 确定生成范围

根据变更清单，确定：

- **受影响模块**：变更 API 所属的模块 → 需生成 `modules/{xx}.md`
- **受影响实体**：变更字段的实体 → 需生成 `entities/{Entity}.md`
- **被引用实体**：变更 API 的请求体/响应体引用的实体（未变更的照抄基线）
- **认证/框架**：检查变更文档第 5、6 节，无变更则主文档照抄基线

### Step 4 — 生成实体文档

仅处理受影响实体和被引用实体。按 `.opencode/references/实体类文档模板.md` 格式生成。

- **新增实体**：全量生成
- **修改实体**：照抄基线实体文档，仅更新变更的字段定义行
- **被引用但未变更的实体**：直接从基线 `entities/` 复制

生成规则参考 `api-doc-entities` skill 的 Agent 规则（CodeGraph 批量读取、JSON 键名优先级、必填判定、父类字段追踪）。**禁止逐条 codegraph_node**。

### Step 5 — 生成模块文档

仅处理受影响的模块。按 `.opencode/references/模块文档模板.md` 格式生成。

- **新增模块**：全量生成（等同于 api-doc-module 的单模块生成）
- **修改模块**：照抄基线模块文档，仅更新变更接口的段落。变更接口按 CodeGraph 当前源码重写，未变更接口段落原样保留
- **删除模块**：不生成，在报告中标记

注意：
- **断言生成（核心规则）**：代码变更文档中有"测试要点"的接口，必须在接口段中生成"#### 断言"节。断言是按项目断言规范（`.opencode/rules/testCase-standards.md` 断言-协议层/业务层/数据层）将测试要点转化为结构化验证规格，供下游 `api-doc-to-testcases` 直接映射为 YAML `expected` 块。
  - 节顺序：变更说明 → 请求/响应变更 → 断言 → 业务规则（如有）
  - 断言表格式：
    ```
    | # | 层级 | 断言项 | 预期值 | 断言消息 |
    |---|:---:|--------|--------|------|
    | 1 | 协议层 | HTTP 状态码 | 200 | "HTTP状态码应为200" |
    | 2 | 业务层 | code | 200 | "业务状态码应为200" |
    | 3 | 业务层 | msg | "查询成功" | "提示消息应为'查询成功'" |
    | 4 | 数据层 | rows[*].address 存在性 | 存在 | "每个岗位应包含address字段" |
    | 5 | 数据层 | rows[*].address 类型 | String | "address字段类型应为String" |
    | 6 | 数据层 | rows[*].address 值 | "LosAngeles" | "address字段值应为'LosAngeles'" |
    ```
  - 层级与 YAML 字段对应关系（供 `api-doc-to-testcases` 消费）：
    | 断言层级 | 断言项格式 | 映射到 YAML `expected` 字段 |
    |:---:|------|------|
    | 协议层 | `HTTP 状态码` | `status_code` |
    | 业务层 | `code` / `msg` | `business_code` / 校验消息 |
    | 数据层 | `{jsonPath} 存在性` | `data_exists: [{field}]` |
    | 数据层 | `{jsonPath} 类型` | `data_type: {field}: {type}` |
    | 数据层 | `{jsonPath} 值` | `data_equals: {field}: {value}` |
  - 从测试要点推导断言的规则：
    1. **每条测试要点至少拆出 3 条断言**：协议层 1 条（HTTP 状态码）+ 业务层 1 条（code）+ 数据层 ≥1 条（字段存在性/类型/值）
    2. 测试要点中预期结果写"HTTP 200，`rows[].address` 存在且值为 X" → 拆为 HTTP 状态码断言 + code 断言 + address 存在性断言 + address 值断言
    3. 回归类测试要点 → 生成对立面的否定断言（如"原有字段不受影响" → `data_exists` 包含 postId/postCode/postName 等原有字段）
    4. 异常类测试要点（无对应正向变更时）→ 协议层 + 业务层断言即可，数据层断言可选
  - 每个变更接口至少生成 5 条断言（协议 ≥1 + 业务 ≥2 + 数据 ≥2）
  - **业务规则**：
    - **modified 模块的变更接口**：检查基线模块文档中该接口是否有"#### 业务规则"节。有则照抄（规则未变，仍适用于增量用例）；无则不写
    - **业务逻辑变更**：代码变更文档中明确涉及业务逻辑变化时（如工作流异常匹配扩展），在断言之后写"#### 业务规则变更"节，以 before/after 表呈现。格式：
      ```
      | 规则 | 变更前 | 变更后 |
      |------|--------|--------|
      | 条件分支异常跳过 | 仅跳过 NULL_CONDITION_VALUE | 同时跳过 NULL_CONDITION_VALUE 和 NULL_SKIP_TYPE |
      ```
    - **新增接口**：不写业务规则（无基线可参照）
- 请求体/响应体有实体文件 → 引用 `entities/` 中的文件；无实体文件 → 展开字段表
- 错误响应追踪三层（DTO 校验 → Service → 全局异常），参照 `api-doc-module` skill 的铁律

### Step 6 — 组装主文档

1. 照抄基线 `API接口文档.md` 的项目信息、测试账号、响应包装、权限体系、认证头（除非认证/框架变更）
2. 更新模块概览表：仅列出受影响的模块行，其余模块不出现
3. 更新已知问题：新增增量特有问题（如"某实体字段变更影响下游"）
4. 文档版本号递增，生成日期更新为当天

### Step 7 — 写 _manifest.yaml

仅含受影响模块，每个模块记录实际变更的 route_indices。格式参照 baseline `_manifest.yaml`，但 `interface_count` 为**变更接口数**（非全量）。

---

## 禁止

- 生成未变更的模块或实体
- 把全量基线整体拷贝到 diff 目录
- 逐条 `codegraph_node`——用 `codegraph_explore` 批量读
- 修改基线 `03-api-docs/` 中的任何文件
