# SysUserOnline -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysUserOnline` |
| **全限定名** | `org.dromara.system.domain.SysUserOnline` |
| **类型** | 响应体 VO |
| **所属模块** | 监控管理 |
| **父类** | 无 |
| **序列化特性** | 无特殊配置 |
| **说明** | 当前在线会话视图对象，从 Redis 缓存的 UserOnlineDTO 复制而来，用于在线用户监控列表 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| tokenId | `tokenId` | string | 否 | — | — | 会话编号（令牌 ID） | `"abc123-def456-xxx"` |
| deptName | `deptName` | string | 否 | — | — | 部门名称 | `"研发部"` |
| userName | `userName` | string | 否 | — | — | 用户账号 | `"admin"` |
| clientKey | `clientKey` | string | 否 | — | — | 客户端标识 | `"web"` |
| deviceType | `deviceType` | string | 否 | — | — | 设备类型 | `"PC"` |
| ipaddr | `ipaddr` | string | 否 | — | — | 登录 IP 地址 | `"192.168.1.100"` |
| loginLocation | `loginLocation` | string | 否 | — | — | 登录地址（登录地点） | `"北京市"` |
| browser | `browser` | string | 否 | — | — | 浏览器类型 | `"Chrome 120"` |
| os | `os` | string | 否 | — | — | 操作系统 | `"Windows 10"` |
| loginTime | `loginTime` | number | 否 | — | — | 登录时间（时间戳，毫秒） | `1720932000000` |

**字段备注**:
- `loginTime`: 类型为 `Long`（Unix 毫秒时间戳），与 SysLogininforVo 中 `loginTime` 的 `Date` 类型不同

---

## JSON 示例

```json
{
  "tokenId": "abc123-def456-xxx",
  "deptName": "研发部",
  "userName": "admin",
  "clientKey": "web",
  "deviceType": "PC",
  "ipaddr": "192.168.1.100",
  "loginLocation": "北京市",
  "browser": "Chrome 120",
  "os": "Windows 10",
  "loginTime": 1720932000000
}
```

---

*基于 `org.dromara.system.domain.SysUserOnline` 源码生成 * 2026-07-14*
