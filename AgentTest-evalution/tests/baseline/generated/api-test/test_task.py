"""
test_task.py --- 由 yaml-to-pytest skill 自动生成，请勿手动修改

数据来源: 04-评测任务模块.yaml
模块: 评测任务模块
"""
import pytest
import yaml
from pathlib import Path

# --- 加载 YAML 数据（修改 YAML 后重新运行 pytest 即可生效，无需重新生成本文件）---
_YAML_DIR = Path(__file__).resolve().parents[2] / "_workflow/04-testcases"
_YAML_FILE = _YAML_DIR / "04-评测任务模块.yaml"
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
def test_TC_TASK_PREP_001(module_context, request_helper):
    """前置_POST /api/evaluation-schemes_创建待发布方案"""
    case = _get_case("TC_TASK_PREP_001")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_PREP_001", case, data)

@pytest.mark.order(2)
def test_TC_TASK_PREP_002(module_context, request_helper):
    """前置_POST /api/evaluation-schemes/{id}/publish_发布方案"""
    case = _get_case("TC_TASK_PREP_002")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_PREP_002", case, data)

@pytest.mark.order(3)
def test_TC_TASK_001(module_context, request_helper):
    """POST /api/evaluation-tasks_合法agentId与schemeId_创建成功返回CREATED任务"""
    case = _get_case("TC_TASK_001")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_001", case, data)

@pytest.mark.order(4)
def test_TC_TASK_002(module_context, request_helper):
    """POST /api/evaluation-tasks_schemeId缺失_返回400校验错误"""
    case = _get_case("TC_TASK_002")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_002", case, data)

@pytest.mark.order(5)
def test_TC_TASK_003(module_context, request_helper):
    """POST /api/evaluation-tasks/ad-hoc_合法参数_创建成功返回CREATED任务"""
    case = _get_case("TC_TASK_003")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_003", case, data)

@pytest.mark.order(6)
def test_TC_TASK_004(module_context, request_helper):
    """POST /api/evaluation-tasks/ad-hoc_indicators为空_返回400校验错误"""
    case = _get_case("TC_TASK_004")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_004", case, data)

@pytest.mark.order(7)
def test_TC_TASK_005(module_context, request_helper):
    """GET /api/evaluation-tasks_分页并按状态过滤_返回分页数据"""
    case = _get_case("TC_TASK_005")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_005", case, data)

@pytest.mark.order(8)
def test_TC_TASK_006(module_context, request_helper):
    """GET /api/evaluation-tasks_status非法枚举_返回400校验错误"""
    case = _get_case("TC_TASK_006")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_006", case, data)

@pytest.mark.order(9)
def test_TC_TASK_007(module_context, request_helper):
    """GET /api/evaluation-tasks/{id}_查询已创建任务_返回任务详情"""
    case = _get_case("TC_TASK_007")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_007", case, data)

@pytest.mark.order(10)
def test_TC_TASK_008(module_context, request_helper):
    """GET /api/evaluation-tasks/{id}_任务不存在_返回404"""
    case = _get_case("TC_TASK_008")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_008", case, data)

@pytest.mark.order(11)
def test_TC_TASK_009(module_context, request_helper):
    """GET /api/evaluation-tasks/{id}/progress_查询已创建任务进度_返回进度信息"""
    case = _get_case("TC_TASK_009")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_009", case, data)

@pytest.mark.order(12)
def test_TC_TASK_010(module_context, request_helper):
    """GET /api/evaluation-tasks/{id}/progress_任务不存在_返回404"""
    case = _get_case("TC_TASK_010")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_010", case, data)

@pytest.mark.order(13)
def test_TC_TASK_011(module_context, request_helper):
    """POST /api/evaluation-tasks/{id}/run_CREATED状态任务启动_返回202异步受理"""
    case = _get_case("TC_TASK_011")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_011", case, data)

@pytest.mark.order(14)
def test_TC_TASK_012(module_context, request_helper):
    """POST /api/evaluation-tasks/{id}/run_任务非CREATED状态重复启动_返回409状态冲突"""
    case = _get_case("TC_TASK_012")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_012", case, data)

@pytest.mark.order(15)
def test_TC_TASK_013(module_context, request_helper):
    """POST /api/evaluation-tasks/{taskId}/measurements_提交合法测量_返回DRAFT证据"""
    case = _get_case("TC_TASK_013")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_013", case, data)

@pytest.mark.order(16)
def test_TC_TASK_014(module_context, request_helper):
    """POST /api/evaluation-tasks/{taskId}/measurements_任务不存在_返回404"""
    case = _get_case("TC_TASK_014")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_014", case, data)

@pytest.mark.order(17)
def test_TC_TASK_015(module_context, request_helper):
    """POST /api/evaluation-tasks/{taskId}/measurements/{measurementId}/confirm_确认DRAFT测量_返回CONFIRMED证据"""
    case = _get_case("TC_TASK_015")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_015", case, data)

@pytest.mark.order(18)
def test_TC_TASK_016(module_context, request_helper):
    """POST /api/evaluation-tasks/{taskId}/measurements/{measurementId}/confirm_测量记录不存在_返回404"""
    case = _get_case("TC_TASK_016")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_016", case, data)

@pytest.mark.order(19)
def test_TC_TASK_017(module_context, request_helper):
    """POST /api/evaluation-tasks/{id}/finalize_任务非COMPLETED状态_返回409状态冲突"""
    case = _get_case("TC_TASK_017")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_017", case, data)

@pytest.mark.order(20)
def test_TC_TASK_018(module_context, request_helper):
    """POST /api/evaluation-tasks/{id}/finalize_id非数字_返回400校验错误"""
    case = _get_case("TC_TASK_018")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_018", case, data)

@pytest.mark.order(21)
def test_TC_TASK_019(module_context, request_helper):
    """GET /api/evaluation-tasks/{id}/results_任务结果未就绪_返回409"""
    case = _get_case("TC_TASK_019")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_019", case, data)

@pytest.mark.order(22)
def test_TC_TASK_020(module_context, request_helper):
    """GET /api/evaluation-tasks/{id}/results_任务不存在_返回404"""
    case = _get_case("TC_TASK_020")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_020", case, data)

@pytest.mark.order(23)
def test_TC_TASK_021(module_context, request_helper):
    """GET /api/evaluation-tasks/{id}/results/indicators_分页查询指标结果_返回分页数据"""
    case = _get_case("TC_TASK_021")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_021", case, data)

@pytest.mark.order(24)
def test_TC_TASK_022(module_context, request_helper):
    """GET /api/evaluation-tasks/{id}/results/indicators_status非法值_返回400校验错误"""
    case = _get_case("TC_TASK_022")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_022", case, data)

@pytest.mark.order(25)
def test_TC_TASK_023(module_context, request_helper):
    """GET /api/evaluation-tasks/{id}/case-results_分页查询用例结果_返回分页数据"""
    case = _get_case("TC_TASK_023")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_023", case, data)

@pytest.mark.order(26)
def test_TC_TASK_024(module_context, request_helper):
    """GET /api/evaluation-tasks/{id}/case-results_passed非法值_返回400校验错误"""
    case = _get_case("TC_TASK_024")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_024", case, data)

@pytest.mark.order(27)
def test_TC_TASK_025(module_context, request_helper):
    """GET /api/evaluation-tasks/{id}/calls_分页查询调用记录_返回分页数据"""
    case = _get_case("TC_TASK_025")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_025", case, data)

@pytest.mark.order(28)
def test_TC_TASK_026(module_context, request_helper):
    """GET /api/evaluation-tasks/{id}/calls_errorType非法值_返回400校验错误"""
    case = _get_case("TC_TASK_026")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_026", case, data)

@pytest.mark.order(29)
def test_TC_TASK_027(module_context, request_helper):
    """GET /api/evaluation-tasks/{id}/report_报告未就绪_返回409"""
    case = _get_case("TC_TASK_027")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_027", case, data)

@pytest.mark.order(30)
def test_TC_TASK_028(module_context, request_helper):
    """GET /api/evaluation-tasks/{id}/report_id非数字_返回400校验错误"""
    case = _get_case("TC_TASK_028")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_TASK_028", case, data)

