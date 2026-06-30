# 用例设计规则

## 正向用例

每个 API 至少 1 条：
- **完整参数**：所有必填+可选字段填有效值 → 断言 status_code + business_code + business_message + 关键返回字段存在
- **仅必填参数**（有可选字段时）：验证默认值
- 数据使用仿真值（符合真实格式的用户名/手机号/邮箱）

## 反向用例

根据 API 特征选择，每个 API 至少覆盖适用的场景：

| 场景 | 适用条件 | 每场景用例数 | 预期值来源 |
|------|---------|------------|-----------|
| 缺少必填参数 | DTO 有 @NotNull/@NotBlank/@NotEmpty | 每个必填字段 1 条 | `business_code` 查 error_codes.validation_fail |
| 参数格式错误 | 有 @Email/@Pattern 等格式校验 | 每种校验 1 条 | 同上 |
| 参数越界 | 有 @Size/@Length/@Min/@Max | 每种约束 1 条 | 同上 |
| 无认证 Token | 接口有认证要求 | 1 条 | 优先使用路由的 `auth_probe_code` 探测值；未探测时查 error_codes.auth_fail |
| 权限不足 | 有 @PreAuthorize 或角色要求 | 1 条 | 查 error_codes.permission_fail |
| 资源不存在 | GET/DELETE/PUT 操作已有资源 | 1 条（使用 `-1` 或 `"99999"` 等无效 ID） | 查 error_codes.business_fail |
| 外部依赖不可用 | 接口依赖 SMS/Email/OSS 等外部服务且 `environment.capabilities` 标记 `false` | 1 条 | `business_code: 500`，`business_message_mode: skip` |

**⛔ 必填字段保留规则（"缺少必填参数"反向用例）**：

生成"缺少必填参数"类型的反向用例时，必须遵守以下规则，避免校验顺序覆盖：

- **仅被测字段缺失或设置无效值**——其他必填字段必须保留有效值
- 有效值来源（按优先级）：
  1. `dto_index` 中该字段的示例值或默认值
  2. 字段类型推断值（string → 非空字符串，int → 正数）
  3. 若字段名与 `auth.accounts` 中某 role 的键名一致 → 取该 role 对应的值

若不遵守此规则，API 先校验到其他缺失字段时，返回的错误消息会掩盖被测字段的校验行为（如预期 "用户名不能为空" 但实际返回 "租户编号不能为空"）。

**注意**：资源不存在场景的无效参数值直接写具体字面量（如 `-1`、`"99999"`），**不要使用 `{placeholder}` 占位符**。

## 优先级

| 优先级 | 分配条件 |
|--------|---------|
| P0 | 核心正向流程、登录认证 |
| P1 | 必填参数缺失、认证/权限验证、资源不存在 |
| P2 | 边界值、格式校验、可选字段 |

## 标签

每条用例至少一个：
`正常`（正向）、`异常`（反向）、`回归`、`冒烟`（P0 核心路径）、`兼容性`、`用户体验`

## 标题格式

- 单接口：`{METHOD} {路径}_{测试条件}_{预期结果}`
- 示例：`POST /system/user_缺少username_返回参数校验错误`

## 断言三层规范

每条用例必须包含：
1. **协议层**：`status_code`
2. **业务层**：`business_code` + `business_message`
3. **数据层**（按需）：`data_exists`（正向）、`data`（精确匹配）

禁止仅断言 HTTP 状态码。

### 业务消息匹配模式

通过 `business_message_mode` 控制断言时的消息匹配方式：

| 模式 | 适用场景 | 示例 |
|------|---------|------|
| `exact`（默认） | 成功消息、单一校验失败 | 期望"操作成功"，实际"操作成功" |
| `contains` | 复合校验消息拼接 | 期望包含"用户名不能为空"，实际"用户名不能为空, 认证客户端id不能为空" |
| `skip` | 消息内容不确定 | 动态异常消息 |

**选择规则**：
- 正向成功用例 → `exact`
- 单一字段缺失的校验失败 → `exact`
- 多字段同时缺失（消息拼接）→ `contains`（查 shared-context 中 `validation_message_mode` 是否为 `concatenated`）
- 不确定消息内容的业务异常 → `skip`

## 变量引用规则

生成 YAML 时，区分两类值：

| 类型 | 判断标准 | 写入方式 | 示例 |
|------|---------|---------|------|
| 动态值 | 生成时未知，运行时才能确定 | `${变量名}` | `${token}`、`${timestamp}`、fixture_extracts 变量、extract 变量 |
| 静态值 | 生成时已知，直接从配置可读取 | 直接写入具体值 | 账号的 username/password 等字段、固定参数值 |

### ${} 适用场景（仅以下四类）

1. **`${token}`** — 登录后获取的认证令牌，写入 `global_headers`
2. **`${<fixture_extracts 变量>}`** — 登录响应中提取的动态值（如跨字段校验的额外 header 值），写入 `global_headers`
3. **`${<extract 变量>}`** — 前置用例提取的资源 ID 等，写入后续用例的 path/body
4. **`${timestamp}`** — 运行时间戳，写入需要唯一值的字段

### 直接内联场景

- **请求体/参数中引用账号字段**：从 `auth.accounts.<role>` 取具体值直接写入，不使用 `${account.xxx}` 引用
- **固定参数值**：pageNum、pageSize 等直接写数字或字符串
- **非动态的 header 值**：常量值直接写，不过变量引用
- **异常测试的无效参数值**：直接写具体字面量（如 `-1`、`""`、`"abc"`），不使用 `{placeholder}` 占位符

### ⛔ 格式禁令

**禁止使用 `{var}` 格式（不带 `$` 前缀）。** 运行时仅识别 `${var}` 格式的变量引用。`{var}` 格式不会被解析，会以字面字符串传入 API（如参数值变为 `{ossIds}` 而非预期值）。

### 理由

账号配置（username、password、认证参数等）在生成 YAML 时已是已知常量，多做一层 `${account.xxx}` 引用只会增加运行时解析的复杂度和 YAML 的阅读成本。只有运行时才能确定的值才需要 `${}`。

## 覆盖率要求

- 每个 API 至少 1 条用例
- 每个必填字段至少 1 条反向用例
- 核心业务逻辑覆盖率 ≥ 90%

## 场景链与用例依赖

对于需要多个接口协作的业务流程（如 POST 创建 → PUT 修改 → DELETE 删除），使用以下机制实现用例间的数据传递：

### extract 链

1. POST 创建接口若返回 `R<XxxVo>`（data 含 ID），在用例中定义 `extract` 提取 ID
2. PUT 修改和 DELETE 删除通过 `depends_on` 声明对前置用例的依赖
3. 参数中使用 `${变量名}` 引用提取的 ID

```yaml
- id: TC_WF_008
  method: POST
  path: /workflow/category
  extract:
    categoryId: "$.data.categoryId"

- id: TC_WF_010
  method: PUT
  path: /workflow/category
  depends_on: ["TC_WF_008"]
  request:
    body:
      categoryId: "${categoryId}"
      categoryName: "分类_${timestamp}"
```

### 约束

- POST 返回 `R<Void>` 或 `void` 时，不生成 extract，跳过依赖此 POST 的 PUT/DELETE 正向成功用例
- 资源不存在等反向用例使用显式无效值（如 `-1`、`"99999"`），不依赖前置用例
- `depends_on` 仅用于同一模块内的用例依赖，跨模块依赖由 fixture_extracts 和 global_headers 处理
