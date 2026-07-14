# SysConfigVo — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysConfigVo` |
| **全限定名** | `org.dromara.system.domain.vo.SysConfigVo` |
| **类型** | 响应体 VO |
| **所属模块** | 系统管理 |
| **父类** | 无（直接实现 `Serializable`） |
| **序列化特性** | 无特殊配置 |
| **说明** | 参数配置视图对象，用于系统参数配置列表查询、详情查看、按key查值等接口的响应数据封装；支持 Excel 导出 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| configId | `configId` | number | — | — | — | 参数主键 | `1` |
| configName | `configName` | string | — | — | — | 参数名称 | `"主框架页-默认皮肤样式名称"` |
| configKey | `configKey` | string | — | — | — | 参数键名（全局唯一） | `"sys.index.skinName"` |
| configValue | `configValue` | string | — | — | — | 参数键值 | `"skin-blue"` |
| configType | `configType` | string | — | — | — | 系统内置标记（Y=内置, N=自定义），使用 `sys_yes_no` 字典翻译 | `"Y"` |
| remark | `remark` | string | — | — | — | 备注 | `"蓝色皮肤"` |
| createTime | `createTime` | string | — | — | — | 创建时间（格式: yyyy-MM-dd HH:mm:ss） | `"2024-01-15 10:30:00"` |

**字段备注**:
- `configType`: 使用 `sys_yes_no` 字典翻译，Y=系统内置参数（不允许删除），N=用户自定义参数。
- `configKey`: 全局唯一的参数标识，也是缓存 key，可通过 `CacheNames.SYS_CONFIG` 缓存读取。
- `configValue`: 参数实际值，最大长度 500 字符。

---

## JSON 示例

```json
{
  "configId": 1,
  "configName": "主框架页-默认皮肤样式名称",
  "configKey": "sys.index.skinName",
  "configValue": "skin-blue",
  "configType": "Y",
  "remark": "蓝色皮肤",
  "createTime": "2024-01-15 10:30:00"
}
```

---

*基于 `org.dromara.system.domain.vo.SysConfigVo` 源码生成 · 2026-07-14*
