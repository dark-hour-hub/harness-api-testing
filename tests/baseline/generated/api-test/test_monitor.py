"""
test_monitor.py --- 由 yaml-to-pytest skill 自动生成，请勿手动修改

数据来源: 03-监控管理.yaml
模块: 监控管理
"""
import pytest
import yaml
from pathlib import Path

# --- 加载 YAML 数据（修改 YAML 后重新运行 pytest 即可生效，无需重新生成本文件）---
_YAML_DIR = Path(__file__).resolve().parents[2] / "_workflow/04-testcases"
_YAML_FILE = _YAML_DIR / "03-监控管理.yaml"
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
def test_TC_MONITOR_001(module_context, request_helper):
    """GET /monitor/logininfor/list_分页查询登录日志_返回rows和total"""
    case = _get_case("TC_MONITOR_001")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_001", case, data)

@pytest.mark.order(2)
def test_TC_MONITOR_002(module_context, request_helper):
    """GET /monitor/logininfor/list_传入非法排序字段_返回排序参数有误"""
    case = _get_case("TC_MONITOR_002")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_002", case, data)

@pytest.mark.order(3)
def test_TC_MONITOR_003(module_context, request_helper):
    """DELETE /monitor/logininfor/{infoIds}_删除存在的登录日志ID_返回操作成功"""
    case = _get_case("TC_MONITOR_003")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_003", case, data)

@pytest.mark.order(4)
def test_TC_MONITOR_004(module_context, request_helper):
    """DELETE /monitor/logininfor/{infoIds}_删除不存在的登录日志ID_返回操作失败"""
    case = _get_case("TC_MONITOR_004")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_004", case, data)

@pytest.mark.order(5)
def test_TC_MONITOR_005(module_context, request_helper):
    """DELETE /monitor/logininfor/clean_清空所有登录日志_返回操作成功"""
    case = _get_case("TC_MONITOR_005")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_005", case, data)

@pytest.mark.order(6)
def test_TC_MONITOR_006(module_context, request_helper):
    """DELETE /monitor/logininfor/clean_并发清理触发防重锁_返回操作失败"""
    case = _get_case("TC_MONITOR_006")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_006", case, data)

@pytest.mark.order(7)
def test_TC_MONITOR_007(module_context, request_helper):
    """GET /monitor/logininfor/unlock/{userName}_解锁被锁定用户_返回操作成功"""
    case = _get_case("TC_MONITOR_007")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_007", case, data)

@pytest.mark.order(8)
def test_TC_MONITOR_008(module_context, request_helper):
    """GET /monitor/logininfor/unlock/{userName}_解锁不存在的用户_返回操作成功"""
    case = _get_case("TC_MONITOR_008")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_008", case, data)

@pytest.mark.order(9)
def test_TC_MONITOR_009(module_context, request_helper):
    """GET /monitor/operlog/list_分页查询操作日志_返回rows和total"""
    case = _get_case("TC_MONITOR_009")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_009", case, data)

@pytest.mark.order(10)
def test_TC_MONITOR_010(module_context, request_helper):
    """GET /monitor/operlog/list_传入非法排序字段_返回排序参数有误"""
    case = _get_case("TC_MONITOR_010")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_010", case, data)

@pytest.mark.order(11)
def test_TC_MONITOR_011(module_context, request_helper):
    """DELETE /monitor/operlog/{operIds}_删除存在的操作日志ID_返回操作成功"""
    case = _get_case("TC_MONITOR_011")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_011", case, data)

@pytest.mark.order(12)
def test_TC_MONITOR_012(module_context, request_helper):
    """DELETE /monitor/operlog/{operIds}_删除不存在的操作日志ID_返回操作失败"""
    case = _get_case("TC_MONITOR_012")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_012", case, data)

@pytest.mark.order(13)
def test_TC_MONITOR_013(module_context, request_helper):
    """DELETE /monitor/operlog/clean_清空所有操作日志_返回操作成功"""
    case = _get_case("TC_MONITOR_013")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_013", case, data)

@pytest.mark.order(14)
def test_TC_MONITOR_014(module_context, request_helper):
    """DELETE /monitor/operlog/clean_并发清理触发防重锁_返回操作失败"""
    case = _get_case("TC_MONITOR_014")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_014", case, data)

@pytest.mark.order(15)
def test_TC_MONITOR_015(module_context, request_helper):
    """GET /monitor/online/list_查询在线用户列表_返回rows和total"""
    case = _get_case("TC_MONITOR_015")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_015", case, data)

@pytest.mark.order(16)
def test_TC_MONITOR_016(module_context, request_helper):
    """GET /monitor/online/list_筛选不存在的用户名_返回空结果集"""
    case = _get_case("TC_MONITOR_016")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_016", case, data)

@pytest.mark.order(17)
def test_TC_MONITOR_017(module_context, request_helper):
    """DELETE /monitor/online/{tokenId}_强退在线用户token_返回操作成功"""
    case = _get_case("TC_MONITOR_017")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_017", case, data)

@pytest.mark.order(18)
def test_TC_MONITOR_018(module_context, request_helper):
    """DELETE /monitor/online/{tokenId}_强退不存在的token_返回操作成功"""
    case = _get_case("TC_MONITOR_018")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_018", case, data)

@pytest.mark.order(19)
def test_TC_MONITOR_019(module_context, request_helper):
    """GET /monitor/online_获取当前用户在线设备列表_返回设备信息"""
    case = _get_case("TC_MONITOR_019")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_019", case, data)

@pytest.mark.order(20)
def test_TC_MONITOR_020(module_context, request_helper):
    """GET /monitor/online_验证返回设备均属于当前登录用户_数据范围正确"""
    case = _get_case("TC_MONITOR_020")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_020", case, data)

@pytest.mark.order(21)
def test_TC_MONITOR_021(module_context, request_helper):
    """DELETE /monitor/online/myself/{tokenId}_强退自己的在线设备_返回操作成功"""
    case = _get_case("TC_MONITOR_021")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_021", case, data)

@pytest.mark.order(22)
def test_TC_MONITOR_022(module_context, request_helper):
    """DELETE /monitor/online/myself/{tokenId}_强退他人或不存在的token_返回操作成功"""
    case = _get_case("TC_MONITOR_022")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_022", case, data)

@pytest.mark.order(23)
def test_TC_MONITOR_023(module_context, request_helper):
    """GET /monitor/cache_获取Redis缓存监控信息_返回info和dbSize和commandStats"""
    case = _get_case("TC_MONITOR_023")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_023", case, data)

@pytest.mark.order(24)
def test_TC_MONITOR_024(module_context, request_helper):
    """GET /monitor/cache_Redis连接异常_返回发生系统异常"""
    case = _get_case("TC_MONITOR_024")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_MONITOR_024", case, data)

