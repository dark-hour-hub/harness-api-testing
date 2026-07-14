# TestLeaveVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `TestLeaveVo` |
| **全限定名** | `org.dromara.workflow.domain.vo.TestLeaveVo` |
| **类型** | 响应体 VO |
| **所属模块** | 工作流管理 |
| **父类** | 无（直接实现 Serializable） |
| **序列化特性** | `@JsonFormat(pattern = "yyyy-MM-dd")` 作用于 startDate、endDate |
| **说明** | 请假视图对象，对应 test_leave 表，用于展示请假申请记录 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | number | 否 | -- | -- | 主键 | `1` |
| applyCode | `applyCode` | string | 否 | -- | -- | 申请编号 | `"L20230721001"` |
| leaveType | `leaveType` | string | 否 | -- | -- | 请假类型 | `"年假"` |
| startDate | `startDate` | string | 否 | -- | -- | 开始时间，格式 yyyy-MM-dd | `"2023-07-25"` |
| endDate | `endDate` | string | 否 | -- | -- | 结束时间，格式 yyyy-MM-dd | `"2023-07-27"` |
| leaveDays | `leaveDays` | number | 否 | -- | -- | 请假天数 | `3` |
| remark | `remark` | string | 否 | -- | -- | 请假原因 | `"家中有事需要处理"` |
| status | `status` | string | 否 | -- | -- | 状态 | `"0"` |

**字段备注**:
- `@ExcelIgnoreUnannotated`: 仅标注了 `@ExcelProperty` 的字段可导出
- `@AutoMapper(target = TestLeave.class)`: 支持与 TestLeave 实体自动映射
- `startDate`, `endDate`: 通过 `@JsonFormat(pattern = "yyyy-MM-dd")` 控制序列化格式
- `leaveType`: 常见取值 "年假"、"事假"、"病假"、"婚假"、"产假"、"调休"等

---

## JSON 示例

```json
{
  "id": 1,
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

*基于 `org.dromara.workflow.domain.vo.TestLeaveVo` 源码生成 . 2026-07-14*
