# FlowSpelBo -- 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `FlowSpelBo` |
| **全限定名** | `org.dromara.workflow.domain.bo.FlowSpelBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 工作流管理 |
| **父类** | `BaseEntity` |
| **序列化特性** | 无特殊配置 |
| **说明** | 流程 SpEL 表达式定义业务对象，对应 flow_spel 表，用于管理自定义 SpEL 表达式 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | number | 否 | -- | -- | 主键ID | `1` |
| componentName | `componentName` | string | 否 | -- | -- | 组件名称 | `"SysUserService"` |
| methodName | `methodName` | string | 否 | -- | -- | 方法名 | `"selectUserByDept"` |
| methodParams | `methodParams` | string | 否 | -- | -- | 方法参数 | `"deptId"` |
| viewSpel | `viewSpel` | string | 是 | `@NotBlank`, groups={AddGroup, EditGroup} | -- | 预览 SpEL 值 | `"@sysUserService.selectUserByDept(deptId)"` |
| status | `status` | string | 是 | `@NotBlank`, groups={AddGroup, EditGroup} | -- | 状态（0正常 1停用） | `"0"` |
| remark | `remark` | string | 否 | -- | -- | 备注 | `"按部门查找审批人"` |
| searchValue | `searchValue` | string | 否 | -- | -- | 搜索值（继承自 BaseEntity） | `""` |
| createDept | `createDept` | number | 否 | -- | -- | 创建部门ID（继承自 BaseEntity） | `103` |
| createBy | `createBy` | number | 否 | -- | -- | 创建者ID（继承自 BaseEntity） | `1` |
| createTime | `createTime` | string | 否 | -- | -- | 创建时间（继承自 BaseEntity） | `"2025-07-04 09:00:00"` |
| updateBy | `updateBy` | number | 否 | -- | -- | 更新者ID（继承自 BaseEntity） | `1` |
| updateTime | `updateTime` | string | 否 | -- | -- | 更新时间（继承自 BaseEntity） | `"2025-07-05 16:20:00"` |
| params | `params` | object | 否 | -- | -- | 额外参数（继承自 BaseEntity） | `{}` |

**字段备注**:
- `status`: 枚举值 `"0"`=正常, `"1"`=停用
- `params`: 由 `@JsonIgnore` 注解标记，不参与 JSON 序列化

---

## JSON 示例

```json
{
  "componentName": "SysUserService",
  "methodName": "selectUserByDept",
  "methodParams": "deptId",
  "viewSpel": "@sysUserService.selectUserByDept(deptId)",
  "status": "0",
  "remark": "按部门查找审批人"
}
```

---

*基于 `org.dromara.workflow.domain.bo.FlowSpelBo` 源码生成 . 2026-07-14*
