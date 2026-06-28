# 值溯源

从源码追踪接口返回的实际 `business_code`、`business_message` 和 HTTP `status_code`。

## 正向响应值

### 追踪链

```
Controller return 语句
  → 静态工厂方法（R.ok() / R.success() / Result.success()）
  → 构造器或工厂方法内部
  → code/message 的常量或硬编码字符串
```

### 追踪步骤（批量读取）

1. 从 A2 补全结果中识别出使用的响应包装类（R.java、TableDataInfo.java 等）
2. **用 `codegraph_explore` 一次性读取** R 类、TableDataInfo 类、全局异常处理器（一次调用传全部类名）：
   ```
   codegraph_explore query="R TableDataInfo GlobalExceptionHandler"
   ```
3. 从批量读取的源码中提取：`R.ok()` 的 code/message、`R.fail()` 的 code/message、`TableDataInfo` 的 code/message
4. 提取 code 赋值来源（常量 `SUCCESS`、枚举值）
5. 提取 message 赋值来源（硬编码字符串）

**禁止**逐个 `codegraph_node` 调用——一次 explore 覆盖全部响应包装类。

### 常见模式与追踪方式

| Controller 返回 | 追踪方式 |
|----------------|---------|
| `return R.ok()` | 进入 `ok()` → 找到无参版本调用 `ok(data)` 或直接调构造器 |
| `return R.ok(data)` | 进入重载方法 → 读取 code/message 参数 |
| `return R.fail(code, msg)` | 直接读取调用参数 |
| `return new R<>(code, msg, data)` | 直接读取构造器参数 |
| `return Result.success(data)` | 同上，进入 `success()` 方法 |

## 反向响应值

反向响应的 code/message 来源取决于触发场景：

| 场景 | code/message 来源 |
|------|------------------|
| 参数校验失败 | DTO 校验注解 message → 全局异常处理器（详见 error-tracing.md） |
| 认证失败 | 安全拦截器的拒绝响应 → R.fail(code, msg) |
| 权限不足 | 权限拦截器的拒绝响应 |
| 业务异常 | Service 中 throw 的异常 → 全局异常处理器 |
| 资源不存在 | Service 中 throw 的异常 → 全局异常处理器 |

## status_code

1. 检查异常处理器方法上的 `@ResponseStatus(HttpStatus.XXX)`
2. 若异常处理器未设置 → 默认 200
3. 检查 `response.setStatus()` 调用

**禁止假设任何 HTTP 状态码。** 即使认证失败，HTTP 状态码也可能是 200（取决于项目设计）。
