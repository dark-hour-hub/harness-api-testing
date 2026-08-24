# -*- coding: utf-8 -*-
# 由 feature-to-playwright skill 自动生成，请勿手动修改
from pathlib import Path
from pytest_bdd import scenarios

FEATURE_DIR = Path(__file__).resolve().parent / "../../_workflow/04-ui-scenarios"
scenarios(str(FEATURE_DIR / "02-agent-projects.feature"))
