"""
test_system_user.py --- 由 yaml-to-pytest skill 自动生成，请勿手动修改

数据来源: 02-系统管理-part1.yaml
模块: 用户管理
"""
import pytest
import yaml
from pathlib import Path

# --- 加载 YAML 数据（修改 YAML 后重新运行 pytest 即可生效，无需重新生成本文件）---
_YAML_DIR = Path(__file__).resolve().parents[2] / "_workflow/02-diff-testcases"
_YAML_FILE = _YAML_DIR / "02-系统管理-part1.yaml"
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
def test_TC_USER_001(module_context, request_helper):
    """GET /system/user/getInfo_有效登录态获取管理员信息_返回用户权限及角色集"""
    case = _get_case("TC_USER_001")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_001", case, data)

@pytest.mark.order(2)
def test_TC_USER_002(module_context, request_helper):
    """GET /system/user/getInfo_携带多余查询参数_系统忽略并正常返回当前用户信息"""
    case = _get_case("TC_USER_002")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_002", case, data)

@pytest.mark.order(3)
def test_TC_USER_003(module_context, request_helper):
    """GET /system/user/{userId}_传入有效管理员用户ID_返回用户详情及岗位address字段"""
    case = _get_case("TC_USER_003")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_003", case, data)

@pytest.mark.order(4)
def test_TC_USER_004(module_context, request_helper):
    """GET /system/user/{userId}_传入不存在的用户ID_返回数据权限校验失败"""
    case = _get_case("TC_USER_004")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_USER_004", case, data)

