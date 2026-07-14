# StartProcessBo -- 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `StartProcessBo` |
| **全限定名** | `org.dromara.workflow.domain.bo.StartProcessBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 工作流管理 |
| **父类** | 无（直接实现 Serializable） |
| **序列化特性** | 无特殊配置 |
| **说明** | 启动流程请求对象，用于发起工作流，包含业务ID、流程编码、办理人、流程变量和业务扩展信息 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| businessId | `businessId` | string | 是 | `@NotBlank`, groups=AddGroup | -- | 业务唯一值ID | `"BIZ20230721001"` |
| flowCode | `flowCode` | string | 是 | `@NotBlank`, groups=AddGroup | -- | 流程定义编码 | `"leave_apply"` |
| handler | `handler` | string | 否 | -- | -- | 办理人（可不填，用于覆盖当前节点办理人） | `"1001"` |
| variables | `variables` | object | 否 | -- | -- | 流程变量，前端会提交一个元素 `{"entity": {业务详情数据对象}}`，getVariables() 自动初始化并过滤 null 值条目 | `{"entity": {"leaveType": "年假", "leaveDays": 3}}` |
| bizExt | `bizExt` | object | 否 | -- | -- | 流程业务扩展信息，getBizExt() 自动初始化 | 见 FlowInstanceBizExt 子字段 |

### FlowInstanceBizExt 子字段（bizExt）

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| bizExt.id | `bizExt.id` | number | 否 | -- | -- | 主键 | `1` |
| bizExt.instanceId | `bizExt.instanceId` | number | 否 | -- | -- | 流程实例ID | `1001` |
| bizExt.businessId | `bizExt.businessId` | string | 否 | -- | -- | 业务ID | `"BIZ20230721001"` |
| bizExt.businessCode | `bizExt.businessCode` | string | 否 | -- | -- | 业务编码 | `"LC20230721001"` |
| bizExt.businessTitle | `bizExt.businessTitle` | string | 否 | -- | -- | 业务标题 | `"张三的请假申请"` |
| bizExt.delFlag | `bizExt.delFlag` | string | 否 | -- | -- | 删除标志（0存在 1删除），由 @TableLogic 管理 | `"0"` |
| bizExt.tenantId | `bizExt.tenantId` | string | 否 | -- | -- | 租户ID（继承自 TenantEntity） | `"000000"` |
| bizExt.searchValue | `bizExt.searchValue` | string | 否 | -- | -- | 搜索值（继承自 TenantEntity -> BaseEntity） | `""` |
| bizExt.createDept | `bizExt.createDept` | number | 否 | -- | -- | 创建部门（继承自 TenantEntity -> BaseEntity） | `103` |
| bizExt.createBy | `bizExt.createBy` | number | 否 | -- | -- | 创建者（继承自 TenantEntity -> BaseEntity） | `1` |
| bizExt.createTime | `bizExt.createTime` | string | 否 | -- | -- | 创建时间（继承自 TenantEntity -> BaseEntity） | `"2025-08-05 10:00:00"` |
| bizExt.updateBy | `bizExt.updateBy` | number | 否 | -- | -- | 更新者（继承自 TenantEntity -> BaseEntity） | `1` |
| bizExt.updateTime | `bizExt.updateTime` | string | 否 | -- | -- | 更新时间（继承自 TenantEntity -> BaseEntity） | `"2025-08-05 10:00:00"` |
| bizExt.params | `bizExt.params` | object | 否 | -- | -- | 额外参数（继承自 TenantEntity -> BaseEntity） | `{}` |

**字段备注**:
- `variables`: 前端通常提交 `{"entity": {业务详情数据}}`，框架会自动注入 initiator（发起人）、initiatorDeptId（发起人部门）、businessId 等变量
- `bizExt`: getBizExt() 方法保证不为 null，自动创建 FlowInstanceBizExt 实例
- `handler`: 如果未填写，系统将使用流程定义中配置的办理人规则

---

## JSON 示例

```json
{
  "businessId": "BIZ20230721001",
  "flowCode": "leave_apply",
  "handler": "1001",
  "variables": {
    "entity": {
      "leaveType": "年假",
      "startDate": "2023-07-25",
      "endDate": "2023-07-27",
      "leaveDays": 3,
      "remark": "家中有事需要处理"
    }
  },
  "bizExt": {
    "businessCode": "L20230721001",
    "businessTitle": "张三的请假申请"
  }
}
```

---

*基于 `org.dromara.workflow.domain.bo.StartProcessBo` 源码生成 . 2026-07-14*
