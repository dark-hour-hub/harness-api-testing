# FlowInstanceVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `FlowInstanceVo` |
| **全限定名** | `org.dromara.workflow.domain.vo.FlowInstanceVo` |
| **类型** | 响应体 VO |
| **所属模块** | 工作流管理 |
| **父类** | 无 |
| **序列化特性** | 无特殊配置 |
| **说明** | 流程实例视图对象，用于展示流程实例列表和详情（包含运行中和已结束的流程） |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | number | 否 | -- | -- | 流程实例ID | `1001` |
| createTime | `createTime` | string | 否 | -- | -- | 创建时间 | `"2023-07-21 09:00:00"` |
| updateTime | `updateTime` | string | 否 | -- | -- | 更新时间 | `"2023-07-22 14:00:00"` |
| tenantId | `tenantId` | string | 否 | -- | -- | 租户ID | `"000000"` |
| delFlag | `delFlag` | string | 否 | -- | -- | 删除标记 | `"0"` |
| definitionId | `definitionId` | number | 否 | -- | -- | 对应 flow_definition 表的ID | `100` |
| flowName | `flowName` | string | 否 | -- | -- | 流程定义名称 | `"请假申请"` |
| flowCode | `flowCode` | string | 否 | -- | -- | 流程定义编码 | `"leave_apply"` |
| businessId | `businessId` | string | 否 | -- | -- | 业务ID | `"BIZ20230721001"` |
| nodeType | `nodeType` | number | 否 | -- | -- | 节点类型（0开始节点 1中间节点 2结束节点 3互斥网关 4并行网关） | `1` |
| nodeCode | `nodeCode` | string | 否 | -- | -- | 流程节点编码（每个流程的 nodeCode 是唯一的，definitionId+nodeCode 唯一） | `"node_approval"` |
| nodeName | `nodeName` | string | 否 | -- | -- | 流程节点名称 | `"部门经理审批"` |
| variable | `variable` | string | 否 | -- | -- | 流程变量（JSON 字符串） | `"{\"leaveType\":\"年假\",\"leaveDays\":3}"` |
| flowStatus | `flowStatus` | string | 否 | -- | -- | 流程状态 | `"1"` |
| flowStatusName | `flowStatusName` | string | 否 | -- | -- | 流程状态名称 | `"审批中"` |
| activityStatus | `activityStatus` | number | 否 | -- | -- | 流程激活状态（0挂起 1激活） | `1` |
| formCustom | `formCustom` | string | 否 | -- | -- | 审批表单是否自定义（Y是 N否） | `"Y"` |
| formPath | `formPath` | string | 否 | -- | -- | 审批表单路径 | `"/workflow/form/leave"` |
| ext | `ext` | string | 否 | -- | -- | 扩展字段，预留给业务系统使用 | `""` |
| version | `version` | string | 否 | -- | -- | 流程定义版本 | `"1"` |
| createBy | `createBy` | string | 否 | -- | -- | 创建者/申请人ID | `"1001"` |
| createByName | `createByName` | string | 否 | -- | -- | 申请人名称，通过 `@Translation` 根据 createBy 翻译而来 | `"张三"` |
| category | `category` | string | 否 | -- | -- | 流程分类ID | `"1"` |
| categoryName | `categoryName` | string | 否 | -- | -- | 流程分类名称，通过 `@Translation` 根据 category 翻译而来 | `"人事审批"` |
| businessCode | `businessCode` | string | 否 | -- | -- | 业务编码（扩展信息） | `"L20230721001"` |
| businessTitle | `businessTitle` | string | 否 | -- | -- | 业务标题（扩展信息） | `"张三的请假申请"` |

**字段备注**:
- `nodeType`: 枚举值 `0`=开始节点, `1`=中间节点, `2`=结束节点, `3`=互斥网关, `4`=并行网关
- `activityStatus`: 枚举值 `0`=挂起, `1`=激活
- `createByName`: 通过 `@Translation(type = TransConstant.USER_ID_TO_NICKNAME, mapper = "createBy")` 自动翻译
- `categoryName`: 通过 `@Translation(type = FlowConstant.CATEGORY_ID_TO_NAME, mapper = "category")` 自动翻译
- `businessCode`, `businessTitle`: 来自 FlowInstanceBizExt 业务扩展表

---

## JSON 示例

```json
{
  "id": 1001,
  "createTime": "2023-07-21 09:00:00",
  "updateTime": "2023-07-22 14:00:00",
  "tenantId": "000000",
  "delFlag": "0",
  "definitionId": 100,
  "flowName": "请假申请",
  "flowCode": "leave_apply",
  "businessId": "BIZ20230721001",
  "nodeType": 1,
  "nodeCode": "node_approval",
  "nodeName": "部门经理审批",
  "variable": "{\"leaveType\":\"年假\",\"leaveDays\":3}",
  "flowStatus": "1",
  "flowStatusName": "审批中",
  "activityStatus": 1,
  "formCustom": "Y",
  "formPath": "/workflow/form/leave",
  "ext": "",
  "version": "1",
  "createBy": "1001",
  "createByName": "张三",
  "category": "1",
  "categoryName": "人事审批",
  "businessCode": "L20230721001",
  "businessTitle": "张三的请假申请"
}
```

---

*基于 `org.dromara.workflow.domain.vo.FlowInstanceVo` 源码生成 . 2026-07-14*
