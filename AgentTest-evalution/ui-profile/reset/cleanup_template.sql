-- 智能体评测平台 UI 测试清理模板（FK 逆序，只删运行期数据）
-- 判定约定：测试自建数据 code 前缀 AGT_UI_ / TC_UI_ / SCHEME_UI_ / TASK_UI_ / IND_UI_
DELETE FROM evaluation_task_result WHERE task_id IN (SELECT id FROM evaluation_task WHERE code LIKE 'TASK_UI_%');
DELETE FROM evaluation_task WHERE code LIKE 'TASK_UI_%';
DELETE FROM evaluation_scheme WHERE scheme_code LIKE 'SCHEME_UI_%';
DELETE FROM test_case WHERE code LIKE 'TC_UI_%';
DELETE FROM agent WHERE code LIKE 'AGT_UI_%';
DELETE FROM indicator WHERE code LIKE 'IND_UI_%';
