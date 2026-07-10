# Owner — 响应体 VO / 表单绑定对象

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `Owner` |
| **全限定名** | `org.springframework.samples.petclinic.owner.Owner` |
| **类型** | 响应体 VO / 请求体 DTO（JPA 实体复用，同时用于 Thymeleaf 表单绑定和视图渲染） |
| **所属模块** | 客户管理 |
| **父类** | `Person` → `BaseEntity` |
| **序列化特性** | Jackson 默认（基于 getter 发现属性），但该项目主要通过 Thymeleaf 渲染 HTML，仅在 `/vets` 接口返回 JSON。Owner 不直接以 JSON 形式返回。 |
| **说明** | 宠物主人实体，映射 `owners` 表。用于客户 CRUD 接口的表单绑定（`@ModelAttribute`）和视图渲染。 |

---

## 字段定义

### 实体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | Integer | 否 | 数据库自增主键（`@GeneratedValue(IDENTITY)`） | `null`（新建时） | 客户ID（继承自 BaseEntity） | `1` |
| firstName | `firstName` | String | ✅ | `@NotBlank`, `@Size(max=30)`, `@Column(length=30)` | — | 名字（继承自 Person） | `"George"` |
| lastName | `lastName` | String | ✅ | `@NotBlank`, `@Size(max=30)`, `@Column(length=30)` | — | 姓氏（继承自 Person） | `"Franklin"` |
| address | `address` | String | ✅ | `@NotBlank` | — | 地址 | `"110 W. Liberty St."` |
| city | `city` | String | ✅ | `@NotBlank` | — | 城市 | `"Madison"` |
| telephone | `telephone` | String | ✅ | `@NotBlank`, `@Pattern(regexp="\\d{10}")` | — | 电话号码（10位数字） | `"6085551023"` |
| pets | `pets` | Array\<Pet\> | 否 | `@OneToMany(cascade=ALL, fetch=EAGER)`, `@OrderBy("name")` | `[]`（空列表时） | 宠物列表（按名称排序） | `[{"id":1,"name":"Leo","birthDate":"2010-09-07","type":{...}}]` |
| pets[].id | `id` | Integer | 否 | 数据库自增主键 | `null` | 宠物ID | `1` |
| pets[].name | `name` | String | ✅ | `@NotBlank` | — | 宠物名称 | `"Leo"` |
| pets[].birthDate | `birthDate` | String | 否 | `@DateTimeFormat(pattern="yyyy-MM-dd")` | — | 宠物生日（序列化为 ISO 日期字符串） | `"2010-09-07"` |
| pets[].type | `type` | Object (PetType) | 否 | `@ManyToOne` | — | 宠物类型（嵌套对象） | `{"id":1,"name":"cat"}` |
| pets[].type.id | `id` | Integer | 否 | 数据库自增主键 | `null` | 类型ID | `1` |
| pets[].type.name | `name` | String | ✅ | `@NotBlank` | — | 类型名称 | `"cat"` |
| pets[].visits | `visits` | Array\<Visit\> | 否 | `@OneToMany(cascade=ALL, fetch=EAGER)`, `@OrderBy("date ASC")` | `[]`（空集合时） | 就诊记录列表（按日期升序） | `[{"id":1,"date":"2013-01-01","description":"rabies shot"}]` |

**字段备注**:
- `pets`: `cascade=ALL` 表示对 Owner 的持久化操作会级联到其下所有 Pet。
- `telephone`: 必须为恰好 10 位数字，校验失败时返回国际化消息 `{telephone.invalid}`。

---

## JSON 示例

```json
{
  "id": 1,
  "firstName": "George",
  "lastName": "Franklin",
  "address": "110 W. Liberty St.",
  "city": "Madison",
  "telephone": "6085551023",
  "pets": [
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
  ]
}
```

---

*基于 `org.springframework.samples.petclinic.owner.Owner` 源码生成 · 2026-07-10*
