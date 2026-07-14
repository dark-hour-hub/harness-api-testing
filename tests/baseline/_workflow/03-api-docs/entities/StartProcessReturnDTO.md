# StartProcessReturnDTO -- 响应体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `StartProcessReturnDTO` |
| **全限定名** | `org.dromara.common.core.domain.dto.StartProcessReturnDTO` |
| **类型** | 响应体 DTO |
| **所属模块** | 工作流管理（定义在 common-core 公共模块） |
| **父类** | 无（直接实现 Serializable） |
| **序列化特性** | 无特殊配置 |
| **说明** | 启动流程返回对象，包含流程实例ID和任务ID，在调用 startWorkFlow 接口后返回 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| processInstanceId | `processInstanceId` | number | 否 | -- | -- | 流程实例ID | `1001` |
| taskId | `taskId` | number | 否 | -- | -- | 任务ID | `2001` |

---

## JSON 示例

```json
{
  "processInstanceId": 1001,
  "taskId": 2001
}
```

---

*基于 `org.dromara.common.core.domain.dto.StartProcessReturnDTO` 源码生成 . 2026-07-14*
