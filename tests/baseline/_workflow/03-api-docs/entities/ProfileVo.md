# ProfileVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `ProfileVo` |
| **全限定名** | `org.dromara.system.controller.system.SysProfileController.ProfileVo` |
| **类型** | 响应体 VO（Java `record`） |
| **所属模块** | 系统管理 |
| **父类** | 无（`java.lang.Record`） |
| **序列化特性** | 无特殊配置 |
| **说明** | 用户个人信息视图对象，用于 `/system/user/profile` 接口返回个人中心信息。包含用户详情（`ProfileUserVo`，未经脱敏处理）、所属角色组名称和岗位组名称。定义在 `SysProfileController` 中作为内部 record |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| user | `user` | object | 否 | — | — | 用户信息 `ProfileUserVo`（未经脱敏，用于个人中心展示） | `{"userId":1,"userName":"admin"}` |
| roleGroup | `roleGroup` | string | 否 | — | — | 用户所属角色组（逗号分隔的角色名称） | `"超级管理员,普通角色"` |
| postGroup | `postGroup` | string | 否 | — | — | 用户所属岗位组（逗号分隔的岗位名称） | `"董事长,项目经理"` |

**字段备注**:
- `user`: 内嵌 `ProfileUserVo` 对象，与 `SysUserVo` 的区别是不包含脱敏注解，因此邮箱和手机号以明文返回，适合个人中心页面展示
- `roleGroup` / `postGroup`: 由服务层 `selectUserRoleGroup` / `selectUserPostGroup` 查询，逗号分隔多值

---

## JSON 示例

```json
{
  "user": {
    "userId": 1,
    "userName": "admin",
    "nickName": "管理员",
    "deptName": "研发部",
    "email": "admin@example.com",
    "phonenumber": "13800138000",
    "sex": "0",
    "avatar": 123,
    "loginIp": "192.168.1.1",
    "loginDate": "2026-07-14 08:30:00"
  },
  "roleGroup": "超级管理员",
  "postGroup": "董事长"
}
```

---

*基于 `org.dromara.system.controller.system.SysProfileController.ProfileVo` 源码生成 * 2026-07-14*
