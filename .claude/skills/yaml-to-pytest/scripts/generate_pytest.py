#!/usr/bin/env python3
"""
YAML -> Pytest 脚本生成器

从 YAML 测试用例目录读取 YAML 测试用例，生成 pytest 脚本。

支持两种模式:
  --mode baseline  → 全量模式（默认）
  --mode diff      → 增量模式

也可显式指定 --yaml-dir 和 --output-dir（优先级高于 --mode）。

用法:
  python generate_pytest.py --mode baseline
  python generate_pytest.py --mode diff
  python generate_pytest.py --yaml-dir <dir> --output-dir <dir>
"""

import sys
import argparse
import shutil
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML 未安装，请执行: pip install pyyaml")
    sys.exit(2)


# ═══════════════════════════════════════════════════════════════
# 常量
# ═══════════════════════════════════════════════════════════════

SKIP_CONTENT_TYPES = {"multipart/form-data"}

# 脚本所在目录 → 向上 4 级到项目根
_PROJECT_ROOT = Path(__file__).resolve().parents[4]
_TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "template"

# 模式 → 默认路径映射
MODE_PATHS = {
    "baseline": {
        "yaml_dir": "tests/baseline/_workflow/04-testcases",
        "output_dir": "tests/baseline/generated/api-test",
        "yaml_rel_path": "_workflow/04-testcases",
    },
    "diff": {
        "yaml_dir": "tests/diff/_workflow/02-diff-testcases",
        "output_dir": "tests/diff/generated/api-test",
        "yaml_rel_path": "_workflow/02-diff-testcases",
    },
}

TEST_FILE_TEMPLATE = '''\
"""
test_{module}.py --- 由 yaml-to-pytest skill 自动生成，请勿手动修改

数据来源: {yaml_filename}
模块: {module_name}
"""
import pytest
import yaml
from pathlib import Path

# --- 加载 YAML 数据（修改 YAML 后重新运行 pytest 即可生效，无需重新生成本文件）---
_YAML_DIR = Path(__file__).resolve().parents[2] / "{yaml_rel_path}"
_YAML_FILE = _YAML_DIR / "{yaml_filename}"
with open(_YAML_FILE, "r", encoding="utf-8") as _f:
    MODULE_DATA = yaml.safe_load(_f)


def _get_case(case_id):
    """按 ID 从 YAML 数据中获取用例"""
    for tc in MODULE_DATA.get("testcases", []):
        if tc.get("id") == case_id:
            return tc
    raise ValueError(f"用例 {{case_id}} 不存在于 {{_YAML_FILE.name}}")


@pytest.fixture(scope="session")
def module_data():
    """覆盖 conftest.py 中的 module_data fixture"""
    return MODULE_DATA


@pytest.fixture(scope="session")
def yaml_dir():
    """覆盖 conftest.py 中的 yaml_dir fixture"""
    return _YAML_DIR


# ═══════════════════════════════════════════════════════════════
# 测试用例
# ═══════════════════════════════════════════════════════════════

{test_functions}
'''

TEST_FUNC_TEMPLATE = '''\
{order_mark}{skip_mark}def test_{case_id}(module_context, request_helper):
    """{title}"""
    case = _get_case("{case_id}")
    resp, data = request_helper.execute(case)
    request_helper.store_extracts("{case_id}", case, data)
'''


# ═══════════════════════════════════════════════════════════════
# 生成逻辑
# ═══════════════════════════════════════════════════════════════

def _is_multipart(case):
    """检查用例是否使用 multipart/form-data"""
    for h in case.get("request", {}).get("headers", []):
        if isinstance(h, dict):
            ct = h.get("value", "").lower()
            if any(skip in ct for skip in SKIP_CONTENT_TYPES):
                return True
    return False


def _compute_order_indices(testcases):
    """为测试用例分配执行顺序索引，依赖用例自动排到被依赖用例之后"""
    order_map = {}
    for i, tc in enumerate(testcases):
        order_map[tc["id"]] = float(i + 1)

    changed = True
    while changed:
        changed = False
        for tc in testcases:
            for dep_id in tc.get("depends_on", []):
                if dep_id in order_map:
                    needed = order_map[dep_id] + 0.5
                    if order_map[tc["id"]] <= needed:
                        order_map[tc["id"]] = needed + 0.1
                        changed = True

    sorted_ids = sorted(order_map, key=order_map.get)
    return {case_id: idx + 1 for idx, case_id in enumerate(sorted_ids)}


def _generate_test_function(case, order_idx):
    """为单个测试用例生成测试函数代码"""
    case_id = case["id"]
    title = case.get("title", "").replace('"', '\\"')
    skip = _is_multipart(case)

    if skip:
        order_mark = ''
        skip_mark = '@pytest.mark.skip(reason="multipart/form-data 上传用例暂不支持")\n'
    else:
        order_mark = f'@pytest.mark.order({order_idx})\n'
        skip_mark = ''

    return TEST_FUNC_TEMPLATE.format(
        case_id=case_id,
        title=title,
        order_mark=order_mark,
        skip_mark=skip_mark,
    ).strip() + "\n"


def generate_conftest(output_dir):
    """从模板复制 conftest.py 到输出目录"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    src = _TEMPLATE_DIR / "conftest.py"
    dst = output_dir / "conftest.py"
    shutil.copy2(src, dst)
    return dst


def generate_test_file(yaml_path, output_dir, yaml_rel_path):
    """从单个 YAML 文件生成 test_{module}.py"""
    yaml_path = Path(yaml_path)
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    module = data.get("module", yaml_path.stem)
    module_name = data.get("module_name", module)
    testcases = data.get("testcases", [])

    if not testcases:
        print(f"  SKIP: {yaml_path.name} --- 无测试用例")
        return None

    order_map = _compute_order_indices(testcases)

    funcs = []
    skipped_count = 0
    for tc in testcases:
        case_id = tc.get("id")
        if not case_id:
            print(f"  WARN: {yaml_path.name} --- 存在缺少 id 的用例，已跳过")
            continue
        func_code = _generate_test_function(tc, order_map.get(case_id, 0))
        if "pytest.mark.skip" in func_code:
            skipped_count += 1
        funcs.append(func_code)

    content = TEST_FILE_TEMPLATE.format(
        module=module,
        yaml_filename=yaml_path.name,
        yaml_rel_path=yaml_rel_path,
        module_name=module_name,
        test_functions="\n".join(funcs),
    )

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"test_{module}.py"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content.lstrip("\n"))

    return output_file, len(testcases), skipped_count


def validate_syntax(output_dir):
    """编译验证所有生成的 .py 文件语法"""
    import py_compile
    errors = 0
    for py_file in sorted(Path(output_dir).glob("*.py")):
        try:
            py_compile.compile(str(py_file), doraise=True)
            print(f"  [OK] {py_file.name}")
        except py_compile.PyCompileError as e:
            print(f"  [FAIL] {py_file.name}: {e}")
            errors += 1
    return errors


def main():
    parser = argparse.ArgumentParser(description="YAML -> Pytest 脚本生成器")
    parser.add_argument(
        "--mode", choices=["baseline", "diff"], default="baseline",
        help="baseline=全量模式（默认）, diff=增量模式",
    )
    parser.add_argument(
        "--yaml-dir", default=None,
        help="YAML 测试用例目录（显式指定时覆盖 --mode 推导）",
    )
    parser.add_argument(
        "--output-dir", default=None,
        help="输出目录（显式指定时覆盖 --mode 推导）",
    )
    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="跳过语法验证",
    )
    args = parser.parse_args()

    # 路径决议: 显式指定 > mode 推导
    mode_config = MODE_PATHS[args.mode]
    yaml_dir_rel = args.yaml_dir if args.yaml_dir else mode_config["yaml_dir"]
    output_dir_rel = args.output_dir if args.output_dir else mode_config["output_dir"]
    yaml_rel_path = mode_config["yaml_rel_path"]

    yaml_dir = _PROJECT_ROOT / yaml_dir_rel
    output_dir = _PROJECT_ROOT / output_dir_rel

    if not yaml_dir.exists():
        print(f"ERROR: YAML 目录不存在: {yaml_dir}")
        sys.exit(1)

    yaml_files = sorted(yaml_dir.glob("*.yaml"))
    if not yaml_files:
        print(f"WARNING: 目录中无 .yaml 文件: {yaml_dir}")
        sys.exit(0)

    print(f"YAML 目录: {yaml_dir}")
    print(f"输出目录: {output_dir}")
    print(f"发现 {len(yaml_files)} 个 YAML 文件")
    print()

    # 1. 复制 conftest.py
    generate_conftest(output_dir)
    print(f"  [OK] conftest.py (从模板复制)")

    # 2. 为每个 YAML 生成 test 文件
    total_cases = 0
    total_skipped = 0
    for yf in yaml_files:
        result = generate_test_file(yf, output_dir, yaml_rel_path)
        if result:
            fpath, n_cases, n_skipped = result
            total_cases += n_cases
            total_skipped += n_skipped
            extra = f" (跳过 {n_skipped} 个 multipart 用例)" if n_skipped else ""
            print(f"  [OK] {fpath.name} --- {n_cases} 个用例{extra}")

    print(f"\n生成完成: {len(yaml_files)} 个文件, {total_cases} 个用例")
    if total_skipped:
        print(f"跳过 {total_skipped} 个 multipart/form-data 文件上传用例")

    # 3. 语法验证
    if not args.no_verify:
        print("\n语法验证...")
        errors = validate_syntax(output_dir)
        if errors:
            print(f"\n!!! {errors} 个文件存在语法错误，请检查 !!!")
            sys.exit(1)
        else:
            print("所有文件语法验证通过")
    else:
        print("(跳过语法验证)")


if __name__ == "__main__":
    main()
