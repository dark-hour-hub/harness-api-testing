---
name: analyze-source
description: 分析源码结构，识别 Controller、API 接口、Vue 页面，支持技术栈检测和微服务分析
allowed-tools: Read, Glob, Grep, Bash
triggers:
  - 执行 /test 命令
  - 用户说"分析源码"、"分析项目"
---

# 源码分析技能

## 执行步骤

### 1. 读取配置

读取 `config.yaml`，获取源码路径配置：
- `source.backend[].path` - 后端源码路径
- `source.frontend[].path` - 前端源码路径

### 2. 初始化 CodeGraph

对于 `config.yaml` 中配置的每个源码路径（`source.backend[].path` 和 `source.frontend[].path`）：

1. 检查项目目录下是否存在 `.codegraph/` 文件夹
2. 如果不存在，执行 `codegraph init -i` 初始化索引
3. 如果已存在，执行 `codegraph --incremental` 更新索引

### 3. 结合 CodeGraph 分析代码

结合上一步生成的 CodeGraph 索引进行深度分析。

**CodeGraph 可用工具**（通过 MCP 或 CLI）：

| 工具 | 用途 |
|------|------|
| `codegraph_status` | 检查索引状态和统计 |
| `codegraph_search` | 按名称查找符号（类/函数/方法） |
| `codegraph_context` | 获取符号的完整上下文（调用者+被调用者） |
| `codegraph_explore` | 查看多个相关符号的源码（一次性返回） |
| `codegraph_trace` | 追踪两个符号之间的调用路径 |
| `codegraph_impact` | 分析变更符号的影响半径 |
| `codegraph_files` | 获取项目文件结构树 |
| `codegraph_callers` | 查找调用某个符号的所有位置 |
| `codegraph_callees` | 查找某个符号调用的所有位置 |

**优先使用 CodeGraph 的场景**：
- 查找符号（类/函数/方法）的位置和定义 → 用 `codegraph_search`
- 理解某个类的调用/被调用关系 → 用 `codegraph_context`
- 追踪数据流（如 "请求如何到达数据库"）→ 用 `codegraph_trace`
- **追踪错误路径（如 "错误密码 → Asserts.fail → GlobalExceptionHandler"）→ 用 `codegraph_trace` 或 `codegraph_callees`**
- 查找"修改这个函数会影响哪些代码" → 用 `codegraph_impact`
- 快速了解项目结构 → 用 `codegraph_files`
- **验证反向用例的真实 code/message → 用 `codegraph_trace` 从 Controller 方法到 Service 方法，找到异常抛出点**

### 4. 技术栈检测

自动检测项目使用的技术框架：

#### 后端框架检测

| 框架 | 检测方式 |
|------|---------|
| Spring MVC | `pom.xml` + `@RestController` |
| Spring WebFlux | `RouterFunction` |
| Flask | `requirements.txt` + `@app.route` |
| Express | `package.json` + `app.get` |

#### 前端框架检测

| 框架 | 检测方式 |
|------|---------|
| Vue 2/3 | `package.json` + `.vue` 文件 |
| React | `package.json` + `.jsx` 文件 |
| Element Plus | `el-input`, `el-button` |

### 5. 微服务架构分析

如果存在多个后端服务，识别：
- 服务名称
- 服务端口
- 服务依赖

### 6. 分析后端源码

找出所有 Controller 类（`*Controller.java`），提取完整的 API 定义，包括请求体和响应字段。

#### 6.1 提取 Controller 方法

1. 识别 HTTP 方法注解（`@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`）
2. 解析路径（`path` 属性）
3. 解析参数来源：
   - `@RequestBody` → 请求体，提取 DTO 类名
   - `@PathVariable` → URL 路径参数
   - `@RequestParam` → 查询参数
   - `@RequestHeader` → 请求头参数
4. 解析权限注解（`@PreAuthorize`, `@Secured`）

#### 6.2 提取请求体定义（request_body）

通过以下方式获取 DTO/BO 的字段结构：

1. **直接分析 DTO 类源码**：
   - 查找 `*DTO.java`, `*VO.java`, `*BO.java`, `*Request.java` 等文件
   - 提取所有字段（field），包括：字段名（name）、数据类型、是否必填、校验注解

2. **类型映射与必填判定**：参见 `template/analysis-reference.md`

#### 6.3 提取响应字段定义（response_fields）

1. **分析 VO 类源码**：查找 `*VO.java`, `*Response.java` 等文件，提取返回数据的字段结构
2. **分析 Result 包装类**：Spring Boot 常用 `Result<T>` 包装，实际数据在 `Result.data` 字段中
3. **常见结构**：`{"code": 200, "message": "操作成功", "data": { ... }}`

#### 6.4 API 定义格式

**模板文件**: `template/output-formats.md`（第1节：API 定义）

#### 6.5 DTO/VO 分析流程

**参考**: `template/analysis-reference.md`

### 6.6 错误路径追踪（必做 — 反向用例的 code/message 不能从 Controller 表面推断）

**核心原则**：Controller 中 `if (result == null) return CommonResult.validateFailed("...")` 这类代码**不一定是实际执行的路径**。Service 层可能在 return null 之前就抛出异常，绕过 Controller 的 return 语句，最终由 GlobalExceptionHandler 返回完全不同的 code 和 message。

**每个反向用例必须执行以下验证流程**：

```
1. 从 Controller 方法追踪进入 Service 实现
   用 codegraph_trace: from=<Controller.method> to=<Service.method>
   (如果 codegraph_trace 不可达，用 codegraph_callees 跳到 Service)

2. 在 Service 方法中定位对应场景的代码路径
   例如"密码错误"→ 找到 passwordEncoder.matches() 返回 false 的分支

3. 识别该路径上是否抛出异常
   - Asserts.fail(message) → throw new ApiException(message)
   - throw new XxxException(...) → 记录异常类型和参数

4. 判断异常是否被捕获：
   - 在 try{} 块内 且 被 catch(Type) 捕获 → 走到 catch 后的逻辑
   - 不在 try{} 内 / 异常类型不匹配 catch → 穿透到 GlobalExceptionHandler

5. 查询 GlobalExceptionHandler 的映射规则
   GlobalExceptionHandler(@ControllerAdvice) 中：
   - @ExceptionHandler(ApiException.class) → 如何提取 code 和 message？
   - errorCode 是否为 null？（查 ApiException 构造器）
   - null → CommonResult.failed(message) → code=500
   - 非null → CommonResult.failed(errorCode) → code=errorCode.getCode()

6. 输出真实的 {code, message} 到断言
```

**常见错误模式**：

| Controller 表面代码 | 实际执行路径 | 正确断言 |
|-------------------|------------|---------|
| `if (token == null) return validateFailed("用户名或密码错误")` | Service 内 `Asserts.fail("密码不正确")` 抛 ApiException → GlobalExceptionHandler → code=500, message="密码不正确" | code=500, "密码不正确" |
| `if (result == null) return failed()` | Service 内 `Asserts.fail(IErrorCode)` 抛 ApiException(errorCode=SOME_CODE) → GlobalExceptionHandler → code=SOME_CODE, message=SOME_CODE.getMessage() | code=SOME_CODE.getCode(), message=SOME_CODE.getMessage() |
| `catch (XxxException) return failed("...")` | 如果 Service 内部 try-catch 了异常，则 Controller 的 return **确实**被执行 | 使用 Controller return 的 code/message |

**验证完成后**：将每个反向用例的 `business_code` 和 `message` 填入从真实调用路径推导的值，而非从 Controller return 语句猜测的值。

### 7. 分析前端源码

找出所有页面文件（`*.vue`），提取页面路径、组件名、元素选择器等信息。

**模板文件**: `template/output-formats.md`（第5节：前端页面）

### 8. 认证机制识别

分析登录流程和认证机制（JWT/Session/OAuth2 等）。

**模板文件**: `template/output-formats.md`（第6节：认证机制）

---

## 输出报告

### 分析报告（Markdown）

输出到 `tests/baseline/specs/{module}/*-analysis.md`。

**模板文件**: `template/output-formats.md`（第2节：分析报告）

### 规格文件（YAML）

输出到 `tests/baseline/specs/{module}/*-spec.yaml`。

**模板文件**: `template/output-formats.md`（第3节：规格文件）

### 测试用例文件（YAML）

分析完成后，为每个模块生成测试用例 YAML 文件，写入 `tests/baseline/_workflow/02-analysis-plan/testcases/{module}-testcases.yaml`。

#### 测试用例生成原则

基于 `apis.json` 中的 API 定义，为每个 API 生成完整的测试用例：

1. **用例完整性**：
   - 正向用例：有效参数验证接口基本功能
   - 反向用例：无效参数、无权限、边界值、必填项缺失等
   - 异常用例：超时、网络异常、依赖服务异常

2. **断言准确性（关键）**：
   - **正向用例**：断言基于 Controller → Service 的正常返回路径，code=200
   - **反向用例**：**禁止仅从 Controller return 语句推断**。必须按 6.6 节追踪完整调用链（Controller → Service → Asserts.fail → ApiException → GlobalExceptionHandler），确认实际的 code 和 message
   - 断言覆盖 HTTP 状态码、业务状态码、消息、数据字段

3. **断言分层**：
   - 协议层断言 → HTTP 状态码
   - 业务层断言 → code 字段（业务状态码）
   - 数据层断言 → message 字段 + data 字段具体值

4. **CRUD 生命周期完整性（必须遵守）**：
   对于有数据副作用的 API（创建、修改、删除），生成测试用例时必须遵循以下规则以确保测试可重复执行、不破坏共享状态：

   - **CREATE 操作 → 必须配对 DELETE 清理**：
     每个正向 CREATE 用例必须生成对应的 DELETE 清理用例，用 `${test_entity_id}` 变量传递被创建实体的 ID。
     ```
     TC_X_CREATE_001        → 创建实体 → 将 ID 存入 runtime_vars['test_entity_id']
     TC_X_CLEANUP_DELETE    → 用 ${test_entity_id} 删除该实体
     ```

   - **UPDATE 操作 → 必须配对 REVERT 还原**：
     每个正向 UPDATE 用例必须生成对应的 REVERT 用例，将修改的字段恢复为原始值。
     ```
     TC_X_UPDATE_001        → 修改字段 F 的值 from A to B
     TC_X_UPDATE_REVERT     → 将字段 F 的值 from B 恢复为 A
     ```

   - **UPDATE_PASSWORD 操作 → 必须配对密码回改（最高优先级）**：
     密码修改会直接影响 admin_token fixture，一旦密码变了但未回改，后续所有测试全部无法登录。
     ```
     TC_X_UPDATE_PASSWORD_001     → 改密码: old → new
     TC_X_UPDATE_PASSWORD_REVERT  → 改回: new → old
     ```

   - **DELETE 操作 → 仅删除 CREATE 创建的数据**：
     DELETE 正向用例只能通过 `${test_entity_id}` 等变量删除由本模块 CREATE 用例创建的测试数据，**严禁**硬编码删除系统预置/种子数据。

   - **禁止硬编码 ID**：
     路径 `/{id}` 中的 ID 禁止写死数字（如 `/admin/update/1`、`/admin/delete/1`），必须使用变量引用（如 `/admin/update/${test_user_id}`）。

   - **标签标记**：所有清理/还原用例必须添加 `cleanup` 和 `lifecycle` 标签。

   - **执行顺序**：清理用例通过 `execution_order: cleanup` 字段声明依赖顺序（执行引擎按此字段排序，cleanup 用例排在最后执行）。

**模板文件**: `template/testcase-template.yaml`（含字段说明、断言语法参考）

#### 测试用例生成流程

```
apis.json (API定义)
    ↓
解析每个API的请求参数 + 响应字段
    ↓
按 API 方法类型分类:
    ├── 读操作 (GET/query) → 无需 lifecycle
    └── 写操作 (POST create/update/delete) → 必须检查生命周期
    ↓
生成正向用例（基于 Controller → Service 正常返回路径）
    ↓
生成反向用例 → 追踪错误路径（6.6节）
    ├── codegraph_trace: Controller.method → Service.method
    ├── 定位异常抛出点（Asserts.fail / throw）
    ├── 判断异常穿透 or 被捕获
    └── 查询 GlobalExceptionHandler 映射 → 得到真实 code/message
    ↓
【CRUD Lifecycle】为写操作生成配对清理用例:
    ├── CREATE → 生成 DELETE cleanup 用例（用 ${test_entity_id} 传递）
    ├── UPDATE → 生成 REVERT 用例（恢复原始值）
    ├── UPDATE_PASSWORD → 最高优先级: 必须生成密码回改用例
    └── DELETE → 验证仅删除测试数据，不禁用系统数据
    ↓
填充测试数据（使用 ${timestamp}、${login_token} 等变量）
    ↓
写入断言（正向: code=200 / 反向: 追踪结果 / cleanup: code=200）
    ↓
输出到 testcases/{module}-testcases.yaml
```

#### YAML 安全规范

生成 YAML 测试用例时，必须遵守以下规则以避免解析错误：

1. **含冒号的值必须加引号**：任何 YAML 值中如果包含 `:` 后跟空格，必须用双引号包裹。
   - ❌ `token: exists_and_type: string`
   - ✅ `token: "exists_and_type: string"`
2. **特殊字符**：含 `#`、`{`、`}`、`[`、`]`、`&`、`*`、`!`、`|`、`>`、`%`、`@`、`` ` `` 的值需加引号。
3. **纯数字/布尔值**：`true`/`false`/`yes`/`no`/`null` 作为字符串时需加引号。

#### pytest 代码生成对照

**模板文件**: `template/pytest-codegen-template.py`

### 接口文件（JSON）

分析完成后，必须写入 `tests/baseline/_workflow/02-analysis-plan/apis.json`。

**模板文件**: `template/output-formats.md`（第4节：apis.json）

**重要**：`apis.json` 必须包含每个 API 的 `request_body` 和 `response_fields` 定义，获取方式：
- 解析 Controller 方法参数上的 `@RequestBody` 注解，找到对应的 DTO 类
- 解析 DTO 类的字段定义，包括类型、是否必填、校验规则
- 解析返回值 `Result<T>` 中的 T 类型（VO 类）获取响应字段

### 测试计划（Markdown）

输出到 `tests/baseline/_workflow/02-analysis-plan/generation-plan.md`。

**模板文件**: `template/generation-plan-template.md`

内容包括：测试范围、测试类型（API / UI / 性能）、预计脚本数量、优先级排序。

---

## 输出文件清单

分析完成后，必须生成以下所有文件：

| 文件 | 路径 | 模板 |
|------|------|------|
| 分析报告 | `tests/baseline/specs/{module}/*-analysis.md` | `template/output-formats.md` |
| 规格文件 | `tests/baseline/specs/{module}/*-spec.yaml` | `template/output-formats.md` |
| 接口文件 | `tests/baseline/_workflow/02-analysis-plan/apis.json` | `template/output-formats.md` |
| 测试计划 | `tests/baseline/_workflow/02-analysis-plan/generation-plan.md` | `template/generation-plan-template.md` |
| 测试用例 | `tests/baseline/_workflow/02-analysis-plan/testcases/{module}-testcases.yaml` | `template/testcase-template.yaml` |

**重要**: 以上所有文件都必须生成，缺一不可。

---

## 支持的分析器

### 后端分析器

| 框架 | 支持 | 识别方式 |
|------|------|---------|
| Spring MVC | ✅ | @GetMapping, @PostMapping 等 |
| Spring WebFlux | ✅ | RouterFunction |
| Flask | ✅ | @app.route |
| Express | ✅ | app.get, app.post |

### 前端分析器

| 框架 | 支持 | 识别方式 |
|------|------|---------|
| Vue 2/3 | ✅ | .vue 文件 + v-model |
| React | ✅ | .jsx 文件 |
| Element Plus | ✅ | el-input, el-button |

---

## 执行输出示例

```
================================================================================
[2/5] 源码分析...
================================================================================

✓ CodeGraph 索引状态:
    - mall-tiny: 95 文件, 1347 节点, 2421 边
    - mall-admin-web: 260 文件, 3343 节点, 7389 边

✓ 检测技术栈: Java Spring Boot + Vue 3
✓ 发现 2 个微服务
  - user-service: 8081
  - course-service: 8082

✓ 提取 API 端点: 85 个（含完整请求/响应结构）
  - 用户模块: 15 个
  - 课程模块: 20 个
  - 活动模块: 25 个
  - 系统模块: 25 个

✓ 提取请求体定义 (request_body): 60 个
  - 解析 DTO/VO 类获取字段结构
  - 识别必填字段（@NotNull/@NotBlank）
  - 识别校验规则（@Length/@Pattern/@Min/@Max）

✓ 提取响应字段定义 (response_fields): 70 个
  - 解析 VO 类获取返回结构
  - 识别 Result<T> 包装结构

✓ 分析前端页面: 30 个
  - 登录页: /login
  - 仪表盘: /dashboard
  - ...

✓ 识别认证机制: JWT
  - Token 头: Authorization: Bearer {token}
  - 登录接口: POST /api/auth/login

✓ 分析完成
  📁 分析报告: tests/baseline/specs/mall/mall-tiny-analysis.md
  📁 规格文件: tests/baseline/specs/mall/mall-spec.yaml
  📁 接口文件: tests/baseline/_workflow/02-analysis-plan/apis.json
  📁 测试计划: tests/baseline/_workflow/02-analysis-plan/generation-plan.md
  📁 测试用例: tests/baseline/_workflow/02-analysis-plan/testcases/ums-testcases.yaml
  📁 测试用例: tests/baseline/_workflow/02-analysis-plan/testcases/course-testcases.yaml
  ...

✓ 生成测试用例统计:
  - 用户模块(ums): 45 个用例
    - P0(核心路径): 8 个
    - P1(主要功能): 20 个
    - P2(细节验证): 17 个
  - 课程模块(course): 60 个用例
    - P0(核心路径): 12 个
    - P1(主要功能): 30 个
    - P2(细节验证): 18 个
  ...
```
