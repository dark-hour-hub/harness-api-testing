---
name: diff-analysis
description: 对 config.yaml 中 source.backend[].path 执行 git diff（基准分支 main），分析变更代码的影响范围，追踪受影响的 Controller 和 Service，输出差异分析报告到 tests/diff/_workflow/01-diff-analysis/。触发：/diff-analysis、执行 diff 分析、git diff 分析、代码变更分析、差异报告。
---

# 差异分析器

对源码执行 git diff，追踪变更代码的影响链（变更文件 → 受影响 Controller → 受影响 Service），输出 Markdown 报告。

## 输入

1. `config.yaml` — 读取 `source.backend[]` 中 `enabled: true` 的项目路径
2. Git 仓库 — 对每个 backend path 执行 `git diff main...HEAD`

## 输出

```
tests/diff/_workflow/01-diff-analysis/
├── diff-report.md              # 差异分析报告
├── changed-files.txt           # 变更文件列表
├── api-impact.yaml             # 受影响 API 清单（结构化数据）
└── call-chain.yaml             # 变更影响链追踪结果
```

## 流程

### Step 1 — 读取配置

读取 `config.yaml`，提取 `source.backend[]` 中所有 `enabled: true` 的项目，收集：
- `name` — 项目名称
- `path` — 源码路径
- `git.branch` — 基准分支（默认 `main`）

### Step 2 — Git Diff

对每个 backend 项目执行：

```bash
cd <project_path>
git fetch origin <base_branch>
git diff origin/<base_branch>...HEAD --name-only
git diff origin/<base_branch>...HEAD -- "*.java"
```

**注意**：
- 基准分支从 `config.yaml` 的 `git.branch` 读取，若为空则默认 `main`
- 仅分析 `.java` 文件变更（Controller 和 Service 层）
- 若项目不是 git 仓库或无变更，记录并跳过

### Step 3 — 变更文件分类

按 Spring MVC 标准目录结构对变更文件分类：

| 文件前缀模式 | 类型 | 分析深度 |
|-------------|------|---------|
| `**/controller/**` | Controller 层 | 提取 API 路径、HTTP 方法、请求参数 |
| `**/service/**` 或 `**/serviceimpl/**` | Service 层 | 提取Service接口和实现类 |
| `**/domain/**` 或 `**/entity/**` | 实体层 | 提取字段变更 |
| `**/mapper/**` | DAO 层 | 仅记录 |
| 其他 | 其他 | 仅记录 |

### Step 4 — Controller 影响分析

对每个变更的 Controller 文件：

1. **读取完整 diff 内容**，提取：
   - 变更的方法签名（新增/修改/删除）
   - 变更的 `@RequestMapping` 系列注解（路径、HTTP 方法）
   - 变更的请求参数（`@RequestBody`、`@PathVariable`、`@RequestParam`）

2. **提取 API 元信息**：
   - 完整路径 = 类级 `@RequestMapping` + 方法级 `@GetMapping`/`@PostMapping` 等
   - HTTP 方法从注解类型判断
   - 权限注解（`@PreAuthorize`）提取权限字符串

3. **输出变更摘要**：
   ```markdown
   ### POST /auth/login - 用户登录

   **变更类型**: 修改（Modification）
   **文件**: `ruoyi-web/src/main/java/org/dromara/web/controller/AuthController.java`

   **变更内容**:
   - 新增参数: `captchaEnabled` (Boolean), `deviceId` (String)
   - 新增响应字段: `refresh_token`, `expires_in`

   **影响分析**:
   - 涉及登录流程变更，需更新登录相关测试用例
   ```

### Step 5 — Service 影响链追踪

对每个变更的 Service 文件，通过 CodeGraph 追踪影响链：

1. **查找 Controller 调用链**：用 `codegraph_callers` 查找谁调用了这个 Service
2. **向上回溯**：如果 Service 被 Controller 调用，标记该 Controller 为受影响
3. **向下追踪**：如果 Service 调用了其他 Service或 Mapper，递归追踪
4. **构建影响链**：

```
变更文件: AuthServiceImpl.java
├── 被调用: AuthController.login()
│   └── API: POST /auth/login
├── 调用: TokenService.refreshToken()
│   └── 影响: Token 相关接口
```

### Step 6 — 生成报告

#### 6.1 diff-report.md

```markdown
# 差异分析报告

**生成时间**: {timestamp}
**基准分支**: {base_branch}
**目标分支**: HEAD
**项目数**: {n}

---

## 变更概览

| 变更类型 | 文件数 | 说明 |
|---------|-------|------|
| Controller | {n} | API 接口变更 |
| Service | {n} | 业务逻辑变更 |
| Entity | {n} | 数据模型变更 |
| Mapper | {n} | 数据访问变更 |
| 其他 | {n} | 配置/工具类等 |

---

## 变更详情（按项目分组）

### 项目: {project_name}

#### 一、Controller 层变更

##### 1. {ClassName}.java - {变更方法数} 个方法变更

| 方法 | HTTP | 路径 | 变更类型 | 说明 |
|------|------|------|---------|------|
| login() | POST | /auth/login | 修改 | 新增参数 |

**Diff 摘要**:
{diff_hunk}

**影响分析**:
- 影响 API: `POST /auth/login`
- 涉及 Service: `AuthService`, `TokenService`

---

## 受影响 API 清单

| API | 方法 | 变更类型 | 影响模块 |
|-----|------|---------|---------|
| /auth/login | POST | 修改 | 认证模块 |
| /auth/token/refresh | POST | 新增 | 认证模块 |

---

## 变更影响链

### 影响链 1: AuthServiceImpl

```
AuthServiceImpl.java (变更)
  └── 调用者: AuthController.login()
       └── API: POST /auth/login
  └── 调用: TokenService.refreshToken()
       └── 影响: Token 刷新逻辑
```

---

## 附录：完整 Diff

<details>
<summary>点击展开</summary>

\`\`\`diff
{full_diff_content}
\`\`\`

</details>
```

#### 6.2 api-impact.yaml（结构化数据）

```yaml
generated_at: "{timestamp}"
base_branch: main
target_branch: HEAD

projects:
  - name: "RuoYi-Vue-Plus"
    path: "D:/java/project/RuoYi-Vue-Plus"

summary:
  total_changed_files: 8
  controller_changes: 3
  service_changes: 4
  entity_changes: 1

changed_apis:
  - class: AuthController
    method: login
    path: /auth/login
    http_method: POST
    change_type: modified
    change_summary: "新增 captchaEnabled, deviceId 参数"
    affected_services:
      - AuthService
      - TokenService

  - class: AuthController
    method: refreshToken
    path: /auth/token/refresh
    http_method: POST
    change_type: added
    change_summary: "新增 refresh token 接口"
    affected_services:
      - TokenService

call_chains:
  - changed_file: AuthServiceImpl.java
    type: service
    callers:
      - class: AuthController
        method: login
        api: POST /auth/login
    callees:
      - TokenService
```

#### 6.3 changed-files.txt

每行一个变更文件路径，格式：`[类型] 文件路径`

```
[Controller] ruoyi-web/src/main/java/org/dromara/web/controller/AuthController.java
[Service] ruoyi-service/src/main/java/org/dromara/system/service/impl/AuthServiceImpl.java
```

## 分析规则

### 变更类型判定

| Git diff 状态 | 变更类型 |
|--------------|---------|
| 新文件 | added |
| 删除文件 | deleted |
| 修改现有文件 | modified |

### 影响范围判定

1. **直接影响的 API**：变更文件是 Controller → 该 Controller 的所有方法标记为受影响
2. **间接影响的 API**：变更文件是 Service → 追踪调用链，找到所有调用该 Service 的 Controller

### CodeGraph 使用

当追踪 Service 影响链时，使用 CodeGraph 工具：

| 场景 | 工具 |
|------|------|
| 查找 Service 被哪些 Controller 调用 | `codegraph_callers` |
| 查找 Service 调用了哪些下层服务 | `codegraph_callees` |
| 追踪完整调用链 | `codegraph_trace` |
| 查看 Service 源码 | `codegraph_node` |

## 注意事项

- 仅分析 `.java` 文件变更，其他文件类型仅记录路径
- Controller 变更需要提取完整的 API 信息（路径、方法、参数）
- Service 变更需要追踪完整影响链
- 如果 git 仓库不可用或无法执行 diff，记录错误并跳过该项目
- 变更文件如果无法解析（路径不规范），标记为 `unknown` 类型
