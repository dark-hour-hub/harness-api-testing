---
name: pytest-generator
description: 从 YAML 测试用例定义生成可独立执行的 pytest 脚本。数据和脚本分离——用户可直接修改 YAML 后重新执行单个用例。触发方式：/pytest-generator、生成pytest脚本、从YAML生成测试脚本、generate pytest tests from yaml、生成接口测试pytest脚本。每次用户提到从 YAML 生成可执行 pytest、数据脚本分离、或者每用例一方法时使用此 skill。
---

# Pytest 脚本生成器

从 `tests/baseline/_workflow/03-testcases/*.yaml` 读取测试用例定义，生成 `tests/baseline/generated/api-test/` 下的可执行 pytest 脚本。

## 设计原则

- **数据与脚本分离**：测试数据（YAML）与测试逻辑（pytest）独立。修改 YAML 后无需重新生成，直接执行。
- **每用例一方法**：每个 YAML 测试用例生成一个 `def test_xxx()` 函数，支持 `pytest -k` 单独执行。
- **无硬编码**：生成脚本和 skill 本身不包含任何特定 YAML 的内容。所有业务数据来自 YAML。
- **变量运行时解析**：`${var}` 引用在测试运行时动态解析，不在生成时固化。

## 执行流程

```bash
python .claude/skills/pytest-generator/scripts/generate_pytest.py \
  --input tests/baseline/_workflow/03-testcases \
  --output tests/baseline/generated/api-test
```

脚本参数：
- `--input`：YAML 测试用例目录（默认 `tests/baseline/_workflow/03-testcases`）
- `--output`：生成 pytest 脚本的输出目录（默认 `tests/baseline/generated/api-test`）

## 生成文件

| 文件 | 说明 |
|------|------|
| `api_utils.py` | JSONPath 提取、变量解析、HTTP 请求构建、响应断言——与 pytest 无关的纯工具函数 |
| `conftest.py` | pytest fixtures：认证登录、token 管理、跨用例变量共享、测试执行上下文 |
| `test_{module}.py` | 每个 YAML 模块生成一个测试文件，每个用例一个 `def test_xxx()` 方法 |
| `pytest.ini` | pytest 配置：markers 定义 |

## 变量体系

### `${变量名}` — 运行时解析
- `${token}` — 当前登录会话的认证 token
- `${clientId}` — 从登录响应中提取的客户端 ID
- `${timestamp}` — 执行时生成的毫秒时间戳，用于构造唯一数据（如用户名）

### `$.data.field` — JSONPath 提取
- 在 `extract` 和 `fixture_extracts` 中用于从 HTTP 响应中提取值
- 提取的变量存入模块级变量池，供同一模块内的后续用例通过 `${变量名}` 引用

## 生成的测试函数结构

每个测试函数遵循统一模式：

```python
def test_tc_auth_001(api_case):
    """TC_AUTH_001: POST /auth/login 完整有效参数 登录成功"""
    api_case.run("TC_AUTH_001")
```

`api_case` fixture 自动完成：查找用例 → 解析变量 → 认证登录 → 发送请求 → 断言 → 提取变量。

## 断言分层

每个用例自动执行三层断言（符合接口案例编写标准）：

1. **协议层**：HTTP 状态码（`expected.status_code`）
2. **业务层**：业务状态码（`expected.business_code`）和业务消息（`expected.business_message`）
3. **数据层**：响应数据字段存在性（`expected.data_exists`）

## 认证处理

- 默认使用 `admin` 账号，用例可通过 `account: visitor` 切换
- 认证 token 按账号缓存，同模块内复用，避免重复登录
- 无认证测试：在 `request.headers` 中将 `Authorization` 设为空字符串即可