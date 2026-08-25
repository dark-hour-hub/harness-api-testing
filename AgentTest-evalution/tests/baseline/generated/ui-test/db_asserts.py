# -*- coding: utf-8 -*-
# 由 feature-to-playwright skill 自动生成，请勿手动修改
# DB 断言编译产物：来自 00-requirements/db-asserts.yaml + 后端 schema.sql 校验
DB_ASSERT_MAP = {
    'AGENT_CREATE_001': {'id': 'AGENT_CREATE_001', 'table': 'agent_config', 'expect_records': 1, 'sql': 'SELECT agent_name, enabled FROM agent_config WHERE agent_code = %(p0)s', 'params': [{'key': 'p0', 'mode': 'var', 'ref': '$code', 'value': None}], 'asserts': [{'field': 'agent_name', 'mode': 'var', 'ref': '$name', 'value': None}, {'field': 'enabled', 'mode': 'literal', 'ref': None, 'value': 1}], 'schema_ref': 'schema.sql#agent_config'},
    'AGENT_CREATE_VALIDATION_001': {'id': 'AGENT_CREATE_VALIDATION_001', 'table': 'agent_config', 'expect_records': 0, 'sql': 'SELECT 1 FROM agent_config WHERE agent_code = %(p0)s', 'params': [{'key': 'p0', 'mode': 'var', 'ref': '$code', 'value': None}], 'asserts': [], 'schema_ref': 'schema.sql#agent_config'},
    'AGENT_DELETE_001': {'id': 'AGENT_DELETE_001', 'table': 'agent_config', 'expect_records': 0, 'sql': 'SELECT 1 FROM agent_config WHERE agent_code = %(p0)s', 'params': [{'key': 'p0', 'mode': 'var', 'ref': '$code', 'value': None}], 'asserts': [], 'schema_ref': 'schema.sql#agent_config'},
    'AGENT_EDIT_001': {'id': 'AGENT_EDIT_001', 'table': 'agent_config', 'expect_records': 1, 'sql': 'SELECT agent_name FROM agent_config WHERE agent_code = %(p0)s', 'params': [{'key': 'p0', 'mode': 'var', 'ref': '$code', 'value': None}], 'asserts': [{'field': 'agent_name', 'mode': 'var', 'ref': '$name2', 'value': None}], 'schema_ref': 'schema.sql#agent_config'},
}
