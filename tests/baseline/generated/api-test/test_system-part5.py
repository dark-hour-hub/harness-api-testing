"""
test_system-part5.py --- 由 yaml-to-pytest skill 自动生成，请勿手动修改

数据来源: 02-系统管理-part5.yaml
模块: 系统管理-通知公告+参数配置+客户端管理
"""
import pytest
import yaml
from pathlib import Path

# --- 加载 YAML 数据（修改 YAML 后重新运行 pytest 即可生效，无需重新生成本文件）---
_YAML_DIR = Path(__file__).resolve().parents[2] / "_workflow/04-testcases"
_YAML_FILE = _YAML_DIR / "02-系统管理-part5.yaml"
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
def test_TC_NOTICE_001(module_context, request_helper):
    """GET /system/notice/list_有效分页查询_返回通知公告分页列表"""
    case = _get_case("TC_NOTICE_001")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_001", case, data)

@pytest.mark.order(2)
def test_TC_NOTICE_002(module_context, request_helper):
    """GET /system/notice/list_不存在的公告标题筛选_返回空分页列表"""
    case = _get_case("TC_NOTICE_002")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_002", case, data)

@pytest.mark.order(3)
def test_TC_NOTICE_003(module_context, request_helper):
    """GET /system/notice/{noticeId}_查询存在的公告ID_返回公告详情"""
    case = _get_case("TC_NOTICE_003")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_003", case, data)

@pytest.mark.order(4)
def test_TC_NOTICE_004(module_context, request_helper):
    """GET /system/notice/{noticeId}_查询不存在的公告ID_返回操作成功无数据"""
    case = _get_case("TC_NOTICE_004")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_004", case, data)

@pytest.mark.order(5)
def test_TC_NOTICE_005(module_context, request_helper):
    """POST /system/notice_有效公告数据_返回新增成功"""
    case = _get_case("TC_NOTICE_005")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_005", case, data)

@pytest.mark.order(6)
def test_TC_NOTICE_006(module_context, request_helper):
    """POST /system/notice_公告标题为空_返回公告标题不能为空"""
    case = _get_case("TC_NOTICE_006")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_006", case, data)

@pytest.mark.order(7)
def test_TC_NOTICE_007(module_context, request_helper):
    """PUT /system/notice_有效公告数据_返回修改成功"""
    case = _get_case("TC_NOTICE_007")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_007", case, data)

@pytest.mark.order(8)
def test_TC_NOTICE_008(module_context, request_helper):
    """PUT /system/notice_公告标题超过50字符_返回标题超长错误"""
    case = _get_case("TC_NOTICE_008")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_008", case, data)

@pytest.mark.order(9)
def test_TC_NOTICE_009(module_context, request_helper):
    """DELETE /system/notice/{noticeIds}_删除存在的公告_返回删除成功"""
    case = _get_case("TC_NOTICE_009")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_009", case, data)

@pytest.mark.order(10)
def test_TC_NOTICE_010(module_context, request_helper):
    """DELETE /system/notice/{noticeIds}_删除不存在的公告ID_返回操作失败"""
    case = _get_case("TC_NOTICE_010")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_010", case, data)

@pytest.mark.order(11)
def test_TC_NOTICE_011(module_context, request_helper):
    """GET /system/config/list_有效分页查询_返回参数配置分页列表"""
    case = _get_case("TC_NOTICE_011")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_011", case, data)

@pytest.mark.order(12)
def test_TC_NOTICE_012(module_context, request_helper):
    """GET /system/config/list_不存在的参数名称筛选_返回空分页列表"""
    case = _get_case("TC_NOTICE_012")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_012", case, data)

@pytest.mark.order(13)
def test_TC_NOTICE_013(module_context, request_helper):
    """GET /system/config/{configId}_查询存在的参数ID_返回参数详情"""
    case = _get_case("TC_NOTICE_013")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_013", case, data)

@pytest.mark.order(14)
def test_TC_NOTICE_014(module_context, request_helper):
    """GET /system/config/{configId}_查询不存在的参数ID_返回操作成功无数据"""
    case = _get_case("TC_NOTICE_014")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_014", case, data)

@pytest.mark.order(15)
def test_TC_NOTICE_015(module_context, request_helper):
    """GET /system/config/configKey/{configKey}_存在的参数键名_返回参数值"""
    case = _get_case("TC_NOTICE_015")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_015", case, data)

@pytest.mark.order(16)
def test_TC_NOTICE_016(module_context, request_helper):
    """GET /system/config/configKey/{configKey}_不存在的参数键名_返回空字符串"""
    case = _get_case("TC_NOTICE_016")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_016", case, data)

@pytest.mark.order(17)
def test_TC_NOTICE_017(module_context, request_helper):
    """POST /system/config_有效参数配置数据_返回新增成功"""
    case = _get_case("TC_NOTICE_017")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_017", case, data)

@pytest.mark.order(18)
def test_TC_NOTICE_018(module_context, request_helper):
    """POST /system/config_参数名称为空_返回参数名称不能为空"""
    case = _get_case("TC_NOTICE_018")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_018", case, data)

@pytest.mark.order(19)
def test_TC_NOTICE_019(module_context, request_helper):
    """PUT /system/config_有效参数配置数据_返回修改成功"""
    case = _get_case("TC_NOTICE_019")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_NOTICE_019", case, data)

@pytest.mark.order(20)
def test_TC_NOTICE_020(module_context, request_helper):
    """PUT /system/config_参数键值为空_返回参数键值不能为空"""
    case = _get_case("TC_NOTICE_020")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_020", case, data)

@pytest.mark.order(21)
def test_TC_NOTICE_021(module_context, request_helper):
    """PUT /system/config/updateByKey_有效键名和数据_返回修改成功"""
    case = _get_case("TC_NOTICE_021")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_NOTICE_021", case, data)

@pytest.mark.order(22)
def test_TC_NOTICE_022(module_context, request_helper):
    """PUT /system/config/updateByKey_不存在的参数键名_返回操作失败"""
    case = _get_case("TC_NOTICE_022")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_022", case, data)

@pytest.mark.order(23)
def test_TC_NOTICE_023(module_context, request_helper):
    """DELETE /system/config/{configIds}_删除自定义参数_返回删除成功"""
    case = _get_case("TC_NOTICE_023")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_023", case, data)

@pytest.mark.order(24)
def test_TC_NOTICE_024(module_context, request_helper):
    """DELETE /system/config/{configIds}_删除内置参数_返回内置参数不能删除"""
    case = _get_case("TC_NOTICE_024")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_024", case, data)

@pytest.mark.order(25)
def test_TC_NOTICE_025(module_context, request_helper):
    """DELETE /system/config/refreshCache_刷新参数缓存_返回操作成功"""
    case = _get_case("TC_NOTICE_025")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_025", case, data)

@pytest.mark.order(26)
def test_TC_NOTICE_026(module_context, request_helper):
    """DELETE /system/config/refreshCache_重复刷新缓存_返回操作成功"""
    case = _get_case("TC_NOTICE_026")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_026", case, data)

@pytest.mark.order(27)
def test_TC_NOTICE_027(module_context, request_helper):
    """GET /system/client/list_有效分页查询_返回客户端管理分页列表"""
    case = _get_case("TC_NOTICE_027")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_027", case, data)

@pytest.mark.order(28)
def test_TC_NOTICE_028(module_context, request_helper):
    """GET /system/client/list_不存在的客户端ID筛选_返回空分页列表"""
    case = _get_case("TC_NOTICE_028")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_028", case, data)

@pytest.mark.order(29)
def test_TC_NOTICE_029(module_context, request_helper):
    """GET /system/client/{id}_查询存在的客户端ID_返回客户端详情"""
    case = _get_case("TC_NOTICE_029")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_029", case, data)

@pytest.mark.order(30)
def test_TC_NOTICE_030(module_context, request_helper):
    """GET /system/client/{id}_查询不存在的客户端ID_返回操作成功无数据"""
    case = _get_case("TC_NOTICE_030")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_030", case, data)

@pytest.mark.order(31)
def test_TC_NOTICE_031(module_context, request_helper):
    """POST /system/client_有效客户端数据_返回新增成功"""
    case = _get_case("TC_NOTICE_031")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_031", case, data)

@pytest.mark.order(32)
def test_TC_NOTICE_032(module_context, request_helper):
    """POST /system/client_客户端key为空_返回客户端key不能为空"""
    case = _get_case("TC_NOTICE_032")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_032", case, data)

@pytest.mark.order(33)
def test_TC_NOTICE_033(module_context, request_helper):
    """PUT /system/client_有效客户端数据_返回修改成功"""
    case = _get_case("TC_NOTICE_033")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_NOTICE_033", case, data)

@pytest.mark.order(34)
def test_TC_NOTICE_034(module_context, request_helper):
    """PUT /system/client_客户端秘钥为空_返回客户端秘钥不能为空"""
    case = _get_case("TC_NOTICE_034")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_034", case, data)

@pytest.mark.order(35)
def test_TC_NOTICE_035(module_context, request_helper):
    """PUT /system/client/changeStatus_切换客户端为停用状态_返回修改成功"""
    case = _get_case("TC_NOTICE_035")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_NOTICE_035", case, data)

@pytest.mark.order(36)
def test_TC_NOTICE_036(module_context, request_helper):
    """PUT /system/client/changeStatus_不存在的客户端ID_返回操作失败"""
    case = _get_case("TC_NOTICE_036")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_NOTICE_036", case, data)

@pytest.mark.order(37)
def test_TC_NOTICE_037(module_context, request_helper):
    """DELETE /system/client/{ids}_删除存在客户端记录_返回删除成功"""
    case = _get_case("TC_NOTICE_037")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_NOTICE_037", case, data)

@pytest.mark.order(38)
def test_TC_NOTICE_038(module_context, request_helper):
    """DELETE /system/client/{ids}_删除不存在的客户端ID_返回操作失败"""
    case = _get_case("TC_NOTICE_038")
    # resp, data = request_helper.execute(case)
    # request_helper.store_extracts("TC_NOTICE_038", case, data)

