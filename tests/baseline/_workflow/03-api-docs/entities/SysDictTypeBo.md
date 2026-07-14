# SysDictTypeBo — 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysDictTypeBo` |
| **全限定名** | `org.dromara.system.domain.bo.SysDictTypeBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 系统管理 |
| **父类** | `BaseEntity` |
| **序列化特性** | 无特殊配置 |
| **说明** | 字典类型业务对象，用于字典类型的新增、修改、查询等操作的请求参数绑定 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| dictId | `dictId` | number | 否 | — | — | 字典主键（修改时必传） | `1` |
| dictName | `dictName` | string | 是 | `@NotBlank`, `@Size(min=0, max=100)` | — | 字典名称 | `"用户性别"` |
| dictType | `dictType` | string | 是 | `@NotBlank`, `@Size(min=0, max=100)`, `@Pattern(regexp="以字母开头，只能为小写字母、数字、下划线")` | — | 字典类型（唯一标识，缓存key） | `"sys_user_sex"` |
| remark | `remark` | string | 否 | — | — | 备注 | `"用户性别列表"` |
| createDept | `createDept` | number | 否 | — | 自动填充 | 创建部门（数据库自动填充） | `103` |
| createBy | `createBy` | number | 否 | — | 自动填充 | 创建者（数据库自动填充） | `1` |
| createTime | `createTime` | string | 否 | — | 自动填充 | 创建时间（格式: yyyy-MM-dd HH:mm:ss） | `"2024-01-15 10:30:00"` |
| updateBy | `updateBy` | number | 否 | — | 自动填充 | 更新者（数据库自动填充） | `1` |
| updateTime | `updateTime` | string | 否 | — | 自动填充 | 更新时间（格式: yyyy-MM-dd HH:mm:ss） | `"2024-06-20 14:00:00"` |
| params | `params` | object | 否 | — | `{}` | 请求参数（扩展查询条件，非空时才序列化，不映射数据库字段） | `{"beginTime":"2024-01-01","endTime":"2024-12-31"}` |

**字段备注**:
- `searchValue` (继承自 `BaseEntity`): `@JsonIgnore` 标记，不参与序列化，不映射数据库字段，仅用于前端搜索框传值。
- `dictType`: 必须符合字典类型格式规范 —— 以字母开头，后续只能包含小写字母、数字和下划线，如 `sys_user_sex`。
- `createDept` / `createBy` / `createTime`: 继承自 `BaseEntity`，由 MyBatis-Plus 在 INSERT 时自动填充。
- `updateBy` / `updateTime`: 继承自 `BaseEntity`，由 MyBatis-Plus 在 INSERT 和 UPDATE 时自动填充。
- `params`: 继承自 `BaseEntity`，`@JsonInclude(NON_EMPTY)`，常用于传递 `beginTime`、`endTime` 等时间范围查询参数。

---

## JSON 示例

```json
{
  "dictName": "用户性别",
  "dictType": "sys_user_sex",
  "remark": "用户性别列表"
}
```

---

*基于 `org.dromara.system.domain.bo.SysDictTypeBo` 源码生成 · 2026-07-14*
