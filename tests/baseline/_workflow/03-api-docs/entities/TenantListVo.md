# TenantListVo — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `TenantListVo` |
| **全限定名** | `org.dromara.web.domain.vo.TenantListVo` |
| **类型** | 响应体 VO |
| **所属模块** | 认证模块 (auth) |
| **父类** | 无 |
| **序列化特性** | 无特殊配置 |
| **说明** | 租户列表条目响应体，展示单个租户的基本信息。通过 MapStruct（`@AutoMapper(target = SysTenantVo.class)`）从 `SysTenantVo` 转换而来 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| tenantId | `tenantId` | string | — | — | — | 租户编号，唯一标识一个租户 | `"100000"` |
| companyName | `companyName` | string | — | — | — | 企业名称 | `"若依科技有限公司"` |
| domain | `domain` | string | — | — | — | 租户域名，用于根据请求域名自动匹配对应租户 | `"admin.ruoyi.vip"` |

---

## JSON 示例

```json
{
  "tenantId": "100000",
  "companyName": "若依科技有限公司",
  "domain": "admin.ruoyi.vip"
}
```

---

*基于 `org.dromara.web.domain.vo.TenantListVo` 源码生成 · 2026-07-14*
