#!/usr/bin/env python3
"""检查config.yaml中tools配置的环境变量和测试依赖是否安装"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

# Windows控制台UTF-8编码支持
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def load_config(config_path: str) -> dict[str, Any]:
    """加载config.yaml"""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def check_path_exists(path: str) -> tuple[bool, str]:
    """检查路径是否存在，Windows下处理bin目录的Python安装"""
    if os.path.exists(path):
        return True, "exists"

    # Windows下特殊处理：检查D:/python/Python314/bin/python.exe的情况
    # 如果配置的bin目录不存在，尝试检查父目录或python.exe
    path_obj = Path(path)
    if sys.platform == "win32":
        # 尝试 path/python.exe
        python_exe = path_obj / "python.exe"
        if python_exe.exists():
            return True, f"exists (via {python_exe})"

        # 尝试 path/Scripts/python.exe (Windows常见结构)
        scripts_python = path_obj.parent / "Scripts" / "python.exe"
        if scripts_python.exists():
            return True, f"exists (via {scripts_python})"

        # 尝试父目录/python.exe
        parent_python = path_obj.parent / "python.exe"
        if parent_python.exists():
            return True, f"exists (via {parent_python})"

    return False, "path not found"


def check_command_available(command: str) -> tuple[bool, str]:
    """检查命令是否可用（通过which或where）"""
    try:
        result = subprocess.run(
            ["where" if sys.platform == "win32" else "which", command],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return True, result.stdout.strip().split("\n")[0]
        return False, "command not found"
    except Exception as e:
        return False, str(e)


def check_python_package(package: str) -> tuple[bool, str]:
    """检查Python包是否已安装"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return True, "installed"
        return False, "not installed"
    except Exception as e:
        return False, str(e)


def main():
    # 项目根目录
    project_root = Path(__file__).parent.parent
    config_path = project_root / "config.yaml"
    output_dir = project_root / "tests/baseline/_workflow/01-config"
    output_file = output_dir / "output.json"

    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)

    # 加载配置
    config = load_config(config_path)
    tools = config.get("tools", {})

    results = {
        "tools": {},
        "dependencies": {},
    }

    # 检查tools配置的环境变量/路径
    for tool_name, tool_path in tools.items():
        if tool_name in ["python", "jmeter", "git"]:
            exists, status = check_path_exists(tool_path)
        else:
            exists, status = check_command_available(tool_name)

        results["tools"][tool_name] = {
            "configured_path": tool_path,
            "exists": exists,
            "status": status,
        }

    # 检查测试依赖
    test_deps = ["pytest", "playwright"]
    for dep in test_deps:
        exists, status = check_python_package(dep)
        results["dependencies"][dep] = {
            "installed": exists,
            "status": status,
        }

    # 统计检查结果
    passed_count = 0
    failed_count = 0

    for tool_name, tool_info in results["tools"].items():
        if tool_info["exists"]:
            passed_count += 1
        else:
            failed_count += 1

    for dep_name, dep_info in results["dependencies"].items():
        if dep_info["installed"]:
            passed_count += 1
        else:
            failed_count += 1

    results["summary"] = {
        "passed": passed_count,
        "failed": failed_count,
        "total": passed_count + failed_count,
        "message": f"检查完成：通过 {passed_count} 项，失败 {failed_count} 项"
    }

    # 写入output.json
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"检查结果已写入: {output_file}")
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()