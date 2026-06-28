"""
Generate YAML testcase files for all modules.
Applies inline rule: account values are inlined, only ${token}/${timestamp}/extract vars use ${}.
"""
import yaml
import os
from pathlib import Path
from collections import defaultdict


class NoAliasDumper(yaml.Dumper):
    """Prevent YAML anchors/aliases for duplicate content."""
    def ignore_aliases(self, data):
        return True


OUT_DIR = Path(r"D:/claude code/harness-testing/tests/baseline/_workflow/03-testcases")
os.makedirs(OUT_DIR, exist_ok=True)

BASE_URL = "http://localhost:8080"
TOKEN_PREFIX = "Bearer "
FIXTURE_EXTRACTS = {"clientId": "$.data.client_id"}
RESPONSE_MSG_FIELD = "msg"

ACCOUNTS = {
    "admin": {
        "username": "admin",
        "password": "admin123",
        "clientId": "e5cd7e4891bf95d1d19206ce24a7b32e",
        "grantType": "password",
        "tenantId": "000000",
    },
    "visitor": {
        "username": "test",
        "password": "666666",
        "clientId": "e5cd7e4891bf95d1d19206ce24a7b32e",
        "grantType": "password",
        "tenantId": "000000",
    },
}

GLOBAL_HEADERS = [
    {"name": "Authorization", "value": "Bearer ${token}", "required": True, "description": "Sa-Token 认证令牌"},
    {"name": "clientid", "value": "${clientId}", "required": True, "description": "客户端ID，与 Token 中的 clientId 校验一致"},
]

AUTH_CONFIG = {
    "type": "sa-token",
    "login_endpoint": "/auth/login",
    "token_header": "Authorization",
    "token_prefix": TOKEN_PREFIX,
    "token_response_path": "$.data.access_token",
    "response_msg_field": RESPONSE_MSG_FIELD,
    "fixture_extracts": FIXTURE_EXTRACTS,
    "accounts": ACCOUNTS,
}

tc_counter = defaultdict(int)


def next_id(module_key):
    tc_counter[module_key] += 1
    prefix = module_key.upper().replace("/", "_")
    return f"TC_{prefix}_{tc_counter[module_key]:03d}"


def with_timestamp(val):
    """Append ${timestamp} for values that need uniqueness."""
    if isinstance(val, str) and any(kw in val for kw in ("test_", "testuser", "关键", "新")):
        return val + "_${timestamp}"
    return val


def build_expected(method, path, negative=False):
    """Build expected section based on method and path."""
    if negative:
        return None  # Provided by negative case definition

    if method == "POST" and "/login" in path:
        return {
            "status_code": 200, "business_code": 200, "business_message": "操作成功",
            "data_exists": ["access_token", "refresh_token", "expire_in", "client_id"],
            "data_type": {"access_token": "str", "client_id": "str"},
        }
    if method == "POST" and "/logout" in path:
        return {"status_code": 200, "business_code": 200, "business_message": "退出成功"}
    if method == "GET" and "/list" in path:
        return {"status_code": 200, "data_exists": ["rows", "total"]}
    if method == "GET" and path == "/system/user/getInfo":
        return {"status_code": 200, "business_code": 200, "business_message": "操作成功", "data_exists": ["user", "permissions", "roles"]}
    if method == "GET" and path == "/auth/tenant/list":
        return {"status_code": 200, "business_code": 200, "business_message": "操作成功", "data_exists": ["tenantEnabled"]}
    if method in ("GET",) and path not in ("/", "/auth/code", "/auth/binding/gitee"):
        return {"status_code": 200, "business_code": 200, "business_message": "操作成功"}
    if method in ("POST", "PUT"):
        return {"status_code": 200, "business_code": 200, "business_message": "操作成功"}
    if method == "DELETE":
        return {"status_code": 200}
    return {"status_code": 200}


def build_title(method, path, neg_label, neg_expected):
    """Build testcase title."""
    base = f"{method} {path}"
    if neg_label:
        msg = neg_expected.get("business_message", "")
        return f"{base}_{neg_label}_{msg}"
    return f"{base}_预期成功"


def build_tags(negative, path):
    """Build tags list."""
    if negative:
        return ["异常", "回归"]
    tags = ["正常", "回归"]
    if path in ("/auth/login", "/auth/logout", "/system/user/getInfo"):
        tags.append("冒烟")
    return tags


def build_priority(method, path, negative):
    """Determine priority."""
    if negative:
        if path in ("/system/user/list", "/monitor/online/list"):
            return "P1"
        return "P1"
    if path in ("/auth/login", "/auth/logout", "/", "/system/user/getInfo", "/system/user/list"):
        return "P0"
    if method in ("POST", "PUT", "DELETE") and "/list" not in path:
        return "P1"
    if method == "GET" and "/list" in path:
        return "P1"
    return "P2"


def apply_body(body, account_name=""):
    """Apply inline account values and ${timestamp} to body dict."""
    result = {}
    for k, v in body.items():
        result[k] = with_timestamp(v)
    return result


def build_testcase(module_key, method, path, account, pos_body, negative):
    """Build a single testcase dict."""
    tc_id = next_id(module_key)

    if negative:
        neg_label, overrides, neg_expected, priority = negative
        title = build_title(method, path, neg_label, neg_expected)
        tags = build_tags(True, path)
        expected = neg_expected

        # Build request body: start from positive body, apply overrides
        body = apply_body(dict(pos_body)) if pos_body else {}

        remove_fields = overrides.get("remove_fields", [])
        for f in remove_fields:
            body.pop(f, None)

        body_overrides = overrides.get("body", {})
        body.update(body_overrides)

        headers = overrides.get("headers")
        params = overrides.get("params")
    else:
        title = build_title(method, path, None, None)
        priority = build_priority(method, path, False)
        tags = build_tags(False, path)
        expected = build_expected(method, path)

        body = apply_body(dict(pos_body)) if pos_body else {}
        headers = None
        params = None

    tc = {
        "id": tc_id,
        "title": title,
        "priority": priority,
        "tags": tags,
        "method": method,
        "path": path,
        "description": f"{method} {path} 接口测试",
    }

    if account:
        tc["account"] = account

    req = {}
    if params:
        req["params"] = params
    if body:
        req["body"] = body
    if headers:
        req["headers"] = headers
    if req:
        tc["request"] = req

    tc["expected"] = expected
    return tc


# ── Module Definitions ────────────────────────────────────────

MODULES = {
    "auth": {
        "module_name": "认证模块",
        "routes": [
            (
                "POST", "/auth/login", "admin", {
                    "clientId": "e5cd7e4891bf95d1d19206ce24a7b32e",
                    "grantType": "password", "tenantId": "000000",
                    "username": "admin", "password": "admin123",
                },
                [
                    ("缺失clientId", {"remove_fields": ["clientId"]},
                     {"status_code": 200, "business_code": 500, "business_message": "认证客户端id不能为空"}, "P1"),
                    ("缺失grantType", {"remove_fields": ["grantType"]},
                     {"status_code": 200, "business_code": 500, "business_message": "认证权限类型不能为空"}, "P1"),
                    ("错误的clientId", {"body": {"clientId": "invalid_client_id_12345"}},
                     {"status_code": 200, "business_code": 500, "business_message": "认证权限类型错误"}, "P1"),
                    ("密码错误", {"body": {"password": "wrongPassword123"}},
                     {"status_code": 200, "business_code": 500, "business_message": "用户不存在/密码错误"}, "P1"),
                ]
            ),
            ("POST", "/auth/logout", "admin", {},
             [("无Token", {"headers": {"Authorization": "", "clientid": ""}},
               {"status_code": 200, "business_code": 401, "business_message": "认证失败，无法访问系统资源"}, "P1")]),
            ("POST", "/auth/register", None, {
                "clientId": "e5cd7e4891bf95d1d19206ce24a7b32e",
                "grantType": "password", "tenantId": "000000",
                "username": "testuser", "password": "Test123456",
            }, [
                ("缺失username", {"remove_fields": ["username"]},
                 {"status_code": 200, "business_code": 500, "business_message": "用户名不能为空"}, "P1"),
                ("缺失password", {"remove_fields": ["password"]},
                 {"status_code": 200, "business_code": 500, "business_message": "用户密码不能为空"}, "P1"),
                ("用户名过短", {"body": {"username": "a"}},
                 {"status_code": 200, "business_code": 500, "business_message": "账户长度必须在2到30个字符之间"}, "P2"),
                ("密码过短", {"body": {"password": "1234"}},
                 {"status_code": 200, "business_code": 500, "business_message": "用户密码长度必须在5到30个字符之间"}, "P2"),
            ]),
            ("GET", "/auth/tenant/list", None, {}, []),
            ("GET", "/auth/binding/gitee", None, {"tenantId": "000000", "domain": "localhost"}, []),
            ("GET", "/auth/code", None, {}, []),
            ("GET", "/", None, {}, []),
            ("POST", "/auth/social/callback", None, {"source": "gitee", "socialCode": "test_code", "socialState": "test_state"},
             [("无Token", {"headers": {"Authorization": "", "clientid": ""}},
               {"status_code": 200, "business_code": 401, "business_message": "认证失败，无法访问系统资源"}, "P1")]),
            ("DELETE", "/auth/unlock/1", None, {},
             [("无Token", {"headers": {"Authorization": "", "clientid": ""}},
               {"status_code": 200, "business_code": 401, "business_message": "认证失败，无法访问系统资源"}, "P1")]),
        ],
    },

    "system": {
        "module_name": "系统管理模块",
        "routes": [
            # ── user (core) ──
            ("GET", "/system/user/list", "admin", {"pageNum": 1, "pageSize": 10},
             [("无Token", {"headers": {"Authorization": "", "clientid": ""}},
               {"status_code": 200, "business_code": 401, "business_message": "认证失败，无法访问系统资源"}, "P1")]),
            ("GET", "/system/user/getInfo", "admin", {}, []),
            ("GET", "/system/user/1", "admin", {}, []),
            ("GET", "/system/user/profile", "admin", {}, []),
            ("GET", "/system/user/deptTree", "admin", {}, []),
            ("GET", "/system/user/optionselect", "admin", {}, []),
            ("GET", "/system/user/authRole/1", "admin", {}, []),
            ("GET", "/system/user/list/dept/100", "admin", {}, []),
            ("POST", "/system/user", "admin", {
                "userName": "testuser", "nickName": "测试用户", "password": "Test123456",
                "phonenumber": "13800138000", "email": "test@test.com",
                "sex": "0", "status": "0", "deptId": 100, "remark": "测试备注",
            }, []),
            ("PUT", "/system/user", "admin", {"userId": 99999, "nickName": "修改昵称"}, []),
            ("PUT", "/system/user/profile", "admin", {"nickName": "新昵称", "phonenumber": "13800138000", "email": "admin@test.com", "sex": "0"}, []),
            ("PUT", "/system/user/profile/updatePwd", "admin", {"oldPassword": "admin123", "newPassword": "NewPwd123!"}, []),
            ("PUT", "/system/user/resetPwd", "admin", {"userId": 99999, "password": "Reset123!"}, []),
            ("PUT", "/system/user/authRole", "admin", {"userId": 99999, "roleIds": [1, 2]}, []),
            ("PUT", "/system/user/changeStatus", "admin", {"userId": 99999, "status": "0"}, []),
            ("DELETE", "/system/user/99999", "admin", {}, []),
            ("POST", "/system/user/export", "admin", {}, []),
            ("POST", "/system/user/importData", "admin", {}, []),
            ("POST", "/system/user/importTemplate", "admin", {}, []),
            # ── role ──
            ("GET", "/system/role/list", "admin", {"pageNum": 1, "pageSize": 10}, []),
            ("GET", "/system/role/1", "admin", {}, []),
            ("GET", "/system/role/optionselect", "admin", {}, []),
            ("GET", "/system/role/authUser/allocatedList", "admin", {}, []),
            ("GET", "/system/role/authUser/unallocatedList", "admin", {}, []),
            ("GET", "/system/role/deptTree/1", "admin", {}, []),
            ("POST", "/system/role", "admin", {"roleName": "test_role", "roleKey": "test_role_key", "roleSort": 1, "status": "0"}, []),
            ("PUT", "/system/role", "admin", {"roleId": 99999, "roleName": "modified_role"}, []),
            ("PUT", "/system/role/dataScope", "admin", {"roleId": 99999, "dataScope": "1", "deptIds": []}, []),
            ("PUT", "/system/role/changeStatus", "admin", {"roleId": 99999, "status": "1"}, []),
            ("DELETE", "/system/role/99999", "admin", {}, []),
            # ── menu ──
            ("GET", "/system/menu/list", "admin", {}, []),
            ("GET", "/system/menu/1", "admin", {}, []),
            ("GET", "/system/menu/getRouters", "admin", {}, []),
            ("GET", "/system/menu/treeselect", "admin", {}, []),
            ("POST", "/system/menu", "admin", {"menuName": "test_menu", "parentId": 0, "orderNum": 1, "path": "/test", "component": "test/index", "menuType": "C", "visible": "0", "status": "0"}, []),
            ("PUT", "/system/menu", "admin", {"menuId": 99999, "menuName": "modified_menu"}, []),
            ("DELETE", "/system/menu/99999", "admin", {}, []),
            # ── dept ──
            ("GET", "/system/dept/list", "admin", {}, []),
            ("GET", "/system/dept/100", "admin", {}, []),
            ("POST", "/system/dept", "admin", {"deptName": "test_dept", "parentId": 100, "orderNum": 1, "leader": "test", "status": "0"}, []),
            ("PUT", "/system/dept", "admin", {"deptId": 99999, "deptName": "modified_dept"}, []),
            ("DELETE", "/system/dept/99999", "admin", {}, []),
            # ── post ──
            ("GET", "/system/post/list", "admin", {"pageNum": 1, "pageSize": 10}, []),
            ("GET", "/system/post/1", "admin", {}, []),
            ("GET", "/system/post/optionselect", "admin", {}, []),
            ("POST", "/system/post", "admin", {"postCode": "test_post", "postName": "测试岗位", "postSort": 1, "status": "0"}, []),
            ("PUT", "/system/post", "admin", {"postId": 99999, "postName": "modified_post"}, []),
            ("DELETE", "/system/post/99999", "admin", {}, []),
            # ── config ──
            ("GET", "/system/config/list", "admin", {"pageNum": 1, "pageSize": 10}, []),
            ("GET", "/system/config/1", "admin", {}, []),
            ("POST", "/system/config", "admin", {"configName": "test_param", "configKey": "test_key", "configValue": "test_value", "configType": "Y"}, []),
            ("PUT", "/system/config", "admin", {"configId": 99999, "configValue": "new_value"}, []),
            ("DELETE", "/system/config/99999", "admin", {}, []),
            # ── notice ──
            ("GET", "/system/notice/list", "admin", {"pageNum": 1, "pageSize": 10}, []),
            ("GET", "/system/notice/1", "admin", {}, []),
            ("POST", "/system/notice", "admin", {"noticeTitle": "测试公告", "noticeType": "1", "noticeContent": "测试内容", "status": "0"}, []),
            ("PUT", "/system/notice", "admin", {"noticeId": 99999, "noticeTitle": "修改公告"}, []),
            ("DELETE", "/system/notice/99999", "admin", {}, []),
            # ── dict ──
            ("GET", "/system/dict/type/list", "admin", {"pageNum": 1, "pageSize": 10}, []),
            ("GET", "/system/dict/type/1", "admin", {}, []),
            ("POST", "/system/dict/type", "admin", {"dictName": "测试字典", "dictType": "test_dict_type", "status": "0"}, []),
            ("PUT", "/system/dict/type", "admin", {"dictId": 99999, "dictName": "修改字典"}, []),
            ("DELETE", "/system/dict/type/99999", "admin", {}, []),
            ("GET", "/system/dict/data/list", "admin", {"pageNum": 1, "pageSize": 10}, []),
            ("GET", "/system/dict/data/1", "admin", {}, []),
            ("POST", "/system/dict/data", "admin", {"dictType": "test_dict_type", "dictLabel": "测试标签", "dictValue": "test_val", "dictSort": 1, "status": "0"}, []),
            ("PUT", "/system/dict/data", "admin", {"dictCode": 99999, "dictLabel": "修改标签"}, []),
            ("DELETE", "/system/dict/data/99999", "admin", {}, []),
            # ── client ──
            ("GET", "/system/client/list", "admin", {"pageNum": 1, "pageSize": 10}, []),
            ("GET", "/system/client/1", "admin", {}, []),
            ("POST", "/system/client", "admin", {"clientName": "test_client", "clientKey": "test_client_key", "grantType": "password"}, []),
            ("PUT", "/system/client", "admin", {"id": 99999, "clientName": "modified_client"}, []),
            ("DELETE", "/system/client/99999", "admin", {}, []),
            # ── tenant ──
            ("GET", "/system/tenant/list", "admin", {"pageNum": 1, "pageSize": 10}, []),
            ("GET", "/system/tenant/1", "admin", {}, []),
            ("POST", "/system/tenant", "admin", {"tenantName": "test_tenant", "tenantType": "0", "status": "0"}, []),
            ("PUT", "/system/tenant", "admin", {"id": 99999, "tenantName": "modified_tenant"}, []),
            ("DELETE", "/system/tenant/99999", "admin", {}, []),
            ("GET", "/system/tenant/package/list", "admin", {"pageNum": 1, "pageSize": 10}, []),
            # ── social ──
            ("GET", "/system/social/list", "admin", {"pageNum": 1, "pageSize": 10}, []),
        ],
    },

    "monitor": {
        "module_name": "系统监控模块",
        "routes": [
            ("GET", "/monitor/online/list", "admin", {"pageNum": 1, "pageSize": 10},
             [("无Token", {"headers": {"Authorization": "", "clientid": ""}},
               {"status_code": 200, "business_code": 401, "business_message": "认证失败，无法访问系统资源"}, "P1")]),
            ("DELETE", "/monitor/online/invalid_token_123", "admin", {}, []),
            ("GET", "/monitor/operlog/list", "admin", {"pageNum": 1, "pageSize": 10}, []),
            ("DELETE", "/monitor/operlog/clean", "admin", {}, []),
            ("GET", "/monitor/logininfor/list", "admin", {"pageNum": 1, "pageSize": 10}, []),
            ("DELETE", "/monitor/logininfor/clean", "admin", {}, []),
            ("GET", "/monitor/logininfor/unlock/test", "admin", {}, []),
            ("GET", "/monitor/cache", "admin", {}, []),
        ],
    },

    "resource": {
        "module_name": "资源管理模块",
        "routes": [
            ("GET", "/resource/oss/list", "admin", {"pageNum": 1, "pageSize": 10},
             [("无Token", {"headers": {"Authorization": "", "clientid": ""}},
               {"status_code": 200, "business_code": 401, "business_message": "认证失败，无法访问系统资源"}, "P1")]),
            ("GET", "/resource/oss/listByIds/1", "admin", {}, []),
            ("GET", "/resource/oss/download/1", "admin", {}, []),
            ("DELETE", "/resource/oss/99999", "admin", {}, []),
            ("GET", "/resource/oss/config/list", "admin", {"pageNum": 1, "pageSize": 10}, []),
            ("GET", "/resource/oss/config/1", "admin", {}, []),
            ("GET", "/resource/sms/code", "admin", {"phonenumber": "13800138000"}, []),
            ("GET", "/resource/email/code", "admin", {"email": "admin@test.com"}, []),
        ],
    },

    "tool/gen": {
        "module_name": "代码生成模块",
        "routes": [
            ("GET", "/tool/gen/list", "admin", {"pageNum": 1, "pageSize": 10},
             [("无Token", {"headers": {"Authorization": "", "clientid": ""}},
               {"status_code": 200, "business_code": 401, "business_message": "认证失败，无法访问系统资源"}, "P1")]),
            ("GET", "/tool/gen/db/list", "admin", {"pageNum": 1, "pageSize": 10}, []),
            ("GET", "/tool/gen/1", "admin", {}, []),
            ("GET", "/tool/gen/column/1", "admin", {}, []),
            ("GET", "/tool/gen/preview/1", "admin", {}, []),
            ("GET", "/tool/gen/getDataNames", "admin", {}, []),
            ("POST", "/tool/gen/importTable", "admin", {"tables": "sys_test"}, []),
            ("DELETE", "/tool/gen/99999", "admin", {}, []),
            ("GET", "/tool/gen/synchDb/1", "admin", {}, []),
        ],
    },

    "workflow": {
        "module_name": "工作流模块",
        "routes": [
            ("GET", "/workflow/category/list", "admin", {},
             [("无Token", {"headers": {"Authorization": "", "clientid": ""}},
               {"status_code": 200, "business_code": 401, "business_message": "认证失败，无法访问系统资源"}, "P1")]),
            ("GET", "/workflow/category/categoryTree", "admin", {}, []),
            ("GET", "/workflow/category/1", "admin", {}, []),
            ("POST", "/workflow/category", "admin", {"categoryName": "test_category", "categoryCode": "test_cat", "parentId": 0}, []),
            ("GET", "/workflow/definition/list", "admin", {"pageNum": 1, "pageSize": 10}, []),
            ("GET", "/workflow/definition/unPublishList", "admin", {"pageNum": 1, "pageSize": 10}, []),
            ("GET", "/workflow/definition/1", "admin", {}, []),
            ("GET", "/workflow/definition/xmlString/1", "admin", {}, []),
            ("GET", "/workflow/instance/pageByRunning", "admin", {"pageNum": 1, "pageSize": 10},
             [("无Token", {"headers": {"Authorization": "", "clientid": ""}},
               {"status_code": 200, "business_code": 401, "business_message": "认证失败，无法访问系统资源"}, "P1")]),
            ("GET", "/workflow/instance/pageByFinish", "admin", {"pageNum": 1, "pageSize": 10}, []),
            ("GET", "/workflow/instance/pageByCurrent", "admin", {"pageNum": 1, "pageSize": 10}, []),
            ("GET", "/workflow/task/pageByTaskWait", "admin", {"pageNum": 1, "pageSize": 10}, []),
            ("GET", "/workflow/task/pageByTaskFinish", "admin", {"pageNum": 1, "pageSize": 10}, []),
            ("GET", "/workflow/task/pageByTaskCopy", "admin", {"pageNum": 1, "pageSize": 10}, []),
            ("GET", "/workflow/spel/list", "admin", {"pageNum": 1, "pageSize": 10}, []),
            ("GET", "/workflow/spel/1", "admin", {}, []),
            ("GET", "/workflow/leave/list", "admin", {"pageNum": 1, "pageSize": 10}, []),
            ("GET", "/workflow/leave/1", "admin", {}, []),
        ],
    },

    "demo": {
        "module_name": "演示模块",
        "routes": [
            ("GET", "/demo/demo/list", "admin", {"pageNum": 1, "pageSize": 10},
             [("无Token", {"headers": {"Authorization": "", "clientid": ""}},
               {"status_code": 200, "business_code": 401, "business_message": "认证失败，无法访问系统资源"}, "P1")]),
            ("GET", "/demo/demo/1", "admin", {}, []),
            ("POST", "/demo/demo", "admin", {"testKey": "test_key", "value": "测试值", "orderNum": 1}, []),
            ("DELETE", "/demo/demo/99999", "admin", {}, []),
            ("GET", "/demo/tree/list", "admin", {}, []),
            ("GET", "/demo/tree/1", "admin", {}, []),
            ("POST", "/demo/tree", "admin", {"treeName": "test_tree", "parentId": 0}, []),
            ("POST", "/demo/batch/add", "admin", {}, []),
            ("POST", "/demo/batch/addOrUpdate", "admin", {}, []),
            ("DELETE", "/demo/batch", "admin", {}, []),
        ],
    },
}


def generate_module(module_key, info):
    """Generate complete YAML data for a module."""
    data = {
        "module": module_key,
        "module_name": info["module_name"],
        "auth": AUTH_CONFIG,
        "base_url": BASE_URL,
        "global_headers": GLOBAL_HEADERS,
    }
    testcases = []
    for route in info["routes"]:
        method, path, account = route[0], route[1], route[2]
        pos_body = route[3] if len(route) > 3 else {}
        negatives = route[4] if len(route) > 4 else []

        # Also generate params from pos_body if path is a list endpoint
        params = None
        body_for_req = {}

        # Separate params from body (params are GET query, body is POST/PUT JSON)
        # The pos_body for GET routes should be treated as params
        if method == "GET" and pos_body:
            params = pos_body
            body_for_req = {}
        elif method in ("POST", "PUT", "DELETE") and pos_body:
            body_for_req = pos_body

        # Positive case
        tc = build_testcase(module_key, method, path, account, body_for_req, None)
        if params and "body" not in (tc.get("request") or {}):
            if "request" not in tc:
                tc["request"] = {}
            tc["request"]["params"] = params
        testcases.append(tc)

        # Negative cases
        for neg in negatives:
            tc = build_testcase(module_key, method, path, account, body_for_req, neg)
            # Add params from override if present
            if params or neg[1].get("params"):
                p = {**(params or {}), **(neg[1].get("params") or {})}
                if "request" not in tc:
                    tc["request"] = {}
                tc["request"]["params"] = p
            testcases.append(tc)

    data["testcases"] = testcases
    return data


# ── Main ──────────────────────────────────────────────────────

total = 0
for module_key, info in MODULES.items():
    data = generate_module(module_key, info)
    filename = f"{module_key.replace('/', '-')}-testcases.yaml"
    out_path = OUT_DIR / filename
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, Dumper=NoAliasDumper, allow_unicode=True, default_flow_style=False, sort_keys=False)
    count = len(data["testcases"])
    total += count
    print(f"  [GEN] {filename}  ({count} cases)")

print(f"\nDone: {len(MODULES)} modules, {total} testcases")
print(f"Output: {OUT_DIR}")
