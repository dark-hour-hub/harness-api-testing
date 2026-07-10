---
name: api-doc-module
description: 为单个模块生成 API 接口文档。读取 _manifest.yaml 获取模块路由清单，用 CodeGraph 读 Controller/Service 源码，按模板逐接口生成完整文档到 modules/{模块}.md。触发：api-doc 全流程第三步、/api-doc-module、生成模块接口文档。
---

# API 模块文档生成器

为每个模块（或拆分后的子模块）生成接口明细文档，输出到 `modules/` 目录。

## 前置输入

1. `tests/baseline/_workflow/03-api-docs/_manifest.yaml` — 模块路由清单 + 全局上下文
2. `tests/baseline/_workflow/03-api-docs/API接口文档.md` — 模块文档
3. `tests/baseline/_workflow/03-api-docs/entities/` — 实体文件目录（按需读取）
4. `.claude/references/模块文档模板.md` — 输出模板（文件头 + 接口段 + 段落规则）
5. `.claude/references/i18n-resolution.md` - i18n 消息解析

## 输出产物

```
tests/baseline/_workflow/03-api-docs/modules/
├── 01-xx.md
├── 02-yy-part1.md
├── 02-yy-part2.md
├── 03-zz.md
└── ...
```

---

## 流程

### Step 1 — 读取 manifest

读 `_manifest.yaml`，获取：
- `system` / `response_wrapper` / `test_accounts` / `auth` / `permission_model` — 全局上下文
- `modules[]` — 所有模块的路由清单

### Step 2 — 确定执行计划

对每个模块，检查 `split_plan`：
- `null` 或接口数 ≤ 15 → **单 Agent**
- 有拆分 → **按 part 数派发多个 Agent**，每个 Agent 处理对应 `route_indices`

**派发优先级**：小模块（≤ 8 接口）先发出，大模块紧接着发出。所有 Agent 并行运行。

### Step 3 — 派发 Agent

每个 Agent prompt 必须包含：

1. **全局上下文**（精简内联）：
   - `base_url`、`auth_header`、`token_prefix`
   - `response_wrapper`（R 的 code/msg/data 字段名、TableDataInfo 的 code/msg/rows/total 字段名）
   - `public_headers` / `auth_headers`
   - `permission_model`

2. **本模块路由清单**（从 manifest 对应 `route_indices` 提取）

3. **Controller 类名 + Service 类名**（Agent 自己用 codegraph 读源码）

4. **输出模板**：Agent 必须在生成前 Read `.claude/references/模块文档模板.md`，严格按照模板中的文件头、接口段、段落规则输出。模板包含：
   - 文件头模板（模块标题 + 请求头引用块）
   - 接口段模板（属性表 → 请求 → 响应 → 业务规则的完整四级标题结构）
   - 段落规则（路径参数/查询参数/请求体/成功响应/错误响应/实体引用的具体格式要求）

5. **生成铁律**（见下方 Agent 规则）

6. **i18n 解析指令**：
   - 错误响应 msg 来源有三种：校验注解 `message="{key}"`（需查 properties）、Service 层 `MessageUtils.message("key")`（需查 properties）、硬编码字符串（直接用）
   - 前两种必须搜索 properties 文件尝试解析，按 `i18n-resolution.md` 流程执行
   - 寻找 properties 文件：用 Glob 搜索源码根目录下 `**/resources/**/messages*.properties`
   - 翻译后的实际文本填入 msg 列；仅在找不到时保留原始 key，并标注 `(i18n key, 未找到翻译)`

### Step 4 — 验证

Agent 返回后，检查模块文件：
- 接口数 = manifest 记录数
- 无摘要表格、无内联字段替代实体引用
- 每个接口有完整的 `#### 请求` / `#### 响应` 四级标题段

对缺失/不合格的模块，派修复 Agent（轻量，只修指定问题）。

---

## Agent 生成规则

### 源码读取（Agent 自己执行）

用 `codegraph_explore` 一次性读取本模块所有 Controller + 关键 ServiceImpl：

```
codegraph_explore query="AuthController CaptchaController SysLoginService" maxFiles=8 projectPath="D:/java/project/RuoYi-Vue-Plus"
```

实体文件从 `entities/` 目录按需 Read，不预加载全部。

**当需要解析 i18n 消息时**，同步搜索项目的 i18n 资源文件。用 Glob 搜索 `{源码根目录}/**/src/main/resources/**/messages*.properties`，优先级：当前模块 resources > 主应用 resources > common 模块 resources。具体解析流程见 `i18n-resolution.md`。

### 输出模板

Agent 必须在开始生成前 Read `.claude/references/模块文档模板.md`，该文件包含：
- 文件头模板（含请求头引用块）
- 接口段模板（属性表 → `#### 请求` → `#### 响应` → `#### 业务规则` 的四级标题结构）
- 段落规则（路径参数表/查询参数表/请求体/成功响应/错误响应/实体引用的具体格式）

### 铁律

1. **每个接口独立成段**：完整的属性表 + `#### 请求` + `#### 响应`(含 `##### 成功响应` 和 `##### 错误响应`)
2. **严禁摘要表格**：不得有"其余接口"、"接口 N-M（摘要）"等折叠形式
3. **实体引用 > 内联**：请求体/响应体有实体文件 → 写 `[{ClassName}](../entities/{ClassName}.md)`，禁止 `（含 xxx、xxx 等字段）`
4. **穷举查询参数**：GET 分页接口 = PageQuery 字段 + Bo 全部可查询字段（排除 @JsonIgnore），每个字段标注实际匹配方式（精确/模糊/区间/IN）
5. **错误路径三层追踪 + i18n 解析**：DTO 校验注解 message → Service 层 throw → 全局异常处理器。每层捕获到的错误消息若为 i18n key 格式（`{xxx}` 或 `MessageUtils.message("key")`），必须尝试从 properties 文件解析为实际文本。解析流程参考 `i18n-resolution.md`。
6. **无则删除**：无路径参数/查询参数/请求体/业务规则 → 删除对应段落，不留空表
7. **i18n key 必须尝试解析**：错误响应 msg 列中的值，若来源为 i18n key（校验注解 `{key}` / `MessageUtils.message("key")`）→ 必须尝试在 properties 文件中查找翻译。找到 → 填入翻译后的实际文本，附注 key 名；找不到 → 保留原始 key，标注为待验证。禁止不经查找直接用 key 作为 msg。

### 返回前自检

- [ ] 每个接口有 `#### 请求` 和 `#### 响应` 四级标题
- [ ] 响应含 `##### 成功响应` 和 `##### 错误响应` 两个子段
- [ ] 无摘要表格、无内联字段描述替代实体引用
- [ ] 模块文档开头有请求头引用块
- [ ] 有实体文件 → 已引用；无 → 已展开完整字段表
- [ ] 错误响应 msg 已从 i18n key 解析为实际文本（能找到的已翻译，找不到的已标记）
- [ ] 错误响应表覆盖 DTO 校验 + Service 异常 + 全局异常处理三层

---

## 禁止

- Agent prompt 中内联 Controller/Service/实体源码——让 Agent 自己按需读取
- 在主会话预读所有实体文件——只传类名清单
- 逐条 `codegraph_node`——用 `codegraph_explore` 批量读
- 一个 Agent 处理多个不相关模块——严格按 manifest 的模块边界
- 靠方法名推断 HTTP 方法——必须看 `@XxxMapping` 注解
- 查询参数筛选——Bo 类字段全部列出，从 ServiceImpl 交叉验证后标注匹配方式
