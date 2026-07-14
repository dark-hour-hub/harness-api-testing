# SysDictDataVo — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysDictDataVo` |
| **全限定名** | `org.dromara.system.domain.vo.SysDictDataVo` |
| **类型** | 响应体 VO |
| **所属模块** | 系统管理 |
| **父类** | 无（直接实现 `Serializable`） |
| **序列化特性** | 无特殊配置 |
| **说明** | 字典数据视图对象，用于字典数据列表查询、按类型查询字典数据、详情查看等接口的响应数据封装；支持 Excel 导出 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| dictCode | `dictCode` | number | — | — | — | 字典编码（主键） | `1` |
| dictSort | `dictSort` | number | — | — | — | 字典排序（数值越小越靠前） | `0` |
| dictLabel | `dictLabel` | string | — | — | — | 字典标签（前端展示用） | `"男"` |
| dictValue | `dictValue` | string | — | — | — | 字典键值（后端存储用） | `"0"` |
| dictType | `dictType` | string | — | — | — | 字典类型 | `"sys_user_sex"` |
| cssClass | `cssClass` | string | — | — | — | 样式属性（其他样式扩展） | `""` |
| listClass | `listClass` | string | — | — | — | 表格回显样式（如 `"default"`, `"primary"`, `"success"`, `"warning"`, `"danger"`） | `"success"` |
| isDefault | `isDefault` | string | — | — | — | 是否默认值（Y=是, N=否） | `"N"` |
| remark | `remark` | string | — | — | — | 备注 | `"性别男"` |
| createTime | `createTime` | string | — | — | — | 创建时间（格式: yyyy-MM-dd HH:mm:ss） | `"2024-01-15 10:30:00"` |

---

## JSON 示例

```json
{
  "dictCode": 1,
  "dictSort": 0,
  "dictLabel": "男",
  "dictValue": "0",
  "dictType": "sys_user_sex",
  "cssClass": "",
  "listClass": "success",
  "isDefault": "N",
  "remark": "性别男",
  "createTime": "2024-01-15 10:30:00"
}
```

---

*基于 `org.dromara.system.domain.vo.SysDictDataVo` 源码生成 · 2026-07-14*
