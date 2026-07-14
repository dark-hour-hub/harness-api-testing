# CompleteTaskBo -- 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `CompleteTaskBo` |
| **全限定名** | `org.dromara.workflow.domain.bo.CompleteTaskBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 工作流管理 |
| **父类** | 无（直接实现 Serializable） |
| **序列化特性** | 无特殊配置 |
| **说明** | 办理任务请求对象，用于审批人办理（通过/驳回）待办任务 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| taskId | `taskId` | number | 是 | `@NotNull`, groups=AddGroup | -- | 任务ID | `2001` |
| fileId | `fileId` | string | 否 | -- | -- | 附件ID | `"oss_abc123"` |
| flowCopyList | `flowCopyList` | array | 否 | -- | -- | 抄送人员列表 | 见 FlowCopyBo 子字段 |
| messageType | `messageType` | array | 否 | -- | -- | 消息类型列表 | `["1", "2", "3"]` |
| message | `message` | string | 否 | -- | -- | 办理意见 | `"同意请假申请"` |
| notice | `notice` | string | 否 | -- | -- | 消息通知内容 | `"您的请假申请已审批通过"` |
| handler | `handler` | string | 否 | -- | -- | 办理人（可不填，用于覆盖当前节点办理人） | `"1002"` |
| variables | `variables` | object | 否 | -- | -- | 流程变量，getVariables() 自动初始化并过滤 null 值条目 | `{"auditResult": "PASS"}` |
| assigneeMap | `assigneeMap` | object | 否 | -- | -- | 弹窗选择的办理人 Map，key 为节点编码，value 为办理人ID | `{"node_2": "1003"}` |
| ext | `ext` | string | 否 | -- | -- | 扩展变量（此处为逗号分隔的 ossId） | `"oss_001,oss_002"` |

### FlowCopyBo 子字段（flowCopyList[]）

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| flowCopyList[].userId | `flowCopyList[].userId` | number | 否 | -- | -- | 抄送用户ID | `1003` |
| flowCopyList[].nickName | `flowCopyList[].nickName` | string | 否 | -- | -- | 用户昵称 | `"李四"` |

**字段备注**:
- `flowCopyList`: 抄送人员信息会被设置到流程变量 `FLOW_COPY_LIST` 中
- `messageType`: 消息类型会被设置到流程变量 `MESSAGE_TYPE` 中
- `notice`: 通知内容会被设置到流程变量 `MESSAGE_NOTICE` 中
- `assigneeMap`: 用于在弹窗中选择下一节点办理人的场景

---

## JSON 示例

```json
{
  "taskId": 2001,
  "fileId": "oss_abc123",
  "flowCopyList": [
    {
      "userId": 1003,
      "nickName": "李四"
    }
  ],
  "messageType": ["1", "2"],
  "message": "同意请假申请",
  "notice": "您的请假申请已审批通过",
  "handler": "1002",
  "variables": {
    "auditResult": "PASS"
  },
  "assigneeMap": {
    "node_2": "1003"
  },
  "ext": "oss_001,oss_002"
}
```

---

*基于 `org.dromara.workflow.domain.bo.CompleteTaskBo` 源码生成 . 2026-07-14*
