"""
test_sys-oss.py --- 由 yaml-to-pytest skill 自动生成，请勿手动修改

数据来源: 02-系统管理-part7.yaml
模块: 系统管理-OSS对象存储+OSS配置
"""
import pytest
import yaml
from pathlib import Path

# --- 加载 YAML 数据（修改 YAML 后重新运行 pytest 即可生效，无需重新生成本文件）---
_YAML_DIR = Path(__file__).resolve().parents[2] / "_workflow/04-testcases"
_YAML_FILE = _YAML_DIR / "02-系统管理-part7.yaml"
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
def test_TC_OSS_001(module_context, request_helper):
    """GET /resource/oss/list_默认分页查询_返回OSS文件列表"""
    case = _get_case("TC_OSS_001")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OSS_001", case, data)

@pytest.mark.order(2)
def test_TC_OSS_002(module_context, request_helper):
    """GET /resource/oss/list_传入非数值pageNum_返回参数绑定异常"""
    case = _get_case("TC_OSS_002")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OSS_002", case, data)

@pytest.mark.order(3)
def test_TC_OSS_003(module_context, request_helper):
    """GET /resource/oss/listByIds/{ossIds}_传入有效ID数组_返回对应OSS文件列表"""
    case = _get_case("TC_OSS_003")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OSS_003", case, data)

@pytest.mark.order(4)
def test_TC_OSS_004(module_context, request_helper):
    """GET /resource/oss/listByIds/{ossIds}_传入空ossIds_返回主键不能为空"""
    case = _get_case("TC_OSS_004")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OSS_004", case, data)

@pytest.mark.order(5)
def test_TC_OSS_005(module_context, request_helper):
    """POST /resource/oss/upload_上传有效文件_返回文件URL和OSS对象信息"""
    case = _get_case("TC_OSS_005")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OSS_005", case, data)

@pytest.mark.order(6)
def test_TC_OSS_006(module_context, request_helper):
    """POST /resource/oss/upload_未上传文件_返回上传文件不能为空"""
    case = _get_case("TC_OSS_006")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OSS_006", case, data)

@pytest.mark.order(7)
def test_TC_OSS_007(module_context, request_helper):
    """DELETE /resource/oss/{ossIds}_删除存在的OSS对象_返回操作成功"""
    case = _get_case("TC_OSS_007")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OSS_007", case, data)

@pytest.mark.order(8)
def test_TC_OSS_008(module_context, request_helper):
    """DELETE /resource/oss/{ossIds}_传入空ossIds_返回主键不能为空"""
    case = _get_case("TC_OSS_008")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OSS_008", case, data)

@pytest.mark.order(9)
def test_TC_OSS_009(module_context, request_helper):
    """GET /resource/oss/config/list_默认分页查询_返回配置列表"""
    case = _get_case("TC_OSS_009")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OSS_009", case, data)

@pytest.mark.order(10)
def test_TC_OSS_010(module_context, request_helper):
    """GET /resource/oss/config/list_传入非数值pageNum_返回参数绑定异常"""
    case = _get_case("TC_OSS_010")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OSS_010", case, data)

@pytest.mark.order(11)
def test_TC_OSS_011(module_context, request_helper):
    """GET /resource/oss/config/{ossConfigId}_查询存在的配置_返回配置详情"""
    case = _get_case("TC_OSS_011")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OSS_011", case, data)

@pytest.mark.order(12)
def test_TC_OSS_012(module_context, request_helper):
    """GET /resource/oss/config/{ossConfigId}_传入非数值ossConfigId_返回参数类型转换异常"""
    case = _get_case("TC_OSS_012")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OSS_012", case, data)

@pytest.mark.order(13)
def test_TC_OSS_013(module_context, request_helper):
    """POST /resource/oss/config_有效完整字段新增配置_返回操作成功"""
    case = _get_case("TC_OSS_013")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OSS_013", case, data)

@pytest.mark.order(14)
def test_TC_OSS_014(module_context, request_helper):
    """POST /resource/oss/config_缺少必填字段configKey_返回配置key不能为空"""
    case = _get_case("TC_OSS_014")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OSS_014", case, data)

@pytest.mark.order(15)
def test_TC_OSS_015(module_context, request_helper):
    """PUT /resource/oss/config_有效字段修改配置_返回操作成功"""
    case = _get_case("TC_OSS_015")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OSS_015", case, data)

@pytest.mark.order(16)
def test_TC_OSS_016(module_context, request_helper):
    """PUT /resource/oss/config_缺少ossConfigId_返回主键不能为空"""
    case = _get_case("TC_OSS_016")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OSS_016", case, data)

@pytest.mark.order(17)
def test_TC_OSS_017(module_context, request_helper):
    """PUT /resource/oss/config/changeStatus_修改配置为默认状态_返回操作成功"""
    case = _get_case("TC_OSS_017")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OSS_017", case, data)

@pytest.mark.order(18)
def test_TC_OSS_018(module_context, request_helper):
    """PUT /resource/oss/config/changeStatus_传入不存在的ossConfigId_返回操作失败"""
    case = _get_case("TC_OSS_018")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OSS_018", case, data)

@pytest.mark.order(19)
def test_TC_OSS_019(module_context, request_helper):
    """DELETE /resource/oss/config/{ossConfigIds}_删除非系统内置配置_返回操作成功"""
    case = _get_case("TC_OSS_019")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OSS_019", case, data)

@pytest.mark.order(20)
def test_TC_OSS_020(module_context, request_helper):
    """DELETE /resource/oss/config/{ossConfigIds}_传入空ossConfigIds_返回主键不能为空"""
    case = _get_case("TC_OSS_020")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_OSS_020", case, data)

