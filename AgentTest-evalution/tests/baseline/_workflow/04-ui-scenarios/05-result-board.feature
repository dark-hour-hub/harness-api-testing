# 结果看板
# 业务需求来源: 模块 6（6.1 结果总览 6.2 明细下钻 6.3 报告查看；未就绪时明确提示）；无登录
# 页面路由: /results（ResultsView.vue —— ResultTaskFilter 智能体/任务筛选 + 结果面板）

Feature: 结果看板
  结果看板展示持久化评测结果；未选择智能体/任务时为空态提示

  Scenario: result board empty state
    Given 打开首页
    When 点击链接 "结果看板"
    And 等待 1 秒
    Then 页面应包含 "请先选择智能体查看评测报告"
    And 页面应包含 "结果内容只展示真实任务和后端持久化报告，不生成默认分数或模拟报告。"

  Scenario: result filters visible
    Given 打开首页
    When 点击链接 "结果看板"
    And 等待 1 秒
    Then 页面应包含 "智能体"
    And 页面应包含 "评测任务"
    And 页面应包含 "请选择智能体"
    And 页面应包含 "请选择评测任务"
