# SysPostBo — 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysPostBo` |
| **全限定名** | `org.dromara.system.domain.bo.SysPostBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 系统管理 |
| **父类** | `BaseEntity` |
| **序列化特性** | 无特殊配置 |
| **说明** | 岗位信息业务对象，用于岗位的新增、修改、查询等操作的请求参数绑定 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| postId | `postId` | number | 否 | — | — | 岗位ID（修改时必传） | `1` |
| deptId | `deptId` | number | 是 | `@NotNull` | — | 部门id（单部门） | `103` |
| belongDeptId | `belongDeptId` | number | 否 | — | — | 归属部门id（部门树搜索用） | `100` |
| postCode | `postCode` | string | 是 | `@NotBlank`, `@Size(min=0, max=64)` | — | 岗位编码 | `"ceo"` |
| postName | `postName` | string | 是 | `@NotBlank`, `@Size(min=0, max=50)` | — | 岗位名称 | `"董事长"` |
| postCategory | `postCategory` | string | 否 | `@Size(min=0, max=100)` | — | 岗位类别编码 | `"manager"` |
| postSort | `postSort` | number | 是 | `@NotNull` | — | 显示顺序（数值越小越靠前） | `1` |
| status | `status` | string | 否 | — | — | 状态（0=正常, 1=停用） | `"0"` |
| remark | `remark` | string | 否 | — | — | 备注 | `"最高管理层岗位"` |
| createDept | `createDept` | number | 否 | — | 自动填充 | 创建部门（数据库自动填充） | `103` |
| createBy | `createBy` | number | 否 | — | 自动填充 | 创建者（数据库自动填充） | `1` |
| createTime | `createTime` | string | 否 | — | 自动填充 | 创建时间（格式: yyyy-MM-dd HH:mm:ss） | `"2024-01-15 10:30:00"` |
| updateBy | `updateBy` | number | 否 | — | 自动填充 | 更新者（数据库自动填充） | `1` |
| updateTime | `updateTime` | string | 否 | — | 自动填充 | 更新时间（格式: yyyy-MM-dd HH:mm:ss） | `"2024-06-20 14:00:00"` |
| params | `params` | object | 否 | — | `{}` | 请求参数（扩展查询条件，非空时才序列化，不映射数据库字段） | `{"beginTime":"2024-01-01","endTime":"2024-12-31"}` |

**字段备注**:
- `searchValue` (继承自 `BaseEntity`): `@JsonIgnore` 标记，不参与序列化，不映射数据库字段，仅用于前端搜索框传值。
- `createDept` / `createBy` / `createTime`: 继承自 `BaseEntity`，由 MyBatis-Plus 在 INSERT 时自动填充，一般无需手动传入。
- `updateBy` / `updateTime`: 继承自 `BaseEntity`，由 MyBatis-Plus 在 INSERT 和 UPDATE 时自动填充。
- `params`: 继承自 `BaseEntity`，`@JsonInclude(NON_EMPTY)`，非空时才出现在 JSON 中，常用于传递 `beginTime`、`endTime` 等扩展查询参数。

---

## JSON 示例

```json
{
  "deptId": 103,
  "postCode": "ceo",
  "postName": "董事长",
  "postCategory": "manager",
  "postSort": 1,
  "status": "0",
  "remark": "最高管理层岗位"
}
```

---

*基于 `org.dromara.system.domain.bo.SysPostBo` 源码生成 · 2026-07-14*
