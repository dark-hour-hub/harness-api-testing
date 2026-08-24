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
SKILL_DIR = Path(__file__).resolve().parent.parent
CONFTEST_SRC = SKILL_DIR / "template" / "conftest.py"
UI_PROFILE_MODULE_SRC = PROJECT_ROOT / "lib" / "ui_profile.py"

MODE_PATHS = {
    "baseline": {
        "feature_dir": PROJECT_ROOT / "tests" / "baseline" / "_workflow" / "04-ui-scenarios",
        "output_dir": PROJECT_ROOT / "tests" / "baseline" / "generated" / "ui-test",
    },
    "diff": {
        "feature_dir": PROJECT_ROOT / "tests" / "diff" / "_workflow" / "02-ui-scenarios",
        "output_dir": PROJECT_ROOT / "tests" / "diff" / "generated" / "ui-test",
    },
}


def slug_module(name: str) -> str:
    """从文件名提取模块名: 01-登录.feature -> login 之类"""
    stem = Path(name).stem
    stem = stem.split("-", 1)[-1] if "-" in stem else stem
    return stem


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

    print(f"[generate_playwright] feature 目录: {feature_dir}")
    print(f"[generate_playwright] 输出目录: {output_dir}")
    print(f"[generate_playwright] 发现 {len(features)} 个 feature 文件")
    for name, out in generated:
        print(f"  [OK] {name} -> {Path(out).name}")
    print(f"[generate_playwright] 生成完成: {len(features)} 个 test 文件 + conftest.py")


if __name__ == "__main__":
    main()
