# 指标配置
# 业务需求来源: 模块 2（2.1 指标维度浏览 2.2 分类浏览 2.3 指标列表 2.4 详情 2.5 目录版本）；无登录
# 页面路由: /indicators（IndicatorsView.vue —— IndicatorDimensionPanel 维度卡片 + IndicatorCategoryPanel 指标大类 + 测试用例区）

Feature: 指标配置
  指标目录按维度展示并支持用例管理；未就绪功能给出后端暂未提供提示

  @smoke
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

  Scenario: indicator dimension default weight shown
    Given 打开首页
    When 点击链接 "指标配置"
    And 等待 1 秒
    Then 页面应包含 "风险默认权重"

  Scenario: ai expand shows unavailable message
    Given 打开首页
    When 点击链接 "指标配置"
    When 点击按钮 "AI扩充"
    Then 应看到提示 "当前后端暂未提供AI扩充接口。"
