# SysDeptBo -- 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysDeptBo` |
| **全限定名** | `org.dromara.system.domain.bo.SysDeptBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 系统管理 |
| **父类** | `BaseEntity` |
| **序列化特性** | 无特殊配置（继承 BaseEntity） |
| **说明** | 部门业务对象，用于部门新增、编辑、查询等接口的请求参数，对应数据库表 `sys_dept` |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| searchValue | `searchValue` | string | 否 | — | — | 搜索值（不参与序列化 `@JsonIgnore`） | — |
| createDept | `createDept` | number | 否 | 插入时自动填充 | — | 创建部门 | `103` |
| createBy | `createBy` | number | 否 | 插入时自动填充 | — | 创建者 | `1` |
| createTime | `createTime` | string | 否 | 插入时自动填充 | — | 创建时间 | `"2026-07-14 10:00:00"` |
| updateBy | `updateBy` | number | 否 | 插入/更新时自动填充 | — | 更新者 | `1` |
| updateTime | `updateTime` | string | 否 | 插入/更新时自动填充 | — | 更新时间 | `"2026-07-14 12:00:00"` |
| params | `params` | object | 否 | — | `{}` | 请求参数 | — |
| deptId | `deptId` | number | 否 | — | — | 部门ID | `100` |
| parentId | `parentId` | number | 否 | — | — | 父部门ID（顶级部门为 `0`） | `0` |
| deptName | `deptName` | string | ✅ | `@NotBlank`；`@Size(min=0, max=30)` | — | 部门名称 | `"研发部"` |
| deptCategory | `deptCategory` | string | 否 | `@Size(min=0, max=100)` | — | 部门类别编码 | `"DEPT_RD"` |
| orderNum | `orderNum` | number | ✅ | `@NotNull` | — | 显示顺序 | `1` |
| leader | `leader` | number | 否 | — | — | 负责人（用户ID） | `1` |
| phone | `phone` | string | 否 | `@Size(min=0, max=11)` | — | 联系电话 | `"010-88888888"` |
| email | `email` | string | 否 | `@Email`；`@Size(min=0, max=50)` | — | 邮箱 | `"rd@example.com"` |
| status | `status` | string | 否 | — | — | 部门状态（`0` 正常、`1` 停用） | `"0"` |
| belongDeptId | `belongDeptId` | number | 否 | — | — | 归属部门ID（部门树） | `0` |

---

## JSON 示例

```json
{
  "parentId": 0,
  "deptName": "研发部",
  "deptCategory": "DEPT_RD",
  "orderNum": 1,
  "leader": 1,
  "phone": "010-88888888",
  "email": "rd@example.com",
  "status": "0"
}
```

---

*基于 `org.dromara.system.domain.bo.SysDeptBo` 源码生成 * 2026-07-14*
