# GenTable -- 业务对象（同时用于请求/响应）

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `GenTable` |
| **全限定名** | `org.dromara.generator.domain.GenTable` |
| **类型** | 业务对象（兼 DTO，同时用于请求体和响应体） |
| **所属模块** | 代码生成 |
| **父类** | `BaseEntity` |
| **序列化特性** | 无特殊配置（父类 `params` 字段为非空时包含） |
| **说明** | 代码生成业务表 `gen_table` 对应实体，用于代码生成配置的请求和响应。部分字段仅作为表单渲染辅助，不映射数据库（`@TableField(exist = false)`） |

---

## 字段定义

### 请求/响应字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| tableId | `tableId` | number | 否 | — | — | 编号（表主键） | `1` |
| dataName | `dataName` | string | ✅ | `@NotBlank` | — | 数据源名称 | `"master"` |
| tableName | `tableName` | string | ✅ | `@NotBlank` | — | 表名称 | `"sys_user"` |
| tableComment | `tableComment` | string | ✅ | `@NotBlank` | — | 表描述 | `"用户信息表"` |
| subTableName | `subTableName` | string | 否 | — | — | 关联父表的表名（主子表场景） | `"sys_user_detail"` |
| subTableFkName | `subTableFkName` | string | 否 | — | — | 本表关联父表的外键名 | `"user_id"` |
| className | `className` | string | ✅ | `@NotBlank` | — | 实体类名称（首字母大写） | `"SysUser"` |
| tplCategory | `tplCategory` | string | 否 | — | — | 使用的模板（crud=单表, tree=树表, sub=主子表） | `"crud"` |
| packageName | `packageName` | string | ✅ | `@NotBlank` | — | 生成包路径 | `"org.dromara.system"` |
| moduleName | `moduleName` | string | ✅ | `@NotBlank` | — | 生成模块名 | `"ruoyi-system"` |
| businessName | `businessName` | string | ✅ | `@NotBlank` | — | 生成业务名 | `"user"` |
| functionName | `functionName` | string | ✅ | `@NotBlank` | — | 生成功能名 | `"用户"` |
| functionAuthor | `functionAuthor` | string | ✅ | `@NotBlank` | — | 生成作者 | `"Lion Li"` |
| genType | `genType` | string | 否 | — | — | 生成代码方式（固定为 0=zip 压缩包） | `"0"` |
| genPath | `genPath` | string | 否 | — | — | 生成路径（兼容历史字段） | `"/"` |
| pkColumn | `pkColumn` | object | 否 | — | — | 主键信息（不映射数据库），嵌套 GenTableColumn 对象 | `{"columnId":1,"javaField":"userId",...}` |
| columns | `columns` | array | 否 | `@Valid` | — | 表列信息（不映射数据库），嵌套 GenTableColumn 对象列表 | `[{"columnId":1,...}]` |
| options | `options` | string | 否 | — | — | 其它生成选项（JSON 字符串） | `"{\"treeParentCode\":\"parent_id\"}"` |
| remark | `remark` | string | 否 | — | — | 备注 | `"用户管理核心表"` |
| treeCode | `treeCode` | string | 否 | — | — | 树编码字段（不映射数据库） | `"dept_id"` |
| treeParentCode | `treeParentCode` | string | 否 | — | — | 树父编码字段（不映射数据库） | `"parent_id"` |
| treeName | `treeName` | string | 否 | — | — | 树名称字段（不映射数据库） | `"dept_name"` |
| menuIds | `menuIds` | array | 否 | — | — | 菜单 ID 列表（不映射数据库） | `[100, 200]` |
| parentMenuId | `parentMenuId` | number | 否 | — | — | 上级菜单 ID（不映射数据库） | `100` |
| parentMenuName | `parentMenuName` | string | 否 | — | — | 上级菜单名称（不映射数据库） | `"系统管理"` |
| createDept | `createDept` | number | 否 | — | — | 创建部门（继承自 BaseEntity） | `103` |
| createBy | `createBy` | number | 否 | — | — | 创建者（继承自 BaseEntity） | `1` |
| createTime | `createTime` | string | 否 | — | — | 创建时间（继承自 BaseEntity） | `"2026-07-14 10:00:00"` |
| updateBy | `updateBy` | number | 否 | — | — | 更新者（继承自 BaseEntity） | `1` |
| updateTime | `updateTime` | string | 否 | — | — | 更新时间（继承自 BaseEntity） | `"2026-07-14 15:30:00"` |
| params | `params` | object | 否 | — | — | 请求参数（继承自 BaseEntity，非空序列化） | `{"beginTime":"2026-01-01","endTime":"2026-12-31"}` |

**字段备注**:
- `searchValue`: 搜索值（继承自 BaseEntity），`@JsonIgnore` 不参与序列化
- `pkColumn`, `columns`, `treeCode`, `treeParentCode`, `treeName`, `menuIds`, `parentMenuId`, `parentMenuName`: `@TableField(exist = false)`，不映射数据库字段，仅作为内存辅助属性
- `tplCategory`: 枚举值 — `"crud"` (单表操作), `"tree"` (树表操作), `"sub"` (主子表操作)
- `genType`: 固定为 `"0"` (zip 压缩包下载)

---

## JSON 示例

```json
{
  "tableId": 1,
  "dataName": "master",
  "tableName": "sys_user",
  "tableComment": "用户信息表",
  "className": "SysUser",
  "tplCategory": "crud",
  "packageName": "org.dromara.system",
  "moduleName": "ruoyi-system",
  "businessName": "user",
  "functionName": "用户",
  "functionAuthor": "Lion Li",
  "genType": "0",
  "genPath": "/",
  "options": "",
  "remark": "用户管理核心表",
  "createDept": 103,
  "createBy": 1,
  "createTime": "2026-07-14 10:00:00",
  "updateBy": 1,
  "updateTime": "2026-07-14 15:30:00",
  "params": {},
  "columns": [
    {
      "columnId": 1,
      "columnName": "user_id",
      "columnComment": "用户ID",
      "javaField": "userId",
      "isPk": "1",
      "isRequired": "1",
      "isInsert": "1",
      "isEdit": "0",
      "isList": "1",
      "isQuery": "1",
      "sort": 1
    }
  ]
}
```

---

*基于 `org.dromara.generator.domain.GenTable` 源码生成 * 2026-07-14*
