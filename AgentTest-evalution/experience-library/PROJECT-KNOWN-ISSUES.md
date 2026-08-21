# 项目级测试经验库（Project Known-Issues）

> **项目**：agent-evaluation-platform（智能体评测平台，`harness-testing/baseline`）
> **用途**：本项目后续所有测试（API/UI/Perf）必须避免的**项目特有**坑。
> **维护**：由 `post-run-analysis` skill 在用户确认后回写。

---

## 一、后端行为事实（被测系统，测试须遵循）

### 1. 方案（evaluation_scheme）约束链
- 唯一约束：`uk_scheme_code_version (scheme_code, version)`（schema.sql:213）；**ARCHIVED 方案不可删**（无删除 API）→ 重跑前必须清理残留，否则 409。
- 状态机：DRAFT → PUBLISHED → ARCHIVED；`updateDraft` 仅允许 DRAFT，否则 `SCHEME_409_STATUS`。
- 校验规则（`SchemeValidator.java`）：
  - `CATALOG_REQUIRED`：目录必选/含 veto 的指标及其所在分类，在方案中必须 `required:true`、`applicable:true`。
  - `DIMENSION_COVERAGE`：COMPREHENSIVE 必须覆盖全部维度（选中指标的维度并集 ⊇ 全部维度）。
  - `DIMENSION_KEYS`：`dimensionWeights.weights` 的键必须与所选维度代码**完全一致**。
  - **weightOverride 同分类和 =1**：`indicators[i].weightOverride` 按(维度/分类)分组后每组之和必须=1（SchemeValidator.java:445-452）。**ad-hoc 每分类只选 1 个指标时，任何 override≠1 即 400** → 全用默认权重即可，不传 override。
- **错误包装**：tasks 控制器未注册 `SchemeValidationException` handler → ad-hoc 校验失败时 `data:null`（错误详情丢失），只能按此认知排查。
- **validate 接口**：200 响应 `data` **只有 `errors` 数组，没有 `valid` 字段**。

### 2. 目录与 ID
- V1：3 维（SAFETY/CAPABILITY/EVOLUTION）、12 分类、30 指标（指标 id 从 1 起，如 1）。
- V2：4 维（SAFETY_COMPLIANCE/CAPABILITY/INTENT_UNDERSTANDING/USER_EXPERIENCE，维度 id 101-104）、17 分类（101-117）、59 指标（1001 起）。
- **分类 id ≠ 指标 id**：101 是 V2 分类 id；V2 指标示例 1001（分类101）/1011（分类105）/1031（分类110）/1048（分类114）。
- **已验证方案配方（publish 200）**：catalogVersion `V2` + evaluationMode `COMPREHENSIVE` + riskTier `B` +
  weights{SAFETY_COMPLIANCE:0.4, CAPABILITY:0.25, INTENT_UNDERSTANDING:0.2, USER_EXPERIENCE:0.15} +
  categories[101,105,110,114](required+applicable) + indicators[1001,1011,1031,1048](required+applicable) + testCases[1,71,181,341]。

### 3. 任务（evaluation_task）
- 创建任务要求引用的方案 **PUBLISHED**（否则 `TASK_409_SCHEME_STATUS`）；ARCHIVED 也不可作 `sourceSchemeId`。
- ad-hoc（POST /evaluation-tasks/ad-hoc）：`indicators` 建议不带 weightOverride（见 1）；`testCaseIds` 要与指标匹配。
- 指标测量（POST /evaluation-tasks/{id}/measurements）：
  - `measurementType` 必须 = 指标 `collectionMethod`（V2 指标全部 `AUTO_API`）。
  - `unit` 必须与指标一致。
  - `periodStart/End` 是 **LocalDateTime，不能带时区偏移**（`+08:00` → 500）。

### 4. 测试用例（test_case）
- import（POST /test-cases/import）**必须带 `referenceAnswer`**，否则 400。
- `CONTAINS` 判定规则必须 `ruleConfig.keywords`（非空字符串数组），可选 `matchMode` ∈ {ALL, ANY}（不是 `keyword`）。
- 用例版本号：接口 import 用 `1.0` 类格式。

### 5. 智能体（agent_config）
- 基准 agent **id=1（AGT.code=CHAT，enabled=1）** 是种子，**不可被测试禁用/删除**（曾因 UI delete 场景被置 enabled=0，连锁搞挂所有依赖 agent 1 的任务创建类用例）。
- GENERIC_HTTP_JSON 适配器**必须配置 answerField**，且创建需完整字段（category/agentType/version/...）。

---

## 二、UI 事实

### 6. 表单/文案
- 用例表单标题真实文案：创建 =「**新增评测用例**」（不是"新增测试用例"）；编辑 =「编辑评测用例」。
- 新增/编辑/删除 toast：智能体已新增 / 智能体已更新 / 智能体删除请求已处理。
- AgentFormDialog 原生 `<select>` 无 aria-label，需按 data-testid：`agent-risk-tier` / `agent-adapter-type` / `agent-method`。
- 种子 agent"问答1"编辑会被前端校验拦截（`headerSecretConfigured=true` 必须重填密钥引用）→ **不要对种子卡片做编辑**。

### 7. 指标页（/indicators）
- 页面初始化自动预选首个启用维度/指标（`initializeIndicatorsPage` → `handleSelectDimension`），因此旧"未选指标→警告"断言在当前版本不可达（点击太快才偶发命中初始化竞态）。
- 点击「新增用例」后应断言打开表单（`#test-case-form-title` 可见）；要容忍初始化竞态 → 用"重试直至表单打开"组合步骤。

### 8. UI 套件重跑
- create 场景使用固定 agentCode `AGT_UI_DEMO` → 二次跑需先清库/删除。
- 破坏性场景（edit/delete）必须用 `在智能体卡片 "{code}" 中点击 "{btn}"` 定向到自建数据。

---

## 三、Perf 事实

### 9. 基准资源（压测运行期依赖，勿删）
- `PERF_SCHEME_BASE`（PUBLISHED，任务创建用，当前 id=17）
- `PERF_SCHEME_DRAFT_BASE`（DRAFT，validate 场景用，当前 id=48049；id 会变，用脚本按 code 查）
- 重建脚本：`C:\Users\17201\AppData\Local\Temp\opencode\perf_setup.py`（幂等：存在则复用）。

### 10. 压测数据污染
- 写场景会分钟级写入数十万行（agent/testcase/scheme/task）→ 列表类基线失真（PERF_TESTCASE_001 从 p95 327ms → 46s）。
- **性能报告须含库内数据规模**；写场景后必须清理（`clean_perf.py`）再跑读场景。
- 清理后保持：agent=1、scheme=基准、task=种子(1,3,5,8,11)、case=seed。

---

## 四、执行前检查清单（避免重复踩坑）

- [ ] 已清理上次运行残留（方案/用例/任务），种子与基准资源就位
- [ ] agent id=1 enabled=1；无 AGT_UI_DEMO 残留（UI 重跑时）
- [ ] 基准方案（PUBLISHED + DRAFT）存在（Perf）
- [ ] 方案 body 用「已验证配方」；ad-hoc 不传 weightOverride
- [ ] 测量接口：AUTO_API + unit 一致 + period 无时区
- [ ] import 带 referenceAnswer；CONTAINS 用 keywords 数组
- [ ] UI 断言文案用真实文本（新增评测用例）；下拉用 data-testid；破坏性操作卡片定向
- [ ] Perf：唯一编码用 `__RandomString(12,A-Z0-9)`；先读后写；压测后清库

---

## 维护记录

| 日期 | 来源 | 新增条目 |
|------|------|---------|
| 2026-08-20 | 全量三线回归（API 96/0、UI 15/0、Perf 15/4） | 1~10 |
