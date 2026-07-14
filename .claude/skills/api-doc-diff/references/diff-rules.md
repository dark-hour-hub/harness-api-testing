# 增量对比规则

当代码变更文档不存在时，本文件提供 git diff + CodeGraph 自动发现变更的详细规则。

---

## 1. Git Diff 发现变更

### 1.1 获取变更文件

对每个 backend 项目：

```bash
cd <project_path>
git diff --name-only        # 工作区 vs HEAD（未提交变更）
git diff HEAD~1 --name-only # 最近一次提交 vs 前一次（已提交变更）

# 只保留 .java 文件
grep "\.java$"
```

### 1.2 分类变更文件

| 路径模式 | 类型 | 处理方式 |
|------|------|------|
| `**/controller/**` | Controller | 提取方法级 diff，映射到 API |
| `**/model/**` 或 `**/entity/**` | Entity | 提取字段 diff |
| `**/service/**` | Service | 通过 CodeGraph 追踪调用链 |
| `**/dto/**` 或 `**/vo/**` | DTO/VO | 等同于 Entity 处理 |

### 1.3 提取 API 变更

对每个变更的 Controller 文件，执行 `git diff <file>`，按以下规则提取：

1. 新增方法上有 `@XxxMapping` → **added**（新 API）
2. 删除方法上有 `@XxxMapping` → **deleted**（删除 API）
3. 方法体内变更（参数/逻辑）→ **modified**（修改 API）
4. 注解属性变更（路径/方法名）→ **modified**

从注解提取：HTTP 方法（`@PostMapping`/`@GetMapping` 等）、完整路径（类级 + 方法级）、请求参数（`@RequestBody`/`@PathVariable`/`@RequestParam`）。

### 1.4 提取实体变更

对每个变更的 Entity/DTO/VO 文件，执行 `git diff <file>`：

1. 新增字段（带 `+` 标记）→ 记录字段名、类型、注解
2. 删除字段（带 `-` 标记）→ 记录字段名
3. 字段注解变更（`@Size`/`@NotBlank`/`@Column` 等属性变化）→ 记录 before/after

用 CodeGraph 追溯所有引用该实体的 API（通过 `_manifest.yaml` 中 routes 的 request_body 和 response_type）。

---

## 2. 对照基线判定变更类型

### 2.1 API 变更判定

对每个从 git diff 提取的 API，在基线 `_manifest.yaml` 的 `modules[].routes[]` 中查找：

| 基线状态 | diff 状态 | 判定为 |
|------|------|:--:|
| 未找到（method+path 不匹配） | 新增文件 | `added` |
| 找到 | 文件被修改 | `modified` |
| 找到 | 文件被删除 | `deleted` |
| 未找到 | 新增于已有 Controller | `added`（可能属于已有模块或新模块） |

### 2.2 实体变更判定

对照基线 `entities/_index.yaml`：

| 基线状态 | diff 状态 | 判定为 |
|------|------|:--:|
| 未找到 | 新增文件 | `added` |
| 找到 | 字段/注解变化 | `modified` |
| 找到 | 文件被删除 | `deleted` |

### 2.3 模块归属

对每个变更 API，在基线 `_manifest.yaml` 中找其所属模块（通过 `modules[].routes[]` 匹配 method+path）。新增 API 按 URL 第一段归入已有模块或创建新模块。

---

## 3. 生成精简变更清单

当代码变更文档不存在时，生成如下格式的临时变更清单（用于驱动后续 Step 4-6）：

```markdown
# 自动发现的变更清单

## 1. 变更概要
（自动统计）

## 2. 接口变更
（每条 API 变更一行，含 method/path/change_type/controller/变更说明）
格式同 `.claude/references/代码变更说明文档模板.md` 的第 2 节。

## 3. 实体字段变更
（每个变更实体一个表）
格式同 `.claude/references/代码变更说明文档模板.md` 的第 3 节。
```

> 测试要点列留空，后续生成模块文档时补充。

---

## 4. 生成范围规则

### 4.1 必须生成

- 所有 `added` / `modified` / `deleted` 的 API 所属模块 → `modules/`
- 所有 `added` / `modified` 的实体 → `entities/`
- 变更 API 的 request_body / response_type 引用的实体（即使未变更）→ `entities/`（照抄基线）
- 主文档 `API接口文档.md`

### 4.2 不生成

- 未变更的模块文档
- 未变更且未被引用的实体文档
- 未变更的接口段落（在模块文档中保留，但不新建未变更模块的文档）

### 4.3 实体引用追溯

对每个变更 API，从基线 `_manifest.yaml` 的 `routes[]` 中提取 `request_body` 和 `response_type` 字段，从全量名称中提取实体类名（如 `R<LoginVo>` → `LoginVo`）。在 `entities/_index.yaml` 中查这些实体，**未变更的照抄、变更的重生成**。

---

## 5. 照抄规则

### 5.1 主文档照抄

直接从基线 `API接口文档.md` 复制以下段落到输出：

- 项目信息表
- 测试账号
- 全局默认请求头
- 响应包装说明
- 权限体系

**例外**：若变更文档第 5、6 节标记认证/框架变更，则对应段落需要更新（按 `api-doc-discover` 的 Step 1 规则重新生成）。

### 5.2 实体文档照抄

从基线 `entities/{Entity}.md` 直接复制未变更实体的完整文件到输出目录。

### 5.3 模块文档局部照抄

对于 `modified` 模块：
1. 先复制基线模块文档的整体结构（文件头 + 请求头引用块）
2. 定位变更 API 的段落（按 `### {序号} {接口名称}` 标题匹配），用当前源码重写该段
3. 未变更 API 的段落原样保留，不修改

---

## 6. 实体文档修改规则

对于 `modified` 实体：
1. 照抄基线 entities/{Entity}.md 中除了"字段定义"表外的所有内容
2. 字段定义表中：
   - 新增字段 → 在表中对应位置插入新行（按源码字段顺序）
   - 修改字段 → 更新对应行的"约束/校验规则"列
   - 删除字段 → 删除对应行
3. 更新"注解转义说明"表（如有新增/删除转义）
4. 更新 JSON 示例（如有字段变更）
5. 更新页脚生成日期
