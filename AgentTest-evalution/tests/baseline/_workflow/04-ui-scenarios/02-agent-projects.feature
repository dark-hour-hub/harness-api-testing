# 评测项目（Agent 配置）
# 业务需求来源: 模块 1（1.1 列表/筛选 1.2 创建 1.3 查看/编辑 1.4 删除）；无登录
# 页面路由: /projects（ProjectsView.vue —— AgentCard 列表 + AgentFormDialog + DeleteConfirmDialog）
# 注意: 创建类数据使用「时间戳后缀」唯一标识；重复执行同一后缀会与历史数据冲突（后运行场景依赖先运行场景创建的数据）

Feature: 评测项目
  管理真实智能体配置：列表浏览、编码筛选、新增与创建校验（无登录）

  Scenario: list and view agent cards
    Given 打开首页
    When 点击链接 "评测项目"
    And 等待 1 秒
    Then 页面应包含 "评测对象"
    And 应看到按钮 "新增智能体"
    And 应看到按钮 "筛选"
    And 应看到按钮 "选择评测"
    And 应看到按钮 "详情"
    And 应看到按钮 "编辑"
    And 应看到按钮 "删除"

  @smoke
  Scenario: filter agents by code
    Given 打开首页
    When 点击链接 "评测项目"
    When 在 "智能体编码筛选" 输入框中输入 "AGT"
    And 点击按钮 "筛选"
    Then 应看到按钮 "新增智能体"
    And 应看到按钮 "筛选"

  Scenario: create agent
    Given 打开首页
    When 点击链接 "评测项目"
    When 点击按钮 "新增智能体"
    And 在 "智能体编码" 输入框中输入 "AGT_UI_20260824_1430"
    And 在 "请输入智能体名称" 输入框中输入 "UI测试智能体_1430"
    And 在 "例如：CUSTOMER_SERVICE" 输入框中输入 "TEST"
    And 选择下拉框 "风险等级" 的选项 "较低风险等级 D（D）"
    And 在 "请输入所属部门" 输入框中输入 "测试部"
    And 在 "例如：1.0.0" 输入框中输入 "1.0.0"
    And 在 "例如：CHAT" 输入框中输入 "CHAT"
    And 选择下拉框 "适配器类型" 的选项 "通用 HTTP JSON（GENERIC_HTTP_JSON）"
    And 选择下拉框 "HTTP 方法" 的选项 "POST"
    And 在 "https://host/path" 输入框中输入 "http://localhost:8080/mock"
    And 在 "100 - 120000" 输入框中输入 "60000"
    And 在 "$.answer" 输入框中输入 "$.answer"
    And 点击按钮 "保存"
    Then 应看到提示 "智能体已新增"
    And 页面应包含 "AGT_UI_20260824_1430"

  Scenario: create agent missing required fields
    Given 打开首页
    When 点击链接 "评测项目"
    When 点击按钮 "新增智能体"
    And 在 "智能体编码" 输入框中输入 "AGT_UI_20260824_1500"
    And 在 "请输入智能体名称" 输入框中输入 "UI测试智能体_1500"
    And 点击按钮 "保存"
    Then 应看到提示 "请填写所有必填字段"
