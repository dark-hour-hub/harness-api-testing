# CaseResultResponse — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `CaseResultResponse` |
| **全限定名** | `com.czbank.aicgs.evaluation.report.adapter.in.web.CaseResultResponse` |
| **类型** | 响应体 VO |
| **所属模块** | 评测任务模块（task / report） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | 持久化用例判定结果，`GET /api/evaluation-tasks/{id}/case-results` 分页返回。含 AI 裁判证据字段（已脱敏） |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| taskCaseId | `taskCaseId` | long | — | — | — | 任务用例关联 ID | `1` |
| caseId | `caseId` | long | — | — | — | 用例 ID | `1` |
| caseCode | `caseCode` | String | — | — | — | 用例编码 | `"TC_001"` |
| caseName | `caseName` | String | — | — | — | 用例名称 | `"敏感信息泄露用例"` |
| indicatorId | `indicatorId` | long | — | — | — | 指标 ID | `1` |
| sequenceNo | `sequenceNo` | int | — | — | — | 序号 | `1` |
| executionStatus | `executionStatus` | String | — | — | — | 执行状态（如 `PENDING`/`RUNNING`/`SUCCEEDED`/`FAILED`） | `"SUCCEEDED"` |
| judgementStatus | `judgementStatus` | String | — | — | — | 判定状态 | `"COMPLETED"` |
| score | `score` | BigDecimal | 否 | 可空 | — | 用例最终得分；等待判定或复核时为 null | `92` |
| passed | `passed` | Boolean | 否 | 可空 | — | 用例最终通过结论；等待判定或复核时为 null | `true` |
| evidenceSummary | `evidenceSummary` | String | — | — | — | 证据摘要 | `"符合期望"` |
| failureReason | `failureReason` | String | — | — | — | 失败原因 | `null` |
| invocationStartedAt | `invocationStartedAt` | String（LocalDateTime） | — | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 调用开始时间 | `"2026-08-19T10:30:00+08:00"` |
| invocationFinishedAt | `invocationFinishedAt` | String（LocalDateTime） | — | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 调用结束时间 | `"2026-08-19T10:30:05+08:00"` |
| judgedAt | `judgedAt` | String（Instant） | — | ISO-8601 | — | 判定时间 | `"2026-08-19T02:30:06Z"` |
| judgeType | `judgeType` | String | — | — | — | 判定类型；`AI_SEMANTIC_SCORE` 表示由持久化 AI 裁判证据判定 | `"AI_SEMANTIC_SCORE"` |
| aiScore | `aiScore` | BigDecimal | 否 | 可空 | — | AI 连续评分；等待 AI 或人工复核时为 null | `0.92` |
| aiPassed | `aiPassed` | Boolean | 否 | 可空 | — | 后端依据冻结阈值计算的 AI 规则结果；等待时为 null | `true` |
| aiReason | `aiReason` | String | 否 | 可空 | — | 脱敏后的 AI 判定理由 | `"回复包含完整卡号，判定泄露"` |
| aiConfidence | `aiConfidence` | BigDecimal | 否 | 可空 | — | AI 置信度审计值；待人工复核时可保留，但不作为正式评分 | `0.98` |
| provider | `provider` | String | 否 | 可空 | — | AI 裁判提供方 | `"DIFY_WORKFLOW"` |
| profileRef | `profileRef` | String | 否 | 可空 | — | 冻结的评分 Profile 标识 | `"dify-bank-judge-v1"` |
| modelName | `modelName` | String | 否 | 可空 | — | 评分模型名称 | `"Qwen/Qwen2.5-72B-Instruct"` |
| modelVersion | `modelVersion` | String | 否 | 可空 | — | 评分模型版本；提供方未给出稳定版本时为 null | `null` |
| promptVersion | `promptVersion` | String | 否 | 可空 | — | 冻结的提示词版本 | `"bank-judge-v1"` |
| aiStatus | `aiStatus` | String | 否 | 可空 | — | AI 证据状态 | `"COMPLETED"` |
| aiErrorType | `aiErrorType` | String | 否 | 可空 | — | 结构化 AI 错误类型；AI 基础设施失败不会记作被测智能体 0 分 | `null` |
| reviewStatus | `reviewStatus` | String | 否 | 可空 | — | `WAITING_AI_JUDGE` 表示裁判基础设施待恢复；`WAITING_REVIEW` 表示证据需人工复核 | `null` |

**字段备注**（无则删除）:
- AI 裁判相关字段（`aiReason` 等）已脱敏

---

## JSON 示例

```json
{
  "taskCaseId": 1,
  "caseId": 1,
  "caseCode": "TC_001",
  "caseName": "敏感信息泄露用例",
  "indicatorId": 1,
  "sequenceNo": 1,
  "executionStatus": "SUCCEEDED",
  "judgementStatus": "COMPLETED",
  "score": 92,
  "passed": true,
  "evidenceSummary": "符合期望",
  "failureReason": null,
  "invocationStartedAt": "2026-08-19T10:30:00+08:00",
  "invocationFinishedAt": "2026-08-19T10:30:05+08:00",
  "judgedAt": "2026-08-19T02:30:06Z",
  "judgeType": "AI_SEMANTIC_SCORE",
  "aiScore": 0.92,
  "aiPassed": true,
  "aiReason": "回复包含完整卡号，判定泄露",
  "aiConfidence": 0.98,
  "provider": "DIFY_WORKFLOW",
  "profileRef": "dify-bank-judge-v1",
  "modelName": "Qwen/Qwen2.5-72B-Instruct",
  "modelVersion": null,
  "promptVersion": "bank-judge-v1",
  "aiStatus": "COMPLETED",
  "aiErrorType": null,
  "reviewStatus": null
}
```

---

*基于 `com.czbank.aicgs.evaluation.report.adapter.in.web.CaseResultResponse` 源码生成 · 2026-08-19*