"""
使用PyInstaller打包后端为Mac应用程序包(.app)
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_backend_mac_app():
    """构建Mac应用程序包(.app)"""
    
    # 切换到backend目录
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # PyInstaller命令 - 创建Mac应用程序包
    cmd = [
        "pyinstaller",
        "--onedir",  # 使用目录模式，适合.app包
        "--windowed",  # 不显示控制台窗口
        "--name", "AI-Audio2Note-Backend",
        "--add-data", "services:services",
        "--hidden-import", "uvicorn.lifespan.on",
        "--hidden-import", "uvicorn.lifespan.off", 
        "--hidden-import", "uvicorn.protocols.websockets.auto",
        "--hidden-import", "uvicorn.protocols.http.auto",
        "--hidden-import", "uvicorn.protocols.websockets.websockets_impl",
        "--hidden-import", "uvicorn.protocols.http.h11_impl",
        "--hidden-import", "uvicorn.protocols.http.httptools_impl",
        "--hidden-import", "uvicorn.loops.auto",
        "--hidden-import", "uvicorn.loops.asyncio",
        "--hidden-import", "uvicorn.loops.uvloop",
        "--hidden-import", "uvicorn.logging",
        "--hidden-import", "uvicorn.logging.default",
        "--hidden-import", "uvicorn.logging.access",
        "main.py"
    ]
    
    print("🍎 开始构建Mac应用程序包(.app)...")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        # 第一步：使用PyInstaller构建
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ PyInstaller构建成功！")
        
        # 第二步：创建.app包结构
        dist_dir = backend_dir / "dist"
        app_name = "AI-Audio2Note-Backend.app"
        app_path = dist_dir / app_name
        
        # 如果已存在，先删除
        if app_path.exists():
            shutil.rmtree(app_path)
        
        # 创建.app包结构
        contents_dir = app_path / "Contents"
        macos_dir = contents_dir / "MacOS"
        resources_dir = contents_dir / "Resources"
        
        for dir_path in [contents_dir, macos_dir, resources_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # 创建Info.plist文件
        info_plist = contents_dir / "Info.plist"
        info_plist.write_text("""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>AI-Audio2Note-Backend</string>
    <key>CFBundleIdentifier</key>
    <string>com.audio2note.backend</string>
    <key>CFBundleName</key>
    <string>AI Audio2Note Backend</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>""")
        
        # 移动PyInstaller生成的文件到MacOS目录
        pyinstaller_dist = dist_dir / "AI-Audio2Note-Backend"
        if pyinstaller_dist.exists():
            for item in pyinstaller_dist.iterdir():
                if item.is_file():
                    shutil.copy2(item, macos_dir / item.name)
                elif item.is_dir():
                    shutil.copytree(item, macos_dir / item.name)
            
            # 删除PyInstaller的原始目录
            shutil.rmtree(pyinstaller_dist)
        
        print("✅ Mac应用程序包构建成功！")
        print(f"输出文件: {app_path}")
        print(f"应用程序包大小: {get_folder_size(app_path):.2f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Mac应用程序包构建失败: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ 创建.app包时出错: {str(e)}")
        return False

def get_folder_size(folder_path):
    """计算文件夹大小（MB）"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
    return total_size / (1024 * 1024)  # 转换为MB

if __name__ == "__main__":
    success = build_backend_mac_app()
    sys.exit(0 if success else 1)
