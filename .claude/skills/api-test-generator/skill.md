---
name: api-test-generator
description: "根据测试用例YAML和测试计划自动生成pytest API接口测试脚本。使用场景：用户要求生成API测试、生成接口测试脚本、生成pytest测试代码、根据测试用例生成自动化测试。触发短语：生成API测试、generate api test、生成接口测试、生成pytest脚本、根据用例生成测试代码、create pytest api tests"
---

# API 测试脚本生成器

根据 `tests/baseline/_workflow/02-analysis-plan/` 下的测试用例 YAML 文件和测试计划，生成可直接运行的 pytest API 接口测试脚本。

## 核心原则

**数据和脚本分离**：YAML 测试用例文件是唯一的数据来源。生成的 pytest 脚本只包含执行逻辑，运行时从对应的 YAML 文件读取用例数据并执行，不硬编码任何测试数据。

**测试规范遵循**：生成时遵守 `.claude/rules/testPoint-interface.md` 中定义的接口测试要点和断言规范。

## 输入文件

### 1. config.yaml（项目根目录）

提取以下配置：

- `source.backend[].path` — 后端工程路径（用于分析源码）
- `source.backend[].name` — 服务名称
- `environments.<env>.backend[].url` — 后端服务地址（base_url）
- `environments.<env>.frontend[].accounts` — 测试账号信息（用户名、密码、角色）

> 以上字段均为配置示例，实际生成时从当前项目的 config.yaml 动态读取。

### 2. 测试用例 YAML（testcases 目录）

默认路径：`tests/baseline/_workflow/02-analysis-plan/testcases/*-testcases.yaml`

每个 YAML 文件包含：
- `module` / `module_name` — 模块标识
- `testcases[]` — 用例列表，每条含 id、title、request、expected_response、assertions、tags 等字段

### 3. API 定义（apis.json）

默认路径：`tests/baseline/_workflow/02-analysis-plan/apis.json`

包含每个 API 的 `request_body` 和 `response_fields` 定义。

### 4. 测试生成计划（generation-plan.md）

默认路径：`tests/baseline/_workflow/02-analysis-plan/generation-plan.md`

包含测试范围、优先级排序、测试数据变量说明。

## 输出目录

```
tests/baseline/generated/api-test/
```

首次生成时自动创建。

## 输出文件结构

```
tests/baseline/generated/api-test/
├── conftest.py              # pytest 配置和共享 fixture
├── test_<module1>.py        # 按模块生成的测试文件
├── test_<module2>.py        # 一个 YAML 对应一个 test_*.py
├── api_utils.py             # API 请求工具类（session管理、认证、断言辅助）
└── pytest.ini               # pytest 配置文件
```

## 技术栈

- **测试框架**：pytest
- **HTTP 客户端**：requests
- **数据加载**：PyYAML（运行时从 YAML 文件读取用例）
- **认证**：通过 fixture 自动获取并管理 Token

## 生成步骤

### Step 1: 读取配置

从项目根目录 `config.yaml` 读取：

```yaml
# 提取后端服务地址
base_url = environments[env].backend[].url

# 提取测试账号
accounts = environments[env].frontend[].accounts
# → admin (超级管理员), visitor (普通用户) 等
```

### Step 2: 扫描测试用例 YAML

扫描 `tests/baseline/_workflow/02-analysis-plan/testcases/` 目录下所有 `*-testcases.yaml` 文件。

每个 YAML 文件对应一个模块，文件名如 `ums-testcases.yaml` → 生成 `test_ums.py`。

### Step 3: 解析用例结构

从每条 YAML 用例中提取：

| YAML 字段 | 用途 |
|-----------|------|
| `id` | 用例唯一标识，生成测试函数名 |
| `title` | 测试函数 docstring |
| `priority` | 用于 pytest.mark 标记（P0/P1/P2） |
| `scenario` | 测试场景描述 |
| `preconditions` | 前置条件说明 |
| `request` (method, path, headers, body, params) | 构造 HTTP 请求 |
| `expected_response` | 预期结果（http_status, business_code, message, data） |
| `assertions[]` | 断言表达式列表 |
| `tags[]` | 用于 pytest.mark 标记 |

### Step 4: 生成 conftest.py

使用 `template/conftest.py.j2` 模板，注入以下 fixture：

- `base_url` — 后端服务地址（来自 config.yaml）
- `api_session` — requests.Session，自动管理认证头
- `admin_token` — 管理员 Token（自动登录获取）
- `visitor_token` — 普通用户 Token（自动登录获取）
- `test_data_loader` — 从 YAML 文件加载测试用例数据的工具函数
- `resolve_variables` — 解析用例中 `${...}` 变量引用的工具函数

认证流程：
1. 用 config.yaml 中的测试账号调用登录接口
2. 提取响应中的 token 字段
3. 设置到 session 的 Authorization 头

### Step 5: 生成 test_*.py（按模块）

使用 `template/test_module.py.j2` 模板。

**数据加载方式**：测试函数通过 `test_data_loader` fixture 从对应的 YAML 文件读取用例，不硬编码任何数据。

```python
# 运行时从 YAML 读取，不硬编码
@pytest.mark.parametrize("case", load_testcases("ums-testcases.yaml", tags=["smoke"]))
def test_case(api_session, case):
    ...
```

**函数命名**：`test_{用例id转小写}()` → 如 `test_tc_ums_admin_login_001()`

**参数化**：使用 `pytest.mark.parametrize` 将 YAML 中的每条用例注入为独立的测试参数。

**断言执行**：循环执行 YAML 中 `assertions` 列表的每一条断言，支持：

| 断言类型 | 实现 |
|----------|------|
| `assert_equal` | `assert left == right` |
| `assert_not_equal` | `assert left != right` |
| `assert_exists` | `assert key_path in response` |
| `assert_not_empty` | `assert value` (truthy check) |
| `assert_contains` | `assert needle in haystack` |
| `assert_in` | `assert value in list` |
| `assert_is_type` | `assert isinstance(value, expected_type)` |

**变量解析**：测试执行前，将 `${timestamp}`、`${admin_token}`、`${test_user_id}` 等变量替换为实际值。

**标签映射**：
| YAML 标签 | pytest marker |
|-----------|---------------|
| smoke | @pytest.mark.smoke |
| regression | @pytest.mark.regression |
| security | @pytest.mark.security |

### Step 6: 生成 pytest.ini

配置 pytest 运行参数：

```ini
[pytest]
markers =
    smoke: 冒烟测试
    regression: 回归测试
    security: 安全测试
    P0: 核心路径
    P1: 主要功能
    P2: 非关键细节
```

### Step 7: 生成 api_utils.py

包含以下工具类和函数：

- `ApiClient` — requests.Session 封装，支持 base_url、认证头、超时
- `load_testcases(yaml_file)` — 从 YAML 文件加载用例列表
- `resolve_variables(data, context)` — 替换 `${var}` 变量
- `execute_assertion(assertion, response)` — 动态执行断言表达式
- `get_token(base_url, username, password)` — 获取认证 Token

### Step 8: 写入文件

确保 `tests/baseline/generated/api-test/` 目录存在，写入所有生成的文件。

## 断言规范

严格遵循 `.claude/rules/testPoint-interface.md`，确保断言分层完整：

1. **协议层断言** — HTTP 状态码（`assert response.status_code == expected`）
2. **业务层断言** — 业务状态码（`assert response.json()['code'] == expected`）
3. **数据层断言** — message 字段 + data 字段具体值/类型/存在性

断言失败时必须提供清晰的错误消息，包含实际值和预期值。

## 模板使用

skill 同级目录 `template/` 下包含 Jinja2 模板：

- `conftest.py.j2` — pytest conftest 模板
- `test_module.py.j2` — 测试模块模板

生成时读取模板，用项目实际配置渲染（不要使用模板中的示例值）。

## 测试数据原则

遵循 `.claude/rules/testCase-standards.md`：

- 每个用例只测一个功能点
- 用例原子化、无执行顺序依赖
- 测试数据与生产一致但脱敏
- 优先使用 YAML 中已定义的测试数据
- `${timestamp}` 等运行时变量在测试执行时动态替换

## 注意事项

- 生成的脚本不要硬编码任何项目特定的 URL、账号、密码
- 所有配置从 config.yaml 读取，所有用例数据从 YAML 读取
- 测试用例的 YAML 文件路径使用相对路径，基于项目根目录
- Token 过期时自动重新登录获取
- 请求超时默认为 30 秒
- 按优先级生成：先 P0（核心路径），然后 P1/P2

## 使用示例

```
用户：生成API测试

→ 读取 config.yaml → 获取后端地址 http://localhost:8080
→ 扫描 testcases/ 目录 → 找到 ums-testcases.yaml (67 条用例)
→ 生成 conftest.py、api_utils.py、test_ums.py、pytest.ini
→ 输出到 tests/baseline/generated/api-test/

运行测试：
  pytest tests/baseline/generated/api-test/ -v          # 全部
  pytest tests/baseline/generated/api-test/ -m smoke     # 冒烟测试
  pytest tests/baseline/generated/api-test/ -m P0        # 核心路径
```
