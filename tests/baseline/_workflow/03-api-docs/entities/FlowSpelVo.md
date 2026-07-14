# FlowSpelVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `FlowSpelVo` |
| **全限定名** | `org.dromara.workflow.domain.vo.FlowSpelVo` |
| **类型** | 响应体 VO |
| **所属模块** | 工作流管理 |
| **父类** | 无（直接实现 Serializable） |
| **序列化特性** | 无特殊配置 |
| **说明** | 流程 SpEL 表达式定义视图对象，对应 flow_spel 表，用于展示 SpEL 表达式配置列表 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| id | `id` | number | 否 | -- | -- | 主键ID | `1` |
| componentName | `componentName` | string | 否 | -- | -- | 组件名称 | `"SysUserService"` |
| methodName | `methodName` | string | 否 | -- | -- | 方法名 | `"selectUserByDept"` |
| methodParams | `methodParams` | string | 否 | -- | -- | 参数 | `"deptId"` |
| viewSpel | `viewSpel` | string | 否 | -- | -- | 预览 SpEL 值 | `"@sysUserService.selectUserByDept(deptId)"` |
| status | `status` | string | 否 | -- | -- | 状态（0正常 1停用） | `"0"` |
| remark | `remark` | string | 否 | -- | -- | 备注 | `"按部门查找审批人"` |
| createTime | `createTime` | string | 否 | -- | -- | 创建时间 | `"2025-07-04 09:00:00"` |

**字段备注**:
- `status`: 枚举值 `"0"`=正常, `"1"`=停用，Excel 导出时使用 `@ExcelDictFormat(readConverterExp = "0=正常,1=停用")` 格式化
- `@ExcelIgnoreUnannotated`: 仅标注了 `@ExcelProperty` 的字段可导出
- `@AutoMapper(target = FlowSpel.class)`: 支持与 FlowSpel 实体自动映射

---

## JSON 示例

```json
{
  "id": 1,
  "componentName": "SysUserService",
  "methodName": "selectUserByDept",
  "methodParams": "deptId",
  "viewSpel": "@sysUserService.selectUserByDept(deptId)",
  "status": "0",
  "remark": "按部门查找审批人",
  "createTime": "2025-07-04 09:00:00"
}
```

---

*基于 `org.dromara.workflow.domain.vo.FlowSpelVo` 源码生成 . 2026-07-14*
