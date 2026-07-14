# Definition -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `Definition` |
| **全限定名** | `org.dromara.warm.flow.core.entity.Definition` |
| **类型** | 响应体 VO / 核心实体（外部库 warm-flow-core 1.8.5） |
| **所属模块** | 工作流管理 |
| **父类** | warm-flow 内部基类 |
| **序列化特性** | 由 warm-flow 库定义 |
| **说明** | warm-flow 流程定义核心实体，用于返回单个流程定义的完整信息（如 getInfo 接口）。来源为外部依赖 `warm-flow-mybatis-plus-sb3-starter`，源码不可直接访问。 |

---

## 字段定义

### 响应体字段

> 以下字段基于 RuoYi-Vue-Plus 代码中的使用模式及 warm-flow 官方文档推断，实际字段以 warm-flow 1.8.5 库定义为准。

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
| ext | `ext` | string | 否 | -- | -- | 扩展字段，JSON 格式，包含流程定义扩展参数（如 autoPass 等） | `"{\"autoPass\": false}"` |

**字段备注**:
- `isPublish`: 枚举值 `0`=未发布, `1`=已发布, `9`=失效
- `activityStatus`: 枚举值 `0`=挂起, `1`=激活
- `ext`: JSON 字符串，可通过 `JsonUtils.parseMap()` 解析为 Dict 对象，常见键如 `autoPass`（自动通过）
- 此对象用于 `GET /workflow/definition/{id}` 返回流程定义详情
- 与 `FlowDefinitionVo` 的区别：`FlowDefinitionVo` 带有 `@Translation` 注解用于列表展示的翻译字段；`Definition` 是 warm-flow 核心实体，不带翻译逻辑
- `FlowDefinition` (ORM 实体) 是 `Definition` (核心实体) 的 MyBatis-Plus 包装

---

## JSON 示例

```json
{
  "id": 100,
  "flowCode": "leave_apply",
  "flowName": "请假申请",
  "version": "1",
  "isPublish": 1,
  "category": "1",
  "formCustom": "Y",
  "formPath": "/workflow/form/leave",
  "activityStatus": 1,
  "listenerType": "",
  "listenerPath": "",
  "ext": "{\"autoPass\": false}"
}
```

---

*基于 `org.dromara.warm.flow.core.entity.Definition`（warm-flow 1.8.5）使用分析生成 . 2026-07-14*
