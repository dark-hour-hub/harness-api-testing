"""
test_testcase.py --- 由 yaml-to-pytest skill 自动生成，请勿手动修改

数据来源: 03-测试用例模块.yaml
模块: 测试用例模块
"""
import pytest
import yaml
from pathlib import Path

# --- 加载 YAML 数据（修改 YAML 后重新运行 pytest 即可生效，无需重新生成本文件）---
_YAML_DIR = Path(__file__).resolve().parents[2] / "_workflow/04-testcases"
_YAML_FILE = _YAML_DIR / "03-测试用例模块.yaml"
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
def test_TC_CASE_001(module_context, request_helper):
    """POST /api/test-cases_创建用例成功_返回用例详情"""
    case = _get_case("TC_CASE_001")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_CASE_001", case, data)

@pytest.mark.order(2)
def test_TC_CASE_002(module_context, request_helper):
    """POST /api/test-cases_caseCode加version已存在_返回409冲突"""
    case = _get_case("TC_CASE_002")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_CASE_002", case, data)

@pytest.mark.order(3)
def test_TC_CASE_003(module_context, request_helper):
    """GET /api/test-cases_按过滤条件分页查询_返回分页数据"""
    case = _get_case("TC_CASE_003")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_CASE_003", case, data)

@pytest.mark.order(4)
def test_TC_CASE_004(module_context, request_helper):
    """GET /api/test-cases_pageSize越界_返回400校验失败"""
    case = _get_case("TC_CASE_004")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_CASE_004", case, data)

@pytest.mark.order(5)
def test_TC_CASE_005(module_context, request_helper):
    """GET /api/test-cases/{id}_查询已创建用例_返回用例详情"""
    case = _get_case("TC_CASE_005")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_CASE_005", case, data)

@pytest.mark.order(6)
def test_TC_CASE_006(module_context, request_helper):
    """GET /api/test-cases/{id}_查询不存在的用例_返回404"""
    case = _get_case("TC_CASE_006")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_CASE_006", case, data)

@pytest.mark.order(7)
def test_TC_CASE_007(module_context, request_helper):
    """PUT /api/test-cases/{id}_全量更新用例_返回更新后详情"""
    case = _get_case("TC_CASE_007")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_CASE_007", case, data)

@pytest.mark.order(8)
def test_TC_CASE_008(module_context, request_helper):
    """PUT /api/test-cases/{id}_更新不存在的用例_返回404"""
    case = _get_case("TC_CASE_008")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_CASE_008", case, data)

@pytest.mark.order(9)
def test_TC_CASE_009(module_context, request_helper):
    """DELETE /api/test-cases/{id}_软删除用例_返回删除结果"""
    case = _get_case("TC_CASE_009")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_CASE_009", case, data)

@pytest.mark.order(10)
def test_TC_CASE_010(module_context, request_helper):
    """DELETE /api/test-cases/{id}_删除不存在的用例_返回404"""
    case = _get_case("TC_CASE_010")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_CASE_010", case, data)

@pytest.mark.order(11)
def test_TC_CASE_011(module_context, request_helper):
    """POST /api/test-cases/import_批量导入有效用例_返回导入成功列表"""
    case = _get_case("TC_CASE_011")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_CASE_011", case, data)

@pytest.mark.order(12)
def test_TC_CASE_012(module_context, request_helper):
    """POST /api/test-cases/import_批内重复caseCode_返回400与行级错误"""
    case = _get_case("TC_CASE_012")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_CASE_012", case, data)

@pytest.mark.skip(reason="multipart/form-data 上传用例暂不支持")
def test_TC_CASE_013(module_context, request_helper):
    """POST /api/test-cases/import/excel_缺少file参数_返回400"""
    case = _get_case("TC_CASE_013")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_CASE_013", case, data)

@pytest.mark.order(14)
def test_TC_CASE_014(module_context, request_helper):
    """GET /api/test-cases/import/template_下载Excel模板_返回xlsx文件流"""
    case = _get_case("TC_CASE_014")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_CASE_014", case, data)

