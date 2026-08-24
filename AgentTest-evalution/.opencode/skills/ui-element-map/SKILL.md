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
| `<el-button>文本</el-button>` / `<button>文本</button>` | `文本` → `{ type: role, role: button, name: "文本" }` |
| `data-testid="xxx"` 的输入/下拉 | 对应文案 → `{ type: data-testid, value: xxx }` |
| `<el-input placeholder="xx" />` | `xx` → `{ type: placeholder, value: "xx" }` |
| `<input aria-label="xx" />` | `xx` → `{ type: label, value: "xx" }` |
| `<el-select placeholder="xx">` | `xx` → `{ type: combobox, name: "xx" }` |

### Step 2 — 与场景文本对齐

读 `tests/baseline/_workflow/04-ui-scenarios/*.feature`，提取场景步骤中的文案（按钮/输入框/下拉框），**凡场景用到但地图缺失的文案必须补条目**——场景文案即 key。

### Step 3 — 生成草稿

- 保留现有 entries（不去重丢失）
- 新条目按「场景使用优先」排序
- 策略优先级：`data-testid > label > placeholder > role > text`；已知必失效的策略（如 EP 原生 select 的 combobox name 匹配）**不写**（参考企业经验库）

### Step 4 — 校验 + 人工确认

1. 运行 `python scripts/validate_elements.py`，必须通过
2. 输出变更清单（新增/修改条目），请用户确认后写入 `ui-profile/elements.yaml`

## 铁律

- 定位文案必须来自源码真实值，禁止猜测
- 不删除用户已确认的条目（只增改）
- 校验不通过禁止入库
