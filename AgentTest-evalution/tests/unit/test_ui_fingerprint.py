# -*- coding: utf-8 -*-
"""scripts/ui_fingerprint.py 单元测试"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from ui_fingerprint import fingerprint_dir  # noqa: E402


def test_fingerprint_stable(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("x", encoding="utf-8")
    fp1 = fingerprint_dir(tmp_path)
    fp2 = fingerprint_dir(tmp_path)
    assert fp1 == fp2 and len(fp1) == 64


def test_fingerprint_changes_on_modify(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("x", encoding="utf-8")
    fp1 = fingerprint_dir(tmp_path)
    f.write_text("y", encoding="utf-8")
    assert fingerprint_dir(tmp_path) != fp1


def test_fingerprint_missing_dir(tmp_path):
    assert fingerprint_dir(tmp_path / "nope") == ""
