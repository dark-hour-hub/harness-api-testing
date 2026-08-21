# IndicatorDimension — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `IndicatorDimension` |
| **全限定名** | `com.czbank.aicgs.evaluation.indicator.domain.model.IndicatorDimension` |
| **类型** | 响应体 VO（领域模型直接序列化） |
| **所属模块** | 指标目录模块（indicator） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | 指标维度，`GET /api/indicator-dimensions` 直接返回 `ApiResponse<List<IndicatorDimension>>` |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | long | — | — | — | 维度主键 ID | `1` |
| dimensionCode | `dimensionCode` | String | — | — | — | 维度编码 | `"SECURITY"` |
| name | `name` | String | — | — | — | 维度名称 | `"安全性"` |
| defaultWeight | `defaultWeight` | BigDecimal | — | — | — | 默认权重 | `0.33333333` |
| sortOrder | `sortOrder` | int | — | — | — | 排序号 | `1` |
| enabled | `enabled` | boolean | — | — | — | 是否启用 | `true` |

**字段备注**（无则删除）:
- 无

---

## JSON 示例

```json
{
  "id": 1,
  "dimensionCode": "SECURITY",
  "name": "安全性",
  "defaultWeight": 0.33333333,
  "sortOrder": 1,
  "enabled": true
}
```

---

*基于 `com.czbank.aicgs.evaluation.indicator.domain.model.IndicatorDimension` 源码生成 · 2026-08-19*
