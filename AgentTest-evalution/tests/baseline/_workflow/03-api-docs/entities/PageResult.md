# PageResult — 分页响应包装（泛型）

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `PageResult` |
| **全限定名** | `com.czbank.aicgs.evaluation.common.api.PageResult` |
| **类型** | 分页响应包装（泛型 `PageResult<T>`） |
| **所属模块** | 通用（common） |
| **父类** | 无（record） |
| **序列化特性** | 无特殊配置（Jackson 默认）；构造时 `items` 复制为不可变列表 |
| **说明** | 分页数据包装，通常作为 `ApiResponse.data` 出现（`ApiResponse<PageResult<T>>`）。字段顺序 items/page/pageSize/total，pageSize 上限 100（Controller 层校验） |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| items | `items` | array（`T`[]） | ✅ | 非空列表（构造时 `List.copyOf` 需非 null） | — | 当前页数据（泛型 `T` 元素列表） | `[{...}, {...}]` |
| page | `page` | long | ✅ | ≥1（Controller 层校验） | `1` | 页码，从 1 开始 | `1` |
| pageSize | `pageSize` | long | ✅ | 1~100（Controller 层校验） | `20` | 每页条数，上限 100 | `20` |
| total | `total` | long | ✅ | — | — | 总记录数 | `42` |

**字段备注**（无则删除）:
- `items` 元素类型由泛型参数 `T` 决定（如 `AgentResponse`、`IndicatorResponse`、`TestCaseResponse`、`EvaluationTask`、`IndicatorResultResponse`、`CaseResultResponse`、`AgentCallResponse`、`EvaluationSchemeResponse`）

---

## JSON 示例

```json
{
  "items": [
    {
      "id": 1,
      "name": "示例条目"
    }
  ],
  "page": 1,
  "pageSize": 20,
  "total": 42
}
```

---

*基于 `com.czbank.aicgs.evaluation.common.api.PageResult` 源码生成 · 2026-08-19*