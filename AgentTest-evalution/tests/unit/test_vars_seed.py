# -*- coding: utf-8 -*-
"""lib/ui_profile.py 动态值展开与种子保护单元测试"""
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))

from ui_profile import expand_vars, seed_protected  # noqa: E402


def test_rand_expansion():
    v = expand_vars("AGT_${rand:8}", base_time=datetime(2026, 8, 24))
    assert v.startswith("AGT_") and len(v) == 12
    assert all(c.isalnum() for c in v[4:])


def test_rand_default_length():
    v = expand_vars("${rand}")
    assert len(v) == 8


def test_uuid_expansion():
    v = expand_vars("TC_${uuid}")
    assert v.startswith("TC_") and len(v) == 15


def test_ts_expansion():
    from datetime import timezone, timedelta
    tz8 = timezone(timedelta(hours=8))
    v = expand_vars("${ts}", base_time=datetime(2026, 8, 24, 10, 30, 0, tzinfo=tz8))
    assert v == "1787538600000"


def test_date_relative():
    v = expand_vars("${date:+1d}", base_time=datetime(2026, 8, 24))
    assert v == "2026-08-25"


def test_date_no_delta():
    v = expand_vars("${date}", base_time=datetime(2026, 8, 24))
    assert v == "2026-08-24"


def test_non_string_unchanged():
    assert expand_vars(123) == 123
    assert expand_vars("no vars here") == "no vars here"


def test_seed_protected_exact():
    assert seed_protected("BANK_AGENT", ["BANK_AGENT", "AGT_SEED_*"])


def test_seed_protected_wildcard():
    assert seed_protected("AGT_SEED_001", ["BANK_AGENT", "AGT_SEED_*"])


def test_seed_protected_not_matched():
    assert not seed_protected("AGT_UI_20260824", ["BANK_AGENT", "AGT_SEED_*"])
    assert not seed_protected("x", [])
