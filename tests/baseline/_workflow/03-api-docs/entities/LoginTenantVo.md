# LoginTenantVo — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `LoginTenantVo` |
| **全限定名** | `org.dromara.web.domain.vo.LoginTenantVo` |
| **类型** | 响应体 VO |
| **所属模块** | 认证模块 (auth) |
| **父类** | 无 |
| **序列化特性** | 无特殊配置 |
| **说明** | 登录页面租户信息响应体，返回租户功能开关及可选租户列表 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| tenantEnabled | `tenantEnabled` | boolean | — | — | — | 租户功能是否启用（由 `tenant.enable` 配置控制），`false` 时 voList 为空 | `true` |
| voList | `voList` | array | — | — | — | 租户列表，元素类型为 `TenantListVo`。若开启租户且当前为超管则返回全部租户；否则按域名过滤 | `[{...}]` |

### voList 元素字段（TenantListVo）

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| voList[].tenantId | `tenantId` | string | — | — | — | 租户编号 | `"100000"` |
| voList[].companyName | `companyName` | string | — | — | — | 企业名称 | `"若依科技有限公司"` |
| voList[].domain | `domain` | string | — | — | — | 域名，用于根据访问域名自动匹配对应租户 | `"admin.ruoyi.vip"` |

---

## JSON 示例

```json
{
  "tenantEnabled": true,
  "voList": [
    {
      "tenantId": "100000",
      "companyName": "若依科技有限公司",
      "domain": "admin.ruoyi.vip"
    },
    {
      "tenantId": "100001",
      "companyName": "某某信息科技公司",
      "domain": "xxx.example.com"
    }
  ]
}
```

---

*基于 `org.dromara.web.domain.vo.LoginTenantVo` 源码生成 · 2026-07-14*
