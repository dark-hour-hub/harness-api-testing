# EvaluationResultResponse — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `EvaluationResultResponse` |
| **全限定名** | `com.czbank.aicgs.evaluation.report.adapter.in.web.EvaluationResultResponse` |
| **类型** | 响应体 VO |
| **所属模块** | 评测任务模块（task / report） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | 任务评测结果汇总（持久化结果，不重算），`GET /api/evaluation-tasks/{id}/results` 返回。嵌套 `AgentSummary`/`SchemeSummary`/`DimensionResult`/`CategoryResult` |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| taskId | `taskId` | long | — | — | — | 任务 ID | `1` |
| taskStatus | `taskStatus` | String | — | — | — | 任务状态 | `"COMPLETED"` |
| agent | `agent` | object（`AgentSummary`） | — | — | — | Agent 摘要 | 见示例 |
| agent.id | `id` | long | — | — | — | Agent ID | `1` |
| agent.code | `code` | String | — | — | — | Agent 编码 | `"AGENT_001"` |
| agent.name | `name` | String | — | — | — | Agent 名称 | `"客服智能体"` |
| agent.version | `version` | String | — | — | — | Agent 版本 | `"1.0.0"` |
| scheme | `scheme` | object（`SchemeSummary`） | — | — | — | 方案摘要 | 见示例 |
| scheme.id | `id` | Long | — | — | — | 方案 ID（可空） | `1` |
| scheme.code | `code` | String | — | — | — | 方案编码 | `"SCHEME_001"` |
| scheme.name | `name` | String | — | — | — | 方案名称 | `"年度评测方案"` |
| scheme.version | `version` | String | — | — | — | 方案版本 | `"1.0.0"` |
| scheme.catalogVersion | `catalogVersion` | String | — | — | — | 目录版本 | `"V1"` |
| scheme.evaluationMode | `evaluationMode` | String | — | — | — | 评测模式 | `"COMPREHENSIVE"` |
| totalScore | `totalScore` | BigDecimal | — | — | — | 总分 | `85.5` |
| grade | `grade` | String | — | — | — | 等级 | `"A"` |
| safetyVetoTriggered | `safetyVetoTriggered` | boolean | — | —（已弃用） | — | 遗留：安全否决触发 | `false` |
| safetyVetoReason | `safetyVetoReason` | String | — | —（已弃用） | — | 遗留：安全否决原因 | `null` |
| dimensions | `dimensions` | array（`DimensionResult`[]） | — | — | — | 维度结果 | 见示例 |
| dimensions[].id | `id` | long | — | — | — | 维度 ID | `1` |
| dimensions[].code | `code` | String | — | — | — | 维度编码 | `"SECURITY"` |
| dimensions[].name | `name` | String | — | — | — | 维度名称 | `"安全性"` |
| dimensions[].score | `score` | BigDecimal | — | — | — | 维度得分 | `90` |
| dimensions[].weight | `weight` | BigDecimal | — | — | — | 权重 | `0.33333333` |
| dimensions[].status | `status` | String | — | — | — | 维度状态 | `"COMPLETED"` |
| dimensions[].vetoTriggered | `vetoTriggered` | boolean | — | — | — | 是否触发否决 | `false` |
| categories | `categories` | array（`CategoryResult`[]） | — | — | — | 分类结果 | 见示例 |
| categories[].id | `id` | long | — | — | — | 分类 ID | `1` |
| categories[].dimensionCode | `dimensionCode` | String | — | — | — | 维度编码 | `"SECURITY"` |
| categories[].code | `code` | String | — | — | — | 分类编码 | `"SEC_PRIVACY"` |
| categories[].name | `name` | String | — | — | — | 分类名称 | `"隐私保护"` |
| categories[].score | `score` | BigDecimal | — | — | — | 分类得分 | `92` |
| categories[].completedIndicatorCount | `completedIndicatorCount` | int | — | — | — | 已完成指标数 | `5` |
| categories[].applicableIndicatorCount | `applicableIndicatorCount` | int | — | — | — | 适用指标数 | `5` |
| categories[].status | `status` | String | — | — | — | 分类状态 | `"COMPLETED"` |
| conclusion | `conclusion` | String | — | —（已弃用） | — | 遗留报告成熟度/兼容性结论 | `null` |
| reportStatus | `reportStatus` | String | — | — | — | 报告状态 | `"COMPLETED"` |
| incompleteReason | `incompleteReason` | String | — | — | — | 未完成原因 | `null` |
| specialScore | `specialScore` | BigDecimal | — | — | — | 专项评分 | `null` |
| specialPassed | `specialPassed` | Boolean | — | — | — | 专项是否通过 | `null` |
| entryConclusion | `entryConclusion` | String | 否 | 可空；值：`PASSED`/`FAILED`/`UNDETERMINED` | — | 准入结论 | `"PASSED"` |
| runningConclusion | `runningConclusion` | String | 否 | 可空；值：`PASSED`/`FAILED`/`UNDETERMINED` | — | 运行结论 | `"FAILED"` |
| entrySafetyVetoTriggered | `entrySafetyVetoTriggered` | Boolean | 否 | 可空 | — | 准入安全否决触发 | `false` |
| entrySafetyVetoReason | `entrySafetyVetoReason` | String | 否 | 可空 | — | 准入安全否决原因 | `null` |
| runningSafetyVetoTriggered | `runningSafetyVetoTriggered` | Boolean | 否 | 可空 | — | 运行安全否决触发 | `false` |
| runningSafetyVetoReason | `runningSafetyVetoReason` | String | 否 | 可空 | — | 运行安全否决原因 | `null` |
| coverage | `coverage` | object（Map） | — | — | — | 覆盖率统计 | `{"total": 10, "completed": 10}` |
| createdAt | `createdAt` | String（LocalDateTime） | — | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 创建时间 | `"2026-08-19T10:00:00+08:00"` |
| startedAt | `startedAt` | String（LocalDateTime） | — | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 开始时间 | `"2026-08-19T10:30:00+08:00"` |
| finishedAt | `finishedAt` | String（LocalDateTime） | — | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 结束时间 | `"2026-08-19T11:00:00+08:00"` |
| generatedAt | `generatedAt` | String（Instant） | — | ISO-8601（Jackson 默认，非时间戳） | — | 生成时间 | `"2026-08-19T03:00:00Z"` |

**字段备注**（无则删除）:
- `safetyVetoTriggered`/`safetyVetoReason`/`conclusion` 标注 `@Schema(deprecated = true)` 为遗留字段

---

## JSON 示例

```json
{
  "taskId": 1,
  "taskStatus": "COMPLETED",
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
  "totalScore": 85.5,
  "grade": "A",
  "safetyVetoTriggered": false,
  "safetyVetoReason": null,
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
  "categories": [
    {
      "id": 1,
      "dimensionCode": "SECURITY",
      "code": "SEC_PRIVACY",
      "name": "隐私保护",
      "score": 92,
      "completedIndicatorCount": 5,
      "applicableIndicatorCount": 5,
      "status": "COMPLETED"
    }
  ],
  "conclusion": null,
  "reportStatus": "COMPLETED",
  "incompleteReason": null,
  "specialScore": null,
  "specialPassed": null,
  "entryConclusion": "PASSED",
  "runningConclusion": "FAILED",
  "entrySafetyVetoTriggered": false,
  "entrySafetyVetoReason": null,
  "runningSafetyVetoTriggered": false,
  "runningSafetyVetoReason": null,
  "coverage": {"total": 10, "completed": 10},
  "createdAt": "2026-08-19T10:00:00+08:00",
  "startedAt": "2026-08-19T10:30:00+08:00",
  "finishedAt": "2026-08-19T11:00:00+08:00",
  "generatedAt": "2026-08-19T03:00:00Z"
}
```

---

*基于 `com.czbank.aicgs.evaluation.report.adapter.in.web.EvaluationResultResponse` 源码生成 · 2026-08-19*