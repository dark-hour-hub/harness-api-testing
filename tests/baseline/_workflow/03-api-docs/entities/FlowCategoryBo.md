# FlowCategoryBo -- 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `FlowCategoryBo` |
| **全限定名** | `org.dromara.workflow.domain.bo.FlowCategoryBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 工作流管理 |
| **父类** | `BaseEntity` |
| **序列化特性** | 无特殊配置 |
| **说明** | 流程分类业务对象，对应 wf_category 表，用于新增/编辑流程分类 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| categoryId | `categoryId` | number | 是(编辑) | `@NotNull`, groups=EditGroup | -- | 流程分类ID | `1` |
| parentId | `parentId` | number | 是 | `@NotNull`, groups={AddGroup, EditGroup} | -- | 父流程分类ID | `0` |
| categoryName | `categoryName` | string | 是 | `@NotBlank`, groups={AddGroup, EditGroup} | -- | 流程分类名称 | `"人事审批"` |
| orderNum | `orderNum` | number | 否 | -- | -- | 显示顺序 | `1` |
| searchValue | `searchValue` | string | 否 | -- | -- | 搜索值（继承自 BaseEntity） | `"人事"` |
| createDept | `createDept` | number | 否 | -- | -- | 创建部门ID（继承自 BaseEntity） | `103` |
| createBy | `createBy` | number | 否 | -- | -- | 创建者ID（继承自 BaseEntity） | `1` |
| createTime | `createTime` | string | 否 | -- | -- | 创建时间（继承自 BaseEntity） | `"2023-06-27 10:00:00"` |
| updateBy | `updateBy` | number | 否 | -- | -- | 更新者ID（继承自 BaseEntity） | `1` |
| updateTime | `updateTime` | string | 否 | -- | -- | 更新时间（继承自 BaseEntity） | `"2023-07-01 14:30:00"` |
| params | `params` | object | 否 | -- | -- | 额外参数（继承自 BaseEntity） | `{}` |

**字段备注**:
- `parentId`: 顶级分类的 parentId 为 0
- `params`: 由 `@JsonIgnore` 注解标记，不参与 JSON 序列化

---

## JSON 示例

```json
{
  "parentId": 0,
  "categoryName": "人事审批",
  "orderNum": 1
}
```

---

*基于 `org.dromara.workflow.domain.bo.FlowCategoryBo` 源码生成 . 2026-07-14*
