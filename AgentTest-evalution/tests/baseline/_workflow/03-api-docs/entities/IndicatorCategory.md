# IndicatorCategory — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `IndicatorCategory` |
| **全限定名** | `com.czbank.aicgs.evaluation.indicator.domain.model.IndicatorCategory` |
| **类型** | 响应体 VO（领域模型直接序列化） |
| **所属模块** | 指标目录模块（indicator） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认） |
| **说明** | 指标分类，`GET /api/indicator-categories` 直接返回 `ApiResponse<List<IndicatorCategory>>` |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | long | — | — | — | 分类主键 ID | `1` |
| dimensionCode | `dimensionCode` | String | — | — | — | 所属维度编码 | `"SECURITY"` |
| categoryCode | `categoryCode` | String | — | — | — | 分类编码 | `"SEC_PRIVACY"` |
| name | `name` | String | — | — | — | 分类名称 | `"隐私保护"` |
| defaultWeight | `defaultWeight` | BigDecimal | — | — | — | 默认权重 | `0.5` |
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
  "categoryCode": "SEC_PRIVACY",
  "name": "隐私保护",
  "defaultWeight": 0.5,
  "sortOrder": 1,
  "enabled": true
}
```

---

*基于 `com.czbank.aicgs.evaluation.indicator.domain.model.IndicatorCategory` 源码生成 · 2026-08-19*
