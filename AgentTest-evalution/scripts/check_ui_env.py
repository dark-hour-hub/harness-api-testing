#!/usr/bin/env python3
"""检查 UI 测试运行环境：Python 依赖（pytest-bdd / pytest-playwright / playwright）、chromium 驱动、前端地址"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

# Windows控制台UTF-8编码支持
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def load_config(config_path: Path) -> dict:
    if yaml is None:
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def find_python(config: dict):
    tool_path = config.get("tools", {}).get("python", "")
    if tool_path:
        for candidate in (Path(tool_path) / "python.exe", Path(tool_path) / "python"):
            if candidate.exists():
                return str(candidate)
    return shutil.which("python") or "python"


def check_package(python: str, package: str) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            [python, "-m", "pip", "show", package],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        if result.returncode == 0:
            version = ""
            for line in result.stdout.splitlines():
                if line.startswith("Version:"):
                    version = line.split(":", 1)[1].strip()
                    break
            return True, f"installed ({version})" if version else "installed"
        return False, "not installed"
    except Exception as e:
        return False, str(e)


def check_chromium(python: str) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            [python, "-m", "playwright", "install", "--dry-run"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=120,
        )
        output = (result.stdout or "") + "\n" + (result.stderr or "")
    except Exception as e:
        return False, f"dry-run failed: {e}"

    installed = []
    missing = []
    for line in output.splitlines():
        line = line.strip()
        if "Install location:" not in line:
            continue
        loc = line.split(":", 1)[1].strip().strip(":")
        if Path(loc).exists():
            installed.append(Path(loc).name)
        else:
            missing.append(Path(loc).name)
    if installed:
        return True, f"installed ({', '.join(installed)})"
    return False, f"missing ({', '.join(missing) or 'chromium not installed'})"


def main():
    project_root = Path(__file__).parent.parent
    config_path = project_root / "config.yaml"
    output_dir = project_root / "tests/baseline/_workflow/01-config"
    output_file = output_dir / "ui-env.json"

    output_dir.mkdir(parents=True, exist_ok=True)

    config = load_config(config_path)
    python = find_python(config)

    env_name = config.get("current_environment", "dev")
    frontend_url = ""
    for fe in config.get("environments", {}).get(env_name, {}).get("frontend", []):
        url = (fe or {}).get("url", "")
        if url:
            frontend_url = url
            break

    results = {
        "environment": {
            "name": env_name,
            "python": python,
        },
        "frontend": {
            "url": frontend_url,
            "configured": bool(frontend_url),
        },
        "dependencies": {},
        "browsers": {},
    }

    for dep in ("playwright", "pytest", "pytest-bdd", "pytest-playwright"):
        installed, status = check_package(python, dep)
        results["dependencies"][dep] = {"installed": installed, "status": status}

    ok, status = check_chromium(python)
    results["browsers"]["chromium"] = {"ready": ok, "status": status}

    deps_ok = all(v["installed"] for v in results["dependencies"].values())
    ready = deps_ok and ok
    results["summary"] = {
        "ready": ready,
        "dependencies_ok": deps_ok,
        "chromium_ready": ok,
        "message": "UI 测试环境就绪" if ready else "UI 测试环境未就绪，请安装缺失依赖/浏览器驱动",
        "fix_hint": [
            f"{python} -m pip install pytest-bdd",
            f"{python} -m playwright install chromium",
        ],
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"检查结果已写入: {output_file}")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    sys.exit(0 if ready else 1)


if __name__ == "__main__":
    main()