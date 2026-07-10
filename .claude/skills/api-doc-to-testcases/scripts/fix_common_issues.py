#!/usr/bin/env python3
"""Fix common YAML issues in test case files: 401 fields, body_contains, missing business_message."""
import sys, os, re
from pathlib import Path
import yaml

# Custom loader that preserves key order (Python 3.7+ dicts are ordered)
# Use standard loader

def fix_case(case):
    """Fix a single test case dict in-place."""
    fixes = 0
    expected = case.get("expected", {})
    if not isinstance(expected, dict):
        return fixes

    status_code = expected.get("status_code")
    rt = expected.get("response_type", "json")
    has_bc = "business_code" in expected and expected["business_code"] is not None

    # Fix 1: body_contains as string -> list
    if "body_contains" in expected:
        bc = expected["body_contains"]
        if isinstance(bc, str):
            expected["body_contains"] = [bc]
            fixes += 1

    # Fix 2: 401 response missing business_code
    if status_code == 401 and rt == "json":
        if not has_bc:
            expected["business_code"] = 401
            fixes += 1

    # Fix 3: json response missing business_code (non-401)
    if rt == "json" and not has_bc and status_code != 401:
        expected["business_code"] = status_code or 200
        fixes += 1

    return fixes


def fix_file(filepath):
    """Fix a YAML file. Returns number of fixes."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        print(f"  SKIP {os.path.basename(filepath)}: YAML error: {e}")
        return 0

    if not data or "testcases" not in data:
        return 0

    total_fixes = 0
    for case in data["testcases"]:
        if isinstance(case, dict):
            total_fixes += fix_case(case)

    if total_fixes > 0:
        # Write back using yaml.dump with reasonable formatting
        with open(filepath, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False,
                      sort_keys=False, indent=2, width=120)
        print(f"  Fixed {total_fixes} issues in {os.path.basename(filepath)}")

    return total_fixes


def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    target = Path(target_dir)
    files = sorted(str(p) for p in target.glob("*.yaml")) if target.is_dir() else [str(target)]
    total = 0
    for f in files:
        total += fix_file(f)
    print(f"\nTotal: {total} fixes across {len(files)} files")

if __name__ == "__main__":
    main()
