# UserDTO -- 响应体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `UserDTO` |
| **全限定名** | `org.dromara.common.core.domain.dto.UserDTO` |
| **类型** | 响应体 DTO |
| **所属模块** | 工作流管理（定义在 common-core 公共模块，属于共享实体） |
| **父类** | 无（直接实现 Serializable） |
| **序列化特性** | 无特殊配置 |
| **说明** | 用户信息传输对象，用于流程任务中返回办理人/审批人的简要用户信息 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| userId | `userId` | number | 否 | -- | -- | 用户ID | `1002` |
| deptId | `deptId` | number | 否 | -- | -- | 部门ID | `103` |
| userName | `userName` | string | 否 | -- | -- | 用户账号 | `"lisi"` |
| nickName | `nickName` | string | 否 | -- | -- | 用户昵称 | `"李四"` |
| userType | `userType` | string | 否 | -- | -- | 用户类型（sys_user系统用户） | `"sys_user"` |
| email | `email` | string | 否 | -- | -- | 用户邮箱 | `"lisi@example.com"` |
| phonenumber | `phonenumber` | string | 否 | -- | -- | 手机号码 | `"13800138001"` |
| sex | `sex` | string | 否 | -- | -- | 用户性别（0男 1女 2未知） | `"0"` |
| status | `status` | string | 否 | -- | -- | 账号状态（0正常 1停用） | `"0"` |
| createTime | `createTime` | string | 否 | -- | -- | 创建时间 | `"2023-06-01 08:00:00"` |

**字段备注**:
- `sex`: 枚举值 `"0"`=男, `"1"`=女, `"2"`=未知
- `status`: 枚举值 `"0"`=正常, `"1"`=停用
- `userType`: 常见值为 `"sys_user"`（系统用户）
- 此实体为公共模块共享实体，被多个模块（如工作流管理、系统管理）共用

---

## JSON 示例

```json
{
  "userId": 1002,
  "deptId": 103,
  "userName": "lisi",
  "nickName": "李四",
  "userType": "sys_user",
  "email": "lisi@example.com",
  "phonenumber": "13800138001",
  "sex": "0",
  "status": "0",
  "createTime": "2023-06-01 08:00:00"
}
```

---

*基于 `org.dromara.common.core.domain.dto.UserDTO` 源码生成 . 2026-07-14*
