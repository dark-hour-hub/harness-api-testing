"""
test_system-part6.py --- 由 yaml-to-pytest skill 自动生成，请勿手动修改

数据来源: 02-系统管理-part6.yaml
模块: 系统管理-租户管理+租户套餐+社会化关系
"""
import pytest
import yaml
from pathlib import Path

# --- 加载 YAML 数据（修改 YAML 后重新运行 pytest 即可生效，无需重新生成本文件）---
_YAML_DIR = Path(__file__).resolve().parents[2] / "_workflow/04-testcases"
_YAML_FILE = _YAML_DIR / "02-系统管理-part6.yaml"
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
def test_TC_TENANT_001(module_context, request_helper):
    """GET /system/tenant/list_默认分页查询租户列表_返回分页数据"""
    case = _get_case("TC_TENANT_001")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_001", case, data)

@pytest.mark.order(2)
def test_TC_TENANT_002(module_context, request_helper):
    """GET /system/tenant/list_传入负数pageNum_返回空数据或参数校验失败"""
    case = _get_case("TC_TENANT_002")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_002", case, data)

@pytest.mark.order(3)
def test_TC_TENANT_003(module_context, request_helper):
    """GET /system/tenant/{id}_查询存在的租户ID_返回租户详情"""
    case = _get_case("TC_TENANT_003")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_003", case, data)

@pytest.mark.order(4)
def test_TC_TENANT_004(module_context, request_helper):
    """GET /system/tenant/{id}_传入不存在的租户ID_返回空数据"""
    case = _get_case("TC_TENANT_004")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_004", case, data)

@pytest.mark.order(5)
def test_TC_TENANT_005(module_context, request_helper):
    """POST /system/tenant_填写完整必填字段新增租户_返回新增成功"""
    case = _get_case("TC_TENANT_005")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_005", case, data)

@pytest.mark.order(6)
def test_TC_TENANT_006(module_context, request_helper):
    """POST /system/tenant_缺少必填字段companyName_返回校验失败"""
    case = _get_case("TC_TENANT_006")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_006", case, data)

@pytest.mark.order(7)
def test_TC_TENANT_007(module_context, request_helper):
    """PUT /system/tenant_修改租户联系人信息_返回修改成功"""
    case = _get_case("TC_TENANT_007")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_007", case, data)

@pytest.mark.order(8)
def test_TC_TENANT_008(module_context, request_helper):
    """PUT /system/tenant_修改默认管理租户_返回不允许操作"""
    case = _get_case("TC_TENANT_008")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_008", case, data)

@pytest.mark.order(9)
def test_TC_TENANT_009(module_context, request_helper):
    """PUT /system/tenant/changeStatus_停用一个租户_返回修改状态成功"""
    case = _get_case("TC_TENANT_009")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_009", case, data)

@pytest.mark.order(10)
def test_TC_TENANT_010(module_context, request_helper):
    """PUT /system/tenant/changeStatus_修改管理租户状态_返回不允许操作"""
    case = _get_case("TC_TENANT_010")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_010", case, data)

@pytest.mark.order(11)
def test_TC_TENANT_011(module_context, request_helper):
    """DELETE /system/tenant/{ids}_删除非超管租户_返回删除成功"""
    case = _get_case("TC_TENANT_011")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_011", case, data)

@pytest.mark.order(12)
def test_TC_TENANT_012(module_context, request_helper):
    """DELETE /system/tenant/{ids}_删除超管租户_返回不允许删除"""
    case = _get_case("TC_TENANT_012")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_012", case, data)

@pytest.mark.order(13)
def test_TC_TENANT_013(module_context, request_helper):
    """GET /system/tenant/dynamic/{tenantId}_切换到有效租户_返回切换成功"""
    case = _get_case("TC_TENANT_013")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_013", case, data)

@pytest.mark.order(14)
def test_TC_TENANT_014(module_context, request_helper):
    """GET /system/tenant/dynamic/{tenantId}_传入不存在的租户编号_返回租户不存在"""
    case = _get_case("TC_TENANT_014")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_014", case, data)

@pytest.mark.order(15)
def test_TC_TENANT_015(module_context, request_helper):
    """GET /system/tenant/dynamic/clear_清除动态租户上下文_返回清除成功"""
    case = _get_case("TC_TENANT_015")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_015", case, data)

@pytest.mark.order(16)
def test_TC_TENANT_016(module_context, request_helper):
    """GET /system/tenant/dynamic/clear_重复清除已清除的租户上下文_返回操作成功"""
    case = _get_case("TC_TENANT_016")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_016", case, data)

@pytest.mark.order(17)
def test_TC_TENANT_017(module_context, request_helper):
    """GET /system/tenant/syncTenantPackage_有效租户同步套餐_返回同步成功"""
    case = _get_case("TC_TENANT_017")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_017", case, data)

@pytest.mark.order(18)
def test_TC_TENANT_018(module_context, request_helper):
    """GET /system/tenant/syncTenantPackage_不传packageId_返回套餐ID不能为空"""
    case = _get_case("TC_TENANT_018")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_018", case, data)

@pytest.mark.order(19)
def test_TC_TENANT_019(module_context, request_helper):
    """GET /system/tenant/syncTenantDict_同步所有租户字典_返回同步成功"""
    case = _get_case("TC_TENANT_019")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_019", case, data)

@pytest.mark.order(20)
def test_TC_TENANT_020(module_context, request_helper):
    """GET /system/tenant/syncTenantDict_非超管角色调用_返回权限不足"""
    case = _get_case("TC_TENANT_020")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_020", case, data)

@pytest.mark.order(21)
def test_TC_TENANT_021(module_context, request_helper):
    """GET /system/tenant/syncTenantConfig_同步所有租户参数配置_返回同步成功"""
    case = _get_case("TC_TENANT_021")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_021", case, data)

@pytest.mark.order(22)
def test_TC_TENANT_022(module_context, request_helper):
    """GET /system/tenant/syncTenantConfig_非超管角色调用_返回权限不足"""
    case = _get_case("TC_TENANT_022")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_022", case, data)

@pytest.mark.order(23)
def test_TC_TENANT_023(module_context, request_helper):
    """GET /system/tenant/package/list_默认分页查询套餐列表_返回分页数据"""
    case = _get_case("TC_TENANT_023")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_023", case, data)

@pytest.mark.order(24)
def test_TC_TENANT_024(module_context, request_helper):
    """GET /system/tenant/package/list_按状态筛选已停用套餐_返回过滤结果"""
    case = _get_case("TC_TENANT_024")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_024", case, data)

@pytest.mark.order(25)
def test_TC_TENANT_025(module_context, request_helper):
    """GET /system/tenant/package/selectList_获取启用的套餐列表_返回套餐数据"""
    case = _get_case("TC_TENANT_025")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_025", case, data)

@pytest.mark.order(26)
def test_TC_TENANT_026(module_context, request_helper):
    """GET /system/tenant/package/selectList_非超管角色调用_返回权限不足"""
    case = _get_case("TC_TENANT_026")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_026", case, data)

@pytest.mark.order(27)
def test_TC_TENANT_027(module_context, request_helper):
    """GET /system/tenant/package/{packageId}_查询存在的套餐ID_返回套餐详情"""
    case = _get_case("TC_TENANT_027")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_027", case, data)

@pytest.mark.order(28)
def test_TC_TENANT_028(module_context, request_helper):
    """GET /system/tenant/package/{packageId}_传入不存在的套餐ID_返回空数据"""
    case = _get_case("TC_TENANT_028")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_028", case, data)

@pytest.mark.order(29)
def test_TC_TENANT_029(module_context, request_helper):
    """POST /system/tenant/package_填写完整字段新增套餐_返回新增成功"""
    case = _get_case("TC_TENANT_029")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_029", case, data)

@pytest.mark.order(30)
def test_TC_TENANT_030(module_context, request_helper):
    """POST /system/tenant/package_缺少套餐名称_返回校验失败"""
    case = _get_case("TC_TENANT_030")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_030", case, data)

@pytest.mark.order(31)
def test_TC_TENANT_031(module_context, request_helper):
    """PUT /system/tenant/package_修改套餐名称和菜单_返回修改成功"""
    case = _get_case("TC_TENANT_031")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_031", case, data)

@pytest.mark.order(32)
def test_TC_TENANT_032(module_context, request_helper):
    """PUT /system/tenant/package_缺少必填字段packageName_返回校验失败"""
    case = _get_case("TC_TENANT_032")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_032", case, data)

@pytest.mark.order(33)
def test_TC_TENANT_033(module_context, request_helper):
    """DELETE /system/tenant/package/{packageIds}_删除未使用的套餐_返回删除成功"""
    case = _get_case("TC_TENANT_033")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_033", case, data)

@pytest.mark.order(34)
def test_TC_TENANT_034(module_context, request_helper):
    """DELETE /system/tenant/package/{packageIds}_删除已被租户使用的套餐_返回不允许删除"""
    case = _get_case("TC_TENANT_034")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_034", case, data)

@pytest.mark.order(35)
def test_TC_TENANT_035(module_context, request_helper):
    """GET /system/social/list_查询当前用户的社会化绑定_返回绑定列表"""
    case = _get_case("TC_TENANT_035")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_035", case, data)

@pytest.mark.order(36)
def test_TC_TENANT_036(module_context, request_helper):
    """GET /system/social/list_普通用户可访问无需权限_返回绑定列表"""
    case = _get_case("TC_TENANT_036")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TENANT_036", case, data)

