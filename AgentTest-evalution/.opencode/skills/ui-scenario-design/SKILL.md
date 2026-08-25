---
name: ui-scenario-design
description: 业务需求驱动的 UI 测试场景设计。把业务需求/业务流程转换为 Gherkin Given-When-Then 场景文件（.feature），基于前端页面源码提取可访问性定位（按钮/输入框/菜单/提示文案）。触发：/ui-scenario-design、设计UI测试场景、业务需求转测试场景、生成Gherkin场景、ui场景设计、设计界面测试用例。
---

# UI 测试场景设计（业务需求 → Gherkin）

以业务需求/业务流程为输入，产出可执行的 Gherkin 场景文件（`.feature`），供 `feature-to-playwright` 生成测试脚本。

## 核心思想

**业务需求驱动**：不关心代码实现，只关心「用户在页面上做什么、看到什么」。

```
业务需求: 管理员可以新增图书
   → Gherkin: 打开首页 → 登录 → 进入图书管理 → 点击新增 → 填写表单 → 保存 → 看到成功提示
```

## 输入

| 来源 | 说明 |
|------|------|
| 业务需求文档 | `tests/baseline/_workflow/00-requirements/ui-requirements.md`（优先读取；不存在时使用用户直接提供的业务需求/流程文本） |
| 前端页面源码 | `config.yaml` 的 `source.frontend[].path` 指向的前端工程 |
| 前端地址 | `config.yaml` 的 `environments.<env>.frontend[].url` |
| 账号 | `config.yaml` 的 `environments.<env>.backend[].accounts`（登录角色/账号） |

## 输出

```
tests/baseline/_workflow/04-ui-scenarios/
├── 01-登录.feature
├── 02-图书管理.feature
├── 03-借阅管理.feature
└── _manifest.yaml          # 场景清单（模块 → feature 文件 + scenario 列表）
```

- `tests/baseline/_workflow/00-requirements/db-asserts.yaml`（可选，AI 从需求文档「数据变更映射」表翻译 + 测试工程师确认；场景关键写操作引用其 id；无映射时省略）

## 设计流程

1. **读业务需求**（从 `tests/baseline/_workflow/00-requirements/ui-requirements.md` 读取，缺失则向用户索要），拆解出可独立验证的业务流程（登录、新增、查询、借阅、删除……）
2. **读前端源码**，为每个交互提取定位信息（这一步是可靠性的关键）：
   - 按钮/菜单/链接 → 可见文本（`get_by_role` 的 name）
   - 输入框 → placeholder 或 label 文案
   - 提示/结果 → el-message 文案、表格单元格文本
3. **写 Gherkin**，每个业务流程一个 `Scenario`，用通用步骤 DSL（见 gherkin-guide）
4. **生成 `_manifest.yaml`** 清单
5. **输出元素候选清单**：场景设计过程中，凡**交互定位步骤**（点击按钮/菜单/链接、输入框、下拉框、上传、日期）的文案未在 `ui-profile/elements.yaml` 中精确匹配（key 一致）的，统一汇总写入 `04-ui-scenarios/_element-candidates.yaml`，并在设计汇报末尾附摘要表：

   | 文案 | 建议定位策略 | 来源源码位置 |
   |------|-------------|-------------|

   输出格式：`文本 → { type: xxx, ... }`（策略类型与 ui-element-map 一致）。文本断言步骤（应看到提示/页面应包含/表格应包含）不属于可定位元素，不进入候选清单。候选清单供 ui-element-map 或人工确认后补入元素地图——与 ui-element-map 的"场景文案即 key"对齐口径一致。
6. **翻译数据映射**：需求文档若有「数据变更映射」表，AI 对照后端 `db/schema.sql` 校验表/列存在性后产出 `00-requirements/db-asserts.yaml` 草稿，输出「业务命名 vs 物理命名」差异表；对不上时**不静默猜测**，由人工裁决后确认入库

## 通用步骤 DSL（见 references/gherkin-guide.md）

场景只用以下通用步骤，即可被 `feature-to-playwright` 的通用步骤库直接执行：

| 关键字 | 步骤模板 | 说明 |
|--------|----------|------|
| Given | `打开首页` 或 `打开首页 "<url>"` | 打开前端 |
| Given | `以账号 "<user>" 密码 "<pwd>" 登录` | UI 登录 |
| When | `点击菜单 "<文本>"` | 侧边栏菜单 |
| When | `点击按钮 "<文本>"` | 按钮（自动跳过 disabled） |
| When | `点击链接 "<文本>"` | 链接 |
| When | `在 "<字段>" 输入框中输入 "<值>"` | 输入框（placeholder/label 回退定位） |
| When | `等待 <N> 秒` | 固定等待 |
| Then | `应看到提示 "<文本>"` | el-message 提示 |
| Then | `页面应包含 "<文本>"` | 任意可见文本 |
| Then | `表格应包含 "<文本>"` | 表格单元格 |
| Then | `应看到按钮 "<文本>"` | 按钮可见 |

## 铁律

- **场景必须用通用步骤 DSL 编写**；通用库覆盖不了的特殊交互（拖拽、上传、复杂弹窗）才写专属步骤定义，并说明原因
- **场景独立**：每个 Scenario 应能独立理解（除非明确声明顺序依赖，如「先借阅后还书」）
- **定位信息必须来自真实页面源码**，禁止凭空猜测 placeholder/文案
- scenario 名称建议用英文（pytest-bdd 用 slug 生成测试函数名，中文名会被 slug 化），业务描述放在步骤和 feature 描述里

## 产物即证据

完成后验证：
- `04-ui-scenarios/` 下存在至少一个 `.feature` 文件
- `_manifest.yaml` 存在且场景数 > 0
