# AvatarVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `AvatarVo` |
| **全限定名** | `org.dromara.system.controller.system.SysProfileController.AvatarVo` |
| **类型** | 响应体 VO（Java `record`） |
| **所属模块** | 系统管理 |
| **父类** | 无（`java.lang.Record`） |
| **序列化特性** | 无特殊配置 |
| **说明** | 用户头像响应对象，用于 `/system/user/profile/avatar` 接口上传头像后返回头像 URL。定义在 `SysProfileController` 中作为内部 record |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| imgUrl | `imgUrl` | string | 否 | — | — | 头像图片地址（OSS 存储 URL） | `"https://oss.example.com/avatar/2026/07/14/xxx.png"` |

---

## JSON 示例

```json
{
  "imgUrl": "https://oss.example.com/avatar/2026/07/14/abc123.png"
}
```

---

*基于 `org.dromara.system.controller.system.SysProfileController.AvatarVo` 源码生成 * 2026-07-14*
