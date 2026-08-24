-- 智能体评测平台 UI 测试清理模板（FK 逆序，只删运行期数据）
-- 判定约定：测试自建数据 code 前缀 AGT_UI_ / TC_UI_ / SCHEME_UI_ / TASK_UI_ / IND_UI_
DELETE FROM evaluation_report WHERE task_id IN (SELECT id FROM evaluation_task WHERE task_no LIKE 'TASK_UI_%');
DELETE FROM manual_review WHERE task_id IN (SELECT id FROM evaluation_task WHERE task_no LIKE 'TASK_UI_%');
DELETE FROM dimension_result WHERE task_id IN (SELECT id FROM evaluation_task WHERE task_no LIKE 'TASK_UI_%');
DELETE FROM category_result WHERE task_id IN (SELECT id FROM evaluation_task WHERE task_no LIKE 'TASK_UI_%');
DELETE FROM indicator_result WHERE task_id IN (SELECT id FROM evaluation_task WHERE task_no LIKE 'TASK_UI_%');
DELETE FROM ai_judge_record WHERE task_id IN (SELECT id FROM evaluation_task WHERE task_no LIKE 'TASK_UI_%');
DELETE FROM agent_call_record WHERE task_id IN (SELECT id FROM evaluation_task WHERE task_no LIKE 'TASK_UI_%');
DELETE FROM test_case_result WHERE task_id IN (SELECT id FROM evaluation_task WHERE task_no LIKE 'TASK_UI_%');
DELETE FROM indicator_measurement WHERE task_id IN (SELECT id FROM evaluation_task WHERE task_no LIKE 'TASK_UI_%');
DELETE FROM evaluation_task_case WHERE task_id IN (SELECT id FROM evaluation_task WHERE task_no LIKE 'TASK_UI_%');
DELETE FROM evaluation_task WHERE task_no LIKE 'TASK_UI_%';
DELETE FROM scheme_test_case WHERE scheme_id IN (SELECT id FROM evaluation_scheme WHERE scheme_code LIKE 'SCHEME_UI_%');
DELETE FROM scheme_indicator WHERE scheme_id IN (SELECT id FROM evaluation_scheme WHERE scheme_code LIKE 'SCHEME_UI_%');
DELETE FROM scheme_category WHERE scheme_id IN (SELECT id FROM evaluation_scheme WHERE scheme_code LIKE 'SCHEME_UI_%');
DELETE FROM evaluation_scheme WHERE scheme_code LIKE 'SCHEME_UI_%';
DELETE FROM test_case_judge_rule WHERE test_case_id IN (SELECT id FROM test_case WHERE case_code LIKE 'TC_UI_%');
DELETE FROM test_case WHERE case_code LIKE 'TC_UI_%';
DELETE FROM indicator_iso_mapping WHERE indicator_id IN (SELECT id FROM indicator_definition WHERE indicator_code LIKE 'IND_UI_%');
DELETE FROM indicator_definition WHERE indicator_code LIKE 'IND_UI_%';
DELETE FROM agent_config WHERE agent_code LIKE 'AGT_UI_%';
