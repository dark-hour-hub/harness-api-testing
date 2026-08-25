"""
conftest.py — 由 feature-to-playwright skill 自动生成，请勿手动修改

提供 UI 测试公共基础设施：
- base_url（从 config.yaml 读取前端地址，--base-url 可覆盖）
- 自动截图（成功和失败场景均截全页，存到 UI_SCREENSHOT_DIR 指定的目录，并写入 JUnit XML property）
- 通用步骤库（Gherkin → Playwright 操作的通用映射）

依赖：pytest-bdd、pytest-playwright、playwright
"""
import json
import os
import re
from pathlib import Path

import pytest
from pytest_bdd import given, when, then, parsers
from playwright.sync_api import expect

# ═══════════════════════════════════════════════════════════════
# 配置读取
# ═══════════════════════════════════════════════════════════════


def _project_root() -> Path:
    """conftest 位于 generated/ui-test/ 下，向上 4 级为项目根"""
    return Path(__file__).resolve().parents[4]


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

try:
    from ui_profile import (
        load_profile, resolve_element, expand_vars, seed_protected,
        resolve_vars, run_db_assert,
    )
except Exception:
    def load_profile(*_a, **_k):
        return None

    def resolve_element(*_a, **_k):
        return None, -1

    def expand_vars(v):
        return v

    def seed_protected(v, s):
        return False

    def resolve_vars(v, s):
        return v

    def run_db_assert(*_a, **_k):
        raise AssertionError("ui_profile.py 缺少 run_db_assert（请重新生成测试目录）")

PROFILE = None
try:
    if load_profile is not None:
        PROFILE = load_profile(Path(PROFILE_DIR))
except Exception:
    PROFILE = None
    import warnings
    warnings.warn(f"ui-profile 加载失败，回退文本直搜: {PROFILE_DIR}", stacklevel=2)

_HIT_LOG: dict = {}


def _record_hit(name: str, strategy_index: int) -> None:
    """记录元素命中的策略级别（供报告输出命中率）"""
    _HIT_LOG[name] = strategy_index


def _action_timeout() -> int:
    if PROFILE is None:
        return 5000
    return PROFILE["business"].get("timeouts", {}).get("action", 5000)


def _assert_not_seed(text: str) -> None:
    """操作目标命中种子保护清单 → 直接报错拦截（企业经验库第 11 条硬约束化）"""
    if PROFILE is None:
        return
    seeds = PROFILE["business"].get("protected_seeds", [])
    if seed_protected(text, seeds):
        raise AssertionError(f"禁止操作种子数据（protected_seeds 命中）: {text}")


def _load_frontend_url() -> str:
    """从环境变量或 config.yaml 读取当前环境的前端 URL"""
    env_url = os.environ.get("UI_BASE_URL", "").strip()
    if env_url:
        return env_url
    config_path = _project_root() / "config.yaml"
    if not config_path.exists():
        return ""
    try:
        import yaml
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        env_name = config.get("current_environment", "dev")
        frontends = config.get("environments", {}).get(env_name, {}).get("frontend", [])
        for fe in frontends:
            url = (fe or {}).get("url", "")
            if url:
                return url
    except Exception:
        pass
    return ""


@pytest.fixture(scope="session")
def base_url(request) -> str:
    cli = request.config.getoption("base_url", default="")
    if cli:
        return cli
    return _load_frontend_url()


# ═══════════════════════════════════════════════════════════════
# 自动截图（成功/失败）
# ═══════════════════════════════════════════════════════════════

SCREENSHOT_DIR = os.environ.get("UI_SCREENSHOT_DIR", "")


@pytest.fixture(autouse=True)
def _capture_page(request, page):
    """捕获 page 到 stash，供自动截图 hook 使用（pytest-bdd 场景下 funcargs 拿不到 page）"""
    request.node.stash["_ui_page"] = page
    yield


# ═══════════════════════════════════════════════════════════════
# BDD 步骤执行记录（供报告展示每个步骤的通过/失败状态）
# ═══════════════════════════════════════════════════════════════


def _record_bdd_step(request, step, status):
    """把当前步骤执行状态暂存到 node stash，最终由 makereport 写入 junit property"""
    steps = request.node.stash.get("_bdd_steps", None)
    if steps is None:
        steps = []
        request.node.stash["_bdd_steps"] = steps
    keyword = getattr(step, "keyword", "") or ""
    text = getattr(step, "text", None) or getattr(step, "name", None) or str(step)
    name = f"{keyword} {text}".strip() if keyword else str(text)
    for rec in steps:
        if rec["name"] == name:
            rec["status"] = status
            return
    steps.append({"name": name, "status": status})


@pytest.hookimpl(tryfirst=True)
def pytest_bdd_before_scenario(request, feature, scenario):
    _HIT_LOG.clear()
    _record_api_sync.node = request.node


@pytest.hookimpl(tryfirst=True)
def pytest_bdd_before_step_call(request, feature, scenario, step, step_func,
                                step_func_args, **kwargs):
    _record_bdd_step(request, step, "running")


@pytest.hookimpl(tryfirst=True)
def pytest_bdd_after_step(request, feature, scenario, step, step_func,
                          step_func_args, **kwargs):
    _record_bdd_step(request, step, "passed")


@pytest.hookimpl(tryfirst=True)
def pytest_bdd_step_error(exception, request, feature, scenario, step,
                          step_func, step_func_args, **kwargs):
    _record_bdd_step(request, step, "failed")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.outcome in ("passed", "failed"):
        page = item.stash.get("_ui_page", None)
        if page is not None and SCREENSHOT_DIR:
            safe_name = re.sub(r"[^\w\-]", "_", item.name)
            shot_path = os.path.join(SCREENSHOT_DIR, f"{safe_name}.png")
            try:
                os.makedirs(SCREENSHOT_DIR, exist_ok=True)
                page.screenshot(path=shot_path, full_page=True)
                item.user_properties.append(("screenshot", os.path.basename(shot_path)))
            except Exception:
                pass
        bdd_steps = item.stash.get("_bdd_steps", None)
        if bdd_steps:
            item.user_properties.append(
                ("bdd_steps", json.dumps(bdd_steps, ensure_ascii=False)))
        if _HIT_LOG:
            item.user_properties.append(
                ("element_hits", json.dumps(_HIT_LOG, ensure_ascii=False)))
        db_asserts = item.stash.get("_db_asserts", None)
        if db_asserts:
            item.user_properties.append(
                ("db_asserts", json.dumps(db_asserts, ensure_ascii=False)))
        api_syncs = item.stash.get("_api_syncs", None)
        if api_syncs:
            item.user_properties.append(
                ("api_syncs", json.dumps(api_syncs, ensure_ascii=False)))


# ═══════════════════════════════════════════════════════════════
# 定位辅助
# ═══════════════════════════════════════════════════════════════


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
                        _click_enabled_with_sync(page, loc, text)
                        return
            loc = page.get_by_role("button", name=text)
            _click_enabled_with_sync(page, loc, text)
            return
        except AssertionError:
            raise
        except Exception as e:
            last_err = e
            page.wait_for_timeout(500)
    if last_err is not None:
        raise last_err
    raise AssertionError(f"未找到可点击的按钮「{text}」")


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


def _api_rule(step_text):
    """查 api_sync_rules，返回 (method, path)；method 为空 = 任意方法；无规则返回 None"""
    if PROFILE is None:
        return None
    rule = PROFILE["business"].get("api_sync_rules", {}).get(step_text)
    if not rule:
        return None
    return rule.get("method", ""), rule.get("path", "")


def _api_timeout() -> int:
    if PROFILE is None:
        return 15000
    return int(PROFILE["business"].get("timeouts", {}).get("api_sync", 15000))


def _record_api_sync(action, method, path, received, status=None):
    """记录 API 同步结果到当前测试节点（供报告展示 API 返回校验）"""
    node = getattr(_record_api_sync, "node", None)
    if node is None:
        return
    recs = node.stash.get("_api_syncs", None)
    if recs is None:
        recs = []
        node.stash["_api_syncs"] = recs
    recs.append({
        "action": action, "method": method or "ANY", "path": path,
        "received": bool(received), "status": status,
    })


def _click_enabled_with_sync(page, loc, text):
    """点击第一个 enabled 候选；有 api 规则时先注册 expect_response 再点击（防漏快响应）。

    同步失败 fail-open（不重试、不抛错），避免已派发点击的重复提交；结果记入报告。
    """
    rule = _api_rule(text)
    if rule is None:
        for candidate in loc.all():
            try:
                if candidate.is_enabled():
                    candidate.click()
                    _wait_busy_gone(page)
                    return
            except Exception:
                continue
        loc.first.click(timeout=_action_timeout())
        _wait_busy_gone(page)
        return
    method, path = rule
    clicked = False
    received, status = False, None
    try:
        with page.expect_response(
            lambda r: (not method or r.request.method == method) and path in r.url,
            timeout=_api_timeout(),
        ) as info:
            for candidate in loc.all():
                try:
                    if candidate.is_enabled():
                        candidate.click()
                        clicked = True
                        break
                except Exception:
                    continue
            if not clicked:
                loc.first.click(timeout=_action_timeout())
                clicked = True
        resp = info.value
        received, status = True, resp.status
    except Exception:
        pass
    _record_api_sync(text, method, path, received, status)
    if not clicked:
        raise AssertionError(f"未找到可点击的按钮「{text}」")
    _wait_busy_gone(page)


def _retry_count() -> int:
    if PROFILE is None:
        return 1
    return int(PROFILE["business"].get("retry", 1))


# ═══════════════════════════════════════════════════════════════
# 场景变量 + DB 断言（db-asserts）
# ═══════════════════════════════════════════════════════════════


def _scenario_vars(request) -> dict:
    if request.node.stash.get("_scenario_vars", None) is None:
        request.node.stash["_scenario_vars"] = {}
    return request.node.stash["_scenario_vars"]


def _db_conn():
    if PROFILE is None:
        raise AssertionError("未配置 ui-profile/business.yaml 的 db 段，无法执行 DB 断言")
    db = PROFILE["business"].get("db") or {}
    if not db.get("database"):
        raise AssertionError("ui-profile/business.yaml 缺少 db.database 配置，无法执行 DB 断言")
    import pymysql
    return pymysql.connect(
        host=db.get("host", "localhost"),
        port=int(db.get("port", 3306)),
        user=db.get("user", "root"),
        password=db.get("password", ""),
        database=db["database"],
        charset=db.get("charset", "utf8mb4"),
        cursorclass=pymysql.cursors.DictCursor,
    )


# ═══════════════════════════════════════════════════════════════
# Given 步骤
# ═══════════════════════════════════════════════════════════════


@given(parsers.parse('打开首页 "{url}"'))
def open_page_with_url(page, url):
    page.goto(url, wait_until="domcontentloaded")


@given('打开首页')
def open_home(page, base_url):
    page.goto(base_url, wait_until="domcontentloaded")


@given(parsers.parse('以账号 "{username}" 密码 "{password}" 登录'))
def login(page, username, password):
    _fill_input(page, "用户名", username)
    _fill_input(page, "密码", password)
    page.get_by_role("button", name=re.compile(r"登\s*录")).first.click()
    page.wait_for_load_state("networkidle")


# ═══════════════════════════════════════════════════════════════
# When 步骤
# ═══════════════════════════════════════════════════════════════


@given(parsers.parse('点击菜单 "{text}"'))
@when(parsers.parse('点击菜单 "{text}"'))
def click_menu(page, text):
    try:
        page.get_by_role("menuitem", name=text).first.click()
    except Exception:
        raise AssertionError(f"未找到菜单「{text}」") from None
    page.wait_for_load_state("networkidle")
    _wait_busy_gone(page)


@given(parsers.parse('点击按钮 "{text}"'))
@when(parsers.parse('点击按钮 "{text}"'))
def click_button(page, text):
    _click_button(page, text)


@given(parsers.parse('点击链接 "{text}"'))
@when(parsers.parse('点击链接 "{text}"'))
def click_link(page, text):
    _assert_not_seed(text)
    page.get_by_role("link", name=text).first.click()
    _wait_busy_gone(page)


@given(parsers.parse('在 "{field}" 输入框中输入 "{value}"'))
@when(parsers.parse('在 "{field}" 输入框中输入 "{value}"'))
def fill_field(page, request, field, value):
    _fill_input(page, field, expand_vars(resolve_vars(value, _scenario_vars(request))))


@when(parsers.parse('等待 {seconds:d} 秒'))
def wait_seconds(page, seconds):
    page.wait_for_timeout(seconds * 1000)


# ═══════════════════════════════════════════════════════════════
# Then 步骤
# ═══════════════════════════════════════════════════════════════


@then(parsers.parse('应看到提示 "{text}"'))
def see_message(page, text):
    locator = page.get_by_text(text).first
    try:
        expect(locator).to_be_visible(timeout=5000)
    except AssertionError:
        raise AssertionError(f"未看到提示文案「{text}」") from None


@then(parsers.parse('页面应包含 "{text}"'))
def page_contains(page, text):
    locator = page.get_by_text(text).first
    try:
        expect(locator).to_be_visible()
    except AssertionError:
        raise AssertionError(f"页面未包含文本「{text}」") from None


@then(parsers.parse('表格应包含 "{text}"'))
def table_contains(page, text):
    locator = page.get_by_role("cell", name=text).first
    try:
        expect(locator).to_be_visible()
    except AssertionError:
        raise AssertionError(f"表格未包含「{text}」") from None


@then(parsers.parse('应看到按钮 "{text}"'))
def see_button(page, text):
    locator = page.get_by_role("button", name=text).first
    try:
        expect(locator).to_be_visible()
    except AssertionError:
        raise AssertionError(f"未看到按钮「{text}」") from None


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


@when(parsers.parse('在智能体卡片 "{code}" 中点击 "{btn}"'))
def click_in_agent_card(page, request, code, btn):
    code = expand_vars(resolve_vars(code, _scenario_vars(request)))
    _assert_not_seed(code)
    card = page.locator(".agent-card", has_text=code).first
    card.get_by_role("button", name=btn).click(timeout=5000)
    _wait_busy_gone(page)


@when(parsers.parse('在表格行包含 "{row_text}" 中点击 "{btn}"'))
def click_in_row(page, request, row_text, btn):
    row_text = expand_vars(resolve_vars(row_text, _scenario_vars(request)))
    _assert_not_seed(row_text)
    row = page.get_by_role("row", name=re.compile(re.escape(row_text))).first
    row.get_by_role("button", name=btn).first.click(timeout=5000)
    _wait_busy_gone(page)


@when(parsers.parse('在对话框 "{title}" 中点击 "{btn}"'))
def click_in_dialog(page, title, btn):
    dialog = page.get_by_role("dialog").or_(page.get_by_role("alertdialog")).filter(has_text=title).first
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
                file_input = loc.first.locator("xpath=.//input[@type='file']")
                if file_input.count() == 0:
                    file_input = page.locator('input[type="file"]').first
                file_input.set_input_files(str(_project_root() / path))
                return
    page.locator('input[type="file"]').first.set_input_files(str(_project_root() / path))


@when(parsers.parse('在 "{field}" 选择日期 "{value}"'))
def fill_date(page, request, field, value):
    _fill_input(page, field, expand_vars(resolve_vars(value, _scenario_vars(request))))


@given(parsers.re(r'令 \$(?P<var>\w+) = "(?P<value>[^"]*)"'))
@when(parsers.re(r'令 \$(?P<var>\w+) = "(?P<value>[^"]*)"'))
def declare_scenario_var(request, var, value):
    _scenario_vars(request)[var] = expand_vars(value)


@then(parsers.parse('且数据已保存到 "{map_id}"'))
def db_assert_saved(request, map_id):
    try:
        from db_asserts import DB_ASSERT_MAP
    except ImportError:
        raise AssertionError(
            "未找到生成的 db_asserts.py（请重新运行 generate_playwright.py）") from None
    compiled = DB_ASSERT_MAP.get(map_id)
    if compiled is None:
        raise AssertionError(f"db_asserts.py 中不存在映射 id: {map_id}")
    conn = _db_conn()
    try:
        detail = run_db_assert(conn, compiled, _scenario_vars(request))
    finally:
        conn.close()
    recs = request.node.stash.get("_db_asserts", None)
    if recs is None:
        recs = []
        request.node.stash["_db_asserts"] = recs
    recs.append(detail)


@when("点击新增用例并等待表单打开")
def click_add_test_case_until_form(page):
    import time
    for _ in range(4):
        page.get_by_role("button", name="新增用例").first.click(timeout=5000)
        try:
            expect(page.locator("#test-case-form-title")).to_be_visible(timeout=3000)
            return
        except AssertionError:
            page.wait_for_timeout(500)
    pytest.fail("点击「新增用例」后表单未打开")
