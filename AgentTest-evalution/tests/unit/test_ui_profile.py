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