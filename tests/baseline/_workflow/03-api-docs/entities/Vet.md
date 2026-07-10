# Vet — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `Vet` |
| **全限定名** | `org.springframework.samples.petclinic.vet.Vet` |
| **类型** | 响应体 VO（JPA 实体复用） |
| **所属模块** | 兽医管理 |
| **父类** | `Person` → `BaseEntity` |
| **序列化特性** | Jackson 默认（基于 getter 发现属性），部分 getter 标注 `@XmlElement`（JAXB XML 序列化） |
| **说明** | 兽医实体，映射 `vets` 表。继承 Person 的基本信息字段，关联多对多专业领域（Specialty）。在 `GET /vets` 响应中作为 `vetList` 数组元素返回。 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | Integer | 否 | 数据库自增主键（`@GeneratedValue(IDENTITY)`） | `null`（新建时） | 兽医ID（继承自 BaseEntity） | `1` |
| firstName | `firstName` | String | ✅ | `@NotBlank`, `@Size(max=30)`, `@Column(length=30)` | — | 名字（继承自 Person） | `"James"` |
| lastName | `lastName` | String | ✅ | `@NotBlank`, `@Size(max=30)`, `@Column(length=30)` | — | 姓氏（继承自 Person） | `"Carter"` |
| specialties | `specialties` | Array\<Specialty\> | 否 | `@ManyToMany(fetch=EAGER)` | `[]`（空集合时） | 专业领域列表（按名称排序），JAXB 标注 `@XmlElement` | `[{"id":1,"name":"radiology"}]` |
| specialties[].id | `id` | Integer | 否 | 数据库自增主键 | `null` | 专业领域ID | `1` |
| specialties[].name | `name` | String | ✅ | `@NotBlank` | — | 专业领域名称 | `"radiology"` |
| nrOfSpecialties | `nrOfSpecialties` | Integer | 否 | — | `0` | 专业领域数量（计算属性，来自 `getSpecialtiesInternal().size()`） | `2` |

**字段备注**:
- `specialties`: 通过中间表 `vet_specialties` 关联，`fetch=EAGER` 立即加载。getter 返回按名称排序的 List。
- `nrOfSpecialties`: 计算属性（非持久化字段），由 `getNrOfSpecialties()` 方法返回。不被 JAXB `@XmlElement` 标注，但 Jackson 会序列化。

---

## JSON 示例

```json
{
  "id": 1,
  "firstName": "James",
  "lastName": "Carter",
  "specialties": [
    {
      "id": 1,
      "name": "radiology"
    },
    {
      "id": 2,
      "name": "surgery"
    }
  ],
  "nrOfSpecialties": 2
}
```

---

*基于 `org.springframework.samples.petclinic.vet.Vet` 源码生成 · 2026-07-10*
