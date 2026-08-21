# AgentResponse — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `AgentResponse` |
| **全限定名** | `com.czbank.aicgs.evaluation.agent.adapter.in.web.AgentResponse` |
| **类型** | 响应体 VO |
| **所属模块** | 智能体模块（agents） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | Agent 配置响应，不返回密钥引用值本身，仅返回 `headerSecretConfigured` 布尔标志 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | Long | — | — | — | 主键 ID | `1` |
| agentCode | `agentCode` | String | — | — | — | 唯一 Agent 编码 | `"AGENT_001"` |
| agentName | `agentName` | String | — | — | — | 显示名称 | `"客服智能体"` |
| category | `category` | String | — | — | — | 业务分类 | `"customer_service"` |
| riskTier | `riskTier` | String（枚举 `RiskTier`） | — | — | — | 风险等级：`A`/`B`/`C`/`D` | `"B"` |
| department | `department` | String | — | — | — | 归属部门 | `"AI 研发部"` |
| version | `version` | String | — | — | — | Agent 版本 | `"1.0.0"` |
| agentType | `agentType` | String | — | — | — | Agent 类型 | `"chat"` |
| adapterType | `adapterType` | String（枚举 `AdapterType`） | — | — | — | 适配器类型：`MINI_ZHEXIAOZHI`/`GENERIC_HTTP_JSON` | `"GENERIC_HTTP_JSON"` |
| endpoint | `endpoint` | String | — | — | — | 端点 URL | `"https://agent.example.com/api/chat"` |
| method | `method` | String | — | — | — | HTTP 方法 | `"POST"` |
| requestTemplate | `requestTemplate` | String | — | — | — | 请求体模板 | `"{\"query\":\"{message}\"}"` |
| messageField | `messageField` | String | — | — | — | 消息字段路径 | `"$.query"` |
| sessionField | `sessionField` | String | — | — | — | 会话字段路径 | `"$.session_id"` |
| answerField | `answerField` | String | — | — | — | 答案字段路径 | `"$.answer"` |
| successField | `successField` | String | — | — | — | 成功标志字段路径 | `"$.success"` |
| errorField | `errorField` | String | — | — | — | 错误字段路径 | `"$.error"` |
| latencyField | `latencyField` | String | — | — | — | 延迟字段路径 | `"$.latency_ms"` |
| tokenField | `tokenField` | String | — | — | — | Token 数字段路径 | `"$.tokens"` |
| toolTraceField | `toolTraceField` | String | — | — | — | 工具调用痕迹字段路径 | `"$.tool_calls"` |
| timeoutMs | `timeoutMs` | long | — | — | — | 超时毫秒数 | `30000` |
| enabled | `enabled` | boolean | — | — | — | 是否启用 | `true` |
| headerSecretConfigured | `headerSecretConfigured` | boolean | — | — | — | 是否配置了密钥引用（值本身永不返回） | `true` |
| createdAt | `createdAt` | String（LocalDateTime） | — | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 创建时间 | `"2026-08-19T10:30:00+08:00"` |
| updatedAt | `updatedAt` | String（LocalDateTime） | — | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 更新时间 | `"2026-08-19T11:00:00+08:00"` |

**字段备注**（无则删除）:
- 无

---

## JSON 示例

```json
{
  "id": 1,
  "agentCode": "AGENT_001",
  "agentName": "客服智能体",
  "category": "customer_service",
  "riskTier": "B",
  "department": "AI 研发部",
  "version": "1.0.0",
  "agentType": "chat",
  "adapterType": "GENERIC_HTTP_JSON",
  "endpoint": "https://agent.example.com/api/chat",
  "method": "POST",
  "requestTemplate": "{\"query\":\"{message}\"}",
  "messageField": "$.query",
  "sessionField": "$.session_id",
  "answerField": "$.answer",
  "successField": "$.success",
  "errorField": "$.error",
  "latencyField": "$.latency_ms",
  "tokenField": "$.tokens",
  "toolTraceField": "$.tool_calls",
  "timeoutMs": 30000,
  "enabled": true,
  "headerSecretConfigured": true,
  "createdAt": "2026-08-19T10:30:00+08:00",
  "updatedAt": "2026-08-19T11:00:00+08:00"
}
```

---

*基于 `com.czbank.aicgs.evaluation.agent.adapter.in.web.AgentResponse` 源码生成 · 2026-08-19*
