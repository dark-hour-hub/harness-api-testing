# SysRoleVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysRoleVo` |
| **全限定名** | `org.dromara.system.domain.vo.SysRoleVo` |
| **类型** | 响应体 VO |
| **所属模块** | 系统管理 |
| **父类** | 无（直接实现 `Serializable`） |
| **序列化特性** | 无特殊配置 |
| **说明** | 角色信息视图对象，用于角色列表、详情查询等接口的响应数据，同时支持 Excel 导出。对应数据库表 `sys_role` |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| roleId | `roleId` | number | 否 | — | — | 角色ID | `1` |
| roleName | `roleName` | string | 否 | — | — | 角色名称 | `"超级管理员"` |
| roleKey | `roleKey` | string | 否 | — | — | 角色权限字符串 | `"superadmin"` |
| roleSort | `roleSort` | number | 否 | — | — | 显示顺序 | `1` |
| dataScope | `dataScope` | string | 否 | — | — | 数据范围（`1` 全部数据权限、`2` 自定义数据权限、`3` 本部门数据权限、`4` 本部门及以下数据权限、`5` 仅本人数据权限、`6` 部门及以下或本人数据权限） | `"1"` |
| menuCheckStrictly | `menuCheckStrictly` | boolean | 否 | — | — | 菜单树选择项是否关联显示 | `true` |
| deptCheckStrictly | `deptCheckStrictly` | boolean | 否 | — | — | 部门树选择项是否关联显示 | `true` |
| status | `status` | string | 否 | — | — | 角色状态（`0` 正常、`1` 停用） | `"0"` |
| remark | `remark` | string | 否 | — | — | 备注 | `"超级管理员角色"` |
| createTime | `createTime` | string | 否 | — | — | 创建时间 | `"2025-01-01 10:00:00"` |
| flag | `flag` | boolean | 否 | — | `false` | 用户是否存在此角色标识（默认不存在） | `false` |

---

## JSON 示例

```json
{
  "roleId": 1,
  "roleName": "超级管理员",
  "roleKey": "superadmin",
  "roleSort": 1,
  "dataScope": "1",
  "menuCheckStrictly": true,
  "deptCheckStrictly": true,
  "status": "0",
  "remark": "超级管理员角色",
  "createTime": "2025-01-01 10:00:00",
  "flag": false
}
```

---

*基于 `org.dromara.system.domain.vo.SysRoleVo` 源码生成 * 2026-07-14*
