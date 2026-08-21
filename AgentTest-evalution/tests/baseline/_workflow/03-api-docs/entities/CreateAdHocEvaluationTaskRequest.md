# CreateAdHocEvaluationTaskRequest — 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `CreateAdHocEvaluationTaskRequest` |
| **全限定名** | `com.czbank.aicgs.evaluation.task.adapter.in.web.CreateAdHocEvaluationTaskRequest` |
| **类型** | 请求体 DTO |
| **所属模块** | 评测任务模块（task） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | 基于当前页面配置创建临场（ad-hoc）任务，不保存方案（`POST /api/evaluation-tasks/ad-hoc`）。`@Valid` 校验。嵌套 `AdHocIndicatorRequest`（当前页指标选择冻结） |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| agentId | `agentId` | Long | ✅ | `@NotNull` `@Positive` | — | Agent ID | `1` |
| sourceSchemeId | `sourceSchemeId` | Long | 否 | `@Positive` | — | 来源方案 ID（可选） | `1` |
| catalogVersion | `catalogVersion` | String | 否 | — | — | 指标目录版本，缺省用唯一默认版本 | `"V1"` |
| evaluationMode | `evaluationMode` | String（枚举 `EvaluationMode`） | ✅ | `@NotNull` | — | 评测覆盖模式：`COMPREHENSIVE`/`SPECIAL` | `"COMPREHENSIVE"` |
| evaluationType | `evaluationType` | String（枚举 `EvaluationType`） | 否 | —（已弃用） | — | 遗留生命周期类型，不再选择评分阈值 | `null` |
| riskTier | `riskTier` | String（枚举 `RiskTier`） | ✅ | `@NotNull` | — | 适用风险等级：`A`/`B`/`C`/`D` | `"B"` |
| thresholdLevel | `thresholdLevel` | String（枚举 `ThresholdLevel`） | 否 | —（已弃用） | — | 遗留单阈值选择 | `null` |
| dimensionWeights | `dimensionWeights` | object（`DimensionWeights`） | 否 | — | — | 维度权重（JSON 键 `weights`，见 DimensionWeights 文档） | 见示例 |
| safetyVetoEnabled | `safetyVetoEnabled` | Boolean | 否 | — | `true` | 启用安全一票否决 | `true` |
| stopOnSafetyFailure | `stopOnSafetyFailure` | Boolean | 否 | — | `true` | 安全失败即停止 | `true` |
| scoringConfigJson | `scoringConfigJson` | String | 否 | — | — | 评分配置 JSON | `"{}"` |
| indicators | `indicators` | array（`AdHocIndicatorRequest`[]） | ✅ | `@NotEmpty` + 嵌套 `@Valid` | — | 指标选择列表 | 见示例 |
| indicators[].indicatorId | `indicatorId` | Long | ✅ | `@NotNull` `@Positive` | — | 指标 ID | `1` |
| indicators[].weightOverride | `weightOverride` | BigDecimal | 否 | `@DecimalMin(value="0", inclusive=false)` | — | 权重覆盖（>0） | `0.4` |
| indicators[].thresholdOverride | `thresholdOverride` | BigDecimal | 否 | `@DecimalMin(value="0", inclusive=false)` | — | 阈值覆盖（>0，已弃用语义） | `0.3` |
| indicators[].normalizationOverrideJson | `normalizationOverrideJson` | String | 否 | — | — | 归一化覆盖 JSON | `null` |
| indicators[].required | `required` | Boolean | 否 | — | — | 是否必评 | `true` |
| testCaseIds | `testCaseIds` | Long[] | ✅ | `@NotEmpty` + 元素 `@Positive` | — | 用例 ID 列表 | `[1, 2, 3]` |
| createdBy | `createdBy` | String | 否 | `@Size(max=100)` | — | 创建人标签 | `"api"` |

**字段备注**（无则删除）:
- `evaluationType`、`thresholdLevel` 标注 `@Schema(deprecated = true)`，为遗留字段
- `dimensionWeights` 为自定义类 `DimensionWeights`，序列化 JSON 键为 `weights`（`@JsonProperty`），未序列化 `safety()`/`capability()`/`evolution()` 便捷方法（`@JsonIgnore`）

---

## JSON 示例

```json
{
  "agentId": 1,
  "sourceSchemeId": 1,
  "catalogVersion": "V1",
  "evaluationMode": "COMPREHENSIVE",
  "evaluationType": null,
  "riskTier": "B",
  "thresholdLevel": null,
  "dimensionWeights": {
    "weights": {
      "SAFETY": 0.4,
      "CAPABILITY": 0.35,
      "EVOLUTION": 0.25
    }
  },
  "safetyVetoEnabled": true,
  "stopOnSafetyFailure": true,
  "scoringConfigJson": "{}",
  "indicators": [
    {
      "indicatorId": 1,
      "weightOverride": 0.4,
      "thresholdOverride": 0.3,
      "normalizationOverrideJson": null,
      "required": true
    }
  ],
  "testCaseIds": [1, 2, 3],
  "createdBy": "api"
}
```

---

*基于 `com.czbank.aicgs.evaluation.task.adapter.in.web.CreateAdHocEvaluationTaskRequest` 源码生成 · 2026-08-19*
