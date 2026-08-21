# 指标配置
# 业务需求: 模块 2/3/4（指标目录浏览、测试用例管理、评测方案保存入口）
# 页面: /indicators（指标维度面板 + 测试用例表格 + 底部操作区）

Feature: 指标配置
  指标目录按维度展示并支持用例管理；未选指标操作给出前置校验提示

  Scenario: indicator page elements
    Given 打开首页
    When 点击链接 "指标配置"
    And 等待 1 秒
    Then 页面应包含 "指标大类"
    And 页面应包含 "评测用例"
    And 应看到按钮 "全选"
    And 应看到按钮 "全不选"
    And 应看到按钮 "保存为方案"
    And 应看到按钮 "开始评测"

  Scenario: ai expand shows unavailable message
    Given 打开首页
    When 点击链接 "指标配置"
    When 点击按钮 "AI扩充"
    Then 应看到提示 "当前后端暂未提供AI扩充接口。"

  Scenario: add test case opens form with pre-selected indicator
    # 页面初始化自动选中第一个启用的维度/指标（IndicatorsView.initializeIndicatorsPage），
    # 「未选择指标」校验在当前前端版本不会触发；点击后直接打开新增用例表单。
    # 注意：初始化为异步，点击过快会命中未初始化竞态（偶发只弹提示不弹表单），
    # 因此使用「点击新增用例并等待表单打开」组合步骤（内部自动重试）。
    Given 打开首页
    When 点击链接 "指标配置"
    When 点击新增用例并等待表单打开
    Then 应看到提示 "新增评测用例"
