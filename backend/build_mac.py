"""
使用PyInstaller打包后端为Mac可执行文件
"""

import os
import sys
import subprocess
from pathlib import Path

def build_backend_mac():
    """构建Mac可执行文件"""
    
    # 切换到backend目录
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # PyInstaller命令 - Mac版本
    cmd = [
        "pyinstaller",
        "--onefile",  # 打包成单个可执行文件
        "--name", "ai-audio2note-backend",  # Mac不需要.exe扩展名
        "--add-data", "services:services",  # Mac使用冒号分隔路径
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
    
    print("🍎 开始构建Mac可执行文件...")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Mac可执行文件构建成功！")
        print(f"输出文件: {backend_dir / 'dist' / 'ai-audio2note-backend'}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Mac可执行文件构建失败: {e.stderr}")
        return False

if __name__ == "__main__":
    success = build_backend_mac()
    sys.exit(0 if success else 1)
