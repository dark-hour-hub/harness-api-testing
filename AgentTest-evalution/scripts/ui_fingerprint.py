# -*- coding: utf-8 -*-
"""
ui_fingerprint.py — 前端版本指纹

对前端工程 src 目录做稳定哈希（文件名+内容），变化即代表前端发版。
供 UI 测试跑前比对：指纹变化 → 提示先跑探针/检查元素地图健康度。
"""
import argparse
import hashlib
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def fingerprint_dir(directory: Path) -> str:
    """对目录下所有文件（排除 .git/__pycache__/node_modules/dist）做 sha256。"""
    directory = Path(directory)
    if not directory.exists():
        return ""
    h = hashlib.sha256()
    files = sorted(
        p for p in directory.rglob("*")
        if p.is_file()
        and not any(part in {".git", "__pycache__", "node_modules", "dist"} for part in p.parts)
    )
    for p in files:
        try:
            rel = str(p.relative_to(directory))
            h.update(rel.encode("utf-8"))
            h.update(p.read_bytes()[: 1 << 20])
        except OSError:
            continue
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description="前端版本指纹")
    parser.add_argument("--frontend", default="",
                        help="前端工程路径（默认读 config.yaml source.frontend）")
    parser.add_argument("--store", default="", help="指纹存储文件路径")
    args = parser.parse_args()

    frontend = args.frontend
    if not frontend:
        import yaml
        config = yaml.safe_load((PROJECT_ROOT / "config.yaml").read_text(encoding="utf-8")) or {}
        frontends = config.get("source", {}).get("frontend", [])
        frontend = frontends[0]["path"] if frontends else ""
    if not frontend:
        print("[ui_fingerprint] 未配置前端路径")
        sys.exit(1)

    fp = fingerprint_dir(Path(frontend))
    if not fp:
        print("[ui_fingerprint] 前端目录不存在")
        sys.exit(1)
    print(f"[ui_fingerprint] {fp}")

    if args.store:
        store = Path(args.store)
        old = store.read_text(encoding="utf-8").strip() if store.exists() else ""
        store.write_text(fp, encoding="utf-8")
        if old and old != fp:
            print("[ui_fingerprint] 前端已变更（指纹与上次不同）")
            sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
