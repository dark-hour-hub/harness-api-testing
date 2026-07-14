# Node -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `Node` |
| **全限定名** | `org.dromara.warm.flow.core.entity.Node` |
| **类型** | 响应体 VO / 核心实体（外部库 warm-flow-core 1.8.5） |
| **所属模块** | 工作流管理 |
| **父类** | warm-flow 内部基类 |
| **序列化特性** | 由 warm-flow 库定义 |
| **说明** | warm-flow 流程节点核心实体，用于返回可驳回的前置节点信息（如 getBackTaskNode 接口的返回值）。来源为外部依赖，源码不可直接访问。 |

---

## 字段定义

### 响应体字段

> 以下字段基于 RuoYi-Vue-Plus 代码中的使用模式及 warm-flow 官方文档推断，实际字段以 warm-flow 1.8.5 库定义为准。

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| nodeCode | `nodeCode` | string | 否 | -- | -- | 节点编码 | `"node_start"` |
| nodeName | `nodeName` | string | 否 | -- | -- | 节点名称 | `"申请人"` |
| nodeType | `nodeType` | number | 否 | -- | -- | 节点类型（0开始节点 1中间节点 2结束节点 3互斥网关 4并行网关） | `0` |
| permissionFlag | `permissionFlag` | string | 否 | -- | -- | 权限标识 | `""` |
| nodeRatio | `nodeRatio` | string | 否 | -- | -- | 签署比例 | `"0"` |
| setHandler | `setHandler` | string | 否 | -- | -- | 指定办理人 | `""` |
| ext | `ext` | string | 否 | -- | -- | 节点扩展属性（JSON 格式） | `""` |

**字段备注**:
- `nodeType`: 枚举值 `0`=开始节点, `1`=中间节点, `2`=结束节点, `3`=互斥网关, `4`=并行网关
- `permissionFlag`: 办理人的权限标识
- 与 `FlowNode` 的区别：`Node` 是 warm-flow 核心层实体，用于计算引擎内部流转；`FlowNode` 是 ORM 层实体，包含数据库持久化字段
- 该实体用于 `GET /workflow/task/getBackTaskNode/{taskId}/{nowNodeCode}` 返回可在驳回时选择的前置节点列表
- 驳回时默认驳回到申请人节点（`nodeType=0` 的开始节点）

---

## JSON 示例

```json
{
  "nodeCode": "node_start",
  "nodeName": "申请人",
  "nodeType": 0,
  "permissionFlag": "",
  "nodeRatio": "0",
  "setHandler": "",
  "ext": ""
}
```

---

*基于 `org.dromara.warm.flow.core.entity.Node`（warm-flow 1.8.5）使用分析生成 . 2026-07-14*
