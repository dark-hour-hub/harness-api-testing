# MenuTreeSelectVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `MenuTreeSelectVo` |
| **全限定名** | `org.dromara.system.controller.system.SysMenuController.MenuTreeSelectVo` |
| **类型** | 响应体 VO（Java `record`） |
| **所属模块** | 系统管理 |
| **父类** | 无（`java.lang.Record`） |
| **序列化特性** | 无特殊配置 |
| **说明** | 菜单树选择视图对象，用于 `/system/menu/roleMenuTreeselect/{roleId}` 和 `/system/menu/tenantPackageMenuTreeselect/{packageId}` 接口返回菜单树结构和已选中菜单ID列表。定义在 `SysMenuController` 中作为内部 record |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| checkedKeys | `checkedKeys` | array | 否 | — | — | 已选中的菜单ID列表 `List<Long>` | `[1, 2, 3, 100, 101]` |
| menus | `menus` | array | 否 | — | — | 菜单树结构列表 `List<Tree<Long>>`（使用 Hutool Tree，节点 key 为 `label`） | `[{"id":1,"label":"系统管理","children":[...]}]` |

**字段备注**:
- `checkedKeys`: 对应角色/套餐已分配的菜单ID列表，前端用于回显树选中状态
- `menus`: 使用 Hutool `TreeUtil` 构建的树形结构，节点 `id` 为 Long 类型菜单ID，`label` 为菜单名称（由 `TreeBuildUtils.DEFAULT_CONFIG` 配置 `nameKey="label"`），含 `children` 子节点

---

## JSON 示例

```json
{
  "checkedKeys": [1, 2, 3, 100, 101],
  "menus": [
    {
      "id": 1,
      "label": "系统管理",
      "children": [
        {
          "id": 100,
          "label": "用户管理",
          "children": []
        },
        {
          "id": 101,
          "label": "角色管理",
          "children": []
        }
      ]
    }
  ]
}
```

---

*基于 `org.dromara.system.controller.system.SysMenuController.MenuTreeSelectVo` 源码生成 * 2026-07-14*
