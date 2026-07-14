# FlowDefinitionVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `FlowDefinitionVo` |
| **全限定名** | `org.dromara.workflow.domain.vo.FlowDefinitionVo` |
| **类型** | 响应体 VO |
| **所属模块** | 工作流管理 |
| **父类** | 无（直接实现 Serializable） |
| **序列化特性** | 无特殊配置 |
| **说明** | 流程定义视图对象，用于展示流程定义列表和详细信息 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | number | 否 | -- | -- | 流程定义ID | `100` |
| createTime | `createTime` | string | 否 | -- | -- | 创建时间 | `"2023-06-15 08:00:00"` |
| updateTime | `updateTime` | string | 否 | -- | -- | 更新时间 | `"2023-07-01 16:30:00"` |
| tenantId | `tenantId` | string | 否 | -- | -- | 租户ID | `"000000"` |
| delFlag | `delFlag` | string | 否 | -- | -- | 删除标记 | `"0"` |
| flowCode | `flowCode` | string | 否 | -- | -- | 流程定义编码 | `"leave_apply"` |
| flowName | `flowName` | string | 否 | -- | -- | 流程定义名称 | `"请假申请"` |
| category | `category` | string | 否 | -- | -- | 流程分类ID | `"1"` |
| categoryName | `categoryName` | string | 否 | -- | -- | 流程分类名称，通过 `@Translation` 根据 category 翻译而来 | `"人事审批"` |
| version | `version` | string | 否 | -- | -- | 流程版本 | `"1"` |
| isPublish | `isPublish` | number | 否 | -- | -- | 是否发布（0未发布 1已发布 9失效） | `1` |
| formCustom | `formCustom` | string | 否 | -- | -- | 审批表单是否自定义（Y是 N否） | `"Y"` |
| formPath | `formPath` | string | 否 | -- | -- | 审批表单路径 | `"/workflow/form/leave"` |
| activityStatus | `activityStatus` | number | 否 | -- | -- | 流程激活状态（0挂起 1激活） | `1` |
| listenerType | `listenerType` | string | 否 | -- | -- | 监听器类型 | `` |
| listenerPath | `listenerPath` | string | 否 | -- | -- | 监听器路径 | `""` |
| ext | `ext` | string | 否 | -- | -- | 扩展字段，预留给业务系统使用 | `""` |

**字段备注**:
- `isPublish`: 枚举值 `0`=未发布, `1`=已发布, `9`=失效
- `activityStatus`: 枚举值 `0`=挂起, `1`=激活
- `formCustom`: 枚举值 `"Y"`=自定义表单, `"N"`=使用默认表单
- `categoryName`: 通过 `@Translation(type = FlowConstant.CATEGORY_ID_TO_NAME, mapper = "category")` 自动翻译

---

## JSON 示例

```json
{
  "id": 100,
  "createTime": "2023-06-15 08:00:00",
  "updateTime": "2023-07-01 16:30:00",
  "tenantId": "000000",
  "delFlag": "0",
  "flowCode": "leave_apply",
  "flowName": "请假申请",
  "category": "1",
  "categoryName": "人事审批",
  "version": "1",
  "isPublish": 1,
  "formCustom": "Y",
  "formPath": "/workflow/form/leave",
  "activityStatus": 1,
  "listenerType": "",
  "listenerPath": "",
  "ext": ""
}
```

---

*基于 `org.dromara.workflow.domain.vo.FlowDefinitionVo` 源码生成 . 2026-07-14*
