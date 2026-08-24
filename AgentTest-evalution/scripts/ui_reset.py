# -*- coding: utf-8 -*-
"""
ui_reset.py — UI 测试环境重置适配器（跑前清理 + 种子恢复）

流程：读取 ui-profile/reset/cleanup_template.sql → 解析清理计划 →
人工确认（--yes 跳过）→ 执行（--dry-run 只打印不执行）。

执行方式（按 business.yaml reset.exec 配置）：
  - ""（默认）：只打印 SQL 供人工执行（安全默认）
  - 形如 "mysql -u root -p < {sql}"：用 {sql} 占位符替换后 subprocess 执行
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def build_plan(sql_path: Path) -> dict:
    """解析清理模板：提取非注释 DELETE/TRUNCATE 语句与其目标表。"""
    sql_path = Path(sql_path)
    if not sql_path.exists():
        return {"statements": [], "tables": []}
    text = sql_path.read_text(encoding="utf-8")
    statements = []
    tables = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("--"):
            continue
        statements.append(stripped)
        m = re.search(r"\b(?:DELETE FROM|TRUNCATE)\s+(\w+)", stripped, re.IGNORECASE)
        if m and m.group(1) not in tables:
            tables.append(m.group(1))
    return {"statements": statements, "tables": tables}


def parse_confirmation(answer: str) -> bool:
    return answer.strip().lower() in ("yes", "y")


def main():
    parser = argparse.ArgumentParser(description="UI 测试环境重置（跑前清理）")
    parser.add_argument("--profile", default=str(PROJECT_ROOT / "ui-profile"),
                        help="profile 目录（默认 ui-profile/）")
    parser.add_argument("--dry-run", action="store_true", help="只展示清理计划，不执行")
    parser.add_argument("--yes", action="store_true", help="跳过确认")
    args = parser.parse_args()

    profile = Path(args.profile)
    sql_path = profile / "reset" / "cleanup_template.sql"
    plan = build_plan(sql_path)

    print("=" * 60)
    print(f"[ui_reset] 清理模板: {sql_path}")
    if not plan["statements"]:
        print("[ui_reset] 无清理语句（模板为空或不存在）——跳过重置")
        return
    print(f"[ui_reset] 将执行 {len(plan['statements'])} 条语句，涉及表: {', '.join(plan['tables'])}")
    for s in plan["statements"]:
        print(f"  > {s}")

    if args.dry_run:
        print("[ui_reset] --dry-run：未执行，请人工核对后执行或去掉 --dry-run")
        return

    if not args.yes:
        try:
            answer = input("确认执行以上清理？（yes/no）: ")
        except EOFError:
            answer = ""
        if not parse_confirmation(answer):
            print("[ui_reset] 已取消")
            return

    # 执行方式：默认打印供人工执行；配置了 reset.exec 则执行
    try:
        import yaml
        business = {}
        bp = profile / "business.yaml"
        if bp.exists():
            business = yaml.safe_load(bp.read_text(encoding="utf-8")) or {}
    except Exception:
        business = {}
    exec_cmd = (business.get("reset") or {}).get("exec", "")
    if not exec_cmd:
        print("[ui_reset] 未配置 reset.exec，以下语句请人工在测试库执行：")
        for s in plan["statements"]:
            print(f"  {s}")
        return
    cmd = exec_cmd.replace("{sql}", str(sql_path))
    print(f"[ui_reset] 执行: {cmd}")
    result = subprocess.run(cmd, shell=True, encoding="utf-8", errors="replace")
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
