# 系统管理 -- 用户管理 + 个人中心 API 文档（增量）

> Controller: `SysUserController`, `SysProfileController` | Base URL: `http://localhost:8080` | Auth: Sa-Token JWT `Authorization: Bearer {token}` + `clientid: e5cd7e4891bf95d1d19206ce24a7b32e`

## 请求头

| 头名称 | 值 | 说明 |
|--------|-----|------|
| Content-Type | `application/json` | 请求体格式；文件上传使用 `multipart/form-data` |
| Authorization | `Bearer {token}` | Sa-Token JWT 令牌，登录后获取 |
| clientid | `e5cd7e4891bf95d1d19206ce24a7b32e` | 客户端 ID，与 Token 绑定 |

---

> 接口 1-4（用户列表、导出、导入、导入模板）未变更，参见基线文档 `02-系统管理-part1.md`。

---

### 5 获取当前用户信息 <span style="color:orange">**[修改]**</span>

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/system/user/getInfo` |
| **接口说明** | 获取当前登录用户的完整信息（基本信息、菜单权限、角色权限），用于前端初始化 |
| **认证方式** | 需要认证 |
| **权限要求** | 无 |
| **标签** | 用户管理, 查询 |
| **变更类型** | `modified` |

---

#### 变更说明

`SysPostVo` 新增 `address` 字段，`SysUserServiceImpl.getUserInfo()` 查询当前用户信息时，`UserInfoVo.user.roles` 中嵌套的岗位信息（若含）将通过 `SysPostVo` 间接影响。同时影响 `POST /auth/login` 响应（登录时构建 `LoginUser` 也包含岗位信息）。

---

#### 请求

**请求头**: [认证]

无请求参数。

---

#### 响应

##### 成功响应 -- HTTP 200

[UserInfoVo](../entities/UserInfoVo.md)

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "user": {
      "userId": 1,
      "userName": "admin",
      "nickName": "管理员",
      "deptName": "研发部",
      "roles": [{"roleId": 1, "roleName": "超级管理员"}]
    },
    "permissions": ["system:user:list", "system:user:add", "system:user:edit"],
    "roles": ["superadmin"]
  }
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 200 | 500 | 当前用户不存在（查询结果为空） | `"没有权限访问用户数据!"` |

---

#### 断言

| # | 层级 | 断言项 | 预期值 | 断言消息 |
|---|:---:|--------|--------|------|
| 1 | 协议层 | HTTP 状态码 | 200 | "HTTP状态码应为200" |
| 2 | 业务层 | code | 200 | "业务状态码应为200" |
| 3 | 业务层 | msg | "操作成功" | "提示消息应为'操作成功'" |
| 4 | 数据层 | data.user 存在性 | 存在 | "响应应包含user对象" |
| 5 | 数据层 | data.permissions 存在性 | 存在 | "响应应包含permissions数组" |
| 6 | 数据层 | data.roles 存在性 | 存在 | "响应应包含roles数组" |
| 7 | 数据层 | data.user.userId 存在性 | 存在 | "user应包含userId" |

---

### 6 根据用户编号获取详细信息 <span style="color:orange">**[修改]**</span>

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/system/user/{userId}` |
| **接口说明** | 根据用户ID获取用户的详细信息，包含关联的角色、岗位等，用于用户编辑页面的数据回填 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:user:query` |
| **标签** | 用户管理, 查询 |
| **变更类型** | `modified` |

---

#### 变更说明

`SysUserInfoVo.posts` 为 `List<SysPostVo>`，用户信息查询时岗位列表将包含 `address` 字段。

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `userId` | number | 否 | 用户ID（可选，不传时仅返回所有正常状态的角色列表） | `2` |

---

#### 响应

##### 成功响应 -- HTTP 200

[SysUserInfoVo](../entities/SysUserInfoVo.md)

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "user": {
      "userId": 2,
      "userName": "zhangsan",
      "nickName": "张三",
      "deptId": 103,
      "deptName": "研发部",
      "email": "z***@example.com",
      "phonenumber": "138****8001",
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
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | DTO 校验失败 -- `userId` 类型不匹配 | `"参数校验失败"` |
| 200 | 500 | 数据权限校验失败 -- 当前用户无该ID数据权限（非超管时） | `"没有权限访问用户数据！"` |

---

#### 断言

| # | 层级 | 断言项 | 预期值 | 断言消息 |
|---|:---:|--------|--------|------|
| 1 | 协议层 | HTTP 状态码 | 200 | "HTTP状态码应为200" |
| 2 | 业务层 | code | 200 | "业务状态码应为200" |
| 3 | 数据层 | data.posts[*].address 存在性 | 存在 | "岗位列表每项应包含address字段" |
| 4 | 数据层 | data.posts[*].address 类型 | String | "address字段类型应为String" |
| 5 | 数据层 | data.posts[*].address 值 | "LosAngeles" | "address字段值应为'LosAngeles'" |
| 6 | 数据层 | data.posts[*].postId 存在性 | 存在 | "原有字段postId应仍然存在" |
| 7 | 数据层 | data.posts[*].postName 存在性 | 存在 | "原有字段postName应仍然存在" |

---

#### 业务规则

| 规则编号 | 规则描述 |
|:---:|------|
| 1 | 非超级管理员用户在查询其他用户详情时，通过 `checkUserDataScope` 校验数据权限 |
| 2 | 角色列表仅返回状态正常的角色；若目标用户非超级管理员，过滤掉超级管理员角色 |

---

> 接口 7-18（新增用户、修改用户、删除用户、重置密码、修改状态、授权角色、部门树、个人中心）未变更，参见基线文档 `02-系统管理-part1.md`。

---

> 文档生成时间: 2026-07-14 | 变更接口数: 2 (用户信息查询) | 覆盖控制器: `SysUserController`
