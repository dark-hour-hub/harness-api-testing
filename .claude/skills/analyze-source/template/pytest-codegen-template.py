# pytest 代码生成模板
# 从 YAML 测试用例生成 pytest 测试代码的参考实现

import yaml


def generate_pytest_from_yaml(yaml_path, output_path):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("import pytest\\n")
        f.write("import requests\\n\\n")

        for tc in data['testcases']:
            # 生成测试函数
            f.write(f"def test_{tc['id'].lower()}():\\n")
            f.write(f"    '''{tc['title']}'''\\n")
            f.write(f"    # Scenario: {tc['scenario'].strip()}\\n\\n")

            # 生成请求代码
            f.write(f"    url = '{tc['request']['path']}'\\n")
            f.write(f"    headers = {tc['request']['headers']}\\n")
            if tc['request'].get('params'):
                f.write(f"    params = {tc['request']['params']}\\n")
            if tc['request'].get('body'):
                f.write(f"    json = {tc['request']['body']}\\n")

            # 生成断言代码
            for assertion in tc['assertions']:
                f.write(f"    # {assertion['description']}\\n")
                # 转换断言表达式为Python代码
                ...