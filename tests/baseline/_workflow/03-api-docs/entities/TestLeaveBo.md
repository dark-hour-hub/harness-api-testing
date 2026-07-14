# TestLeaveBo -- 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `TestLeaveBo` |
| **全限定名** | `org.dromara.workflow.domain.bo.TestLeaveBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 工作流管理 |
| **父类** | `BaseEntity` |
| **序列化特性** | `@JsonFormat(pattern = "yyyy-MM-dd")` 作用于 startDate、endDate |
| **说明** | 请假业务对象，对应 test_leave 表，用于发起请假审批流程 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | number | 是(编辑) | `@NotNull`, groups=EditGroup | -- | 主键 | `1` |
| flowCode | `flowCode` | string | 否 | -- | -- | 流程编码 | `"leave_apply"` |
| applyCode | `applyCode` | string | 否 | -- | -- | 申请编号 | `"L20230721001"` |
| leaveType | `leaveType` | string | 是 | `@NotBlank`, groups={AddGroup, EditGroup} | -- | 请假类型 | `"年假"` |
| startDate | `startDate` | string | 是 | `@NotNull`, groups={AddGroup, EditGroup} | -- | 开始时间，格式 yyyy-MM-dd | `"2023-07-25"` |
| endDate | `endDate` | string | 是 | `@NotNull`, groups={AddGroup, EditGroup} | -- | 结束时间，格式 yyyy-MM-dd | `"2023-07-27"` |
| leaveDays | `leaveDays` | number | 否 | -- | -- | 请假天数 | `3` |
| startLeaveDays | `startLeaveDays` | number | 否 | -- | -- | 开始时间（天数偏移） | `1` |
| endLeaveDays | `endLeaveDays` | number | 否 | -- | -- | 结束时间（天数偏移） | `3` |
| remark | `remark` | string | 否 | -- | -- | 请假原因 | `"家中有事需要处理"` |
| status | `status` | string | 否 | -- | -- | 状态 | `"0"` |
| searchValue | `searchValue` | string | 否 | -- | -- | 搜索值（继承自 BaseEntity） | `""` |
| createDept | `createDept` | number | 否 | -- | -- | 创建部门ID（继承自 BaseEntity） | `103` |
| createBy | `createBy` | number | 否 | -- | -- | 创建者ID（继承自 BaseEntity） | `1` |
| createTime | `createTime` | string | 否 | -- | -- | 创建时间（继承自 BaseEntity） | `"2023-07-21 09:00:00"` |
| updateBy | `updateBy` | number | 否 | -- | -- | 更新者ID（继承自 BaseEntity） | `1` |
| updateTime | `updateTime` | string | 否 | -- | -- | 更新时间（继承自 BaseEntity） | `"2023-07-21 14:00:00"` |
| params | `params` | object | 否 | -- | -- | 额外参数（继承自 BaseEntity） | `{}` |

**字段备注**:
- `startDate`, `endDate`: 前后端均使用 `yyyy-MM-dd` 格式，由 `@JsonFormat` 和 `@DateTimeFormat` 共同控制
- `leaveType`: 常见请假类型包括 "年假"、"事假"、"病假"、"婚假"、"产假"、"调休" 等
- `params`: 由 `@JsonIgnore` 注解标记，不参与 JSON 序列化

---

## JSON 示例

```json
{
  "flowCode": "leave_apply",
  "applyCode": "L20230721001",
  "leaveType": "年假",
  "startDate": "2023-07-25",
  "endDate": "2023-07-27",
  "leaveDays": 3,
  "remark": "家中有事需要处理",
  "status": "0"
}
```

---

*基于 `org.dromara.workflow.domain.bo.TestLeaveBo` 源码生成 . 2026-07-14*
