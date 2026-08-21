# IndicatorCatalogVersion — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `IndicatorCatalogVersion` |
| **全限定名** | `com.czbank.aicgs.evaluation.indicator.domain.model.IndicatorCatalogVersion` |
| **类型** | 响应体 VO（领域模型直接序列化） |
| **所属模块** | 指标目录模块（indicator） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认）；构造时 `riskWeights` 深拷贝为不可变 Map |
| **说明** | 已发布的指标目录版本，`GET /api/indicator-catalog-versions` 返回 `ApiResponse<List<IndicatorCatalogVersion>>` |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| versionCode | `versionCode` | String | — | — | — | 版本编码 | `"V1"` |
| displayName | `displayName` | String | — | — | — | 版本显示名 | `"2026-08 版"` |
| status | `status` | String（枚举 `CatalogVersionStatus`） | — | — | — | 目录版本状态：`DRAFT`/`PUBLISHED`/`RETIRED` | `"PUBLISHED"` |
| isDefault | `isDefault` | boolean | — | — | — | 是否默认版本 | `true` |
| dimensionCount | `dimensionCount` | int | — | — | — | 维度数量 | `3` |
| categoryCount | `categoryCount` | int | — | — | — | 分类数量 | `9` |
| indicatorCount | `indicatorCount` | int | — | — | — | 指标数量 | `42` |
| riskWeights | `riskWeights` | object（`Map<RiskTier, Map<String, BigDecimal>>`） | — | — | — | 风险等级 →（维度编码 → 权重）映射 | 见示例 |
| publishedAt | `publishedAt` | String（LocalDateTime） | — | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 发布时间 | `"2026-08-01T00:00:00+08:00"` |
| createdAt | `createdAt` | String（LocalDateTime） | — | 全局 Jackson 格式 `yyyy-MM-dd'T'HH:mm:ssXXX` | — | 创建时间 | `"2026-07-20T09:00:00+08:00"` |

**字段备注**（无则删除）:
- 无

---

## JSON 示例

```json
{
  "versionCode": "V1",
  "displayName": "2026-08 版",
  "status": "PUBLISHED",
  "isDefault": true,
  "dimensionCount": 3,
  "categoryCount": 9,
  "indicatorCount": 42,
  "riskWeights": {
    "A": {
      "SECURITY": 0.5,
      "CAPABILITY": 0.3,
      "EVOLUTION": 0.2
    },
    "B": {
      "SECURITY": 0.4,
      "CAPABILITY": 0.35,
      "EVOLUTION": 0.25
    }
  },
  "publishedAt": "2026-08-01T00:00:00+08:00",
  "createdAt": "2026-07-20T09:00:00+08:00"
}
```

---

*基于 `com.czbank.aicgs.evaluation.indicator.domain.model.IndicatorCatalogVersion` 源码生成 · 2026-08-19*
