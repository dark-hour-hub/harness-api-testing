# BackProcessBo -- 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `BackProcessBo` |
| **全限定名** | `org.dromara.workflow.domain.bo.BackProcessBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 工作流管理 |
| **父类** | 无（直接实现 Serializable） |
| **序列化特性** | 无特殊配置 |
| **说明** | 驳回参数请求对象，用于审批人驳回任务（将流程退回到上一节点或申请人节点） |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| taskId | `taskId` | number | 是 | `@NotNull`, groups=AddGroup | -- | 任务ID | `2001` |
| fileId | `fileId` | string | 否 | -- | -- | 附件ID | `"oss_abc123"` |
| messageType | `messageType` | array | 否 | -- | -- | 消息类型列表 | `["1", "2"]` |
| nodeCode | `nodeCode` | string | 否 | -- | -- | 驳回的节点编码（目前未使用，直接驳回到申请人） | `"node_start"` |
| message | `message` | string | 否 | -- | -- | 办理意见 | `"请假申请信息不完整，请补充后重新提交"` |
| notice | `notice` | string | 否 | -- | -- | 通知内容 | `"您的请假申请已被驳回"` |
| variables | `variables` | object | 否 | -- | -- | 流程变量，getVariables() 自动初始化并过滤 null 值条目 | `{"rejectReason": "信息不完整"}` |

**字段备注**:
- `nodeCode`: 该字段标注为"目前未使用，直接驳回到申请人"，说明当前版本固定驳回至申请人节点
- `variables`: 同 CompleteTaskBo 中的 variables 处理逻辑

---

## JSON 示例

```json
{
  "taskId": 2001,
  "messageType": ["1"],
  "message": "请假申请信息不完整，请补充后重新提交",
  "notice": "您的请假申请已被驳回，请查看原因",
  "variables": {
    "rejectReason": "信息不完整"
  }
}
```

---

*基于 `org.dromara.workflow.domain.bo.BackProcessBo` 源码生成 . 2026-07-14*
