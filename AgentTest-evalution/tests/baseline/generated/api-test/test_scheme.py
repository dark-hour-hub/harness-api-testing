"""
test_scheme.py --- 由 yaml-to-pytest skill 自动生成，请勿手动修改

数据来源: 05-评测方案模块.yaml
模块: 评测方案模块
"""
import pytest
import yaml
from pathlib import Path

# --- 加载 YAML 数据（修改 YAML 后重新运行 pytest 即可生效，无需重新生成本文件）---
_YAML_DIR = Path(__file__).resolve().parents[2] / "_workflow/04-testcases"
_YAML_FILE = _YAML_DIR / "05-评测方案模块.yaml"
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
def test_TC_SCHEME_001(module_context, request_helper):
    """POST /api/evaluation-schemes_创建方案草稿_返回DRAFT状态"""
    case = _get_case("TC_SCHEME_001")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_SCHEME_001", case, data)

@pytest.mark.order(2)
def test_TC_SCHEME_002(module_context, request_helper):
    """POST /api/evaluation-schemes_缺少必填项schemeName_返回400"""
    case = _get_case("TC_SCHEME_002")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_SCHEME_002", case, data)

@pytest.mark.order(3)
def test_TC_SCHEME_003(module_context, request_helper):
    """POST /api/evaluation-schemes_version非法_返回400"""
    case = _get_case("TC_SCHEME_003")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_SCHEME_003", case, data)

@pytest.mark.order(4)
def test_TC_SCHEME_004(module_context, request_helper):
    """GET /api/evaluation-schemes_分页并按schemeCode模糊过滤_返回分页数据"""
    case = _get_case("TC_SCHEME_004")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_SCHEME_004", case, data)

@pytest.mark.order(5)
def test_TC_SCHEME_005(module_context, request_helper):
    """GET /api/evaluation-schemes_status非法_返回400"""
    case = _get_case("TC_SCHEME_005")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_SCHEME_005", case, data)

@pytest.mark.order(6)
def test_TC_SCHEME_006(module_context, request_helper):
    """GET /api/evaluation-schemes/{id}_查询已创建方案详情_返回方案数据"""
    case = _get_case("TC_SCHEME_006")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_SCHEME_006", case, data)

@pytest.mark.order(7)
def test_TC_SCHEME_007(module_context, request_helper):
    """GET /api/evaluation-schemes/{id}_id非数字_返回400"""
    case = _get_case("TC_SCHEME_007")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_SCHEME_007", case, data)

@pytest.mark.order(8)
def test_TC_SCHEME_008(module_context, request_helper):
    """GET /api/evaluation-schemes/{id}_方案不存在_返回404"""
    case = _get_case("TC_SCHEME_008")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_SCHEME_008", case, data)

@pytest.mark.order(9)
def test_TC_SCHEME_009(module_context, request_helper):
    """POST /api/evaluation-schemes/{id}/validate_校验DRAFT草稿_返回valid=true"""
    case = _get_case("TC_SCHEME_009")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_SCHEME_009", case, data)

@pytest.mark.order(10)
def test_TC_SCHEME_010(module_context, request_helper):
    """POST /api/evaluation-schemes/{id}/validate_方案不存在_返回404"""
    case = _get_case("TC_SCHEME_010")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_SCHEME_010", case, data)

@pytest.mark.order(11)
def test_TC_SCHEME_011(module_context, request_helper):
    """PUT /api/evaluation-schemes/{id}_更新DRAFT草稿_返回更新后方案"""
    case = _get_case("TC_SCHEME_011")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_SCHEME_011", case, data)

@pytest.mark.order(12)
def test_TC_SCHEME_012(module_context, request_helper):
    """PUT /api/evaluation-schemes/{id}_version非法_返回400"""
    case = _get_case("TC_SCHEME_012")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_SCHEME_012", case, data)

@pytest.mark.order(13)
def test_TC_SCHEME_013(module_context, request_helper):
    """POST /api/evaluation-schemes/{id}/publish_发布DRAFT方案_返回PUBLISHED"""
    case = _get_case("TC_SCHEME_013")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_SCHEME_013", case, data)

@pytest.mark.order(14)
def test_TC_SCHEME_014(module_context, request_helper):
    """POST /api/evaluation-schemes/{id}/publish_重复发布_返回409"""
    case = _get_case("TC_SCHEME_014")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_SCHEME_014", case, data)

@pytest.mark.order(15)
def test_TC_SCHEME_015(module_context, request_helper):
    """GET /api/evaluation-schemes/{id}/deletion-impact_预览已发布方案删除影响_返回影响结构"""
    case = _get_case("TC_SCHEME_015")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_SCHEME_015", case, data)

@pytest.mark.order(16)
def test_TC_SCHEME_016(module_context, request_helper):
    """GET /api/evaluation-schemes/{id}/deletion-impact_方案不存在_返回404"""
    case = _get_case("TC_SCHEME_016")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_SCHEME_016", case, data)

@pytest.mark.order(17)
def test_TC_SCHEME_017(module_context, request_helper):
    """POST /api/evaluation-schemes/{id}/clone_克隆已发布方案_返回新DRAFT草稿"""
    case = _get_case("TC_SCHEME_017")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_SCHEME_017", case, data)

@pytest.mark.order(18)
def test_TC_SCHEME_018(module_context, request_helper):
    """POST /api/evaluation-schemes/{id}/clone_克隆DRAFT草稿_返回409"""
    case = _get_case("TC_SCHEME_018")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_SCHEME_018", case, data)

@pytest.mark.order(19)
def test_TC_SCHEME_019(module_context, request_helper):
    """POST /api/evaluation-schemes/{id}/archive_归档已发布方案_返回ARCHIVED"""
    case = _get_case("TC_SCHEME_019")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_SCHEME_019", case, data)

@pytest.mark.order(20)
def test_TC_SCHEME_020(module_context, request_helper):
    """POST /api/evaluation-schemes/{id}/archive_已归档再次归档_返回409"""
    case = _get_case("TC_SCHEME_020")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_SCHEME_020", case, data)

@pytest.mark.order(21)
def test_TC_SCHEME_021(module_context, request_helper):
    """DELETE /api/evaluation-schemes/{id}_删除未引用DRAFT草稿_物理删除"""
    case = _get_case("TC_SCHEME_021")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_SCHEME_021", case, data)

@pytest.mark.order(22)
def test_TC_SCHEME_022(module_context, request_helper):
    """DELETE /api/evaluation-schemes/{id}_删除已归档方案_返回409"""
    case = _get_case("TC_SCHEME_022")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_SCHEME_022", case, data)

