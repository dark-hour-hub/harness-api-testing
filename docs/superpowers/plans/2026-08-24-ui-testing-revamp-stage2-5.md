# UI 测试链路重构 · 阶段 2~5（地图生成器 / 数据闭环 / 稳定性效率 / 迭代闭环）实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 完成阶段 2~5：元素地图自动生成与校验、数据闭环（动态值/种子保护/重置适配器）、稳定性与效率（busy/API 同步/重试/并行/tag）、迭代闭环（版本指纹/探针/命中率报告/定位修复建议）。

**Architecture:** 延续阶段 1 的结构——`lib/ui_profile.py` 承载纯逻辑（动态值展开/种子保护/校验，均可单测）；conftest 模板增量集成新 DSL 步骤与同步机制；`run_ui.py` 增加并行/tag/指纹/命中率报告；新增 `scripts/validate_elements.py`、`scripts/ui_reset.py`、`scripts/ui_fingerprint.py`；skill 文档更新（ui-element-map 新建、ui-scenario-design/post-run-analysis 扩展）。

**Tech Stack:** Python 3.12、pytest、pytest-bdd + Playwright、PyYAML、concurrent.futures。

**依赖上游设计:** `docs/superpowers/specs/2026-08-24-ui-testing-revamp-design.md`（阶段 2~5）。阶段 1 已完成（元素地图解析器、conftest 地图优先、生成器相对路径）。

**注意：** 本计划 14 个任务严格顺序执行（conftest/run_ui 是连续修改的文件）。每个任务 TDD：先测试后实现。

---

### Task 1: 元素地图校验器 validate_elements.py（TDD）

**Files:**
- Create: `AgentTest-evalution/scripts/validate_elements.py`
- Create: `AgentTest-evalution/tests/unit/test_validate_elements.py`

- [ ] **Step 1: 先写测试（红）**

```python
# -*- coding: utf-8 -*-
"""scripts/validate_elements.py 单元测试"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from validate_elements import validate  # noqa: E402

GOOD = """elements:
  新增智能体:
    strategies:
      - { type: role, role: button, name: "新增智能体" }
  风险等级:
    strategies:
      - { type: data-testid, value: agent-risk-tier }
"""


def test_valid_map_no_errors(tmp_path):
    p = tmp_path / "elements.yaml"
    p.write_text(GOOD, encoding="utf-8")
    assert validate(p) == []


def test_unknown_strategy_type(tmp_path):
    p = tmp_path / "elements.yaml"
    p.write_text(
        "elements:\n  x:\n    strategies:\n      - { type: nope, value: a }\n",
        encoding="utf-8",
    )
    errors = validate(p)
    assert len(errors) == 1 and "nope" in errors[0]


def test_missing_strategies(tmp_path):
    p = tmp_path / "elements.yaml"
    p.write_text("elements:\n  x:\n    strategies: []\n", encoding="utf-8")
    errors = validate(p)
    assert len(errors) == 1 and "strategies" in errors[0]


def test_role_strategy_needs_name(tmp_path):
    p = tmp_path / "elements.yaml"
    p.write_text(
        "elements:\n  x:\n    strategies:\n      - { type: role, role: button }\n",
        encoding="utf-8",
    )
    errors = validate(p)
    assert len(errors) == 1 and "name" in errors[0]


def test_duplicate_keys(tmp_path):
    p = tmp_path / "elements.yaml"
    p.write_text(
        "elements:\n  a:\n    strategies:\n      - { type: text, value: a }\n"
        "  a:\n    strategies:\n      - { type: text, value: b }\n",
        encoding="utf-8",
    )
    assert any("重复" in e for e in validate(p))


def test_missing_file(tmp_path):
    assert validate(tmp_path / "not-exists.yaml") == []
```

- [ ] **Step 2: 运行确认失败**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/unit/test_validate_elements.py -v`（AgentTest-evalution 目录）
Expected: 全 FAIL 于 ModuleNotFoundError / ImportError

- [ ] **Step 3: 实现**

```python
# -*- coding: utf-8 -*-
"""
validate_elements.py — 校验 ui-profile/elements.yaml 结构与策略类型

供 ui-element-map skill 生成后与人工确认前调用；返回错误清单（空 = 通过）。
"""
from pathlib import Path

import yaml

KNOWN_TYPES = {"data-testid", "placeholder", "label", "role", "combobox", "css", "text"}


def validate(path: Path) -> list:
    """返回错误信息列表；文件不存在返回空（最小绑定合法）。"""
    path = Path(path)
    if not path.exists():
        return []
    errors = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        return [f"YAML 解析失败: {e}"]

    elements = data.get("elements") or {}
    seen = set()
    for key, entry in elements.items():
        if key in seen:
            errors.append(f"元素 key 重复: {key}")
        seen.add(key)
        if not key or not str(key).strip():
            errors.append("存在空 key")
        strategies = (entry or {}).get("strategies") or []
        if not strategies:
            errors.append(f"元素「{key}」无 strategies")
        for s in strategies:
            stype = s.get("type")
            if stype not in KNOWN_TYPES:
                errors.append(f"元素「{key}」未知策略类型: {stype}")
            if stype == "role" and not s.get("name"):
                errors.append(f"元素「{key}」role 策略缺 name")
    return errors


if __name__ == "__main__":
    import sys
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "ui-profile" / "elements.yaml"
    errs = validate(target)
    if errs:
        print(f"[validate_elements] 校验失败: {target}")
        for e in errs:
            print(f"  - {e}")
        sys.exit(1)
    print(f"[validate_elements] 校验通过: {target}")
```

- [ ] **Step 4: 运行确认通过（并顺手校验现有 ui-profile）**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/unit/test_validate_elements.py -v`
Expected: 6 passed
Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe scripts/validate_elements.py`（AgentTest-evalution 目录）
Expected: `[validate_elements] 校验通过: ...ui-profile/elements.yaml`

- [ ] **Step 5: 提交**

```bash
git add AgentTest-evalution/scripts/validate_elements.py AgentTest-evalution/tests/unit/test_validate_elements.py
git commit -m "feat(ui): 元素地图校验器 validate_elements.py"
```

---

### Task 2: 新建 ui-element-map skill

**Files:**
- Create: `AgentTest-evalution/.opencode/skills/ui-element-map/SKILL.md`

- [ ] **Step 1: 创建 SKILL.md**

```markdown
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
```

- [ ] **Step 2: 提交**

```bash
git add AgentTest-evalution/.opencode/skills/ui-element-map/SKILL.md
git commit -m "feat(ui): ui-element-map skill（前端源码→元素地图草稿）"
```

---

### Task 3: ui-scenario-design skill 增加元素候选输出

**Files:**
- Modify: `AgentTest-evalution/.opencode/skills/ui-scenario-design/SKILL.md`

- [ ] **Step 1: 在设计流程中追加一步（在"生成 _manifest.yaml 清单"之后）**

```markdown
### 4.5 输出元素候选清单

场景设计过程中，凡步骤文案未在 `ui-profile/elements.yaml` 中收录的，统一汇总输出（设计报告末尾）：

| 文案 | 建议定位策略 | 来源源码位置 |
|------|-------------|-------------|

输出格式：`文本 → { type: xxx, ... }`，供 `ui-element-map` skill 或人工确认后补入元素地图。这是"场景与地图同步"的闭环环节。
```

- [ ] **Step 2: 提交**

```bash
git add AgentTest-evalution/.opencode/skills/ui-scenario-design/SKILL.md
git commit -m "docs(ui): ui-scenario-design 增加元素候选输出环节"
```

---

### Task 4: 动态值展开与种子保护（TDD）

**Files:**
- Modify: `AgentTest-evalution/lib/ui_profile.py`
- Create: `AgentTest-evalution/tests/unit/test_vars_seed.py`

- [ ] **Step 1: 先写测试（红）**

```python
# -*- coding: utf-8 -*-
"""lib/ui_profile.py 动态值展开与种子保护单元测试"""
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))

from ui_profile import expand_vars, seed_protected  # noqa: E402


def test_rand_expansion():
    v = expand_vars("AGT_${rand:8}", base_time=datetime(2026, 8, 24))
    assert v.startswith("AGT_") and len(v) == 12
    assert all(c.isalnum() for c in v[4:])


def test_rand_default_length():
    v = expand_vars("${rand}")
    assert len(v) == 8


def test_uuid_expansion():
    v = expand_vars("TC_${uuid}")
    assert v.startswith("TC_") and len(v) == 15


def test_ts_expansion():
    from datetime import timezone, timedelta
    tz8 = timezone(timedelta(hours=8))
    v = expand_vars("${ts}", base_time=datetime(2026, 8, 24, 10, 30, 0, tzinfo=tz8))
    assert v == "1787625000000"


def test_date_relative():
    v = expand_vars("${date:+1d}", base_time=datetime(2026, 8, 24))
    assert v == "2026-08-25"


def test_date_no_delta():
    v = expand_vars("${date}", base_time=datetime(2026, 8, 24))
    assert v == "2026-08-24"


def test_non_string_unchanged():
    assert expand_vars(123) == 123
    assert expand_vars("no vars here") == "no vars here"


def test_seed_protected_exact():
    assert seed_protected("BANK_AGENT", ["BANK_AGENT", "AGT_SEED_*"])


def test_seed_protected_wildcard():
    assert seed_protected("AGT_SEED_001", ["BANK_AGENT", "AGT_SEED_*"])


def test_seed_protected_not_matched():
    assert not seed_protected("AGT_UI_20260824", ["BANK_AGENT", "AGT_SEED_*"])
    assert not seed_protected("x", [])
```

- [ ] **Step 2: 运行确认失败**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/unit/test_vars_seed.py -v`
Expected: FAIL（ImportError: cannot import name expand_vars）

- [ ] **Step 3: 在 lib/ui_profile.py 追加实现**（文件末尾追加；顶部补 `import fnmatch, random, re, string, uuid, datetime` 相关导入）

```python
_VAR_RE = re.compile(r"\$\{(rand|uuid|ts|date)(?::([^}]*))?\}")


def expand_vars(value, base_time=None):
    """场景值中的动态值占位符展开（确定性执行层）：

    - ${rand:8}    N 位随机大写字母数字（默认 8）
    - ${uuid}      UUID 前 12 位大写（去连字符）
    - ${ts}        13 位毫秒时间戳
    - ${date:+Nd}  相对日期 yyyy-MM-dd（+N/-N 天，可省略）
    """
    if not isinstance(value, str):
        return value
    base = base_time or datetime.datetime.now()

    def _repl(m):
        kind, arg = m.group(1), m.group(2)
        if kind == "rand":
            n = int(arg) if arg and arg.isdigit() else 8
            return "".join(random.choices(string.ascii_uppercase + string.digits, k=n))
        if kind == "uuid":
            return str(uuid.uuid4()).replace("-", "")[:12].upper()
        if kind == "ts":
            return str(int(base.timestamp() * 1000))
        if kind == "date":
            days = 0
            if arg and arg[0] in "+-" and arg[1:].isdigit():
                days = int(arg)
            return (base + datetime.timedelta(days=days)).strftime("%Y-%m-%d")
        return m.group(0)

    return _VAR_RE.sub(_repl, value)


def seed_protected(value, protected_seeds):
    """值命中种子保护清单（支持 fnmatch 通配）→ True"""
    if not protected_seeds or not isinstance(value, str):
        return False
    return any(fnmatch.fnmatch(value, p) or value == p for p in protected_seeds)
```

（`datetime` 以 `import datetime` 形式导入，`datetime.datetime.now()` 调用。）

- [ ] **Step 4: 运行确认通过**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/unit/test_vars_seed.py -v`
Expected: 10 passed

- [ ] **Step 5: 提交**

```bash
git add AgentTest-evalution/lib/ui_profile.py AgentTest-evalution/tests/unit/test_vars_seed.py
git commit -m "feat(ui): 动态值占位符展开与种子保护判定"
```

---

### Task 5: conftest 集成动态值与种子保护

**Files:**
- Modify: `AgentTest-evalution/.opencode/skills/feature-to-playwright/template/conftest.py`

- [ ] **Step 1: 追加导入与辅助函数**

在 `from ui_profile import load_profile, resolve_element` 处改为：

```python
    from ui_profile import load_profile, resolve_element, expand_vars, seed_protected
```

在 `_action_timeout()` 函数之后追加：

```python
def _assert_not_seed(text: str) -> None:
    """操作目标命中种子保护清单 → 直接报错拦截（企业经验库第 11 条硬约束化）"""
    if PROFILE is None:
        return
    seeds = PROFILE["business"].get("protected_seeds", [])
    if seed_protected(text, seeds):
        raise AssertionError(f"禁止操作种子数据（protected_seeds 命中）: {text}")
```

- [ ] **Step 2: 修改 `fill_field` 步骤（值先展开动态值）**

```python
@given(parsers.parse('在 "{field}" 输入框中输入 "{value}"'))
@when(parsers.parse('在 "{field}" 输入框中输入 "{value}"'))
def fill_field(page, field, value):
    _fill_input(page, field, expand_vars(value))
```

- [ ] **Step 3: 修改 `_click_button` 入口（种子保护）**

在 `_click_button(page, text)` 函数体第一行加：

```python
    _assert_not_seed(text)
```

（map 命中与回退两分支均被覆盖。）

- [ ] **Step 4: 提交**

```bash
git add AgentTest-evalution/.opencode/skills/feature-to-playwright/template/conftest.py
git commit -m "feat(ui): conftest 集成动态值展开与种子保护拦截"
```

---

### Task 6: conftest 新增 DSL 步骤（表格行/对话框/上传/日期）

**Files:**
- Modify: `AgentTest-evalution/.opencode/skills/feature-to-playwright/template/conftest.py`

- [ ] **Step 1: 在 `_click_button` 定义之后、Given 步骤区之前追加通用点击辅助**

```python
def _wait_busy_gone(page):
    """等待所有 busy 指示器消失（business.yaml busy_indicators）"""
    if PROFILE is None:
        return
    busy = PROFILE["business"].get("busy_indicators", [])
    if not busy:
        return
    timeout = PROFILE["business"].get("timeouts", {}).get("busy", 15000)
    for sel in busy:
        try:
            page.locator(sel).first.wait_for(state="detached", timeout=timeout)
        except Exception:
            pass
```

- [ ] **Step 2: 在 When 步骤区追加 4 个新步骤（放在 `click_add_test_case_until_form` 之前）**

```python
@when(parsers.parse('在表格行包含 "{row_text}" 中点击 "{btn}"'))
def click_in_row(page, row_text, btn):
    _assert_not_seed(row_text)
    row = page.get_by_role("row", name=re.compile(re.escape(row_text))).first
    row.get_by_role("button", name=btn).first.click(timeout=5000)
    _wait_busy_gone(page)


@when(parsers.parse('在对话框 "{title}" 中点击 "{btn}"'))
def click_in_dialog(page, title, btn):
    dialog = page.get_by_role("dialog").filter(has_text=title).first
    dialog.get_by_role("button", name=btn).first.click(timeout=5000)
    _wait_busy_gone(page)


@when(parsers.parse('上传文件到 "{field}" 文件 "{path}"'))
def upload_file(page, field, path):
    if PROFILE is not None:
        el = PROFILE["map"].lookup(field)
        if el is not None:
            loc, idx = resolve_element(page, el, _action_timeout())
            if loc is not None:
                _record_hit(field, idx)
                file_input = loc.first.locator("xpath=ancestor-or-self::*[@type='file']")
                if file_input.count() == 0:
                    file_input = page.locator('input[type="file"]').first
                file_input.set_input_files(str(_project_root() / path))
                return
    page.locator('input[type="file"]').first.set_input_files(str(_project_root() / path))


@when(parsers.parse('在 "{field}" 选择日期 "{value}"'))
def fill_date(page, field, value):
    _fill_input(page, field, expand_vars(value))
```

注意：`re` 模块已在文件头导入（模板已有 `import re`）。

- [ ] **Step 3: 在既有点击步骤（click_menu/click_link/click_in_agent_card）点击后补 `_wait_busy_gone(page)`**

- `click_menu`：`page.wait_for_load_state("networkidle")` 行改为保留，并在其后加 `_wait_busy_gone(page)`
- `click_link`：点击后加 `_wait_busy_gone(page)`
- `click_in_agent_card`：`card.get_by_role(...).click(...)` 后加 `_wait_busy_gone(page)`
- `_click_button`：两个分支点击成功后各加 `_wait_busy_gone(page)`

- [ ] **Step 4: 提交**

```bash
git add AgentTest-evalution/.opencode/skills/feature-to-playwright/template/conftest.py
git commit -m "feat(ui): 新增表格行/对话框/上传/日期 DSL 步骤与 busy 等待"
```

---

### Task 7: profile 扩展（protected_seeds / api_sync_rules / retry）

**Files:**
- Modify: `AgentTest-evalution/ui-profile/business.yaml`
- Modify: `AgentTest-evalution/ui-profile-template/business.yaml`

- [ ] **Step 1: 修改 `ui-profile/business.yaml`**（保留原有内容，追加）

```yaml
protected_seeds: ["BANK_AGENT", "AGT_SEED_*"]
api_sync_rules:
  保存:
    method: POST
    path: /api/agents
retry: 1
```

- [ ] **Step 2: 修改 `ui-profile-template/business.yaml`**（注释示例化，供新项目参考）

```yaml
# protected_seeds: ["SEED_CODE_*"]   # 种子保护清单：操作命中即报错（阶段 3）
# api_sync_rules:                    # UI 操作 → 等待的后端请求（阶段 4）
#   保存:
#     method: POST
#     path: /api/xxx
# retry: 1                            # 定位类失败确定性重试次数（阶段 4）
```

- [ ] **Step 3: 提交**

```bash
git add AgentTest-evalution/ui-profile/business.yaml AgentTest-evalution/ui-profile-template/business.yaml
git commit -m "feat(ui): profile 增加种子保护/api 同步规则/重试配置"
```

---

### Task 8: 重置适配器 ui_reset.py + 清理模板

**Files:**
- Create: `AgentTest-evalution/scripts/ui_reset.py`
- Create: `AgentTest-evalution/ui-profile/reset/cleanup_template.sql`
- Create: `AgentTest-evalution/ui-profile-template/reset/cleanup_template.sql`
- Create: `AgentTest-evalution/tests/unit/test_ui_reset.py`

- [ ] **Step 1: 先写测试（红）**

```python
# -*- coding: utf-8 -*-
"""scripts/ui_reset.py 单元测试"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from ui_reset import build_plan, parse_confirmation  # noqa: E402

SQL = """-- 智能体评测平台 UI 测试清理模板（FK 逆序）
-- 运行期数据判定：created_by 为 ui-test 或 code 以 AGT_UI_/TC_UI_/SCHEME_UI_ 开头
DELETE FROM agent WHERE code LIKE 'AGT_UI_%' OR code LIKE 'AGT_SEED_%';
DELETE FROM indicator WHERE code LIKE 'IND_UI_%';
"""


def test_build_plan(tmp_path):
    p = tmp_path / "cleanup_template.sql"
    p.write_text(SQL, encoding="utf-8")
    plan = build_plan(p)
    assert len(plan["statements"]) == 2
    assert "agent" in plan["tables"]
    assert "indicator" in plan["tables"]


def test_build_plan_missing_file(tmp_path):
    plan = build_plan(tmp_path / "nope.sql")
    assert plan["statements"] == [] and plan["tables"] == []


def test_parse_confirmation():
    assert parse_confirmation("yes") is True
    assert parse_confirmation("y") is True
    assert parse_confirmation("no") is False
    assert parse_confirmation("") is False
```

- [ ] **Step 2: 运行确认失败**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/unit/test_ui_reset.py -v`
Expected: FAIL（ImportError）

- [ ] **Step 3: 实现 ui_reset.py**

```python
# -*- coding: utf-8 -*-
"""
ui_reset.py — UI 测试环境重置适配器（跑前清理 + 种子恢复）

流程：读取 ui-profile/reset/cleanup_template.sql → 解析清理计划 →
人工确认（--yes 跳过）→ 执行（--dry-run 只打印不执行）。

执行方式（按 business.yaml reset.exec 配置）：
  - ""（默认）：只打印 SQL 供人工执行（安全默认）
  - 形如 "mysql -u root -p < {sql}"：用 {sql} 占位符替换后 subprocess 执行
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def build_plan(sql_path: Path) -> dict:
    """解析清理模板：提取非注释 DELETE/TRUNCATE 语句与其目标表。"""
    sql_path = Path(sql_path)
    if not sql_path.exists():
        return {"statements": [], "tables": []}
    text = sql_path.read_text(encoding="utf-8")
    statements = []
    tables = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("--"):
            continue
        statements.append(stripped)
        m = re.search(r"\b(?:DELETE FROM|TRUNCATE)\s+(\w+)", stripped, re.IGNORECASE)
        if m and m.group(1) not in tables:
            tables.append(m.group(1))
    return {"statements": statements, "tables": tables}


def parse_confirmation(answer: str) -> bool:
    return answer.strip().lower() in ("yes", "y")


def main():
    parser = argparse.ArgumentParser(description="UI 测试环境重置（跑前清理）")
    parser.add_argument("--profile", default=str(PROJECT_ROOT / "ui-profile"),
                        help="profile 目录（默认 ui-profile/）")
    parser.add_argument("--dry-run", action="store_true", help="只展示清理计划，不执行")
    parser.add_argument("--yes", action="store_true", help="跳过确认")
    args = parser.parse_args()

    profile = Path(args.profile)
    sql_path = profile / "reset" / "cleanup_template.sql"
    plan = build_plan(sql_path)

    print("=" * 60)
    print(f"[ui_reset] 清理模板: {sql_path}")
    if not plan["statements"]:
        print("[ui_reset] 无清理语句（模板为空或不存在）——跳过重置")
        return
    print(f"[ui_reset] 将执行 {len(plan['statements'])} 条语句，涉及表: {', '.join(plan['tables'])}")
    for s in plan["statements"]:
        print(f"  > {s}")

    if args.dry_run:
        print("[ui_reset] --dry-run：未执行，请人工核对后执行或去掉 --dry-run")
        return

    if not args.yes:
        answer = input("确认执行以上清理？（yes/no）: ")
        if not parse_confirmation(answer):
            print("[ui_reset] 已取消")
            return

    # 执行方式：默认打印供人工执行；配置了 reset.exec 则执行
    try:
        import yaml
        business = {}
        bp = profile / "business.yaml"
        if bp.exists():
            business = yaml.safe_load(bp.read_text(encoding="utf-8")) or {}
    except Exception:
        business = {}
    exec_cmd = (business.get("reset") or {}).get("exec", "")
    if not exec_cmd:
        print("[ui_reset] 未配置 reset.exec，以下语句请人工在测试库执行：")
        for s in plan["statements"]:
            print(f"  {s}")
        return
    cmd = exec_cmd.replace("{sql}", str(sql_path))
    print(f"[ui_reset] 执行: {cmd}")
    result = subprocess.run(cmd, shell=True, encoding="utf-8", errors="replace")
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: 运行确认通过**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/unit/test_ui_reset.py -v`
Expected: 3 passed

- [ ] **Step 5: 创建清理模板**（两个目录各一份，内容相同）

```sql
-- 智能体评测平台 UI 测试清理模板（FK 逆序，只删运行期数据）
-- 判定约定：测试自建数据 code 前缀 AGT_UI_ / TC_UI_ / SCHEME_UI_ / TASK_UI_ / IND_UI_
DELETE FROM evaluation_task_result WHERE task_id IN (SELECT id FROM evaluation_task WHERE code LIKE 'TASK_UI_%');
DELETE FROM evaluation_task WHERE code LIKE 'TASK_UI_%';
DELETE FROM evaluation_scheme WHERE scheme_code LIKE 'SCHEME_UI_%';
DELETE FROM test_case WHERE code LIKE 'TC_UI_%';
DELETE FROM agent WHERE code LIKE 'AGT_UI_%';
DELETE FROM indicator WHERE code LIKE 'IND_UI_%';
```

（表名按被测项目实际 schema 调整；仅作模板示例。）

- [ ] **Step 6: 提交**

```bash
git add AgentTest-evalution/scripts/ui_reset.py AgentTest-evalution/tests/unit/test_ui_reset.py AgentTest-evalution/ui-profile/reset/ AgentTest-evalution/ui-profile-template/reset/
git commit -m "feat(ui): 重置适配器 ui_reset.py 与清理模板"
```

---

### Task 9: conftest 稳定性（API 同步 + 确定性重试）

**Files:**
- Modify: `AgentTest-evalution/.opencode/skills/feature-to-playwright/template/conftest.py`

- [ ] **Step 1: 在 `_wait_busy_gone` 之后追加两个辅助**

```python
def _api_sync(page, step_text):
    """操作后等待对应后端请求返回（business.yaml api_sync_rules）"""
    if PROFILE is None:
        return
    rule = PROFILE["business"].get("api_sync_rules", {}).get(step_text)
    if not rule:
        return
    timeout = PROFILE["business"].get("timeouts", {}).get("api_sync", 15000)
    method = rule.get("method", "GET")
    path = rule.get("path", "")
    try:
        page.wait_for_response(
            lambda r: r.request.method == method and path in r.url,
            timeout=timeout,
        )
    except Exception:
        pass


def _retry_count() -> int:
    if PROFILE is None:
        return 1
    return int(PROFILE["business"].get("retry", 1))
```

- [ ] **Step 2: 点击统一走重试 + 同步**——将 `_click_button` 整体替换为：

```python
def _click_button(page, text):
    """点击第一个 enabled 的按钮（跳过 disabled）；元素地图优先；失败确定性重试"""
    _assert_not_seed(text)
    attempts = _retry_count() + 1
    last_err = None
    for _ in range(attempts):
        try:
            if PROFILE is not None:
                el = PROFILE["map"].lookup(text)
                if el is not None:
                    loc, idx = resolve_element(page, el, _action_timeout())
                    if loc is not None:
                        _record_hit(text, idx)
                        for candidate in loc.all():
                            try:
                                if candidate.is_enabled():
                                    candidate.click()
                                    _wait_busy_gone(page)
                                    _api_sync(page, text)
                                    return
                            except Exception:
                                continue
                        raise AssertionError(f"未找到可点击的按钮「{text}」")
            loc = page.get_by_role("button", name=text)
            for candidate in loc.all():
                try:
                    if candidate.is_enabled():
                        candidate.click()
                        _wait_busy_gone(page)
                        _api_sync(page, text)
                        return
                except Exception:
                    continue
            loc.first.click()
            _wait_busy_gone(page)
            _api_sync(page, text)
            return
        except AssertionError:
            raise
        except Exception as e:
            last_err = e
            page.wait_for_timeout(500)
    if last_err is not None:
        raise last_err
    raise AssertionError(f"未找到可点击的按钮「{text}」")
```

- [ ] **Step 3: 提交**

```bash
git add AgentTest-evalution/.opencode/skills/feature-to-playwright/template/conftest.py
git commit -m "feat(ui): API 级同步与确定性重试"
```

---

### Task 10: run_ui.py 并行 + tag 分层

**Files:**
- Modify: `AgentTest-evalution/.opencode/skills/ui-runner/scripts/run_ui.py`

- [ ] **Step 1: 修改 main()：增加 --parallel 与 --tags 参数、并行执行**

在 `parser.add_argument("-k", "--keyword", default=None)` 后追加：

```python
    parser.add_argument("--parallel", type=int, default=2, help="并行执行的 feature 进程数（默认 2）")
    parser.add_argument("--tags", default=None, help="pytest -m 表达式（如 smoke）")
```

将 `run_pytest_file` 的 pytest 命令构建处（`cmd` 组装后）追加 tag 支持：

```python
    if tags:
        cmd.extend(["-m", tags])
```

（`run_pytest_file` 签名增加 `tags: str = None` 参数。）

将 main() 中顺序执行循环 `for i, test_file in enumerate(test_files):` 整体替换为并行版本：

```python
    from concurrent.futures import ThreadPoolExecutor, as_completed

    total_start = time.time()
    all_results = []
    crashed = []
    lock = threading.Lock()
    progress = {"done": 0}

    def _run_one(test_file):
        file_name = os.path.basename(test_file)
        junit_xml = os.path.join(cache_dir, f"results_{file_name}.xml")
        exit_code, elapsed, stdout, stderr = run_pytest_file(
            test_file, junit_xml, base_url, screenshot_dir,
            args.headed, args.keyword, args.tags,
        )
        with lock:
            progress["done"] += 1
            if os.path.exists(junit_xml):
                module_name = os.path.splitext(file_name)[0]
                if module_name.startswith("test_"):
                    module_name = module_name[5:]
                data = parse_junit_xml(junit_xml, module_name)
                s = data["summary"]
                if s["tests"] > 0:
                    all_results.append(data)
                    status = "PASS" if s["failures"] == 0 and s["errors"] == 0 else "FAIL"
                    print(f"  [{progress['done']}/{len(test_files)}] {file_name:<35} {status:>6}  "
                          f"{s['tests']:>2} scenarios | {s['failures']:>2} failed | {elapsed}s")
                    return
                print(f"  [{progress['done']}/{len(test_files)}] {file_name:<35} {'EMPTY':>6}  (无匹配场景)")
                return
            print(f"  [{progress['done']}/{len(test_files)}] {file_name:<35} {'ERROR':>6}  未生成报告 (exit={exit_code})")
            for line in (stderr or "").strip().split("\n")[-6:]:
                print(f"         {line}")
            crashed.append(file_name)

    workers = max(1, args.parallel)
    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(_run_one, test_files))
```

文件头补 `import threading`。

- [ ] **Step 2: feature 加 @smoke tag**——在 `04-ui-scenarios/02-agent-projects.feature` 的 `create agent` 场景与 `03-indicator-config.feature` 的 `indicator page elements` 场景前各加一行 `@smoke`

- [ ] **Step 3: 提交**

```bash
git add AgentTest-evalution/.opencode/skills/ui-runner/scripts/run_ui.py AgentTest-evalution/tests/baseline/_workflow/04-ui-scenarios/02-agent-projects.feature AgentTest-evalution/tests/baseline/_workflow/04-ui-scenarios/03-indicator-config.feature
git commit -m "feat(ui): run_ui 并行执行与 tag 分层"
```

---

### Task 11: 版本指纹 ui_fingerprint.py + 集成

**Files:**
- Create: `AgentTest-evalution/scripts/ui_fingerprint.py`
- Create: `AgentTest-evalution/tests/unit/test_ui_fingerprint.py`
- Modify: `AgentTest-evalution/.opencode/skills/ui-runner/scripts/run_ui.py`

- [ ] **Step 1: 先写测试（红）**

```python
# -*- coding: utf-8 -*-
"""scripts/ui_fingerprint.py 单元测试"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from ui_fingerprint import fingerprint_dir  # noqa: E402


def test_fingerprint_stable(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("x", encoding="utf-8")
    fp1 = fingerprint_dir(tmp_path)
    fp2 = fingerprint_dir(tmp_path)
    assert fp1 == fp2 and len(fp1) == 64


def test_fingerprint_changes_on_modify(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("x", encoding="utf-8")
    fp1 = fingerprint_dir(tmp_path)
    f.write_text("y", encoding="utf-8")
    assert fingerprint_dir(tmp_path) != fp1


def test_fingerprint_missing_dir(tmp_path):
    assert fingerprint_dir(tmp_path / "nope") == ""
```

- [ ] **Step 2: 运行确认失败**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/unit/test_ui_fingerprint.py -v`
Expected: FAIL（ImportError）

- [ ] **Step 3: 实现 ui_fingerprint.py**

```python
# -*- coding: utf-8 -*-
"""
ui_fingerprint.py — 前端版本指纹

对前端工程 src 目录做稳定哈希（文件名+内容），变化即代表前端发版。
供 UI 测试跑前比对：指纹变化 → 提示先跑探针/检查元素地图健康度。
"""
import argparse
import hashlib
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def fingerprint_dir(directory: Path) -> str:
    """对目录下所有文件（排除 .git/__pycache__/node_modules/dist）做 sha256。"""
    directory = Path(directory)
    if not directory.exists():
        return ""
    h = hashlib.sha256()
    files = sorted(
        p for p in directory.rglob("*")
        if p.is_file()
        and not any(part in {".git", "__pycache__", "node_modules", "dist"} for part in p.parts)
    )
    for p in files:
        try:
            rel = str(p.relative_to(directory))
            h.update(rel.encode("utf-8"))
            h.update(p.read_bytes()[: 1 << 20])
        except OSError:
            continue
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description="前端版本指纹")
    parser.add_argument("--frontend", default="",
                        help="前端工程路径（默认读 config.yaml source.frontend）")
    parser.add_argument("--store", default="", help="指纹存储文件路径")
    args = parser.parse_args()

    frontend = args.frontend
    if not frontend:
        import yaml
        config = yaml.safe_load((PROJECT_ROOT / "config.yaml").read_text(encoding="utf-8")) or {}
        frontends = config.get("source", {}).get("frontend", [])
        frontend = frontends[0]["path"] if frontends else ""
    if not frontend:
        print("[ui_fingerprint] 未配置前端路径")
        sys.exit(1)

    fp = fingerprint_dir(Path(frontend))
    if not fp:
        print("[ui_fingerprint] 前端目录不存在")
        sys.exit(1)
    print(f"[ui_fingerprint] {fp}")

    if args.store:
        store = Path(args.store)
        old = store.read_text(encoding="utf-8").strip() if store.exists() else ""
        store.write_text(fp, encoding="utf-8")
        if old and old != fp:
            print("[ui_fingerprint] 前端已变更（指纹与上次不同）")
            sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: 运行确认通过**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/unit/test_ui_fingerprint.py -v`
Expected: 3 passed

- [ ] **Step 5: run_ui.py 集成**——在 `main()` 的 `print("[run_ui] 开始执行...")` 前插入：

```python
    if not args.no_fingerprint:
        fp_script = PROJECT_ROOT / "scripts" / "ui_fingerprint.py"
        if fp_script.exists():
            store = os.path.join(cache_dir, "ui_fingerprint.txt")
            fp_result = subprocess.run(
                [find_python(), str(fp_script), "--store", store],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
            )
            fp_out = (fp_result.stdout or "").strip()
            if fp_result.returncode == 2:
                print(f"[run_ui] 注意: 前端已变更（{fp_out}），若元素地图失效请先跑探针/更新 ui-profile")
```

并在 argparse 增加 `parser.add_argument("--no-fingerprint", action="store_true", help="跳过前端版本指纹检查")`。

- [ ] **Step 6: 提交**

```bash
git add AgentTest-evalution/scripts/ui_fingerprint.py AgentTest-evalution/tests/unit/test_ui_fingerprint.py AgentTest-evalution/.opencode/skills/ui-runner/scripts/run_ui.py
git commit -m "feat(ui): 前端版本指纹检查与提示"
```

---

### Task 12: 报告渲染元素地图命中率

**Files:**
- Modify: `AgentTest-evalution/.opencode/skills/ui-runner/scripts/run_ui.py`
- Modify: `AgentTest-evalution/.opencode/skills/ui-runner/template/ui_report_template.html`

- [ ] **Step 1: parse_junit_xml 增加 element_hits 解析**

在 `parse_junit_xml` 的 case 初始化与 property 读取处追加：

```python
            case = {
                "name": tc.attrib.get("name", ""),
                "time": round(float(tc.attrib.get("time", 0)), 3),
                "status": "passed",
                "message": "",
                "trace": "",
                "screenshot": "",
                "element_hits": {},
            }
```

在 property 读取循环内追加：

```python
                    elif prop.attrib.get("name") == "element_hits":
                        try:
                            case["element_hits"] = json.loads(prop.attrib.get("value", "{}"))
                        except Exception:
                            case["element_hits"] = {}
```

- [ ] **Step 2: 新增聚合函数与渲染段（放在 build_sections 之前）**

```python
def build_element_hit_report(cases: list) -> str:
    """聚合全部用例的 element_hits：元素 → 最高命中级别；未记录 = 走回退（脆弱点）"""
    import collections
    best = {}
    for case in cases:
        for name, level in (case.get("element_hits") or {}).items():
            best[name] = max(best.get(name, -1), level)
    if not best:
        return ""
    rows = []
    for name in sorted(best):
        level = best[name]
        status = "地图命中" if level >= 0 else "回退"
        color = "#10b981" if level == 0 else ("#f59e0b" if level == 1 else "#ef4444")
        rows.append(
            f"<tr><td>{html_escape(name)}</td><td style='color:{color}'>{status}</td>"
            f"<td>策略第 {level + 1} 级</td></tr>")
    return (f'<div class="d-section"><div class="d-title">元素地图命中报告（本运行）</div>'
            f'<table class="detail-table"><thead><tr><th>元素</th><th>命中方式</th><th>策略级别</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')
```

- [ ] **Step 3: generate_report 注入**

```python
    html = html.replace("{{ELEMENT_HITS}}", build_element_hit_report(data.get("cases", [])))
```

- [ ] **Step 4: ui_report_template.html 增加占位符**——在 `{{SECTIONS}}` 替换后追加一行

```html
{{ELEMENT_HITS}}
```

- [ ] **Step 5: 提交**

```bash
git add AgentTest-evalution/.opencode/skills/ui-runner/scripts/run_ui.py AgentTest-evalution/.opencode/skills/ui-runner/template/ui_report_template.html
git commit -m "feat(ui): 报告渲染元素地图命中率"
```

---

### Task 13: post-run-analysis 增加定位修复建议环节

**Files:**
- Modify: `AgentTest-evalution/.opencode/skills/post-run-analysis/SKILL.md`

- [ ] **Step 1: 在"步骤 1：采集证据"后追加新步骤（原步骤 2~5 顺延）**

```markdown
### 步骤 1.5：定位失败 → 地图修复建议（新增）

当失败原因为定位类（找不到按钮/输入框/元素超时）时，额外执行：

1. 只读获取目标页面当前 DOM（curl 或 playwright probe，禁止重跑用例）
2. 对照失败步骤文案与 `ui-profile/elements.yaml` 现有条目，判断：文案变更？策略失效？缺失条目？
3. 输出「地图修复建议」：`文案 → { type: xxx, value: xxx }`（新策略），与失败分析一并提交用户确认
4. 用户确认后写入 `ui-profile/elements.yaml`，并运行 `python scripts/validate_elements.py` 校验

铁律：AI 只产出建议，**不经确认禁止修改元素地图**（执行层确定性边界）。
```

- [ ] **Step 2: 提交**

```bash
git add AgentTest-evalution/.opencode/skills/post-run-analysis/SKILL.md
git commit -m "docs(ui): post-run-analysis 增加定位修复建议环节"
```

---

### Task 14: 全流程回归验证

**Files:**
- 无新建（执行验证）

- [ ] **Step 1: 单元测试全量**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/unit -v`（AgentTest-evalution 目录）
Expected: 全部 passed（原 11 + 新 6 + 10 + 3 + 3 = 33）

- [ ] **Step 2: 校验元素地图**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe scripts/validate_elements.py`
Expected: 校验通过

- [ ] **Step 3: 重置适配器 dry-run**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe scripts/ui_reset.py --dry-run`
Expected: 打印清理计划（6 条语句），不执行

- [ ] **Step 4: 重新生成 + 收集校验**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe .opencode/skills/feature-to-playwright/scripts/generate_playwright.py --mode baseline`
Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/baseline/generated/ui-test --collect-only -q`
Expected: 15 tests collected，无步骤错误

- [ ] **Step 5: 全量执行（并行）**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe .opencode/skills/ui-runner/scripts/run_ui.py --mode baseline --parallel 2`
Expected: 15/15 通过（并行下执行成功）；报告含元素地图命中率段

- [ ] **Step 6: smoke 分层验证**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe .opencode/skills/ui-runner/scripts/run_ui.py --mode baseline --tags smoke --parallel 2`
Expected: 仅 @smoke 场景执行（2 个）且通过

- [ ] **Step 7: 提交产物**

```bash
git add AgentTest-evalution/tests/baseline/generated/ui-test/
git commit -m "chore(ui): 阶段 2~5 完成后重新生成测试脚本"
```