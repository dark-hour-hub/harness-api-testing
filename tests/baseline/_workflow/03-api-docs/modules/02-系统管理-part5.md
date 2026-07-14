# 系统管理 Part 5 — 通知公告 + 参数配置 + 客户端管理 API 文档

> Controllers: `SysNoticeController`, `SysConfigController`, `SysClientController` | Base URL: `http://localhost:8080` | Auth: Sa-Token JWT `Authorization: Bearer {token}` + `clientid: {value}`

## 请求头

| 头名称 | 值 | 说明 |
|--------|-----|------|
| Content-Type | `application/json` | 请求体格式；文件下载接口无需 |
| Authorization | `Bearer {token}` | Sa-Token JWT 令牌，登录后获取 |
| clientid | `e5cd7e4891bf95d1d19206ce24a7b32e` | 客户端 ID，与 Token 绑定 |

---

## 一、通知公告

### 1 获取通知公告列表

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/system/notice/list` |
| **接口说明** | 分页查询通知公告列表，支持按标题、类型、创建人筛选，按公告ID升序排列 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:notice:list` |
| **标签** | 系统管理-通知公告 |

---

#### 请求

**请求头**: [认证]

**查询参数**:

| 参数名 | 类型 | 必填 | 匹配方式 | 说明 | 示例 |
|--------|------|:---:|:---:|------|------|
| `pageNum` | Integer | 否 | — | 当前页码，默认 1 | `1` |
| `pageSize` | Integer | 否 | — | 每页条数，默认 10 | `10` |
| `orderByColumn` | String | 否 | — | 排序列名 | `"createTime"` |
| `isAsc` | String | 否 | — | 升序/降序 (asc/desc) | `"desc"` |
| `noticeTitle` | String | 否 | like | 公告标题（模糊匹配） | `"系统升级"` |
| `noticeType` | String | 否 | eq | 公告类型（1=通知, 2=公告） | `"1"` |
| `createByName` | String | 否 | eq | 创建人名称（先按名称查用户ID，再按创建人ID精确匹配） | `"管理员"` |

---

#### 响应

##### 成功响应 — HTTP 200

分页列表，数据项为 [SysNoticeVo](../entities/SysNoticeVo.md)。

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "rows": [
      {
        "noticeId": 1,
        "noticeTitle": "关于系统升级的通知",
        "noticeType": "1",
        "noticeContent": "<p>系统将于2024年7月20日进行升级维护。</p>",
        "status": "0",
        "remark": "",
        "createBy": 1,
        "createByName": "管理员",
        "createTime": "2024-01-15 10:30:00"
      }
    ],
    "total": 10
  }
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |

---

### 2 根据通知公告编号获取详细信息

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/system/notice/{noticeId}` |
| **接口说明** | 根据公告ID查询单条通知公告的详细信息 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:notice:query` |
| **标签** | 系统管理-通知公告 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `noticeId` | Long | 是 | 公告ID | `1` |

---

#### 响应

##### 成功响应 — HTTP 200

[SysNoticeVo](../entities/SysNoticeVo.md)

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "noticeId": 1,
    "noticeTitle": "关于系统升级的通知",
    "noticeType": "1",
    "noticeContent": "<p>系统将于2024年7月20日进行升级维护。</p>",
    "status": "0",
    "remark": "",
    "createBy": 1,
    "createByName": "管理员",
    "createTime": "2024-01-15 10:30:00"
  }
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 200 | 查询成功 | `"操作成功"` |

---

### 3 新增通知公告

| 属性 | 值 |
|------|-----|
| **请求方式** | `POST` |
| **接口路径** | `/system/notice` |
| **接口说明** | 新增一条通知公告，成功后通过 SSE 向所有在线用户推送公告消息 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:notice:add` |
| **标签** | 系统管理-通知公告 |
| **防重提交** | 开启（`@RepeatSubmit`） |

---

#### 请求

**请求头**: [认证]

**请求体**: [SysNoticeBo](../entities/SysNoticeBo.md)

```json
{
  "noticeTitle": "关于系统升级的通知",
  "noticeType": "1",
  "noticeContent": "<p>系统将于2024年7月20日进行升级维护，届时请勿登录系统。</p>",
  "status": "0"
}
```

---

#### 响应

##### 成功响应 — HTTP 200

```json
{
  "code": 200,
  "msg": "操作成功"
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | `noticeTitle` 为空 | `"公告标题不能为空"` |
| 200 | 500 | `noticeTitle` 超过 50 个字符 | `"公告标题不能超过50个字符"` |
| 200 | 500 | `noticeTitle` 包含脚本字符（XSS） | `"公告标题不能包含脚本字符"` |
| 200 | 500 | 数据库插入失败（返回行数 <= 0） | `"操作失败"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 防重提交 | 使用 Sa-Token `@RepeatSubmit` 注解，防止短时间内重复提交同一公告 |
| SSE 推送 | 新增成功后，通过 `SseMessageUtils.publishAll()` 向所有在线用户推送公告消息，格式为 `[{类型名称}] {公告标题}` |
| 字典翻译 | 公告类型 `noticeType` 通过字典表 `sys_notice_type` 翻译为中文名称用于推送消息 |

---

### 4 修改通知公告

| 属性 | 值 |
|------|-----|
| **请求方式** | `PUT` |
| **接口路径** | `/system/notice` |
| **接口说明** | 修改已有通知公告的信息 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:notice:edit` |
| **标签** | 系统管理-通知公告 |
| **防重提交** | 开启（`@RepeatSubmit`） |

---

#### 请求

**请求头**: [认证]

**请求体**: [SysNoticeBo](../entities/SysNoticeBo.md)（需包含 `noticeId`）

```json
{
  "noticeId": 1,
  "noticeTitle": "关于系统升级的通知（更新）",
  "noticeType": "1",
  "noticeContent": "<p>系统升级时间调整为2024年7月22日。</p>",
  "status": "0"
}
```

---

#### 响应

##### 成功响应 — HTTP 200

```json
{
  "code": 200,
  "msg": "操作成功"
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | `noticeTitle` 为空 | `"公告标题不能为空"` |
| 200 | 500 | `noticeTitle` 超过 50 个字符 | `"公告标题不能超过50个字符"` |
| 200 | 500 | `noticeTitle` 包含脚本字符（XSS） | `"公告标题不能包含脚本字符"` |
| 200 | 500 | 数据库更新失败（返回行数 <= 0） | `"操作失败"` |

---

### 5 删除通知公告

| 属性 | 值 |
|------|-----|
| **请求方式** | `DELETE` |
| **接口路径** | `/system/notice/{noticeIds}` |
| **接口说明** | 批量删除通知公告，支持一次删除多个（传递多个ID，逗号分隔） |
| **认证方式** | 需要认证 |
| **权限要求** | `system:notice:remove` |
| **标签** | 系统管理-通知公告 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `noticeIds` | Long[] | 是 | 公告ID数组，逗号分隔 | `1,2,3` |

---

#### 响应

##### 成功响应 — HTTP 200

```json
{
  "code": 200,
  "msg": "操作成功"
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | 数据库删除失败（返回行数 <= 0） | `"操作失败"` |

---

## 二、参数配置

### 6 获取参数配置列表

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/system/config/list` |
| **接口说明** | 分页查询参数配置列表，支持按参数名称（模糊）、参数键名（模糊）、参数类型（精确）、创建时间区间筛选，按参数ID升序排列 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:config:list` |
| **标签** | 系统管理-参数配置 |

---

#### 请求

**请求头**: [认证]

**查询参数**:

| 参数名 | 类型 | 必填 | 匹配方式 | 说明 | 示例 |
|--------|------|:---:|:---:|------|------|
| `pageNum` | Integer | 否 | — | 当前页码，默认 1 | `1` |
| `pageSize` | Integer | 否 | — | 每页条数，默认 10 | `10` |
| `orderByColumn` | String | 否 | — | 排序列名 | `"configId"` |
| `isAsc` | String | 否 | — | 升序/降序 (asc/desc) | `"asc"` |
| `configName` | String | 否 | like | 参数名称（模糊匹配） | `"皮肤"` |
| `configKey` | String | 否 | like | 参数键名（模糊匹配） | `"sys.index"` |
| `configType` | String | 否 | eq | 系统内置标记（Y=内置, N=自定义） | `"Y"` |
| `params[beginTime]` | String | 否 | between | 创建开始时间 | `"2024-01-01"` |
| `params[endTime]` | String | 否 | between | 创建结束时间 | `"2024-12-31"` |

> **注意**: `beginTime` 和 `endTime` 必须同时传入才会生效，通过 `params` 嵌套参数传递。

---

#### 响应

##### 成功响应 — HTTP 200

分页列表，数据项为 [SysConfigVo](../entities/SysConfigVo.md)。

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "rows": [
      {
        "configId": 1,
        "configName": "主框架页-默认皮肤样式名称",
        "configKey": "sys.index.skinName",
        "configValue": "skin-blue",
        "configType": "Y",
        "remark": "蓝色皮肤",
        "createTime": "2024-01-15 10:30:00"
      }
    ],
    "total": 50
  }
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |

---

### 7 导出参数配置列表

| 属性 | 值 |
|------|-----|
| **请求方式** | `POST` |
| **接口路径** | `/system/config/export` |
| **接口说明** | 按查询条件导出参数配置数据为 Excel 文件（.xlsx） |
| **认证方式** | 需要认证 |
| **权限要求** | `system:config:export` |
| **标签** | 系统管理-参数配置 |

---

#### 请求

**请求头**: [认证]

**查询参数**: 同接口6（参数配置列表查询），无需分页参数。

---

#### 响应

##### 成功响应 — HTTP 200

直接返回 Excel 文件流（`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`），文件名由 `ExcelUtil.exportExcel()` 自动生成。

```json
{
  "code": 200,
  "msg": "操作成功"
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |

---

### 8 根据参数编号获取详细信息

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/system/config/{configId}` |
| **接口说明** | 根据参数ID查询单条参数配置的详细信息 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:config:query` |
| **标签** | 系统管理-参数配置 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `configId` | Long | 是 | 参数ID | `1` |

---

#### 响应

##### 成功响应 — HTTP 200

[SysConfigVo](../entities/SysConfigVo.md)

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "configId": 1,
    "configName": "主框架页-默认皮肤样式名称",
    "configKey": "sys.index.skinName",
    "configValue": "skin-blue",
    "configType": "Y",
    "remark": "蓝色皮肤",
    "createTime": "2024-01-15 10:30:00"
  }
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 查询成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |

---

### 9 根据参数键名查询参数值

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/system/config/configKey/{configKey}` |
| **接口说明** | 根据参数键名查询参数值，返回字符串类型的参数值；使用 `CacheNames.SYS_CONFIG` 缓存 |
| **认证方式** | 需要认证 |
| **权限要求** | 无 |
| **标签** | 系统管理-参数配置 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `configKey` | String | 是 | 参数键名 | `"sys.index.skinName"` |

---

#### 响应

##### 成功响应 — HTTP 200

返回参数键名对应的参数值字符串。

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": "skin-blue"
}
```

当键名不存在时，返回空字符串。

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": ""
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 查询成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |

---

### 10 新增参数配置

| 属性 | 值 |
|------|-----|
| **请求方式** | `POST` |
| **接口路径** | `/system/config` |
| **接口说明** | 新增一条参数配置，新增成功后自动写入 `CacheNames.SYS_CONFIG` 缓存（key 为 `configKey`） |
| **认证方式** | 需要认证 |
| **权限要求** | `system:config:add` |
| **标签** | 系统管理-参数配置 |
| **防重提交** | 开启（`@RepeatSubmit`） |

---

#### 请求

**请求头**: [认证]

**请求体**: [SysConfigBo](../entities/SysConfigBo.md)

```json
{
  "configName": "主框架页-默认皮肤样式名称",
  "configKey": "sys.index.skinName",
  "configValue": "skin-blue",
  "configType": "Y",
  "remark": "蓝色皮肤"
}
```

---

#### 响应

##### 成功响应 — HTTP 200

```json
{
  "code": 200,
  "msg": "操作成功"
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | `configName` 为空 | `"参数名称不能为空"` |
| 200 | 500 | `configName` 超过 100 个字符 | `"参数名称不能超过100个字符"` |
| 200 | 500 | `configKey` 为空 | `"参数键名不能为空"` |
| 200 | 500 | `configKey` 超过 100 个字符 | `"参数键名长度不能超过100个字符"` |
| 200 | 500 | `configValue` 为空 | `"参数键值不能为空"` |
| 200 | 500 | `configValue` 超过 500 个字符 | `"参数键值长度不能超过500个字符"` |
| 200 | 500 | `configKey` 已存在 | `"新增参数'{configName}'失败，参数键名已存在"` |
| 200 | 500 | 数据库插入失败 | `"操作失败"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 键名唯一性 | 新增前会校验 `configKey` 是否已存在，已存在则返回错误 |
| 缓存更新 | 新增成功后，通过 `@CachePut` 自动将 `configValue` 写入缓存 `CacheNames.SYS_CONFIG` |
| 防重提交 | 使用 `@RepeatSubmit` 注解，防止短时间内重复提交同一参数 |

---

### 11 修改参数配置

| 属性 | 值 |
|------|-----|
| **请求方式** | `PUT` |
| **接口路径** | `/system/config` |
| **接口说明** | 根据 `configId` 修改已有参数配置；如果键名发生变更，会清除旧键名的缓存并写入新键名缓存 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:config:edit` |
| **标签** | 系统管理-参数配置 |
| **防重提交** | 开启（`@RepeatSubmit`） |

---

#### 请求

**请求头**: [认证]

**请求体**: [SysConfigBo](../entities/SysConfigBo.md)（需包含 `configId`）

```json
{
  "configId": 1,
  "configName": "主框架页-默认皮肤样式名称",
  "configKey": "sys.index.skinName",
  "configValue": "skin-green",
  "configType": "Y",
  "remark": "绿色皮肤"
}
```

---

#### 响应

##### 成功响应 — HTTP 200

```json
{
  "code": 200,
  "msg": "操作成功"
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | `configName` 为空 | `"参数名称不能为空"` |
| 200 | 500 | `configName` 超过 100 个字符 | `"参数名称不能超过100个字符"` |
| 200 | 500 | `configKey` 为空 | `"参数键名不能为空"` |
| 200 | 500 | `configKey` 超过 100 个字符 | `"参数键名长度不能超过100个字符"` |
| 200 | 500 | `configValue` 为空 | `"参数键值不能为空"` |
| 200 | 500 | `configValue` 超过 500 个字符 | `"参数键值长度不能超过500个字符"` |
| 200 | 500 | 修改后的 `configKey` 与其他记录重复 | `"修改参数'{configName}'失败，参数键名已存在"` |
| 200 | 500 | 数据库更新失败 | `"操作失败"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 键名唯一性 | 修改前会校验 `configKey` 是否已被其他记录占用（排除自身），已占用则返回错误 |
| 缓存管理 | 若 `configId` 存在 → 走按 ID 更新逻辑；若键名变更 → 清除旧键名缓存 + 写入新键名缓存；若 `configId` 为 null → 按 key 更新并清除旧缓存 |
| 缓存淘汰 | 键名变更时调用 `CacheUtils.evict(CacheNames.SYS_CONFIG, oldConfigKey)` 清除旧缓存 |

---

### 12 根据参数键名修改参数配置

| 属性 | 值 |
|------|-----|
| **请求方式** | `PUT` |
| **接口路径** | `/system/config/updateByKey` |
| **接口说明** | 根据 `configKey` 直接修改参数配置（不依赖 `configId`），按键名匹配更新 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:config:edit` |
| **标签** | 系统管理-参数配置 |
| **防重提交** | 开启（`@RepeatSubmit`） |

---

#### 请求

**请求头**: [认证]

**请求体**: [SysConfigBo](../entities/SysConfigBo.md)（无需 `configId`，通过 `configKey` 定位）

```json
{
  "configKey": "sys.index.skinName",
  "configValue": "skin-green",
  "configName": "主框架页-默认皮肤样式名称"
}
```

---

#### 响应

##### 成功响应 — HTTP 200

```json
{
  "code": 200,
  "msg": "操作成功"
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | 数据库更新失败 | `"操作失败"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 按 Key 更新 | 与接口11不同，此接口未加 `@Validated` 分组校验，仅按 `configKey` 定位记录并更新 |
| 缓存更新 | 走 `updateConfig()` 的 else 分支（`configId` 为 null），清除旧 key 缓存后按新数据更新 |

---

### 13 删除参数配置

| 属性 | 值 |
|------|-----|
| **请求方式** | `DELETE` |
| **接口路径** | `/system/config/{configIds}` |
| **接口说明** | 批量删除参数配置，支持一次删除多个；内置参数（`configType=Y`）不允许删除 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:config:remove` |
| **标签** | 系统管理-参数配置 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `configIds` | Long[] | 是 | 参数ID数组，逗号分隔 | `1,2,3` |

---

#### 响应

##### 成功响应 — HTTP 200

```json
{
  "code": 200,
  "msg": "操作成功"
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | 尝试删除内置参数（`configType=Y`） | `"内置参数【{configKey}】不能删除"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 内置参数保护 | `configType=Y`（`SystemConstants.YES`）的参数为系统内置参数，不允许删除，删除前逐个检查 |
| 缓存清除 | 每条被删除的参数都会调用 `CacheUtils.evict(CacheNames.SYS_CONFIG, configKey)` 清除对应缓存 |
| 无参数格式校验 | `configIds` 路径变量无 `@NotEmpty` 校验，传入空数组不会拦截 |

---

### 14 刷新参数缓存

| 属性 | 值 |
|------|-----|
| **请求方式** | `DELETE` |
| **接口路径** | `/system/config/refreshCache` |
| **接口说明** | 清除 `CacheNames.SYS_CONFIG` 缓存中的所有参数缓存数据 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:config:remove` |
| **标签** | 系统管理-参数配置 |

---

#### 请求

**请求头**: [认证]

无请求参数、路径参数、请求体。

---

#### 响应

##### 成功响应 — HTTP 200

```json
{
  "code": 200,
  "msg": "操作成功"
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 全量清除 | 调用 `CacheUtils.clear(CacheNames.SYS_CONFIG)` 清除所有参数缓存，下次访问时重新从数据库加载 |
| 接口方法 | 使用 `@DeleteMapping` 而非 `@PostMapping`/`@PutMapping`，语义上为删除操作 |
| 权限复用 | 与删除参数配置共享同一权限 `system:config:remove` |

---

## 三、客户端管理

### 15 查询客户端管理列表

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/system/client/list` |
| **接口说明** | 分页查询 OAuth2 客户端管理列表，支持按 clientId、clientKey、clientSecret、status 精确筛选，按主键ID升序排列 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:client:list` |
| **标签** | 系统管理-客户端管理 |

---

#### 请求

**请求头**: [认证]

**查询参数**:

| 参数名 | 类型 | 必填 | 匹配方式 | 说明 | 示例 |
|--------|------|:---:|:---:|------|------|
| `pageNum` | Integer | 否 | — | 当前页码，默认 1 | `1` |
| `pageSize` | Integer | 否 | — | 每页条数，默认 10 | `10` |
| `orderByColumn` | String | 否 | — | 排序列名 | `"id"` |
| `isAsc` | String | 否 | — | 升序/降序 (asc/desc) | `"asc"` |
| `clientId` | String | 否 | eq | 客户端ID（精确匹配） | `"system-client"` |
| `clientKey` | String | 否 | eq | 客户端key（精确匹配） | `"system-key"` |
| `clientSecret` | String | 否 | eq | 客户端秘钥（精确匹配） | `"abc123def456"` |
| `status` | String | 否 | eq | 状态（0=正常, 1=停用） | `"0"` |

---

#### 响应

##### 成功响应 — HTTP 200

分页列表，数据项为 [SysClientVo](../entities/SysClientVo.md)。`grantTypeList` 在后端自动从 `grantType` 逗号分隔字符串拆分为数组。

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "rows": [
      {
        "id": 1,
        "clientId": "e5cd7e4891bf95d1d19206ce24a7b32e",
        "clientKey": "system-key",
        "clientSecret": "abc****f456",
        "grantTypeList": ["password", "sms", "social"],
        "grantType": "password,sms,social",
        "deviceType": "pc",
        "activeTimeout": 1800,
        "timeout": 604800,
        "status": "0"
      }
    ],
    "total": 5
  }
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |

---

### 16 导出客户端管理列表

| 属性 | 值 |
|------|-----|
| **请求方式** | `POST` |
| **接口路径** | `/system/client/export` |
| **接口说明** | 按查询条件导出客户端管理数据为 Excel 文件（.xlsx） |
| **认证方式** | 需要认证 |
| **权限要求** | `system:client:export` |
| **标签** | 系统管理-客户端管理 |

---

#### 请求

**请求头**: [认证]

**查询参数**: 同接口15（客户端列表查询），无需分页参数。

---

#### 响应

##### 成功响应 — HTTP 200

直接返回 Excel 文件流（`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`）。

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |

---

### 17 获取客户端管理详细信息

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/system/client/{id}` |
| **接口说明** | 根据主键ID查询单条客户端管理的详细信息，`grantTypeList` 自动从逗号分隔字符串拆分为数组 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:client:query` |
| **标签** | 系统管理-客户端管理 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `id` | Long | 是 | 主键ID | `1` |

---

#### 响应

##### 成功响应 — HTTP 200

[SysClientVo](../entities/SysClientVo.md)

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "id": 1,
    "clientId": "e5cd7e4891bf95d1d19206ce24a7b32e",
    "clientKey": "system-key",
    "clientSecret": "abc****f456",
    "grantTypeList": ["password", "sms", "social"],
    "grantType": "password,sms,social",
    "deviceType": "pc",
    "activeTimeout": 1800,
    "timeout": 604800,
    "status": "0"
  }
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 查询成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | `id` 为 null | `"主键不能为空"` |

---

### 18 新增客户端管理

| 属性 | 值 |
|------|-----|
| **请求方式** | `POST` |
| **接口路径** | `/system/client` |
| **接口说明** | 新增一个 OAuth2 客户端，`clientId` 由系统根据 `clientKey + clientSecret` 的 MD5 自动生成 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:client:add` |
| **标签** | 系统管理-客户端管理 |
| **防重提交** | 开启（`@RepeatSubmit`） |

---

#### 请求

**请求头**: [认证]

**请求体**: [SysClientBo](../entities/SysClientBo.md)（`AddGroup` 分组校验）

```json
{
  "clientKey": "system-key",
  "clientSecret": "abc123def456",
  "grantTypeList": ["password", "sms", "social"],
  "deviceType": "pc",
  "activeTimeout": 1800,
  "timeout": 604800,
  "status": "0"
}
```

---

#### 响应

##### 成功响应 — HTTP 200

```json
{
  "code": 200,
  "msg": "操作成功"
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | `clientKey` 为空 | `"客户端key不能为空"` |
| 200 | 500 | `clientSecret` 为空 | `"客户端秘钥不能为空"` |
| 200 | 500 | `grantTypeList` 为 null | `"授权类型不能为空"` |
| 200 | 500 | `clientKey` 已存在 | `"新增客户端'{clientKey}'失败，客户端key已存在"` |
| 200 | 500 | 数据库插入失败 | `"操作失败"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| clientId 生成 | `clientId = MD5(clientKey + clientSecret)`，系统自动生成，无需前端传入 |
| 授权类型合并 | 前端传入 `grantTypeList` 数组，持久化时通过 `CollUtil.join()` 转为逗号分隔字符串存入 `grantType` 字段 |
| 唯一性校验 | 新增前校验 `clientKey` 是否已存在，已存在则返回错误 |
| 防重提交 | 使用 `@RepeatSubmit` 注解 |

---

### 19 修改客户端管理

| 属性 | 值 |
|------|-----|
| **请求方式** | `PUT` |
| **接口路径** | `/system/client` |
| **接口说明** | 修改已有 OAuth2 客户端信息，成功后清除对应 `clientId` 的缓存 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:client:edit` |
| **标签** | 系统管理-客户端管理 |
| **防重提交** | 开启（`@RepeatSubmit`） |

---

#### 请求

**请求头**: [认证]

**请求体**: [SysClientBo](../entities/SysClientBo.md)（`EditGroup` 分组校验，需包含 `id`）

```json
{
  "id": 1,
  "clientKey": "system-key",
  "clientSecret": "newSecret456",
  "grantTypeList": ["password", "sms"],
  "deviceType": "pc",
  "activeTimeout": 3600,
  "timeout": 86400,
  "status": "0"
}
```

---

#### 响应

##### 成功响应 — HTTP 200

```json
{
  "code": 200,
  "msg": "操作成功"
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | `id` 为 null | `"id不能为空"` |
| 200 | 500 | `clientKey` 为空 | `"客户端key不能为空"` |
| 200 | 500 | `clientSecret` 为空 | `"客户端秘钥不能为空"` |
| 200 | 500 | `grantTypeList` 为 null | `"授权类型不能为空"` |
| 200 | 500 | 修改后的 `clientKey` 与其他记录重复 | `"修改客户端'{clientKey}'失败，客户端key已存在"` |
| 200 | 500 | 数据库更新失败 | `"操作失败"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 分组校验 | 使用 `EditGroup` 分组校验，`id` 字段在校验组内必填 |
| 缓存清除 | 成功后通过 `@CacheEvict(cacheNames = CacheNames.SYS_CLIENT, key = "#bo.clientId")` 清除对应 clientId 的缓存 |
| 唯一性校验 | 修改前校验 `clientKey` 是否已被其他记录占用（排除自身），已占用则返回错误 |
| 授权类型 | 前端传入 `grantTypeList`，后端通过 `StringUtils.joinComma()` 转为逗号分隔字符串 |

---

### 20 修改客户端状态

| 属性 | 值 |
|------|-----|
| **请求方式** | `PUT` |
| **接口路径** | `/system/client/changeStatus` |
| **接口说明** | 修改客户端的启用/停用状态，成功后清除对应 `clientId` 的缓存 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:client:edit` |
| **标签** | 系统管理-客户端管理 |

---

#### 请求

**请求头**: [认证]

**请求体**: [SysClientBo](../entities/SysClientBo.md)（仅需 `clientId` 和 `status`）

```json
{
  "clientId": "e5cd7e4891bf95d1d19206ce24a7b32e",
  "status": "1"
}
```

---

#### 响应

##### 成功响应 — HTTP 200

```json
{
  "code": 200,
  "msg": "操作成功"
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | 数据库更新失败 | `"操作失败"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 缓存清除 | 成功后通过 `@CacheEvict(cacheNames = CacheNames.SYS_CLIENT, key = "#clientId")` 清除对应缓存 |
| 状态切换 | `status` 取值：`"0"`=正常（启用），`"1"`=停用（禁用客户端认证） |
| 无分组校验 | 此接口未加 `@Validated` 分组，直接按 `SysClientBo` 接收参数 |

---

### 21 删除客户端管理

| 属性 | 值 |
|------|-----|
| **请求方式** | `DELETE` |
| **接口路径** | `/system/client/{ids}` |
| **接口说明** | 批量删除客户端管理记录，支持一次删除多个，删除后清除全部客户端缓存 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:client:remove` |
| **标签** | 系统管理-客户端管理 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `ids` | Long[] | 是 | 主键ID数组，逗号分隔 | `1,2,3` |

---

#### 响应

##### 成功响应 — HTTP 200

```json
{
  "code": 200,
  "msg": "操作成功"
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | `ids` 为空 | `"主键不能为空"` |
| 200 | 500 | 数据库删除失败 | `"操作失败"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 全量缓存清除 | 删除后通过 `@CacheEvict(cacheNames = CacheNames.SYS_CLIENT, allEntries = true)` 清除所有客户端缓存 |
| 批量删除 | 支持一次删除多条记录，调用 `baseMapper.deleteByIds(ids)` |
| `ids` 校验 | 使用 `@NotEmpty(message = "主键不能为空")` 校验，空数组会被拦截 |

---

*文档生成时间: 2026-07-14 · 共 21 个接口*
