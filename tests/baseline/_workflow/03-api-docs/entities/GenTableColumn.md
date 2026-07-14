# GenTableColumn -- 业务对象（同时用于请求/响应）

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `GenTableColumn` |
| **全限定名** | `org.dromara.generator.domain.GenTableColumn` |
| **类型** | 业务对象（兼 DTO，同时用于请求体和响应体） |
| **所属模块** | 代码生成 |
| **父类** | `BaseEntity` |
| **序列化特性** | 无特殊配置（父类 `params` 字段为非空时包含） |
| **说明** | 代码生成业务字段表 `gen_table_column` 对应实体，描述表中每个列的代码生成配置（如是否列表/查询/编辑字段、控件类型等） |

---

## 字段定义

### 请求/响应字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| columnId | `columnId` | number | 否 | — | — | 编号（字段主键） | `1` |
| tableId | `tableId` | number | 否 | — | — | 归属表编号，关联 gen_table 主键 | `1` |
| columnName | `columnName` | string | 否 | — | — | 数据库列名称 | `"user_name"` |
| columnComment | `columnComment` | string | 否 | — | — | 列描述（数据库注释） | `"用户账号"` |
| columnType | `columnType` | string | 否 | — | — | 列类型（数据库原始类型，小写） | `"varchar(50)"` |
| javaType | `javaType` | string | 否 | — | — | JAVA 类型 | `"String"` |
| javaField | `javaField` | string | ✅ | `@NotBlank` | — | JAVA 字段名（驼峰） | `"userName"` |
| isPk | `isPk` | string | 否 | — | — | 是否主键（1=是） | `"0"` |
| isIncrement | `isIncrement` | string | 否 | — | — | 是否自增（1=是） | `"0"` |
| isRequired | `isRequired` | string | 否 | — | — | 是否必填（1=是） | `"1"` |
| isInsert | `isInsert` | string | 否 | — | — | 是否为插入字段（1=是） | `"1"` |
| isEdit | `isEdit` | string | 否 | — | — | 是否编辑字段（1=是） | `"1"` |
| isList | `isList` | string | 否 | — | — | 是否列表字段（1=是） | `"1"` |
| isQuery | `isQuery` | string | 否 | — | — | 是否查询字段（1=是） | `"1"` |
| queryType | `queryType` | string | 否 | — | — | 查询方式（EQ=等于, NE=不等于, GT=大于, LT=小于, LIKE=模糊, BETWEEN=范围） | `"LIKE"` |
| htmlType | `htmlType` | string | 否 | — | — | 显示类型（input=文本框, textarea=文本域, select=下拉框, checkbox=复选框, radio=单选框, datetime=日期控件, image=图片上传, upload=文件上传, editor=富文本） | `"input"` |
| dictType | `dictType` | string | 否 | — | — | 字典类型 | `"sys_user_sex"` |
| sort | `sort` | number | 否 | — | — | 排序号 | `1` |
| createDept | `createDept` | number | 否 | — | — | 创建部门（继承自 BaseEntity） | `103` |
| createBy | `createBy` | number | 否 | — | — | 创建者（继承自 BaseEntity） | `1` |
| createTime | `createTime` | string | 否 | — | — | 创建时间（继承自 BaseEntity） | `"2026-07-14 10:00:00"` |
| updateBy | `updateBy` | number | 否 | — | — | 更新者（继承自 BaseEntity） | `1` |
| updateTime | `updateTime` | string | 否 | — | — | 更新时间（继承自 BaseEntity） | `"2026-07-14 15:30:00"` |
| params | `params` | object | 否 | — | — | 请求参数（继承自 BaseEntity，非空序列化） | `{}` |

**字段备注**:
- `searchValue`: 搜索值（继承自 BaseEntity），`@JsonIgnore` 不参与序列化
- `isPk`, `isIncrement`, `isRequired`, `isInsert`, `isEdit`, `isList`, `isQuery`: 均为字符串 `"0"` 或 `"1"`，通过实例方法（如 `isPk()`）提供 boolean 判断
- `queryType`: 枚举值 — `"EQ"`, `"NE"`, `"GT"`, `"LT"`, `"LIKE"`, `"BETWEEN"`
- `htmlType`: 枚举值 — `"input"`, `"textarea"`, `"select"`, `"checkbox"`, `"radio"`, `"datetime"`, `"image"`, `"upload"`, `"editor"`

---

## JSON 示例

```json
{
  "columnId": 1,
  "tableId": 1,
  "columnName": "user_name",
  "columnComment": "用户账号",
  "columnType": "varchar(50)",
  "javaType": "String",
  "javaField": "userName",
  "isPk": "0",
  "isIncrement": "0",
  "isRequired": "1",
  "isInsert": "1",
  "isEdit": "1",
  "isList": "1",
  "isQuery": "1",
  "queryType": "LIKE",
  "htmlType": "input",
  "dictType": "",
  "sort": 1,
  "createDept": 103,
  "createBy": 1,
  "createTime": "2026-07-14 10:00:00",
  "updateBy": 1,
  "updateTime": "2026-07-14 15:30:00",
  "params": {}
}
```

---

*基于 `org.dromara.generator.domain.GenTableColumn` 源码生成 * 2026-07-14*
