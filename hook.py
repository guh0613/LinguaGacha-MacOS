# -*- coding: utf-8 -*-
"""
在 macOS .app 启动时把 CWD 切到 .app 同级目录
"""

import os, sys
from pathlib import Path

if getattr(sys, "frozen", False):                     # 只在冻结环境生效
    app_exe = Path(sys.executable).resolve()          # …/MyApp.app/Contents/MacOS/MyApp
    bundle_parent = app_exe.parents[3]                # dist/   (.app 的上一级)
    os.chdir(bundle_parent)                   # 👉 CWD = dist/res