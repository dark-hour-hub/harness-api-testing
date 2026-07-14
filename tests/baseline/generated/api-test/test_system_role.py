"""
test_system_role.py --- 由 yaml-to-pytest skill 自动生成，请勿手动修改

数据来源: 02-系统管理-part2.yaml
模块: 角色管理
"""
import pytest
import yaml
from pathlib import Path

# --- 加载 YAML 数据（修改 YAML 后重新运行 pytest 即可生效，无需重新生成本文件）---
_YAML_DIR = Path(__file__).resolve().parents[2] / "_workflow/04-testcases"
_YAML_FILE = _YAML_DIR / "02-系统管理-part2.yaml"
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
def test_TC_ROLE_001(module_context, request_helper):
    """GET /system/role/list_默认分页查询角色列表_返回分页数据"""
    case = _get_case("TC_ROLE_001")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_001", case, data)

@pytest.mark.order(2)
def test_TC_ROLE_002(module_context, request_helper):
    """GET /system/role/list_传入无效排序字段_返回服务器错误"""
    case = _get_case("TC_ROLE_002")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_002", case, data)

@pytest.mark.order(3)
def test_TC_ROLE_003(module_context, request_helper):
    """GET /system/role/{roleId}_查询存在的角色ID_返回角色详情"""
    case = _get_case("TC_ROLE_003")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_003", case, data)

@pytest.mark.order(4)
def test_TC_ROLE_004(module_context, request_helper):
    """GET /system/role/{roleId}_传入不存在的角色ID_返回空数据"""
    case = _get_case("TC_ROLE_004")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_004", case, data)

@pytest.mark.order(5)
def test_TC_ROLE_005(module_context, request_helper):
    """POST /system/role_填写完整必填字段新增角色_返回新增成功"""
    case = _get_case("TC_ROLE_005")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_005", case, data)

@pytest.mark.order(6)
def test_TC_ROLE_006(module_context, request_helper):
    """POST /system/role_角色名称已存在_返回新增失败"""
    case = _get_case("TC_ROLE_006")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_006", case, data)

@pytest.mark.order(7)
def test_TC_ROLE_007(module_context, request_helper):
    """PUT /system/role_修改普通角色信息_返回修改成功"""
    case = _get_case("TC_ROLE_007")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_007", case, data)

@pytest.mark.order(8)
def test_TC_ROLE_008(module_context, request_helper):
    """PUT /system/role_修改超级管理员角色_返回不允许操作"""
    case = _get_case("TC_ROLE_008")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_008", case, data)

@pytest.mark.order(9)
def test_TC_ROLE_009(module_context, request_helper):
    """PUT /system/role/dataScope_修改普通角色数据权限_返回修改成功"""
    case = _get_case("TC_ROLE_009")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_009", case, data)

@pytest.mark.order(10)
def test_TC_ROLE_010(module_context, request_helper):
    """PUT /system/role/dataScope_修改超级管理员角色数据权限_返回不允许操作"""
    case = _get_case("TC_ROLE_010")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_010", case, data)

@pytest.mark.order(11)
def test_TC_ROLE_011(module_context, request_helper):
    """PUT /system/role/changeStatus_修改普通角色状态_返回修改成功"""
    case = _get_case("TC_ROLE_011")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_011", case, data)

@pytest.mark.order(12)
def test_TC_ROLE_012(module_context, request_helper):
    """PUT /system/role/changeStatus_修改超级管理员角色状态_返回不允许操作"""
    case = _get_case("TC_ROLE_012")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_012", case, data)

@pytest.mark.order(13)
def test_TC_ROLE_013(module_context, request_helper):
    """DELETE /system/role/{roleIds}_删除非超管角色_返回删除成功"""
    case = _get_case("TC_ROLE_013")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_013", case, data)

@pytest.mark.order(14)
def test_TC_ROLE_014(module_context, request_helper):
    """DELETE /system/role/{roleIds}_删除超级管理员角色_返回不允许操作"""
    case = _get_case("TC_ROLE_014")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_014", case, data)

@pytest.mark.order(15)
def test_TC_ROLE_015(module_context, request_helper):
    """GET /system/role/optionselect_获取全部正常角色列表_返回角色下拉数据"""
    case = _get_case("TC_ROLE_015")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_015", case, data)

@pytest.mark.order(16)
def test_TC_ROLE_016(module_context, request_helper):
    """GET /system/role/optionselect_传入不存在的角色ID_返回空列表"""
    case = _get_case("TC_ROLE_016")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_016", case, data)

@pytest.mark.order(17)
def test_TC_ROLE_017(module_context, request_helper):
    """GET /system/role/authUser/allocatedList_查询已分配用户列表_返回分页数据"""
    case = _get_case("TC_ROLE_017")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_017", case, data)

@pytest.mark.order(18)
def test_TC_ROLE_018(module_context, request_helper):
    """GET /system/role/authUser/allocatedList_传入不存在的角色ID_返回空列表"""
    case = _get_case("TC_ROLE_018")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_018", case, data)

@pytest.mark.order(19)
def test_TC_ROLE_019(module_context, request_helper):
    """GET /system/role/authUser/unallocatedList_查询未分配用户列表_返回分页数据"""
    case = _get_case("TC_ROLE_019")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_019", case, data)

@pytest.mark.order(20)
def test_TC_ROLE_020(module_context, request_helper):
    """GET /system/role/authUser/unallocatedList_传入不存在的角色ID_返回空列表"""
    case = _get_case("TC_ROLE_020")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_020", case, data)

@pytest.mark.order(21)
def test_TC_ROLE_021(module_context, request_helper):
    """PUT /system/role/authUser/cancel_取消非当前用户的角色授权_返回取消成功"""
    case = _get_case("TC_ROLE_021")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_021", case, data)

@pytest.mark.order(22)
def test_TC_ROLE_022(module_context, request_helper):
    """PUT /system/role/authUser/cancel_取消当前登录用户角色_返回不允许修改"""
    case = _get_case("TC_ROLE_022")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_022", case, data)

@pytest.mark.order(23)
def test_TC_ROLE_023(module_context, request_helper):
    """PUT /system/role/authUser/cancelAll_批量取消非当前用户授权_返回取消成功"""
    case = _get_case("TC_ROLE_023")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_023", case, data)

@pytest.mark.order(24)
def test_TC_ROLE_024(module_context, request_helper):
    """PUT /system/role/authUser/cancelAll_批量取消包含当前登录用户_返回不允许修改"""
    case = _get_case("TC_ROLE_024")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_024", case, data)

@pytest.mark.order(25)
def test_TC_ROLE_025(module_context, request_helper):
    """PUT /system/role/authUser/selectAll_批量授权非当前用户_返回授权成功"""
    case = _get_case("TC_ROLE_025")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_025", case, data)

@pytest.mark.order(26)
def test_TC_ROLE_026(module_context, request_helper):
    """PUT /system/role/authUser/selectAll_批量授权包含当前登录用户_返回不允许修改"""
    case = _get_case("TC_ROLE_026")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_026", case, data)

@pytest.mark.order(27)
def test_TC_ROLE_027(module_context, request_helper):
    """GET /system/role/deptTree/{roleId}_查询存在角色的部门树_返回部门树及已选部门"""
    case = _get_case("TC_ROLE_027")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_027", case, data)

@pytest.mark.order(28)
def test_TC_ROLE_028(module_context, request_helper):
    """GET /system/role/deptTree/{roleId}_传入不存在的角色ID_返回空数据"""
    case = _get_case("TC_ROLE_028")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_ROLE_028", case, data)

