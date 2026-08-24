# UI 测试链路重构设计（配置驱动 + 元素地图 + 迭代适应闭环）

> 日期：2026-08-24
> 状态：已与用户逐节确认
> 范围：AgentTest-evalution（harness）的 UI 测试链路（ui-scenario-design / feature-to-playwright / ui-runner / post-run-analysis 及相关脚本）

---

## 一、背景与现状痛点

现有 UI 测试链路：业务需求 → Gherkin 场景 → 模板生成 pytest-bdd 脚本 → Playwright 执行 → 截图 HTML 报告。经梳理存在以下问题：

1. **可移植性差**：conftest 模板硬编码本项目内容（`agent-risk-tier` 等 testid 映射、`.agent-card` 定位、`#test-case-form-title`、中文"用户名/密码"文案）——换被测系统必须改模板，但铁律又禁止改 conftest，自相矛盾。
2. **定位脆弱**：全依赖可见文本/placeholder 直搜；前端改文案即全链路失败，失败信息只有"找不到按钮"。
3. **无智能等待**：`等待 N 秒` 固定 sleep + `networkidle`（SPA 长轮询下不可靠）。
4. **写场景不自愈**：唯一约束冲突（如 agentCode）、种子数据被误操作，只靠流程纪律约束（企业经验库第 10/11 条）。
5. **串行执行慢**、生成产物路径硬编码（`test_*.py` 内写死绝对 FEATURE_DIR）。

## 二、目标与约束（已确认）

| 约束 | 结论 |
|------|------|
| 目标 | 稳定性、维护成本、覆盖面、执行效率、可移植性 五项全要 |
| 使用方式 | 同一 harness 工程被不同项目拉取绑定，测该项目及其后续迭代版本 → **内核 100% 通用，项目差异全进配置层** |
| 技术栈 | 会变（不固定 Element Plus）→ 定位策略不能绑死 EP |
| 数据环境 | 独立测试环境可重置，但无现成脚本 → **harness 提供清理模板，人工确认后执行** |
| AI 角色 | 只做设计/分析，**执行层保持确定性**（不做 AI 自动改定位+重跑） |
| 人工角色 | **人只做"确认闸门"，不做"生产"**——所有草稿（地图/场景/清理模板/修复建议）由 AI 生产，人工只确认 |

## 三、总体架构

```
AIHarness-wu/  (harness 内核 —— 拉取后按项目绑定)
├── .opencode/skills/
│   ├── ui-scenario-design      改造：场景设计时同步产出元素地图
│   ├── ui-element-map          (新) 读前端源码自动生成 elements.yaml
│   ├── feature-to-playwright   改造：DSL 步骤经元素地图解析
│   ├── ui-runner               改造：重置钩子 + 并行 + 报告升级
│   └── post-run-analysis       扩展：定位失败 → 输出地图修改建议(人工确认)
│
├── ui-profile-template/        (新) 项目绑定层模板 —— 所有项目差异的唯一边界
│   ├── elements.yaml           元素地图
│   ├── business.yaml           下拉框/账号/种子保护清单/busy 指示器/超时体系
│   ├── reset/
│   │   ├── cleanup_template.sql  清表模板（FK 逆序 + 只删运行期数据）
│   │   └── seed/                 种子数据恢复脚本
│   └── scenarios/              业务需求 + .feature 场景
│
└── tests/<project>/            运行产物（分析/生成/报告，结构现状不变）
```

**分工铁律**：harness 内核不含任何项目特有内容；新项目绑定 = 生成一份 `ui-profile/`（AI 草稿 + 人工确认，见第五节）；前端文案/结构/技术栈变化只动 profile，不动内核。

## 四、元素地图（吸收 page object 思想）

`elements.yaml`：逻辑名/文案 → 定位策略链（按序尝试，命中即止，确定性）：

```yaml
elements:
  agentCodeInput:
    strategies:
      - { type: data-testid, value: agent-code-input }
      - { type: placeholder, value: 例如：BANK_AGENT }
      - { type: role, role: textbox, name: 智能体编码 }
  riskTierSelect:
    strategies:
      - { type: data-testid, value: agent-risk-tier }
      - { type: combobox, name: 风险等级 }
  saveButton:
    strategies:
      - { type: role, role: button, name: 保存 }
      - { type: text, value: 保存 }
busy_indicators: [".el-loading-mask", ".loading"]
protected_seeds: ["BANK_AGENT", "AGT_SEED_*"]
```

关键机制：

1. 策略链按序尝试、命中即止——确定性执行，不依赖 AI 猜测。
2. **场景文件保持业务语言**（`在"智能体编码"输入框中输入`），DSL 步骤先查元素地图（文案即 key）→ 命中用策略链；**未命中回退现有文本直搜**——老场景零改动平滑过渡。
3. 前端改文案/加 testid → 只改地图一处；技术栈变 → 只换地图生成器适配。
4. 地图由 `ui-element-map` skill 从前端源码生成草稿（placeholder/testid/文案），人工确认入库；运行期**地图命中率统计**进报告（标注靠第几级策略命中、哪些长期文本直搜的脆弱点）。

## 五、人工参与模型（确认闸门，不做生产）

| 环节 | 人工角色 | 频率 |
|------|---------|------|
| 项目绑定（生成 ui-profile/） | 批量确认 AI 草稿 | 每项目一次（可渐进：首跑≈0 成本，地图从运行中"长"出来） |
| 跑前重置 | 确认闸门（可配置自动跳过） | 每次跑前 |
| AI 场景/地图草案 | 评审确认 | 需求变更时 |
| 前端发版 → 迭代适应 | 批量确认 AI 修复草案 | 发版时（多数情况零人工，见第六节） |
| 失败复盘/经验回写 | 确认闸门 | 有失败时 |

项目绑定输入仅依赖已有的 `config.yaml`（源码路径/地址/账号）：
- 元素地图草稿 ← 前端源码扫描
- 清理模板草稿 ← 后端 schema.sql / 实体类 / DB 元数据（表清单、FK 逆序、运行期数据判定列）
- 种子清单草稿 ← 经验库（PROJECT-KNOWN-ISSUES 已有配方）+ DB 现有数据识别

## 六、同项目多版本迭代的适应闭环（三道防线）

**防线 1 · 策略链回退（零人工）**：前端改文案但 data-testid 仍在 → 自动切到第 1 级策略，测试照跑，报告黄色预警"命中降级"。

**防线 2 · 定位探针 + AI 草案 + 批量确认**：版本指纹（前端 commit hash / 构建时间，记录在 profile）变化 → 自动跑**只读探针**（打开各页面验证元素地图命中）→ 产出《地图健康报告》→ AI 读新源码生成地图更新草案 → 人工批量确认 → 更新 profile → 重跑探针验证 → 才跑全量。

**防线 3 · profile 分版本（仅大重构）**：UI 大改版（Vue2→Vue3、整体重构）时 `ui-profile/versions/v2/` 分叉；与 v1 相同的场景共享，仅差异场景分叉；默认不 fork，探针健康度持续差才启动。

配套：**触发条件是"探针报告有失效元素"，不是"发版了"**；命中率报告反推前端规范（哪些元素加 testid 收益最大）。

## 七、DSL 扩展与场景分层

新增通用步骤（全部走元素地图解析）：

| 步骤 | 解决 |
|------|------|
| `在表格行包含 "X" 中点击 "编辑"` | 通用化行作用域（取代硬编码卡片专属步骤） |
| `在对话框 "标题" 中点击 "保存"` | 弹窗内定位隔离 |
| `上传文件到 "导入" 文件 "data/x.json"` | 上传交互 |
| `在 "开始日期" 选择日期 "2026-08-01"` | 日期选择器 |
| `${rand:8}` / `${uuid}` / `${date:+1d}` | 场景内联动态值，解决唯一约束 |
| `元素 "x" 应不可见` / 行存在性断言 | 补反向断言 |

场景分层：`@smoke` / `@P0` / `@P1` tag，runner 按 tag 裁剪（发版后 smoke 快速反馈，夜间全量）。

## 八、等待与稳定性（确定性执行层）

按可靠性递增三级替换 `等待 N 秒` / `networkidle`：

1. Playwright 原生 actionability 自动等待（保持）。
2. **busy 指示器同步**：business.yaml 声明 `busy_indicators`，操作步骤后自动等 busy 消失（替代固定 sleep）。
3. **API 级同步**：操作后 `page.wait_for_response` 等页面发出的后端请求返回（如保存后等 `POST /api/agents` 200）。请求路径**来自已有 API 文档链路（03-api-docs）**，零新增人工输入——UI 测试与接口文档链路的集成点。

纪律：定位类失败确定性重试 1 次（可配置，非 AI 重跑）；失败截图前先等 busy 消失；超时体系统一收进 business.yaml（操作 5s / busy 15s / 断言 10s / API 同步 15s）。

## 九、数据闭环

```
跑前 pre-run（ui-runner 集成 reset 适配器）
  1. 版本指纹比对 → 变化先跑探针
  2. 重置确认门：展示清理计划（表、删除范围）→ 人工确认 / 配置自动跳过
  3. 执行 cleanup_template.sql（FK 逆序清表，只删运行期数据，保留种子）
  4. 恢复种子 seed/
跑中：动态值自建数据；protected_seeds 命中 → DSL 报错拦截（种子保护硬约束化）
跑后：报告 + 可选清理（默认不清理，下次跑前重置）
```

## 十、并行与效率

- 逐 feature 独立进程并行（保留隔离设计），进程数可配置（默认 2~4，规避 Windows 端口耗尽——企业经验库第 9 条）
- session 级登录态复用（保留现状）
- 分层执行：smoke 快速 → 全量夜间
- 报告聚合复用现有 run_ui.py 的 JUnit 解析逻辑

## 十一、迁移路径（增量演进，不推倒重来）

| 阶段 | 内容 | 交付后状态 |
|------|------|-----------|
| 1 地基 | ui-profile-template/ 骨架 + conftest 元素地图解析器（未命中回退文本直搜） | 现有场景零改动可跑 |
| 2 生成器 | ui-element-map skill + ui-scenario-design 同步产地图 | 新项目绑定自动化 |
| 3 数据闭环 | reset 适配器 + 清理模板 + 种子保护拦截 + 动态值 DSL | 消除数据 flaky |
| 4 稳定性 | busy 同步 + API 级同步 + 确定性重试 + 并行 + tag 分层 | 稳定与提速 |
| 5 迭代闭环 | 版本指纹 + 探针 + AI 修复草案 + 批量确认 + 命中率报告 | 前端改动零/低人工 |

每阶段独立可用、可回滚；阶段 1 完成后现有测试不受影响。

## 十二、明确不做（YAGNI）

- 不做 AI 自动改定位+自动重跑（违反执行层确定性约束）
- 不做全 AI 生成场景（保持 Gherkin 业务语言可读性）
- 不替换 pytest-bdd/Playwright 框架底座（Robot Framework / Playwright 原生 runner 方案已评估，吸收 page object 思想即可）
- 场景不强制用逻辑名（文案即 key + 回退，兼顾非工程师可写）
- profile 分版本仅在大重构时启用（默认单 profile 自适应）