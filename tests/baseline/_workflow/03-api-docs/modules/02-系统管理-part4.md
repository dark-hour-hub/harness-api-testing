# 系统管理 Part 4 -- 岗位管理 + 字典管理 API 文档

> Controllers: `SysPostController`, `SysDictTypeController`, `SysDictDataController` | Base URL: `http://localhost:8080` | Auth: Sa-Token JWT `Authorization: Bearer {token}` + `clientid: e5cd7e4891bf95d1d19206ce24a7b32e`

## 请求头

| 头名称 | 值 | 说明 |
|--------|-----|------|
| Content-Type | `application/json` | 请求体格式；文件下载使用 `application/octet-stream` |
| Authorization | `Bearer {token}` | Sa-Token JWT 令牌，登录后获取 |
| clientid | `e5cd7e4891bf95d1d19206ce24a7b32e` | 客户端 ID，与 Token 绑定 |

---

## 一、岗位管理

### 1 获取岗位列表

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/system/post/list` |
| **接口说明** | 分页查询岗位列表，支持按岗位编码、岗位名称、岗位类别、状态、部门等条件筛选 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:post:list` |
| **标签** | 岗位管理 |

---

#### 请求

**请求头**: [认证]

**查询参数**:

| 参数名 | 类型 | 必填 | 匹配方式 | 说明 | 示例 |
|--------|------|:---:|:---:|------|------|
| `pageNum` | Integer | 否 | -- | 当前页码，默认 1 | `1` |
| `pageSize` | Integer | 否 | -- | 每页条数，默认 Integer.MAX_VALUE | `10` |
| `orderByColumn` | String | 否 | -- | 排序列名 | `"postSort"` |
| `isAsc` | String | 否 | -- | 升序/降序 (asc/desc) | `"asc"` |
| `postCode` | String | 否 | like | 岗位编码，模糊匹配 | `"ceo"` |
| `postCategory` | String | 否 | like | 岗位类别编码，模糊匹配 | `"manager"` |
| `postName` | String | 否 | like | 岗位名称，模糊匹配 | `"董事长"` |
| `status` | String | 否 | eq | 状态 (0=正常, 1=停用) | `"0"` |
| `deptId` | Long | 否 | eq | 部门ID（单部门精确搜索，优先级高于 belongDeptId） | `103` |
| `belongDeptId` | Long | 否 | in | 归属部门ID（部门树搜索，查询该部门及所有子部门的岗位） | `100` |
| `params[beginTime]` | String | 否 | between | 创建时间起始（需与 endTime 同时传入，作用于 createTime） | `"2024-01-01"` |
| `params[endTime]` | String | 否 | between | 创建时间截止（需与 beginTime 同时传入，作用于 createTime） | `"2024-12-31"` |

**备注**:
- `deptId` 与 `belongDeptId` 互斥：当 `deptId` 有值时优先使用单部门精确搜索；当 `belongDeptId` 有值时使用部门树搜索（含子部门）。
- 结果默认按 `postSort` 升序排列。

---

#### 响应

##### 成功响应 -- HTTP 200

响应体引用: [SysPostVo](../entities/SysPostVo.md)

外层由 `TableDataInfo` 包装，结构如下：

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "rows": [
      {
        "postId": 1,
        "deptId": 103,
        "postCode": "ceo",
        "postName": "董事长",
        "postCategory": "manager",
        "postSort": 1,
        "status": "0",
        "remark": "",
        "createTime": "2024-01-15 10:30:00",
        "deptName": "总公司",
        "address": "LosAngeles"
      }
    ],
    "total": 1
  }
}
```

`rows` 字段为 `List<SysPostVo>`，`total` 为总记录数。

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |

---

### 2 导出岗位列表

| 属性 | 值 |
|------|-----|
| **请求方式** | `POST` |
| **接口路径** | `/system/post/export` |
| **接口说明** | 根据查询条件导出岗位数据到 Excel 文件 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:post:export` |
| **标签** | 岗位管理 |

---

#### 请求

**请求头**: [认证]

**查询参数**:

| 参数名 | 类型 | 必填 | 匹配方式 | 说明 | 示例 |
|--------|------|:---:|:---:|------|------|
| `postCode` | String | 否 | like | 岗位编码 | `"ceo"` |
| `postName` | String | 否 | like | 岗位名称 | `"董事长"` |
| `postCategory` | String | 否 | like | 岗位类别编码 | `"manager"` |
| `status` | String | 否 | eq | 状态 | `"0"` |
| `deptId` | Long | 否 | eq | 部门ID | `103` |
| `belongDeptId` | Long | 否 | in | 归属部门ID | `100` |
| `params[beginTime]` | String | 否 | between | 创建时间起始 | `"2024-01-01"` |
| `params[endTime]` | String | 否 | between | 创建时间截止 | `"2024-12-31"` |

---

#### 响应

##### 成功响应 -- HTTP 200

直接返回 Excel 二进制文件流，文件名格式为 `岗位数据.xlsx`。Content-Type 为 `application/octet-stream`，`Content-Disposition` 包含 `attachment` 头。

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 导出成功 | -- |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |

---

### 3 根据岗位编号获取详细信息

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/system/post/{postId}` |
| **接口说明** | 根据岗位ID查询单个岗位的详细信息 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:post:query` |
| **标签** | 岗位管理 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `postId` | Long | 是 | 岗位ID | `1` |

---

#### 响应

##### 成功响应 -- HTTP 200

响应体引用: [SysPostVo](../entities/SysPostVo.md)

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "postId": 1,
    "deptId": 103,
    "postCode": "ceo",
    "postName": "董事长",
    "postCategory": "manager",
    "postSort": 1,
    "status": "0",
    "remark": "",
    "createTime": "2024-01-15 10:30:00",
    "deptName": "总公司",
    "address": "LosAngeles"
  }
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | 岗位ID不存在（查询返回 null） | `"操作成功"`（data 为 null） |

---

### 4 新增岗位

| 属性 | 值 |
|------|-----|
| **请求方式** | `POST` |
| **接口路径** | `/system/post` |
| **接口说明** | 新增一个岗位信息 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:post:add` |
| **防重提交** | 是（`@RepeatSubmit`） |
| **标签** | 岗位管理 |

---

#### 请求

**请求头**: [认证]

**请求体**: [SysPostBo](../entities/SysPostBo.md)

```json
{
  "deptId": 103,
  "postCode": "ceo",
  "postName": "董事长",
  "postCategory": "manager",
  "postSort": 1,
  "status": "0",
  "remark": "最高管理层岗位"
}
```

**必填字段**: `deptId`, `postCode`, `postName`, `postSort`

---

#### 响应

##### 成功响应 -- HTTP 200

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
| 200 | 500 | 岗位名称已存在（同部门下） | `"新增岗位'董事长'失败，岗位名称已存在"` |
| 200 | 500 | 岗位编码已存在 | `"新增岗位'董事长'失败，岗位编码已存在"` |
| 200 | 500 | DTO 校验失败（`deptId` 为空） | 校验消息（如 `"* 必须填写"`） |
| 200 | 500 | DTO 校验失败（`postCode` 为空） | 校验消息 |
| 200 | 500 | DTO 校验失败（`postName` 为空） | 校验消息 |
| 200 | 500 | DTO 校验失败（`postSort` 为空） | 校验消息 |
| 200 | 500 | 重复提交 | `"不允许重复提交，请稍候再试"` |

**三层错误追踪**:
1. **DTO 校验层**: `@Validated` + `@NotNull`/`@NotBlank` 触发 `MethodArgumentNotValidException`，由 `GlobalExceptionHandler.handleMethodArgumentNotValidException` 捕获，提取 `DefaultMessageSourceResolvable.getDefaultMessage()` 拼接返回。
2. **Controller 业务检查**: 调用 `checkPostNameUnique` / `checkPostCodeUnique`，不唯一时直接 `R.fail("新增岗位'...'失败，...")`，返回 code=500。
3. **全局异常处理**: `ServiceException` 由 `GlobalExceptionHandler.handleServiceException` 捕获，`R.fail(e.getMessage())` 返回 code=500。

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 岗位名称唯一性 | 同部门下岗位名称必须唯一（`deptId` + `postName` 联合校验） |
| 岗位编码唯一性 | 岗位编码全局唯一（`postCode` 单独校验） |
| 修改时排除自身 | 修改时唯一性校验排除当前岗位ID |

---

### 5 修改岗位

| 属性 | 值 |
|------|-----|
| **请求方式** | `PUT` |
| **接口路径** | `/system/post` |
| **接口说明** | 修改一个已有岗位的信息 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:post:edit` |
| **防重提交** | 是（`@RepeatSubmit`） |
| **标签** | 岗位管理 |

---

#### 请求

**请求头**: [认证]

**请求体**: [SysPostBo](../entities/SysPostBo.md)

```json
{
  "postId": 1,
  "deptId": 103,
  "postCode": "ceo",
  "postName": "董事长",
  "postCategory": "manager",
  "postSort": 1,
  "status": "0",
  "remark": "最高管理层岗位"
}
```

**必填字段**: `postId`（修改必须指定）, `deptId`, `postCode`, `postName`, `postSort`

---

#### 响应

##### 成功响应 -- HTTP 200

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
| 200 | 500 | 岗位名称已存在（同部门下，排除自身） | `"修改岗位'董事长'失败，岗位名称已存在"` |
| 200 | 500 | 岗位编码已存在（排除自身） | `"修改岗位'董事长'失败，岗位编码已存在"` |
| 200 | 500 | 岗位被禁用但存在已分配用户 | `"该岗位下存在已分配用户，不能禁用!"` |
| 200 | 500 | DTO 校验失败 | 校验消息 |
| 200 | 500 | 重复提交 | `"不允许重复提交，请稍候再试"` |

**三层错误追踪**:
1. **DTO 校验层**: `@Validated` 触发校验，异常由 `GlobalExceptionHandler.handleMethodArgumentNotValidException` 处理。
2. **Controller 业务检查**: 依次校验名称唯一性、编码唯一性、禁用条件。不满足时直接 `R.fail(...)` 返回。
3. **全局异常处理**: 同新增岗位。

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 岗位名称唯一性 | 同部门下岗位名称必须唯一（修改时排除自身） |
| 岗位编码唯一性 | 岗位编码全局唯一（修改时排除自身） |
| 禁用限制 | 当岗位下有已分配用户时，不允许将状态设为禁用 |

---

### 6 删除岗位

| 属性 | 值 |
|------|-----|
| **请求方式** | `DELETE` |
| **接口路径** | `/system/post/{postIds}` |
| **接口说明** | 批量删除岗位（支持多个ID，逗号分隔） |
| **认证方式** | 需要认证 |
| **权限要求** | `system:post:remove` |
| **标签** | 岗位管理 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `postIds` | Long[] | 是 | 岗位ID数组，多个用逗号分隔 | `1,2,3` |

---

#### 响应

##### 成功响应 -- HTTP 200

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
| 200 | 500 | 岗位下存在已分配用户 | `"{岗位名称}已分配，不能删除!"` |

**三层错误追踪**:
1. **路径参数类型转换失败**: 传入非数字时触发 `MethodArgumentTypeMismatchException`，全局处理器返回 `"请求参数类型不匹配，参数[postIds]要求类型为：'[Ljava.lang.Long;'，但输入值为：'...'"` 。
2. **Service 层业务检查**: `deletePostByIds` 遍历待删除岗位，若 `countUserPostById > 0` 则 `throw new ServiceException("{}已分配，不能删除!", post.getPostName())`，`{}` 由 `StrFormatter.format` 替换为岗位名称。
3. **全局异常处理**: `handleServiceException` 捕获，`R.fail(e.getMessage())`，code=500。

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 分配检查 | 岗位下存在已分配用户时不允许删除 |
| 批量删除 | 支持一次删除多个岗位，任一岗位不满足条件则整个请求失败 |

---

### 7 获取岗位选择框列表

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/system/post/optionselect` |
| **接口说明** | 获取岗位下拉选择框数据，可按部门筛选或按指定岗位ID列表查询 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:post:query` |
| **标签** | 岗位管理 |

---

#### 请求

**请求头**: [认证]

**查询参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `postIds` | Long[] | 否 | 岗位ID数组（与 deptId 互斥，优先由 deptId 决定逻辑） | `1,2,3` |
| `deptId` | Long | 否 | 部门ID（传入时按部门筛选岗位） | `103` |

**查询逻辑**:
- 当 `deptId` 不为空时：按部门筛选岗位列表（仅返回该部门下的岗位）。
- 当 `deptId` 为空且 `postIds` 不为空时：按岗位ID列表查询（仅返回状态为正常 `"0"` 的岗位，且仅返回 `postId`、`postName`、`postCode` 三个字段）。
- 两者都为空时：返回空列表。

---

#### 响应

##### 成功响应 -- HTTP 200

`R<List<SysPostVo>>`，仅包含 `postId`、`postName`、`postCode` 字段。

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": [
    {
      "postId": 1,
      "postCode": "ceo",
      "postName": "董事长"
    },
    {
      "postId": 2,
      "postCode": "se",
      "postName": "项目经理"
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

---

### 8 获取部门树列表

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/system/post/deptTree` |
| **接口说明** | 获取部门树结构数据，用于岗位管理页面的部门筛选下拉树 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:post:list` |
| **标签** | 岗位管理 |

---

#### 请求

**请求头**: [认证]

**查询参数**: [SysDeptBo](../entities/SysDeptBo.md) 中的查询字段

| 参数名 | 类型 | 必填 | 匹配方式 | 说明 | 示例 |
|--------|------|:---:|:---:|------|------|
| `deptId` | Long | 否 | eq | 部门ID（精确匹配） | `100` |
| `parentId` | Long | 否 | eq | 父部门ID | `0` |
| `deptName` | String | 否 | like | 部门名称（模糊匹配） | `"研发"` |
| `deptCategory` | String | 否 | like | 部门类别编码（模糊匹配） | `"DEPT_RD"` |
| `status` | String | 否 | eq | 状态 (0=正常, 1=停用) | `"0"` |
| `belongDeptId` | Long | 否 | in | 归属部门ID（部门树搜索） | `100` |
| `params[beginTime]` | String | 否 | between | 创建时间起始 | `"2024-01-01"` |
| `params[endTime]` | String | 否 | between | 创建时间截止 | `"2024-12-31"` |

**备注**: 查询结果自动排除已删除部门（`delFlag='0'`），并构建为树形结构返回。

---

#### 响应

##### 成功响应 -- HTTP 200

`R<List<Tree<Long>>>`，树节点结构如下：

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": [
    {
      "id": 100,
      "label": "总公司",
      "children": [
        {
          "id": 101,
          "label": "研发部",
          "children": []
        },
        {
          "id": 102,
          "label": "市场部",
          "children": []
        }
      ]
    }
  ]
}
```

`Tree<Long>` 字段说明：

| JSON 键名 | 类型 | 说明 |
|-----------|------|------|
| `id` | Long | 节点ID（部门ID） |
| `label` | String | 节点名称（部门名称） |
| `children` | List | 子节点列表 |

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |

---

## 二、字典类型管理

### 9 查询字典类型列表

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/system/dict/type/list` |
| **接口说明** | 分页查询字典类型列表，支持按字典名称、字典类型、创建时间等条件筛选 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:dict:list` |
| **标签** | 字典管理 |

---

#### 请求

**请求头**: [认证]

**查询参数**:

| 参数名 | 类型 | 必填 | 匹配方式 | 说明 | 示例 |
|--------|------|:---:|:---:|------|------|
| `pageNum` | Integer | 否 | -- | 当前页码，默认 1 | `1` |
| `pageSize` | Integer | 否 | -- | 每页条数，默认 Integer.MAX_VALUE | `10` |
| `orderByColumn` | String | 否 | -- | 排序列名 | `"dictId"` |
| `isAsc` | String | 否 | -- | 升序/降序 (asc/desc) | `"asc"` |
| `dictName` | String | 否 | like | 字典名称，模糊匹配 | `"用户性别"` |
| `dictType` | String | 否 | like | 字典类型，模糊匹配 | `"sys_user_sex"` |
| `params[beginTime]` | String | 否 | between | 创建时间起始（需与 endTime 同时传入，作用于 createTime） | `"2024-01-01"` |
| `params[endTime]` | String | 否 | between | 创建时间截止（需与 beginTime 同时传入，作用于 createTime） | `"2024-12-31"` |

**备注**: 默认按 `dictId` 升序排列。

---

#### 响应

##### 成功响应 -- HTTP 200

响应体引用: [SysDictTypeVo](../entities/SysDictTypeVo.md)

外层由 `TableDataInfo` 包装：

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "rows": [
      {
        "dictId": 1,
        "dictName": "用户性别",
        "dictType": "sys_user_sex",
        "remark": "用户性别列表",
        "createTime": "2024-01-15 10:30:00"
      }
    ],
    "total": 1
  }
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |

---

### 10 导出字典类型列表

| 属性 | 值 |
|------|-----|
| **请求方式** | `POST` |
| **接口路径** | `/system/dict/type/export` |
| **接口说明** | 根据查询条件导出字典类型数据到 Excel 文件 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:dict:export` |
| **标签** | 字典管理 |

---

#### 请求

**请求头**: [认证]

**查询参数**:

| 参数名 | 类型 | 必填 | 匹配方式 | 说明 | 示例 |
|--------|------|:---:|:---:|------|------|
| `dictName` | String | 否 | like | 字典名称 | `"用户性别"` |
| `dictType` | String | 否 | like | 字典类型 | `"sys_user_sex"` |
| `params[beginTime]` | String | 否 | between | 创建时间起始 | `"2024-01-01"` |
| `params[endTime]` | String | 否 | between | 创建时间截止 | `"2024-12-31"` |

---

#### 响应

##### 成功响应 -- HTTP 200

直接返回 Excel 二进制文件流，文件名格式为 `字典类型.xlsx`。

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 导出成功 | -- |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |

---

### 11 查询字典类型详细

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/system/dict/type/{dictId}` |
| **接口说明** | 根据字典ID查询字典类型的详细信息 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:dict:query` |
| **标签** | 字典管理 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `dictId` | Long | 是 | 字典主键 | `1` |

---

#### 响应

##### 成功响应 -- HTTP 200

响应体引用: [SysDictTypeVo](../entities/SysDictTypeVo.md)

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "dictId": 1,
    "dictName": "用户性别",
    "dictType": "sys_user_sex",
    "remark": "用户性别列表",
    "createTime": "2024-01-15 10:30:00"
  }
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | 字典ID不存在 | `"操作成功"`（data 为 null） |

---

### 12 新增字典类型

| 属性 | 值 |
|------|-----|
| **请求方式** | `POST` |
| **接口路径** | `/system/dict/type` |
| **接口说明** | 新增一个字典类型，同时初始化对应缓存 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:dict:add` |
| **防重提交** | 是（`@RepeatSubmit`） |
| **标签** | 字典管理 |

---

#### 请求

**请求头**: [认证]

**请求体**: [SysDictTypeBo](../entities/SysDictTypeBo.md)

```json
{
  "dictName": "用户性别",
  "dictType": "sys_user_sex",
  "remark": "用户性别列表"
}
```

**必填字段**: `dictName`, `dictType`

---

#### 响应

##### 成功响应 -- HTTP 200

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
| 200 | 500 | 字典类型已存在 | `"新增字典'用户性别'失败，字典类型已存在"` |
| 200 | 500 | 插入数据库失败 | `"操作失败"` |
| 200 | 500 | DTO 校验失败（`dictName` 为空） | 校验消息 |
| 200 | 500 | DTO 校验失败（`dictType` 为空） | 校验消息 |
| 200 | 500 | DTO 校验失败（`dictType` 格式不合法） | 校验消息（`@Pattern` 验证） |
| 200 | 500 | 重复提交 | `"不允许重复提交，请稍候再试"` |

**三层错误追踪**:
1. **DTO 校验层**: `@Validated` + `@NotBlank`/`@Size`/`@Pattern` 触发校验异常，由 `GlobalExceptionHandler.handleMethodArgumentNotValidException` 处理。
2. **Controller 业务检查**: `checkDictTypeUnique` 返回 false 时 `R.fail("新增字典'...'失败，字典类型已存在")`。
3. **Service 层**: `insertDictType` 中 `baseMapper.insert` 返回 0 行时 `throw new ServiceException("操作失败")`，由全局处理器捕获。

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 字典类型唯一性 | `dictType` 全局唯一（新增时不排除任何记录） |
| 字典类型格式 | 必须以字母开头，后续只能为小写字母、数字、下划线 |
| 缓存初始化 | 新增成功后自动将该字典类型的缓存设为空列表（防止缓存穿透） |

---

### 13 修改字典类型

| 属性 | 值 |
|------|-----|
| **请求方式** | `PUT` |
| **接口路径** | `/system/dict/type` |
| **接口说明** | 修改一个已有字典类型的信息，同时更新关联的字典数据及缓存 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:dict:edit` |
| **防重提交** | 是（`@RepeatSubmit`） |
| **标签** | 字典管理 |

---

#### 请求

**请求头**: [认证]

**请求体**: [SysDictTypeBo](../entities/SysDictTypeBo.md)

```json
{
  "dictId": 1,
  "dictName": "用户性别",
  "dictType": "sys_user_sex",
  "remark": "用户性别列表"
}
```

**必填字段**: `dictId`（修改必须指定）, `dictName`, `dictType`

---

#### 响应

##### 成功响应 -- HTTP 200

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
| 200 | 500 | 字典类型已存在（排除自身） | `"修改字典'用户性别'失败，字典类型已存在"` |
| 200 | 500 | 更新数据库失败 | `"操作失败"` |
| 200 | 500 | DTO 校验失败 | 校验消息 |
| 200 | 500 | 重复提交 | `"不允许重复提交，请稍候再试"` |

**三层错误追踪**:
1. **DTO 校验层**: `@Validated` 触发校验，异常由全局处理器处理。
2. **Controller 业务检查**: `checkDictTypeUnique` 返回 false 时 `R.fail("修改字典'...'失败，字典类型已存在")`。
3. **Service 层**: `updateDictType` 中更新失败时 `throw new ServiceException("操作失败")`（带事务回滚）。

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 字典类型唯一性 | `dictType` 全局唯一（修改时排除自身） |
| 级联更新 | 修改 `dictType` 时，同步更新 `sys_dict_data` 表中所有关联记录的 `dict_type` 字段 |
| 缓存更新 | 修改后刷新缓存：清除旧的 dictType 缓存 + 更新新的 dictType 缓存 |
| 事务保护 | 使用 `@Transactional`，修改失败时自动回滚字典类型和字典数据的变更 |

---

### 14 删除字典类型

| 属性 | 值 |
|------|-----|
| **请求方式** | `DELETE` |
| **接口路径** | `/system/dict/type/{dictIds}` |
| **接口说明** | 批量删除字典类型，同时清除对应缓存 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:dict:remove` |
| **标签** | 字典管理 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `dictIds` | Long[] | 是 | 字典ID数组，多个用逗号分隔 | `1,2,3` |

---

#### 响应

##### 成功响应 -- HTTP 200

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
| 200 | 500 | 字典类型下存在字典数据 | `"{字典名称}已分配,不能删除"` |

**三层错误追踪**:
1. **路径参数类型转换失败**: 非数字时触发 `MethodArgumentTypeMismatchException`。
2. **Service 层业务检查**: `deleteDictTypeByIds` 遍历待删除字典，若该 `dictType` 被 `sys_dict_data` 引用则 `throw new ServiceException("{}已分配,不能删除", x.getDictName())`，`{}` 由 `StrFormatter.format` 替换。
3. **全局异常处理**: `handleServiceException` 捕获，返回 code=500。

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 分配检查 | 字典类型下存在字典数据时不允许删除 |
| 缓存清除 | 删除成功后清除对应字典类型在 `SYS_DICT` 和 `SYS_DICT_TYPE` 缓存中的数据 |

---

### 15 刷新字典缓存

| 属性 | 值 |
|------|-----|
| **请求方式** | `DELETE` |
| **接口路径** | `/system/dict/type/refreshCache` |
| **接口说明** | 清空所有字典相关 Redis 缓存（SYS_DICT + SYS_DICT_TYPE） |
| **认证方式** | 需要认证 |
| **权限要求** | `system:dict:remove` |
| **分布式锁** | 是（`@Lock4j`） |
| **标签** | 字典管理 |

---

#### 请求

**请求头**: [认证]

无请求参数。

---

#### 响应

##### 成功响应 -- HTTP 200

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
| 分布式锁 | 使用 `@Lock4j` 分布式锁保护，防止并发刷新导致缓存不一致 |
| 缓存范围 | 清空所有 `SYS_DICT` (字典数据) 和 `SYS_DICT_TYPE` (字典类型) 缓存 |
| 自动重建 | 缓存清空后，后续查询时会自动从数据库加载并重新缓存 |

---

### 16 获取字典选择框列表

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/system/dict/type/optionselect` |
| **接口说明** | 获取所有字典类型的下拉选择框数据 |
| **认证方式** | 需要认证 |
| **权限要求** | 无 |
| **标签** | 字典管理 |

---

#### 请求

**请求头**: [认证]

无请求参数。

---

#### 响应

##### 成功响应 -- HTTP 200

`R<List<SysDictTypeVo>>`

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": [
    {
      "dictId": 1,
      "dictName": "用户性别",
      "dictType": "sys_user_sex",
      "remark": "用户性别列表",
      "createTime": "2024-01-15 10:30:00"
    },
    {
      "dictId": 2,
      "dictName": "菜单状态",
      "dictType": "sys_show_hide",
      "remark": "菜单状态列表",
      "createTime": "2024-01-15 10:30:00"
    }
  ]
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |

---

## 三、字典数据管理

### 17 查询字典数据列表

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/system/dict/data/list` |
| **接口说明** | 分页查询字典数据列表，支持按字典标签、字典类型、排序号等条件筛选 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:dict:list` |
| **标签** | 字典管理 |

---

#### 请求

**请求头**: [认证]

**查询参数**:

| 参数名 | 类型 | 必填 | 匹配方式 | 说明 | 示例 |
|--------|------|:---:|:---:|------|------|
| `pageNum` | Integer | 否 | -- | 当前页码，默认 1 | `1` |
| `pageSize` | Integer | 否 | -- | 每页条数，默认 Integer.MAX_VALUE | `10` |
| `orderByColumn` | String | 否 | -- | 排序列名 | `"dictSort"` |
| `isAsc` | String | 否 | -- | 升序/降序 (asc/desc) | `"asc"` |
| `dictSort` | Integer | 否 | eq | 字典排序号，精确匹配 | `0` |
| `dictLabel` | String | 否 | like | 字典标签，模糊匹配 | `"男"` |
| `dictType` | String | 否 | eq | 字典类型，精确匹配 | `"sys_user_sex"` |

**备注**: 默认按 `dictSort` ASC, `dictCode` ASC 排序。

---

#### 响应

##### 成功响应 -- HTTP 200

响应体引用: [SysDictDataVo](../entities/SysDictDataVo.md)

外层由 `TableDataInfo` 包装：

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "rows": [
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
    ],
    "total": 1
  }
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |

---

### 18 导出字典数据列表

| 属性 | 值 |
|------|-----|
| **请求方式** | `POST` |
| **接口路径** | `/system/dict/data/export` |
| **接口说明** | 根据查询条件导出字典数据到 Excel 文件 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:dict:export` |
| **标签** | 字典管理 |

---

#### 请求

**请求头**: [认证]

**查询参数**:

| 参数名 | 类型 | 必填 | 匹配方式 | 说明 | 示例 |
|--------|------|:---:|:---:|------|------|
| `dictSort` | Integer | 否 | eq | 字典排序 | `0` |
| `dictLabel` | String | 否 | like | 字典标签 | `"男"` |
| `dictType` | String | 否 | eq | 字典类型 | `"sys_user_sex"` |

---

#### 响应

##### 成功响应 -- HTTP 200

直接返回 Excel 二进制文件流，文件名格式为 `字典数据.xlsx`。

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 导出成功 | -- |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |

---

### 19 查询字典数据详细

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/system/dict/data/{dictCode}` |
| **接口说明** | 根据字典编码查询单个字典数据的详细信息 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:dict:query` |
| **标签** | 字典管理 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `dictCode` | Long | 是 | 字典编码（主键） | `1` |

---

#### 响应

##### 成功响应 -- HTTP 200

响应体引用: [SysDictDataVo](../entities/SysDictDataVo.md)

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
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
}
```

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |
| 200 | 500 | 字典数据不存在 | `"操作成功"`（data 为 null） |

---

### 20 根据字典类型查询字典数据

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/system/dict/data/type/{dictType}` |
| **接口说明** | 根据字典类型查询该类型下所有字典数据（含缓存） |
| **认证方式** | 需要认证 |
| **权限要求** | 无 |
| **标签** | 字典管理 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `dictType` | String | 是 | 字典类型 | `"sys_user_sex"` |

---

#### 响应

##### 成功响应 -- HTTP 200

`R<List<SysDictDataVo>>`

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": [
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
    },
    {
      "dictCode": 2,
      "dictSort": 1,
      "dictLabel": "女",
      "dictValue": "1",
      "dictType": "sys_user_sex",
      "cssClass": "",
      "listClass": "warning",
      "isDefault": "N",
      "remark": "性别女",
      "createTime": "2024-01-15 10:30:00"
    }
  ]
}
```

**备注**: 当数据库和缓存中都没有数据时，返回空数组 `[]`。

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 操作成功 | `"操作成功"` |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 缓存优先 | 使用 `@Cacheable`（Redis），缓存名 `SYS_DICT`，key 为 `dictType`。首次查询从数据库加载并缓存，后续查询直接从缓存返回 |
| 空值保护 | 若数据库查询结果为空（null），返回空列表而非 null，防止缓存穿透 |

---

### 21 新增字典数据

| 属性 | 值 |
|------|-----|
| **请求方式** | `POST` |
| **接口路径** | `/system/dict/data` |
| **接口说明** | 新增一条字典数据项，同时更新对应类型缓存 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:dict:add` |
| **防重提交** | 是（`@RepeatSubmit`） |
| **标签** | 字典管理 |

---

#### 请求

**请求头**: [认证]

**请求体**: [SysDictDataBo](../entities/SysDictDataBo.md)

```json
{
  "dictSort": 0,
  "dictLabel": "男",
  "dictValue": "0",
  "dictType": "sys_user_sex",
  "cssClass": "",
  "listClass": "success",
  "isDefault": "N",
  "remark": "性别男"
}
```

**必填字段**: `dictLabel`, `dictValue`, `dictType`

---

#### 响应

##### 成功响应 -- HTTP 200

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
| 200 | 500 | 同类型下字典键值已存在 | `"新增字典数据'0'失败，字典键值已存在"` |
| 200 | 500 | 插入数据库失败 | `"操作失败"` |
| 200 | 500 | DTO 校验失败（`dictLabel` 为空） | 校验消息 |
| 200 | 500 | DTO 校验失败（`dictValue` 为空） | 校验消息 |
| 200 | 500 | DTO 校验失败（`dictType` 为空） | 校验消息 |
| 200 | 500 | 重复提交 | `"不允许重复提交，请稍候再试"` |

**三层错误追踪**:
1. **DTO 校验层**: `@Validated` + `@NotBlank`/`@Size` 触发校验，全局异常处理器处理。
2. **Controller 业务检查**: `checkDictDataUnique` 返回 false 时 `R.fail("新增字典数据'...'失败，字典键值已存在")`。
3. **Service 层**: `insertDictData` 中 `baseMapper.insert` 返回 0 行时 `throw new ServiceException("操作失败")`。

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 键值唯一性 | 同 `dictType` 下 `dictValue` 必须唯一（新增时不排除任何记录） |
| 缓存更新 | 新增成功后自动更新 `SYS_DICT` 缓存（key=`dictType`），刷新为包含新数据的列表 |

---

### 22 修改字典数据

| 属性 | 值 |
|------|-----|
| **请求方式** | `PUT` |
| **接口路径** | `/system/dict/data` |
| **接口说明** | 修改一条已有字典数据项的信息，同时更新对应类型缓存 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:dict:edit` |
| **防重提交** | 是（`@RepeatSubmit`） |
| **标签** | 字典管理 |

---

#### 请求

**请求头**: [认证]

**请求体**: [SysDictDataBo](../entities/SysDictDataBo.md)

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
  "remark": "性别男"
}
```

**必填字段**: `dictCode`（修改必须指定）, `dictLabel`, `dictValue`, `dictType`

---

#### 响应

##### 成功响应 -- HTTP 200

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
| 200 | 500 | 同类型下字典键值已存在（排除自身） | `"修改字典数据'0'失败，字典键值已存在"` |
| 200 | 500 | 更新数据库失败 | `"操作失败"` |
| 200 | 500 | DTO 校验失败 | 校验消息 |
| 200 | 500 | 重复提交 | `"不允许重复提交，请稍候再试"` |

**三层错误追踪**:
1. **DTO 校验层**: `@Validated` 触发校验，全局处理器处理。
2. **Controller 业务检查**: `checkDictDataUnique` 返回 false 时 `R.fail("修改字典数据'...'失败，字典键值已存在")`。
3. **Service 层**: `updateDictData` 中更新失败时 `throw new ServiceException("操作失败")`（含缓存更新失败）。

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 键值唯一性 | 同 `dictType` 下 `dictValue` 必须唯一（修改时排除自身 `dictCode`） |
| 缓存更新 | 修改成功后自动更新 `SYS_DICT` 缓存（key=`dictType`），刷新为最新的字典数据列表 |

---

### 23 删除字典数据

| 属性 | 值 |
|------|-----|
| **请求方式** | `DELETE` |
| **接口路径** | `/system/dict/data/{dictCodes}` |
| **接口说明** | 批量删除字典数据，同时清除对应类型的缓存 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:dict:remove` |
| **标签** | 字典管理 |

---

#### 请求

**请求头**: [认证]

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|:---:|------|------|
| `dictCodes` | Long[] | 是 | 字典编码数组，多个用逗号分隔 | `1,2,3` |

---

#### 响应

##### 成功响应 -- HTTP 200

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
| 200 | 500 | 路径参数类型不匹配 | `"请求参数类型不匹配，参数[dictCodes]要求类型为：'[Ljava.lang.Long;'，但输入值为：'...'"` |

**备注**: 删除字典数据无需分配检查，可直接删除。删除后自动清除对应 `dictType` 的 `SYS_DICT` 缓存。

**三层错误追踪**:
1. **路径参数类型转换失败**: 非数字触发 `MethodArgumentTypeMismatchException`。
2. **Service 层**: `deleteDictDataByIds` 查询待删除记录后执行删除，每删除一条清除对应类型的缓存。
3. **全局异常处理**: `handleMethodArgumentTypeMismatchException` 返回参数类型不匹配消息。

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 缓存清除 | 删除后逐条清除被删数据对应 `dictType` 的 `SYS_DICT` 缓存，后续查询将自动从数据库重新加载 |
| 批量删除 | 支持一次删除多条字典数据 |

---

> 文档生成时间: 2026-07-14 | 接口总数: 23 | 覆盖控制器: `SysPostController`, `SysDictTypeController`, `SysDictDataController`
