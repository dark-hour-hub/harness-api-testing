# SysMenuVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysMenuVo` |
| **全限定名** | `org.dromara.system.domain.vo.SysMenuVo` |
| **类型** | 响应体 VO |
| **所属模块** | 系统管理 |
| **父类** | 无（直接实现 `Serializable`） |
| **序列化特性** | 无特殊配置 |
| **说明** | 菜单权限视图对象，用于菜单列表查询等接口的响应数据，支持树形结构（通过 `children` 字段递归）。对应数据库表 `sys_menu` |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| menuId | `menuId` | number | 否 | — | — | 菜单ID | `1` |
| menuName | `menuName` | string | 否 | — | — | 菜单名称 | `"系统管理"` |
| parentId | `parentId` | number | 否 | — | — | 父菜单ID（顶级为 `0`） | `0` |
| orderNum | `orderNum` | number | 否 | — | — | 显示顺序 | `1` |
| path | `path` | string | 否 | — | — | 路由地址 | `"/system"` |
| component | `component` | string | 否 | — | — | 组件路径 | `""` |
| queryParam | `queryParam` | string | 否 | — | — | 路由参数 | `""` |
| isFrame | `isFrame` | string | 否 | — | — | 是否为外链（`0` 是、`1` 否） | `"1"` |
| isCache | `isCache` | string | 否 | — | — | 是否缓存（`0` 缓存、`1` 不缓存） | `"0"` |
| menuType | `menuType` | string | 否 | — | — | 菜单类型（`M` 目录、`C` 菜单、`F` 按钮） | `"M"` |
| visible | `visible` | string | 否 | — | — | 显示状态（`0` 显示、`1` 隐藏） | `"0"` |
| status | `status` | string | 否 | — | — | 菜单状态（`0` 正常、`1` 停用） | `"0"` |
| perms | `perms` | string | 否 | — | — | 权限标识 | `"system:user:list"` |
| icon | `icon` | string | 否 | — | — | 菜单图标 | `"system"` |
| createDept | `createDept` | number | 否 | — | — | 创建部门 | `103` |
| remark | `remark` | string | 否 | — | — | 备注 | `"系统管理目录"` |
| createTime | `createTime` | string | 否 | — | — | 创建时间 | `"2025-01-01 10:00:00"` |
| children | `children` | array | 否 | — | `[]` | 子菜单列表 `List<SysMenuVo>`（递归结构） | `[{"menuId":100,"menuName":"用户管理"}]` |

**字段备注**:
- `children`: 递归嵌套 `SysMenuVo` 列表，构成菜单树形结构。默认初始化为 `new ArrayList<>()`

---

## JSON 示例

```json
{
  "menuId": 1,
  "menuName": "系统管理",
  "parentId": 0,
  "orderNum": 1,
  "path": "/system",
  "component": "",
  "queryParam": "",
  "isFrame": "1",
  "isCache": "0",
  "menuType": "M",
  "visible": "0",
  "status": "0",
  "perms": "",
  "icon": "system",
  "createDept": 103,
  "remark": "系统管理目录",
  "createTime": "2025-01-01 10:00:00",
  "children": [
    {
      "menuId": 100,
      "menuName": "用户管理",
      "parentId": 1,
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
      "children": []
    }
  ]
}
```

---

*基于 `org.dromara.system.domain.vo.SysMenuVo` 源码生成 * 2026-07-14*
