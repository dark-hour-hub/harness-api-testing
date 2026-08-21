---
name: api-doc-entities
description: 从 DTO/VO 源码生成实体类文档。读取 _manifest.yaml 中的 DTO/VO 清单，按模块并行派发 Agent，每个 Agent 用 CodeGraph 读取源码并按模板输出 entities/{ClassName}.md。触发：api-doc 全流程第二步、/api-doc-entities、生成实体文档。
---

# API 实体类文档生成器

从 manifest 的 DTO/VO 清单，按模块并行生成实体类文档到 `entities/` 目录。

## 前置输入

0. `config.yaml` — `source.backend[].path`（仅 `enabled: true`），作为 codegraph 的 `projectPath`
1. `tests/baseline/_workflow/03-api-docs/_manifest.yaml` — 取 `all_dtos` 和 `all_vos` 字段
2. `.opencode/references/实体类文档模板.md` — 实体文件模板
3. `.opencode/skills/api-doc-entities/references/field-resolution.md` — JSON 键名优先级链

## 输出产物

```
tests/baseline/_workflow/03-api-docs/entities/
├── _index.yaml          # 实体索引（ClassName → 文件路径 + 字段摘要）
├── LoginBody.md
├── LoginVo.md
├── SysUserBo.md
└── ...
```

---

## 流程

### Step 0 — 读取源码路径配置

读 `config.yaml`，提取 `source.backend[]` 中 `enabled: true` 的 `path`。取第一个作为默认 `projectPath`。

多后端时：每个 Agent 收到的 prompt 中标注该模块实体对应的 projectPath。若 `source.backend[]` 为空或全部 disabled，报错退出。

### Step 1 — 读取输入

读 `_manifest.yaml`，提取 `all_dtos` 和 `all_vos`。合并为一个全局去重清单，按模块分组。

### Step 2 — 按模块并行派发 Agent

对每个模块组（如 auth: 11 个实体、system: 39 个实体），并行派发一个 Agent。

**Agent prompt 必须包含**：

1. **本模块 DTO/VO 类名清单**（从 manifest 提取，仅本模块的）
2. **实体类文档模板**（完整内联）
3. **字段解析规则**（精简版，见下方 Agent 规则）
4. **源码项目路径**（Step 0 提取的 `projectPath`，传递给 codegraph 工具）
5. **禁止清单**

### Step 3 — 汇总索引

所有 Agent 完成后，扫描 `entities/` 目录下所有 `.md` 文件（排除 `_index.yaml`），写入 `entities/_index.yaml`：

```yaml
# 实体索引 — 由 api-doc-entities 生成
entities:
  LoginBody:
    file: LoginBody.md
    module: auth
    type: DTO
    fields: [code, uuid, username, password]
  LoginVo:
    file: LoginVo.md
    module: auth
    type: VO
    fields: [token, scope]
  # ...
```

---

## Agent 生成规则

### 源码读取

用 `codegraph_explore` 一次性批量读取本模块所有 DTO/VO 源码（1-2 次调用），**必须传入 `projectPath`**。**禁止逐条 `codegraph_node`**。

```
codegraph_explore query="LoginBody PasswordLoginBody LoginVo CaptchaVo ..." maxFiles=15 projectPath="{backend_path}"
```

`{backend_path}` 替换为 Step 0 获取的源码路径。

### 字段 JSON 键名（优先级链，命中即停止）

| 优先级 | 来源 | 示例 |
|--------|------|------|
| 1 | `@JsonProperty("xxx")` | `userName` → JSON 键 `"userName"` |
| 1 | `@JSONField(name="xxx")` | 同上 |
| 1 | `@SerializedName("xxx")` | 同上 |
| 2 | 类级 `@JsonNaming(SnakeCaseStrategy.class)` | `userName` → `"user_name"` |
| 3 | 全局 `spring.jackson.property-naming-strategy` | 检查 application.yml |
| 4 | 默认（Jackson 默认） | Java 字段名即为 JSON 键名 |

**注解转义记录**：Java 字段名 ≠ JSON 键名时，必须在实体文件的"注解转义说明"表中记录。

### 必填判定

从校验注解确定：`@NotNull`/`@NotBlank`/`@NotEmpty` → ✅ 必填。`@Length`/`@Size`/`@Pattern`/`@Min`/`@Max`/`@Email` 等 → 记录到"约束/校验规则"列。

### 父类字段

DTO/VO 有父类（如 `extends BaseEntity`）→ 递归追踪父类字段，合并到字段定义表。

### 输出

严格按实体类文档模板输出每个实体文件，包含：
- 基本信息表（类名、全限定名、类型、所属模块、父类、序列化特性）
- 注解转义说明（无则删除此段）
- 完整字段定义表（字段路径、JSON 键名、类型、必填、约束、默认值、说明、示例值）
- JSON 示例
- 嵌套对象展开子字段，`@JsonIgnore` 标注的字段保留但注明不参与序列化

### 去重

检查 `entities/` 目录已存在的文件，已存在则跳过（跨模块共享的实体只生成一次）。

---

## 禁止

- 逐条 `codegraph_node`——用 `codegraph_explore` 批量读
- 用 Java 字段名直接当 JSON 键名——必须检查序列化注解
- 跳过父类字段追踪
- 跳过注解转义记录
- 在 Agent 中积攒多个实体文件不写入——每完成一个实体立即写磁盘
- 生成非本模块的实体——严格按 manifest 清单执行
