# SysMenuBo -- 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysMenuBo` |
| **全限定名** | `org.dromara.system.domain.bo.SysMenuBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 系统管理 |
| **父类** | `BaseEntity` |
| **序列化特性** | `perms` 字段 `@JsonInclude(NON_NULL)`（省略 null 值） |
| **说明** | 菜单权限业务对象，用于菜单新增、编辑、查询等接口的请求参数，对应数据库表 `sys_menu` |

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
| params | `params` | object | 否 | — | `{}` | 请求参数 | — |
| menuId | `menuId` | number | 否 | — | — | 菜单ID | `1` |
| parentId | `parentId` | number | 否 | — | — | 父菜单ID（顶级菜单为 `0`） | `0` |
| menuName | `menuName` | string | ✅ | `@NotBlank`；`@Size(min=0, max=50)` | — | 菜单名称 | `"用户管理"` |
| orderNum | `orderNum` | number | ✅ | `@NotNull` | — | 显示顺序 | `1` |
| path | `path` | string | 否 | `@Size(min=0, max=200)` | — | 路由地址 | `"/system/user"` |
| component | `component` | string | 否 | `@Size(min=0, max=200)` | — | 组件路径 | `"system/user/index"` |
| queryParam | `queryParam` | string | 否 | `@JsonPattern(type=OBJECT)`（须为合法 JSON 对象格式） | — | 路由参数（JSON 字符串） | `"{\"id\": 1}"` |
| isFrame | `isFrame` | string | 否 | — | — | 是否为外链（`0` 是、`1` 否） | `"1"` |
| isCache | `isCache` | string | 否 | — | — | 是否缓存（`0` 缓存、`1` 不缓存） | `"0"` |
| menuType | `menuType` | string | ✅ | `@NotBlank` | — | 菜单类型（`M` 目录、`C` 菜单、`F` 按钮） | `"C"` |
| visible | `visible` | string | 否 | — | — | 显示状态（`0` 显示、`1` 隐藏） | `"0"` |
| status | `status` | string | 否 | — | — | 菜单状态（`0` 正常、`1` 停用） | `"0"` |
| perms | `perms` | string | 否 | `@Size(min=0, max=100)`；`@Pattern(regexp=RegexConstants.PERMISSION_STRING)`；`@JsonInclude(NON_NULL)` | — | 权限标识（格式 `tool:build:list`），为 null 时不序列化 | `"system:user:list"` |
| icon | `icon` | string | 否 | — | — | 菜单图标 | `"user"` |
| remark | `remark` | string | 否 | — | — | 备注 | `"用户管理菜单"` |

**字段备注**:
- `queryParam`: `@JsonPattern(type = JsonType.OBJECT)` 要求路由参数必须符合 JSON 对象格式
- `perms`: `@Pattern(regexp = RegexConstants.PERMISSION_STRING)` 要求权限标识符合 `tool:build:list` 格式（三段式冒号分隔）；`@JsonInclude(NON_NULL)` 为 null 时从 JSON 中省略

---

## JSON 示例

```json
{
  "parentId": 0,
  "menuName": "用户管理",
  "orderNum": 1,
  "path": "/system/user",
  "component": "system/user/index",
  "isFrame": "1",
  "isCache": "0",
  "menuType": "C",
  "visible": "0",
  "status": "0",
  "perms": "system:user:list",
  "icon": "user",
  "remark": "用户管理菜单"
}
```

---

*基于 `org.dromara.system.domain.bo.SysMenuBo` 源码生成 * 2026-07-14*
