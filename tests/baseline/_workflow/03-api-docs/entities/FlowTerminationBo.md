# FlowTerminationBo -- 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `FlowTerminationBo` |
| **全限定名** | `org.dromara.workflow.domain.bo.FlowTerminationBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 工作流管理 |
| **父类** | 无（直接实现 Serializable） |
| **序列化特性** | 无特殊配置 |
| **说明** | 终止任务请求对象，用于强制终止正在进行的流程任务 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| taskId | `taskId` | number | 是 | `@NotNull`, groups=AddGroup | -- | 任务ID | `2001` |
| comment | `comment` | string | 否 | -- | -- | 审批意见 | `"业务已取消，终止流程"` |

---

## JSON 示例

```json
{
  "taskId": 2001,
  "comment": "业务已取消，终止流程"
}
```

---

*基于 `org.dromara.workflow.domain.bo.FlowTerminationBo` 源码生成 . 2026-07-14*
