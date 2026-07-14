"""
test_gen.py --- 由 yaml-to-pytest skill 自动生成，请勿手动修改

数据来源: 04-代码生成.yaml
模块: 代码生成
"""
import pytest
import yaml
from pathlib import Path

# --- 加载 YAML 数据（修改 YAML 后重新运行 pytest 即可生效，无需重新生成本文件）---
_YAML_DIR = Path(__file__).resolve().parents[2] / "_workflow/04-testcases"
_YAML_FILE = _YAML_DIR / "04-代码生成.yaml"
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
def test_TC_GEN_001(module_context, request_helper):
    """GET /tool/gen/list_分页查询已导入表配置_返回代码生成列表"""
    case = _get_case("TC_GEN_001")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_GEN_001", case, data)

@pytest.mark.order(2)
def test_TC_GEN_002(module_context, request_helper):
    """GET /tool/gen/list_传入非法排序参数_返回排序参数有误"""
    case = _get_case("TC_GEN_002")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_GEN_002", case, data)

@pytest.mark.order(3)
def test_TC_GEN_003(module_context, request_helper):
    """GET /tool/gen/{tableId}_查询已导入表配置详情_返回表信息和字段列表"""
    case = _get_case("TC_GEN_003")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_GEN_003", case, data)

@pytest.mark.order(4)
def test_TC_GEN_004(module_context, request_helper):
    """GET /tool/gen/{tableId}_传入不存在的tableId_返回未知异常"""
    case = _get_case("TC_GEN_004")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_GEN_004", case, data)

@pytest.mark.order(5)
def test_TC_GEN_005(module_context, request_helper):
    """GET /tool/gen/db/list_分页查询未导入数据库表_返回数据库表列表"""
    case = _get_case("TC_GEN_005")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_GEN_005", case, data)

@pytest.mark.order(6)
def test_TC_GEN_006(module_context, request_helper):
    """GET /tool/gen/db/list_传入非法排序参数_返回排序参数有误"""
    case = _get_case("TC_GEN_006")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_GEN_006", case, data)

@pytest.mark.order(7)
def test_TC_GEN_007(module_context, request_helper):
    """GET /tool/gen/column/{tableId}_查询表字段列表_返回字段配置信息"""
    case = _get_case("TC_GEN_007")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_GEN_007", case, data)

@pytest.mark.order(8)
def test_TC_GEN_008(module_context, request_helper):
    """GET /tool/gen/column/{tableId}_tableId传入非数字字符串_返回参数类型不匹配"""
    case = _get_case("TC_GEN_008")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_GEN_008", case, data)

@pytest.mark.order(9)
def test_TC_GEN_009(module_context, request_helper):
    """POST /tool/gen/importTable_导入有效表结构_返回导入成功"""
    case = _get_case("TC_GEN_009")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_GEN_009", case, data)

@pytest.mark.order(10)
def test_TC_GEN_010(module_context, request_helper):
    """POST /tool/gen/importTable_tables参数为空_返回导入失败"""
    case = _get_case("TC_GEN_010")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_GEN_010", case, data)

@pytest.mark.order(11)
def test_TC_GEN_011(module_context, request_helper):
    """PUT /tool/gen_修改代码生成配置_返回修改成功"""
    case = _get_case("TC_GEN_011")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_GEN_011", case, data)

@pytest.mark.order(12)
def test_TC_GEN_012(module_context, request_helper):
    """PUT /tool/gen_dataName字段为空_返回数据源名称不能为空"""
    case = _get_case("TC_GEN_012")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_GEN_012", case, data)

@pytest.mark.order(13)
def test_TC_GEN_013(module_context, request_helper):
    """DELETE /tool/gen/{tableIds}_删除已导入的代码生成配置_返回删除成功"""
    case = _get_case("TC_GEN_013")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_GEN_013", case, data)

@pytest.mark.order(14)
def test_TC_GEN_014(module_context, request_helper):
    """DELETE /tool/gen/{tableIds}_tableIds传入非数字字符串_返回参数类型不匹配"""
    case = _get_case("TC_GEN_014")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_GEN_014", case, data)

@pytest.mark.order(15)
def test_TC_GEN_015(module_context, request_helper):
    """GET /tool/gen/preview/{tableId}_预览已配置表的生成代码_返回代码内容映射"""
    case = _get_case("TC_GEN_015")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_GEN_015", case, data)

@pytest.mark.order(16)
def test_TC_GEN_016(module_context, request_helper):
    """GET /tool/gen/preview/{tableId}_传入不存在的tableId_返回未知异常"""
    case = _get_case("TC_GEN_016")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_GEN_016", case, data)

@pytest.mark.order(17)
def test_TC_GEN_017(module_context, request_helper):
    """GET /tool/gen/synchDb/{tableId}_同步数据库表结构_返回同步成功"""
    case = _get_case("TC_GEN_017")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_GEN_017", case, data)

@pytest.mark.order(18)
def test_TC_GEN_018(module_context, request_helper):
    """GET /tool/gen/synchDb/{tableId}_传入不存在的tableId_返回未知异常"""
    case = _get_case("TC_GEN_018")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_GEN_018", case, data)

@pytest.mark.order(19)
def test_TC_GEN_019(module_context, request_helper):
    """GET /tool/gen/getDataNames_查询可用数据源列表_返回数据源名称数组"""
    case = _get_case("TC_GEN_019")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_GEN_019", case, data)

@pytest.mark.order(20)
def test_TC_GEN_020(module_context, request_helper):
    """GET /tool/gen/getDataNames_未携带认证Token_返回401认证失败"""
    case = _get_case("TC_GEN_020")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_GEN_020", case, data)

