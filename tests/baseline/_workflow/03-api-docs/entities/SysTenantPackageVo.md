# SysTenantPackageVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysTenantPackageVo` |
| **全限定名** | `org.dromara.system.domain.vo.SysTenantPackageVo` |
| **类型** | 响应体 VO |
| **所属模块** | 系统管理 |
| **父类** | 无（实现 `Serializable`） |
| **序列化特性** | 无特殊配置 |
| **说明** | 租户套餐视图对象，用于套餐列表和详情的查询响应 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| packageId | `packageId` | number | 否 | — | — | 租户套餐 ID | `1` |
| packageName | `packageName` | string | 否 | — | — | 套餐名称 | `"企业标准版"` |
| menuIds | `menuIds` | string | 否 | — | — | 关联菜单 ID（逗号分隔） | `"1,2,3,100"` |
| remark | `remark` | string | 否 | — | — | 备注 | `"适合中小企业使用"` |
| menuCheckStrictly | `menuCheckStrictly` | boolean | 否 | — | — | 菜单树选择项是否关联显示 | `true` |
| status | `status` | string | 否 | — | — | 状态（0=正常 1=停用） | `"0"` |

---

## JSON 示例

```json
{
  "packageId": 1,
  "packageName": "企业标准版",
  "menuIds": "1,2,3,100",
  "remark": "适合中小企业使用",
  "menuCheckStrictly": true,
  "status": "0"
}
```

---

*基于 `org.dromara.system.domain.vo.SysTenantPackageVo` 源码生成 * 2026-07-14*
