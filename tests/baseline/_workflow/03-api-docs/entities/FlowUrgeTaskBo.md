# FlowUrgeTaskBo -- 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `FlowUrgeTaskBo` |
| **全限定名** | `org.dromara.workflow.domain.bo.FlowUrgeTaskBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 工作流管理 |
| **父类** | 无（直接实现 Serializable） |
| **序列化特性** | 无特殊配置 |
| **说明** | 催办任务请求对象，用于向任务办理人发送催办消息 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| taskIdList | `taskIdList` | array | 是 | `@NotNull`, groups=AddGroup | -- | 任务ID列表 | `[2001, 2002, 2003]` |
| messageType | `messageType` | array | 否 | -- | -- | 消息类型列表 | `["1", "2"]` |
| message | `message` | string | 是 | `@NotNull`, groups=AddGroup | -- | 催办内容 | `"请尽快处理您的待办任务"` |

---

## JSON 示例

```json
{
  "taskIdList": [2001, 2002, 2003],
  "messageType": ["1", "2"],
  "message": "请尽快处理您的待办任务"
}
```

---

*基于 `org.dromara.workflow.domain.bo.FlowUrgeTaskBo` 源码生成 . 2026-07-14*
