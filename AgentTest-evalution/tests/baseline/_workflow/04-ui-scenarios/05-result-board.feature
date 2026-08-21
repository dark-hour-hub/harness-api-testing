# 结果看板
# 业务需求: 模块 6（结果总览/明细/报告；未选择任务时空态）
# 页面: /results（ResultTaskFilter + 任务结果面板）

Feature: 结果看板
  结果看板展示持久化评测结果；未选择智能体/任务时为空态提示

  Scenario: result board empty state
    Given 打开首页
    When 点击链接 "结果看板"
    Then 页面应包含 "请先选择智能体查看评测报告"
    And 页面应包含 "结果内容只展示真实任务和后端持久化报告，不生成默认分数或模拟报告。"

  Scenario: result filters visible
    Given 打开首页
    When 点击链接 "结果看板"
    Then 页面应包含 "请选择智能体"
    And 页面应包含 "请选择评测任务"

  Scenario: navigate back to overview
    Given 打开首页
    When 点击链接 "结果看板"
    When 点击链接 "返回首页"
    Then 页面应包含 "快捷入口"
