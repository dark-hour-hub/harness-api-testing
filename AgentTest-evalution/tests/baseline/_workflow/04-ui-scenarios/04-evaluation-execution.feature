# 评测执行
# 业务需求: 模块 5（任务详情与执行进度；无 taskId 时为空态）
# 页面: /execution（当前任务卡 + 执行进度面板）

Feature: 评测执行
  评测执行页展示任务详情与执行进度；未选择任务时为空态提示

  Scenario: execution empty state
    Given 打开首页
    When 点击链接 "评测执行"
    Then 页面应包含 "当前未选择评测任务"
    And 页面应包含 "任务状态记录"
    And 应看到按钮 "请从指标配置页启动"

  Scenario: reset shows unavailable message
    Given 打开首页
    When 点击链接 "评测执行"
    When 点击按钮 "重置"
    Then 应看到提示 "当前后端暂未提供此操作"
