# 评测执行（测试用例管理 + 评测方案管理 + 评测任务）
# 业务需求来源: 模块 3（测试用例管理）、模块 4（评测方案管理）、模块 5（评测任务/执行进度）；无登录
# 页面路由: 测试用例与方案在 /indicators（IndicatorsView.vue 内 TestCaseFormDialog/SchemeSaveDialog）；
#           评测任务与进度在 /execution（ExecutionView.vue + ExecutionProgressPanel）

Feature: 评测执行
  覆盖测试用例新增、评测方案草稿校验与评测任务执行进度；未选择任务时为空态提示

  Scenario: add test case opens form with pre-selected indicator（新增用例表单预选指标）
    # 页面初始化自动选中第一个启用的维度/指标（IndicatorsView.initializeIndicatorsPage），
    # 点击过快会命中未初始化竞态（偶发只弹提示不弹表单），因此使用「点击新增用例并等待表单打开」组合步骤（内部自动重试）。
    Given 打开首页
    When 点击链接 "指标配置"
    When 点击新增用例并等待表单打开
    Then 应看到提示 "新增评测用例"

  Scenario: save scheme dialog validates required fields（方案保存必填校验）
    Given 打开首页
    When 点击链接 "指标配置"
    When 点击按钮 "保存为方案"
    Then 应看到提示 "方案基本信息"
    And 应看到按钮 "保存为草稿"
    And 应看到按钮 "保存并发布"
    When 点击按钮 "保存为草稿"
    Then 应看到提示 "请填写所有必填字段"

  Scenario: execution empty state（执行空态）
    Given 打开首页
    When 点击链接 "评测执行"
    And 等待 1 秒
    Then 页面应包含 "当前未选择评测任务"
    And 页面应包含 "任务状态记录"
    And 应看到按钮 "请从指标配置页启动"

  Scenario: reset shows unavailable message（重置不可用提示）
    Given 打开首页
    When 点击链接 "评测执行"
    When 点击按钮 "重置"
    Then 应看到提示 "当前后端暂未提供此操作"
