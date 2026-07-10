# Diff 分析报告输出格式参考

## 报告结构

### 1. diff-report.md（主报告）

#### 文件头（Frontmatter）

```markdown
# 差异分析报告

**生成时间**: 2026-07-09 10:30:00
**基准分支**: main
**目标分支**: HEAD
**项目数**: 1
**分析路径**: D:/java/project/RuoYi-Vue-Plus
```

#### 变更概览表格

```markdown
## 变更概览

| 变更类型 | 文件数 | 说明 |
|---------|-------|------|
| Controller | 3 | API 接口变更 |
| Service | 4 | 业务逻辑变更 |
| Entity | 1 | 数据模型变更 |
| Mapper | 2 | 数据访问变更 |
| 其他 | 1 | 配置/工具类变更 |
| **合计** | **11** | |
```

#### Controller 变更详情

```markdown
### 项目: RuoYi-Vue-Plus

#### 一、Controller 层变更

##### 1. AuthController.java - 2 个方法变更

| 方法 | HTTP | 路径 | 变更类型 | 说明 |
|------|------|------|---------|------|
| login() | POST | /auth/login | 修改 | 新增参数 captchaEnabled, deviceId |
| refreshToken() | POST | /auth/token/refresh | 新增 | 新增 refresh token 接口 |

**Diff 摘要**:
```diff
-    public R<LoginVo> login(@RequestBody LoginBody loginBody) {
+    public R<LoginVo> login(@RequestBody LoginBody loginBody,
+                            @RequestParam(required = false) Boolean captchaEnabled,
+                            @RequestParam(required = false) String deviceId) {
```

**影响分析**:
- 影响 API: `POST /auth/login`
- 涉及 Service: `AuthService`, `TokenService`
- 建议: 更新登录测试用例，新增 token 刷新测试
```

#### Service 变更详情

```markdown
#### 二、Service 层变更

##### 1. AuthServiceImpl.java - 业务逻辑变更

**变更内容**:
- 新增方法: `refreshToken(String refreshToken)`
- 修改方法: `login(LoginBody loginBody)` - 新增设备绑定逻辑

**影响链追踪**:
```
AuthServiceImpl (变更)
  ├── 被调用: AuthController.login() → API: POST /auth/login
  ├── 被调用: AuthController.refreshToken() → API: POST /auth/token/refresh (新增)
  └── 调用: TokenService.refreshToken()
```

##### 2. TokenService.java - Token 处理变更

**变更内容**:
- 新增方法: `refreshToken()`, `validateRefreshToken()`

**影响链追踪**:
```
TokenService (变更)
  ├── 被调用: AuthServiceImpl.refreshToken()
  └── 调用: SysUserService.getUserById()
```
```

#### 受影响 API 清单

```markdown
## 受影响 API 清单

| API | 方法 | 变更类型 | 影响模块 | 测试建议 |
|-----|------|---------|---------|---------|
| /auth/login | POST | 修改 | 认证模块 | 更新现有用例，新增参数断言 |
| /auth/token/refresh | POST | 新增 | 认证模块 | 新增用例 |
| /auth/logout | POST | 无变更 | 认证模块 | 回归验证 |
```

#### 附录：完整 Diff

```markdown
## 附录：完整 Diff

<details>
<summary>点击展开</summary>

\`\`\`diff
diff --git a/ruoyi-web/src/main/java/org/dromara/web/controller/AuthController.java
...
@@ -45,8 +47,10 @@ public class AuthController {
-    public R<LoginVo> login(@RequestBody LoginBody loginBody) {
+    public R<LoginVo> login(@RequestBody LoginBody loginBody,
+                            @RequestParam(required = false) Boolean captchaEnabled,
+                            @RequestParam(required = false) String deviceId) {
...
\`\`\`

</details>
```

---

### 2. api-impact.yaml（结构化数据）

```yaml
generated_at: "2026-07-09T10:30:00"
base_branch: main
target_branch: HEAD

summary:
  total_changed_files: 11
  by_type:
    controller: 3
    service: 4
    entity: 1
    mapper: 2
    other: 1

projects:
  - name: "RuoYi-Vue-Plus"
    path: "D:/java/project/RuoYi-Vue-Plus"

changed_apis:
  - class: "AuthController"
    file: "ruoyi-web/src/main/java/org/dromara/web/controller/AuthController.java"
    changes:
      - method: "login"
        http_method: "POST"
        path: "/auth/login"
        change_type: "modified"
        change_summary: "新增 captchaEnabled, deviceId 参数"
        diff_hunk: |
          -    public R<LoginVo> login(@RequestBody LoginBody loginBody) {
          +    public R<LoginVo> login(@RequestBody LoginBody loginBody,
          +                            @RequestParam(required = false) Boolean captchaEnabled,
          +                            @RequestParam(required = false) String deviceId) {

  - class: "AuthController"
    file: "ruoyi-web/src/main/java/org/dromara/web/controller/AuthController.java"
    changes:
      - method: "refreshToken"
        http_method: "POST"
        path: "/auth/token/refresh"
        change_type: "added"
        change_summary: "新增 refresh token 接口"

changed_services:
  - class: "AuthServiceImpl"
    file: "ruoyi-service/src/main/java/org/dromara/system/service/impl/AuthServiceImpl.java"
    change_type: "modified"
    change_summary: "新增 refreshToken 方法，修改 login 方法"
    callers:
      - class: "AuthController"
        method: "login"
        api: "POST /auth/login"
      - class: "AuthController"
        method: "refreshToken"
        api: "POST /auth/token/refresh"
    callees:
      - "TokenService"

  - class: "TokenService"
    file: "ruoyi-service/src/main/java/org/dromara/system/service/TokenService.java"
    change_type: "modified"
    change_summary: "新增 refreshToken, validateRefreshToken 方法"
    callers:
      - "AuthServiceImpl"
    callees:
      - "SysUserService"
```

---

### 3. call-chain.yaml（调用链追踪）

```yaml
generated_at: "2026-07-09T10:30:00"

call_chains:
  - changed_file: "AuthServiceImpl.java"
    changed_type: "service"
    full_path: "ruoyi-service/src/main/java/org/dromara/system/service/impl/AuthServiceImpl.java"

    callers:
      - class: "AuthController"
        method: "login"
        api: "POST /auth/login"
        change_type: "modified"

    callees:
      - service: "TokenService"
        method: "refreshToken"
        change_type: "modified"

  - changed_file: "TokenService.java"
    changed_type: "service"
    full_path: "ruoyi-service/src/main/java/org/dromara/system/service/TokenService.java"

    callers:
      - service: "AuthServiceImpl"
        method: "refreshToken"
        change_type: "added"

    callees:
      - service: "SysUserService"
        method: "getUserById"
        change_type: "none"
```

---

### 4. changed-files.txt（文件清单）

```
[Controller] ruoyi-web/src/main/java/org/dromara/web/controller/AuthController.java
[Service] ruoyi-service/src/main/java/org/dromara/system/service/impl/AuthServiceImpl.java
[Service] ruoyi-service/src/main/java/org/dromara/system/service/TokenService.java
[Entity] ruoyi-system/src/main/java/org/dromara/system/domain/SysUser.java
[Mapper] ruoyi-system/src/main/java/org/dromara/system/mapper/SysUserMapper.java
[Mapper] ruoyi-system/src/main/java/org/dromara/system/mapper/SysRoleMapper.java
[Other] ruoyi-common/src/main/java/org/dromara/common/core/config/JacksonConfig.java
```
