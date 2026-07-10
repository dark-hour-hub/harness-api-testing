---
name: yaml-to-pytest
description: 从 04-testcases/ 下的 YAML 测试用例文件生成 pytest 脚本到 generated/api-test/。触发：/yaml-to-pytest、YAML转pytest、生成pytest脚本、生成接口测试脚本、yaml to pytest、generate pytest tests。读取所有 YAML 测试用例，每个 YAML 生成一个 test_{module}.py 脚本，同时生成 conftest.py。
---

# YAML → Pytest 脚本生成器

从 `tests/baseline/_workflow/04-testcases/` 读取 YAML 测试用例定义，生成可执行的 pytest 脚本到 `tests/baseline/generated/api-test/`。

## 设计原则

- **数据驱动**：所有测试数据来自 YAML，生成的脚本不包含硬编码值。修改 YAML 后无需重新生成脚本即可生效
- **每用例一方法**：每个 YAML 测试用例映射为一个 pytest 测试函数
- **依赖感知**：支持 `depends_on` 声明用例执行顺序，支持 `${TC_XXX.extracts.xxx}` 跨用例变量传递
- **独立可执行**：每个测试方法可以单独运行（`pytest test_auth.py::test_TC_AUTH_001`）
- **路径安全**：YAML 文件路径使用 `Path(__file__).resolve()` 计算，无论 pytest 从何处执行都不会出错

## 输入

| 来源 | 路径 | 用途 |
|------|------|------|
| YAML 用例 | `tests/baseline/_workflow/04-testcases/*.yaml` | 测试用例定义 |
| 字段规范 | `.claude/skills/api-doc-to-testcases/references/yaml-schema.md` | YAML 字段含义 |
| 变量引用规范 | `.claude/skills/api-doc-to-testcases/references/variable-reference.md` | `${...}` 解析规则 |

## 输出

```
tests/baseline/generated/api-test/
├── conftest.py        # 公共 fixtures + 工具函数
├── test_auth.py       # 认证模块
├── test_resource.py   # 资源管理
├── test_system_dept.py # 部门管理
└── ...
```

## 执行

```bash
python .claude/skills/yaml-to-pytest/scripts/generate_pytest.py \
  --yaml-dir tests/baseline/_workflow/04-testcases \
  --output-dir tests/baseline/generated/api-test
```

无参数时使用上述默认路径。

## 生成内容说明

### conftest.py

提供所有测试文件共享的基础设施：

- **ModuleContext**：模块级共享上下文，存储用例 extracts 结果，支持 `${TC_XXX.extracts.xxx}` 跨用例引用
- **变量解析函数**：`resolve_vars()` 递归解析 `${auth.xxx}`、`${global_variables.xxx}`、`${TC_XXX.extracts.xxx}`，遵循 extracts 跳过规则和精确层级路径规则
- **JSONPath 提取**：`jsonpath_extract()` 从响应 JSON 中按 `$.data.xxx` 路径提取值
- **请求头构建**：`build_headers()` 合并 public_headers + auth_headers（仅当 `auth.required=true`）+ 用例特有 headers
- **认证 fixture** `auth_values`：session 级自动登录
  - 如果模块包含登录接口的测试用例（path 匹配 `login_endpoint`），跳过自动登录，由测试用例自身完成登录并通过 extracts + `__auth__` 传递 token
  - 其他模块：自动 POST 登录获取 token，缓存到 session 级
- **module_context fixture**：module 级共享上下文
- **request_helper fixture**：封装请求执行 + 断言全流程

### test_{module}.py

- 模块级加载对应 YAML 文件（路径通过 `Path(__file__).resolve().parents[2]` 定位）
- 覆盖 `module_data` fixture 返回本模块的 YAML 数据
- 每个测试用例 → 一个 `test_{case_id}` 函数
- 每个函数：获取用例数据 → 解析变量 → 构建请求 → 发送 → 断言 → 存储 extracts
- 使用 `@pytest.mark.order(N)` 确保依赖用例先执行

## 变量引用解析

严格遵循 [variable-reference.md](..\api-doc-to-testcases\references\variable-reference.md)：

| 引用格式 | 解析来源 |
|---------|---------|
| `${auth.token}` | auth_setup.extracts（跳过 extracts 层级） |
| `${auth.token_prefix}` | auth_setup 顶层字段 |
| `${auth.params.admin.client_id}` | auth_setup.params |
| `${auth.accounts.admin.username}` | auth_setup.accounts |
| `${global_variables.default_page_size}` | global_variables |
| `${TC_AUTH_001.extracts.login_token}` | module_context 中 TC_AUTH_001 的 extracts |

## 跳过规则

- `request.headers` 含 `Content-Type: multipart/form-data` 的用例自动跳过（文件上传暂不支持）
- 跳过的用例生成时标记为 `@pytest.mark.skip`

## 禁止项

- 禁止在生成的脚本中硬编码测试数据
- 禁止在 conftest.py 中硬编码任何模块特定的路径或值
- 禁止生成不存在的 YAML 字段引用
