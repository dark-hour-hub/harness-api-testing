# 数据安全规则

## 核心原则

配置中的测试账号为只读账号。测试用例只能创建新资源后操作新资源，禁止修改/删除已有系统数据。

## 账号保护

- 涉及"操作当前用户自身数据"的接口（修改密码、个人信息等）：
  - 若有可 extract 的 POST 创建接口（如 register 返回含 ID 的 VO）→ 先创建临时用户，用临时用户测试
  - 若无创建接口 → **跳过正向成功用例**，仅测试参数校验，添加注释说明原因
  - **禁止**使用 config.yaml accounts 中的任何账号测试此类接口——即使换用非特权账号（如 visitor），也会永久破坏该账号的密码
- 未指定 `account` 时使用最高权限账号

```yaml
- id: TC_XXX
  account: visitor          # 对应 config.yaml 中的 role
```

## 系统数据保护

以下类型禁止修改/删除已有记录：系统账号、菜单、权限、角色、系统配置、字典数据。

处理策略：
- 模块有 POST 且返回 data 含 ID → 创建新数据后操作新数据（extract 链）
- 模块无 POST 或 POST 返回 data 为 null → 仅生成 GET 查询用例，跳过 PUT/DELETE 成功用例，添加注释说明

## extract 前置验证

生成 POST 正向用例前必须检查返回类型：
- `R<Void>` / `void` / 无泛型 → data 为 null，**不生成 extract**，**跳过依赖此 POST 的 PUT/DELETE**
- `R<XxxVo>` → 可 extract，JSONPath 字段名需经序列化验证

## extract 链

```yaml
# POST — 创建并提取 ID
- id: TC_XXX_001
  extract:
    resourceId: "$.data.id"  # JSONPath，字段名已序列化验证

# PUT — 使用提取的 ID，通过 depends_on 声明依赖
- id: TC_XXX_002
  depends_on: ["TC_XXX_001"]
  path: /xxx/${resourceId}
  request:
    body:
      id: "${resourceId}"

# DELETE — 使用提取的 ID，通过 depends_on 声明依赖
- id: TC_XXX_003
  depends_on: ["TC_XXX_001"]
  path: /xxx/${resourceId}
```

### depends_on 说明

`depends_on` 声明用例间的数据依赖关系，确保运行时按序执行：

- 值：依赖的前置用例 ID 列表（`["TC_XXX_001"]`）
- 用途：标记 extract 变量来源，运行时框架据此决定执行顺序
- 范围：仅用于同一模块内的用例依赖

**规则**：
- POST 创建 → PUT 修改 / DELETE 删除 → 必须加 `depends_on`
- 资源不存在等反向用例 → 不使用 `depends_on`（参数为显式无效值）
- 仅有信息查询的用例 → 不需要 `depends_on`

## 资源 ID 规则

- PUT/DELETE 的资源 ID → 来自 `${变量名}` 引用，禁止硬编码已有 ID
- 查询已有数据 → 可硬编码 ID
- 参数校验反向用例（预期失败）→ 可用任意有效格式 ID

### 硬编码系统 ID 检测规则

生成阶段检测：

1. 扫描每条 PUT/DELETE 用例的 `path` 字段和 `request.body`
2. 若路径中包含纯数字段（如 `/xxx/1`、`/xxx/2`）且该段不是 `${变量}` 引用 → 标记为违规
3. 违规处理：
   - 若能从前置 POST 用例 extract ID → 改为 `${变量}` 引用 + 添加 `depends_on`
   - 若 POST 返回 `R<Void>` 无法 extract → 跳过该 PUT/DELETE 正向用例，仅保留参数校验反向用例，添加注释说明原因
4. 例外：GET 查询已有数据的用例可硬编码已知 ID（如查询默认管理员详情 `/xxx/1`）

**路径扫描正则**：匹配路径中纯数字段（如 `/1`、`/99999`），排除 `${变量}` 引用段。数字范围 1-999 属于可疑硬编码系统 ID（因系统数据通常在此范围内）。

## 唯一标识

创建数据时，唯一字段必须含随机后缀避免重复：

```yaml
request:
  body:
    username: "testuser_${timestamp}"
```

`${timestamp}` 由 runner_utils.py 在运行时替换为毫秒时间戳。

## 检查清单

- [ ] POST 返回类型已检查（`R<Void>` vs `R<XxxVo>`）
- [ ] extract JSONPath 字段名已经序列化验证
- [ ] PUT/DELETE 资源 ID 来自 extract 变量引用
- [ ] 场景链用例使用了 `depends_on` 声明依赖关系
- [ ] 唯一标识含 `${timestamp}`
- [ ] 无 POST 模块已跳过 PUT/DELETE 成功用例并注释
- [ ] 修改密码用例使用非特权账号
