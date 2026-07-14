# SysUserInfoVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysUserInfoVo` |
| **全限定名** | `org.dromara.system.domain.vo.SysUserInfoVo` |
| **类型** | 响应体 VO |
| **所属模块** | 系统管理 |
| **父类** | 无 |
| **序列化特性** | 无特殊配置 |
| **说明** | 用户详情信息视图对象，用于 `/system/user/{userId}` 接口返回指定用户的详细信息，包含用户基本信息、角色列表、岗位列表等关联数据 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| user | `user` | object | 否 | — | — | 用户基本信息 `SysUserVo` | `{"userId":1,"userName":"admin"}` |
| roleIds | `roleIds` | array | 否 | — | — | 角色ID列表 `List<Long>` | `[1, 2]` |
| roles | `roles` | array | 否 | — | — | 角色列表 `List<SysRoleVo>`（所有正常状态角色） | `[{"roleId":1,"roleName":"超级管理员"}]` |
| postIds | `postIds` | array | 否 | — | — | 岗位ID列表 `List<Long>` | `[1]` |
| posts | `posts` | array | 否 | — | — | 岗位列表 `List<SysPostVo>` | `[{"postId":1,"postName":"董事长"}]` |

**字段备注**:
- `user`: 内嵌 `SysUserVo`，当前查询用户的详细信息
- `roleIds`: 当前用户已分配的角色ID列表
- `roles`: 系统中所有状态正常的角色列表（非超级管理员时过滤掉超级管理员角色），用于前端下拉选择
- `postIds`: 当前用户已分配的岗位ID列表
- `posts`: 用户所属部门下的岗位列表，用于前端下拉选择；<span style="color:orange">**[间接变更]**</span> `SysPostVo` 新增 `address` 字段，`posts[*].address` 将出现在响应中

---

## JSON 示例

```json
{
  "user": {
    "userId": 2,
    "userName": "zhangsan",
    "nickName": "张三",
    "deptId": 103,
    "deptName": "研发部",
    "email": "zhangsan@example.com",
    "phonenumber": "13800138001",
    "sex": "0",
    "status": "0"
  },
  "roleIds": [2],
  "roles": [
    {"roleId": 2, "roleName": "普通角色", "roleKey": "common", "status": "0"}
  ],
  "postIds": [2],
  "posts": [
    {"postId": 2, "postName": "项目经理", "address": "LosAngeles"}
  ]
}
```

---

*基于 `org.dromara.system.domain.vo.SysUserInfoVo` 源码生成 * 2026-07-14*
