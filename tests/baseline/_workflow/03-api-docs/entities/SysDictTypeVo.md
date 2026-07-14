# SysDictTypeVo — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysDictTypeVo` |
| **全限定名** | `org.dromara.system.domain.vo.SysDictTypeVo` |
| **类型** | 响应体 VO |
| **所属模块** | 系统管理 |
| **父类** | 无（直接实现 `Serializable`） |
| **序列化特性** | 无特殊配置 |
| **说明** | 字典类型视图对象，用于字典类型列表查询、详情查看、缓存读取等接口的响应数据封装；支持 Excel 导出 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| dictId | `dictId` | number | — | — | — | 字典主键 | `1` |
| dictName | `dictName` | string | — | — | — | 字典名称 | `"用户性别"` |
| dictType | `dictType` | string | — | — | — | 字典类型（唯一标识，格式: 以字母开头，小写字母+数字+下划线） | `"sys_user_sex"` |
| remark | `remark` | string | — | — | — | 备注 | `"用户性别列表"` |
| createTime | `createTime` | string | — | — | — | 创建时间（格式: yyyy-MM-dd HH:mm:ss） | `"2024-01-15 10:30:00"` |

---

## JSON 示例

```json
{
  "dictId": 1,
  "dictName": "用户性别",
  "dictType": "sys_user_sex",
  "remark": "用户性别列表",
  "createTime": "2024-01-15 10:30:00"
}
```

---

*基于 `org.dromara.system.domain.vo.SysDictTypeVo` 源码生成 · 2026-07-14*
