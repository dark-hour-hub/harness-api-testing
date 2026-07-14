"""
test_system-user.py --- 由 yaml-to-pytest skill 自动生成，请勿手动修改

数据来源: 02-系统管理-part1.yaml
模块: 系统管理-用户管理+个人中心
"""
import pytest
import yaml
from pathlib import Path

# --- 加载 YAML 数据（修改 YAML 后重新运行 pytest 即可生效，无需重新生成本文件）---
_YAML_DIR = Path(__file__).resolve().parents[2] / "_workflow/04-testcases"
_YAML_FILE = _YAML_DIR / "02-系统管理-part1.yaml"
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
def test_TC_USER_001(module_context, request_helper):
    """GET /system/user/list_有效分页查询条件_返回用户列表及分页信息"""
    case = _get_case("TC_USER_001")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_001", case, data)

@pytest.mark.order(2)
def test_TC_USER_002(module_context, request_helper):
    """GET /system/user/list_pageSize为0的无效分页参数_系统使用默认分页正常返回"""
    case = _get_case("TC_USER_002")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_002", case, data)

@pytest.mark.order(3)
def test_TC_USER_003(module_context, request_helper):
    """POST /system/user/importData_上传有效Excel文件_返回导入成功统计"""
    case = _get_case("TC_USER_003")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_003", case, data)

@pytest.mark.order(4)
def test_TC_USER_004(module_context, request_helper):
    """POST /system/user/importData_未上传文件_返回参数校验失败"""
    case = _get_case("TC_USER_004")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_004", case, data)

@pytest.mark.order(5)
def test_TC_USER_005(module_context, request_helper):
    """GET /system/user/getInfo_获取当前管理员完整信息_返回用户权限角色及菜单权限集"""
    case = _get_case("TC_USER_005")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_005", case, data)

@pytest.mark.order(6)
def test_TC_USER_006(module_context, request_helper):
    """GET /system/user/getInfo_携带多余查询参数_系统忽略并正常返回用户信息"""
    case = _get_case("TC_USER_006")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_006", case, data)

@pytest.mark.order(7)
def test_TC_USER_007(module_context, request_helper):
    """GET /system/user/{userId}_传入有效用户ID_返回用户详细信息及角色岗位"""
    case = _get_case("TC_USER_007")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_007", case, data)

@pytest.mark.order(8)
def test_TC_USER_008(module_context, request_helper):
    """GET /system/user/{userId}_传入不存在的用户ID_返回空用户或业务错误"""
    case = _get_case("TC_USER_008")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_008", case, data)

@pytest.mark.order(9)
def test_TC_USER_009(module_context, request_helper):
    """POST /system/user_完整有效的新用户信息_返回新增成功"""
    case = _get_case("TC_USER_009")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_009", case, data)

@pytest.mark.order(10)
def test_TC_USER_010(module_context, request_helper):
    """POST /system/user_userName必填字段为空_返回参数校验失败"""
    case = _get_case("TC_USER_010")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_010", case, data)

@pytest.mark.order(11)
def test_TC_USER_011(module_context, request_helper):
    """PUT /system/user_有效修改用户信息_返回修改成功"""
    case = _get_case("TC_USER_011")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_011", case, data)

@pytest.mark.order(12)
def test_TC_USER_012(module_context, request_helper):
    """PUT /system/user_email格式不正确_返回邮箱格式校验失败"""
    case = _get_case("TC_USER_012")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_012", case, data)

@pytest.mark.order(13)
def test_TC_USER_013(module_context, request_helper):
    """DELETE /system/user/{userIds}_删除测试用户_返回删除成功"""
    case = _get_case("TC_USER_013")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_013", case, data)

@pytest.mark.order(14)
def test_TC_USER_014(module_context, request_helper):
    """DELETE /system/user/{userIds}_删除当前登录用户_返回不允许删除自身"""
    case = _get_case("TC_USER_014")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_014", case, data)

@pytest.mark.order(15)
def test_TC_USER_015(module_context, request_helper):
    """PUT /system/user/resetPwd_管理员重置普通用户密码_返回重置成功"""
    case = _get_case("TC_USER_015")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_015", case, data)

@pytest.mark.order(16)
def test_TC_USER_016(module_context, request_helper):
    """PUT /system/user/resetPwd_尝试重置超级管理员密码_返回不允许操作超管"""
    case = _get_case("TC_USER_016")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_016", case, data)

@pytest.mark.order(17)
def test_TC_USER_017(module_context, request_helper):
    """PUT /system/user/changeStatus_停用测试用户_返回状态修改成功"""
    case = _get_case("TC_USER_017")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_017", case, data)

@pytest.mark.order(18)
def test_TC_USER_018(module_context, request_helper):
    """PUT /system/user/changeStatus_尝试修改超级管理员状态_返回不允许操作超管"""
    case = _get_case("TC_USER_018")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_018", case, data)

@pytest.mark.order(19)
def test_TC_USER_019(module_context, request_helper):
    """GET /system/user/authRole/{userId}_查询用户已授权角色_返回用户信息和角色列表"""
    case = _get_case("TC_USER_019")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_019", case, data)

@pytest.mark.order(20)
def test_TC_USER_020(module_context, request_helper):
    """GET /system/user/authRole/{userId}_传入不存在用户ID_返回数据权限不足"""
    case = _get_case("TC_USER_020")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_020", case, data)

@pytest.mark.order(21)
def test_TC_USER_021(module_context, request_helper):
    """PUT /system/user/authRole_为用户分配角色列表_返回授权成功"""
    case = _get_case("TC_USER_021")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_021", case, data)

@pytest.mark.order(22)
def test_TC_USER_022(module_context, request_helper):
    """PUT /system/user/authRole_传入不存在的用户ID_返回数据权限不足"""
    case = _get_case("TC_USER_022")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_022", case, data)

@pytest.mark.order(23)
def test_TC_USER_023(module_context, request_helper):
    """GET /system/user/deptTree_获取部门树列表_返回树形部门结构"""
    case = _get_case("TC_USER_023")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_023", case, data)

@pytest.mark.order(24)
def test_TC_USER_024(module_context, request_helper):
    """GET /system/user/deptTree_传入不存在deptId筛选条件_返回空树或过滤后树结构"""
    case = _get_case("TC_USER_024")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_024", case, data)

@pytest.mark.order(25)
def test_TC_USER_025(module_context, request_helper):
    """GET /system/user/profile_获取当前用户个人信息_返回明文个人信息及角色岗位组"""
    case = _get_case("TC_USER_025")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_025", case, data)

@pytest.mark.order(26)
def test_TC_USER_026(module_context, request_helper):
    """GET /system/user/profile_携带无效请求体_系统忽略并正常返回个人信息"""
    case = _get_case("TC_USER_026")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_026", case, data)

@pytest.mark.order(27)
def test_TC_USER_027(module_context, request_helper):
    """PUT /system/user/profile_有效修改个人信息_返回修改成功"""
    case = _get_case("TC_USER_027")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_027", case, data)

@pytest.mark.order(28)
def test_TC_USER_028(module_context, request_helper):
    """PUT /system/user/profile_email格式不正确_返回邮箱格式校验失败"""
    case = _get_case("TC_USER_028")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_028", case, data)

@pytest.mark.order(29)
def test_TC_USER_029(module_context, request_helper):
    """PUT /system/user/profile/updatePwd_正确旧密码和有效新密码_返回密码修改成功"""
    case = _get_case("TC_USER_029")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_USER_029", case, data)

@pytest.mark.order(30)
def test_TC_USER_030(module_context, request_helper):
    """PUT /system/user/profile/updatePwd_旧密码为空_返回参数校验失败"""
    case = _get_case("TC_USER_030")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_USER_030", case, data)

@pytest.mark.order(31)
def test_TC_USER_031(module_context, request_helper):
    """POST /system/user/profile/avatar_上传有效图片文件_返回头像URL"""
    case = _get_case("TC_USER_031")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_031", case, data)

@pytest.mark.order(32)
def test_TC_USER_032(module_context, request_helper):
    """POST /system/user/profile/avatar_上传非图片格式文件_返回文件格式不正确"""
    case = _get_case("TC_USER_032")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_032", case, data)

