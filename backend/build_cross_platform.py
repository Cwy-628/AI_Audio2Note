"""
跨平台构建脚本 - 支持Windows和Mac
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def detect_platform():
    """检测当前平台"""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "mac"
    elif system == "linux":
        return "linux"
    else:
        return "unknown"

def build_for_platform(target_platform=None):
    """根据平台构建相应的可执行文件"""
    
    if target_platform is None:
        target_platform = detect_platform()
    
    print(f"🎯 目标平台: {target_platform}")
    
    # 切换到backend目录
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    if target_platform == "windows":
        return build_windows()
    elif target_platform == "mac":
        return build_mac()
    elif target_platform == "linux":
        return build_linux()
    else:
        print(f"❌ 不支持的平台: {target_platform}")
        return False

def build_windows():
    """构建Windows exe文件"""
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name", "ai-audio2note-backend",
        "--add-data", "services;services",
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
    
    print("🪟 开始构建Windows exe文件...")
    return run_build_command(cmd, "ai-audio2note-backend.exe")

def build_mac():
    """构建Mac可执行文件"""
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name", "ai-audio2note-backend",
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
    
    print("🍎 开始构建Mac可执行文件...")
    return run_build_command(cmd, "ai-audio2note-backend")

def build_linux():
    """构建Linux可执行文件"""
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name", "ai-audio2note-backend",
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
    
    print("🐧 开始构建Linux可执行文件...")
    return run_build_command(cmd, "ai-audio2note-backend")

def run_build_command(cmd, expected_output):
    """运行构建命令"""
    print(f"命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 构建成功！")
        
        backend_dir = Path(__file__).parent
        output_path = backend_dir / "dist" / expected_output
        print(f"输出文件: {output_path}")
        
        if output_path.exists():
            size_mb = output_path.stat().st_size / (1024 * 1024)
            print(f"文件大小: {size_mb:.2f} MB")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e.stderr}")
        return False

def main():
    """主函数"""
    if len(sys.argv) > 1:
        target_platform = sys.argv[1].lower()
        if target_platform not in ["windows", "mac", "linux"]:
            print("❌ 无效的平台参数。支持: windows, mac, linux")
            sys.exit(1)
    else:
        target_platform = None
    
    success = build_for_platform(target_platform)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
