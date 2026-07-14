# SysUserVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysUserVo` |
| **全限定名** | `org.dromara.system.domain.vo.SysUserVo` |
| **类型** | 响应体 VO |
| **所属模块** | 系统管理 |
| **父类** | 无（直接实现 `Serializable`） |
| **序列化特性** | `password` 字段 `@JsonIgnore`（序列化时忽略）+ `@JsonProperty`（允许反序列化） |
| **说明** | 用户信息视图对象，用于用户列表、详情、信息查询等接口的响应数据，对应数据库表 `sys_user` |

---

## 注解转义说明

> 仅列出 Java 字段名与 JSON 键名不一致、或有额外显示名注解的字段。若所有字段均无转义，删除此段。

| Java 字段名 | JSON 键名 | 显示名 | 转义来源 |
|------------|----------|--------|----------|
| `password` | `password` | — | `@JsonIgnore`（序列化忽略）、`@JsonProperty`（反序列化保留） |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| userId | `userId` | number | 否 | — | — | 用户ID | `1` |
| tenantId | `tenantId` | string | 否 | — | — | 租户ID | `"000000"` |
| deptId | `deptId` | number | 否 | — | — | 部门ID | `103` |
| userName | `userName` | string | 否 | — | — | 用户账号 | `"admin"` |
| nickName | `nickName` | string | 否 | — | — | 用户昵称 | `"管理员"` |
| userType | `userType` | string | 否 | — | — | 用户类型（`sys_user` 系统用户） | `"sys_user"` |
| email | `email` | string | 否 | 脱敏条件 `@Sensitive(strategy=EMAIL, perms="system:user:edit")` | — | 用户邮箱（无 `system:user:edit` 权限时脱敏显示） | `"a***@example.com"` |
| phonenumber | `phonenumber` | string | 否 | 脱敏条件 `@Sensitive(strategy=PHONE, perms="system:user:edit")` | — | 手机号码（无 `system:user:edit` 权限时脱敏显示） | `"138****8001"` |
| sex | `sex` | string | 否 | — | — | 用户性别（`0` 男、`1` 女、`2` 未知） | `"0"` |
| avatar | `avatar` | number | 否 | `@Translation(type=OSS_ID_TO_URL)` | — | 头像地址（OSS 文件ID，经翻译注解转为 URL） | `123` |
| password | `password` | string | 否 | `@JsonIgnore`（序列化忽略） | — | 密码（不参与序列化，仅反序列化时使用） | — |
| status | `status` | string | 否 | — | — | 账号状态（`0` 正常、`1` 停用） | `"0"` |
| loginIp | `loginIp` | string | 否 | — | — | 最后登录IP | `"192.168.1.1"` |
| loginDate | `loginDate` | string | 否 | — | — | 最后登录时间 | `"2026-07-14 08:30:00"` |
| remark | `remark` | string | 否 | — | — | 备注 | `"超级管理员"` |
| createTime | `createTime` | string | 否 | — | — | 创建时间 | `"2025-01-01 10:00:00"` |
| deptName | `deptName` | string | 否 | `@Translation(type=DEPT_ID_TO_NAME, mapper="deptId")` | — | 部门名（经由 `deptId` 翻译为部门名称） | `"研发部"` |
| roles | `roles` | array | 否 | — | — | 角色对象列表 `List<SysRoleVo>` | `[{"roleId":1,"roleName":"超级管理员"}]` |
| roleIds | `roleIds` | array | 否 | — | — | 角色组（Long 数组） | `[1, 2]` |
| postIds | `postIds` | array | 否 | — | — | 岗位组（Long 数组） | `[1]` |
| roleId | `roleId` | number | 否 | — | — | 数据权限 当前角色ID | `1` |

**字段备注**:
- `password`: 标注 `@JsonIgnore` + `@JsonProperty`，序列化时被忽略（响应中不包含），反序列化时可接收
- `email` / `phonenumber`: 标注 `@Sensitive`，根据当前用户权限决定是否脱敏。拥有 `system:user:edit` 权限则明文返回，否则分别按 EMAIL / PHONE 策略脱敏
- `avatar`: 标注 `@Translation(type = OSS_ID_TO_URL)`，存储的是 OSS 文件 ID，响应时翻译为完整 URL
- `deptName`: 标注 `@Translation(type = DEPT_ID_TO_NAME, mapper = "deptId")`，通过 `deptId` 字段值翻译为部门名称
- `roles`: 嵌套 `SysRoleVo` 对象列表，由服务层额外填充

---

## JSON 示例

```json
{
  "userId": 1,
  "tenantId": "000000",
  "deptId": 103,
  "userName": "admin",
  "nickName": "管理员",
  "userType": "sys_user",
  "email": "a***@example.com",
  "phonenumber": "138****8001",
  "sex": "0",
  "avatar": 123,
  "status": "0",
  "loginIp": "192.168.1.1",
  "loginDate": "2026-07-14 08:30:00",
  "remark": "超级管理员",
  "createTime": "2025-01-01 10:00:00",
  "deptName": "研发部",
  "roles": [
    {
      "roleId": 1,
      "roleName": "超级管理员",
      "roleKey": "superadmin",
      "status": "0"
    }
  ],
  "roleIds": [1],
  "postIds": [1],
  "roleId": 1
}
```

---

*基于 `org.dromara.system.domain.vo.SysUserVo` 源码生成 * 2026-07-14*
