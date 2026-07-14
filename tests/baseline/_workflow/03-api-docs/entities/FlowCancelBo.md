# FlowCancelBo -- 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `FlowCancelBo` |
| **全限定名** | `org.dromara.workflow.domain.bo.FlowCancelBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 工作流管理 |
| **父类** | 无（直接实现 Serializable） |
| **序列化特性** | 无特殊配置 |
| **说明** | 撤销任务请求对象，用于撤销流程申请 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| businessId | `businessId` | string | 是 | `@NotBlank`, groups=AddGroup | -- | 业务ID | `"BIZ20230721001"` |
| message | `message` | string | 否 | -- | -- | 办理意见 | `"申请撤销该流程"` |

---

## JSON 示例

```json
{
  "businessId": "BIZ20230721001",
  "message": "申请撤销该流程"
}
```

---

*基于 `org.dromara.workflow.domain.bo.FlowCancelBo` 源码生成 . 2026-07-14*
