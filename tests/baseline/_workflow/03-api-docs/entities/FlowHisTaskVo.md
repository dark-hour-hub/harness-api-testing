# FlowHisTaskVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `FlowHisTaskVo` |
| **全限定名** | `org.dromara.workflow.domain.vo.FlowHisTaskVo` |
| **类型** | 响应体 VO |
| **所属模块** | 工作流管理 |
| **父类** | 无（直接实现 Serializable） |
| **序列化特性** | 无特殊配置 |
| **说明** | 历史任务视图对象，用于展示已办任务列表（审批历史记录） |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | number | 否 | -- | -- | 主键ID | `3001` |
| createTime | `createTime` | string | 否 | -- | -- | 创建时间，getCreateTime() 返回格式化后的友好时间 | `"3天前"` |
| updateTime | `updateTime` | string | 否 | -- | -- | 更新时间 | `"2023-07-23 10:00:00"` |
| tenantId | `tenantId` | string | 否 | -- | -- | 租户ID | `"000000"` |
| delFlag | `delFlag` | string | 否 | -- | -- | 删除标记 | `"0"` |
| definitionId | `definitionId` | number | 否 | -- | -- | 对应 flow_definition 表的ID | `100` |
| flowName | `flowName` | string | 否 | -- | -- | 流程定义名称 | `"请假申请"` |
| instanceId | `instanceId` | number | 否 | -- | -- | 流程实例表ID | `1001` |
| taskId | `taskId` | number | 否 | -- | -- | 任务表ID | `2001` |
| cooperateType | `cooperateType` | number | 否 | -- | -- | 协作方式（1审批 2转办 3委派 4会签 5票签 6加签 7减签） | `1` |
| cooperateTypeName | `cooperateTypeName` | string | 否 | -- | -- | 协作方式名称，setCooperateType() 自动根据 cooperateType 设置 | `"审批"` |
| businessId | `businessId` | string | 否 | -- | -- | 业务ID | `"BIZ20230721001"` |
| nodeCode | `nodeCode` | string | 否 | -- | -- | 开始节点编码 | `"node_approval"` |
| nodeName | `nodeName` | string | 否 | -- | -- | 开始节点名称 | `"部门经理审批"` |
| nodeType | `nodeType` | number | 否 | -- | -- | 开始节点类型（0开始节点 1中间节点 2结束节点 3互斥网关 4并行网关） | `1` |
| targetNodeCode | `targetNodeCode` | string | 否 | -- | -- | 目标节点编码 | `"node_hr"` |
| targetNodeName | `targetNodeName` | string | 否 | -- | -- | 结束节点名称 | `"人事审批"` |
| approver | `approver` | string | 否 | -- | -- | 审批者ID | `"1002"` |
| approveName | `approveName` | string | 否 | -- | -- | 审批者名称，通过 `@Translation` 根据 approver 翻译 | `"李四"` |
| collaborator | `collaborator` | string | 否 | -- | -- | 协作人（只有转办、会签、票签、委派时有值） | `"1003"` |
| permissionList | `permissionList` | array | 否 | -- | -- | 权限标识列表（permissionFlag 的 list 形式） | `["1002"]` |
| skipType | `skipType` | string | 否 | -- | -- | 跳转类型（PASS通过 REJECT退回 NONE无动作） | `"PASS"` |
| flowStatus | `flowStatus` | string | 否 | -- | -- | 流程状态 | `"1"` |
| flowTaskStatus | `flowTaskStatus` | string | 否 | -- | -- | 任务状态 | `"PASS"` |
| flowStatusName | `flowStatusName` | string | 否 | -- | -- | 流程状态名称 | `"审批中"` |
| message | `message` | string | 否 | -- | -- | 审批意见 | `"同意请假申请"` |
| ext | `ext` | string | 否 | -- | -- | 业务详情（业务类的 JSON） | `""` |
| createBy | `createBy` | string | 否 | -- | -- | 创建者/申请人ID | `"1001"` |
| createByName | `createByName` | string | 否 | -- | -- | 申请人名称，通过 `@Translation` 根据 createBy 翻译 | `"张三"` |
| category | `category` | string | 否 | -- | -- | 流程分类ID | `"1"` |
| categoryName | `categoryName` | string | 否 | -- | -- | 流程分类名称，通过 `@Translation` 根据 category 翻译 | `"人事审批"` |
| formCustom | `formCustom` | string | 否 | -- | -- | 审批表单是否自定义（Y是 N否） | `"Y"` |
| formPath | `formPath` | string | 否 | -- | -- | 审批表单路径 | `"/workflow/form/leave"` |
| flowCode | `flowCode` | string | 否 | -- | -- | 流程定义编码 | `"leave_apply"` |
| version | `version` | string | 否 | -- | -- | 流程版本号 | `"1"` |
| runDuration | `runDuration` | string | 否 | -- | -- | 运行时长，自动计算（updateTime - createTime），在 setCreateTime/setUpdateTime 时自动更新 | `"1天2小时"` |
| businessCode | `businessCode` | string | 否 | -- | -- | 业务编码（扩展信息） | `"L20230721001"` |
| businessTitle | `businessTitle` | string | 否 | -- | -- | 业务标题（扩展信息） | `"张三的请假申请"` |

**字段备注**:
- `createTime`: getCreateTime() 返回 `DateUtils.formatFriendlyTime(createTime)` 的友好时间格式
- `runDuration`: 通过 setCreateTime()/setUpdateTime() 触发 updateRunDuration() 自动计算，使用 `DateUtils.getTimeDifference(updateTime, createTime)` 计算差值
- `cooperateTypeName`: 通过 setCooperateType() 自动翻译，使用 `CooperateType.getValueByKey(cooperateType)` 
- `cooperateType`: 枚举值 `1`=审批, `2`=转办, `3`=委派, `4`=会签, `5`=票签, `6`=加签, `7`=减签
- `nodeType`: 枚举值 `0`=开始节点, `1`=中间节点, `2`=结束节点, `3`=互斥网关, `4`=并行网关
- `skipType`: 枚举值 `"PASS"`=通过, `"REJECT"`=退回, `"NONE"`=无动作
- `approveName`: 通过 `@Translation(type = TransConstant.USER_ID_TO_NICKNAME, mapper = "approver")` 翻译
- `createByName`: 通过 `@Translation(type = TransConstant.USER_ID_TO_NICKNAME, mapper = "createBy")` 翻译
- `categoryName`: 通过 `@Translation(type = FlowConstant.CATEGORY_ID_TO_NAME, mapper = "category")` 翻译

---

## JSON 示例

```json
{
  "id": 3001,
  "createTime": "3天前",
  "updateTime": "2023-07-24 16:00:00",
  "tenantId": "000000",
  "delFlag": "0",
  "definitionId": 100,
  "flowName": "请假申请",
  "instanceId": 1001,
  "taskId": 2001,
  "cooperateType": 1,
  "cooperateTypeName": "审批",
  "businessId": "BIZ20230721001",
  "nodeCode": "node_approval",
  "nodeName": "部门经理审批",
  "nodeType": 1,
  "targetNodeCode": "node_hr",
  "targetNodeName": "人事审批",
  "approver": "1002",
  "approveName": "李四",
  "collaborator": "",
  "permissionList": ["1002"],
  "skipType": "PASS",
  "flowStatus": "2",
  "flowTaskStatus": "PASS",
  "flowStatusName": "已完成",
  "message": "同意请假申请",
  "ext": "",
  "createBy": "1001",
  "createByName": "张三",
  "category": "1",
  "categoryName": "人事审批",
  "formCustom": "Y",
  "formPath": "/workflow/form/leave",
  "flowCode": "leave_apply",
  "version": "1",
  "runDuration": "3天7小时",
  "businessCode": "L20230721001",
  "businessTitle": "张三的请假申请"
}
```

---

*基于 `org.dromara.workflow.domain.vo.FlowHisTaskVo` 源码生成 . 2026-07-14*
