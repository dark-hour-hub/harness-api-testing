"""
test_workflow-instance-spel.py --- 由 yaml-to-pytest skill 自动生成，请勿手动修改

数据来源: 05-工作流管理-part2.yaml
模块: 工作流管理-流程实例+Spel表达式
"""
import pytest
import yaml
from pathlib import Path

# --- 加载 YAML 数据（修改 YAML 后重新运行 pytest 即可生效，无需重新生成本文件）---
_YAML_DIR = Path(__file__).resolve().parents[2] / "_workflow/04-testcases"
_YAML_FILE = _YAML_DIR / "05-工作流管理-part2.yaml"
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
def test_TC_WF_INSTANCE_001(module_context, request_helper):
    """GET /workflow/instance/pageByRunning_默认分页查询_返回运行中流程实例列表"""
    case = _get_case("TC_WF_INSTANCE_001")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_001", case, data)

@pytest.mark.order(2)
def test_TC_WF_INSTANCE_002(module_context, request_helper):
    """GET /workflow/instance/pageByRunning_传入超界页码_返回空列表"""
    case = _get_case("TC_WF_INSTANCE_002")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_002", case, data)

@pytest.mark.order(3)
def test_TC_WF_INSTANCE_003(module_context, request_helper):
    """GET /workflow/instance/pageByFinish_默认分页查询_返回已结束流程实例列表"""
    case = _get_case("TC_WF_INSTANCE_003")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_003", case, data)

@pytest.mark.order(4)
def test_TC_WF_INSTANCE_004(module_context, request_helper):
    """GET /workflow/instance/pageByFinish_传入超界页码_返回空列表"""
    case = _get_case("TC_WF_INSTANCE_004")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_004", case, data)

@pytest.mark.order(5)
def test_TC_WF_INSTANCE_005(module_context, request_helper):
    """GET /workflow/instance/getInfo/{businessId}_有效业务ID查询_返回流程实例详情"""
    case = _get_case("TC_WF_INSTANCE_005")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_005", case, data)

@pytest.mark.order(6)
def test_TC_WF_INSTANCE_006(module_context, request_helper):
    """GET /workflow/instance/getInfo/{businessId}_不存在的业务ID_返回未找到流程实例"""
    case = _get_case("TC_WF_INSTANCE_006")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_006", case, data)

@pytest.mark.order(7)
def test_TC_WF_INSTANCE_007(module_context, request_helper):
    """DELETE /workflow/instance/deleteByBusinessIds/{businessIds}_有效业务ID删除_返回操作成功"""
    case = _get_case("TC_WF_INSTANCE_007")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_007", case, data)

@pytest.mark.order(8)
def test_TC_WF_INSTANCE_008(module_context, request_helper):
    """DELETE /workflow/instance/deleteByBusinessIds/{businessIds}_所有业务ID均不存在_返回操作失败"""
    case = _get_case("TC_WF_INSTANCE_008")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_008", case, data)

@pytest.mark.order(9)
def test_TC_WF_INSTANCE_009(module_context, request_helper):
    """DELETE /workflow/instance/deleteByInstanceIds/{instanceIds}_有效实例ID删除_返回操作成功"""
    case = _get_case("TC_WF_INSTANCE_009")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_009", case, data)

@pytest.mark.order(10)
def test_TC_WF_INSTANCE_010(module_context, request_helper):
    """DELETE /workflow/instance/deleteByInstanceIds/{instanceIds}_所有实例ID均不存在_返回操作失败"""
    case = _get_case("TC_WF_INSTANCE_010")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_010", case, data)

@pytest.mark.order(11)
def test_TC_WF_INSTANCE_011(module_context, request_helper):
    """DELETE /workflow/instance/deleteHisByInstanceIds/{instanceIds}_有效已完成实例ID删除_返回操作成功"""
    case = _get_case("TC_WF_INSTANCE_011")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_011", case, data)

@pytest.mark.order(12)
def test_TC_WF_INSTANCE_012(module_context, request_helper):
    """DELETE /workflow/instance/deleteHisByInstanceIds/{instanceIds}_所有实例ID均不存在_返回操作失败"""
    case = _get_case("TC_WF_INSTANCE_012")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_012", case, data)

@pytest.mark.order(13)
def test_TC_WF_INSTANCE_013(module_context, request_helper):
    """PUT /workflow/instance/cancelProcessApply_发起人撤销待审核流程_返回操作成功"""
    case = _get_case("TC_WF_INSTANCE_013")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_013", case, data)

@pytest.mark.order(14)
def test_TC_WF_INSTANCE_014(module_context, request_helper):
    """PUT /workflow/instance/cancelProcessApply_不存在业务ID_返回未找到流程实例"""
    case = _get_case("TC_WF_INSTANCE_014")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_014", case, data)

@pytest.mark.order(15)
def test_TC_WF_INSTANCE_015(module_context, request_helper):
    """PUT /workflow/instance/active/{id}_激活流程实例_返回操作成功"""
    case = _get_case("TC_WF_INSTANCE_015")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_015", case, data)

@pytest.mark.order(16)
def test_TC_WF_INSTANCE_016(module_context, request_helper):
    """PUT /workflow/instance/active/{id}_挂起不存在的流程实例_返回操作失败"""
    case = _get_case("TC_WF_INSTANCE_016")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_016", case, data)

@pytest.mark.order(17)
def test_TC_WF_INSTANCE_017(module_context, request_helper):
    """GET /workflow/instance/pageByCurrent_默认分页查询_返回当前登录人流程实例列表"""
    case = _get_case("TC_WF_INSTANCE_017")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_017", case, data)

@pytest.mark.order(18)
def test_TC_WF_INSTANCE_018(module_context, request_helper):
    """GET /workflow/instance/pageByCurrent_传入超界页码_返回空列表"""
    case = _get_case("TC_WF_INSTANCE_018")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_018", case, data)

@pytest.mark.order(19)
def test_TC_WF_INSTANCE_019(module_context, request_helper):
    """GET /workflow/instance/flowHisTaskList/{businessId}_有效业务ID查询_返回流程图和任务记录"""
    case = _get_case("TC_WF_INSTANCE_019")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_019", case, data)

@pytest.mark.order(20)
def test_TC_WF_INSTANCE_020(module_context, request_helper):
    """GET /workflow/instance/flowHisTaskList/{businessId}_不存在的业务ID_返回未找到流程实例"""
    case = _get_case("TC_WF_INSTANCE_020")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_020", case, data)

@pytest.mark.order(21)
def test_TC_WF_INSTANCE_021(module_context, request_helper):
    """GET /workflow/instance/instanceVariable/{instanceId}_有效实例ID查询_返回流程变量键值对"""
    case = _get_case("TC_WF_INSTANCE_021")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_021", case, data)

@pytest.mark.order(22)
def test_TC_WF_INSTANCE_022(module_context, request_helper):
    """GET /workflow/instance/instanceVariable/{instanceId}_不存在的实例ID_返回未找到流程实例"""
    case = _get_case("TC_WF_INSTANCE_022")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_022", case, data)

@pytest.mark.order(23)
def test_TC_WF_INSTANCE_023(module_context, request_helper):
    """PUT /workflow/instance/updateVariable_修改已存在的流程变量_返回操作成功"""
    case = _get_case("TC_WF_INSTANCE_023")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_023", case, data)

@pytest.mark.order(24)
def test_TC_WF_INSTANCE_024(module_context, request_helper):
    """PUT /workflow/instance/updateVariable_key为null_返回参数必须填写"""
    case = _get_case("TC_WF_INSTANCE_024")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_024", case, data)

@pytest.mark.order(25)
def test_TC_WF_INSTANCE_025(module_context, request_helper):
    """POST /workflow/instance/invalid_作废待审核流程_返回操作成功"""
    case = _get_case("TC_WF_INSTANCE_025")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_025", case, data)

@pytest.mark.order(26)
def test_TC_WF_INSTANCE_026(module_context, request_helper):
    """POST /workflow/instance/invalid_id为null_返回参数必须填写"""
    case = _get_case("TC_WF_INSTANCE_026")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_026", case, data)

@pytest.mark.order(27)
def test_TC_WF_INSTANCE_027(module_context, request_helper):
    """GET /workflow/spel/list_默认分页查询_返回Spel表达式定义列表"""
    case = _get_case("TC_WF_INSTANCE_027")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_027", case, data)

@pytest.mark.order(28)
def test_TC_WF_INSTANCE_028(module_context, request_helper):
    """GET /workflow/spel/list_按状态过滤已停用_返回筛选结果"""
    case = _get_case("TC_WF_INSTANCE_028")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_028", case, data)

@pytest.mark.order(29)
def test_TC_WF_INSTANCE_029(module_context, request_helper):
    """GET /workflow/spel/{id}_有效ID查询_返回Spel表达式详情"""
    case = _get_case("TC_WF_INSTANCE_029")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_029", case, data)

@pytest.mark.order(30)
def test_TC_WF_INSTANCE_030(module_context, request_helper):
    """GET /workflow/spel/{id}_id为null_返回主键不能为空"""
    case = _get_case("TC_WF_INSTANCE_030")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_030", case, data)

@pytest.mark.order(31)
def test_TC_WF_INSTANCE_031(module_context, request_helper):
    """POST /workflow/spel_新增有效Spel表达式定义_返回操作成功"""
    case = _get_case("TC_WF_INSTANCE_031")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_031", case, data)

@pytest.mark.order(32)
def test_TC_WF_INSTANCE_032(module_context, request_helper):
    """POST /workflow/spel_缺少viewSpel_返回参数必须填写"""
    case = _get_case("TC_WF_INSTANCE_032")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_032", case, data)

@pytest.mark.order(33)
def test_TC_WF_INSTANCE_033(module_context, request_helper):
    """PUT /workflow/spel_修改已有Spel表达式定义_返回操作成功"""
    case = _get_case("TC_WF_INSTANCE_033")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_033", case, data)

@pytest.mark.order(34)
def test_TC_WF_INSTANCE_034(module_context, request_helper):
    """PUT /workflow/spel_缺少status_返回参数必须填写"""
    case = _get_case("TC_WF_INSTANCE_034")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_034", case, data)

@pytest.mark.order(35)
def test_TC_WF_INSTANCE_035(module_context, request_helper):
    """DELETE /workflow/spel/{ids}_有效ID删除_返回操作成功"""
    case = _get_case("TC_WF_INSTANCE_035")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_035", case, data)

@pytest.mark.order(36)
def test_TC_WF_INSTANCE_036(module_context, request_helper):
    """DELETE /workflow/spel/{ids}_ids为空_返回主键不能为空"""
    case = _get_case("TC_WF_INSTANCE_036")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_INSTANCE_036", case, data)

