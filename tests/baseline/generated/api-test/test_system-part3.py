"""
test_system-part3.py --- 由 yaml-to-pytest skill 自动生成，请勿手动修改

数据来源: 02-系统管理-part3.yaml
模块: 系统管理-菜单管理+部门管理
"""
import pytest
import yaml
from pathlib import Path

# --- 加载 YAML 数据（修改 YAML 后重新运行 pytest 即可生效，无需重新生成本文件）---
_YAML_DIR = Path(__file__).resolve().parents[2] / "_workflow/04-testcases"
_YAML_FILE = _YAML_DIR / "02-系统管理-part3.yaml"
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
def test_TC_MENU_001(module_context, request_helper):
    """GET /system/menu/getRouters_管理员获取路由信息_返回路由列表"""
    case = _get_case("TC_MENU_001")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_001", case, data)

@pytest.mark.order(2)
def test_TC_MENU_002(module_context, request_helper):
    """GET /system/menu/getRouters_普通用户获取路由_返回受限路由列表"""
    case = _get_case("TC_MENU_002")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_002", case, data)

@pytest.mark.order(3)
def test_TC_MENU_003(module_context, request_helper):
    """GET /system/menu/list_管理员查询菜单列表_返回菜单数据"""
    case = _get_case("TC_MENU_003")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_003", case, data)

@pytest.mark.order(4)
def test_TC_MENU_004(module_context, request_helper):
    """GET /system/menu/list_查询不存在的菜单名称_返回空列表"""
    case = _get_case("TC_MENU_004")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_004", case, data)

@pytest.mark.order(5)
def test_TC_MENU_005(module_context, request_helper):
    """GET /system/menu/{menuId}_查询存在的菜单_返回菜单详情"""
    case = _get_case("TC_MENU_005")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_005", case, data)

@pytest.mark.order(6)
def test_TC_MENU_006(module_context, request_helper):
    """GET /system/menu/{menuId}_查询不存在的菜单_返回空数据"""
    case = _get_case("TC_MENU_006")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_006", case, data)

@pytest.mark.order(7)
def test_TC_MENU_007(module_context, request_helper):
    """GET /system/menu/treeselect_管理员获取菜单树_返回树形结构"""
    case = _get_case("TC_MENU_007")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_007", case, data)

@pytest.mark.order(8)
def test_TC_MENU_008(module_context, request_helper):
    """GET /system/menu/treeselect_按不存在的菜单名称过滤_返回空树"""
    case = _get_case("TC_MENU_008")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_008", case, data)

@pytest.mark.order(9)
def test_TC_MENU_009(module_context, request_helper):
    """GET /system/menu/roleMenuTreeselect/{roleId}_查询角色菜单树_返回选中键和树结构"""
    case = _get_case("TC_MENU_009")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_009", case, data)

@pytest.mark.order(10)
def test_TC_MENU_010(module_context, request_helper):
    """GET /system/menu/roleMenuTreeselect/{roleId}_查询不存在的角色_返回空选中键"""
    case = _get_case("TC_MENU_010")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_010", case, data)

@pytest.mark.order(11)
def test_TC_MENU_011(module_context, request_helper):
    """GET /system/menu/tenantPackageMenuTreeselect/{packageId}_查询套餐菜单树_返回选中键和树结构"""
    case = _get_case("TC_MENU_011")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_011", case, data)

@pytest.mark.order(12)
def test_TC_MENU_012(module_context, request_helper):
    """GET /system/menu/tenantPackageMenuTreeselect/{packageId}_新建套餐查询_返回空选中键"""
    case = _get_case("TC_MENU_012")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_012", case, data)

@pytest.mark.order(13)
def test_TC_MENU_013(module_context, request_helper):
    """POST /system/menu_新增菜单有效字段_返回新增成功"""
    case = _get_case("TC_MENU_013")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_013", case, data)

@pytest.mark.order(14)
def test_TC_MENU_014(module_context, request_helper):
    """POST /system/menu_缺少必填字段menuName_返回菜单名称不能为空"""
    case = _get_case("TC_MENU_014")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_014", case, data)

@pytest.mark.order(15)
def test_TC_MENU_015(module_context, request_helper):
    """PUT /system/menu_修改菜单名称_返回修改成功"""
    case = _get_case("TC_MENU_015")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_015", case, data)

@pytest.mark.order(16)
def test_TC_MENU_016(module_context, request_helper):
    """PUT /system/menu_缺少必填字段menuName_返回菜单名称不能为空"""
    case = _get_case("TC_MENU_016")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_016", case, data)

@pytest.mark.order(17)
def test_TC_MENU_017(module_context, request_helper):
    """DELETE /system/menu/{menuId}_删除可删除菜单_返回删除成功"""
    case = _get_case("TC_MENU_017")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_017", case, data)

@pytest.mark.order(18)
def test_TC_MENU_018(module_context, request_helper):
    """DELETE /system/menu/{menuId}_删除存在子菜单的菜单_返回不允许删除"""
    case = _get_case("TC_MENU_018")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_018", case, data)

@pytest.mark.order(19)
def test_TC_MENU_019(module_context, request_helper):
    """DELETE /system/menu/cascade/{menuIds}_批量级联删除可删除菜单_返回删除成功"""
    case = _get_case("TC_MENU_019")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_019", case, data)

@pytest.mark.order(20)
def test_TC_MENU_020(module_context, request_helper):
    """DELETE /system/menu/cascade/{menuIds}_批量删除含子菜单的菜单_返回不允许删除"""
    case = _get_case("TC_MENU_020")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_020", case, data)

@pytest.mark.order(21)
def test_TC_MENU_021(module_context, request_helper):
    """GET /system/dept/list_管理员查询部门列表_返回部门数据"""
    case = _get_case("TC_MENU_021")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_021", case, data)

@pytest.mark.order(22)
def test_TC_MENU_022(module_context, request_helper):
    """GET /system/dept/list_查询不存在的部门名称_返回空列表"""
    case = _get_case("TC_MENU_022")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_022", case, data)

@pytest.mark.order(23)
def test_TC_MENU_023(module_context, request_helper):
    """GET /system/dept/list/exclude/{deptId}_排除指定部门_返回排除后的部门列表"""
    case = _get_case("TC_MENU_023")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_023", case, data)

@pytest.mark.order(24)
def test_TC_MENU_024(module_context, request_helper):
    """GET /system/dept/list/exclude/{deptId}_排除不存在的部门_返回全部部门"""
    case = _get_case("TC_MENU_024")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_024", case, data)

@pytest.mark.order(25)
def test_TC_MENU_025(module_context, request_helper):
    """GET /system/dept/{deptId}_查询存在的部门_返回部门详情"""
    case = _get_case("TC_MENU_025")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_025", case, data)

@pytest.mark.order(26)
def test_TC_MENU_026(module_context, request_helper):
    """GET /system/dept/{deptId}_查询不存在的部门_返回空数据"""
    case = _get_case("TC_MENU_026")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_026", case, data)

@pytest.mark.order(27)
def test_TC_MENU_027(module_context, request_helper):
    """POST /system/dept_新增部门有效字段_返回新增成功"""
    case = _get_case("TC_MENU_027")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_027", case, data)

@pytest.mark.order(28)
def test_TC_MENU_028(module_context, request_helper):
    """POST /system/dept_缺少必填字段deptName_返回部门名称不能为空"""
    case = _get_case("TC_MENU_028")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_028", case, data)

@pytest.mark.order(29)
def test_TC_MENU_029(module_context, request_helper):
    """PUT /system/dept_修改部门名称_返回修改成功"""
    case = _get_case("TC_MENU_029")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_029", case, data)

@pytest.mark.order(30)
def test_TC_MENU_030(module_context, request_helper):
    """PUT /system/dept_缺少必填字段deptName_返回部门名称不能为空"""
    case = _get_case("TC_MENU_030")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_030", case, data)

@pytest.mark.order(31)
def test_TC_MENU_031(module_context, request_helper):
    """DELETE /system/dept/{deptId}_删除可删除部门_返回删除成功"""
    case = _get_case("TC_MENU_031")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_031", case, data)

@pytest.mark.order(32)
def test_TC_MENU_032(module_context, request_helper):
    """DELETE /system/dept/{deptId}_删除默认部门_返回不允许删除"""
    case = _get_case("TC_MENU_032")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_032", case, data)

@pytest.mark.order(33)
def test_TC_MENU_033(module_context, request_helper):
    """GET /system/dept/optionselect_管理员获取部门下拉列表_返回部门选项"""
    case = _get_case("TC_MENU_033")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_033", case, data)

@pytest.mark.order(34)
def test_TC_MENU_034(module_context, request_helper):
    """GET /system/dept/optionselect_筛选不存在的部门ID_返回空列表"""
    case = _get_case("TC_MENU_034")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MENU_034", case, data)

