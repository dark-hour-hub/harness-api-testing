# AgentCallResponse — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `AgentCallResponse` |
| **全限定名** | `com.czbank.aicgs.evaluation.report.adapter.in.web.AgentCallResponse` |
| **类型** | 响应体 VO |
| **所属模块** | 评测任务模块（task / report） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | 持久化的 Agent 调用记录（已脱敏），`GET /api/evaluation-tasks/{id}/calls` 分页返回 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| callId | `callId` | long | — | — | — | 调用 ID | `1` |
| taskId | `taskId` | long | — | — | — | 任务 ID | `1` |
| taskCaseId | `taskCaseId` | long | — | — | — | 任务用例关联 ID | `1` |
| sequenceNo | `sequenceNo` | int | — | — | — | 调用序号 | `1` |
| httpStatus | `httpStatus` | Integer | — | — | — | HTTP 状态码（可空） | `200` |
| latencyMs | `latencyMs` | long | — | — | — | 延迟毫秒 | `523` |
| success | `success` | boolean | — | — | — | 调用是否成功 | `true` |
| errorType | `errorType` | String | — | — | — | 错误类型（如 `TIMEOUT`/`CONNECTION_FAILURE`/`HTTP_NON_2XX`/`EMPTY_RESPONSE`/`INVALID_JSON`/`ANSWER_FIELD_MISSING`/`TEMPLATE_ERROR`/`SECRET_RESOLUTION_FAILURE`/`UNSUPPORTED_CONFIGURATION`；成功为 null） | `null` |
| answerMasked | `answerMasked` | String | — | — | — | 脱敏后的答案 | `"很抱歉，我无法提供该信息"` |
| requestSummaryMasked | `requestSummaryMasked` | String | — | — | — | 脱敏后的请求摘要 | `"query=***"` |
| errorMessageMasked | `errorMessageMasked` | String | — | — | — | 脱敏后的错误消息 | `null` |
| createdAt | `createdAt` | String（Instant） | — | ISO-8601 | — | 调用创建时间 | `"2026-08-19T02:30:00Z"` |

**字段备注**（无则删除）:
- 请求/响应内容均脱敏（`answerMasked`/`requestSummaryMasked`/`errorMessageMasked`）

---

## JSON 示例

```json
{
  "callId": 1,
  "taskId": 1,
  "taskCaseId": 1,
  "sequenceNo": 1,
  "httpStatus": 200,
  "latencyMs": 523,
  "success": true,
  "errorType": null,
  "answerMasked": "很抱歉，我无法提供该信息",
  "requestSummaryMasked": "query=***",
  "errorMessageMasked": null,
  "createdAt": "2026-08-19T02:30:00Z"
}
```

---

*基于 `com.czbank.aicgs.evaluation.report.adapter.in.web.AgentCallResponse` 源码生成 · 2026-08-19*