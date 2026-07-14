# 系统管理 Part 4 -- 岗位管理 + 字典管理 API 文档（增量）

> Controllers: `SysPostController`, `SysDictTypeController`, `SysDictDataController` | Base URL: `http://localhost:8080` | Auth: Sa-Token JWT `Authorization: Bearer {token}` + `clientid: e5cd7e4891bf95d1d19206ce24a7b32e`

## 请求头

| 头名称 | 值 | 说明 |
|--------|-----|------|
| Content-Type | `application/json` | 请求体格式；文件下载使用 `application/octet-stream` |
| Authorization | `Bearer {token}` | Sa-Token JWT 令牌，登录后获取 |
| clientid | `e5cd7e4891bf95d1d19206ce24a7b32e` | 客户端 ID，与 Token 绑定 |

---

## 一、岗位管理

### 1 获取岗位列表 <span style="color:orange">**[修改]**</span>

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/system/post/list` |
| **接口说明** | 分页查询岗位列表，支持按岗位编码、岗位名称、岗位类别、状态、部门等条件筛选 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:post:list` |
| **标签** | 岗位管理 |
| **变更类型** | `modified` |

---

#### 变更说明

`SysPostVo` 新增 `address` 字段（String 类型），`SysPostServiceImpl.selectPostList()` 遍历每个岗位 VO 设置 `address = "LosAngeles"`。本变更疑似调试/占位代码，正式上线前需确认字段用途。

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

#### 断言

| # | 层级 | 断言项 | 预期值 | 断言消息 |
|---|:---:|--------|--------|------|
| 1 | 协议层 | HTTP 状态码 | 200 | "HTTP状态码应为200" |
| 2 | 业务层 | code | 200 | "业务状态码应为200" |
| 3 | 业务层 | msg | "查询成功" | "提示消息应为'查询成功'" |
| 4 | 数据层 | rows[*].address 存在性 | 存在 | "每个岗位应包含address字段" |
| 5 | 数据层 | rows[*].address 类型 | String | "address字段类型应为String" |
| 6 | 数据层 | rows[*].address 值 | "LosAngeles" | "address字段值应为'LosAngeles'" |
| 7 | 数据层 | rows[*].postId 存在性 | 存在 | "原有字段postId应仍然存在" |
| 8 | 数据层 | rows[*].postCode 存在性 | 存在 | "原有字段postCode应仍然存在" |
| 9 | 数据层 | rows[*].postName 存在性 | 存在 | "原有字段postName应仍然存在" |
| 10 | 数据层 | rows[0].address 值 | "LosAngeles" | "第一个岗位address应为'LosAngeles'" |

---

### 2 导出岗位列表 <span style="color:orange">**[修改]**</span>

| 属性 | 值 |
|------|-----|
| **请求方式** | `POST` |
| **接口路径** | `/system/post/export` |
| **接口说明** | 根据查询条件导出岗位数据到 Excel 文件 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:post:export` |
| **标签** | 岗位管理 |
| **变更类型** | `modified` |

---

#### 变更说明

导出功能调用 `selectPostList()`，Excel 导出结果将包含新增的 `address` 列。

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

直接返回 Excel 二进制文件流，文件名格式为 `岗位数据.xlsx`。Content-Type 为 `application/octet-stream`，`Content-Disposition` 包含 `attachment` 头。Excel 包含 `address` 列。

##### 错误响应

| HTTP | code | 触发条件 | msg |
|:----:|:----:|----------|-----|
| 200 | 200 | 导出成功 | -- |
| 401 | 401 | Token 缺失或失效 | `"认证失败，无法访问系统资源"` |
| 403 | 403 | 权限不足 | `"没有访问权限，请联系管理员授权"` |

---

#### 断言

| # | 层级 | 断言项 | 预期值 | 断言消息 |
|---|:---:|--------|--------|------|
| 1 | 协议层 | HTTP 状态码 | 200 | "HTTP状态码应为200" |
| 2 | 业务层 | Content-Type | `application/octet-stream` | "应为Excel文件流" |
| 3 | 业务层 | Content-Disposition 包含 attachment | 包含 `"attachment"` | "应触发文件下载" |
| 4 | 数据层 | 导出文件包含 address 列 | 存在 | "导出文件应包含address列" |
| 5 | 数据层 | 导出文件包含原有列 postCode | 存在 | "导出文件应包含postCode列" |

---

### 3 根据岗位编号获取详细信息 <span style="color:orange">**[修改]**</span>

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/system/post/{postId}` |
| **接口说明** | 根据岗位ID查询单个岗位的详细信息 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:post:query` |
| **标签** | 岗位管理 |
| **变更类型** | `modified` |

---

#### 变更说明

`SysPostServiceImpl.selectPostById()` → `baseMapper.selectVoList()` 返回的 `SysPostVo` 包含新增 `address` 字段。

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

#### 断言

| # | 层级 | 断言项 | 预期值 | 断言消息 |
|---|:---:|--------|--------|------|
| 1 | 协议层 | HTTP 状态码 | 200 | "HTTP状态码应为200" |
| 2 | 业务层 | code | 200 | "业务状态码应为200" |
| 3 | 数据层 | data.address 存在性 | 存在 | "岗位详情应包含address字段" |
| 4 | 数据层 | data.address 类型 | String | "address字段类型应为String" |
| 5 | 数据层 | data.address 值 | "LosAngeles" | "address字段值应为'LosAngeles'" |

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

---

#### 业务规则

| 规则 | 说明 |
|------|------|
| 分配检查 | 岗位下存在已分配用户时不允许删除 |
| 批量删除 | 支持一次删除多个岗位，任一岗位不满足条件则整个请求失败 |

---

### 7 获取岗位选择框列表 <span style="color:orange">**[修改]**</span>

| 属性 | 值 |
|------|-----|
| **请求方式** | `GET` |
| **接口路径** | `/system/post/optionselect` |
| **接口说明** | 获取岗位下拉选择框数据，可按部门筛选或按指定岗位ID列表查询 |
| **认证方式** | 需要认证 |
| **权限要求** | `system:post:query` |
| **标签** | 岗位管理 |
| **变更类型** | `modified` |

---

#### 变更说明

`SysPostVo` 新增 `address` 字段影响此接口。当按部门筛选（`deptId` 存在）时，返回的岗位列表每项包含 `address` 字段。

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

`R<List<SysPostVo>>`

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": [
    {
      "postId": 1,
      "postCode": "ceo",
      "postName": "董事长",
      "address": "LosAngeles"
    },
    {
      "postId": 2,
      "postCode": "se",
      "postName": "项目经理",
      "address": "LosAngeles"
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

#### 断言

| # | 层级 | 断言项 | 预期值 | 断言消息 |
|---|:---:|--------|--------|------|
| 1 | 协议层 | HTTP 状态码 | 200 | "HTTP状态码应为200" |
| 2 | 业务层 | code | 200 | "业务状态码应为200" |
| 3 | 数据层 | data[*].address 存在性（deptId模式） | 存在 | "选项列表每项应包含address字段" |
| 4 | 数据层 | data[*].address 值 | "LosAngeles" | "address字段值应为'LosAngeles'" |
| 5 | 数据层 | data[*].postId 存在性 | 存在 | "postId字段应存在" |
| 6 | 数据层 | data[*].postCode 存在性 | 存在 | "postCode字段应存在" |

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
        }
      ]
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

> 以下字典类型管理、字典数据管理接口（9-23）未变更，参见基线文档 `02-系统管理-part4.md`。

---

> 文档生成时间: 2026-07-14 | 变更接口数: 4 (岗位管理) | 覆盖控制器: `SysPostController`
