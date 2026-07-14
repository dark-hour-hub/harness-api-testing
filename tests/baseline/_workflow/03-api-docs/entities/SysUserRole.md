# SysUserRole -- 业务对象

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysUserRole` |
| **全限定名** | `org.dromara.system.domain.SysUserRole` |
| **类型** | 业务对象（Domain Entity / 请求体） |
| **所属模块** | 系统管理 |
| **父类** | 无 |
| **序列化特性** | 无特殊配置 |
| **说明** | 用户与角色关联对象，对应数据库表 `sys_user_role`。用于批量授权/取消授权用户角色时传递的用户-角色关联数据 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| userId | `userId` | number | 否 | `@TableId(type=INPUT)`（手动赋值主键） | — | 用户ID | `1` |
| roleId | `roleId` | number | 否 | — | — | 角色ID | `2` |

---

## JSON 示例

```json
{
  "userId": 1,
  "roleId": 2
}
```

---

*基于 `org.dromara.system.domain.SysUserRole` 源码生成 * 2026-07-14*
