"""
test_owner.py --- 由 yaml-to-pytest skill 自动生成，请勿手动修改

数据来源: 03-客户管理.yaml
模块: 客户管理
"""
import pytest
import yaml
from pathlib import Path

# --- 加载 YAML 数据（修改 YAML 后重新运行 pytest 即可生效，无需重新生成本文件）---
_YAML_DIR = Path(__file__).resolve().parents[2] / "_workflow" / "04-testcases"
_YAML_FILE = _YAML_DIR / "03-客户管理.yaml"
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
def test_TC_OWNER_001(module_context, request_helper):
    """GET /owners_查询客户列表_返回分页HTML页面"""
    case = _get_case("TC_OWNER_001")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_001", case, data)

@pytest.mark.order(2)
def test_TC_OWNER_002(module_context, request_helper):
    """GET /owners_搜索不存在的姓氏_返回查找表单"""
    case = _get_case("TC_OWNER_002")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_002", case, data)

@pytest.mark.order(3)
def test_TC_OWNER_003(module_context, request_helper):
    """GET /owners/find_访问查找客户表单_返回HTML页面"""
    case = _get_case("TC_OWNER_003")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_003", case, data)

@pytest.mark.order(4)
def test_TC_OWNER_004(module_context, request_helper):
    """GET /owners/find_服务器内部错误_返回错误页面"""
    case = _get_case("TC_OWNER_004")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_004", case, data)

@pytest.mark.order(5)
def test_TC_OWNER_005(module_context, request_helper):
    """GET /owners/new_访问新增客户表单_返回空白表单"""
    case = _get_case("TC_OWNER_005")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_005", case, data)

@pytest.mark.order(6)
def test_TC_OWNER_006(module_context, request_helper):
    """GET /owners/new_服务器内部错误_返回错误页面"""
    case = _get_case("TC_OWNER_006")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_006", case, data)

@pytest.mark.order(7)
def test_TC_OWNER_007(module_context, request_helper):
    """POST /owners/new_提交合法客户信息_创建成功并重定向"""
    case = _get_case("TC_OWNER_007")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_007", case, data)

@pytest.mark.order(8)
def test_TC_OWNER_008(module_context, request_helper):
    """POST /owners/new_firstName为空_校验失败重定向回表单"""
    case = _get_case("TC_OWNER_008")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_008", case, data)

@pytest.mark.order(9)
def test_TC_OWNER_009(module_context, request_helper):
    """GET /owners/{ownerId}_查看存在的客户_返回详情页面"""
    case = _get_case("TC_OWNER_009")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_009", case, data)

@pytest.mark.order(10)
def test_TC_OWNER_010(module_context, request_helper):
    """GET /owners/{ownerId}_客户不存在_返回错误页面"""
    case = _get_case("TC_OWNER_010")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_010", case, data)

@pytest.mark.order(11)
def test_TC_OWNER_011(module_context, request_helper):
    """GET /owners/{ownerId}/edit_访问编辑客户表单_返回预填充表单"""
    case = _get_case("TC_OWNER_011")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_011", case, data)

@pytest.mark.order(12)
def test_TC_OWNER_012(module_context, request_helper):
    """GET /owners/{ownerId}/edit_客户不存在_返回错误页面"""
    case = _get_case("TC_OWNER_012")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_012", case, data)

@pytest.mark.order(13)
def test_TC_OWNER_013(module_context, request_helper):
    """POST /owners/{ownerId}/edit_提交合法更新_更新成功并重定向"""
    case = _get_case("TC_OWNER_013")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_013", case, data)

@pytest.mark.order(14)
def test_TC_OWNER_014(module_context, request_helper):
    """POST /owners/{ownerId}/edit_firstName为空_校验失败重定向回表单"""
    case = _get_case("TC_OWNER_014")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_014", case, data)

@pytest.mark.order(15)
def test_TC_OWNER_015(module_context, request_helper):
    """GET /owners/{ownerId}/pets/new_访问新增宠物表单_返回空白表单"""
    case = _get_case("TC_OWNER_015")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_015", case, data)

@pytest.mark.order(16)
def test_TC_OWNER_016(module_context, request_helper):
    """GET /owners/{ownerId}/pets/new_客户不存在_返回错误页面"""
    case = _get_case("TC_OWNER_016")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_016", case, data)

@pytest.mark.order(17)
def test_TC_OWNER_017(module_context, request_helper):
    """POST /owners/{ownerId}/pets/new_提交合法宠物信息_创建成功并重定向"""
    case = _get_case("TC_OWNER_017")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_017", case, data)

@pytest.mark.order(18)
def test_TC_OWNER_018(module_context, request_helper):
    """POST /owners/{ownerId}/pets/new_name为空_校验失败重定向回表单"""
    case = _get_case("TC_OWNER_018")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_018", case, data)

@pytest.mark.order(19)
def test_TC_OWNER_019(module_context, request_helper):
    """GET /owners/{ownerId}/pets/{petId}/edit_访问编辑宠物表单_返回预填充表单"""
    case = _get_case("TC_OWNER_019")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_019", case, data)

@pytest.mark.order(20)
def test_TC_OWNER_020(module_context, request_helper):
    """GET /owners/{ownerId}/pets/{petId}/edit_宠物不存在_返回错误页面"""
    case = _get_case("TC_OWNER_020")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_020", case, data)

@pytest.mark.order(21)
def test_TC_OWNER_021(module_context, request_helper):
    """POST /owners/{ownerId}/pets/{petId}/edit_提交合法更新_更新成功并重定向"""
    case = _get_case("TC_OWNER_021")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_021", case, data)

@pytest.mark.order(22)
def test_TC_OWNER_022(module_context, request_helper):
    """POST /owners/{ownerId}/pets/{petId}/edit_name为空_校验失败重定向回表单"""
    case = _get_case("TC_OWNER_022")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_022", case, data)

@pytest.mark.order(23)
def test_TC_OWNER_023(module_context, request_helper):
    """GET /owners/{ownerId}/pets/{petId}/visits/new_访问新增就诊表单_返回空白表单"""
    case = _get_case("TC_OWNER_023")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_023", case, data)

@pytest.mark.order(24)
def test_TC_OWNER_024(module_context, request_helper):
    """GET /owners/{ownerId}/pets/{petId}/visits/new_宠物不存在_返回错误页面"""
    case = _get_case("TC_OWNER_024")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_024", case, data)

@pytest.mark.order(25)
def test_TC_OWNER_025(module_context, request_helper):
    """POST /owners/{ownerId}/pets/{petId}/visits/new_提交合法就诊信息_创建成功并重定向"""
    case = _get_case("TC_OWNER_025")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_025", case, data)

@pytest.mark.order(26)
def test_TC_OWNER_026(module_context, request_helper):
    """POST /owners/{ownerId}/pets/{petId}/visits/new_description为空_校验失败重定向回表单"""
    case = _get_case("TC_OWNER_026")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OWNER_026", case, data)

