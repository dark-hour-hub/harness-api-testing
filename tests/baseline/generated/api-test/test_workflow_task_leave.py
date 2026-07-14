"""
test_workflow_task_leave.py --- 由 yaml-to-pytest skill 自动生成，请勿手动修改

数据来源: 05-工作流管理-part3.yaml
模块: 工作流管理-任务管理+请假示例
"""
import pytest
import yaml
from pathlib import Path

# --- 加载 YAML 数据（修改 YAML 后重新运行 pytest 即可生效，无需重新生成本文件）---
_YAML_DIR = Path(__file__).resolve().parents[2] / "_workflow/04-testcases"
_YAML_FILE = _YAML_DIR / "05-工作流管理-part3.yaml"
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
def test_TC_WF_TASK_001(module_context, request_helper):
    """POST /workflow/task/startWorkFlow_有效流程信息启动任务_返回流程实例和任务ID"""
    case = _get_case("TC_WF_TASK_001")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_001", case, data)

@pytest.mark.order(2)
def test_TC_WF_TASK_002(module_context, request_helper):
    """POST /workflow/task/startWorkFlow_businessId为空_返回业务ID不能为空"""
    case = _get_case("TC_WF_TASK_002")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_002", case, data)

@pytest.mark.order(3)
def test_TC_WF_TASK_003(module_context, request_helper):
    """POST /workflow/task/completeTask_有效taskId办理任务_返回操作成功"""
    case = _get_case("TC_WF_TASK_003")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_003", case, data)

@pytest.mark.order(4)
def test_TC_WF_TASK_004(module_context, request_helper):
    """POST /workflow/task/completeTask_taskId为空_返回任务id不能为空"""
    case = _get_case("TC_WF_TASK_004")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_004", case, data)

@pytest.mark.order(5)
def test_TC_WF_TASK_005(module_context, request_helper):
    """GET /workflow/task/pageByTaskWait_默认分页查询待办任务_返回待办列表及总数"""
    case = _get_case("TC_WF_TASK_005")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_005", case, data)

@pytest.mark.order(6)
def test_TC_WF_TASK_006(module_context, request_helper):
    """GET /workflow/task/pageByTaskWait_分页参数异常_返回空列表或默认分页"""
    case = _get_case("TC_WF_TASK_006")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_006", case, data)

@pytest.mark.order(7)
def test_TC_WF_TASK_007(module_context, request_helper):
    """GET /workflow/task/pageByTaskFinish_默认分页查询已办任务_返回已办列表及总数"""
    case = _get_case("TC_WF_TASK_007")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_007", case, data)

@pytest.mark.order(8)
def test_TC_WF_TASK_008(module_context, request_helper):
    """GET /workflow/task/pageByTaskFinish_分页参数异常_返回空列表或默认分页"""
    case = _get_case("TC_WF_TASK_008")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_008", case, data)

@pytest.mark.order(9)
def test_TC_WF_TASK_009(module_context, request_helper):
    """GET /workflow/task/pageByAllTaskWait_管理员查询所有待办任务_返回待办列表及总数"""
    case = _get_case("TC_WF_TASK_009")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_009", case, data)

@pytest.mark.order(10)
def test_TC_WF_TASK_010(module_context, request_helper):
    """GET /workflow/task/pageByAllTaskWait_按流程名称筛选查询_返回匹配的待办任务"""
    case = _get_case("TC_WF_TASK_010")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_010", case, data)

@pytest.mark.order(11)
def test_TC_WF_TASK_011(module_context, request_helper):
    """GET /workflow/task/pageByAllTaskFinish_管理员查询所有已办任务_返回已办列表及总数"""
    case = _get_case("TC_WF_TASK_011")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_011", case, data)

@pytest.mark.order(12)
def test_TC_WF_TASK_012(module_context, request_helper):
    """GET /workflow/task/pageByAllTaskFinish_按流程状态筛选查询_返回匹配的已办任务"""
    case = _get_case("TC_WF_TASK_012")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_012", case, data)

@pytest.mark.order(13)
def test_TC_WF_TASK_013(module_context, request_helper):
    """GET /workflow/task/pageByTaskCopy_默认分页查询抄送任务_返回抄送列表及总数"""
    case = _get_case("TC_WF_TASK_013")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_013", case, data)

@pytest.mark.order(14)
def test_TC_WF_TASK_014(module_context, request_helper):
    """GET /workflow/task/pageByTaskCopy_分页参数异常_返回空列表或默认分页"""
    case = _get_case("TC_WF_TASK_014")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_014", case, data)

@pytest.mark.order(15)
def test_TC_WF_TASK_015(module_context, request_helper):
    """GET /workflow/task/getTask/{taskId}_有效taskId查询任务_返回任务详情"""
    case = _get_case("TC_WF_TASK_015")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_015", case, data)

@pytest.mark.order(16)
def test_TC_WF_TASK_016(module_context, request_helper):
    """GET /workflow/task/getTask/{taskId}_不存在的taskId_返回data为null"""
    case = _get_case("TC_WF_TASK_016")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_016", case, data)

@pytest.mark.order(17)
def test_TC_WF_TASK_017(module_context, request_helper):
    """POST /workflow/task/getNextNodeList_有效taskId获取下一节点_返回节点列表"""
    case = _get_case("TC_WF_TASK_017")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_017", case, data)

@pytest.mark.order(18)
def test_TC_WF_TASK_018(module_context, request_helper):
    """POST /workflow/task/getNextNodeList_不存在的taskId_返回任务不存在"""
    case = _get_case("TC_WF_TASK_018")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_018", case, data)

@pytest.mark.order(19)
def test_TC_WF_TASK_019(module_context, request_helper):
    """POST /workflow/task/terminationTask_有效taskId终止任务_返回终止成功"""
    case = _get_case("TC_WF_TASK_019")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_019", case, data)

@pytest.mark.order(20)
def test_TC_WF_TASK_020(module_context, request_helper):
    """POST /workflow/task/terminationTask_taskId为空_返回任务id为空"""
    case = _get_case("TC_WF_TASK_020")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_020", case, data)

@pytest.mark.order(21)
def test_TC_WF_TASK_021(module_context, request_helper):
    """POST /workflow/task/taskOperation/{taskOperation}_委派任务_返回操作成功"""
    case = _get_case("TC_WF_TASK_021")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_021", case, data)

@pytest.mark.order(22)
def test_TC_WF_TASK_022(module_context, request_helper):
    """POST /workflow/task/taskOperation/{taskOperation}_无效操作类型_返回操作类型无效"""
    case = _get_case("TC_WF_TASK_022")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_022", case, data)

@pytest.mark.order(23)
def test_TC_WF_TASK_023(module_context, request_helper):
    """PUT /workflow/task/updateAssignee/{userId}_批量修改任务办理人_返回操作成功"""
    case = _get_case("TC_WF_TASK_023")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_023", case, data)

@pytest.mark.order(24)
def test_TC_WF_TASK_024(module_context, request_helper):
    """PUT /workflow/task/updateAssignee/{userId}_taskIdList为空_返回false不执行操作"""
    case = _get_case("TC_WF_TASK_024")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_024", case, data)

@pytest.mark.order(25)
def test_TC_WF_TASK_025(module_context, request_helper):
    """POST /workflow/task/backProcess_有效taskId驳回审批_返回操作成功"""
    case = _get_case("TC_WF_TASK_025")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_025", case, data)

@pytest.mark.order(26)
def test_TC_WF_TASK_026(module_context, request_helper):
    """POST /workflow/task/backProcess_taskId为空_返回任务ID不能为空"""
    case = _get_case("TC_WF_TASK_026")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_026", case, data)

@pytest.mark.order(27)
def test_TC_WF_TASK_027(module_context, request_helper):
    """GET /workflow/task/getBackTaskNode/{taskId}/{nowNodeCode}_有效参数获取可驳回节点_返回前置节点列表"""
    case = _get_case("TC_WF_TASK_027")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_027", case, data)

@pytest.mark.order(28)
def test_TC_WF_TASK_028(module_context, request_helper):
    """GET /workflow/task/getBackTaskNode/{taskId}/{nowNodeCode}_不存在的taskId_返回空列表"""
    case = _get_case("TC_WF_TASK_028")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_028", case, data)

@pytest.mark.order(29)
def test_TC_WF_TASK_029(module_context, request_helper):
    """GET /workflow/task/currentTaskAllUser/{taskId}_有效taskId获取办理人_返回办理人列表"""
    case = _get_case("TC_WF_TASK_029")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_029", case, data)

@pytest.mark.order(30)
def test_TC_WF_TASK_030(module_context, request_helper):
    """GET /workflow/task/currentTaskAllUser/{taskId}_不存在的taskId_返回空列表"""
    case = _get_case("TC_WF_TASK_030")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_030", case, data)

@pytest.mark.order(31)
def test_TC_WF_TASK_031(module_context, request_helper):
    """POST /workflow/task/urgeTask_有效taskIdList催办任务_返回操作成功"""
    case = _get_case("TC_WF_TASK_031")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_031", case, data)

@pytest.mark.order(32)
def test_TC_WF_TASK_032(module_context, request_helper):
    """POST /workflow/task/urgeTask_message为空_返回催办内容为空"""
    case = _get_case("TC_WF_TASK_032")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_032", case, data)

@pytest.mark.order(33)
def test_TC_WF_TASK_033(module_context, request_helper):
    """POST /workflow/task/copyTask_有效抄送人员列表_返回操作成功"""
    case = _get_case("TC_WF_TASK_033")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_033", case, data)

@pytest.mark.order(34)
def test_TC_WF_TASK_034(module_context, request_helper):
    """POST /workflow/task/copyTask_空抄送列表_返回操作成功但不执行抄送"""
    case = _get_case("TC_WF_TASK_034")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_034", case, data)

@pytest.mark.order(35)
def test_TC_WF_TASK_035(module_context, request_helper):
    """GET /workflow/leave/list_默认分页查询请假列表_返回请假列表及总数"""
    case = _get_case("TC_WF_TASK_035")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_035", case, data)

@pytest.mark.order(36)
def test_TC_WF_TASK_036(module_context, request_helper):
    """GET /workflow/leave/list_按请假类型筛选查询_返回匹配的请假记录"""
    case = _get_case("TC_WF_TASK_036")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_036", case, data)

@pytest.mark.order(37)
def test_TC_WF_TASK_037(module_context, request_helper):
    """GET /workflow/leave/{id}_有效id查询请假_返回请假详情"""
    case = _get_case("TC_WF_TASK_037")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_037", case, data)

@pytest.mark.order(38)
def test_TC_WF_TASK_038(module_context, request_helper):
    """GET /workflow/leave/{id}_不存在的id_返回data为null"""
    case = _get_case("TC_WF_TASK_038")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_038", case, data)

@pytest.mark.order(39)
def test_TC_WF_TASK_039(module_context, request_helper):
    """POST /workflow/leave_有效请假信息新增请假_返回创建的请假记录"""
    case = _get_case("TC_WF_TASK_039")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_039", case, data)

@pytest.mark.order(40)
def test_TC_WF_TASK_040(module_context, request_helper):
    """POST /workflow/leave_leaveType为空_返回请假类型不能为空"""
    case = _get_case("TC_WF_TASK_040")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_040", case, data)

@pytest.mark.order(41)
def test_TC_WF_TASK_041(module_context, request_helper):
    """POST /workflow/leave/submitAndFlowStart_有效请假信息提交并启动流程_返回请假记录"""
    case = _get_case("TC_WF_TASK_041")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_041", case, data)

@pytest.mark.order(42)
def test_TC_WF_TASK_042(module_context, request_helper):
    """POST /workflow/leave/submitAndFlowStart_startDate为空_返回开始时间不能为空"""
    case = _get_case("TC_WF_TASK_042")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_042", case, data)

@pytest.mark.order(43)
def test_TC_WF_TASK_043(module_context, request_helper):
    """PUT /workflow/leave_有效请假信息修改请假_返回更新后的请假记录"""
    case = _get_case("TC_WF_TASK_043")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_043", case, data)

@pytest.mark.order(44)
def test_TC_WF_TASK_044(module_context, request_helper):
    """PUT /workflow/leave_id为空_返回主键不能为空"""
    case = _get_case("TC_WF_TASK_044")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_044", case, data)

@pytest.mark.order(45)
def test_TC_WF_TASK_045(module_context, request_helper):
    """DELETE /workflow/leave/{ids}_有效id删除请假_返回操作成功"""
    case = _get_case("TC_WF_TASK_045")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_045", case, data)

@pytest.mark.order(46)
def test_TC_WF_TASK_046(module_context, request_helper):
    """DELETE /workflow/leave/{ids}_ids为空_返回主键不能为空"""
    case = _get_case("TC_WF_TASK_046")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_WF_TASK_046", case, data)

