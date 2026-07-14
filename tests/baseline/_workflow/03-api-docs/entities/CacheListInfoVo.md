# CacheListInfoVo -- 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `CacheListInfoVo` |
| **全限定名** | `org.dromara.system.controller.monitor.CacheController.CacheListInfoVo` |
| **类型** | 响应体 VO |
| **所属模块** | 监控管理 |
| **父类** | 无（Java `record`） |
| **序列化特性** | 无特殊配置 |
| **说明** | 缓存监控信息视图对象（Java record），封装 Redis 运行信息、数据库大小和命令统计，用于缓存监控页面展示 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| info | `info` | object | 否 | — | — | Redis INFO 命令返回的全部属性信息（键值对集合） | `{"redis_version":"7.0.0","uptime_in_seconds":"86400",...}` |
| dbSize | `dbSize` | number | 否 | — | — | 当前数据库的键数量（DBSIZE 结果） | `1024` |
| commandStats | `commandStats` | array | 否 | — | — | Redis 命令统计列表，每项含 name（命令名）和 value（调用次数） | `[{"name":"get","value":"5000"},{"name":"set","value":"1200"}]` |

**字段备注**:
- `info`: Java 类型为 `java.util.Properties`，序列化为 JSON 时表现为键值对对象
- `commandStats`: Java 类型为 `List<Map<String, String>>`，单个元素为 `{"name": "...", "value": "..."}` 结构

---

## JSON 示例

```json
{
  "info": {
    "redis_version": "7.0.0",
    "uptime_in_seconds": "86400",
    "connected_clients": "10",
    "used_memory_human": "128M",
    "total_connections_received": "5000",
    "total_commands_processed": "50000"
  },
  "dbSize": 1024,
  "commandStats": [
    {"name": "get", "value": "5000"},
    {"name": "set", "value": "1200"},
    {"name": "del", "value": "800"},
    {"name": "hget", "value": "3000"}
  ]
}
```

---

*基于 `org.dromara.system.controller.monitor.CacheController.CacheListInfoVo` 源码生成 * 2026-07-14*
