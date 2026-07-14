# 工作流管理 — 流程实例 + Spel表达式 API 文档

> Controller: `FlwInstanceController`, `FlwSpelController` | Base URL: `http://localhost:8080` | Auth: Sa-Token JWT `Authorization: Bearer {token}` + `clientid: e5cd7e4891bf95d1d19206ce24a7b32e`

## 请求头

| 头名称 | 值 | 说明 |
|--------|-----|------|
| Content-Type | `application/json` | 请求体格式 |
| Authorization | `Bearer {token}` | Sa-Token JWT 令牌，登录后获取 |
| clientid | `e5cd7e4891bf95d1d19206ce24a7b32e` | 客户端 ID，与 Token 绑定 |

---

## /workflow/instance — 流程实例管理

### 1 查询正在运行的流程实例列表

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/workflow/instance/pageByRunning` |
| **接口说明** | 分页查询正在运行的流程实例（状态包含草稿、待审核、已退回、已撤销） |
| **认证方式** | 需要认证 |
| **权限要求** | `workflow:instance:list` |
| **标签** | 流程实例 |

---

#### 请求

**请求头**: [认证]

**查询参数**:

| 参数名 | 类型 | 必填 | 匹配方式 | 说明 | 示例 |
|--------|------|:---:|:---:|------|------|
| `pageNum` | Integer | 否 | -- | 当前页码，默认 1 | `1` |
| `pageSize` | Integer | 否 | -- | 每页条数，默认 10 | `10` |
| `orderByColumn` | String | 否 | -- | 排序列名 | `"createTime"` |
| `isAsc` | String | 否 | -- | 升序/降序 (asc/desc) | `"desc"` |
| `flowName` | String | 否 | like | 流程定义名称，模糊匹配 | `"请假"` |
| `flowCode` | String | 否 | like | 流程定义编码，模糊匹配 | `"leave_apply"` |
| `startUserId` | String | 否 | -- | 任务发起人 | `"1"` |
| `businessId` | String | 否 | eq | 业务ID，精确匹配 | `"BIZ20230721001"` |
| `category` | String | 否 | in | 流程分类ID，根据父级ID查询所有子分类 | `"1"` |
| `nodeName` | String | 否 | like | 任务名称/节点名称，模糊匹配 | `"部门经理"` |
| `createByIds` | List\<String\> | 否 | in | 申请人ID列表，批量精确匹配 | `"1001,1002"` |

**说明**:
- 固定过滤条件: `flow_status IN ('draft', 'waiting', 'back', 'cancel')` 且 `del_flag = '0'`
- 默认按 `create_time DESC` 排序

---

#### 响应

##### 成功响应 — HTTP 200

[TableDataInfo] 封装，`rows` 为 [FlowInstanceVo](../entities/FlowInstanceVo.md) 数组。

```json
{
  "code": 200,
  "msg": "操作成功",
  "total": 50,
  "rows": [
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
      "flowStatus": "waiting",
      "flowStatusName": "待审核",
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
  ]
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |

---

### 2 查询已结束的流程实例列表

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/workflow/instance/pageByFinish` |
| **接口说明** | 分页查询已结束的流程实例（状态包含已完成、已作废、已终止） |
| **认证方式** | 需要认证 |
| **权限要求** | `workflow:instance:list` |
| **标签** | 流程实例 |

---

#### 请求

**请求头**: [认证]

**查询参数**:

| 参数名 | 类型 | 必填 | 匹配方式 | 说明 | 示例 |
|--------|------|:---:|:---:|------|------|
| `pageNum` | Integer | 否 | -- | 当前页码，默认 1 | `1` |
| `pageSize` | Integer | 否 | -- | 每页条数，默认 10 | `10` |
| `orderByColumn` | String | 否 | -- | 排序列名 | `"createTime"` |
| `isAsc` | String | 否 | -- | 升序/降序 (asc/desc) | `"desc"` |
| `flowName` | String | 否 | like | 流程定义名称，模糊匹配 | `"请假"` |
| `flowCode` | String | 否 | like | 流程定义编码，模糊匹配 | `"leave_apply"` |
| `startUserId` | String | 否 | -- | 任务发起人 | `"1"` |
| `businessId` | String | 否 | eq | 业务ID，精确匹配 | `"BIZ20230721001"` |
| `category` | String | 否 | in | 流程分类ID，根据父级ID查询所有子分类 | `"1"` |
| `nodeName` | String | 否 | like | 任务名称/节点名称，模糊匹配 | `"部门经理"` |
| `createByIds` | List\<String\> | 否 | in | 申请人ID列表，批量精确匹配 | `"1001,1002"` |

**说明**:
- 固定过滤条件: `flow_status IN ('finish', 'invalid', 'termination')` 且 `del_flag = '0'`
- 默认按 `create_time DESC` 排序

---

#### 响应

##### 成功响应 — HTTP 200

[TableDataInfo] 封装，`rows` 为 [FlowInstanceVo](../entities/FlowInstanceVo.md) 数组。

```json
{
  "code": 200,
  "msg": "操作成功",
  "total": 30,
  "rows": [
    {
      "id": 1002,
      "createTime": "2023-07-20 08:00:00",
      "updateTime": "2023-07-21 16:00:00",
      "flowName": "报销审批",
      "flowCode": "expense_apply",
      "businessId": "BIZ20230720001",
      "flowStatus": "finish",
      "flowStatusName": "已完成",
      "createByName": "李四"
    }
  ]
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |

---

### 3 根据业务ID查询流程实例详细信息

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/workflow/instance/getInfo/{businessId}` |
| **接口说明** | 根据业务ID查询流程实例的详细信息，包含流程定义名称、编码、版本等扩展信息 |
| **认证方式** | 需要认证 |
| **权限要求** | `workflow:instance:query` |
| **标签** | 流程实例 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `businessId` | Long | 是 | 业务ID | `20230721001` |

---

#### 响应

##### 成功响应 — HTTP 200

[R] 封装，`data` 为 [FlowInstanceVo](../entities/FlowInstanceVo.md)。

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "id": 1001,
    "createTime": "2023-07-21 09:00:00",
    "updateTime": "2023-07-22 14:00:00",
    "definitionId": 100,
    "flowName": "请假申请",
    "flowCode": "leave_apply",
    "businessId": "BIZ20230721001",
    "nodeType": 1,
    "nodeCode": "node_approval",
    "nodeName": "部门经理审批",
    "flowStatus": "waiting",
    "flowStatusName": "待审核",
    "activityStatus": 1,
    "formCustom": "Y",
    "formPath": "/workflow/form/leave",
    "version": "1",
    "category": "1",
    "createBy": "1001",
    "createByName": "张三",
    "categoryName": "人事审批"
  }
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | 业务ID对应的流程实例不存在 | `"未找到流程实例"` (warm-flow ExceptionCons.NOT_FOUNT_INSTANCE) |
| 200 | 500 | 流程实例对应的流程定义不存在 | `"未找到流程定义"` (warm-flow ExceptionCons.NOT_FOUNT_DEF) |

---

### 4 按照业务ID删除流程实例

| 属性 | 值 |
|------|-----|
| **请求方式** | `DELETE` |
| **接口路径** | `/workflow/instance/deleteByBusinessIds/{businessIds}` |
| **接口说明** | 按照业务ID批量删除流程实例（不存在的业务ID将被忽略，不报错） |
| **认证方式** | 需要认证 |
| **权限要求** | `workflow:instance:remove` |
| **标签** | 流程实例 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `businessIds` | List\<Long\> | 是 | 业务ID列表，逗号分隔 | `20230721001,20230721002` |

---

#### 响应

##### 成功响应 — HTTP 200

[R]\<Void\> 封装，无 data 字段。

```json
{
  "code": 200,
  "msg": "操作成功"
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | 所有 businessId 对应的实例均未找到（服务层返回 false） | `"操作失败"` |

---

### 5 按照实例ID删除流程实例

| 属性 | 值 |
|------|-----|
| **请求方式** | `DELETE` |
| **接口路径** | `/workflow/instance/deleteByInstanceIds/{instanceIds}` |
| **接口说明** | 按照实例ID批量删除流程实例（不存在的实例ID将被忽略，不报错） |
| **认证方式** | 需要认证 |
| **权限要求** | `workflow:instance:remove` |
| **标签** | 流程实例 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `instanceIds` | List\<Long\> | 是 | 流程实例ID列表，逗号分隔 | `1001,1002` |

---

#### 响应

##### 成功响应 — HTTP 200

[R]\<Void\> 封装，无 data 字段。

```json
{
  "code": 200,
  "msg": "操作成功"
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | 所有 instanceId 对应的实例均未找到（服务层返回 false） | `"操作失败"` |

---

### 6 按照实例ID删除已完成的流程实例

| 属性 | 值 |
|------|-----|
| **请求方式** | `DELETE` |
| **接口路径** | `/workflow/instance/deleteHisByInstanceIds/{instanceIds}` |
| **接口说明** | 按照实例ID批量删除已完成的流程实例，同时清理关联的任务、用户、历史任务数据（不存在的实例ID将被忽略） |
| **认证方式** | 需要认证 |
| **权限要求** | `workflow:instance:remove` |
| **标签** | 流程实例 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `instanceIds` | List\<Long\> | 是 | 流程实例ID列表，逗号分隔 | `1001,1002` |

---

#### 响应

##### 成功响应 — HTTP 200

[R]\<Void\> 封装，无 data 字段。

```json
{
  "code": 200,
  "msg": "操作成功"
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | 所有 instanceId 对应的实例均未找到（服务层返回 false） | `"操作失败"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 级联删除 | 删除实例时同时删除关联的待办任务、用户任务关联、历史任务数据 |
| 事件发送 | 删除前会发送流程实例删除事件（`processDeleteHandler`），通知关联的业务模块 |

---

### 7 撤销流程

| 属性 | 值 |
|------|-----|
| **请求方式** | `PUT` |
| **接口路径** | `/workflow/instance/cancelProcessApply` |
| **接口说明** | 撤销指定流程申请，仅流程发起人或超级管理员可操作；已撤销/已完成/已作废/已终止/已退回的流程不可撤销 |
| **认证方式** | 需要认证 |
| **权限要求** | `workflow:instance:cancel` |
| **标签** | 流程实例 |
| **防重提交** | 是 (`@RepeatSubmit`) |

---

#### 请求

**请求头**: [认证]

**请求体**: [FlowCancelBo](../entities/FlowCancelBo.md)

```json
{
  "businessId": "BIZ20230721001",
  "message": "申请撤销该流程"
}
```

---

#### 响应

##### 成功响应 — HTTP 200

[R]\<Void\> 封装，无 data 字段。

```json
{
  "code": 200,
  "msg": "操作成功"
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | 业务ID对应的流程实例不存在 | `"未找到流程实例"` |
| 200 | 500 | 流程实例对应的流程定义不存在 | `"未找到流程定义"` |
| 200 | 500 | 非流程发起人且非超级管理员 | `"权限不足，无法撤销流程!"` |
| 200 | 500 | 流程已撤销 | `"该单据已撤销！"` |
| 200 | 500 | 流程已完成 | `"该单据已完成申请！"` |
| 200 | 500 | 流程已作废 | `"该单据已作废！"` |
| 200 | 500 | 流程已终止 | `"该单据已终止！"` |
| 200 | 500 | 流程已退回 | `"该单据已退回！"` |
| 200 | 500 | 流程状态为空 | `"流程状态为空！"` |
| 200 | 500 | 防重提交，短时间内重复请求 | `"不允许重复提交，请稍候再试"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 权限校验 | 仅流程发起人（`createBy`）或超级管理员可撤销 |
| 状态校验 | 通过 `BusinessStatusEnum.checkCancelStatus()` 检查状态，已撤销/已完成/已作废/已终止/已退回/空状态均不允许撤销 |
| 撤销效果 | 设置流程状态为 `cancel`，历史状态为 `cancel`，忽略后续节点 |

---

### 8 激活/挂起流程实例

| 属性 | 值 |
|------|-----|
| **请求方式** | `PUT` |
| **接口路径** | `/workflow/instance/active/{id}` |
| **接口说明** | 激活或挂起指定流程实例 |
| **认证方式** | 需要认证 |
| **权限要求** | `workflow:instance:active` |
| **标签** | 流程实例 |
| **防重提交** | 是 (`@RepeatSubmit`) |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `id` | Long | 是 | 流程实例ID | `1001` |

**查询参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `active` | Boolean | 是 | `true`=激活，`false`=挂起 | `true` |

---

#### 响应

##### 成功响应 — HTTP 200

[R]\<Boolean\> 封装，`data` 为操作结果。

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": true
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | 防重提交，短时间内重复请求 | `"不允许重复提交，请稍候再试"` |

---

### 9 获取当前登录人发起的流程实例

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/workflow/instance/pageByCurrent` |
| **接口说明** | 分页查询当前登录用户发起的流程实例列表 |
| **认证方式** | 需要认证 |
| **权限要求** | `workflow:instance:currentList` |
| **标签** | 流程实例 |

---

#### 请求

**请求头**: [认证]

**查询参数**:

| 参数名 | 类型 | 必填 | 匹配方式 | 说明 | 示例 |
|--------|------|:---:|:---:|------|------|
| `pageNum` | Integer | 否 | -- | 当前页码，默认 1 | `1` |
| `pageSize` | Integer | 否 | -- | 每页条数，默认 10 | `10` |
| `orderByColumn` | String | 否 | -- | 排序列名 | `"createTime"` |
| `isAsc` | String | 否 | -- | 升序/降序 (asc/desc) | `"desc"` |
| `flowName` | String | 否 | like | 流程定义名称，模糊匹配 | `"请假"` |
| `flowCode` | String | 否 | like | 流程定义编码，模糊匹配 | `"leave_apply"` |
| `startUserId` | String | 否 | -- | 任务发起人 | `"1"` |
| `businessId` | String | 否 | eq | 业务ID，精确匹配 | `"BIZ20230721001"` |
| `category` | String | 否 | in | 流程分类ID，根据父级ID查询所有子分类 | `"1"` |
| `nodeName` | String | 否 | like | 任务名称/节点名称，模糊匹配 | `"部门经理"` |
| `createByIds` | List\<String\> | 否 | in | 申请人ID列表，批量精确匹配 | `"1001,1002"` |

**说明**:
- 固定过滤条件: `fi.create_by = {当前登录用户ID}` 且 `del_flag = '0'`
- 默认按 `create_time DESC` 排序

---

#### 响应

##### 成功响应 — HTTP 200

[TableDataInfo] 封装，`rows` 为 [FlowInstanceVo](../entities/FlowInstanceVo.md) 数组。

```json
{
  "code": 200,
  "msg": "操作成功",
  "total": 10,
  "rows": [
    {
      "id": 1001,
      "createTime": "2023-07-21 09:00:00",
      "flowName": "请假申请",
      "flowCode": "leave_apply",
      "businessId": "BIZ20230721001",
      "flowStatus": "waiting",
      "flowStatusName": "待审核",
      "createByName": "张三"
    }
  ]
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |

---

### 10 获取流程图和流程记录

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/workflow/instance/flowHisTaskList/{businessId}` |
| **接口说明** | 根据业务ID获取流程图数据和流程任务记录（包含待审批任务和历史已处理任务） |
| **认证方式** | 需要认证 |
| **权限要求** | `workflow:instance:query` |
| **标签** | 流程实例 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `businessId` | String | 是 | 业务ID | `"BIZ20230721001"` |

---

#### 响应

##### 成功响应 — HTTP 200

[R]\<Map\<String, Object\>\> 封装，`data` 字段展开如下：

**响应字段**:

| 字段路径 | JSON 键名 | 类型 | 说明 |
|----------|-----------|------|------|
| data | `data` | Object | 响应数据 |
| data.instanceId | `instanceId` | Long | 流程实例ID |
| data.list | `list` | Array\<Object\> | 任务列表（待审批任务在前，历史任务在后） |
| data.list[].id | `id` | Long | 任务ID |
| data.list[].instanceId | `instanceId` | Long | 流程实例ID |
| data.list[].nodeCode | `nodeCode` | String | 节点编码 |
| data.list[].nodeName | `nodeName` | String | 节点名称 |
| data.list[].nodeType | `nodeType` | Integer | 节点类型 |
| data.list[].flowStatus | `flowStatus` | String | 任务状态（待审批任务固定为 `"waiting"`） |
| data.list[].approver | `approver` | String | 审批人名称（多审批人用逗号分隔） |
| data.list[].createTime | `createTime` | String | 创建时间 |
| data.list[].updateTime | `updateTime` | String | 更新时间（待审批任务为 null） |
| data.list[].runDuration | `runDuration` | String | 运行时长（待审批任务为 null） |

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "instanceId": 1001,
    "list": [
      {
        "id": 2001,
        "instanceId": 1001,
        "nodeCode": "node_approval",
        "nodeName": "部门经理审批",
        "nodeType": 1,
        "flowStatus": "waiting",
        "approver": "李四,王五",
        "createTime": "2023-07-21 09:00:00",
        "updateTime": null,
        "runDuration": null
      },
      {
        "id": 2000,
        "instanceId": 1001,
        "nodeCode": "node_start",
        "nodeName": "发起申请",
        "nodeType": 0,
        "flowStatus": "finish",
        "approver": "张三",
        "createTime": "2023-07-21 09:00:00",
        "updateTime": "2023-07-21 09:01:00",
        "runDuration": "1分钟"
      }
    ]
  }
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | 业务ID对应的流程实例不存在 | `"未找到流程实例"` |

---

### 11 获取流程变量

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/workflow/instance/instanceVariable/{instanceId}` |
| **接口说明** | 根据流程实例ID获取该流程的变量信息，包含变量键值对列表和原始变量JSON字符串 |
| **认证方式** | 需要认证 |
| **权限要求** | `workflow:instance:variableQuery` |
| **标签** | 流程实例 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `instanceId` | Long | 是 | 流程实例ID | `1001` |

---

#### 响应

##### 成功响应 — HTTP 200

[R]\<Map\<String, Object\>\> 封装，`data` 字段展开如下：

**响应字段**:

| 字段路径 | JSON 键名 | 类型 | 说明 |
|----------|-----------|------|------|
| data | `data` | Object | 响应数据 |
| data.variableList | `variableList` | Array\<Object\> | 变量键值对列表 |
| data.variableList[].key | `key` | String | 变量键名 |
| data.variableList[].value | `value` | Object | 变量值 |
| data.variable | `variable` | String | 原始变量JSON字符串 |

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "variableList": [
      { "key": "leaveType", "value": "年假" },
      { "key": "leaveDays", "value": 3 },
      { "key": "applicant", "value": "张三" }
    ],
    "variable": "{\"leaveType\":\"年假\",\"leaveDays\":3,\"applicant\":\"张三\"}"
  }
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | 流程实例ID对应的实例不存在 | `"未找到流程实例"` |

---

### 12 修改流程变量

| 属性 | 值 |
|------|-----|
| **请求方式** | `PUT` |
| **接口路径** | `/workflow/instance/updateVariable` |
| **接口说明** | 修改指定流程实例的流程变量值（仅可修改已存在的变量key，不存在的key将操作失败） |
| **认证方式** | 需要认证 |
| **权限要求** | `workflow:instance:variable` |
| **标签** | 流程实例 |
| **防重提交** | 是 (`@RepeatSubmit`) |

---

#### 请求

**请求头**: [认证]

**请求体**: [FlowVariableBo](../entities/FlowVariableBo.md)

```json
{
  "instanceId": 1001,
  "key": "leaveDays",
  "value": "5"
}
```

---

#### 响应

##### 成功响应 — HTTP 200

[R]\<Void\> 封装，无 data 字段。

```json
{
  "code": 200,
  "msg": "操作成功"
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | instanceId 为 null（DTO校验失败） | `"instanceId * 必须填写"` (i18n key: `not.null`) |
| 200 | 500 | key 为 null（DTO校验失败） | `"key * 必须填写"` (i18n key: `not.null`) |
| 200 | 500 | value 为 null（DTO校验失败） | `"value * 必须填写"` (i18n key: `not.null`) |
| 200 | 500 | 流程实例不存在 | `"未找到流程实例"` |
| 200 | 500 | 要修改的变量key在流程变量中不存在（服务层返回 false） | `"操作失败"` |
| 200 | 500 | 防重提交，短时间内重复请求 | `"不允许重复提交，请稍候再试"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 变量存在性校验 | 只能修改已存在的流程变量key，不存在的key返回操作失败 |
| 变量覆盖 | 新值会完全覆盖旧值 |

---

### 13 作废流程

| 属性 | 值 |
|------|-----|
| **请求方式** | `POST` |
| **接口路径** | `/workflow/instance/invalid` |
| **接口说明** | 作废指定流程实例，已完成的流程不可作废 |
| **认证方式** | 需要认证 |
| **权限要求** | `workflow:instance:invalid` |
| **标签** | 流程实例 |
| **防重提交** | 是 (`@RepeatSubmit`) |

---

#### 请求

**请求头**: [认证]

**请求体**: [FlowInvalidBo](../entities/FlowInvalidBo.md)

```json
{
  "id": 1001,
  "comment": "流程信息有误，予以作废"
}
```

---

#### 响应

##### 成功响应 — HTTP 200

[R]\<Boolean\> 封装，`data` 为操作结果。

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": true
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | id 为 null（DTO校验失败） | `"id * 必须填写"` (i18n key: `not.null`) |
| 200 | 500 | 流程已完成 | `"该单据已完成申请！"` |
| 200 | 500 | 流程已作废 | `"该单据已作废！"` |
| 200 | 500 | 流程已终止 | `"该单据已终止！"` |
| 200 | 500 | 流程状态为空 | `"流程状态为空！"` |
| 200 | 500 | 防重提交，短时间内重复请求 | `"不允许重复提交，请稍候再试"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 作废条件 | 已完成（finish）、已作废（invalid）、已终止（termination）状态的流程不可作废 |
| 作废效果 | 设置流程状态为 `invalid`，历史状态为 `invalid`，终止实例下所有任务 |
| 空实例处理 | 若实例ID对应实例不存在，跳过状态校验，直接尝试作废 |

---

## /workflow/spel — 流程Spel表达式定义管理

### 14 查询流程Spel表达式定义列表

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/workflow/spel/list` |
| **接口说明** | 分页查询流程Spel表达式定义列表 |
| **认证方式** | 需要认证 |
| **权限要求** | `workflow:spel:list` |
| **标签** | Spel表达式 |

---

#### 请求

**请求头**: [认证]

**查询参数**:

| 参数名 | 类型 | 必填 | 匹配方式 | 说明 | 示例 |
|--------|------|:---:|:---:|------|------|
| `pageNum` | Integer | 否 | -- | 当前页码，默认 1 | `1` |
| `pageSize` | Integer | 否 | -- | 每页条数，默认 10 | `10` |
| `orderByColumn` | String | 否 | -- | 排序列名 | `"createTime"` |
| `isAsc` | String | 否 | -- | 升序/降序 (asc/desc) | `"desc"` |
| `componentName` | String | 否 | like | 组件名称，模糊匹配 | `"SysUser"` |
| `methodName` | String | 否 | like | 方法名，模糊匹配 | `"selectUser"` |
| `methodParams` | String | 否 | eq | 方法参数，精确匹配 | `"deptId"` |
| `viewSpel` | String | 否 | eq | 预览SpEL表达式，精确匹配 | `"@sysUserService.selectUserByDept(deptId)"` |
| `status` | String | 否 | eq | 状态（`"0"`=正常, `"1"`=停用），精确匹配 | `"0"` |
| `remark` | String | 否 | like | 备注，模糊匹配 | `"审批"` |

**说明**:
- 默认按 `id ASC` 排序

---

#### 响应

##### 成功响应 — HTTP 200

[TableDataInfo] 封装，`rows` 为 [FlowSpelVo](../entities/FlowSpelVo.md) 数组。

```json
{
  "code": 200,
  "msg": "操作成功",
  "total": 5,
  "rows": [
    {
      "id": 1,
      "componentName": "SysUserService",
      "methodName": "selectUserByDept",
      "methodParams": "deptId",
      "viewSpel": "@sysUserService.selectUserByDept(deptId)",
      "status": "0",
      "remark": "按部门查找审批人",
      "createTime": "2025-07-04 09:00:00"
    }
  ]
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |

---

### 15 获取流程Spel表达式定义详细信息

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/workflow/spel/{id}` |
| **接口说明** | 根据主键ID获取流程Spel表达式定义详细信息 |
| **认证方式** | 需要认证 |
| **权限要求** | `workflow:spel:query` |
| **标签** | Spel表达式 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `id` | Long | 是 | Spel表达式定义主键ID | `1` |

---

#### 响应

##### 成功响应 — HTTP 200

[R] 封装，`data` 为 [FlowSpelVo](../entities/FlowSpelVo.md)。

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "id": 1,
    "componentName": "SysUserService",
    "methodName": "selectUserByDept",
    "methodParams": "deptId",
    "viewSpel": "@sysUserService.selectUserByDept(deptId)",
    "status": "0",
    "remark": "按部门查找审批人",
    "createTime": "2025-07-04 09:00:00"
  }
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | id 为 null（校验注解 `@NotNull`） | `"主键不能为空"` |

---

### 16 新增流程Spel表达式定义

| 属性 | 值 |
|------|-----|
| **请求方式** | `POST` |
| **接口路径** | `/workflow/spel` |
| **接口说明** | 新增一条流程Spel表达式定义记录 |
| **认证方式** | 需要认证 |
| **权限要求** | `workflow:spel:add` |
| **标签** | Spel表达式 |
| **防重提交** | 是 (`@RepeatSubmit`) |

---

#### 请求

**请求头**: [认证]

**请求体**: [FlowSpelBo](../entities/FlowSpelBo.md) (AddGroup 校验组)

```json
{
  "componentName": "SysUserService",
  "methodName": "selectUserByDept",
  "methodParams": "deptId",
  "viewSpel": "@sysUserService.selectUserByDept(deptId)",
  "status": "0",
  "remark": "按部门查找审批人"
}
```

---

#### 响应

##### 成功响应 — HTTP 200

[R]\<Void\> 封装，无 data 字段。

```json
{
  "code": 200,
  "msg": "操作成功"
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | viewSpel 为空（DTO校验失败，AddGroup） | `"viewSpel * 必须填写"` (i18n key: `not.null`) |
| 200 | 500 | status 为空（DTO校验失败，AddGroup） | `"status * 必须填写"` (i18n key: `not.null`) |
| 200 | 500 | viewSpel 表达式已存在（业务校验重复） | `"SpEL表达式已存在，请勿重复添加"` |
| 200 | 500 | 防重提交，短时间内重复请求 | `"不允许重复提交，请稍候再试"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 唯一性校验 | `viewSpel` 表达式全局唯一，重复添加将抛出业务异常 |
| 必填字段 | `viewSpel`（SpEL预览值）、`status`（状态）为必填 |

---

### 17 修改流程Spel表达式定义

| 属性 | 值 |
|------|-----|
| **请求方式** | `PUT` |
| **接口路径** | `/workflow/spel` |
| **接口说明** | 修改一条流程Spel表达式定义记录 |
| **认证方式** | 需要认证 |
| **权限要求** | `workflow:spel:edit` |
| **标签** | Spel表达式 |
| **防重提交** | 是 (`@RepeatSubmit`) |

---

#### 请求

**请求头**: [认证]

**请求体**: [FlowSpelBo](../entities/FlowSpelBo.md) (EditGroup 校验组)

```json
{
  "id": 1,
  "componentName": "SysUserService",
  "methodName": "selectUserByDept",
  "methodParams": "deptId",
  "viewSpel": "@sysUserService.selectUserByDept(deptId)",
  "status": "0",
  "remark": "按部门查找审批人（更新后的备注）"
}
```

---

#### 响应

##### 成功响应 — HTTP 200

[R]\<Void\> 封装，无 data 字段。

```json
{
  "code": 200,
  "msg": "操作成功"
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | viewSpel 为空（DTO校验失败，EditGroup） | `"viewSpel * 必须填写"` (i18n key: `not.null`) |
| 200 | 500 | status 为空（DTO校验失败，EditGroup） | `"status * 必须填写"` (i18n key: `not.null`) |
| 200 | 500 | viewSpel 表达式与其他记录冲突（业务校验） | `"SpEL表达式已存在，请勿重复添加"` |
| 200 | 500 | 防重提交，短时间内重复请求 | `"不允许重复提交，请稍候再试"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 唯一性校验 | 修改时校验 `viewSpel` 是否与其他记录冲突（排除自身ID），冲突时抛出异常 |
| 必填字段 | `viewSpel`、`status` 为必填，与新增一致 |

---

### 18 删除流程Spel表达式定义

| 属性 | 值 |
|------|-----|
| **请求方式** | `DELETE` |
| **接口路径** | `/workflow/spel/{ids}` |
| **接口说明** | 批量删除流程Spel表达式定义 |
| **认证方式** | 需要认证 |
| **权限要求** | `workflow:spel:remove` |
| **标签** | Spel表达式 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `ids` | Long[] | 是 | 主键ID数组，逗号分隔 | `1,2,3` |

---

#### 响应

##### 成功响应 — HTTP 200

[R]\<Void\> 封装，无 data 字段。

```json
{
  "code": 200,
  "msg": "操作成功"
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | ids 为空（校验注解 `@NotEmpty`） | `"主键不能为空"` |

---

*基于 RuoYi-Vue-Plus 源码生成 . 2026-07-14*
