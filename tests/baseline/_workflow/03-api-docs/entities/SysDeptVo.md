# SysDeptVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysDeptVo` |
| **全限定名** | `org.dromara.system.domain.vo.SysDeptVo` |
| **类型** | 响应体 VO |
| **所属模块** | 系统管理 |
| **父类** | 无（直接实现 `Serializable`） |
| **序列化特性** | 无特殊配置 |
| **说明** | 部门视图对象，用于部门列表、树形查询等接口的响应数据，支持 Excel 导出。对应数据库表 `sys_dept`，通过 `children` 字段支持树形结构 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| deptId | `deptId` | number | 否 | — | — | 部门ID | `100` |
| parentId | `parentId` | number | 否 | — | — | 父部门ID（顶级为 `0`） | `0` |
| parentName | `parentName` | string | 否 | — | — | 父部门名称 | `"总公司"` |
| ancestors | `ancestors` | string | 否 | — | — | 祖级列表（逗号分隔的上级部门ID串） | `"0,100"` |
| deptName | `deptName` | string | 否 | — | — | 部门名称 | `"研发部"` |
| deptCategory | `deptCategory` | string | 否 | — | — | 部门类别编码 | `"DEPT_RD"` |
| orderNum | `orderNum` | number | 否 | — | — | 显示顺序 | `1` |
| leader | `leader` | number | 否 | — | — | 负责人ID（用户ID） | `1` |
| leaderName | `leaderName` | string | 否 | — | — | 负责人名称 | `"管理员"` |
| phone | `phone` | string | 否 | — | — | 联系电话 | `"010-88888888"` |
| email | `email` | string | 否 | — | — | 邮箱 | `"rd@example.com"` |
| status | `status` | string | 否 | — | — | 部门状态（`0` 正常、`1` 停用） | `"0"` |
| createTime | `createTime` | string | 否 | — | — | 创建时间 | `"2025-01-01 10:00:00"` |
| children | `children` | array | 否 | — | `[]` | 子部门列表 `List<SysDeptVo>`（递归结构） | `[{"deptId":101,"deptName":"前端组"}]` |

**字段备注**:
- `ancestors`: 祖级列表，记录从顶级到当前部门的所有父级ID，如 `"0,100,101"` 表示顶级>总公司>研发部
- `children`: 递归嵌套 `SysDeptVo` 列表，构成部门树形结构。默认初始化为 `new ArrayList<>()`

---

## JSON 示例

```json
{
  "deptId": 100,
  "parentId": 0,
  "parentName": "总公司",
  "ancestors": "0",
  "deptName": "研发部",
  "deptCategory": "DEPT_RD",
  "orderNum": 1,
  "leader": 1,
  "leaderName": "管理员",
  "phone": "010-88888888",
  "email": "rd@example.com",
  "status": "0",
  "createTime": "2025-01-01 10:00:00",
  "children": [
    {
      "deptId": 101,
      "parentId": 100,
      "parentName": "研发部",
      "ancestors": "0,100",
      "deptName": "前端组",
      "orderNum": 1,
      "leader": 2,
      "leaderName": "张三",
      "status": "0",
      "children": []
    }
  ]
}
```

---

*基于 `org.dromara.system.domain.vo.SysDeptVo` 源码生成 * 2026-07-14*
