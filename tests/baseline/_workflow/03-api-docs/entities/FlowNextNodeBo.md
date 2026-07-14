# FlowNextNodeBo -- 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `FlowNextNodeBo` |
| **全限定名** | `org.dromara.workflow.domain.bo.FlowNextNodeBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 工作流管理 |
| **父类** | 无（直接实现 Serializable） |
| **序列化特性** | 无特殊配置 |
| **说明** | 下一节点信息请求对象，用于查询当前任务的后续节点列表 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| taskId | `taskId` | number | 否 | -- | -- | 任务ID | `2001` |
| variables | `variables` | object | 否 | -- | -- | 流程变量，键值对 Map，getVariables() 自动初始化非空 Map 并过滤 null 值条目 | `{"leaveType": "年假"}` |

---

## JSON 示例

```json
{
  "taskId": 2001,
  "variables": {
    "leaveType": "年假",
    "leaveDays": 5
  }
}
```

---

*基于 `org.dromara.workflow.domain.bo.FlowNextNodeBo` 源码生成 . 2026-07-14*
