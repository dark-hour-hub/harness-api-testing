"""
test_auth.py --- 由 yaml-to-pytest skill 自动生成，请勿手动修改

数据来源: 01-认证模块.yaml
模块: 认证模块
"""
import pytest
import yaml
from pathlib import Path

# --- 加载 YAML 数据（修改 YAML 后重新运行 pytest 即可生效，无需重新生成本文件）---
_YAML_DIR = Path(__file__).resolve().parents[2] / "_workflow/02-diff-testcases"
_YAML_FILE = _YAML_DIR / "01-认证模块.yaml"
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
def test_TC_AUTH_001(module_context, request_helper):
    """POST /auth/login_有效密码凭证登录_返回token"""
    case = _get_case("TC_AUTH_001")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_AUTH_001", case, data)

@pytest.mark.order(2)
def test_TC_AUTH_002(module_context, request_helper):
    """POST /auth/login_密码错误_返回用户认证失败"""
    case = _get_case("TC_AUTH_002")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("TC_AUTH_002", case, data)

