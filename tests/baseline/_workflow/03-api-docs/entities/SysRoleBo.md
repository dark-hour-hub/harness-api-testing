# SysRoleBo -- 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysRoleBo` |
| **全限定名** | `org.dromara.system.domain.bo.SysRoleBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 系统管理 |
| **父类** | `BaseEntity` |
| **序列化特性** | 无特殊配置（继承 BaseEntity） |
| **说明** | 角色信息业务对象，用于角色新增、编辑、分页查询、状态变更等接口的请求参数，对应数据库表 `sys_role` |

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
| roleId | `roleId` | number | 否 | — | — | 角色ID | `1` |
| roleName | `roleName` | string | ✅ | `@NotBlank`；`@Size(min=0, max=30)` | — | 角色名称 | `"管理员"` |
| roleKey | `roleKey` | string | ✅ | `@NotBlank`；`@Size(min=0, max=100)` | — | 角色权限字符串 | `"admin"` |
| roleSort | `roleSort` | number | ✅ | `@NotNull` | — | 显示顺序 | `1` |
| dataScope | `dataScope` | string | 否 | — | — | 数据范围（`1` 全部数据权限、`2` 自定数据权限、`3` 本部门数据权限、`4` 本部门及以下数据权限、`5` 仅本人数据权限、`6` 部门及以下或本人数据权限） | `"1"` |
| menuCheckStrictly | `menuCheckStrictly` | boolean | 否 | — | — | 菜单树选择项是否关联显示 | `true` |
| deptCheckStrictly | `deptCheckStrictly` | boolean | 否 | — | — | 部门树选择项是否关联显示 | `true` |
| status | `status` | string | 否 | — | — | 角色状态（`0` 正常、`1` 停用） | `"0"` |
| remark | `remark` | string | 否 | — | — | 备注 | `"系统管理员角色"` |
| menuIds | `menuIds` | array | 否 | — | — | 菜单组（Long 数组，角色关联的菜单ID列表） | `[1, 2, 3]` |
| deptIds | `deptIds` | array | 否 | — | — | 部门组（Long 数组，数据权限关联的部门ID列表） | `[100, 101]` |

---

## JSON 示例

```json
{
  "roleName": "测试角色",
  "roleKey": "test",
  "roleSort": 2,
  "dataScope": "5",
  "menuCheckStrictly": false,
  "deptCheckStrictly": false,
  "status": "0",
  "menuIds": [1, 2, 3],
  "deptIds": [100],
  "remark": "测试用角色"
}
```

---

*基于 `org.dromara.system.domain.bo.SysRoleBo` 源码生成 * 2026-07-14*
