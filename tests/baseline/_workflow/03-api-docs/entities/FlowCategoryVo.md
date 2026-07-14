# FlowCategoryVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `FlowCategoryVo` |
| **全限定名** | `org.dromara.workflow.domain.vo.FlowCategoryVo` |
| **类型** | 响应体 VO |
| **所属模块** | 工作流管理 |
| **父类** | 无（直接实现 Serializable） |
| **序列化特性** | 无特殊配置 |
| **说明** | 流程分类视图对象，对应 wf_category 表，用于流程分类列表展示 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| categoryId | `categoryId` | number | 否 | -- | -- | 流程分类ID | `1` |
| parentId | `parentId` | number | 否 | -- | -- | 父级分类ID | `0` |
| parentName | `parentName` | string | 否 | -- | -- | 父级分类名称，通过 `@Translation` 根据 parentId 翻译而来 | `"行政类"` |
| ancestors | `ancestors` | string | 否 | -- | -- | 祖级列表 | `"0,1"` |
| categoryName | `categoryName` | string | 否 | -- | -- | 流程分类名称 | `"人事审批"` |
| orderNum | `orderNum` | number | 否 | -- | -- | 显示顺序 | `1` |
| createTime | `createTime` | string | 否 | -- | -- | 创建时间 | `"2023-06-27 10:00:00"` |

**字段备注**:
- `parentName`: 通过 `@Translation(type = FlowConstant.CATEGORY_ID_TO_NAME, mapper = "parentId")` 自动翻译，根据 parentId 查找对应的分类名称
- `@ExcelIgnoreUnannotated`: 仅标注了 `@ExcelProperty` 的字段可导出（categoryId, categoryName, orderNum, createTime）
- `@AutoMapper(target = FlowCategory.class)`: 支持与 FlowCategory 实体自动映射

---

## JSON 示例

```json
{
  "categoryId": 1,
  "parentId": 0,
  "parentName": "根节点",
  "ancestors": "0",
  "categoryName": "人事审批",
  "orderNum": 1,
  "createTime": "2023-06-27 10:00:00"
}
```

---

*基于 `org.dromara.workflow.domain.vo.FlowCategoryVo` 源码生成 . 2026-07-14*
