# TaskOperationBo -- 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `TaskOperationBo` |
| **全限定名** | `org.dromara.workflow.domain.bo.TaskOperationBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 工作流管理 |
| **父类** | 无（直接实现 Serializable） |
| **序列化特性** | 无特殊配置 |
| **说明** | 任务操作业务对象，用于描述任务委派（delegateTask）、转办（transferTask）、加签（addSignature）、减签（reductionSignature）等操作的必要参数 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| userId | `userId` | string | 是(委派/转办) | `@NotNull`, groups=AddGroup | -- | 委派/转办人的用户ID | `"1003"` |
| userIds | `userIds` | array | 是(加签/减签) | `@NotNull`, groups=EditGroup | -- | 加签/减签人的用户ID列表 | `["1004", "1005"]` |
| taskId | `taskId` | number | 是 | `@NotNull` | -- | 任务ID | `2001` |
| messageType | `messageType` | array | 否 | -- | -- | 消息类型列表 | `["1", "2"]` |
| message | `message` | string | 否 | -- | -- | 意见或备注信息 | `"委派给王五处理"` |

**字段备注**:
- `userId`: 用于委派（delegateTask）和转办（transferTask）操作，属于 AddGroup 校验组
- `userIds`: 用于加签（addSignature）和减签（reductionSignature）操作，属于 EditGroup 校验组
- 操作类型通过 URL 路径参数 `taskOperation` 指定：`delegateTask`、`transferTask`、`addSignature`、`reductionSignature`
- 加签/减签操作仅适用于会签或票签节点（非或签）

---

## JSON 示例

### 委派操作

```json
{
  "userId": "1003",
  "taskId": 2001,
  "message": "委派给王五处理此人离职流程"
}
```

### 加签操作

```json
{
  "userIds": ["1004", "1005"],
  "taskId": 2001,
  "message": "请赵六、钱七参与审批"
}
```

---

*基于 `org.dromara.workflow.domain.bo.TaskOperationBo` 源码生成 . 2026-07-14*
