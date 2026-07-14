# SysConfigBo — 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysConfigBo` |
| **全限定名** | `org.dromara.system.domain.bo.SysConfigBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 系统管理 |
| **父类** | `BaseEntity` |
| **序列化特性** | 无特殊配置 |
| **说明** | 参数配置业务对象，用于系统参数配置的新增、修改、查询等操作的请求参数绑定 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| configId | `configId` | number | 否 | — | — | 参数主键（修改时必传） | `1` |
| configName | `configName` | string | 是 | `@NotBlank`, `@Size(min=0, max=100)` | — | 参数名称 | `"主框架页-默认皮肤样式名称"` |
| configKey | `configKey` | string | 是 | `@NotBlank`, `@Size(min=0, max=100)` | — | 参数键名（唯一标识，缓存key） | `"sys.index.skinName"` |
| configValue | `configValue` | string | 是 | `@NotBlank`, `@Size(min=0, max=500)` | — | 参数键值 | `"skin-blue"` |
| configType | `configType` | string | 否 | — | — | 系统内置标记（Y=内置不可删除, N=用户自定义） | `"Y"` |
| remark | `remark` | string | 否 | — | — | 备注 | `"蓝色皮肤"` |
| createDept | `createDept` | number | 否 | — | 自动填充 | 创建部门（数据库自动填充） | `103` |
| createBy | `createBy` | number | 否 | — | 自动填充 | 创建者（数据库自动填充） | `1` |
| createTime | `createTime` | string | 否 | — | 自动填充 | 创建时间（格式: yyyy-MM-dd HH:mm:ss） | `"2024-01-15 10:30:00"` |
| updateBy | `updateBy` | number | 否 | — | 自动填充 | 更新者（数据库自动填充） | `1` |
| updateTime | `updateTime` | string | 否 | — | 自动填充 | 更新时间（格式: yyyy-MM-dd HH:mm:ss） | `"2024-06-20 14:00:00"` |
| params | `params` | object | 否 | — | `{}` | 请求参数（扩展查询条件，非空时才序列化，不映射数据库字段） | `{"beginTime":"2024-01-01","endTime":"2024-12-31"}` |

**字段备注**:
- `searchValue` (继承自 `BaseEntity`): `@JsonIgnore` 标记，不参与序列化，不映射数据库字段，仅用于前端搜索框传值。
- `configKey`: 系统内唯一，新增/修改时后端会进行唯一性校验。也是缓存 key，修改后缓存自动更新。
- `configType`: Y=系统内置参数（不允许删除），N=用户自定义参数。
- `createDept` / `createBy` / `createTime`: 继承自 `BaseEntity`，由 MyBatis-Plus 在 INSERT 时自动填充。
- `updateBy` / `updateTime`: 继承自 `BaseEntity`，由 MyBatis-Plus 在 INSERT 和 UPDATE 时自动填充。
- `params`: 继承自 `BaseEntity`，`@JsonInclude(NON_EMPTY)`。

---

## JSON 示例

```json
{
  "configName": "主框架页-默认皮肤样式名称",
  "configKey": "sys.index.skinName",
  "configValue": "skin-blue",
  "configType": "Y",
  "remark": "蓝色皮肤"
}
```

---

*基于 `org.dromara.system.domain.bo.SysConfigBo` 源码生成 · 2026-07-14*
