# RouterVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `RouterVo` |
| **全限定名** | `org.dromara.system.domain.vo.RouterVo` |
| **类型** | 响应体 VO |
| **所属模块** | 系统管理 |
| **父类** | 无 |
| **序列化特性** | 类级 `@JsonInclude(NON_EMPTY)`（空字符串、空数组、null 值均不序列化） |
| **说明** | 路由配置信息视图对象，用于 `/getRouters` 接口返回前端 Vue Router 所需的路由配置。由 `SysMenuServiceImpl.buildMenus()` 方法动态构建 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| name | `name` | string | 否 | `@JsonInclude(NON_EMPTY)` | — | 路由名字（格式 `首字母大写路径 + 菜单ID`，如 `System1`） | `"System1"` |
| path | `path` | string | 否 | `@JsonInclude(NON_EMPTY)` | — | 路由地址 | `"/system"` |
| hidden | `hidden` | boolean | 否 | `@JsonInclude(NON_EMPTY)` | — | 是否隐藏路由（`true` 时侧边栏不显示） | `false` |
| redirect | `redirect` | string | 否 | `@JsonInclude(NON_EMPTY)` | — | 重定向地址（`noRedirect` 时面包屑不可点击） | `"noRedirect"` |
| component | `component` | string | 否 | `@JsonInclude(NON_EMPTY)` | — | 组件地址 | `"system/user/index"` |
| query | `query` | string | 否 | `@JsonInclude(NON_EMPTY)` | — | 路由参数（JSON 字符串，如 `{"id":1,"name":"ry"}`） | `"{\"id\":1}"` |
| alwaysShow | `alwaysShow` | boolean | 否 | `@JsonInclude(NON_EMPTY)` | — | 子路由超过1个时自动嵌套模式 | `true` |
| meta | `meta` | object | 否 | — | — | 路由元信息 `MetaVo` | `{"title":"系统管理","icon":"system"}` |
| children | `children` | array | 否 | `@JsonInclude(NON_EMPTY)` | — | 子路由列表 `List<RouterVo>` | `[{"name":"User1","path":"user",...}]` |

**字段备注**:
- 类级 `@JsonInclude(NON_EMPTY)`：所有空值字段在序列化时被省略，减少网络传输体积
- `name`: 由 `SysMenu.getRouteName()` + 菜单ID 拼接而成，用于 Vue Router 的命名路由
- `meta`: 嵌套 `MetaVo` 对象，包含标题、图标、缓存配置、内链地址等路由元信息

---

## JSON 示例

```json
{
  "name": "System1",
  "path": "/system",
  "hidden": false,
  "redirect": "noRedirect",
  "alwaysShow": true,
  "meta": {
    "title": "系统管理",
    "icon": "system",
    "noCache": false,
    "link": null
  },
  "children": [
    {
      "name": "User100",
      "path": "user",
      "hidden": false,
      "component": "system/user/index",
      "meta": {
        "title": "用户管理",
        "icon": "user",
        "noCache": false
      }
    }
  ]
}
```

---

*基于 `org.dromara.system.domain.vo.RouterVo` 源码生成 * 2026-07-14*
