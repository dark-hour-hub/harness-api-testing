---
name: ui-element-map
description: 从前端源码自动生成 ui-profile/elements.yaml 草稿（元素地图）。扫描 .vue 页面/组件的按钮文本、placeholder、data-testid、下拉框文案，输出结构化候选清单，人工确认后写入元素地图并校验。触发：/ui-element-map、生成元素地图、扫描前端元素、elements map。
---

# 元素地图生成器（前端源码 → elements.yaml 草稿）

从 `config.yaml` 的 `source.frontend[].path` 指向的前端工程，扫描真实定位信息，生成 `ui-profile/elements.yaml` 草稿。

## 输入

1. `config.yaml` — `source.frontend[].path`、`environments.<env>.frontend[].url`
2. 现有 `ui-profile/elements.yaml`（增量补全，保留已有条目）

## 产出

- `ui-profile/elements.yaml`（草稿，人工确认后入库）
- 校验：`python scripts/validate_elements.py` 必须通过

## 流程

### Step 1 — 扫描源码

用 Grep/Glob 扫描前端 `src/views/` 与 `src/components/` 下所有 `.vue` 文件，提取：

| 源码特征 | 元素地图条目 |
|---------|-------------|
| `<button>文本</button>` / `<a-button>文本</a-button>` | `文本` → `{ type: role, role: button, name: "文本" }` |
| `data-testid="xxx"` 的输入/下拉 | 见下方"data-testid 条目 key 推导" |
| `<input placeholder="xx" />` / `<el-input placeholder="xx" />` | `xx` → `{ type: placeholder, value: "xx" }` |
| `<input aria-label="xx" />` | `xx` → `{ type: label, value: "xx" }` |
| 原生 `<select>`（无 aria-label） | `data-testid` 优先；不写 combobox name 策略（企业经验库第 12 条：必失效） |

> 表格为示例模式，实际以前端源码 Grep 结果为准（如 Ant Design Vue 的 a-button、原生 button 均按可见文本提取）。

**data-testid 条目 key 推导**：key = 控件旁可见标签文本（el-form label/表头/placeholder），场景文案即 key 优先；源码无法确定可见标签时，在草稿中标注"key 待人工确认"，禁止凭结构猜测。

### Step 2 — 与场景文本对齐

优先输入：若存在 `04-ui-scenarios/_element-candidates.yaml`（ui-scenario-design 产出），以其为准核对补全，避免重复扫描推导。

读 `tests/baseline/_workflow/04-ui-scenarios/*.feature`，提取场景步骤中的文案（按钮/输入框/下拉框），**凡场景用到但地图缺失的文案必须补条目**——场景文案即 key。

### Step 3 — 生成草稿

- 保留现有 entries（不去重丢失）
- 新条目按「场景使用优先」排序
- 策略优先级：`data-testid > label > placeholder > role > text`；已知必失效的策略（如原生 select 的 combobox name 匹配）**不写**（参考企业经验库：`AgentTest-evalution/experience-library/PROJECT-KNOWN-ISSUES.md` 项目级 / `experience-library/ENTERPRISE-KNOWN-ISSUES.md` 企业级）

### Step 4 — 校验 + 人工确认

1. 生成草稿到 `ui-profile/elements.yaml.draft`（**不直接写 elements.yaml**）
2. 校验草稿：`python scripts/validate_elements.py ui-profile/elements.yaml.draft`（校验器支持参数指定路径），必须通过
3. 输出变更清单（新增/修改条目），请用户确认
4. 确认后：草稿内容写入 `ui-profile/elements.yaml`，再跑一次校验复验

## 铁律

- 定位文案必须来自源码真实值，禁止猜测
- 不删除用户已确认的条目（只增改）
- 校验不通过禁止入库
