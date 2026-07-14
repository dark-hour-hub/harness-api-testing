# FlowVariableBo -- 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `FlowVariableBo` |
| **全限定名** | `org.dromara.workflow.domain.bo.FlowVariableBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 工作流管理 |
| **父类** | 无（直接实现 Serializable） |
| **序列化特性** | 无特殊配置 |
| **说明** | 流程变量参数，用于修改流程实例的变量值 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| instanceId | `instanceId` | number | 是 | `@NotNull`, groups=AddGroup | -- | 流程实例ID | `1001` |
| key | `key` | string | 是 | `@NotNull`, groups=AddGroup | -- | 流程变量key | `"leaveDays"` |
| value | `value` | string | 是 | `@NotNull`, groups=AddGroup | -- | 流程变量value | `"3"` |

---

## JSON 示例

```json
{
  "instanceId": 1001,
  "key": "leaveDays",
  "value": "3"
}
```

---

*基于 `org.dromara.workflow.domain.bo.FlowVariableBo` 源码生成 . 2026-07-14*
