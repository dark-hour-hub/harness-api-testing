# EvaluationTask — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `EvaluationTask` |
| **全限定名** | `com.czbank.aicgs.evaluation.task.domain.model.EvaluationTask` |
| **类型** | 响应体 VO（领域模型直接序列化） |
| **所属模块** | 评测任务模块（task） |
| **父类** | 无（record） |
| **序列化特性** | 字段 `schemeId` 通过 getter 注解 `@JsonProperty("sourceSchemeId")` 转义为 `sourceSchemeId` |
| **说明** | 评测任务详情，`POST /api/evaluation-tasks`、`GET /api/evaluation-tasks`、`GET /api/evaluation-tasks/{id}` 返回。嵌套 `AgentConfigSnapshot`、`SchemeSnapshot`、`EvaluationTaskCase` |

---

## 注解转义说明

| Java 字段名 | JSON 键名 | 显示名 | 转义来源 |
|------------|----------|--------|----------|
| `schemeId` | `sourceSchemeId` | — | getter `sourceSchemeId()` 上 `@JsonProperty("sourceSchemeId")` |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | Long | — | — | — | 任务主键 ID | `1` |
| taskNo | `taskNo` | String | — | — | — | 任务编号 | `"T20260819001"` |
| agentId | `agentId` | long | — | — | — | Agent ID | `1` |
| schemeId | `sourceSchemeId` | Long | — | — | — | 方案 ID（JSON 中为 `sourceSchemeId`） | `1` |
| sourceType | `sourceType` | String（枚举 `TaskSourceType`） | — | — | `SCHEME` | 任务来源：`SCHEME`/`AD_HOC` | `"SCHEME"` |
| agentSnapshot | `agentSnapshot` | object（`AgentConfigSnapshot`） | — | — | — | Agent 快照（详见嵌套展开） | 见示例 |
| schemeSnapshot | `schemeSnapshot` | object（`SchemeSnapshot`） | — | — | — | 方案快照（详见嵌套展开） | 见示例 |
| snapshotHash | `snapshotHash` | String | — | — | — | 快照哈希 | `"a1b2c3..."` |
| evaluationMode | `evaluationMode` | String（枚举 `EvaluationMode`） | — | — | — | 评测模式：`COMPREHENSIVE`/`SPECIAL` | `"COMPREHENSIVE"` |
| riskTier | `riskTier` | String（枚举 `RiskTier`） | — | — | — | 风险等级 | `"B"` |
| evaluationType | `evaluationType` | String（枚举 `EvaluationType`） | — | —（已弃用） | — | 遗留评测类型 | `null` |
| thresholdLevel | `thresholdLevel` | String（枚举 `ThresholdLevel`） | — | —（已弃用） | — | 遗留阈值等级 | `null` |
| status | `status` | String（枚举 `TaskStatus`） | — | — | — | 任务状态：`CREATED`/`RUNNING`/`COMPLETED`/`FAILED` | `"CREATED"` |
| progress | `progress` | BigDecimal | — | — | — | 进度（0~1） | `0` |
| startedAt | `startedAt` | String（LocalDateTime） | — | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 开始时间 | `null` |
| finishedAt | `finishedAt` | String（LocalDateTime） | — | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 结束时间 | `null` |
| interruptionReason | `interruptionReason` | String | — | — | — | 中断原因 | `null` |
| createdBy | `createdBy` | String | — | — | — | 创建人 | `"api"` |
| createdAt | `createdAt` | String（LocalDateTime） | — | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 创建时间 | `"2026-08-19T10:00:00+08:00"` |
| updatedAt | `updatedAt` | String（LocalDateTime） | — | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 更新时间 | `"2026-08-19T10:00:00+08:00"` |
| cases | `cases` | array（`EvaluationTaskCase`[]） | — | — | `[]` | 任务用例（详见嵌套展开） | 见示例 |

**agentSnapshot 嵌套展开（AgentConfigSnapshot，23 字段）**：

| 字段路径 | JSON 键名 | 类型 | 说明 |
|----------|-----------|------|------|
| agentSnapshot.id | `id` | long | Agent ID |
| agentSnapshot.agentCode | `agentCode` | String | Agent 编码 |
| agentSnapshot.agentName | `agentName` | String | Agent 名称 |
| agentSnapshot.category | `category` | String | 业务分类 |
| agentSnapshot.riskTier | `riskTier` | String（枚举 RiskTier） | 风险等级 |
| agentSnapshot.department | `department` | String | 部门 |
| agentSnapshot.version | `version` | String | 版本 |
| agentSnapshot.agentType | `agentType` | String | Agent 类型 |
| agentSnapshot.adapterType | `adapterType` | String（枚举 AdapterType） | 适配器类型 |
| agentSnapshot.endpoint | `endpoint` | String | 端点 URL |
| agentSnapshot.method | `method` | String | HTTP 方法 |
| agentSnapshot.requestTemplate | `requestTemplate` | String | 请求模板 |
| agentSnapshot.messageField ~ toolTraceField | `messageField`~`toolTraceField` | String | 各 JsonPath 字段（message/session/answer/success/error/latency/token/toolTrace） |
| agentSnapshot.headerSecretRef | `headerSecretRef` | String | 密钥引用 |
| agentSnapshot.timeoutMs | `timeoutMs` | long | 超时毫秒 |
| agentSnapshot.enabled | `enabled` | boolean | 启用标志 |

**schemeSnapshot 嵌套展开（SchemeSnapshot，18 字段）**：

| 字段路径 | JSON 键名 | 类型 | 说明 |
|----------|-----------|------|------|
| schemeSnapshot.id | `id` | Long | 方案 ID |
| schemeSnapshot.schemeCode | `schemeCode` | String | 方案编码 |
| schemeSnapshot.schemeName | `schemeName` | String | 方案名称 |
| schemeSnapshot.version | `version` | String | 版本 |
| schemeSnapshot.catalogVersion | `catalogVersion` | String | 目录版本，缺省 `"V1"` |
| schemeSnapshot.status | `status` | String（枚举 SchemeStatus） | 方案状态 |
| schemeSnapshot.evaluationMode | `evaluationMode` | String（枚举 EvaluationMode） | 评测模式 |
| schemeSnapshot.evaluationType | `evaluationType` | String（枚举 EvaluationType） | 遗留评测类型（已弃用） |
| schemeSnapshot.riskTier | `riskTier` | String（枚举 RiskTier） | 风险等级 |
| schemeSnapshot.thresholdLevel | `thresholdLevel` | String（枚举 ThresholdLevel） | 遗留阈值等级（已弃用） |
| schemeSnapshot.dimensionWeights | `dimensionWeights` | object（DimensionWeights） | 维度权重，JSON 键 `weights` |
| schemeSnapshot.safetyVetoEnabled | `safetyVetoEnabled` | boolean | 安全一票否决 |
| schemeSnapshot.stopOnSafetyFailure | `stopOnSafetyFailure` | boolean | 安全失败停止 |
| schemeSnapshot.scoringConfigJson | `scoringConfigJson` | String | 评分配置 JSON |
| schemeSnapshot.dimensions | `dimensions` | array（DimensionSnapshot[]） | 维度快照（id/dimensionCode/name/effectiveWeight/sortOrder） |
| schemeSnapshot.categories | `categories` | array（CategorySnapshot[]） | 分类快照（id/dimensionCode/categoryCode/name/defaultWeight/sortOrder/enabled/effectiveWeight/required） |
| schemeSnapshot.indicators | `indicators` | array（IndicatorSnapshot[]） | 指标快照（28 字段，含 definition/阈值/collectionMethod/effectiveWeight/effectiveThreshold/normalizationParametersJson/required 等） |
| schemeSnapshot.testCases | `testCases` | array（TestCaseSnapshot[]） | 用例快照（21 字段，含 catalogWeight/effectiveWeight/passScore/combineMode/rules[]） |

**cases 嵌套展开（EvaluationTaskCase，11 字段）**：

| 字段路径 | JSON 键名 | 类型 | 说明 |
|----------|-----------|------|------|
| cases[].id | `id` | Long | 用例任务关联 ID |
| cases[].taskId | `taskId` | Long | 任务 ID |
| cases[].testCaseId | `testCaseId` | long | 用例 ID |
| cases[].indicatorId | `indicatorId` | long | 指标 ID |
| cases[].sequenceNo | `sequenceNo` | int | 序号 |
| cases[].status | `status` | String | 用例执行状态 |
| cases[].attemptCount | `attemptCount` | int | 尝试次数 |
| cases[].sessionKey | `sessionKey` | String | 会话键 |
| cases[].currentResultId | `currentResultId` | Long | 当前结果 ID |
| cases[].startedAt | `startedAt` | String（LocalDateTime） | 开始时间 |
| cases[].finishedAt | `finishedAt` | String（LocalDateTime） | 结束时间 |

**字段备注**（无则删除）:
- `schemeId` → `sourceSchemeId` 注解转义（见注解转义说明）

---

## JSON 示例

```json
{
  "id": 1,
  "taskNo": "T20260819001",
  "agentId": 1,
  "sourceSchemeId": 1,
  "sourceType": "SCHEME",
  "agentSnapshot": {
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
    "headerSecretRef": "env:AGENT_HEADER",
    "timeoutMs": 30000,
    "enabled": true
  },
  "schemeSnapshot": {
    "id": 1,
    "schemeCode": "SCHEME_001",
    "schemeName": "年度评测方案",
    "version": "1.0.0",
    "catalogVersion": "V1",
    "status": "PUBLISHED",
    "evaluationMode": "COMPREHENSIVE",
    "evaluationType": null,
    "riskTier": "B",
    "thresholdLevel": null,
    "dimensionWeights": {"weights": {"SAFETY": 0.4, "CAPABILITY": 0.35, "EVOLUTION": 0.25}},
    "safetyVetoEnabled": true,
    "stopOnSafetyFailure": true,
    "scoringConfigJson": "{}",
    "dimensions": [],
    "categories": [],
    "indicators": [],
    "testCases": []
  },
  "snapshotHash": "a1b2c3d4e5f6",
  "evaluationMode": "COMPREHENSIVE",
  "riskTier": "B",
  "evaluationType": null,
  "thresholdLevel": null,
  "status": "CREATED",
  "progress": 0,
  "startedAt": null,
  "finishedAt": null,
  "interruptionReason": null,
  "createdBy": "api",
  "createdAt": "2026-08-19T10:00:00+08:00",
  "updatedAt": "2026-08-19T10:00:00+08:00",
  "cases": [
    {
      "id": 1,
      "taskId": 1,
      "testCaseId": 1,
      "indicatorId": 1,
      "sequenceNo": 1,
      "status": "PENDING",
      "attemptCount": 0,
      "sessionKey": null,
      "currentResultId": null,
      "startedAt": null,
      "finishedAt": null
    }
  ]
}
```

---

*基于 `com.czbank.aicgs.evaluation.task.domain.model.EvaluationTask` 源码生成 · 2026-08-19*
