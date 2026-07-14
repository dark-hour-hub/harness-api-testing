# 工作流管理 Part 3: 任务管理 + 请假示例 API 文档（增量）

> Controller: `FlwTaskController`, `TestLeaveController` | Base URL: `http://localhost:8080` | Auth: Sa-Token JWT `Authorization: Bearer {token}` + `clientid: e5cd7e4891bf95d1d19206ce24a7b32e`

## 请求头

| 头名称 | 值 | 说明 |
|--------|-----|------|
| Content-Type | `application/json` | 请求体格式；导出接口使用 `application/x-www-form-urlencoded` |
| Authorization | `Bearer {token}` | Sa-Token JWT 令牌，登录后获取 |
| clientid | `e5cd7e4891bf95d1d19206ce24a7b32e` | 客户端 ID，与 Token 绑定 |

---

## 一、任务管理接口 `/workflow/task`

---

> 接口 1（启动任务）未变更，参见基线文档。

---

### 2 办理任务 <span style="color:orange">**[修改]**</span>

| 属性 | 值 |
|------|-----|
| **请求方式** | `POST` |
| **接口路径** | `/workflow/task/completeTask` |
| **接口说明** | 办理（审批通过）待办任务，推动流程流转到下一节点 |
| **认证方式** | 需要认证 |
| **权限要求** | 无 |
| **标签** | 任务管理 |
| **防重** | `@RepeatSubmit()` 防止重复提交 |
| **变更类型** | `modified`（间接影响） |

---

#### 变更说明

`FlwTaskServiceImpl.completeTask()` 内部调用 `getNextNodeList()`，间接受到异常匹配逻辑扩展的影响（`NULL_SKIP_TYPE` 异常现在被跳过而非抛出）。

---

#### 请求

**请求头**: [认证]

**请求体**: [CompleteTaskBo](../entities/CompleteTaskBo.md)

---

#### 响应

##### 成功响应 — HTTP 200

返回 `R<Void>`，无 data 内容。

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": null
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 200 | 500 | `taskId` 为空（`@NotNull` 校验） | `"任务id不能为空"` |
| 200 | 500 | 流程任务不存在或已审批 | `"流程任务不存在或任务已审批！"` |
| 200 | 500 | 流程实例不存在 | `"流程实例不存在"` |
| 200 | 500 | 重复提交 | `"不允许重复提交，请稍候再试"` |
| 200 | 500 | 流程状态校验失败（草稿/撤销/退回状态会继续，其他状态异常） | 业务状态校验异常消息 |

---

#### 断言

| # | 层级 | 断言项 | 预期值 | 断言消息 |
|---|:---:|--------|--------|------|
| 1 | 协议层 | HTTP 状态码 | 200 | "HTTP状态码应为200" |
| 2 | 业务层 | code | 200 | "业务状态码应为200" |
| 3 | 业务层 | msg | "操作成功" | "提示消息应为'操作成功'" |
| 4 | 数据层 | data | null | "返回data应为null" |
| 5 | 业务层 | 任务完成后流程推进到下一节点 | 流程状态变更 | "流程应推进到下一节点" |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 抄送人处理 | `flowCopyList` 被注入到流程变量 `FLOW_COPY_LIST` 中，WorkflowGlobalListener 在任务完成后自动处理抄送 |
| 消息类型 | `messageType` 被注入到流程变量 `MESSAGE_TYPE` 中，用于消息通知渠道 |
| 消息通知 | `notice` 被注入到流程变量 `MESSAGE_NOTICE` 中 |
| 弹窗办理人 | `assigneeMap` 用于弹窗选择的下一节点处理人，会合并到实例变量中 |
| 草稿/撤销/退回续办 | 若流程状态为草稿、已撤销或已退回，会自动标记 `SUBMIT=true` 触发流程提交监听 |
| 分布式锁 | 使用 `@Lock4j` 对 `taskId` 加锁，防止并发办理 |

---

> 接口 3-8（待办/已办/抄送/查询任务）未变更，参见基线文档。

---

### 9 获取下一节点信息 <span style="color:orange">**[修改]**</span>

| 属性 | 值 |
|------|-----|
| **请求方式** | `POST` |
| **接口路径** | `/workflow/task/getNextNodeList` |
| **接口说明** | 查询当前任务的下一个审批节点列表（用于办理前预览后续审批环节） |
| **认证方式** | 需要认证 |
| **权限要求** | 无 |
| **标签** | 任务管理 |
| **变更类型** | `modified`（直接修改） |

---

#### 变更说明

`FlwTaskServiceImpl.getNextNodeList()` 中条件变量缺失的异常匹配逻辑扩展：从仅匹配 `NULL_CONDITION_VALUE` 改为同时匹配 `NULL_CONDITION_VALUE` 和 `NULL_SKIP_TYPE`。修复条件分支跳过类型缺失导致流程异常中断的问题。

**源码变更**:

```java
// 变更前
if (!ExceptionCons.NULL_CONDITION_VALUE.equals(e.getMessage())) {
    throw e;
}

// 变更后
if (!StringUtils.containsAny(e.getMessage(), ExceptionCons.NULL_CONDITION_VALUE, ExceptionCons.NULL_SKIP_TYPE)) {
    throw e;
}
```

---

#### 请求

**请求头**: [认证]

**请求体**: [FlowNextNodeBo](../entities/FlowNextNodeBo.md)

---

#### 响应

##### 成功响应 — HTTP 200

`data` 为 `List<FlowNode>` 数组。

[FlowNode](../entities/FlowNode.md)

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": [
    {
      "id": 5002,
      "definitionId": 100,
      "nodeCode": "node_hr",
      "nodeName": "人事审批",
      "nodeType": 1,
      "permissionFlag": "role:hr",
      "nodeRatio": "0",
      "version": "1",
      "skipAnyNode": "N",
      "coordinate": "400,300",
      "ext": "",
      "createTime": "2023-06-15 08:00:00",
      "updateTime": "2023-07-01 16:30:00"
    }
  ]
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 200 | 500 | 任务不存在 | `"任务不存在！"` |
| 200 | 500 | 流程实例不存在 | `"流程实例不存在"` |
| 200 | 500 | 流程定义不存在 | `"流程定义不存在"` |
| 200 | 200 | 无下一节点（流程已结束） | `"操作成功"`（返回空数组） |

---

#### 断言

| # | 层级 | 断言项 | 预期值 | 断言消息 |
|---|:---:|--------|--------|------|
| 1 | 协议层 | HTTP 状态码 | 200 | "HTTP状态码应为200" |
| 2 | 业务层 | code | 200 | "业务状态码应为200" |
| 3 | 业务层 | 包含跳过类型节点的流程获取下一节点 | 正常返回，不抛异常 | "NULL_SKIP_TYPE异常应被跳过而非中断" |
| 4 | 业务层 | 其他类型 FlowException（非跳过类） | 抛出异常（500） | "非跳过类异常应正常抛出" |
| 5 | 数据层 | data[*].nodeCode 存在性 | 存在 | "返回的节点列表每项应包含nodeCode" |
| 6 | 数据层 | data[*].nodeName 存在性 | 存在 | "返回的节点列表每项应包含nodeName" |
| 7 | 数据层 | data[*].nodeType 存在性 | 存在 | "返回的节点列表每项应包含nodeType" |

---

#### 业务规则变更

| 规则 | 变更前 | 变更后 |
|------|--------|--------|
| 条件分支异常跳过 | 仅跳过 `NULL_CONDITION_VALUE` 异常 | 同时跳过 `NULL_CONDITION_VALUE` 和 `NULL_SKIP_TYPE` 异常 |

---

> 接口 10-12（终止任务、任务操作、修改办理人）未变更，参见基线文档。

---

### 13 驳回审批 <span style="color:orange">**[修改]**</span>

| 属性 | 值 |
|------|-----|
| **请求方式** | `POST` |
| **接口路径** | `/workflow/task/backProcess` |
| **接口说明** | 驳回当前任务到前一节点（默认驳回至申请人节点） |
| **认证方式** | 需要认证 |
| **权限要求** | 无 |
| **标签** | 任务管理 |
| **防重** | `@RepeatSubmit()` 防止重复提交 |
| **变更类型** | `modified`（间接影响） |

---

#### 变更说明

`FlwTaskServiceImpl.backProcess()` 内部调用 `getNextNodeList()`，间接受到异常匹配逻辑扩展的影响。

---

#### 请求

**请求头**: [认证]

**请求体**: [BackProcessBo](../entities/BackProcessBo.md)

---

#### 响应

##### 成功响应 — HTTP 200

返回 `R<Void>`，无 data 内容。

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": null
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 200 | 500 | `taskId` 为空（`@NotNull` 校验） | `"任务ID不能为空"` |
| 200 | 500 | 任务不存在 | `"任务不存在！"` |
| 200 | 500 | 流程实例不存在 | `"流程实例不存在"` |
| 200 | 500 | 流程状态不允许驳回（checkBackStatus） | 业务状态校验异常消息 |
| 200 | 500 | 重复提交 | `"不允许重复提交，请稍候再试"` |

---

#### 断言

| # | 层级 | 断言项 | 预期值 | 断言消息 |
|---|:---:|--------|--------|------|
| 1 | 协议层 | HTTP 状态码 | 200 | "HTTP状态码应为200" |
| 2 | 业务层 | code | 200 | "业务状态码应为200" |
| 3 | 业务层 | msg | "操作成功" | "提示消息应为'操作成功'" |
| 4 | 业务层 | 驳回成功后可重新提交 | 流程状态变更 | "驳回后流程可重新提交" |
| 5 | 数据层 | data | null | "返回data应为null" |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 驳回目标 | 当前版本 `nodeCode` 字段未使用，统一驳回至申请人节点 |
| 驳回回申请人 | 若 `nodeCode` 等于申请人节点编码，流程状态设为 `BACK`（已退回） |
| 驳回至其他节点 | 若 `nodeCode` 不等于申请人节点，流程状态设为 `WAITING`（待处理） |
| 状态校验 | 通过 `BusinessStatusEnum.checkBackStatus()` 校验，已完成/已终止/已作废的流程不允许驳回 |
| 跳转类型 | 固定使用 `SkipType.REJECT`（退回跳转） |

---

> 接口 14-17（可驳回前置节点、办理人列表、催办、抄送）及请假示例接口（18-24）未变更，参见基线文档。

---

> 文档生成时间: 2026-07-14 | 变更接口数: 3 (任务管理) | 覆盖控制器: `FlwTaskController`
