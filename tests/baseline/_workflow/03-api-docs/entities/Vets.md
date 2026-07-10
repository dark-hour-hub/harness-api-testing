# Vets — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `Vets` |
| **全限定名** | `org.springframework.samples.petclinic.vet.Vets` |
| **类型** | 响应体 VO |
| **所属模块** | 兽医管理 |
| **父类** | 无（继承 `java.lang.Object`） |
| **序列化特性** | Jackson 默认（基于 getter 发现属性），同时支持 JAXB XML 序列化（`@XmlRootElement`） |
| **说明** | 兽医列表的简单包装类，用于 `GET /vets` 的 JSON/XML 响应。包含一个 `vetList` 数组属性。 |

---

## 注解转义说明

| Java 字段名 | JSON 键名 | 显示名 | 转义来源 |
|------------|----------|--------|----------|
| `vets` | `vetList` | — | Jackson getter 命名：`getVetList()` → `vetList` |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| vetList | `vetList` | Array\<Vet\> | 否 | — | `[]`（空列表时） | 兽医列表，为 null 时初始化为空 ArrayList | `[{"id":1,"firstName":"James","lastName":"Carter","specialties":[...],"nrOfSpecialties":1}]` |
| vetList[].id | `id` | Integer | 否 | 数据库自增主键 | `null`（新建时） | 兽医ID | `1` |
| vetList[].firstName | `firstName` | String | ✅ | `@NotBlank`, `@Size(max=30)` | — | 名字 | `"James"` |
| vetList[].lastName | `lastName` | String | ✅ | `@NotBlank`, `@Size(max=30)` | — | 姓氏 | `"Carter"` |
| vetList[].specialties | `specialties` | Array\<Specialty\> | 否 | — | `[]`（空集合时） | 专业领域列表（按名称排序），JAXB 标注 `@XmlElement` | `[{"id":1,"name":"radiology"}]` |
| vetList[].specialties[].id | `id` | Integer | 否 | 数据库自增主键 | `null` | 专业领域ID | `1` |
| vetList[].specialties[].name | `name` | String | ✅ | `@NotBlank` | — | 专业领域名称 | `"radiology"` |
| vetList[].nrOfSpecialties | `nrOfSpecialties` | Integer | 否 | — | `0` | 专业领域数量（计算属性，来自 `getSpecialtiesInternal().size()`） | `1` |

**字段备注**:
- `nrOfSpecialties`: 计算属性（非持久化字段），由 `getNrOfSpecialties()` 方法返回，值为 `specialties` 集合的 size。

---

## JSON 示例

```json
{
  "vetList": [
    {
      "id": 1,
      "firstName": "James",
      "lastName": "Carter",
      "specialties": [],
      "nrOfSpecialties": 0
    },
    {
      "id": 2,
      "firstName": "Helen",
      "lastName": "Leary",
      "specialties": [
        {
          "id": 1,
          "name": "radiology"
        }
      ],
      "nrOfSpecialties": 1
    }
  ]
}
```

---

*基于 `org.springframework.samples.petclinic.vet.Vets` 源码生成 · 2026-07-10*
