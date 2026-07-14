"""
test_auth.py --- 由 yaml-to-pytest skill 自动生成，请勿手动修改

数据来源: 01-认证模块.yaml
模块: 认证模块
"""
import pytest
import yaml
from pathlib import Path

# --- 加载 YAML 数据（修改 YAML 后重新运行 pytest 即可生效，无需重新生成本文件）---
_YAML_DIR = Path(__file__).resolve().parents[2] / "_workflow/04-testcases"
_YAML_FILE = _YAML_DIR / "01-认证模块.yaml"
with open(_YAML_FILE, "r", encoding="utf-8") as _f:
    MODULE_DATA = yaml.safe_load(_f)


def _get_case(case_id):
    """按 ID 从 YAML 数据中获取用例"""
    for tc in MODULE_DATA.get("testcases", []):
        if tc.get("id") == case_id:
            return tc
    raise ValueError(f"用例 {case_id} 不存在于 {_YAML_FILE.name}")


@pytest.fixture(scope="session")
def module_data():
    """覆盖 conftest.py 中的 module_data fixture"""
    return MODULE_DATA


@pytest.fixture(scope="session")
def yaml_dir():
    """覆盖 conftest.py 中的 yaml_dir fixture"""
    return _YAML_DIR


# ═══════════════════════════════════════════════════════════════
# 测试用例
# ═══════════════════════════════════════════════════════════════

@pytest.mark.order(1)
def test_TC_AUTH_001(module_context, request_helper):
    """POST /auth/login_有效密码凭证登录_返回token"""
    case = _get_case("TC_AUTH_001")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_AUTH_001", case, data)

@pytest.mark.order(2)
def test_TC_AUTH_002(module_context, request_helper):
    """POST /auth/login_密码错误_返回用户认证失败"""
    case = _get_case("TC_AUTH_002")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_AUTH_002", case, data)

@pytest.mark.order(3)
def test_TC_AUTH_003(module_context, request_helper):
    """GET /auth/binding/{source}_获取github授权URL_返回OAuth跳转地址"""
    case = _get_case("TC_AUTH_003")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_AUTH_003", case, data)

@pytest.mark.order(4)
def test_TC_AUTH_004(module_context, request_helper):
    """GET /auth/binding/{source}_未配置的第三方平台_返回平台不支持"""
    case = _get_case("TC_AUTH_004")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_AUTH_004", case, data)

@pytest.mark.order(5)
def test_TC_AUTH_005(module_context, request_helper):
    """POST /auth/social/callback_绑定第三方账号_返回绑定成功"""
    case = _get_case("TC_AUTH_005")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_AUTH_005", case, data)

@pytest.mark.order(6)
def test_TC_AUTH_006(module_context, request_helper):
    """POST /auth/social/callback_未携带Token_返回401认证失败"""
    case = _get_case("TC_AUTH_006")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_AUTH_006", case, data)

@pytest.mark.order(7)
def test_TC_AUTH_007(module_context, request_helper):
    """DELETE /auth/unlock/{socialId}_取消第三方授权_返回取消成功"""
    case = _get_case("TC_AUTH_007")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_AUTH_007", case, data)

@pytest.mark.order(8)
def test_TC_AUTH_008(module_context, request_helper):
    """DELETE /auth/unlock/{socialId}_传入不存在的绑定记录_返回取消失败"""
    case = _get_case("TC_AUTH_008")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_AUTH_008", case, data)

@pytest.mark.order(9)
def test_TC_AUTH_009(module_context, request_helper):
    """POST /auth/logout_正常退出登录_返回退出成功"""
    case = _get_case("TC_AUTH_009")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_AUTH_009", case, data)

@pytest.mark.order(10)
def test_TC_AUTH_010(module_context, request_helper):
    """POST /auth/logout_未登录状态调用_返回退出成功"""
    case = _get_case("TC_AUTH_010")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_AUTH_010", case, data)

@pytest.mark.order(11)
def test_TC_AUTH_011(module_context, request_helper):
    """POST /auth/register_有效信息注册新用户_返回注册成功"""
    case = _get_case("TC_AUTH_011")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_AUTH_011", case, data)

@pytest.mark.order(12)
def test_TC_AUTH_012(module_context, request_helper):
    """POST /auth/register_用户名已存在_返回注册失败"""
    case = _get_case("TC_AUTH_012")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_AUTH_012", case, data)

@pytest.mark.order(13)
def test_TC_AUTH_013(module_context, request_helper):
    """GET /auth/tenant/list_获取租户列表_返回租户信息"""
    case = _get_case("TC_AUTH_013")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_AUTH_013", case, data)

@pytest.mark.order(14)
def test_TC_AUTH_014(module_context, request_helper):
    """GET /auth/tenant/list_触发限流_返回访问频繁提示"""
    case = _get_case("TC_AUTH_014")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_AUTH_014", case, data)

@pytest.mark.order(15)
def test_TC_AUTH_015(module_context, request_helper):
    """GET /auth/code_生成图形验证码_返回验证码图片及uuid"""
    case = _get_case("TC_AUTH_015")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_AUTH_015", case, data)

@pytest.mark.order(16)
def test_TC_AUTH_016(module_context, request_helper):
    """GET /auth/code_验证码功能关闭_返回captchaEnabled为false"""
    case = _get_case("TC_AUTH_016")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_AUTH_016", case, data)

@pytest.mark.order(17)
def test_TC_AUTH_017(module_context, request_helper):
    """GET /resource/sms/code_有效手机号发送短信验证码_返回发送成功"""
    case = _get_case("TC_AUTH_017")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_AUTH_017", case, data)

@pytest.mark.order(18)
def test_TC_AUTH_018(module_context, request_helper):
    """GET /resource/sms/code_手机号为空_返回参数校验失败"""
    case = _get_case("TC_AUTH_018")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_AUTH_018", case, data)

@pytest.mark.order(19)
def test_TC_AUTH_019(module_context, request_helper):
    """GET /resource/email/code_有效邮箱发送邮箱验证码_返回发送成功"""
    case = _get_case("TC_AUTH_019")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_AUTH_019", case, data)

@pytest.mark.order(20)
def test_TC_AUTH_020(module_context, request_helper):
    """GET /resource/email/code_邮箱为空_返回参数校验失败"""
    case = _get_case("TC_AUTH_020")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_AUTH_020", case, data)

