import os
import sys
import PyInstaller.__main__

# --- 配置 ---
APP_NAME = "LinguaGacha"
ENTRY_SCRIPT = "./app.py"
RESOURCE_DIR = "./resource"
DIST_PATH = "./dist"

# --- 参数列表 ---
cmd = [
    ENTRY_SCRIPT,
    "--name", APP_NAME, 
    "--clean",          
    "--noconfirm",      
    f"--distpath={DIST_PATH}", 
    "--windowed",
    "--onedir", 
]

# --- 平台特定设置 ---
if sys.platform == "darwin": # macOS
    print("Detected macOS platform.")
    icon_file = os.path.join(RESOURCE_DIR, "icon.icns")
    if os.path.exists(icon_file):
        cmd.append(f"--icon={icon_file}")
        print(f"Using icon: {icon_file}")
    else:
        print(f"WARNING: '{icon_file}' not found. Application will have a default icon.")
    # 添加hook
    cmd.append("--runtime-hook=./hook.py")

elif sys.platform == "win32": # Windows
    print("Detected Windows platform.")
    icon_file = os.path.join(RESOURCE_DIR, "icon.ico")
    if os.path.exists(icon_file):
        cmd.append(f"--icon={icon_file}")
        print(f"Using icon: {icon_file}")
    else:
        print(f"WARNING: '{icon_file}' not found. Application may lack an icon.")

else:
    print(f"Detected other platform: {sys.platform}. Using default settings.")

# --- 处理隐藏导入 ---
requirements_file = "./requirements.txt"
print(f"Checking for hidden imports in '{requirements_file}'...")
if os.path.exists(requirements_file):
    added_hidden = 0
    with open(requirements_file, "r", encoding="utf-8") as reader:
        for line in reader:
            line = line.strip()
            # 忽略空行和注释行
            if line and not line.startswith("#"):
                cmd.append("--hidden-import=" + line)
                added_hidden += 1
    print(f"Added {added_hidden} potential hidden imports from requirements.txt.")
    if added_hidden > 0:
         print("WARNING: Adding hidden imports from requirements.txt is fragile and may lead to errors or large executables.")
else:
    print(f"'{requirements_file}' not found, skipping hidden import scan.")


# --- 执行 PyInstaller ---
print("-" * 30)
print(f"Running PyInstaller with command:\n{' '.join(cmd)}")
print("-" * 30)
PyInstaller.__main__.run(cmd)
print("-" * 30)
print("PyInstaller finished.")

# --- 检查输出 ---
expected_output = ""
if sys.platform == "darwin":
    # --onedir 在 macOS 上会创建 dist/AppName.app
    expected_output = os.path.join(DIST_PATH, f"{APP_NAME}.app")
elif sys.platform == "win32":
    if "--onedir" in cmd:
        # --onedir 在 Windows 上会创建 dist/AppName/AppName.exe
        expected_output = os.path.join(DIST_PATH, APP_NAME, f"{APP_NAME}.exe")
    # elif "--onefile" in cmd:
        # expected_output = os.path.join(DIST_PATH, f"{APP_NAME}.exe") 

if expected_output and os.path.exists(expected_output):
    print(f"Build output successfully created at: {expected_output}")
elif expected_output:
    print(f"WARNING: Expected build output not found at: {expected_output}")
