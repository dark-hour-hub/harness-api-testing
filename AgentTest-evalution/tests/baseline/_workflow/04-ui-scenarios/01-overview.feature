# 总览
# 业务需求来源: 模块 7（总览导航与快捷入口，7.1 平台数据入口 / 7.2 导航跳转）；无登录
# 页面路由: /overview（OverviewView.vue —— PageHeader 标题、五步导航 StepNavigation、统计卡、快捷入口、摘要卡片）

Feature: 总览
  总览页展示平台导航、统计卡与快捷入口，支持一键跳转各业务页面

  Scenario: overview navigation elements
    Given 打开首页
    Then 页面应包含 "浙商银行智能体评测平台"
    And 页面应包含 "总览"
    And 页面应包含 "评测项目"
    And 页面应包含 "指标配置"
    And 页面应包含 "评测执行"
    And 页面应包含 "结果看板"
    And 页面应包含 "快捷入口"
    And 页面应包含 "已配置智能体"

  Scenario: navigate to agent projects via quick action
    Given 打开首页
    When 点击链接 "管理智能体"
    Then 页面应包含 "评测对象"
    And 应看到按钮 "新增智能体"
