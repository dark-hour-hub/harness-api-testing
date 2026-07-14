# SysUserBo -- 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysUserBo` |
| **全限定名** | `org.dromara.system.domain.bo.SysUserBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 系统管理 |
| **父类** | `BaseEntity` |
| **序列化特性** | 无特殊配置（继承 BaseEntity，`params` 字段省略空值） |
| **说明** | 用户信息业务对象，用于用户新增、编辑、密码重置、状态变更、分页查询等接口的请求参数，对应数据库表 `sys_user` |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| searchValue | `searchValue` | string | 否 | — | — | 搜索值（不参与序列化 `@JsonIgnore`） | — |
| createDept | `createDept` | number | 否 | 插入时自动填充 | — | 创建部门 | `103` |
| createBy | `createBy` | number | 否 | 插入时自动填充 | — | 创建者 | `1` |
| createTime | `createTime` | string | 否 | 插入时自动填充 | — | 创建时间 | `"2026-07-14 10:00:00"` |
| updateBy | `updateBy` | number | 否 | 插入/更新时自动填充 | — | 更新者 | `1` |
| updateTime | `updateTime` | string | 否 | 插入/更新时自动填充 | — | 更新时间 | `"2026-07-14 12:00:00"` |
| params | `params` | object | 否 | — | `{}` | 请求参数（含 `beginTime`/`endTime` 等查询参数） | `{"beginTime":"2026-01-01"}` |
| userId | `userId` | number | 否 | — | — | 用户ID | `1` |
| deptId | `deptId` | number | 否 | — | — | 部门ID | `103` |
| userName | `userName` | string | ✅ | `@NotBlank`；`@Size(min=2, max=30)`；`@Xss`（防脚本注入） | — | 用户账号 | `"admin"` |
| nickName | `nickName` | string | ✅ | `@NotBlank`；`@Size(min=0, max=30)`；`@Xss`（防脚本注入） | — | 用户昵称 | `"管理员"` |
| userType | `userType` | string | 否 | — | — | 用户类型（`sys_user` 系统用户） | `"sys_user"` |
| email | `email` | string | 否 | `@Email`；`@Size(min=0, max=50)` | — | 用户邮箱 | `"admin@example.com"` |
| phonenumber | `phonenumber` | string | 否 | — | — | 手机号码 | `"13800138000"` |
| sex | `sex` | string | 否 | — | — | 用户性别（`0` 男、`1` 女、`2` 未知） | `"0"` |
| password | `password` | string | 否 | — | — | 密码（新增时传入明文，服务端加密存储） | `"Admin@123"` |
| status | `status` | string | 否 | — | — | 账号状态（`0` 正常、`1` 停用） | `"0"` |
| remark | `remark` | string | 否 | — | — | 备注 | `"超级管理员"` |
| roleIds | `roleIds` | array | 否 | `@Size(min=1)` | — | 角色组（Long 数组） | `[1, 2]` |
| postIds | `postIds` | array | 否 | — | — | 岗位组（Long 数组） | `[1]` |
| roleId | `roleId` | number | 否 | — | — | 数据权限 当前角色ID | `1` |
| userIds | `userIds` | string | 否 | — | — | 用户ID串（逗号分隔，用于批量查询） | `"1,2,3"` |
| excludeUserIds | `excludeUserIds` | string | 否 | — | — | 排除不查询的用户（工作流用，逗号分隔） | `"100"` |

---

## JSON 示例

```json
{
  "userName": "zhangsan",
  "nickName": "张三",
  "deptId": 103,
  "phonenumber": "13800138001",
  "email": "zhangsan@example.com",
  "sex": "0",
  "password": "Admin@123",
  "status": "0",
  "roleIds": [2],
  "postIds": [1],
  "remark": "测试用户"
}
```

---

*基于 `org.dromara.system.domain.bo.SysUserBo` 源码生成 * 2026-07-14*
