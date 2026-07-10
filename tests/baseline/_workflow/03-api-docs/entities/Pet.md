# Pet — 响应体 VO / 表单绑定对象

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `Pet` |
| **全限定名** | `org.springframework.samples.petclinic.owner.Pet` |
| **类型** | 响应体 VO / 请求体 DTO（JPA 实体复用，同时用于 Thymeleaf 表单绑定和视图渲染） |
| **所属模块** | 客户管理 |
| **父类** | `NamedEntity` → `BaseEntity` |
| **序列化特性** | Jackson 默认（基于 getter 发现属性） |
| **说明** | 宠物实体，映射 `pets` 表。通过 `type_id` 外键关联宠物类型，通过 `owner_id` 外键归属客户。由 PetValidator 进行自定义校验。 |

---

## 字段定义

### 实体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | Integer | 否 | 数据库自增主键（`@GeneratedValue(IDENTITY)`） | `null`（新建时） | 宠物ID（继承自 BaseEntity） | `1` |
| name | `name` | String | ✅ | `@NotBlank` | — | 宠物名称（继承自 NamedEntity） | `"Leo"` |
| birthDate | `birthDate` | LocalDate | 否 | `@DateTimeFormat(pattern="yyyy-MM-dd")` | — | 宠物生日 | `"2010-09-07"` |
| type | `type` | PetType | 否 | `@ManyToOne`, `@JoinColumn(name="type_id")` | — | 宠物类型（关联 `types` 表） | `{"id":1,"name":"cat"}` |
| type.id | `id` | Integer | 否 | 数据库自增主键 | `null` | 类型ID | `1` |
| type.name | `name` | String | ✅ | `@NotBlank` | — | 类型名称 | `"cat"` |
| visits | `visits` | Array\<Visit\> | 否 | `@OneToMany(cascade=ALL, fetch=EAGER)`, `@OrderBy("date ASC")` | `[]`（空集合时） | 就诊记录列表（按日期升序） | `[{"id":1,"date":"2013-01-01","description":"rabies shot"}]` |
| visits[].id | `id` | Integer | 否 | 数据库自增主键 | `null` | 就诊记录ID | `1` |
| visits[].date | `date` | LocalDate | 否 | `@DateTimeFormat(pattern="yyyy-MM-dd")`, 列名 `visit_date` | 明天（`LocalDate.now().plusDays(1)`） | 就诊日期 | `"2013-01-01"` |
| visits[].description | `description` | String | ✅ | `@NotBlank` | — | 就诊描述 | `"rabies shot"` |

**字段备注**:
- `birthDate`: 使用 `@DateTimeFormat` 指定 Thymeleaf 表单绑定格式。Jackson 默认将 `LocalDate` 序列化为 ISO-8601 字符串。
- `type`: 必需字段（PetValidator 会校验），在新增/编辑宠物表单中通过下拉选择。
- `visits`: `cascade=ALL` 级联持久化，`OrderBy("date ASC")` 按就诊日期升序排列。

---

## JSON 示例

```json
{
  "id": 1,
  "name": "Leo",
  "birthDate": "2010-09-07",
  "type": {
    "id": 1,
    "name": "cat"
  },
  "visits": [
    {
      "id": 1,
      "date": "2013-01-01",
      "description": "rabies shot"
    }
  ]
}
```

---

*基于 `org.springframework.samples.petclinic.owner.Pet` 源码生成 · 2026-07-10*
