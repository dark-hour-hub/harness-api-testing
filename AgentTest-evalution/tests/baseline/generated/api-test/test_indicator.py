"""
test_indicator.py --- 由 yaml-to-pytest skill 自动生成，请勿手动修改

数据来源: 02-指标目录模块.yaml
模块: 指标目录模块
"""
import pytest
import yaml
from pathlib import Path

# --- 加载 YAML 数据（修改 YAML 后重新运行 pytest 即可生效，无需重新生成本文件）---
_YAML_DIR = Path(__file__).resolve().parents[2] / "_workflow/04-testcases"
_YAML_FILE = _YAML_DIR / "02-指标目录模块.yaml"
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
def test_TC_IND_001(module_context, request_helper):
    """GET /api/indicator-dimensions_默认参数查询_返回维度列表"""
    case = _get_case("TC_IND_001")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_IND_001", case, data)

@pytest.mark.order(2)
def test_TC_IND_002(module_context, request_helper):
    """GET /api/indicator-dimensions_指定catalogVersion过滤_返回对应版本维度列表"""
    case = _get_case("TC_IND_002")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_IND_002", case, data)

@pytest.mark.order(3)
def test_TC_IND_003(module_context, request_helper):
    """GET /api/indicator-dimensions_指定不存在的catalogVersion_返回404"""
    case = _get_case("TC_IND_003")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_IND_003", case, data)

@pytest.mark.order(4)
def test_TC_IND_004(module_context, request_helper):
    """GET /api/indicator-categories_默认参数查询_返回分类列表"""
    case = _get_case("TC_IND_004")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_IND_004", case, data)

@pytest.mark.order(5)
def test_TC_IND_005(module_context, request_helper):
    """GET /api/indicator-categories_按维度编码过滤_返回对应分类列表"""
    case = _get_case("TC_IND_005")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_IND_005", case, data)

@pytest.mark.order(6)
def test_TC_IND_006(module_context, request_helper):
    """GET /api/indicator-categories_指定不存在的catalogVersion_返回404"""
    case = _get_case("TC_IND_006")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_IND_006", case, data)

@pytest.mark.order(7)
def test_TC_IND_007(module_context, request_helper):
    """GET /api/indicators_默认分页查询_返回分页数据"""
    case = _get_case("TC_IND_007")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_IND_007", case, data)

@pytest.mark.order(8)
def test_TC_IND_008(module_context, request_helper):
    """GET /api/indicators_多条件过滤查询_返回过滤后分页数据"""
    case = _get_case("TC_IND_008")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_IND_008", case, data)

@pytest.mark.order(9)
def test_TC_IND_009(module_context, request_helper):
    """GET /api/indicators_pageSize越界_返回400"""
    case = _get_case("TC_IND_009")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_IND_009", case, data)

@pytest.mark.order(10)
def test_TC_IND_010(module_context, request_helper):
    """GET /api/indicators_direction非法枚举_返回400"""
    case = _get_case("TC_IND_010")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_IND_010", case, data)

@pytest.mark.order(11)
def test_TC_IND_011(module_context, request_helper):
    """GET /api/indicators/{id}_查询指标详情_返回指标详情"""
    case = _get_case("TC_IND_011")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_IND_011", case, data)

@pytest.mark.order(12)
def test_TC_IND_012(module_context, request_helper):
    """GET /api/indicators/{id}_指标不存在_返回404"""
    case = _get_case("TC_IND_012")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_IND_012", case, data)

@pytest.mark.order(13)
def test_TC_IND_013(module_context, request_helper):
    """GET /api/indicators/{id}_id非数字_返回400"""
    case = _get_case("TC_IND_013")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_IND_013", case, data)

@pytest.mark.order(14)
def test_TC_IND_014(module_context, request_helper):
    """GET /api/indicator-catalog-versions_默认查询_返回版本列表"""
    case = _get_case("TC_IND_014")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_IND_014", case, data)

