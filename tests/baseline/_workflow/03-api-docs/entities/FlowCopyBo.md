# FlowCopyBo -- 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `FlowCopyBo` |
| **全限定名** | `org.dromara.workflow.domain.bo.FlowCopyBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 工作流管理 |
| **父类** | 无（直接实现 Serializable） |
| **序列化特性** | 无特殊配置 |
| **说明** | 抄送对象，用于指定流程任务的抄送人员信息 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| userId | `userId` | number | 否 | -- | -- | 抄送用户ID | `1001` |
| nickName | `nickName` | string | 否 | -- | -- | 用户昵称 | `"张三"` |

---

## JSON 示例

```json
{
  "userId": 1001,
  "nickName": "张三"
}
```

---

*基于 `org.dromara.workflow.domain.bo.FlowCopyBo` 源码生成 . 2026-07-14*
