"""
test_agents.py --- 由 yaml-to-pytest skill 自动生成，请勿手动修改

数据来源: 01-智能体模块.yaml
模块: 智能体模块
"""
import pytest
import yaml
from pathlib import Path

# --- 加载 YAML 数据（修改 YAML 后重新运行 pytest 即可生效，无需重新生成本文件）---
_YAML_DIR = Path(__file__).resolve().parents[2] / "_workflow/04-testcases"
_YAML_FILE = _YAML_DIR / "01-智能体模块.yaml"
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
def test_TC_AGENT_001(module_context, request_helper):
    """GET /api/agents_分页查询智能体列表_返回分页数据"""
    case = _get_case("TC_AGENT_001")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_AGENT_001", case, data)

@pytest.mark.order(2)
def test_TC_AGENT_002(module_context, request_helper):
    """GET /api/agents_组合过滤条件查询_返回分页数据"""
    case = _get_case("TC_AGENT_002")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_AGENT_002", case, data)

@pytest.mark.order(3)
def test_TC_AGENT_003(module_context, request_helper):
    """GET /api/agents_page越界_返回400"""
    case = _get_case("TC_AGENT_003")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_AGENT_003", case, data)

@pytest.mark.order(4)
def test_TC_AGENT_004(module_context, request_helper):
    """GET /api/agents_riskTier非法_返回400"""
    case = _get_case("TC_AGENT_004")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_AGENT_004", case, data)

@pytest.mark.order(5)
def test_TC_AGENT_005(module_context, request_helper):
    """POST /api/agents_创建智能体_返回创建详情"""
    case = _get_case("TC_AGENT_005")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_AGENT_005", case, data)

@pytest.mark.order(6)
def test_TC_AGENT_006(module_context, request_helper):
    """POST /api/agents_缺少必填agentCode_返回400"""
    case = _get_case("TC_AGENT_006")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_AGENT_006", case, data)

@pytest.mark.order(7)
def test_TC_AGENT_007(module_context, request_helper):
    """POST /api/agents_agentCode重复_返回409"""
    case = _get_case("TC_AGENT_007")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_AGENT_007", case, data)

@pytest.mark.order(8)
def test_TC_AGENT_008(module_context, request_helper):
    """POST /api/agents_timeoutMs越界_返回400"""
    case = _get_case("TC_AGENT_008")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_AGENT_008", case, data)

@pytest.mark.order(9)
def test_TC_AGENT_009(module_context, request_helper):
    """GET /api/agents/{id}_查询智能体详情_返回配置详情"""
    case = _get_case("TC_AGENT_009")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_AGENT_009", case, data)

@pytest.mark.order(10)
def test_TC_AGENT_010(module_context, request_helper):
    """GET /api/agents/{id}_id不存在_返回404"""
    case = _get_case("TC_AGENT_010")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_AGENT_010", case, data)

@pytest.mark.order(11)
def test_TC_AGENT_011(module_context, request_helper):
    """GET /api/agents/{id}_id非数字_返回400"""
    case = _get_case("TC_AGENT_011")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_AGENT_011", case, data)

@pytest.mark.order(12)
def test_TC_AGENT_012(module_context, request_helper):
    """PUT /api/agents/{id}_更新智能体_返回更新详情"""
    case = _get_case("TC_AGENT_012")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_AGENT_012", case, data)

@pytest.mark.order(13)
def test_TC_AGENT_013(module_context, request_helper):
    """PUT /api/agents/{id}_id不存在_返回404"""
    case = _get_case("TC_AGENT_013")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_AGENT_013", case, data)

@pytest.mark.order(14)
def test_TC_AGENT_014(module_context, request_helper):
    """PUT /api/agents/{id}_id非数字_返回400"""
    case = _get_case("TC_AGENT_014")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_AGENT_014", case, data)

@pytest.mark.order(15)
def test_TC_AGENT_015(module_context, request_helper):
    """DELETE /api/agents/{id}_删除智能体_返回成功"""
    case = _get_case("TC_AGENT_015")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_AGENT_015", case, data)

@pytest.mark.order(16)
def test_TC_AGENT_016(module_context, request_helper):
    """DELETE /api/agents/{id}_id不存在_返回404"""
    case = _get_case("TC_AGENT_016")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_AGENT_016", case, data)

@pytest.mark.order(17)
def test_TC_AGENT_017(module_context, request_helper):
    """DELETE /api/agents/{id}_id非数字_返回400"""
    case = _get_case("TC_AGENT_017")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_AGENT_017", case, data)

