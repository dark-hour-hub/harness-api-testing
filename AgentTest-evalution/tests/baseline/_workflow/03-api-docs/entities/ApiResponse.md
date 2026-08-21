# ApiResponse — 通用响应包装（泛型）

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `ApiResponse` |
| **全限定名** | `com.czbank.aicgs.evaluation.common.api.ApiResponse` |
| **类型** | 通用响应包装（泛型 `ApiResponse<T>`，请求体/响应体通用） |
| **所属模块** | 通用（common） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认）；构造时校验 `traceId` 非空（代码层约束，成功路径由 `success()` 生成） |
| **说明** | 全项目统一响应包装。成功时 `code="200"`、`message="success"`；`data` 为泛型负载（可为 `null` 或 `Void`）。`code` 为 String 类型 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| code | `code` | String | ✅ | — | `"200"` | 业务码（String 类型）；成功固定 `"200"`，失败为错误码枚举名（如 `COMMON_404_RESOURCE`） | `"200"` |
| message | `message` | String | ✅ | — | `"success"` | 提示信息；成功固定 `"success"` | `"success"` |
| data | `data` | T | 否 | — | — | 业务数据负载（泛型 `T`；`ApiResponse<Void>` 时为 null；分页时为 `PageResult<T>`） | 见示例 |
| traceId | `traceId` | String | ✅ | 非空（构造时校验） | — | 链路追踪 ID（TraceIdFilter 透传/回写响应头；缺失时服务端生成 32 位十六进制 UUID） | `"3f2a9c1e0d4b5a7f8e9d0c1b2a3f4e5d"` |

**字段备注**（无则删除）:
- `data` 类型由泛型参数 `T` 决定：单对象为实体 VO；分页为 `PageResult<T>`；`ApiResponse<Void>` 时 `data=null`
- 成功码 `200` 为字符串而非数字，测试断言时需注意类型

---

## JSON 示例

```json
{
  "code": "200",
  "message": "success",
  "data": {
    "id": 1,
    "agentCode": "AGENT_001"
  },
  "traceId": "3f2a9c1e0d4b5a7f8e9d0c1b2a3f4e5d"
}
```

---

*基于 `com.czbank.aicgs.evaluation.common.api.ApiResponse` 源码生成 · 2026-08-19*