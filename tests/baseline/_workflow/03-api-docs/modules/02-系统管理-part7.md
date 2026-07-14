# OSS 对象存储 + OSS 配置 API 文档

> Controller: `SysOssController` / `SysOssConfigController` | Base URL: `/resource/oss` / `/resource/oss/config` | Auth: Sa-Token JWT `Authorization: Bearer {token}` + `clientid: e5cd7e4891bf95d1d19206ce24a7b32e`

## 请求头

| 头名称 | 值 | 说明 |
|--------|-----|------|
| Content-Type | `application/json` | 请求体格式；文件上传使用 `multipart/form-data` |
| Authorization | `Bearer {token}` | Sa-Token JWT 令牌，登录后获取 |
| clientid | `e5cd7e4891bf95d1d19206ce24a7b32e` | 客户端 ID，与 Token 绑定 |

---

## OSS 对象存储

### 1 查询 OSS 对象存储列表

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/resource/oss/list` |
| **接口说明** | 分页查询 OSS 对象存储文件列表，支持多条件过滤 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:oss:list` |
| **标签** | 系统管理-OSS 对象存储 |

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
| `fileName` | String | 否 | like | 文件名（模糊匹配） | `"20260714"` |
| `originalName` | String | 否 | like | 原始文件名（模糊匹配） | `"avatar"` |
| `fileSuffix` | String | 否 | eq | 文件后缀名（精确匹配） | `".png"` |
| `url` | String | 否 | eq | URL 地址（精确匹配） | `"https://oss.example.com/ruoyi/"` |
| `service` | String | 否 | eq | 服务商配置 key（精确匹配） | `"minio"` |
| `createBy` | Long | 否 | eq | 上传人 ID（精确匹配） | `1` |
| `beginCreateTime` | String | 否 | between | 创建时间起始（通过 params 传递） | `"2026-07-01"` |
| `endCreateTime` | String | 否 | between | 创建时间结束（通过 params 传递） | `"2026-07-14"` |

> **注意**: `beginCreateTime` 和 `endCreateTime` 通过 `params` 参数传递，格式为 `params[beginCreateTime]=2026-07-01&params[endCreateTime]=2026-07-14`。两者必须同时存在才生效。

查询结果按 `ossId` 升序排列。

---

#### 响应

##### 成功响应 — HTTP 200

[List<SysOssVo>](../entities/SysOssVo.md) 的分页包装，分页格式为 `TableDataInfo<SysOssVo>`：

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "rows": [
      {
        "ossId": 1001,
        "fileName": "20260714_abc123.png",
        "originalName": "avatar.png",
        "fileSuffix": ".png",
        "url": "https://oss.example.com/ruoyi/20260714_abc123.png?sign=xxx",
        "ext1": "{\"fileSize\":102400,\"contentType\":\"image/png\"}",
        "createTime": "2026-07-14 15:30:00",
        "createBy": 1,
        "createByName": "张三",
        "service": "minio"
      }
    ],
    "total": 100
  }
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | 数据库查询异常 | `"发生未知异常，请联系管理员"` |

---

### 2 查询 OSS 对象基于 ID 串

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/resource/oss/listByIds/{ossIds}` |
| **接口说明** | 根据一组 OSS 对象 ID 查询对应的文件信息列表 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:oss:query` |
| **标签** | 系统管理-OSS 对象存储 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `ossIds` | Long[] | 是 | OSS 对象 ID 数组，逗号分隔 | `1001,1002,1003` |

> **校验规则**: `@NotEmpty(message = "主键不能为空")`，不允许空数组。

---

#### 响应

##### 成功响应 — HTTP 200

[List<SysOssVo>](../entities/SysOssVo.md) 的列表：

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": [
    {
      "ossId": 1001,
      "fileName": "20260714_abc123.png",
      "originalName": "avatar.png",
      "fileSuffix": ".png",
      "url": "https://oss.example.com/ruoyi/20260714_abc123.png?sign=xxx",
      "ext1": "{\"fileSize\":102400,\"contentType\":\"image/png\"}",
      "createTime": "2026-07-14 15:30:00",
      "createBy": 1,
      "createByName": "张三",
      "service": "minio"
    }
  ]
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | ossIds 为空（校验层：@NotEmpty） | `"主键不能为空"` |
| 200 | 500 | 数据库查询异常 | `"发生未知异常，请联系管理员"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 数据过滤 | 不存在的 ossId 对应记录会被跳过，不会抛出异常 |
| URL 匹配 | 返回的 URL 会根据桶权限类型处理：private 桶生成 120 秒临时签名 URL，public 桶返回原始 URL |
| OSS 异常容错 | 若 OSS 服务连接异常，该条记录仍正常返回（使用数据库中的原始 URL），不中断查询 |

---

### 3 上传 OSS 对象存储

| 属性 | 值 |
|------|-----|
| **请求方式** | `POST` |
| **接口路径** | `/resource/oss/upload` |
| **接口说明** | 上传文件到默认 OSS 对象存储服务，保存文件信息到数据库 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:oss:upload` |
| **标签** | 系统管理-OSS 对象存储 |
| **操作日志** | `@Log(title = "OSS对象存储", businessType = INSERT)` |

---

#### 请求

**请求头**: [认证] + `Content-Type: multipart/form-data`

**请求体** (multipart/form-data):

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `file` | MultipartFile | 是 | 上传的文件（参数名必须为 `file`） | `avatar.png` |

> **参数名**: 使用 `@RequestPart("file")` 接收，表单字段名必须为 `file`。

---

#### 响应

##### 成功响应 — HTTP 200

[SysOssUploadVo](../entities/SysOssUploadVo.md)：

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "url": "https://oss.example.com/ruoyi/20260714_abc123.png",
    "fileName": "20260714_abc123.png",
    "ossId": "1001"
  }
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | 上传文件为空（Service 层） | `"上传文件不能为空"` |
| 200 | 500 | OSS 配置错误或连接失败 | `"配置错误! 请检查系统配置:[...]"` |
| 200 | 500 | OSS 上传失败 | `"上传文件失败，请检查配置信息:[...]"` |
| 200 | 500 | 文件大小超出限制 | `"上传的文件大小超出限制的文件大小！<br/>允许的文件最大大小是：{0}MB！"` |
| 200 | 500 | 文件名长度超出限制 | `"上传的文件名最长{0}个字符"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 文件非空校验 | file 为 null 或 isEmpty() 时抛出 `ServiceException("上传文件不能为空")` |
| 后缀提取 | 从原始文件名末尾提取后缀（含 `.`），如 `avatar.png` -> `.png` |
| 默认 OSS 配置 | 使用 `OssFactory.instance()` 获取默认 OSS 配置（status=0 的配置为默认） |
| 扩展字段 | ext1 存储文件大小（fileSize）和内容类型（contentType）的 JSON |
| 上传方式 | 使用 S3 TransferManager 通过 InputStream 上传，支持大文件分块 |
| 临时文件清理 | 上传完成后自动删除临时文件 |

---

### 4 下载 OSS 对象

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/resource/oss/download/{ossId}` |
| **接口说明** | 根据 OSS 对象 ID 下载文件，直接返回文件流 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:oss:download` |
| **标签** | 系统管理-OSS 对象存储 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `ossId` | Long | 是 | OSS 对象 ID | `1001` |

---

#### 响应

##### 成功响应 — HTTP 200

直接返回文件二进制流。响应头由 `FileUtils.setAttachmentResponseHeader` 设置：

- `Content-Disposition: attachment; filename="原始文件名"`
- `Content-Type: application/octet-stream; charset=UTF-8`
- `Content-Length: <文件大小>`

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| — | — | 文件流正常返回 | （无 JSON body，直接返回文件流） |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | ossId 对应的文件不存在（Service 层） | `"文件数据不存在!"` |
| 200 | 500 | OSS 服务连接失败 | 抛出 IOException，由全局处理器返回 `"发生未知异常，请联系管理员"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 缓存查询 | 先通过 `@Cacheable(cacheNames = SYS_OSS, key = #ossId)` 从缓存获取，缓存未命中则查数据库 |
| 文件校验 | 若数据库中无对应记录，抛出 `ServiceException("文件数据不存在!")` |
| OSS 下载 | 通过 `OssFactory.instance(service)` 获取对应服务商的 OssClient，调用 download 方法 |
| 流式下载 | 使用 `response.getOutputStream()` 流式写入，支持大文件下载 |

---

### 5 删除 OSS 对象存储

| 属性 | 值 |
|------|-----|
| **请求方式** | `DELETE` |
| **接口路径** | `/resource/oss/{ossIds}` |
| **接口说明** | 批量删除 OSS 对象存储文件，同时删除 OSS 服务中的实际文件 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:oss:remove` |
| **标签** | 系统管理-OSS 对象存储 |
| **操作日志** | `@Log(title = "OSS对象存储", businessType = DELETE)` |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `ossIds` | Long[] | 是 | OSS 对象 ID 数组，逗号分隔 | `1001,1002` |

> **校验规则**: `@NotEmpty(message = "主键不能为空")`，不允许空数组。

---

#### 响应

##### 成功响应 — HTTP 200

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": null
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功（删除影响行数 > 0） | `"操作成功"` |
| 200 | 500 | 操作失败（删除影响行数 = 0，数据可能已被删除） | `"操作失败"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | ossIds 为空（校验层：@NotEmpty） | `"主键不能为空"` |
| 200 | 500 | 数据库删除异常 | `"发生未知异常，请联系管理员"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 级联删除 | 先查询数据库中的 OSS 记录，再调用对应 OssClient 删除 OSS 服务中的实际文件，最后删除数据库记录 |
| 事务控制 | 未使用 @Transactional；若 OSS 文件删除成功但数据库删除失败，OSS 文件已被删除不可回滚 |
| 批量处理 | 支持批量删除，每个 ID 对应的 OSS 文件都会被删除 |
| 结果判断 | `toAjax(rows)` 根据影响行数判断：>0 返回成功，=0 返回失败 |

---

## OSS 配置管理

### 6 查询对象存储配置列表

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/resource/oss/config/list` |
| **接口说明** | 分页查询 OSS 对象存储配置列表，支持按配置 key、桶名称、状态过滤 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:ossConfig:list` |
| **标签** | 系统管理-OSS 配置 |

---

#### 请求

**请求头**: [认证]

**查询参数**:

| 参数名 | 类型 | 必填 | 匹配方式 | 说明 | 示例 |
|--------|------|:---:|:---:|------|------|
| `pageNum` | Integer | 否 | — | 当前页码，默认 1 | `1` |
| `pageSize` | Integer | 否 | — | 每页条数，默认 10 | `10` |
| `orderByColumn` | String | 否 | — | 排序列名 | `"ossConfigId"` |
| `isAsc` | String | 否 | — | 升序/降序 (asc/desc) | `"asc"` |
| `configKey` | String | 否 | eq | 配置 key（精确匹配） | `"minio"` |
| `bucketName` | String | 否 | like | 桶名称（模糊匹配） | `"ruoyi"` |
| `status` | String | 否 | eq | 是否默认（精确匹配，0=是, 1=否） | `"0"` |

> 查询结果按 `ossConfigId` 升序排列。

---

#### 响应

##### 成功响应 — HTTP 200

[SysOssConfigVo](../entities/SysOssConfigVo.md) 的分页包装，分页格式为 `TableDataInfo<SysOssConfigVo>`：

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "rows": [
      {
        "ossConfigId": 1,
        "configKey": "minio",
        "accessKey": "minioadmin",
        "secretKey": "minioadmin",
        "bucketName": "ruoyi",
        "prefix": "dev/",
        "endpoint": "http://localhost:9000",
        "domain": "https://oss.example.com",
        "isHttps": "Y",
        "status": "0",
        "region": "cn-north-1",
        "ext1": "",
        "remark": "MinIO 本地存储",
        "accessPolicy": "1"
      }
    ],
    "total": 5
  }
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | 数据库查询异常 | `"发生未知异常，请联系管理员"` |

---

### 7 获取对象存储配置详细信息

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/resource/oss/config/{ossConfigId}` |
| **接口说明** | 根据配置 ID 获取 OSS 对象存储配置的详细信息 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:ossConfig:list` |
| **标签** | 系统管理-OSS 配置 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `ossConfigId` | Long | 是 | OSS 配置 ID | `1` |

> **校验规则**: `@NotNull(message = "主键不能为空")`，不允许 null。

---

#### 响应

##### 成功响应 — HTTP 200

[SysOssConfigVo](../entities/SysOssConfigVo.md)：

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "ossConfigId": 1,
    "configKey": "minio",
    "accessKey": "minioadmin",
    "secretKey": "minioadmin",
    "bucketName": "ruoyi",
    "prefix": "dev/",
    "endpoint": "http://localhost:9000",
    "domain": "https://oss.example.com",
    "isHttps": "Y",
    "status": "0",
    "region": "cn-north-1",
    "ext1": "",
    "remark": "MinIO 本地存储",
    "accessPolicy": "1"
  }
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | ossConfigId 为 null（校验层：@NotNull） | `"主键不能为空"` |
| 200 | 500 | 配置不存在（Service 层返回 null，但 R.ok(null) 仍返回 200） | `"操作成功"`（data 为 null） |
| 200 | 500 | 数据库查询异常 | `"发生未知异常，请联系管理员"` |

---

### 8 新增对象存储配置

| 属性 | 值 |
|------|-----|
| **请求方式** | `POST` |
| **接口路径** | `/resource/oss/config` |
| **接口说明** | 新增 OSS 对象存储配置，configKey 必须唯一 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:ossConfig:add` |
| **标签** | 系统管理-OSS 配置 |
| **防重提交** | `@RepeatSubmit()`，默认 5 秒内不允许重复提交 |
| **操作日志** | `@Log(title = "对象存储配置", businessType = INSERT)` |

---

#### 请求

**请求头**: [认证]

**请求体**: [SysOssConfigBo](../entities/SysOssConfigBo.md)

> **校验分组**: `AddGroup`，校验以下字段：`configKey`、`accessKey`、`secretKey`、`bucketName`、`endpoint`、`accessPolicy`。

JSON 示例：

```json
{
  "configKey": "minio",
  "accessKey": "minioadmin",
  "secretKey": "minioadmin",
  "bucketName": "ruoyi",
  "prefix": "dev/",
  "endpoint": "http://localhost:9000",
  "domain": "https://oss.example.com",
  "isHttps": "Y",
  "status": "0",
  "region": "cn-north-1",
  "ext1": "",
  "remark": "MinIO 本地存储",
  "accessPolicy": "1"
}
```

---

#### 响应

##### 成功响应 — HTTP 200

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": null
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功（插入影响行数 > 0） | `"操作成功"` |
| 200 | 500 | 操作失败（插入影响行数 = 0） | `"操作失败"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | 重复提交（@RepeatSubmit 拦截） | `"不允许重复提交，请稍候再试"` |
| 200 | 500 | configKey 为空（校验层：@NotBlank） | `"配置key不能为空"` |
| 200 | 500 | accessKey 为空（校验层：@NotBlank） | `"accessKey不能为空"` |
| 200 | 500 | secretKey 为空（校验层：@NotBlank） | `"secretKey不能为空"` |
| 200 | 500 | bucketName 为空（校验层：@NotBlank） | `"桶名称不能为空"` |
| 200 | 500 | endpoint 为空（校验层：@NotBlank） | `"访问站点不能为空"` |
| 200 | 500 | accessPolicy 为空（校验层：@NotBlank） | `"桶权限类型不能为空"` |
| 200 | 500 | configKey 长度不在 2~100 之间（校验层：@Size） | `"configKey长度必须介于2和100 之间"` |
| 200 | 500 | accessKey 长度不在 2~100 之间（校验层：@Size） | `"accessKey长度必须介于2和100 之间"` |
| 200 | 500 | secretKey 长度不在 2~100 之间（校验层：@Size） | `"secretKey长度必须介于2和100 之间"` |
| 200 | 500 | bucketName 长度不在 2~100 之间（校验层：@Size） | `"bucketName长度必须介于2和100之间"` |
| 200 | 500 | endpoint 长度不在 2~100 之间（校验层：@Size） | `"endpoint长度必须介于2和100之间"` |
| 200 | 500 | configKey 已存在（Service 层唯一性校验） | `"操作配置'{configKey}'失败, 配置key已存在!"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| configKey 唯一性 | 新增前校验 configKey 是否已存在，重复则抛出 `ServiceException` |
| 缓存同步 | 插入成功后，将完整配置数据写入缓存 `CacheNames.SYS_OSS_CONFIG`（key 为 configKey） |
| 防重提交 | `@RepeatSubmit()` 默认 5 秒内相同参数不允许重复提交 |
| 敏感信息 | `accessKey` 和 `secretKey` 以明文形式存储和返回，注意接口权限控制 |

---

### 9 修改对象存储配置

| 属性 | 值 |
|------|-----|
| **请求方式** | `PUT` |
| **接口路径** | `/resource/oss/config` |
| **接口说明** | 修改 OSS 对象存储配置，configKey 不可与已有配置重复 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:ossConfig:edit` |
| **标签** | 系统管理-OSS 配置 |
| **防重提交** | `@RepeatSubmit()`，默认 5 秒内不允许重复提交 |
| **操作日志** | `@Log(title = "对象存储配置", businessType = UPDATE)` |

---

#### 请求

**请求头**: [认证]

**请求体**: [SysOssConfigBo](../entities/SysOssConfigBo.md)

> **校验分组**: `EditGroup`，校验 `ossConfigId`（@NotNull）和与 AddGroup 相同的业务字段。

JSON 示例：

```json
{
  "ossConfigId": 1,
  "configKey": "minio",
  "accessKey": "newAccessKey",
  "secretKey": "newSecretKey",
  "bucketName": "ruoyi-v2",
  "prefix": "prod/",
  "endpoint": "http://newhost:9000",
  "domain": "https://newoss.example.com",
  "isHttps": "Y",
  "status": "1",
  "region": "cn-north-2",
  "ext1": "",
  "remark": "MinIO 生产环境",
  "accessPolicy": "0"
}
```

---

#### 响应

##### 成功响应 — HTTP 200

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": null
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功（更新影响行数 > 0） | `"操作成功"` |
| 200 | 500 | 操作失败（更新影响行数 = 0） | `"操作失败"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | 重复提交（@RepeatSubmit 拦截） | `"不允许重复提交，请稍候再试"` |
| 200 | 500 | ossConfigId 为 null（校验层：@NotNull） | `"主键不能为空"` |
| 200 | 500 | 各字段校验失败（同新增接口校验规则） | （同新增接口的校验错误消息） |
| 200 | 500 | configKey 与其他配置重复（Service 层唯一性校验） | `"操作配置'{configKey}'失败, 配置key已存在!"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| configKey 唯一性 | 校验修改后的 configKey 是否与其他已有配置重复（排除自身） |
| 空值写入 | 若 `prefix`、`region`、`ext1`、`remark` 为 null，会自动写入空字符串 `""` |
| 缓存同步 | 更新成功后，将完整配置数据写入缓存 `CacheNames.SYS_OSS_CONFIG` |
| 部分更新 | 使用 `LambdaUpdateWrapper` 更新，仅更新非 null 字段，null 字段写入空字符串 |

---

### 10 修改对象存储配置状态

| 属性 | 值 |
|------|-----|
| **请求方式** | `PUT` |
| **接口路径** | `/resource/oss/config/changeStatus` |
| **接口说明** | 修改对象存储配置的启用/禁用状态，同一时间仅允许一个默认配置 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:ossConfig:edit` |
| **标签** | 系统管理-OSS 配置 |
| **防重提交** | `@RepeatSubmit()`，默认 5 秒内不允许重复提交 |
| **操作日志** | `@Log(title = "对象存储状态修改", businessType = UPDATE)` |

---

#### 请求

**请求头**: [认证]

**请求体**: [SysOssConfigBo](../entities/SysOssConfigBo.md)

> **无校验分组**: 本接口不声明 `@Validated` 分组，因此不对字段做校验注解约束。

JSON 示例：

```json
{
  "ossConfigId": 2,
  "configKey": "aliyun-oss",
  "status": "0"
}
```

---

#### 响应

##### 成功响应 — HTTP 200

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": null
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 200 | 500 | 操作失败 | `"操作失败"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | 重复提交（@RepeatSubmit 拦截） | `"不允许重复提交，请稍候再试"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 事务控制 | 使用 `@Transactional(rollbackFor = Exception.class)` 保证数据一致性 |
| 唯一默认配置 | 修改状态前，先将所有配置的 status 设为 "1"（取消默认），再将目标配置设为 "0"（设为默认） |
| Redis 更新 | 操作完成后更新 Redis 中的 `OssConstant.DEFAULT_CONFIG_KEY`，指向新的默认配置 key |
| 状态值 | `"0"` = 默认配置（启用），`"1"` = 非默认配置（禁用） |

---

### 11 删除对象存储配置

| 属性 | 值 |
|------|-----|
| **请求方式** | `DELETE` |
| **接口路径** | `/resource/oss/config/{ossConfigIds}` |
| **接口说明** | 批量删除 OSS 对象存储配置 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:ossConfig:remove` |
| **标签** | 系统管理-OSS 配置 |
| **操作日志** | `@Log(title = "对象存储配置", businessType = DELETE)` |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `ossConfigIds` | Long[] | 是 | OSS 配置 ID 数组，逗号分隔 | `2,3` |

> **校验规则**: `@NotEmpty(message = "主键不能为空")`，不允许空数组。

---

#### 响应

##### 成功响应 — HTTP 200

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": null
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 200 | 500 | 操作失败 | `"操作失败"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | ossConfigIds 为空（校验层：@NotEmpty） | `"主键不能为空"` |
| 200 | 500 | 尝试删除系统内置数据（Service 层） | `"系统内置, 不可删除!"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 系统数据保护 | 若 `isValid=true`（本接口硬编码传入 true），检查 ID 列表中是否包含系统内置数据 ID（`OssConstant.SYSTEM_DATA_IDS`），包含则抛出 `ServiceException("系统内置, 不可删除!")` |
| 缓存清理 | 删除成功后，遍历被删除的配置列表，逐个从缓存 `CacheNames.SYS_OSS_CONFIG` 中清除 |
| 批量删除 | 支持批量删除，一次可删除多个配置 ID |

---

*基于源码 `SysOssController`、`SysOssConfigController`、`SysOssServiceImpl`、`SysOssConfigServiceImpl` 生成 * 2026-07-14*
