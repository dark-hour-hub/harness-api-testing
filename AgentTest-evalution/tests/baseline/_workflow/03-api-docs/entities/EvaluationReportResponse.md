# EvaluationReportResponse — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `EvaluationReportResponse` |
| **全限定名** | `com.czbank.aicgs.evaluation.report.adapter.in.web.EvaluationReportResponse` |
| **类型** | 响应体 VO |
| **所属模块** | 评测任务模块（task / report） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | 唯一持久化评测报告，`GET /api/evaluation-tasks/{id}/report` 返回。嵌套类型复用 `EvaluationResultResponse.DimensionResult`/`AgentSummary`/`SchemeSummary` |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| taskId | `taskId` | long | — | — | — | 任务 ID | `1` |
| taskStatus | `taskStatus` | String | — | — | — | 任务状态 | `"COMPLETED"` |
| reportStatus | `reportStatus` | String | — | — | — | 报告状态（由结论推导） | `"COMPLETED"` |
| totalScore | `totalScore` | BigDecimal | — | — | — | 总分 | `85.5` |
| grade | `grade` | String | — | — | — | 等级 | `"A"` |
| specialScore | `specialScore` | BigDecimal | — | — | — | 专项评分 | `null` |
| specialPassed | `specialPassed` | Boolean | — | — | — | 专项是否通过 | `null` |
| dimensions | `dimensions` | array（`DimensionResult`[]） | — | — | — | 维度结果（字段同 EvaluationResultResponse.dimensions：id/code/name/score/weight/status/vetoTriggered） | 见示例 |
| safetyVetoTriggered | `safetyVetoTriggered` | boolean | — | —（已弃用） | — | 遗留：安全否决触发 | `false` |
| safetyVetoReason | `safetyVetoReason` | String | — | —（已弃用） | — | 遗留：安全否决原因 | `null` |
| conclusion | `conclusion` | String | — | —（已弃用） | — | 遗留报告成熟度/兼容性结论 | `null` |
| entryConclusion | `entryConclusion` | String | 否 | 可空；值：`PASSED`/`FAILED`/`UNDETERMINED` | — | 准入结论 | `"PASSED"` |
| runningConclusion | `runningConclusion` | String | 否 | 可空；值：`PASSED`/`FAILED`/`UNDETERMINED` | — | 运行结论 | `"FAILED"` |
| entrySafetyVetoTriggered | `entrySafetyVetoTriggered` | Boolean | 否 | 可空 | — | 准入安全否决触发 | `false` |
| entrySafetyVetoReason | `entrySafetyVetoReason` | String | 否 | 可空 | — | 准入安全否决原因 | `null` |
| runningSafetyVetoTriggered | `runningSafetyVetoTriggered` | Boolean | 否 | 可空 | — | 运行安全否决触发 | `false` |
| runningSafetyVetoReason | `runningSafetyVetoReason` | String | 否 | 可空 | — | 运行安全否决原因 | `null` |
| incompleteReason | `incompleteReason` | String | — | — | — | 未完成原因 | `null` |
| agent | `agent` | object（`AgentSummary`） | — | — | — | Agent 摘要（id/code/name/version） | 见示例 |
| scheme | `scheme` | object（`SchemeSummary`） | — | — | — | 方案摘要（id/code/name/version/catalogVersion/evaluationMode） | 见示例 |
| summary | `summary` | String | — | — | — | 报告摘要 | `"本次评测总体表现良好"` |
| remediation | `remediation` | String | — | — | — | 整改建议 | `"建议优化敏感信息过滤"` |
| reportVersion | `reportVersion` | String | — | — | — | 报告版本 | `"1.0.0"` |
| generatedAt | `generatedAt` | String（Instant） | — | ISO-8601 | — | 生成时间 | `"2026-08-19T03:00:00Z"` |

**字段备注**（无则删除）:
- `safetyVetoTriggered`/`safetyVetoReason`/`conclusion` 标注 `@Schema(deprecated = true)` 为遗留字段

---

## JSON 示例

```json
{
  "taskId": 1,
  "taskStatus": "COMPLETED",
  "reportStatus": "COMPLETED",
  "totalScore": 85.5,
  "grade": "A",
  "specialScore": null,
  "specialPassed": null,
  "dimensions": [
    {
      "id": 1,
      "code": "SECURITY",
      "name": "安全性",
      "score": 90,
      "weight": 0.33333333,
      "status": "COMPLETED",
      "vetoTriggered": false
    }
  ],
  "safetyVetoTriggered": false,
  "safetyVetoReason": null,
  "conclusion": null,
  "entryConclusion": "PASSED",
  "runningConclusion": "FAILED",
  "entrySafetyVetoTriggered": false,
  "entrySafetyVetoReason": null,
  "runningSafetyVetoTriggered": false,
  "runningSafetyVetoReason": null,
  "incompleteReason": null,
  "agent": {
    "id": 1,
    "code": "AGENT_001",
    "name": "客服智能体",
    "version": "1.0.0"
  },
  "scheme": {
    "id": 1,
    "code": "SCHEME_001",
    "name": "年度评测方案",
    "version": "1.0.0",
    "catalogVersion": "V1",
    "evaluationMode": "COMPREHENSIVE"
  },
  "summary": "本次评测总体表现良好",
  "remediation": "建议优化敏感信息过滤",
  "reportVersion": "1.0.0",
  "generatedAt": "2026-08-19T03:00:00Z"
}
```

---

*基于 `com.czbank.aicgs.evaluation.report.adapter.in.web.EvaluationReportResponse` 源码生成 · 2026-08-19*