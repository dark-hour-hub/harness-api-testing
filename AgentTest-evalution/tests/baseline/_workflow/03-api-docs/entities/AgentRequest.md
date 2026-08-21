# AgentRequest — 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `AgentRequest` |
| **全限定名** | `com.czbank.aicgs.evaluation.agent.adapter.in.web.AgentRequest` |
| **类型** | 请求体 DTO |
| **所属模块** | 智能体模块（agents） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认，JSON 键名 = Java 字段名） |
| **说明** | Agent 配置输入。无任何校验注解，必填项由 Controller 手工校验（`AgentController.requireRequest` + `AgentConfigService.validate`），失败返回 `COMMON_400_VALIDATION` / `AGENT_400_CONFIG` |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| agentCode | `agentCode` | String | ✅ | 手工校验：正则 `[A-Z0-9_]{2,64}` | — | 唯一 Agent 编码 | `"AGENT_001"` |
| agentName | `agentName` | String | ✅ | 手工校验：非空 | — | 显示名称 | `"客服智能体"` |
| category | `category` | String | ✅ | 手工校验：非空 | — | 业务分类 | `"customer_service"` |
| riskTier | `riskTier` | String | ✅ | 手工校验：枚举 `A`/`B`/`C`/`D` | — | 风险等级 | `"B"` |
| department | `department` | String | 否 | — | — | 归属部门 | `"AI 研发部"` |
| version | `version` | String | ✅ | 手工校验：非空 | — | Agent 版本 | `"1.0.0"` |
| agentType | `agentType` | String | ✅ | 手工校验：非空 | — | Agent 类型 | `"chat"` |
| adapterType | `adapterType` | String | ✅ | 手工校验：枚举 `MINI_ZHEXIAOZHI`/`GENERIC_HTTP_JSON` | — | 适配器类型 | `"GENERIC_HTTP_JSON"` |
| endpoint | `endpoint` | String | ✅ | 手工校验：http/https URI 且含 host | — | 绝对端点 URL | `"https://agent.example.com/api/chat"` |
| method | `method` | String | ✅ | 手工校验：非空 | — | HTTP 方法 | `"POST"` |
| requestTemplate | `requestTemplate` | String | 否 | 手工校验：必须是合法 JSON | — | 请求体模板 | `"{\"query\":\"{message}\"}"` |
| messageField | `messageField` | String | 否 | 手工校验：合法 JsonPath（非空时） | — | 消息字段路径 | `"$.query"` |
| sessionField | `sessionField` | String | 否 | 手工校验：合法 JsonPath（非空时） | — | 会话字段路径 | `"$.session_id"` |
| answerField | `answerField` | String | 条件 | 手工校验：`adapterType=GENERIC_HTTP_JSON` 时必填；合法 JsonPath | — | 答案 JSON 字段路径 | `"$.answer"` |
| successField | `successField` | String | 否 | 手工校验：合法 JsonPath（非空时） | — | 成功标志字段路径 | `"$.success"` |
| errorField | `errorField` | String | 否 | 手工校验：合法 JsonPath（非空时） | — | 错误字段路径 | `"$.error"` |
| latencyField | `latencyField` | String | 否 | 手工校验：合法 JsonPath（非空时） | — | 延迟字段路径 | `"$.latency_ms"` |
| tokenField | `tokenField` | String | 否 | 手工校验：合法 JsonPath（非空时） | — | Token 数字段路径 | `"$.tokens"` |
| toolTraceField | `toolTraceField` | String | 否 | 手工校验：合法 JsonPath（非空时） | — | 工具调用痕迹字段路径 | `"$.tool_calls"` |
| headerSecretRef | `headerSecretRef` | String | 否 | 手工校验：正则 `(?:env:[A-Za-z_][A-Za-z0-9_]*\|secret:[A-Za-z0-9][A-Za-z0-9._:/-]*\|app-[A-Za-z0-9]{6,})`；禁止裸密钥标签（password/token/apiKey 等）与 authorization 引用 | — | 运行时密钥引用（`env:NAME` 或 Dify Key `app-xxxxxx`），密钥值永不内嵌 | `"env:AGENT_HEADER"` |
| timeoutMs | `timeoutMs` | String | ✅ | 手工校验：数值 100~120000 | — | 请求超时毫秒数（注意：声明类型为 String，由 Controller 解析） | `"30000"` |
| enabled | `enabled` | String | 否 | 手工校验：`true`/`false` | `"true"` | 启用标志，缺省视为 true | `"true"` |

**字段备注**（无则删除）:
- 无

---

## JSON 示例

```json
{
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
  "headerSecretRef": "env:AGENT_HEADER",
  "timeoutMs": "30000",
  "enabled": "true"
}
```

---

*基于 `com.czbank.aicgs.evaluation.agent.adapter.in.web.AgentRequest` 源码生成 · 2026-08-19*
