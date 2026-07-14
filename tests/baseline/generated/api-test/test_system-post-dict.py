"""
test_system-post-dict.py --- 由 yaml-to-pytest skill 自动生成，请勿手动修改

数据来源: 02-系统管理-part4.yaml
模块: 系统管理-岗位管理+字典管理
"""
import pytest
import yaml
from pathlib import Path

# --- 加载 YAML 数据（修改 YAML 后重新运行 pytest 即可生效，无需重新生成本文件）---
_YAML_DIR = Path(__file__).resolve().parents[2] / "_workflow/04-testcases"
_YAML_FILE = _YAML_DIR / "02-系统管理-part4.yaml"
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
def test_TC_POST_001(module_context, request_helper):
    """GET /system/post/list_正常分页查询岗位列表_返回分页数据和岗位字段"""
    case = _get_case("TC_POST_001")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_001", case, data)

@pytest.mark.order(2)
def test_TC_POST_002(module_context, request_helper):
    """GET /system/post/list_传入无效分页参数_返回参数绑定异常"""
    case = _get_case("TC_POST_002")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_002", case, data)

@pytest.mark.order(3)
def test_TC_POST_003(module_context, request_helper):
    """GET /system/post/{postId}_查询存在的岗位ID_返回岗位完整信息"""
    case = _get_case("TC_POST_003")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_003", case, data)

@pytest.mark.order(4)
def test_TC_POST_004(module_context, request_helper):
    """GET /system/post/{postId}_查询不存在的岗位ID_返回data为null"""
    case = _get_case("TC_POST_004")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_004", case, data)

@pytest.mark.order(5)
def test_TC_POST_005(module_context, request_helper):
    """POST /system/post_填写完整必填字段新增岗位_返回新增成功"""
    case = _get_case("TC_POST_005")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_005", case, data)

@pytest.mark.order(6)
def test_TC_POST_006(module_context, request_helper):
    """POST /system/post_缺少必填字段deptId_返回校验失败"""
    case = _get_case("TC_POST_006")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_006", case, data)

@pytest.mark.order(7)
def test_TC_POST_007(module_context, request_helper):
    """PUT /system/post_修改岗位备注信息_返回修改成功"""
    case = _get_case("TC_POST_007")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_007", case, data)

@pytest.mark.order(8)
def test_TC_POST_008(module_context, request_helper):
    """PUT /system/post_缺少必填字段postName_返回校验失败"""
    case = _get_case("TC_POST_008")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_008", case, data)

@pytest.mark.order(9)
def test_TC_POST_009(module_context, request_helper):
    """DELETE /system/post/{postIds}_删除无用户关联的岗位_返回删除成功"""
    case = _get_case("TC_POST_009")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_009", case, data)

@pytest.mark.order(10)
def test_TC_POST_010(module_context, request_helper):
    """DELETE /system/post/{postIds}_传入非数字postIds_返回参数类型错误"""
    case = _get_case("TC_POST_010")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_010", case, data)

@pytest.mark.order(11)
def test_TC_POST_011(module_context, request_helper):
    """GET /system/post/optionselect_按deptId查询岗位_返回岗位选项列表"""
    case = _get_case("TC_POST_011")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_011", case, data)

@pytest.mark.order(12)
def test_TC_POST_012(module_context, request_helper):
    """GET /system/post/optionselect_传入不存在的deptId_返回空列表"""
    case = _get_case("TC_POST_012")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_012", case, data)

@pytest.mark.order(13)
def test_TC_POST_013(module_context, request_helper):
    """GET /system/post/deptTree_查询全部部门树_返回树形结构数据"""
    case = _get_case("TC_POST_013")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_013", case, data)

@pytest.mark.order(14)
def test_TC_POST_014(module_context, request_helper):
    """GET /system/post/deptTree_传入不存在的deptId_返回空列表"""
    case = _get_case("TC_POST_014")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_014", case, data)

@pytest.mark.order(15)
def test_TC_POST_015(module_context, request_helper):
    """GET /system/dict/type/list_正常分页查询字典类型_返回分页数据和字典类型字段"""
    case = _get_case("TC_POST_015")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_015", case, data)

@pytest.mark.order(16)
def test_TC_POST_016(module_context, request_helper):
    """GET /system/dict/type/list_传入无效分页参数_返回参数绑定异常"""
    case = _get_case("TC_POST_016")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_016", case, data)

@pytest.mark.order(17)
def test_TC_POST_017(module_context, request_helper):
    """GET /system/dict/type/{dictId}_查询存在的字典类型ID_返回字典类型详情"""
    case = _get_case("TC_POST_017")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_017", case, data)

@pytest.mark.order(18)
def test_TC_POST_018(module_context, request_helper):
    """GET /system/dict/type/{dictId}_查询不存在的字典类型ID_返回data为null"""
    case = _get_case("TC_POST_018")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_018", case, data)

@pytest.mark.order(19)
def test_TC_POST_019(module_context, request_helper):
    """POST /system/dict/type_填写完整必填字段新增字典类型_返回新增成功"""
    case = _get_case("TC_POST_019")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_019", case, data)

@pytest.mark.order(20)
def test_TC_POST_020(module_context, request_helper):
    """POST /system/dict/type_缺少必填字段dictName_返回校验失败"""
    case = _get_case("TC_POST_020")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_020", case, data)

@pytest.mark.order(21)
def test_TC_POST_021(module_context, request_helper):
    """PUT /system/dict/type_修改字典类型备注_返回修改成功"""
    case = _get_case("TC_POST_021")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_021", case, data)

@pytest.mark.order(22)
def test_TC_POST_022(module_context, request_helper):
    """PUT /system/dict/type_缺少必填字段dictType_返回校验失败"""
    case = _get_case("TC_POST_022")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_022", case, data)

@pytest.mark.order(23)
def test_TC_POST_023(module_context, request_helper):
    """DELETE /system/dict/type/{dictIds}_删除无字典数据的字典类型_返回删除成功"""
    case = _get_case("TC_POST_023")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_023", case, data)

@pytest.mark.order(24)
def test_TC_POST_024(module_context, request_helper):
    """DELETE /system/dict/type/{dictIds}_传入非数字dictIds_返回参数类型错误"""
    case = _get_case("TC_POST_024")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_024", case, data)

@pytest.mark.order(25)
def test_TC_POST_025(module_context, request_helper):
    """DELETE /system/dict/type/refreshCache_正常刷新字典缓存_返回刷新成功"""
    case = _get_case("TC_POST_025")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_025", case, data)

@pytest.mark.order(26)
def test_TC_POST_026(module_context, request_helper):
    """DELETE /system/dict/type/refreshCache_连续两次刷新缓存_验证幂等性无异常"""
    case = _get_case("TC_POST_026")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_026", case, data)

@pytest.mark.order(27)
def test_TC_POST_027(module_context, request_helper):
    """GET /system/dict/type/optionselect_获取全部字典类型选项_返回选项列表"""
    case = _get_case("TC_POST_027")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_027", case, data)

@pytest.mark.order(28)
def test_TC_POST_028(module_context, request_helper):
    """GET /system/dict/type/optionselect_增加不必要查询参数_系统忽略并正常响应"""
    case = _get_case("TC_POST_028")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_028", case, data)

@pytest.mark.order(29)
def test_TC_POST_029(module_context, request_helper):
    """GET /system/dict/data/list_按字典类型分页查询_返回分页数据和字典数据字段"""
    case = _get_case("TC_POST_029")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_029", case, data)

@pytest.mark.order(30)
def test_TC_POST_030(module_context, request_helper):
    """GET /system/dict/data/list_传入无效分页参数_返回参数绑定异常"""
    case = _get_case("TC_POST_030")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_030", case, data)

@pytest.mark.order(31)
def test_TC_POST_031(module_context, request_helper):
    """GET /system/dict/data/{dictCode}_查询存在的字典编码_返回字典数据详情"""
    case = _get_case("TC_POST_031")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_031", case, data)

@pytest.mark.order(32)
def test_TC_POST_032(module_context, request_helper):
    """GET /system/dict/data/{dictCode}_查询不存在的字典编码_返回data为null"""
    case = _get_case("TC_POST_032")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_032", case, data)

@pytest.mark.order(33)
def test_TC_POST_033(module_context, request_helper):
    """GET /system/dict/data/type/{dictType}_根据存在的字典类型查询_返回字典数据列表"""
    case = _get_case("TC_POST_033")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_033", case, data)

@pytest.mark.order(34)
def test_TC_POST_034(module_context, request_helper):
    """GET /system/dict/data/type/{dictType}_查询不存在的字典类型_返回空列表"""
    case = _get_case("TC_POST_034")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_034", case, data)

@pytest.mark.order(35)
def test_TC_POST_035(module_context, request_helper):
    """POST /system/dict/data_填写完整必填字段新增字典数据_返回新增成功"""
    case = _get_case("TC_POST_035")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_035", case, data)

@pytest.mark.order(36)
def test_TC_POST_036(module_context, request_helper):
    """POST /system/dict/data_缺少必填字段dictLabel_返回校验失败"""
    case = _get_case("TC_POST_036")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_036", case, data)

@pytest.mark.order(37)
def test_TC_POST_037(module_context, request_helper):
    """PUT /system/dict/data_修改字典数据标签和备注_返回修改成功"""
    case = _get_case("TC_POST_037")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_037", case, data)

@pytest.mark.order(38)
def test_TC_POST_038(module_context, request_helper):
    """PUT /system/dict/data_缺少必填字段dictValue_返回校验失败"""
    case = _get_case("TC_POST_038")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_038", case, data)

@pytest.mark.order(39)
def test_TC_POST_039(module_context, request_helper):
    """DELETE /system/dict/data/{dictCodes}_删除字典数据_返回删除成功"""
    case = _get_case("TC_POST_039")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_039", case, data)

@pytest.mark.order(40)
def test_TC_POST_040(module_context, request_helper):
    """DELETE /system/dict/data/{dictCodes}_传入非数字dictCodes_返回参数类型错误"""
    case = _get_case("TC_POST_040")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_POST_040", case, data)

