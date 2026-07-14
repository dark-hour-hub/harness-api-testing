# SysOperLogVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysOperLogVo` |
| **全限定名** | `org.dromara.system.domain.vo.SysOperLogVo` |
| **类型** | 响应体 VO |
| **所属模块** | 监控管理 |
| **父类** | 无（实现 `Serializable`） |
| **序列化特性** | 无特殊配置 |
| **说明** | 操作日志记录视图对象，用于操作日志列表查询和导出 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| operId | `operId` | number | 否 | — | — | 日志主键 ID | `2001` |
| tenantId | `tenantId` | string | 否 | — | — | 租户编号 | `"T0001"` |
| title | `title` | string | 否 | — | — | 模块标题 | `"用户管理"` |
| businessType | `businessType` | number | 否 | — | — | 业务类型（0=其它 1=新增 2=修改 3=删除，字典: sys_oper_type） | `2` |
| businessTypes | `businessTypes` | array | 否 | — | — | 业务类型数组（查询参数，非单条日志属性） | `[1, 2]` |
| method | `method` | string | 否 | — | — | 方法名称 | `"org.dromara.system.controller.SysUserController.edit()"` |
| requestMethod | `requestMethod` | string | 否 | — | — | 请求方式 | `"PUT"` |
| operatorType | `operatorType` | number | 否 | — | — | 操作类别（0=其它 1=后台用户 2=手机端用户） | `1` |
| operName | `operName` | string | 否 | — | — | 操作人员 | `"admin"` |
| deptName | `deptName` | string | 否 | — | — | 部门名称 | `"研发部"` |
| operUrl | `operUrl` | string | 否 | — | — | 请求 URL | `"/system/user"` |
| operIp | `operIp` | string | 否 | — | — | 主机地址（操作 IP） | `"192.168.1.100"` |
| operLocation | `operLocation` | string | 否 | — | — | 操作地点 | `"北京市"` |
| operParam | `operParam` | string | 否 | — | — | 请求参数 | `"{\"userId\":1,\"userName\":\"admin\"}"` |
| jsonResult | `jsonResult` | string | 否 | — | — | 返回参数（响应 JSON） | `"{\"code\":200,\"msg\":\"操作成功\"}"` |
| status | `status` | number | 否 | — | — | 操作状态（0=正常 1=异常，字典: sys_common_status） | `0` |
| errorMsg | `errorMsg` | string | 否 | — | — | 错误消息 | `""` |
| operTime | `operTime` | string | 否 | — | — | 操作时间 | `"2026-07-14 15:30:00"` |
| costTime | `costTime` | number | 否 | — | — | 消耗时间（毫秒） | `156` |

---

## JSON 示例

```json
{
  "operId": 2001,
  "tenantId": "T0001",
  "title": "用户管理",
  "businessType": 2,
  "method": "org.dromara.system.controller.SysUserController.edit()",
  "requestMethod": "PUT",
  "operatorType": 1,
  "operName": "admin",
  "deptName": "研发部",
  "operUrl": "/system/user",
  "operIp": "192.168.1.100",
  "operLocation": "北京市",
  "operParam": "{\"userId\":1,\"userName\":\"admin\"}",
  "jsonResult": "{\"code\":200,\"msg\":\"操作成功\"}",
  "status": 0,
  "errorMsg": "",
  "operTime": "2026-07-14 15:30:00",
  "costTime": 156
}
```

---

*基于 `org.dromara.system.domain.vo.SysOperLogVo` 源码生成 * 2026-07-14*
