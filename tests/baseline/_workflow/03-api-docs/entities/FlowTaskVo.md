# FlowTaskVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `FlowTaskVo` |
| **全限定名** | `org.dromara.workflow.domain.vo.FlowTaskVo` |
| **类型** | 响应体 VO |
| **所属模块** | 工作流管理 |
| **父类** | 无（直接实现 Serializable） |
| **序列化特性** | 无特殊配置 |
| **说明** | 任务视图对象，用于展示待办/已办/抄送任务列表和任务详情 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | number | 否 | -- | -- | 任务ID | `2001` |
| createTime | `createTime` | string | 否 | -- | -- | 创建时间，getCreateTime() 返回格式化后的友好时间 | `"2小时前"` |
| updateTime | `updateTime` | string | 否 | -- | -- | 更新时间 | `"2023-07-22 15:00:00"` |
| tenantId | `tenantId` | string | 否 | -- | -- | 租户ID | `"000000"` |
| delFlag | `delFlag` | string | 否 | -- | -- | 删除标记 | `"0"` |
| definitionId | `definitionId` | number | 否 | -- | -- | 对应 flow_definition 表的ID | `100` |
| instanceId | `instanceId` | number | 否 | -- | -- | 流程实例表ID | `1001` |
| flowName | `flowName` | string | 否 | -- | -- | 流程定义名称 | `"请假申请"` |
| businessId | `businessId` | string | 否 | -- | -- | 业务ID | `"BIZ20230721001"` |
| nodeCode | `nodeCode` | string | 否 | -- | -- | 节点编码 | `"node_approval"` |
| nodeName | `nodeName` | string | 否 | -- | -- | 节点名称 | `"部门经理审批"` |
| nodeType | `nodeType` | number | 否 | -- | -- | 节点类型（0开始节点 1中间节点 2结束节点 3互斥网关 4并行网关） | `1` |
| permissionList | `permissionList` | array | 否 | -- | -- | 权限标识列表（permissionFlag 的 list 形式） | `["1002", "1003"]` |
| userList | `userList` | array | 否 | -- | -- | 流程用户列表（warm-flow User 对象数组） | `[{"userId": 1002, "nickName": "李四"}]` |
| formCustom | `formCustom` | string | 否 | -- | -- | 审批表单是否自定义（Y是 N否） | `"Y"` |
| formPath | `formPath` | string | 否 | -- | -- | 审批表单路径 | `"/workflow/form/leave"` |
| flowCode | `flowCode` | string | 否 | -- | -- | 流程定义编码 | `"leave_apply"` |
| version | `version` | string | 否 | -- | -- | 流程版本号 | `"1"` |
| flowStatus | `flowStatus` | string | 否 | -- | -- | 流程状态 | `"1"` |
| flowStatusName | `flowStatusName` | string | 否 | -- | -- | 流程状态名称，通过 `@Translation` 从字典 wf_business_status 翻译 | `"审批中"` |
| category | `category` | string | 否 | -- | -- | 流程分类ID | `"1"` |
| categoryName | `categoryName` | string | 否 | -- | -- | 流程分类名称，通过 `@Translation` 根据 category 翻译 | `"人事审批"` |
| type | `type` | string | 否 | -- | -- | 办理人类型 | `"1"` |
| assigneeIds | `assigneeIds` | string | 否 | -- | -- | 办理人ID列表 | `"1002"` |
| assigneeNames | `assigneeNames` | string | 否 | -- | -- | 办理人名称，通过 `@Translation` 根据 assigneeIds 翻译 | `"李四"` |
| processedBy | `processedBy` | string | 否 | -- | -- | 抄送人ID | `"1003"` |
| processedByName | `processedByName` | string | 否 | -- | -- | 抄送人名称，通过 `@Translation` 根据 processedBy 翻译 | `"王五"` |
| nodeRatio | `nodeRatio` | string | 否 | -- | -- | 流程签署比例值，大于0为票签、会签 | `"0"` |
| createBy | `createBy` | string | 否 | -- | -- | 申请人ID | `"1001"` |
| createByName | `createByName` | string | 否 | -- | -- | 申请人名称，通过 `@Translation` 根据 createBy 翻译 | `"张三"` |
| applyNode | `applyNode` | boolean | 否 | -- | -- | 是否为申请人节点 | `false` |
| buttonList | `buttonList` | array | 否 | -- | -- | 按钮权限列表 | `[{"code": "PASS", "name": "通过"}]` |
| copyList | `copyList` | array | 否 | -- | -- | 抄送对象 ID 集合，根据扩展属性中 CopySettingEnum 类型的数据生成 | `[{"userId": 1003, "nickName": "王五"}]` |
| varList | `varList` | object | 否 | -- | -- | 自定义参数 Map，根据扩展属性中 VariablesEnum 类型的数据生成 | `{"key1": "value1"}` |
| businessCode | `businessCode` | string | 否 | -- | -- | 业务编码（扩展信息） | `"L20230721001"` |
| businessTitle | `businessTitle` | string | 否 | -- | -- | 业务标题（扩展信息） | `"张三的请假申请"` |

**字段备注**:
- `createTime`: getCreateTime() 返回 `DateUtils.formatFriendlyTime(createTime)` 的友好时间格式（如"刚刚"、"2小时前"、"3天前"）
- `nodeType`: 枚举值 `0`=开始节点, `1`=中间节点, `2`=结束节点, `3`=互斥网关, `4`=并行网关
- `flowStatusName`: 通过 `@Translation(type = TransConstant.DICT_TYPE_TO_LABEL, mapper = "flowStatus", other = "wf_business_status")` 从字典翻译
- `assigneeNames`: 通过 `@Translation(type = TransConstant.USER_ID_TO_NICKNAME, mapper = "assigneeIds")` 翻译
- `processedByName`: 通过 `@Translation(type = TransConstant.USER_ID_TO_NICKNAME, mapper = "processedBy")` 翻译
- `createByName`: 通过 `@Translation(type = TransConstant.USER_ID_TO_NICKNAME, mapper = "createBy")` 翻译
- `categoryName`: 通过 `@Translation(type = FlowConstant.CATEGORY_ID_TO_NAME, mapper = "category")` 翻译
- `copyList`: 存储的是 `FlowCopyVo` 对象列表
- `varList`: 存储的是 `String` -> `String` 的键值对
- `businessCode`, `businessTitle`: 来自业务扩展信息

---

## JSON 示例

```json
{
  "id": 2001,
  "createTime": "2小时前",
  "updateTime": "2023-07-22 15:00:00",
  "tenantId": "000000",
  "delFlag": "0",
  "definitionId": 100,
  "instanceId": 1001,
  "flowName": "请假申请",
  "businessId": "BIZ20230721001",
  "nodeCode": "node_approval",
  "nodeName": "部门经理审批",
  "nodeType": 1,
  "permissionList": ["1002"],
  "formCustom": "Y",
  "formPath": "/workflow/form/leave",
  "flowCode": "leave_apply",
  "version": "1",
  "flowStatus": "1",
  "flowStatusName": "审批中",
  "category": "1",
  "categoryName": "人事审批",
  "type": "1",
  "assigneeIds": "1002",
  "assigneeNames": "李四",
  "nodeRatio": "0",
  "createBy": "1001",
  "createByName": "张三",
  "applyNode": false,
  "buttonList": [
    {"code": "PASS", "name": "通过"},
    {"code": "REJECT", "name": "驳回"}
  ],
  "copyList": [],
  "varList": {},
  "businessCode": "L20230721001",
  "businessTitle": "张三的请假申请"
}
```

---

*基于 `org.dromara.workflow.domain.vo.FlowTaskVo` 源码生成 . 2026-07-14*
