# SysUserPasswordBo -- 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysUserPasswordBo` |
| **全限定名** | `org.dromara.system.domain.bo.SysUserPasswordBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 系统管理 |
| **父类** | 无（直接实现 `Serializable`） |
| **序列化特性** | 无特殊配置 |
| **说明** | 用户密码修改请求对象，用于 `/system/user/profile/updatePwd` 重置个人密码。包含旧密码和新密码两个字段，接口对旧密码进行校验、新密码加密后存储 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| oldPassword | `oldPassword` | string | ✅ | `@NotBlank` | — | 旧密码 | `"OldPass@123"` |
| newPassword | `newPassword` | string | ✅ | `@NotBlank` | — | 新密码（明文传输，需 `@ApiEncrypt` 接口级加密） | `"NewPass@456"` |

---

## JSON 示例

```json
{
  "oldPassword": "OldPass@123",
  "newPassword": "NewPass@456"
}
```

---

*基于 `org.dromara.system.domain.bo.SysUserPasswordBo` 源码生成 * 2026-07-14*
