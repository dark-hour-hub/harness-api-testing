"""
test_workflow-category-definition.py --- 由 yaml-to-pytest skill 自动生成，请勿手动修改

数据来源: 05-工作流管理-part1.yaml
模块: 工作流管理-流程分类+流程定义
"""
import pytest
import yaml
from pathlib import Path

# --- 加载 YAML 数据（修改 YAML 后重新运行 pytest 即可生效，无需重新生成本文件）---
_YAML_DIR = Path(__file__).resolve().parents[2] / "_workflow/04-testcases"
_YAML_FILE = _YAML_DIR / "05-工作流管理-part1.yaml"
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
def test_TC_WF_CATEGORY_001(module_context, request_helper):
    """GET /workflow/category/list_无条件查询_返回流程分类列表"""
    case = _get_case("TC_WF_CATEGORY_001")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_001", case, data)

@pytest.mark.order(2)
def test_TC_WF_CATEGORY_002(module_context, request_helper):
    """GET /workflow/category/list_查询不存在的分类名称_返回空列表"""
    case = _get_case("TC_WF_CATEGORY_002")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_002", case, data)

@pytest.mark.order(3)
def test_TC_WF_CATEGORY_003(module_context, request_helper):
    """GET /workflow/category/{categoryId}_已存在的分类ID_返回分类详细信息"""
    case = _get_case("TC_WF_CATEGORY_003")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_003", case, data)

@pytest.mark.order(4)
def test_TC_WF_CATEGORY_004(module_context, request_helper):
    """GET /workflow/category/{categoryId}_传入不存在的分类ID_返回查询失败"""
    case = _get_case("TC_WF_CATEGORY_004")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_004", case, data)

@pytest.mark.order(5)
def test_TC_WF_CATEGORY_005(module_context, request_helper):
    """POST /workflow/category_有效分类名称和父级ID_返回新增成功"""
    case = _get_case("TC_WF_CATEGORY_005")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_005", case, data)

@pytest.mark.order(6)
def test_TC_WF_CATEGORY_006(module_context, request_helper):
    """POST /workflow/category_分类名称为空_返回校验失败"""
    case = _get_case("TC_WF_CATEGORY_006")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_006", case, data)

@pytest.mark.order(7)
def test_TC_WF_CATEGORY_007(module_context, request_helper):
    """PUT /workflow/category_修改分类名称和排序_返回修改成功"""
    case = _get_case("TC_WF_CATEGORY_007")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_007", case, data)

@pytest.mark.order(8)
def test_TC_WF_CATEGORY_008(module_context, request_helper):
    """PUT /workflow/category_缺少categoryId_返回校验失败"""
    case = _get_case("TC_WF_CATEGORY_008")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_008", case, data)

@pytest.mark.order(9)
def test_TC_WF_CATEGORY_009(module_context, request_helper):
    """DELETE /workflow/category/{categoryId}_已存在的可删除分类_返回删除成功"""
    case = _get_case("TC_WF_CATEGORY_009")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_009", case, data)

@pytest.mark.order(10)
def test_TC_WF_CATEGORY_010(module_context, request_helper):
    """DELETE /workflow/category/{categoryId}_删除默认分类_返回不允许删除"""
    case = _get_case("TC_WF_CATEGORY_010")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_010", case, data)

@pytest.mark.order(11)
def test_TC_WF_CATEGORY_011(module_context, request_helper):
    """GET /workflow/category/categoryTree_无条件查询_返回分类树结构"""
    case = _get_case("TC_WF_CATEGORY_011")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_011", case, data)

@pytest.mark.order(12)
def test_TC_WF_CATEGORY_012(module_context, request_helper):
    """GET /workflow/category/categoryTree_查询不存在的分类ID_返回空树列表"""
    case = _get_case("TC_WF_CATEGORY_012")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_012", case, data)

@pytest.mark.order(13)
def test_TC_WF_CATEGORY_013(module_context, request_helper):
    """GET /workflow/definition/list_无条件分页查询_返回已发布流程定义列表"""
    case = _get_case("TC_WF_CATEGORY_013")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_013", case, data)

@pytest.mark.order(14)
def test_TC_WF_CATEGORY_014(module_context, request_helper):
    """GET /workflow/definition/list_查询不存在的流程编码_返回空分页结果"""
    case = _get_case("TC_WF_CATEGORY_014")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_014", case, data)

@pytest.mark.order(15)
def test_TC_WF_CATEGORY_015(module_context, request_helper):
    """GET /workflow/definition/unPublishList_无条件分页查询_返回未发布流程定义列表"""
    case = _get_case("TC_WF_CATEGORY_015")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_015", case, data)

@pytest.mark.order(16)
def test_TC_WF_CATEGORY_016(module_context, request_helper):
    """GET /workflow/definition/unPublishList_查询不存在的流程名称_返回空分页结果"""
    case = _get_case("TC_WF_CATEGORY_016")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_016", case, data)

@pytest.mark.order(17)
def test_TC_WF_CATEGORY_017(module_context, request_helper):
    """GET /workflow/definition/{id}_已存在的流程定义ID_返回流程定义详情"""
    case = _get_case("TC_WF_CATEGORY_017")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_017", case, data)

@pytest.mark.order(18)
def test_TC_WF_CATEGORY_018(module_context, request_helper):
    """GET /workflow/definition/{id}_不存在的流程定义ID_返回查询失败"""
    case = _get_case("TC_WF_CATEGORY_018")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_018", case, data)

@pytest.mark.order(19)
def test_TC_WF_CATEGORY_019(module_context, request_helper):
    """POST /workflow/definition_有效流程定义信息_返回新增成功"""
    case = _get_case("TC_WF_CATEGORY_019")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_019", case, data)

@pytest.mark.order(20)
def test_TC_WF_CATEGORY_020(module_context, request_helper):
    """POST /workflow/definition_流程名称为空_返回warm-flow校验失败"""
    case = _get_case("TC_WF_CATEGORY_020")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_020", case, data)

@pytest.mark.order(21)
def test_TC_WF_CATEGORY_021(module_context, request_helper):
    """PUT /workflow/definition_修改流程定义名称_返回修改成功"""
    case = _get_case("TC_WF_CATEGORY_021")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_021", case, data)

@pytest.mark.order(22)
def test_TC_WF_CATEGORY_022(module_context, request_helper):
    """PUT /workflow/definition_不存在的流程定义ID_返回warm-flow修改失败"""
    case = _get_case("TC_WF_CATEGORY_022")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_022", case, data)

@pytest.mark.order(23)
def test_TC_WF_CATEGORY_023(module_context, request_helper):
    """PUT /workflow/definition/publish/{id}_已存在的未发布流程定义_返回发布成功"""
    case = _get_case("TC_WF_CATEGORY_023")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_023", case, data)

@pytest.mark.order(24)
def test_TC_WF_CATEGORY_024(module_context, request_helper):
    """PUT /workflow/definition/publish/{id}_不存在的流程定义ID_返回发布失败"""
    case = _get_case("TC_WF_CATEGORY_024")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_024", case, data)

@pytest.mark.order(25)
def test_TC_WF_CATEGORY_025(module_context, request_helper):
    """PUT /workflow/definition/unPublish/{id}_已发布的流程定义_返回取消发布成功"""
    case = _get_case("TC_WF_CATEGORY_025")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_025", case, data)

@pytest.mark.order(26)
def test_TC_WF_CATEGORY_026(module_context, request_helper):
    """PUT /workflow/definition/unPublish/{id}_不存在的流程定义ID_返回取消发布失败"""
    case = _get_case("TC_WF_CATEGORY_026")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_026", case, data)

@pytest.mark.order(27)
def test_TC_WF_CATEGORY_027(module_context, request_helper):
    """DELETE /workflow/definition/{ids}_未被使用的流程定义_返回删除成功"""
    case = _get_case("TC_WF_CATEGORY_027")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_027", case, data)

@pytest.mark.order(28)
def test_TC_WF_CATEGORY_028(module_context, request_helper):
    """DELETE /workflow/definition/{ids}_不存在的流程定义ID_返回删除失败"""
    case = _get_case("TC_WF_CATEGORY_028")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_028", case, data)

@pytest.mark.order(29)
def test_TC_WF_CATEGORY_029(module_context, request_helper):
    """POST /workflow/definition/copy/{id}_已存在的流程定义_返回复制成功"""
    case = _get_case("TC_WF_CATEGORY_029")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_029", case, data)

@pytest.mark.order(30)
def test_TC_WF_CATEGORY_030(module_context, request_helper):
    """POST /workflow/definition/copy/{id}_不存在的流程定义ID_返回复制失败"""
    case = _get_case("TC_WF_CATEGORY_030")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_030", case, data)

@pytest.mark.skip(reason="multipart/form-data 上传用例暂不支持")
def test_TC_WF_CATEGORY_031(module_context, request_helper):
    """POST /workflow/definition/importDef_上传有效JSON文件和分类ID_返回导入成功"""
    case = _get_case("TC_WF_CATEGORY_031")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_031", case, data)

@pytest.mark.skip(reason="multipart/form-data 上传用例暂不支持")
def test_TC_WF_CATEGORY_032(module_context, request_helper):
    """POST /workflow/definition/importDef_未上传文件_返回文件读取失败"""
    case = _get_case("TC_WF_CATEGORY_032")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_032", case, data)

@pytest.mark.order(33)
def test_TC_WF_CATEGORY_033(module_context, request_helper):
    """GET /workflow/definition/xmlString/{id}_已存在的流程定义ID_返回JSON字符串"""
    case = _get_case("TC_WF_CATEGORY_033")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_033", case, data)

@pytest.mark.order(34)
def test_TC_WF_CATEGORY_034(module_context, request_helper):
    """GET /workflow/definition/xmlString/{id}_不存在的流程定义ID_返回查询失败"""
    case = _get_case("TC_WF_CATEGORY_034")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_034", case, data)

@pytest.mark.order(35)
def test_TC_WF_CATEGORY_035(module_context, request_helper):
    """PUT /workflow/definition/active/{id}_active为true激活流程_返回激活成功"""
    case = _get_case("TC_WF_CATEGORY_035")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_035", case, data)

@pytest.mark.order(36)
def test_TC_WF_CATEGORY_036(module_context, request_helper):
    """PUT /workflow/definition/active/{id}_缺少active参数_返回参数校验失败"""
    case = _get_case("TC_WF_CATEGORY_036")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_CATEGORY_036", case, data)

