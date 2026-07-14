# UserInfoVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `UserInfoVo` |
| **全限定名** | `org.dromara.system.domain.vo.UserInfoVo` |
| **类型** | 响应体 VO |
| **所属模块** | 系统管理 |
| **父类** | 无 |
| **序列化特性** | 无特殊配置 |
| **说明** | 登录用户信息视图对象，用于 `/system/user/getInfo` 接口返回当前登录用户的完整信息，包含用户基本信息、菜单权限集合和角色权限集合 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| user | `user` | object | 否 | — | — | 用户基本信息 `SysUserVo` | `{"userId":1,"userName":"admin"}` |
| permissions | `permissions` | array | 否 | — | — | 菜单权限集合 `Set<String>` | `["system:user:list","system:user:add"]` |
| roles | `roles` | array | 否 | — | — | 角色权限集合 `Set<String>` | `["admin","common"]` |

**字段备注**:
- `user`: 内嵌 `SysUserVo` 对象，包含完整的用户基本信息、部门、角色等。<span style="color:orange">**[间接变更]**</span> `user.roles[*]` 中的岗位信息将包含 `address` 字段（若 roles 中嵌套岗位数据）
- `permissions`: 当前用户拥有的一级菜单权限标识集合，用于前端路由/按钮权限控制
- `roles`: 当前用户拥有的角色权限字符串集合，用于前端角色级权限控制

---

## JSON 示例

```json
{
  "user": {
    "userId": 1,
    "userName": "admin",
    "nickName": "管理员",
    "deptName": "研发部",
    "roles": [
      {"roleId": 1, "roleName": "超级管理员"}
    ]
  },
  "permissions": [
    "system:user:list",
    "system:user:add",
    "system:user:edit",
    "system:role:list"
  ],
  "roles": [
    "superadmin"
  ]
}
```

---

*基于 `org.dromara.system.domain.vo.UserInfoVo` 源码生成 * 2026-07-14*
