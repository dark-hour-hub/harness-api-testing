# 增量测试需求

> **分析范围**: 工作区未提交变更 (`git diff HEAD`) + 最近一次提交 (`git diff HEAD~1..HEAD`)
> **生成时间**: `2026-07-13`
> **源码项目**: `RuoYi-Vue-Plus` (`D:/java/project/RuoYi-Vue-Plus`)
> **基线路径**: `tests/baseline/_workflow`
> **HEAD 提交**: `e49f02f89` — update 优化 异常处理
>
> 本文档基于 `git diff HEAD` + `git diff HEAD~1..HEAD` + CodeGraph 影响链分析生成。开发者可手动修改。

---

## 1. 变更概要

| 维度 | 数量 | 说明 |
|------|:----:|------|
| 新增接口 | 1 | `GET /new`（工作区未提交） |
| 修改接口 | 1 (直接) + 8 (间接) | 岗位列表响应体新增字段；工作流异常匹配修复 |
| 删除接口 | 0 | |
| 新增/修改实体字段 | 1 | `SysPostVo.address` 新增 |
| 认证变更 | 否 | |
| 框架变更 | 是 | Java 17 → 21（工作区未提交）；验证码/API加密关闭 |

---

## 2. 接口变更

---

### 2.1 `GET /new` — 新增首页欢迎接口 `新增`

| 属性 | 值 |
|------|-----|
| **变更类型** | `add` |
| **所属模块** | ruoyi-admin (首页) |
| **Controller** | `IndexController.hello()` |
| **变更说明** | 在 `IndexController` 中新增 `GET /new` 端点，无鉴权，返回欢迎消息字符串。与已有的 `GET /` 类似但不返回 JSON 统一响应体格式。 |
| **影响已有用例** | 无 |
| **来源** | 工作区未提交 |

**测试要点**：

| # | 分类 | 优先级 | 测试点 | 预期结果 |
|---|------|:---:|------|------|
| 1 | 正向功能 | P0 | `GET /new` 无鉴权访问 | HTTP 200，返回包含应用名称的欢迎字符串 |
| 2 | 正向功能 | P1 | `GET /new` 携带有效 token 访问 | HTTP 200，正常返回（无鉴权拦截） |
| 3 | 正向功能 | P1 | 验证响应格式为纯文本字符串（非 `{code, msg, data}` 结构） | HTTP 200，`Content-Type: text/plain` |

---

### 2.2 `GET /system/post/list` — 岗位列表响应体新增 `address` 字段 `修改`

| 属性 | 值 |
|------|-----|
| **变更类型** | `update` |
| **所属模块** | ruoyi-system (系统管理-岗位管理) |
| **Controller** | `SysPostController.list()` |
| **变更说明** | `SysPostVo` 新增 `address` 字段；`SysPostServiceImpl.selectPostList()` 遍历每个岗位 VO 设置 `address = "LosAngeles"`。本变更疑似调试/占位代码，正式上线前需确认字段用途。 |
| **影响已有用例** | TC_POST_001, TC_POST_002（岗位列表断言需增加 address 字段校验） |
| **来源** | 工作区未提交 |

**测试要点**：

| # | 分类 | 优先级 | 测试点 | 预期结果 |
|---|------|:---:|------|------|
| 1 | 响应字段变更 | P0 | `GET /system/post/list` 分页查询岗位列表 | HTTP 200，`rows[].address` 字段存在且值为 `"LosAngeles"` |
| 2 | 数据一致性 | P1 | `GET /system/post/list` 查询所有岗位，验证每个岗位均包含 `address` 字段 | 所有岗位 `address = "LosAngeles"`，字段类型为 String |
| 3 | 回归 | P1 | `GET /system/post/list` 正常分页参数 | 原有字段（postId, postCode, postName 等）不受影响 |

---

### 2.3 `GET /system/post/{postId}` — 岗位详情响应体新增 `address` 字段 `修改`

| 属性 | 值 |
|------|-----|
| **变更类型** | `update` |
| **所属模块** | ruoyi-system (系统管理-岗位管理) |
| **Controller** | `SysPostController.getInfo()` |
| **变更说明** | 通过 `SysPostServiceImpl.selectPostById()` → `baseMapper.selectVoList()` 返回的 `SysPostVo` 包含新增 `address` 字段。 |
| **影响已有用例** | TC_POST_*（岗位详情查询） |
| **来源** | 工作区未提交 |

**测试要点**：

| # | 分类 | 优先级 | 测试点 | 预期结果 |
|---|------|:---:|------|------|
| 1 | 响应字段变更 | P1 | `GET /system/post/{postId}` 查询单个岗位 | HTTP 200，响应体包含 `address` 字段 |

---

### 2.4 `GET /system/post/optionselect` — 岗位选项响应体新增 `address` 字段 `修改`

| 属性 | 值 |
|------|-----|
| **变更类型** | `update` |
| **所属模块** | ruoyi-system (系统管理-岗位管理) |
| **Controller** | `SysPostController.optionselect()` |
| **变更说明** | `SysPostVo` 新增字段影响所有返回 `SysPostVo` 的接口。 |
| **影响已有用例** | 岗位选项相关用例 |
| **来源** | 工作区未提交 |

**测试要点**：

| # | 分类 | 优先级 | 测试点 | 预期结果 |
|---|------|:---:|------|------|
| 1 | 响应字段变更 | P1 | `GET /system/post/optionselect` | HTTP 200，选项列表每项包含 `address` 字段 |

---

### 2.5 `POST /system/post/export` — 岗位导出包含 `address` 列 `修改`

| 属性 | 值 |
|------|-----|
| **变更类型** | `update` |
| **所属模块** | ruoyi-system (系统管理-岗位管理) |
| **Controller** | `SysPostController.export()` |
| **变更说明** | 导出功能调用 `selectPostList()`，Excel 导出结果将包含新增的 `address` 列。 |
| **影响已有用例** | 岗位导出相关用例 |
| **来源** | 工作区未提交 |

**测试要点**：

| # | 分类 | 优先级 | 测试点 | 预期结果 |
|---|------|:---:|------|------|
| 1 | 响应字段变更 | P1 | `POST /system/post/export` 导出岗位 | 导出文件包含 `address` 列 |

---

### 2.6 `GET /system/user/getInfo` — 用户信息中岗位数据含 `address` `修改`

| 属性 | 值 |
|------|-----|
| **变更类型** | `update` |
| **所属模块** | ruoyi-system (系统管理-用户管理) |
| **Controller** | `SysUserController.getInfo()` |
| **变更说明** | `SysUserInfoVo.posts` 为 `List<SysPostVo>`，用户信息查询时岗位列表将包含 `address` 字段。同时影响 `POST /auth/login` 响应（登录时构建 `LoginUser` 也包含岗位信息）。 |
| **影响已有用例** | TC_USER_*（用户信息查询），登录相关用例 |
| **来源** | 工作区未提交 |

**测试要点**：

| # | 分类 | 优先级 | 测试点 | 预期结果 |
|---|------|:---:|------|------|
| 1 | 响应字段变更 | P1 | `GET /system/user/getInfo` | 响应中 `posts[].address` 字段存在 |
| 2 | 回归 | P0 | `POST /auth/login` 登录成功 | 登录响应中岗位信息正常，无异常 |

---

### 2.7 `POST /workflow/task/getNextNodeList` — 异常跳过条件扩展 `修改`

| 属性 | 值 |
|------|-----|
| **变更类型** | `update` |
| **所属模块** | ruoyi-workflow (工作流-任务管理) |
| **Controller** | `FlwTaskController.getNextNodeList()` |
| **变更说明** | `FlwTaskServiceImpl.getNextNodeList()` 中条件变量缺失的异常匹配逻辑扩展：从仅匹配 `NULL_CONDITION_VALUE` 改为同时匹配 `NULL_CONDITION_VALUE` 和 `NULL_SKIP_TYPE`。修复条件分支跳过类型缺失导致流程异常中断的问题。 |
| **影响已有用例** | TC_WF_TASK_*（工作流任务查询相关） |
| **来源** | 已提交 (e49f02f89) |

**测试要点**：

| # | 分类 | 优先级 | 测试点 | 预期结果 |
|---|------|:---:|------|------|
| 1 | 正向功能 | P0 | `POST /workflow/task/getNextNodeList` 在包含跳过类型节点的流程中获取下一节点 | 正常返回下一节点列表，不因 `NULL_SKIP_TYPE` 异常中断 |
| 2 | 异常处理 | P1 | 模拟其他类型 `FlowException`（非跳过/条件缺失类异常） | 仍然正常抛出异常，不会被错误跳过 |
| 3 | 回归 | P0 | `POST /workflow/task/getNextNodeList` 正常流程获取下一节点 | 功能不受影响 |

---

### 2.8 `POST /workflow/task/completeTask` + `POST /workflow/task/backProcess` + `POST /workflow/task/skipTask` — 间接影响 `修改`

| 属性 | 值 |
|------|-----|
| **变更类型** | `update` |
| **所属模块** | ruoyi-workflow (工作流-任务管理) |
| **Controller** | `FlwTaskController.completeTask()` / `FlwTaskController.backProcess()` |
| **变更说明** | `FlwTaskServiceImpl.completeTask()` 和 `skipTask()` 内部也调用 `getNextNodeList()`，间接受到异常匹配逻辑扩展的影响。 |
| **影响已有用例** | TC_WF_TASK_* |
| **来源** | 已提交 (e49f02f89) |

**测试要点**：

| # | 分类 | 优先级 | 测试点 | 预期结果 |
|---|------|:---:|------|------|
| 1 | 回归 | P0 | `POST /workflow/task/completeTask` 正常办理任务 | 任务完成，流程推进到下一节点 |
| 2 | 回归 | P0 | `POST /workflow/task/backProcess` 正常驳回任务 | 驳回成功，可再重新提交 |

---

## 3. 实体字段变更

### 3.1 `SysPostVo.address`

| 字段 | 变更类型 | 类型 | 变更前 | 变更后 |
|------|:---:|------|------|------|
| `address` | `add` | `String` | 不存在 | `private String address;`（`selectPostList()` 中赋值为 `"LosAngeles"`） |

**受影响接口**：

| 接口 | 影响方式 | 说明 |
|------|:---:|------|
| `GET /system/post/list` | 响应体 | 列表每项含 `address` |
| `GET /system/post/{postId}` | 响应体 | 详情含 `address` |
| `GET /system/post/optionselect` | 响应体 | 选项含 `address` |
| `POST /system/post/export` | 响应体(导出文件) | 导出含 `address` 列 |
| `GET /system/user/getInfo` | 响应体 | 用户岗位信息含 `address` |
| `POST /auth/login` | 响应体 | 登录用户岗位含 `address` |
| `GET /workflow/task/currentTaskAllUser/{taskId}` | 响应体(summary) | 任务指派人岗位含 `address` |

> 已包含在第 2 节接口变更中，此处不再重复列出测试要点。

---

## 4. Service 层变更（间接影响）

| Service | 变更方法 | 受影响 API | 影响说明 | 建议 |
|------|------|------|------|------|
| `SysPostServiceImpl` | `selectPostList` (修改) | `GET /system/post/list`, `/post/{postId}`, `/post/optionselect`, `/post/export` | 遍历结果设置 `address = "LosAngeles"` | 确认是否为调试代码；如正式功能需补充数据库字段 |
| `SysPostServiceImpl` | `selectPostAll` (间接) | `GET /system/post/optionselect` | 返回 `List<SysPostVo>`，VO 包含新增字段 | 回归 |
| `SysPostServiceImpl` | `selectPostById` (间接) | `GET /system/post/{postId}` | 同上 | 回归 |
| `SysPostServiceImpl` | `selectPostsByUserId` (间接) | `GET /system/user/getInfo`, `POST /auth/login` | 同上 | 回归 |
| `FlwTaskServiceImpl` | `getNextNodeList` (修改) | `POST /workflow/task/getNextNodeList` | 异常匹配扩展 `NULL_SKIP_TYPE` | 回归含条件分支的流程 |
| `FlwTaskServiceImpl` | `completeTask` (间接) | `POST /workflow/task/completeTask` | 内部调用 `getNextNodeList` | 回归 |
| `FlwTaskServiceImpl` | `skipTask` (间接) | `POST /workflow/task/taskOperation/{skip}` | 内部调用 `getNextNodeList` | 回归 |

---

## 5. 认证变更

> 无直接认证逻辑变更。但以下配置变更影响认证测试：
> - 验证码 (`captcha.enable`) 已关闭 → 登录测试不再需要验证码
> - API 加密 (`api-decrypt.enabled`) 已关闭 → 请求体不再需要 AES 加密

---

## 6. 框架/配置变更

| 变更项 | 变更前 | 变更后 | 测试影响 |
|------|------|------|------|
| Java 版本 | 17 | 21 | 虚拟线程等新特性可用；需确认测试环境 JDK ≥ 21 |
| 验证码 (`captcha.enable`) | `true` | `false` | 登录测试无需获取验证码，简化测试流程 |
| API 接口加密 (`api-decrypt.enabled`) | `true` | `false` | 请求体无需 AES 加密，可直接传明文 JSON |
| 数据库地址 | `localhost:3306` | `180.76.180.32:3306` | 远程数据库，注意网络延迟和权限 |
| Redis 地址 | `localhost:6379` | `180.76.180.32:6379` | 远程 Redis，确认密码 `123456` |
| Redisson clientName | `RuoYi-Vue-Plus` | (注释掉) | 使用默认名称 |
| 邮件配置 | `xxx@163.com` | `17816890438@163.com` / `2472072904@qq.com` | 仅开发环境 |

---

## 7. 回归清单

| 接口 | 回归原因 | 来源 |
|------|------|:---:|
| `GET /` | `IndexController` 同文件修改，确认原有首页未受影响 | `same_module` |
| `GET /system/post/list` | `SysPostVo` 新增字段 + `selectPostList` 逻辑修改 | `service_chain` |
| `GET /system/post/{postId}` | `SysPostVo` 新增字段 | `service_chain` |
| `GET /system/post/optionselect` | `SysPostVo` 新增字段 | `service_chain` |
| `POST /system/post/export` | `SysPostVo` 新增字段 | `service_chain` |
| `POST /system/post` | 新增岗位确认不受 address 字段影响 | `same_module` |
| `PUT /system/post` | 修改岗位确认不受 address 字段影响 | `same_module` |
| `DELETE /system/post/{postIds}` | 删除岗位确认正常 | `same_module` |
| `GET /system/user/getInfo` | 用户信息中岗位数据新增 address | `service_chain` |
| `POST /workflow/task/getNextNodeList` | `NULL_SKIP_TYPE` 异常跳过逻辑扩展 | `service_chain` |
| `POST /workflow/task/completeTask` | 间接调用 `getNextNodeList` | `service_chain` |
| `POST /workflow/task/backProcess` | 间接调用 `getNextNodeList` | `service_chain` |
| `POST /auth/login` | 冒烟基线 + 验证码已关闭需重新验证登录流程 | `smoke` |
| `POST /auth/logout` | 冒烟基线 | `smoke` |
| `GET /system/user/list` | 冒烟基线 | `smoke` |

---

## 8. 废弃用例

> 无。

---

## 附录：变更源码对照

### A. `IndexController.java` (`ruoyi-admin/src/main/java/org/dromara/web/controller/IndexController.java`) — 工作区未提交

```diff
+    @GetMapping("/new")
+    public String hello() {
+        return StringUtils.format("{} 新增接口", SpringUtils.getApplicationName());
+    }
```

### B. `SysPostVo.java` (`ruoyi-modules/ruoyi-system/src/main/java/org/dromara/system/domain/vo/SysPostVo.java`) — 工作区未提交

```diff
+    /**
+     * 地址
+     */
+    private String address;
```

### C. `SysPostServiceImpl.java` (`ruoyi-modules/ruoyi-system/src/main/java/org/dromara/system/service/impl/SysPostServiceImpl.java`) — 工作区未提交

```diff
-        return baseMapper.selectVoList(buildQueryWrapper(post));
+        List<SysPostVo> sysPostVos = baseMapper.selectVoList(buildQueryWrapper(post));
+        for (SysPostVo sysPostVo : sysPostVos) {
+            sysPostVo.setAddress("LosAngeles");
+        }
+        return sysPostVos;
```

### D. `FlwTaskServiceImpl.java` (`ruoyi-modules/ruoyi-workflow/src/main/java/org/dromara/workflow/service/impl/FlwTaskServiceImpl.java`) — 已提交 e49f02f89

```diff
-                if (!ExceptionCons.NULL_CONDITION_VALUE.equals(e.getMessage())) {
+                if (!StringUtils.containsAny(e.getMessage(), ExceptionCons.NULL_CONDITION_VALUE, ExceptionCons.NULL_SKIP_TYPE)) {
                     throw e;
                 }
```

### E. `pom.xml` — 工作区未提交

```diff
-        <java.version>17</java.version>
+        <java.version>21</java.version>
```

### F. `application.yml` (`ruoyi-admin/src/main/resources/application.yml`) — 工作区未提交

```diff
-  enable: true    # captcha
+  enable: false   # captcha

-  enabled: true   # api-decrypt
+  enabled: false  # api-decrypt
```

### 影响链

```
工作区未提交:
  IndexController.hello() 新增
    └── GET /new → 新增无鉴权端点

  SysPostVo.address 新增
    └── SysPostServiceImpl.selectPostList() 赋值 "LosAngeles"
         ├── GET /system/post/list → 响应体新增 address 字段
         ├── GET /system/post/{postId} → 响应体新增 address 字段
         ├── GET /system/post/optionselect → 响应体新增 address 字段
         └── POST /system/post/export → 导出含 address 列
              └── SysPostServiceImpl.selectPostAll() / selectPostById() / selectPostsByUserId()
                   ├── GET /system/user/getInfo → 用户岗位含 address
                   └── POST /auth/login → 登录响应岗位含 address

  配置变更:
    ├── captcha.enable=false → 登录无需验证码
    ├── api-decrypt.enabled=false → 请求无需 AES 加密
    ├── java.version=21 → 需 JDK 21 运行
    └── DB/Redis → 远程 180.76.180.32

已提交 e49f02f89:
  FlwTaskServiceImpl.getNextNodeList() 异常匹配扩展
    ├── POST /workflow/task/getNextNodeList → NULL_SKIP_TYPE 异常不再中断
    ├── FlwTaskServiceImpl.completeTask() → 间接影响
    │    └── POST /workflow/task/completeTask
    ├── FlwTaskServiceImpl.skipTask() → 间接影响
    │    └── POST /workflow/task/taskOperation/{skip}
    └── POST /workflow/task/backProcess → 独立调用，无间接影响
```
