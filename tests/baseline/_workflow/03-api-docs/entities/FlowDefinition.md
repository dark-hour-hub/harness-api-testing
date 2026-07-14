# FlowDefinition -- 查询参数 BO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `FlowDefinition` |
| **全限定名** | `org.dromara.warm.flow.orm.entity.FlowDefinition` |
| **类型** | 查询参数 BO（外部库 warm-flow-mybatis-plus-sb3-starter 1.8.5） |
| **所属模块** | 工作流管理 |
| **父类** | warm-flow 内部基类 |
| **序列化特性** | 由 warm-flow 库定义 |
| **说明** | warm-flow 流程定义 ORM 实体，同时作为查询参数 BO 用于流程定义列表查询。来源为外部依赖 `warm-flow-mybatis-plus-sb3-starter`，源码不可直接访问。 |

---

## 字段定义

### 查询参数 / 请求体字段

> 以下字段基于 RuoYi-Vue-Plus 代码中的使用模式推断，实际字段以 warm-flow 1.8.5 库定义为准。

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | number | 否 | -- | -- | 流程定义ID | `100` |
| flowCode | `flowCode` | string | 否 | -- | -- | 流程定义编码 | `"leave_apply"` |
| flowName | `flowName` | string | 否 | -- | -- | 流程定义名称 | `"请假申请"` |
| version | `version` | string | 否 | -- | -- | 流程版本 | `"1"` |
| isPublish | `isPublish` | number | 否 | -- | -- | 是否发布（0未发布 1已发布 9失效） | `1` |
| category | `category` | string | 否 | -- | -- | 流程分类ID | `"1"` |
| formCustom | `formCustom` | string | 否 | -- | -- | 审批表单是否自定义（Y是 N否） | `"Y"` |
| formPath | `formPath` | string | 否 | -- | -- | 审批表单路径 | `"/workflow/form/leave"` |
| activityStatus | `activityStatus` | number | 否 | -- | -- | 流程激活状态（0挂起 1激活） | `1` |
| listenerType | `listenerType` | string | 否 | -- | -- | 监听器类型 | `""` |
| listenerPath | `listenerPath` | string | 否 | -- | -- | 监听器路径 | `""` |
| ext | `ext` | string | 否 | -- | -- | 扩展字段 | `""` |
| createTime | `createTime` | string | 否 | -- | -- | 创建时间 | `"2023-06-15 08:00:00"` |
| updateTime | `updateTime` | string | 否 | -- | -- | 更新时间 | `"2023-07-01 16:30:00"` |

**字段备注**:
- `isPublish`: 枚举值 `0`=未发布, `1`=已发布, `9`=失效（来源 PublishStatus 枚举）
- `activityStatus`: 枚举值 `0`=挂起, `1`=激活
- 作为 GET 请求查询参数时，字段通过 URL query string 传递
- 作为 POST/PUT 请求体时，用于新增/修改流程定义
- 与 `FlowDefinitionVo` 对应，但 FlowDefinitionVo 是 VO（响应），FlowDefinition 是实体/BO（请求/查询）
- 此类是 warm-flow 外部库提供的 MyBatis-Plus 实体，详细的字段定义和注解以 warm-flow 库源码为准

---

## JSON 示例

### 查询参数（GET 请求 query string）

```
GET /workflow/definition/list?flowCode=leave_apply&flowName=请假申请&pageNum=1&pageSize=10
```

### 新增请求体（POST 请求）

```json
{
  "flowCode": "leave_apply",
  "flowName": "请假申请",
  "category": "1",
  "version": "1",
  "isPublish": 0,
  "formCustom": "Y",
  "formPath": "/workflow/form/leave",
  "activityStatus": 1
}
```

---

*基于 `org.dromara.warm.flow.orm.entity.FlowDefinition`（warm-flow 1.8.5）使用分析生成 . 2026-07-14*
