# 模块分析报告 — UMS (用户管理系统)

## 技术栈

- **后端**: Java Spring Boot 2.x + MyBatis-Plus
- **前端**: Vue 3 + TypeScript + Element Plus
- **数据库**: MySQL
- **认证**: JWT (Spring Security)
- **API 文档**: Swagger/OpenAPI

## 微服务

单服务架构，共 1 个服务。

| 服务名 | 端口 | 描述 |
|--------|------|------|
| mall-tiny | 8080 | 后台管理系统 |

## API 端点汇总

### UmsAdminController (/admin) — 后台用户管理 — 14 端点

| 方法 | 路径 | 描述 | 权限 |
|------|------|------|------|
| POST | /admin/register | 用户注册 | 无 (白名单) |
| POST | /admin/login | 登录获取Token | 无 (白名单) |
| GET | /admin/refreshToken | 刷新Token | 需要认证 |
| GET | /admin/info | 获取当前用户信息 | 无 (白名单) |
| POST | /admin/logout | 登出 | 无 (白名单) |
| GET | /admin/list | 分页获取用户列表 | 需要认证 |
| GET | /admin/{id} | 获取指定用户信息 | 需要认证 |
| POST | /admin/update/{id} | 修改指定用户信息 | 需要认证 |
| POST | /admin/updatePassword | 修改用户密码 | 需要认证 |
| POST | /admin/delete/{id} | 删除指定用户 | 需要认证 |
| POST | /admin/updateStatus/{id} | 修改帐号状态 | 需要认证 |
| POST | /admin/role/update | 给用户分配角色 | 需要认证 |
| GET | /admin/role/{adminId} | 获取用户角色列表 | 需要认证 |

### UmsRoleController (/role) — 后台角色管理 — 10 端点

| 方法 | 路径 | 描述 | 权限 |
|------|------|------|------|
| POST | /role/create | 添加角色 | 需要认证 |
| POST | /role/update/{id} | 修改角色 | 需要认证 |
| POST | /role/delete | 批量删除角色 | 需要认证 |
| GET | /role/listAll | 获取所有角色 | 需要认证 |
| GET | /role/list | 分页获取角色列表 | 需要认证 |
| POST | /role/updateStatus/{id} | 修改角色状态 | 需要认证 |
| GET | /role/listMenu/{roleId} | 获取角色相关菜单 | 需要认证 |
| GET | /role/listResource/{roleId} | 获取角色相关资源 | 需要认证 |
| POST | /role/allocMenu | 给角色分配菜单 | 需要认证 |
| POST | /role/allocResource | 给角色分配资源 | 需要认证 |

### UmsMenuController (/menu) — 后台菜单管理 — 7 端点

| 方法 | 路径 | 描述 | 权限 |
|------|------|------|------|
| POST | /menu/create | 添加后台菜单 | 需要认证 |
| POST | /menu/update/{id} | 修改后台菜单 | 需要认证 |
| GET | /menu/{id} | 根据ID获取菜单详情 | 需要认证 |
| POST | /menu/delete/{id} | 根据ID删除后台菜单 | 需要认证 |
| GET | /menu/list/{parentId} | 分页查询后台菜单 | 需要认证 |
| GET | /menu/treeList | 树形结构返回所有菜单 | 需要认证 |
| POST | /menu/updateHidden/{id} | 修改菜单显示状态 | 需要认证 |

### UmsResourceController (/resource) — 后台资源管理 — 6 端点

| 方法 | 路径 | 描述 | 权限 |
|------|------|------|------|
| POST | /resource/create | 添加后台资源 | 需要认证 |
| POST | /resource/update/{id} | 修改后台资源 | 需要认证 |
| GET | /resource/{id} | 根据ID获取资源详情 | 需要认证 |
| POST | /resource/delete/{id} | 删除后台资源 | 需要认证 |
| GET | /resource/list | 分页模糊查询后台资源 | 需要认证 |
| GET | /resource/listAll | 查询所有后台资源 | 需要认证 |

### UmsResourceCategoryController (/resourceCategory) — 资源分类管理 — 4 端点

| 方法 | 路径 | 描述 | 权限 |
|------|------|------|------|
| GET | /resourceCategory/listAll | 查询所有资源分类 | 需要认证 |
| POST | /resourceCategory/create | 添加后台资源分类 | 需要认证 |
| POST | /resourceCategory/update/{id} | 修改后台资源分类 | 需要认证 |
| POST | /resourceCategory/delete/{id} | 删除后台资源分类 | 需要认证 |

**总计: 41 个 API 端点**

## 前端页面

| 路径 | 组件 | 描述 |
|------|------|------|
| /ums/admin | views/ums/admin.vue | 用户列表管理 |
| /ums/role | views/ums/role.vue | 角色管理 |
| /ums/menu | views/ums/menu.vue | 菜单管理 |
| /ums/resource | views/ums/resource.vue | 资源管理 |
| /login | views/login/index.vue | 登录页 |
| /dashboard | views/home/index.vue | 控制台 |

## 认证机制

- **类型**: JWT (JSON Web Token)
- **Token 请求头**: Authorization: Bearer {token}
- **Token 前缀**: Bearer
- **Token 有效期**: 604800 秒 (7 天)
- **登录接口**: POST /admin/login
- **白名单路径**: /admin/login, /admin/register, /admin/info, /admin/logout

## 错误处理机制

### ApiException 处理链

```
Asserts.fail(message) → throw new ApiException(message) [errorCode=null]
Asserts.fail(IErrorCode) → throw new ApiException(errorCode) [errorCode!=null]
        ↓
GlobalExceptionHandler.handle(ApiException e)
  ├── e.getErrorCode() != null → CommonResult.failed(e.getErrorCode()) → code=errorCode.getCode()
  └── e.getErrorCode() == null → CommonResult.failed(e.getMessage()) → code=500
```

### ResultCode 业务状态码

| ResultCode | code | message | 使用场景 |
|------------|------|---------|---------|
| SUCCESS | 200 | 操作成功 | 操作成功 |
| FAILED | 500 | 操作失败 | 通用失败 |
| VALIDATE_FAILED | 404 | 参数检验失败 | 参数校验失败 |
| UNAUTHORIZED | 401 | 暂未登录或token已经过期 | 未授权/Token无效 |
| FORBIDDEN | 403 | 没有相关权限 | 无权限 |

### 登录失败路径验证

- **密码错误**: Controller → Service.login() → passwordEncoder.matches()=false → Asserts.fail("密码不正确") → ApiException(message) [errorCode=null] → GlobalExceptionHandler → **code=500, message="密码不正确"**
- **帐号禁用**: Controller → Service.login() → userDetails.isEnabled()=false → Asserts.fail("帐号已被禁用") → ApiException(message) → GlobalExceptionHandler → **code=500, message="帐号已被禁用"**
- **用户不存在**: Controller → Service.login() → loadUserByUsername() throws UsernameNotFoundException → catch AuthenticationException → return null → Controller returns CommonResult.validateFailed("用户名或密码错误") → **code=404, message="用户名或密码错误"**

### 注册失败路径

- **重复用户名**: Controller → Service.register() → 查询存在同名用户 → return null → Controller returns CommonResult.failed() → **code=500, message="操作失败"**

### 修改密码失败路径

- **参数缺失**(username/oldPassword/newPassword 为空): Service returns -1 → Controller → **code=500, message="提交参数不合法"**
- **用户不存在**: Service returns -2 → Controller → **code=500, message="找不到该用户"**
- **旧密码错误**: Service returns -3 → Controller → **code=500, message="旧密码错误"**
