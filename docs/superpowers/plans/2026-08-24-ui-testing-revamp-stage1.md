# UI 测试链路重构 · 阶段 1（地基：ui-profile 模板 + 元素地图解析器）实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立 ui-profile 配置层骨架与元素地图解析器，使 DSL 步骤"地图优先、文本直搜回退"，现有场景零改动可跑。

**Architecture:** 新增 `ui-profile-template/`（项目绑定层模板）与 `lib/ui_profile.py`（纯函数加载器/解析器，无浏览器依赖，可单测）；`feature-to-playwright` 的 conftest 模板集成"地图优先"解析并记录命中级别；生成器把 `ui_profile.py` 复制到测试目录并修复 FEATURE_DIR 硬编码绝对路径的问题。

**Tech Stack:** Python 3.12、pytest、pytest-bdd + Playwright（沿用现状）、PyYAML。

**依赖上游设计:** `docs/superpowers/specs/2026-08-24-ui-testing-revamp-design.md`（阶段 1 = 设计文档第十一节"阶段 1 地基"）。后续阶段 2~5（生成器/数据闭环/稳定性/迭代闭环）各自独立成计划，不在本文档范围。

---

### Task 1: 创建 ui-profile-template/ 模板骨架

**Files:**
- Create: `AgentTest-evalution/ui-profile-template/elements.yaml`
- Create: `AgentTest-evalution/ui-profile-template/business.yaml`

- [ ] **Step 1: 创建 `elements.yaml` 模板**

```yaml
# ui-profile 元素地图 —— 项目绑定层的核心配置
# 约定：
#   - key = 场景步骤中使用的业务文案（文案即 key）
#   - strategies 按序尝试，命中即止；前端文案/结构改动只需更新此文件
#   - 未在 map 中定义的文案，DSL 回退到文本直搜（兼容老场景）
#   - 由 ui-element-map skill 自动生成草稿，人工确认后入库（阶段 2）
elements:
  # 示例条目（新项目绑定时删除注释，按项目实际填写）：
  # agentCodeInput:
  #   strategies:
  #     - { type: data-testid, value: agent-code-input }
  #     - { type: placeholder, value: "例如：BANK_AGENT" }
  #     - { type: role, role: textbox, name: "智能体编码" }
  # saveButton:
  #   strategies:
  #     - { type: role, role: button, name: "保存" }
  #     - { type: text, value: "保存" }
```

- [ ] **Step 2: 创建 `business.yaml` 模板**

```yaml
# business.yaml —— 项目业务配置（非定位类）
# 以下字段按阶段启用：
busy_indicators: [".el-loading-mask", ".loading"]
timeouts:
  action: 5000
  busy: 15000
  assertion: 10000
  api_sync: 15000
# protected_seeds: []      # 种子保护清单（阶段 3 启用）
# api_sync_rules: {}       # UI 操作 → 等待的后端请求（阶段 4 启用）
```

- [ ] **Step 3: 提交**

```bash
git add AgentTest-evalution/ui-profile-template/
git commit -m "feat(ui): ui-profile-template 骨架（元素地图+业务配置模板）"
```

---

### Task 2: 编写解析器单元测试（TDD 红）

**Files:**
- Create: `AgentTest-evalution/tests/unit/test_ui_profile.py`

- [ ] **Step 1: 编写测试文件（此时 lib/ui_profile.py 不存在，运行必失败）**

```python
# -*- coding: utf-8 -*-
"""lib/ui_profile.py 单元测试（无浏览器依赖：FakePage 模拟定位表面）"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))

from ui_profile import ElementMap, load_profile, resolve_element  # noqa: E402


class FakeLocator:
    def __init__(self, attached: bool):
        self._attached = attached

    @property
    def first(self):
        return self

    def wait_for(self, state="attached", timeout=0):
        if not self._attached:
            raise TimeoutError("element not attached")


class FakePage:
    """模拟 Playwright page 的定位表面：known 形如 {"data-testid:agent-code-input": True}"""

    def __init__(self, known: dict):
        self.known = known

    def _get(self, kind: str, value: str) -> FakeLocator:
        return FakeLocator(self.known.get(f"{kind}:{value}", False))

    def get_by_test_id(self, value):
        return self._get("data-testid", value)

    def get_by_placeholder(self, value):
        return self._get("placeholder", value)

    def get_by_label(self, value):
        return self._get("label", value)

    def get_by_role(self, role, name=None):
        return self._get(f"role:{role}", name)

    def get_by_text(self, value):
        return self._get("text", value)

    def locator(self, value):
        return self._get("css", value)


ELEMENT_DEF = {
    "strategies": [
        {"type": "data-testid", "value": "agent-code-input"},
        {"type": "placeholder", "value": "例如：BANK_AGENT"},
        {"type": "role", "value": {"role": "textbox", "name": "智能体编码"}},
    ]
}


def test_lookup_by_chinese_text():
    elements = {"智能体编码": ELEMENT_DEF}
    em = ElementMap(elements)
    assert em.lookup("智能体编码") == ELEMENT_DEF
    assert em.lookup("不存在") is None


def test_load_profile_parses_yaml(tmp_path):
    (tmp_path / "elements.yaml").write_text(
        "elements:\n  agentCodeInput:\n    strategies:\n"
        "      - { type: data-testid, value: agent-code-input }\n",
        encoding="utf-8",
    )
    (tmp_path / "business.yaml").write_text(
        "busy_indicators: [\".el-loading-mask\"]\ntimeouts:\n  action: 3000\n",
        encoding="utf-8",
    )
    profile = load_profile(tmp_path)
    assert profile["map"].lookup("agentCodeInput") is not None
    assert profile["business"]["busy_indicators"] == [".el-loading-mask"]
    assert profile["business"]["timeouts"]["action"] == 3000


def test_load_profile_missing_files(tmp_path):
    profile = load_profile(tmp_path)
    assert profile["map"].elements == {}
    assert profile["business"] == {}


def test_resolve_first_strategy_hit():
    page = FakePage({"data-testid:agent-code-input": True})
    loc, idx = resolve_element(page, ELEMENT_DEF, timeout_ms=500)
    assert loc is not None and idx == 0


def test_resolve_fallback_to_second_strategy():
    page = FakePage({"placeholder:例如：BANK_AGENT": True})
    loc, idx = resolve_element(page, ELEMENT_DEF, timeout_ms=500)
    assert loc is not None and idx == 1


def test_resolve_all_strategies_fail():
    page = FakePage({})
    loc, idx = resolve_element(page, ELEMENT_DEF, timeout_ms=500)
    assert loc is None and idx == -1


def test_resolve_skips_unknown_strategy_type():
    page = FakePage({"placeholder:例如：BANK_AGENT": True})
    weird = {"strategies": [{"type": "unknown-type", "value": "x"}, ELEMENT_DEF["strategies"][1]]}
    loc, idx = resolve_element(page, weird, timeout_ms=500)
    assert loc is not None and idx == 1
```

- [ ] **Step 2: 运行测试确认失败**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/unit/test_ui_profile.py -v`
Expected: 全部 FAIL 于 `ModuleNotFoundError: No module named 'ui_profile'`

- [ ] **Step 3: 提交**

```bash
git add AgentTest-evalution/tests/unit/test_ui_profile.py
git commit -m "test(ui): 元素地图解析器单元测试（红）"
```

---

### Task 3: 实现 lib/ui_profile.py（TDD 绿）

**Files:**
- Create: `AgentTest-evalution/lib/ui_profile.py`

- [ ] **Step 1: 编写实现**

```python
# -*- coding: utf-8 -*-
"""
ui_profile.py — ui-profile 配置加载与元素定位解析（确定性执行层）

职责：
- 加载 ui-profile/ 目录（elements.yaml + business.yaml）
- 按策略链解析元素 → Playwright locator（按序尝试，命中即止）
- 供 generated/ui-test/conftest.py（副本）与单元测试共用

依赖：pyyaml；playwright 仅在 resolve_element 的 page 参数上鸭子类型使用，
加载层本身不依赖浏览器。
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import yaml


class ElementMap:
    """元素地图：文案即 key → 定位策略链"""

    def __init__(self, elements: Optional[dict] = None):
        self.elements = elements or {}

    @classmethod
    def load(cls, path: Path) -> "ElementMap":
        if not path.exists():
            return cls()
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return cls(elements=data.get("elements"))

    def lookup(self, key: str) -> Optional[dict]:
        """按业务文案查元素定义；未命中返回 None"""
        return self.elements.get(key)


def load_profile(profile_dir: Path) -> dict:
    """加载 profile 目录，返回 {"map": ElementMap, "business": dict}。

    文件缺失时返回空 map / 空 business，保证最小绑定也能跑（回退文本直搜）。
    """
    profile_dir = Path(profile_dir)
    element_map = ElementMap.load(profile_dir / "elements.yaml")
    business: dict = {}
    business_path = profile_dir / "business.yaml"
    if business_path.exists():
        with open(business_path, "r", encoding="utf-8") as f:
            business = yaml.safe_load(f) or {}
    return {"map": element_map, "business": business}


def _build_locator(page, strategy: dict):
    """按策略类型构造 locator；未知类型返回 None"""
    stype = strategy.get("type")
    value = strategy.get("value")
    if stype == "data-testid":
        return page.get_by_test_id(value)
    if stype == "placeholder":
        return page.get_by_placeholder(value)
    if stype == "label":
        return page.get_by_label(value)
    if stype == "role":
        return page.get_by_role(value.get("role", "button"), name=value.get("name"))
    if stype == "combobox":
        return page.get_by_role("combobox", name=value)
    if stype == "css":
        return page.locator(value)
    if stype == "text":
        return page.get_by_text(value)
    return None


def resolve_element(page, element_def: dict, timeout_ms: int = 5000):
    """按策略链解析元素（确定性：按序尝试，命中即止）。

    返回 (locator, strategy_index)：命中返回首个 attach 成功的 locator 与策略序号；
    全部失败返回 (None, -1)。
    """
    for idx, strategy in enumerate(element_def.get("strategies", [])):
        locator = _build_locator(page, strategy)
        if locator is None:
            continue
        try:
            locator.first.wait_for(state="attached", timeout=timeout_ms)
            return locator, idx
        except Exception:
            continue
    return None, -1
```

- [ ] **Step 2: 运行测试确认通过**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/unit/test_ui_profile.py -v`
Expected: 8 passed（含 test_resolve_stops_at_first_hit）

- [ ] **Step 3: 提交**

```bash
git add AgentTest-evalution/lib/ui_profile.py
git commit -m "feat(ui): lib/ui_profile.py 元素地图加载与解析器"
```

---

### Task 4: 预填当前项目的 ui-profile/（真实地图子集）

**Files:**
- Create: `AgentTest-evalution/ui-profile/elements.yaml`
- Create: `AgentTest-evalution/ui-profile/business.yaml`

- [ ] **Step 1: 创建 `ui-profile/elements.yaml`**（内容取自现有 conftest 硬编码 testid + 现有 feature 场景文案；阶段 2 会由生成器全量重建）

```yaml
# ui-profile 元素地图 —— 智能体评测平台（绑定项目）
# 阶段 1 预填子集：覆盖现有 04-ui-scenarios/02-agent-projects.feature 的关键元素
elements:
  智能体编码:
    strategies:
      - { type: placeholder, value: "例如：BANK_AGENT" }
  请输入智能体名称:
    strategies:
      - { type: placeholder, value: "请输入智能体名称" }
  风险等级:
    strategies:
      - { type: data-testid, value: agent-risk-tier }
      - { type: combobox, name: "风险等级" }
  适配器类型:
    strategies:
      - { type: data-testid, value: agent-adapter-type }
      - { type: combobox, name: "适配器类型" }
  HTTP 方法:
    strategies:
      - { type: data-testid, value: agent-method }
      - { type: combobox, name: "HTTP 方法" }
  新增智能体:
    strategies:
      - { type: role, role: button, name: "新增智能体" }
  筛选:
    strategies:
      - { type: role, role: button, name: "筛选" }
  保存:
    strategies:
      - { type: role, role: button, name: "保存" }
```

- [ ] **Step 2: 创建 `ui-profile/business.yaml`**（照抄模板默认值）

```yaml
busy_indicators: [".el-loading-mask", ".loading"]
timeouts:
  action: 5000
  busy: 15000
  assertion: 10000
  api_sync: 15000
```

- [ ] **Step 3: 提交**

```bash
git add AgentTest-evalution/ui-profile/
git commit -m "feat(ui): 预填智能体评测平台 ui-profile（元素地图子集）"
```

---

### Task 5: 改造生成器（复制 ui_profile.py + 修复绝对路径）

**Files:**
- Modify: `AgentTest-evalution/.opencode/skills/feature-to-playwright/scripts/generate_playwright.py`

- [ ] **Step 1: 修改 `generate_playwright.py`**

在文件顶部 `CONFTEST_SRC` 定义后追加：

```python
UI_PROFILE_MODULE_SRC = PROJECT_ROOT / "lib" / "ui_profile.py"
```

将 `generate_test_file` 函数整体替换为（修复 FEATURE_DIR 硬编码绝对路径，改用相对路径，baseline/diff 双模式均正确）：

```python
def generate_test_file(feature_file: Path, feature_dir: Path, output_dir: Path) -> str:
    """为一个 feature 生成 test_{module}.py"""
    module = slug_module(feature_file.name)
    rel = os.path.relpath(feature_dir, output_dir).replace("\\", "/")
    content = (
        "# -*- coding: utf-8 -*-\n"
        "# 由 feature-to-playwright skill 自动生成，请勿手动修改\n"
        "from pathlib import Path\n"
        "from pytest_bdd import scenarios\n\n"
        f'FEATURE_DIR = Path(__file__).resolve().parent / "{rel}"\n'
        f'scenarios(str(FEATURE_DIR / "{feature_file.name}"))\n'
    )
    out_file = output_dir / f"test_{module}.py"
    out_file.write_text(content, encoding="utf-8")
    return str(out_file)
```

在 `main()` 中复制 conftest.py 的代码块之后追加（复制 ui_profile.py 到输出目录，保证生成目录自包含）：

```python
    if UI_PROFILE_MODULE_SRC.exists():
        shutil.copy(UI_PROFILE_MODULE_SRC, output_dir / "ui_profile.py")
        print("[generate_playwright] [OK] ui_profile.py 已复制")
```

注意：`generate_playwright.py` 顶部需确认已有 `import os`（当前只有 argparse/shutil/sys/pathlib，需补 `import os`）。

- [ ] **Step 2: 语法检查**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m py_compile .opencode/skills/feature-to-playwright/scripts/generate_playwright.py`
Expected: 无输出（编译通过）

- [ ] **Step 3: 提交**

```bash
git add AgentTest-evalution/.opencode/skills/feature-to-playwright/scripts/generate_playwright.py
git commit -m "fix(ui): 生成器复制 ui_profile.py 并修复 FEATURE_DIR 相对路径"
```

---

### Task 6: 改造 conftest 模板（地图优先 + 回退 + 命中记录）

**Files:**
- Modify: `AgentTest-evalution/.opencode/skills/feature-to-playwright/template/conftest.py`

- [ ] **Step 1: 在 `_project_root()` 定义之后追加 profile 加载段**

```python
def _locate_profile_dir() -> str:
    """profile 目录决议：环境变量 > 项目 ui-profile/ > ui-profile-template/"""
    env_dir = os.environ.get("UI_PROFILE_DIR", "").strip()
    if env_dir:
        return env_dir
    project_dir = _project_root() / "ui-profile"
    if project_dir.exists():
        return str(project_dir)
    return str(_project_root() / "ui-profile-template")


PROFILE_DIR = _locate_profile_dir()
PROFILE = None
try:
    from ui_profile import load_profile
    PROFILE = load_profile(Path(PROFILE_DIR))
except Exception:
    PROFILE = None

_HIT_LOG: dict = {}


def _record_hit(name: str, strategy_index: int) -> None:
    """记录元素命中的策略级别（供报告输出命中率）"""
    _HIT_LOG[name] = strategy_index


def _action_timeout() -> int:
    if PROFILE is None:
        return 5000
    return PROFILE["business"].get("timeouts", {}).get("action", 5000)
```

- [ ] **Step 2: 将 `_fill_input` 整体替换为（地图优先）**

```python
def _fill_input(page, name, value):
    """元素地图优先 → 回退 placeholder → label → role 直搜"""
    if PROFILE is not None:
        el = PROFILE["map"].lookup(name)
        if el is not None:
            loc, idx = resolve_element(page, el, _action_timeout())
            if loc is not None:
                _record_hit(name, idx)
                loc.first.fill(str(value), timeout=3000)
                return
    locators = (
        page.get_by_placeholder(name),
        page.get_by_label(name),
        page.get_by_role("textbox", name=name),
        page.get_by_role("spinbutton", name=name),
    )
    for loc in locators:
        try:
            loc.first.fill(str(value), timeout=3000)
            return
        except Exception:
            continue
    raise AssertionError(f"找不到输入框: {name}")
```

- [ ] **Step 3: 将 `_click_button` 整体替换为（地图优先）**

```python
def _click_button(page, text):
    """点击第一个 enabled 的按钮（跳过 disabled）；元素地图优先"""
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
                            return
                    except Exception:
                        continue
                raise AssertionError(f"未找到可点击的按钮「{text}」")
    loc = page.get_by_role("button", name=text)
    for candidate in loc.all():
        try:
            if candidate.is_enabled():
                candidate.click()
                return
        except Exception:
            continue
    try:
        loc.first.click()
    except Exception:
        raise AssertionError(f"未找到可点击的按钮「{text}」") from None
```

- [ ] **Step 4: 将 `select_dropdown_option` 整体替换为（地图优先，原 testid 字典降级为回退）**

```python
@when(parsers.parse('选择下拉框 "{name}" 的选项 "{option}"'))
def select_dropdown_option(page, name, option):
    if PROFILE is not None:
        el = PROFILE["map"].lookup(name)
        if el is not None:
            loc, idx = resolve_element(page, el, _action_timeout())
            if loc is not None:
                _record_hit(name, idx)
                loc.first.select_option(label=option, timeout=5000)
                return
    testid = {
        "风险等级": "agent-risk-tier",
        "适配器类型": "agent-adapter-type",
        "HTTP 方法": "agent-method",
    }.get(name)
    if testid:
        page.get_by_test_id(testid).first.select_option(label=option, timeout=5000)
    else:
        page.get_by_role("combobox", name=name).first.select_option(label=option, timeout=5000)
```

- [ ] **Step 5: 在 `pytest_runtest_makereport` 中追加元素命中记录 property**

在现有 `if bdd_steps:` 块之后追加：

```python
        if _HIT_LOG:
            item.user_properties.append(
                ("element_hits", json.dumps(_HIT_LOG, ensure_ascii=False)))
```

- [ ] **Step 6: 提交**

```bash
git add AgentTest-evalution/.opencode/skills/feature-to-playwright/template/conftest.py
git commit -m "feat(ui): conftest 模板集成元素地图（地图优先+回退+命中记录）"
```

---

### Task 7: 回归验证

**Files:**
- 无新建（执行验证）

- [ ] **Step 1: 重新生成 UI 测试脚本**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe .opencode/skills/feature-to-playwright/scripts/generate_playwright.py --mode baseline`
Expected: 5 个 test 文件 + conftest.py + ui_profile.py 复制成功；`test_agent-projects.py` 内容含 `FEATURE_DIR = Path(__file__).resolve().parent / "../../_workflow/04-ui-scenarios"`

- [ ] **Step 2: 收集校验（验证步骤注册与 conftest 导入无错）**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/baseline/generated/ui-test --collect-only -q`
Expected: `collection succeeded`，无 `StepDefinitionNotFoundError`，无 import 错误

- [ ] **Step 3: 重跑单元测试确认回归无损**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/unit/test_ui_profile.py -v`
Expected: 11 passed（8 原始 + 3 扁平格式双格式兼容测试）

- [ ] **Step 4: （可选，需前端环境）真实运行一个场景验证地图命中**

Run: `C:/Users/17201/AppData/Local/Programs/Python/Python312/python.exe -m pytest tests/baseline/generated/ui-test/test_agent-projects.py -k "list_and_view_agent_cards" -v`
Expected: 场景通过（或按环境实际结果记录）；若前端未启动则跳过此步并注明

- [ ] **Step 5: 提交（如有产物变更）**

```bash
git add AgentTest-evalution/tests/baseline/generated/ui-test/
git commit -m "chore(ui): 重新生成 UI 测试脚本（相对路径+ui_profile 副本）"
```

---

### Task 8: 阶段收尾自检

- [ ] **Step 1: 对照设计文档确认阶段 1 范围全部落地**

- [ ] 设计文档 §三：`ui-profile-template/` 骨架存在（elements.yaml + business.yaml）
- [ ] 设计文档 §四：元素地图策略链解析实现（lib/ui_profile.py），地图命中记录已挂到报告 property
- [ ] 设计文档 §四-2：未命中回退文本直搜（conftest 保持原逻辑）
- [ ] 设计文档 §十一阶段 1：现有场景零改动可跑（Task 7 已验证）

- [ ] **Step 2: 更新维护记录**（如发现新的坑，按 post-run-analysis 流程回写经验库；本阶段预计无）