---
name: ui-requirements-analyze
description: 从 ui-requirements.md（5 节模板）解析全部价值信息，对照前端源码与后端 schema.sql，产出项目绑定四件套草稿（elements.yaml 元素地图 / business.yaml 业务配置 / db-asserts.yaml DB 断言映射 / api_sync_rules 接口规则），供人工确认后驱动完整 UI 测试链路。触发：/ui-requirements-analyze、解析需求、项目绑定、生成元素地图、生成DB断言映射、需求转配置、绑定新项目、requirements to profile。
---

# UI 需求分析（ui-requirements.md → 项目绑定四件套）

以 ui-requirements.md 为**唯一事实源**，AI 从中提取全部有价值信息，对照真实源码产出配置草稿。人工只做确认闸门。

## 核心思想

**新项目绑定 = 一次需求分析**：业务方只写一份 5 节模板需求文档，AI 解析后生成整个 ui-profile 配置层 + DB 断言映射 + 场景骨架。所有信息必须**有真实来源**（需求文档/前端源码/后端 schema），禁止凭空猜测。

## 输入

| 来源 | 说明 |
|------|------|
| 需求文档 | `tests/{mode}/_workflow/00-requirements/ui-requirements.md`（必填，缺失则中止并向用户索要） |
| 前端源码 | `config.yaml` 的 `source.frontend[].path` |
| 后端 schema | `config.yaml` 的 `source.backend[].path` 下的 `db/schema.sql`（或其下的 schema.sql） |
| 后端接口 | 已有 API 文档链路 `03-api-docs/`（优先）或后端 Controller 源码 |

## 输出（全部为 AI 草稿，人工确认后入库）

```
ui-profile/
├── elements.yaml        # 元素地图：文案即 key → 定位策略链（来自前端源码）
├── business.yaml        # busy 指示器/超时/种子保护/api_sync_rules/db 连接/重试
tests/{mode}/_workflow/00-requirements/
└── db-asserts.yaml      # DB 断言映射：需求第 3 节翻译 + schema 校验
```

## 分析流程

### 1. 解析需求文档（结构化提取）

| 需求章节 | 提取信息 | 流向 |
|---------|---------|------|
| 第 1 节 模块与版本 | 模块清单/页面路由 | 场景设计的模块划分 |
| 第 2 节 业务流程 | 每个业务流的操作步骤与业务反馈文案 | Gherkin 场景骨架 + elements.yaml 的「业务反馈断言」条目 |
| 第 3 节 数据变更映射 | **写操作 → 业务表/变更类型/关键字段与取值** | db-asserts.yaml（核心输入） |
| 第 4 节 字段明细 | 字段值来源（表单值/初始值/计算规则/枚举） | 场景填写值 + DB 断言语义 |
| 第 5 节 数据约束 | 唯一约束/种子清单/状态机/删除语义 | business.yaml（protected_seeds）+ 场景动态值策略 |

### 2. 读前端源码 → 元素地图草稿

对**场景步骤会交互的每个元素**，从源码提取真实定位策略，按可靠性排序：

| 元素类型 | 源码提取 | 策略链建议 |
|---------|---------|-----------|
| 输入框 | `<input placeholder="..." />` / `data-testid` | `data-testid` → `placeholder` → `label` → `role textbox` |
| 下拉框 | `<select data-testid>` / aria | `data-testid` → `role combobox` |
| 按钮/菜单/链接 | 可见文本 / `data-testid` | `role button/menuitem/link + name` → `text` |
| 业务反馈 | `ElMessage.success('...')` 等 | 记录为断言文案（key 用文案本身） |
| 复杂定位 | `.agent-card` 等 class | `css` 策略（写明选择器） |

铁律：
- **文案即 key**：场景步骤文案必须与 elements.yaml 的 key 完全一致
- **定位文案必须来自真实源码**（placeholder/testid/可见文本/提示字符串），禁止编造
- 每个元素至少 1 条策略；`data-testid` 存在时放第 1 级

### 3. 读后端 schema → DB 断言映射草稿

需求第 3 节的每一行「数据变更映射」翻译为 db-asserts.yaml 条目：

```yaml
db_asserts:
  - id: AGENT_CREATE_001                    # ID 规范: {模块}_{操作}_{序号}
    ui_action: 保存新增智能体表单            # 对应需求第 3 节「业务操作」
    table: agent_config                     # 物理表名（业务命名翻译 + schema 校验）
    expect_records: 1                       # 新增/修改=1；删除（无引用）=0；停用=1
    where:
      - { field: agent_code, from: var, ref: $code }   # 唯一键字段用场景变量
    assert_fields:
      - { field: agent_name, from: var, ref: $name }   # 值来自场景变量
      - { field: enabled, equals: 1 }                  # 值来自需求「关键字段与取值」
    sync: { api: "POST /api/agents", status: 200 }     # 来自后端接口
    schema_ref: schema.sql#agent_config
```

规则：
- 表名/字段名必须经 `lib/db_asserts.py::parse_schema_columns` 校验存在，对不上输出差异表
- **反向断言**：需求中「校验失败不落库」的操作（如必填校验拦截）→ `expect_records: 0`
- 删除语义按需求第 5 节：物理删除 → 0 条；软删除/停用 → 断言状态字段
- where 条件禁止为空；唯一键字段优先做 where（业务命名 → 物理列在差异表确认）
- 校验/编译复用 `lib/db_asserts.py`（load/structural_errors/compile/validate）

### 4. 读后端接口 → api_sync_rules 草稿

需求第 3 节每个写操作的「业务反馈」对应后端接口（来自 03-api-docs 或 Controller）：

```yaml
api_sync_rules:
  保存:      { path: /api/agents }          # 不写方法 = 任意方法（创建 POST / 编辑 PUT）
  确认删除:  { method: DELETE, path: /api/agents }
```

规则：
- 同一按钮文案可能对应多个方法（创建/编辑共用一个「保存」按钮）→ 省略 method（任意方法）
- 操作按钮文案必须与 elements.yaml 的 key 一致

### 5. 数据约束 → business.yaml 草稿

需求第 5 节：
- 种子清单 → `protected_seeds`（模式串，如 `["CHAT", "AGT_SEED_*"]`）
- 唯一约束 → 场景创建类值必须用动态值 `${ts}`/`${rand:8}`（写入场景设计指南）
- db 连接 → `db:` 段（host/port/user/password/database/charset，从后端 application-*.yml 读）

## 输出差异表（必须呈现给用户）

| 业务命名（需求文档） | 物理命名（schema/源码） | 结论 |
|---------------------|------------------------|------|
| 智能体配置表 | agent_config | 已确认 |
| 启用状态 | enabled | 已确认 |
| ... | ... | 需人工裁决（无法自动确认的） |

**人工确认闸门**：四件套草稿 + 差异表一并呈现，用户确认后入库。未经确认禁止写入 ui-profile/。

## 产物即证据

完成后验证（缺失则流程中止）：
- `ui-profile/elements.yaml` 存在且非空
- `ui-profile/business.yaml` 存在（含 api_sync_rules/db 段）
- `00-requirements/db-asserts.yaml` 存在（可先为子集，写操作覆盖优先）

## 与下游 skill 的关系

| 下游 | 消费什么 |
|------|---------|
| ui-scenario-design | elements.yaml（定位保障）、db-asserts.yaml（写操作引用映射 id）、第 5 节约束（动态值/状态机顺序） |
| feature-to-playwright | db-asserts.yaml（生成期校验 + 编译）、business.yaml（运行期） |
| ui-runner | business.yaml（db 连接/api 同步）、elements.yaml（命中报告） |

## 铁律

- 禁止 AI 凭空编造定位文案、表名、字段名（必须来自源码/schema）
- 禁止未经人工确认写入 ui-profile/（执行层确定性边界）
- 禁止把需求文档没有的写操作硬造映射（需求第 3 节没有的 → 不做 DB 断言）