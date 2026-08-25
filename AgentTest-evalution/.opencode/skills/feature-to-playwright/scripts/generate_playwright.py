"""
Gherkin .feature → pytest-bdd + Playwright 脚本生成器

读取 feature 目录下的所有 .feature 文件，为每个 feature 生成一个
test_{module}.py（scenarios 绑定），并复制 conftest.py（含通用步骤库 +
截图 hook）到输出目录。

用法:
    python generate_playwright.py --mode baseline
    python generate_playwright.py --feature-dir <dir> --output-dir <dir>
"""
import argparse
import os
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "lib"))

import yaml

from db_asserts import (  # noqa: E402
    load_db_asserts, structural_errors, parse_schema_columns,
    compile_assert, validate_feature, build_module_source,
)

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFTEST_SRC = SKILL_DIR / "template" / "conftest.py"
UI_PROFILE_MODULE_SRC = PROJECT_ROOT / "lib" / "ui_profile.py"

MODE_PATHS = {
    "baseline": {
        "feature_dir": PROJECT_ROOT / "tests" / "baseline" / "_workflow" / "04-ui-scenarios",
        "output_dir": PROJECT_ROOT / "tests" / "baseline" / "generated" / "ui-test",
        "db_asserts": PROJECT_ROOT / "tests" / "baseline" / "_workflow" / "00-requirements" / "db-asserts.yaml",
    },
    "diff": {
        "feature_dir": PROJECT_ROOT / "tests" / "diff" / "_workflow" / "02-ui-scenarios",
        "output_dir": PROJECT_ROOT / "tests" / "diff" / "generated" / "ui-test",
        "db_asserts": PROJECT_ROOT / "tests" / "diff" / "_workflow" / "00-requirements" / "db-asserts.yaml",
    },
}


def slug_module(name: str) -> str:
    """从文件名提取模块名: 01-登录.feature -> login 之类"""
    stem = Path(name).stem
    stem = stem.split("-", 1)[-1] if "-" in stem else stem
    return stem


def resolve_schema_path(config: dict):
    """从 config.yaml source.backend[].path 定位后端 db/schema.sql；找不到返回 None"""
    for be in config.get("source", {}).get("backend", []):
        root = Path(be.get("path", ""))
        cand = root / "db" / "schema.sql"
        if cand.exists():
            return cand
        for cand in root.rglob("schema.sql"):
            return cand
    return None


def validate_and_compile(db_asserts_path, schema_path, features):
    """生成期静态校验 + 编译。返回 (compiled_map, errors)：
    - db-asserts.yaml 缺失/空 → ({}, [])（跳过 DB 断言）
    - 有映射但 schema 缺失 → errors
    - 表/列/id/变量问题 → errors（含行号）
    """
    asserts = load_db_asserts(db_asserts_path)
    if not asserts:
        return {}, []
    if schema_path is None:
        return {}, ["db-asserts.yaml 存在但未找到后端 db/schema.sql（检查 config.yaml source.backend[].path）"]
    schema_columns = parse_schema_columns(schema_path.read_text(encoding="utf-8"))
    errors = list(structural_errors(asserts))
    for feature in features:
        errors.extend(validate_feature(feature.read_text(encoding="utf-8"), asserts, schema_columns))
    compiled = {}
    for rid, entry in asserts.items():
        try:
            compiled[rid] = compile_assert(entry, schema_columns)
        except ValueError as e:
            errors.append(str(e))
    return compiled, errors


def generate_test_file(feature_file: Path, feature_dir: Path, output_dir: Path) -> str:
    """为一个 feature 生成 test_{module}.py"""
    module = slug_module(feature_file.name)
    rel = os.path.relpath(feature_dir, output_dir).replace("\\", "/")
    content = (
        "# -*- coding: utf-8 -*-\n"
        "# 由 feature-to-playwright skill 自动生成，请勿手动修改\n"
        "from pathlib import Path\n"
        "from pytest_bdd import scenarios\n\n"
        f'FEATURE_DIR = Path(__file__).resolve().parent / "{rel}"\n'
        f'scenarios(str(FEATURE_DIR / "{feature_file.name}"))\n'
    )
    out_file = output_dir / f"test_{module}.py"
    out_file.write_text(content, encoding="utf-8")
    return str(out_file)


def main():
    parser = argparse.ArgumentParser(description="生成 pytest-bdd + Playwright 测试脚本")
    parser.add_argument("--mode", choices=["baseline", "diff"], default="baseline",
                        help="模式: baseline=全量, diff=增量 (默认: baseline)")
    parser.add_argument("--feature-dir", default=None, help="feature 文件目录（优先级高于 --mode）")
    parser.add_argument("--output-dir", default=None, help="输出目录（优先级高于 --mode）")
    parser.add_argument("--db-asserts", default=None, help="db-asserts.yaml 路径（默认按 mode 决议）")
    args = parser.parse_args()

    mode_config = MODE_PATHS[args.mode]
    feature_dir = Path(args.feature_dir) if args.feature_dir else mode_config["feature_dir"]
    output_dir = Path(args.output_dir) if args.output_dir else mode_config["output_dir"]

    if not feature_dir.exists():
        print(f"[generate_playwright] 错误: feature 目录不存在: {feature_dir}")
        sys.exit(1)

    features = sorted(feature_dir.glob("*.feature"))
    if not features:
        print(f"[generate_playwright] 错误: 未找到 .feature 文件: {feature_dir}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    # —— DB 断言：生成期静态校验 + 编译产物 ——
    db_asserts_path = Path(args.db_asserts) if args.db_asserts else mode_config["db_asserts"]
    config = {}
    config_path = PROJECT_ROOT / "config.yaml"
    if config_path.exists():
        try:
            config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        except Exception:
            config = {}
    compiled_map, errors = validate_and_compile(db_asserts_path, resolve_schema_path(config), features)
    if errors:
        print("[generate_playwright] DB 断言校验失败：")
        for e in errors:
            print(f"  [ERROR] {e}")
        sys.exit(1)
    if compiled_map:
        (output_dir / "db_asserts.py").write_text(
            build_module_source(compiled_map), encoding="utf-8")
        print(f"[generate_playwright] [OK] db_asserts.py 已生成（{len(compiled_map)} 条映射）")
    else:
        print("[generate_playwright] 未找到 db-asserts.yaml，跳过 DB 断言")

    # 清空旧的 test_*.py（保留用户补充的 steps）
    for old in output_dir.glob("test_*.py"):
        old.unlink()

    generated = []
    for f in features:
        out = generate_test_file(f, feature_dir, output_dir)
        generated.append((f.name, out))

    # 复制 conftest.py
    if not CONFTEST_SRC.exists():
        print(f"[generate_playwright] 错误: conftest 模板不存在: {CONFTEST_SRC}")
        sys.exit(1)
    shutil.copy(CONFTEST_SRC, output_dir / "conftest.py")

    if UI_PROFILE_MODULE_SRC.exists():
        shutil.copy(UI_PROFILE_MODULE_SRC, output_dir / "ui_profile.py")
        print("[generate_playwright] [OK] ui_profile.py 已复制")
    else:
        print(f"[generate_playwright] 错误: ui_profile 模块不存在: {UI_PROFILE_MODULE_SRC}")
        sys.exit(1)

    print(f"[generate_playwright] feature 目录: {feature_dir}")
    print(f"[generate_playwright] 输出目录: {output_dir}")
    print(f"[generate_playwright] 发现 {len(features)} 个 feature 文件")
    for name, out in generated:
        print(f"  [OK] {name} -> {Path(out).name}")
    print(f"[generate_playwright] 生成完成: {len(features)} 个 test 文件 + conftest.py")


if __name__ == "__main__":
    main()
