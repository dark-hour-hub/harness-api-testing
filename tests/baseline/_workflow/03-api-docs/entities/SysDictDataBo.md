# SysDictDataBo — 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysDictDataBo` |
| **全限定名** | `org.dromara.system.domain.bo.SysDictDataBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 系统管理 |
| **父类** | `BaseEntity` |
| **序列化特性** | 无特殊配置 |
| **说明** | 字典数据业务对象，用于字典数据项的新增、修改、查询等操作的请求参数绑定 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| dictCode | `dictCode` | number | 否 | — | — | 字典编码（修改时必传） | `1` |
| dictSort | `dictSort` | number | 否 | — | — | 字典排序（数值越小越靠前） | `0` |
| dictLabel | `dictLabel` | string | 是 | `@NotBlank`, `@Size(min=0, max=100)` | — | 字典标签（前端展示用） | `"男"` |
| dictValue | `dictValue` | string | 是 | `@NotBlank`, `@Size(min=0, max=100)` | — | 字典键值（后端存储用，同类型下唯一） | `"0"` |
| dictType | `dictType` | string | 是 | `@NotBlank`, `@Size(min=0, max=100)` | — | 字典类型（关联 `sys_dict_type.dict_type`） | `"sys_user_sex"` |
| cssClass | `cssClass` | string | 否 | `@Size(min=0, max=100)` | — | 样式属性（其他样式扩展，如 `"primary"`） | `""` |
| listClass | `listClass` | string | 否 | — | — | 表格回显样式（如 `"default"`, `"success"`） | `"success"` |
| isDefault | `isDefault` | string | 否 | — | — | 是否默认值（Y=是, N=否） | `"N"` |
| createDept | `createDept` | number | 否 | — | — | 创建部门 | `103` |
| remark | `remark` | string | 否 | — | — | 备注 | `"性别男"` |
| searchValue | `searchValue` | string | 否 | — | — | 搜索值（`@JsonIgnore`，不参与序列化，不映射数据库） | `"男"` |
| createBy | `createBy` | number | 否 | — | 自动填充 | 创建者（数据库自动填充） | `1` |
| createTime | `createTime` | string | 否 | — | 自动填充 | 创建时间（格式: yyyy-MM-dd HH:mm:ss） | `"2024-01-15 10:30:00"` |
| updateBy | `updateBy` | number | 否 | — | 自动填充 | 更新者（数据库自动填充） | `1` |
| updateTime | `updateTime` | string | 否 | — | 自动填充 | 更新时间（格式: yyyy-MM-dd HH:mm:ss） | `"2024-06-20 14:00:00"` |
| params | `params` | object | 否 | — | `{}` | 请求参数（扩展查询条件，非空时才序列化，不映射数据库字段） | `{}` |

**字段备注**:
- `searchValue` (继承自 `BaseEntity`): `@JsonIgnore` 标记，不参与序列化，不映射数据库字段，仅用于前端搜索框传值。
- `createDept` (子类覆盖): 本类中直接声明了 `createDept` 字段，无 `@TableField` 自动填充，需手动传入。
- `createBy` / `createTime`: 继承自 `BaseEntity`，由 MyBatis-Plus 在 INSERT 时自动填充。
- `updateBy` / `updateTime`: 继承自 `BaseEntity`，由 MyBatis-Plus 在 INSERT 和 UPDATE 时自动填充。
- `params`: 继承自 `BaseEntity`，`@JsonInclude(NON_EMPTY)`。
- `dictValue`: 同类型字典下必须唯一，新增/修改时后端会进行唯一性校验。

---

## JSON 示例

```json
{
  "dictSort": 0,
  "dictLabel": "男",
  "dictValue": "0",
  "dictType": "sys_user_sex",
  "cssClass": "",
  "listClass": "success",
  "isDefault": "N",
  "remark": "性别男"
}
```

---

*基于 `org.dromara.system.domain.bo.SysDictDataBo` 源码生成 · 2026-07-14*
