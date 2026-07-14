# SysPostVo — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysPostVo` |
| **全限定名** | `org.dromara.system.domain.vo.SysPostVo` |
| **类型** | 响应体 VO |
| **所属模块** | 系统管理 |
| **父类** | 无（直接实现 `Serializable`） |
| **序列化特性** | 无特殊配置 |
| **说明** | 岗位信息视图对象，用于岗位列表查询、详情查看等接口的响应数据封装；支持 Excel 导出 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| postId | `postId` | number | — | — | — | 岗位ID | `1` |
| deptId | `deptId` | number | — | — | — | 部门id | `103` |
| postCode | `postCode` | string | — | — | — | 岗位编码 | `"ceo"` |
| postName | `postName` | string | — | — | — | 岗位名称 | `"董事长"` |
| postCategory | `postCategory` | string | — | — | — | 岗位类别编码 | `"manager"` |
| postSort | `postSort` | number | — | — | — | 显示顺序 | `1` |
| status | `status` | string | — | — | — | 状态（0=正常, 1=停用） | `"0"` |
| remark | `remark` | string | — | — | — | 备注 | `""` |
| createTime | `createTime` | string | — | — | — | 创建时间（格式: yyyy-MM-dd HH:mm:ss） | `"2024-01-15 10:30:00"` |
| deptName | `deptName` | string | — | — | — | 部门名称（通过 `@Translation` 从 `deptId` 自动翻译） | `"总公司"` |
| address | `address` | string | — | — | — | 地址（自定义扩展字段，如 `"LosAngeles"`） | `"LosAngeles"` |

**字段备注**:
- `deptName`: 由 `@Translation(type=DEPT_ID_TO_NAME, mapper="deptId")` 翻译注解自动填充，根据 `deptId` 查询部门名称。
- `address`: <span style="color:orange">**[新增]**</span> 非数据库字段，在 `SysPostServiceImpl.selectPostList()` 中被硬编码为 `"LosAngeles"`，属于示例扩展字段。
- `status`: 使用 `sys_normal_disable` 字典翻译（0=正常, 1=停用）。

---

## JSON 示例

```json
{
  "postId": 1,
  "deptId": 103,
  "postCode": "ceo",
  "postName": "董事长",
  "postCategory": "manager",
  "postSort": 1,
  "status": "0",
  "remark": "",
  "createTime": "2024-01-15 10:30:00",
  "deptName": "总公司",
  "address": "LosAngeles"
}
```

---

*基于 `org.dromara.system.domain.vo.SysPostVo` 源码生成 · 2026-07-14*
