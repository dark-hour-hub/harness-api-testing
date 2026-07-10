# Visit — 响应体 VO / 表单绑定对象

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `Visit` |
| **全限定名** | `org.springframework.samples.petclinic.owner.Visit` |
| **类型** | 响应体 VO / 请求体 DTO（JPA 实体复用，同时用于 Thymeleaf 表单绑定和视图渲染） |
| **所属模块** | 客户管理 |
| **父类** | `BaseEntity` |
| **序列化特性** | Jackson 默认（基于 getter 发现属性） |
| **说明** | 就诊记录实体，映射 `visits` 表。记录宠物的就诊日期和描述信息。 |

---

## 字段定义

### 实体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | Integer | 否 | 数据库自增主键（`@GeneratedValue(IDENTITY)`） | `null`（新建时） | 就诊记录ID（继承自 BaseEntity） | `1` |
| date | `date` | LocalDate | 否 | `@DateTimeFormat(pattern="yyyy-MM-dd")`, `@Column(name="visit_date")` | 明天（`LocalDate.now().plusDays(1)`） | 就诊日期（数据库中列名为 `visit_date`） | `"2013-01-01"` |
| description | `description` | String | ✅ | `@NotBlank` | — | 就诊描述 | `"rabies shot"` |

**字段备注**:
- `date`: 构造器中默认设置为明天，为用户提供合理的默认值。`@Column(name="visit_date")` 指定数据库列名，但不影响 JSON 键名。
- `description`: 通过 `@NotBlank` 校验非空，在 POST 提交时由 `@Valid` 触发校验。

---

## JSON 示例

```json
{
  "id": 1,
  "date": "2013-01-01",
  "description": "rabies shot"
}
```

---

*基于 `org.springframework.samples.petclinic.owner.Visit` 源码生成 · 2026-07-10*
