# YAML 输出格式规范

## 完整结构

```yaml
module: <URL前缀>
module_name: "<中文名>"

auth:
  type: <认证类型>
  login_endpoint: <登录路径>
  token_header: <header名>
  token_prefix: "<前缀>"
  token_response_path: <token JSONPath>
  response_msg_field: <消息字段名>
  fixture_extracts:
    <变量名>: "<JSONPath>"
  accounts:
    <role>:
      <key>: <value>

base_url: <当前环境 base_url>

global_headers:
  - name: <header名>
    value: "<值>"
    required: true
    description: "<说明>"

testcases:
  - id: TC_<MODULE>_<NNN>
    title: "<METHOD> <路径>_<条件>_<预期>"
    priority: P0
    tags: [正常, 回归]
    method: POST
    path: /xxx
    description: "<描述>"
    account: <role>               # 可选
    depends_on: ["TC_<MODULE>_<NNN>"]  # 可选，依赖的前置用例 ID
    request:
      body: {}
      params: {}
      headers: {}
    expected:
      status_code: 200
      business_code: 200
      business_message: "操作成功"
      data: {}
      data_exists: []
      data_type: {}
      data_contains: ""
      data_length: 0
      data_db:
        table: ""
        where: {}
        expected: {}
    extract:
      <变量名>: "$.data.<JSON键名>"
```

## 断言类型

| 字段 | 层 | 说明 |
|------|---|------|
| `status_code` | 协议层 | HTTP 状态码，必填 |
| `business_code` | 业务层 | 业务状态码，必填 |
| `business_message` | 业务层 | 业务消息，必填 |
| `business_message_mode` | 业务层 | 消息匹配模式：`exact`（默认，完全匹配）/ `contains`（包含匹配，复合拼接消息时使用）/ `skip`（不校验消息） |
| `data` | 数据层 | 精确匹配 data 中字段值 |
| `data_exists` | 数据层 | 字段在 data 中存在，值为 `list[str]` |
| `data_type` | 数据层 | 字段类型：str/int/float/bool/list/dict |
| `data_contains` | 数据层 | 响应体包含此字符串 |
| `data_length` | 数据层 | 数组长度 |
| `data_db` | 数据层 | 数据库校验（table/where/expected） |

## 变量

YAML 中仅以下 `${}` 变量合法，其余值应直接写入具体内容（从配置或源码分析结果中获取）。

| 变量 | 来源 | 用途 |
|------|------|------|
| `${token}` | 登录 fixture | global_headers 认证头 |
| `${<fixture_extracts key>}` | 登录响应中提取 | global_headers 跨字段校验值 |
| `${<extract key>}` | 前置用例提取 | 后续用例的 path 参数、请求体字段；用例通过 `depends_on` 声明依赖关系 |
| `${timestamp}` | runner_utils | 唯一标识后缀 |

**禁止使用 `${account.xxx}` 引用账号字段。** 账号的 username、password、认证参数等字段在生成 YAML 时已从 `auth.accounts` 中确定，应直接写入具体值。

**禁止使用 `{var}` 格式（不带 `$` 前缀）。** 运行时仅识别 `${var}` 格式的变量引用。异常测试中使用的无效参数值应直接写为具体值（如 `-1`、`""`、`"abc"`），不要使用 `{placeholder}` 占位符——它们会以字面字符串传入 API。
