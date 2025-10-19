"""
使用PyInstaller打包后端为exe文件
"""

import os
import sys
import subprocess
from pathlib import Path

def build_backend_exe():
    """构建后端exe文件"""
    
    # 切换到backend目录
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # PyInstaller命令
    cmd = [
        "pyinstaller",
        "--onefile",  # 打包成单个exe文件
        "--name", "ai-audio2note-backend",
        "--add-data", "services;services",  # 包含services目录
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
    
    print("🔧 开始构建后端exe文件...")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 后端exe构建成功！")
        print(f"输出文件: {backend_dir / 'dist' / 'ai-audio2note-backend.exe'}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 后端exe构建失败: {e.stderr}")
        return False

if __name__ == "__main__":
    success = build_backend_exe()
    sys.exit(0 if success else 1)
