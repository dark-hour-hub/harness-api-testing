# FlowNode -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `FlowNode` |
| **全限定名** | `org.dromara.warm.flow.orm.entity.FlowNode` |
| **类型** | 响应体 VO / ORM 实体（外部库 warm-flow-mybatis-plus-sb3-starter 1.8.5） |
| **所属模块** | 工作流管理 |
| **父类** | warm-flow 内部基类 |
| **序列化特性** | 由 warm-flow 库定义 |
| **说明** | warm-flow 流程节点 ORM 实体，用于返回流程的节点信息列表（如 getNextNodeList 接口的返回值）。来源为外部依赖，源码不可直接访问。 |

---

## 字段定义

### 响应体字段

> 以下字段基于 RuoYi-Vue-Plus 代码中的使用模式及 warm-flow 官方文档推断，实际字段以 warm-flow 1.8.5 库定义为准。

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | number | 否 | -- | -- | 节点ID | `5001` |
| definitionId | `definitionId` | number | 否 | -- | -- | 对应流程定义表的ID | `100` |
| nodeCode | `nodeCode` | string | 否 | -- | -- | 节点编码 | `"node_approval"` |
| nodeName | `nodeName` | string | 否 | -- | -- | 节点名称 | `"部门经理审批"` |
| nodeType | `nodeType` | number | 否 | -- | -- | 节点类型（0开始节点 1中间节点 2结束节点 3互斥网关 4并行网关） | `1` |
| permissionFlag | `permissionFlag` | string | 否 | -- | -- | 权限标识，配置办理人规则 | `"role:dept_manager"` |
| nodeRatio | `nodeRatio` | string | 否 | -- | -- | 签署比例/会签票签配置，大于0为票签或会签 | `"0"` |
| version | `version` | string | 否 | -- | -- | 版本号 | `"1"` |
| skipAnyNode | `skipAnyNode` | string | 否 | -- | -- | 是否可以跳转到任意节点 | `"N"` |
| coordinate | `coordinate` | string | 否 | -- | -- | 节点在流程图中的坐标位置 | `"400,200"` |
| ext | `ext` | string | 否 | -- | -- | 节点扩展属性（JSON 格式），存储节点级别的自定义配置 | `""` |
| createTime | `createTime` | string | 否 | -- | -- | 创建时间 | `"2023-06-15 08:00:00"` |
| updateTime | `updateTime` | string | 否 | -- | -- | 更新时间 | `"2023-07-01 16:30:00"` |

**字段备注**:
- `nodeType`: 枚举值 `0`=开始节点, `1`=中间节点, `2`=结束节点, `3`=互斥网关, `4`=并行网关
- `nodeRatio`: 会签/票签的通过比例值，为 `"0"` 或空表示非会签模式；为数字（如 `"0.5"` 或正整数）表示需要 50% 或指定人数通过
- `permissionFlag`: 办理人权限标识，可用格式包括角色标识、用户ID、SpEL 表达式等
- 与 `Node` 的区别：`FlowNode` 是 ORM 层实体，包含数据库映射字段（id, createTime, updateTime 等）；`Node` 是核心实体，不含 ORM 特定字段
- `ext`: 可包含 copySetting（抄送配置）、variables（自定义参数）等节点级别扩展信息

---

## JSON 示例

```json
{
  "id": 5001,
  "definitionId": 100,
  "nodeCode": "node_approval",
  "nodeName": "部门经理审批",
  "nodeType": 1,
  "permissionFlag": "role:dept_manager",
  "nodeRatio": "0",
  "version": "1",
  "skipAnyNode": "N",
  "coordinate": "400,200",
  "ext": "",
  "createTime": "2023-06-15 08:00:00",
  "updateTime": "2023-07-01 16:30:00"
}
```

---

*基于 `org.dromara.warm.flow.orm.entity.FlowNode`（warm-flow 1.8.5）使用分析生成 . 2026-07-14*
