# FlowInvalidBo -- 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `FlowInvalidBo` |
| **全限定名** | `org.dromara.workflow.domain.bo.FlowInvalidBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 工作流管理 |
| **父类** | 无（直接实现 Serializable） |
| **序列化特性** | 无特殊配置 |
| **说明** | 作废请求对象，用于作废流程实例 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | number | 是 | `@NotNull`, groups=AddGroup | -- | 流程实例ID | `1001` |
| comment | `comment` | string | 否 | -- | -- | 审批意见 | `"流程信息有误，予以作废"` |

---

## JSON 示例

```json
{
  "id": 1001,
  "comment": "流程信息有误，予以作废"
}
```

---

*基于 `org.dromara.workflow.domain.bo.FlowInvalidBo` 源码生成 . 2026-07-14*
