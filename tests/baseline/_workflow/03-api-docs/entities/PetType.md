# PetType — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `PetType` |
| **全限定名** | `org.springframework.samples.petclinic.owner.PetType` |
| **类型** | 响应体 VO（JPA 实体复用） |
| **所属模块** | 客户管理 |
| **父类** | `NamedEntity` → `BaseEntity` |
| **序列化特性** | Jackson 默认（基于 getter 发现属性） |
| **说明** | 宠物类型实体，映射 `types` 表。用于宠物类型下拉选项的数据源，如 Cat、Dog、Hamster 等。无额外字段。 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | Integer | 否 | 数据库自增主键（`@GeneratedValue(IDENTITY)`） | `null`（新建时） | 类型ID（继承自 BaseEntity） | `1` |
| name | `name` | String | ✅ | `@NotBlank` | — | 类型名称（继承自 NamedEntity） | `"cat"` |

---

## JSON 示例

```json
{
  "id": 1,
  "name": "cat"
}
```

---

*基于 `org.springframework.samples.petclinic.owner.PetType` 源码生成 · 2026-07-10*
