# SysLogininforVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysLogininforVo` |
| **全限定名** | `org.dromara.system.domain.vo.SysLogininforVo` |
| **类型** | 响应体 VO |
| **所属模块** | 监控管理 |
| **父类** | 无（实现 `Serializable`） |
| **序列化特性** | 无特殊配置 |
| **说明** | 系统访问记录（登录日志）视图对象，用于登录日志列表查询和导出 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| infoId | `infoId` | number | 否 | — | — | 访问记录 ID | `1001` |
| tenantId | `tenantId` | string | 否 | — | — | 租户编号 | `"T0001"` |
| userName | `userName` | string | 否 | — | — | 用户账号 | `"admin"` |
| clientKey | `clientKey` | string | 否 | — | — | 客户端标识 | `"web"` |
| deviceType | `deviceType` | string | 否 | — | — | 设备类型（字典: sys_device_type） | `"PC"` |
| status | `status` | string | 否 | — | — | 登录状态（0=成功 1=失败，字典: sys_common_status） | `"0"` |
| ipaddr | `ipaddr` | string | 否 | — | — | 登录 IP 地址 | `"192.168.1.100"` |
| loginLocation | `loginLocation` | string | 否 | — | — | 登录地点 | `"北京市"` |
| browser | `browser` | string | 否 | — | — | 浏览器类型 | `"Chrome 120"` |
| os | `os` | string | 否 | — | — | 操作系统 | `"Windows 10"` |
| msg | `msg` | string | 否 | — | — | 提示消息（成功或失败信息） | `"登录成功"` |
| loginTime | `loginTime` | string | 否 | — | — | 访问时间 | `"2026-07-14 08:00:00"` |

---

## JSON 示例

```json
{
  "infoId": 1001,
  "tenantId": "T0001",
  "userName": "admin",
  "clientKey": "web",
  "deviceType": "PC",
  "status": "0",
  "ipaddr": "192.168.1.100",
  "loginLocation": "北京市",
  "browser": "Chrome 120",
  "os": "Windows 10",
  "msg": "登录成功",
  "loginTime": "2026-07-14 08:00:00"
}
```

---

*基于 `org.dromara.system.domain.vo.SysLogininforVo` 源码生成 * 2026-07-14*
