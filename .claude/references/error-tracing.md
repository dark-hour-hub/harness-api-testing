# 错误路径追踪

为反向用例确定准确的 `business_code`、`business_message`、`status_code`。

## 异常抛出链

```
请求进入 → Jackson 反序列化 → @Validated 校验
  → 校验失败抛异常（携带字段名 + 注解 message）
  → 全局异常处理器 @ExceptionHandler 捕获
  → 格式化最终响应（code + message + HTTP status）
```

## 追踪步骤

### 1. 定位 DTO 校验注解 message

**优先使用 shared-context.yaml 的 `dto_index`**——Phase A3b 已预索引所有 DTO 的校验注解 message。仅当 dto_index 中未覆盖时，才用 `codegraph_explore` 批量读取缺失的 DTO。

从 dto_index 或批量读取的结果中找目标字段的校验注解：
- 有 `message = "xxx"` → 记录该值，替换占位符 `{min}`/`{max}`/`{value}`
- 无 → 记录默认模板（见附录）

**重要**：此时得到的是注解中的原始 message 模板（如 `{i18n.key}` 格式），**不是最终返回给客户端的文本**。需要执行步骤 1b 的 i18n 解析。

### 1b. i18n 消息解析（必做）

从步骤 1 获得的 message 模板可能包含 i18n 占位符，需要查 properties 文件解析为最终文本。

**判断是否需要解析**：
- 值为 `{xxx}` 格式（花括号包裹）→ 提取 key，执行 i18n 解析
- 值为普通字符串 → 即为最终 `business_message`，跳过此步骤
- 值为 null/空 → 使用 JSR-380 默认模板（见附录），无需解析

**解析流程**：
1. 提取 key（去掉 `{` `}` 包裹）
2. 搜索项目 i18n properties 文件（`messages*.properties`、`ValidationMessages.properties`）
3. 用查到的翻译值作为 `business_message`
4. 若所有 properties 文件中均未找到 → 保留原始 key，加 TODO 注释标记人工验证

详细解析规则见 `references/i18n-resolution.md`。

### 1c. 业务异常消息解析

对于 Service 层抛出的业务异常（非校验注解触发），同样需要 i18n 解析：

- 追踪 `throw` 语句 → 若调用了项目 i18n 工具方法（如 `MessageUtils.message(key)` 或类似封装）→ 提取 key → 按步骤 1b 解析
- 若 `throw` 语句传入的是硬编码字符串 → 直接作为 `business_message`
- 若异常构造器内部对 key 做了格式化（如带 `String.format` 参数）→ 查 properties 获取模板后按格式填入预期值

### 2. 定位全局异常处理器

用 `codegraph_search` 搜索 `@ControllerAdvice` / `@RestControllerAdvice`（1-2 个类），然后**用 `codegraph_explore` 一次性读取**异常处理器 + 所有相关异常类：

```
codegraph_explore query="GlobalExceptionHandler MethodArgumentNotValidException AuthException BusinessException"
```

在批量读取的源码中找对应异常处理器：
- `MethodArgumentNotValidException` → `@RequestBody` 校验失败
- `ConstraintViolationException` → `@RequestParam`/`@PathVariable` 校验失败
- `BindException` → `@ModelAttribute` 校验失败

### 3. 识别格式化模式

| 模式 | 代码特征 | 最终 message |
|------|---------|-------------|
| A. 原样透传 | `fe.getDefaultMessage()` | 注解 message 原值 |
| B. 字段名拼接 | `fe.getField() + fe.getDefaultMessage()` | `"字段名" + 注解 message` |
| C. 固定兜底 | 硬编码字符串，不读异常 | 固定字符串 |
| D. i18n 解析 | `messageSource.getMessage(...)` | i18n 解析结果 |

### 4. 确定 business_code

从异常处理器的 `R.fail(code, msg)` 调用中提取 code 参数。

### 5. 确定 status_code

- 异常处理器方法有 `@ResponseStatus(HttpStatus.XXX)` → 取该值
- 无 → 默认 200

## 附录：JSR-380 注解默认 message

| 注解 | 默认 message（英文） |
|------|---------------------|
| `@NotNull` | `must not be null` |
| `@NotBlank` | `must not be blank` |
| `@NotEmpty` | `must not be empty` |
| `@Size(min, max)` | `size must be between {min} and {max}` |
| `@Length(min, max)` | `length must be between {min} and {max}` |
| `@Email` | `must be a well-formed email address` |
| `@Pattern(regexp)` | `must match "{regexp}"` |
| `@Min(value)` | `must be greater than or equal to {value}` |
| `@Max(value)` | `must be less than or equal to {value}` |

若项目有 `ValidationMessages.properties` / `messages.properties`，使用 i18n 翻译值。

## 禁止

- 禁止跳过 DTO 注解直接取全局处理器的兜底值
- 禁止假设 status_code = 400
- 禁止凭注解名称臆造 message
- 禁止一条反向用例同时缺失多个必填字段
