#!/usr/bin/env python3
"""
AI Audio2Note 快速构建脚本
简化版本，专注于核心功能
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """运行命令并打印输出"""
    print(f"🔧 执行: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {e}")
        if e.stderr:
            print(f"错误信息: {e.stderr}")
        return False

def check_dependencies():
    """检查基本依赖"""
    print("🔍 检查依赖...")
    
    # 检查Python
    if sys.version_info < (3, 8):
        print("❌ Python版本过低，需要3.8+")
        return False
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller已安装")
    except ImportError:
        print("📦 安装PyInstaller...")
        if not run_command([sys.executable, "-m", "pip", "install", "pyinstaller"]):
            return False
    
    # 检查Node.js
    if not run_command(["node", "--version"], check=False):
        print("❌ Node.js未安装，请先安装Node.js")
        return False
    
    # 检查npm
    if not run_command(["npm", "--version"], check=False):
        print("❌ npm未安装，请先安装npm")
        return False
    
    print("✅ 所有依赖检查通过")
    return True

def build_backend():
    """构建后端"""
    print("🔨 构建后端...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ backend目录不存在")
        return False
    
    # 检查是否已经构建过
    backend_exe = backend_dir / "dist" / "ai-audio2note-backend"
    if backend_exe.exists():
        print("✅ 后端已构建，跳过构建步骤")
        return True
    
    # 直接使用PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name", "ai-audio2note-backend",
        "--add-data", "services:services",
        "--console",
        "main.py"
    ]
    return run_command(cmd, cwd=backend_dir)

def build_frontend():
    """构建前端"""
    print("⚡ 构建前端...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ frontend目录不存在")
        return False
    
    # 检查是否已经安装依赖
    node_modules = frontend_dir / "node_modules"
    if not node_modules.exists():
        print("📦 安装前端依赖...")
        if not run_command(["npm", "install"], cwd=frontend_dir):
            return False
    else:
        print("✅ 前端依赖已安装")
    
    # 由于electron-builder网络问题，我们跳过构建步骤
    # 直接使用源码运行
    print("✅ 前端准备完成（使用源码模式）")
    return True

def create_package():
    """创建分发包"""
    print("📦 创建分发包...")
    
    system = platform.system().lower()
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)
    
    if system == "windows":
        return create_windows_package()
    elif system == "darwin":
        return create_mac_package()
    else:
        print(f"❌ 不支持的操作系统: {system}")
        return False

def create_windows_package():
    """创建Windows分发包"""
    print("🪟 创建Windows分发包...")
    
    package_dir = Path("dist/AI_Audio2Note_Windows")
    package_dir.mkdir(exist_ok=True)
    
    # 复制后端
    backend_exe = Path("backend/dist/ai-audio2note-backend.exe")
    if backend_exe.exists():
        shutil.copy2(backend_exe, package_dir / "ai-audio2note-backend.exe")
        print("✅ 后端已复制")
    else:
        print("❌ 后端可执行文件不存在")
        return False
    
    # 复制前端
    frontend_dist = Path("frontend/dist/win-unpacked")
    if frontend_dist.exists():
        shutil.copytree(frontend_dist, package_dir / "AI_Audio2Note", dirs_exist_ok=True)
        print("✅ 前端已复制")
    else:
        print("❌ 前端应用不存在")
        return False
    
    # 创建启动脚本
    startup_script = package_dir / "启动AI_Audio2Note.bat"
    with open(startup_script, 'w', encoding='utf-8') as f:
        f.write("""@echo off
echo 启动AI Audio2Note...
start /B ai-audio2note-backend.exe
timeout /t 3 /nobreak >nul
start AI_Audio2Note\\AI_Audio2Note.exe
echo 应用已启动！
pause
""")
    
    print(f"✅ Windows分发包创建完成: {package_dir}")
    return True

def create_mac_package():
    """创建Mac分发包"""
    print("🍎 创建Mac分发包...")
    
    package_dir = Path("dist/AI_Audio2Note_Mac")
    package_dir.mkdir(exist_ok=True)
    
    # 复制后端
    backend_exe = Path("backend/dist/ai-audio2note-backend")
    if backend_exe.exists():
        shutil.copy2(backend_exe, package_dir / "ai-audio2note-backend")
        os.chmod(package_dir / "ai-audio2note-backend", 0o755)
        print("✅ 后端已复制")
    else:
        print("❌ 后端可执行文件不存在")
        return False
    
    # 创建FFmpeg安装脚本
    ffmpeg_install_script = package_dir / "安装FFmpeg.command"
    with open(ffmpeg_install_script, 'w', encoding='utf-8') as f:
        f.write("""#!/bin/bash
echo "安装FFmpeg..."

# 检查是否已安装Homebrew
if ! command -v brew &> /dev/null; then
    echo "正在安装Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# 安装FFmpeg
echo "正在安装FFmpeg..."
brew install ffmpeg

echo "FFmpeg安装完成！"
echo "现在可以运行 启动AI_Audio2Note.command 启动应用"
""")
    os.chmod(ffmpeg_install_script, 0o755)
    print("✅ FFmpeg安装脚本已创建")
    
    # 复制前端源码
    frontend_dir = Path("frontend")
    frontend_package_dir = package_dir / "frontend"
    shutil.copytree(frontend_dir, frontend_package_dir, dirs_exist_ok=True)
    print("✅ 前端源码已复制")
    
    # 创建启动脚本
    startup_script = package_dir / "启动AI_Audio2Note.command"
    with open(startup_script, 'w', encoding='utf-8') as f:
        f.write("""#!/bin/bash
echo "启动AI Audio2Note..."

# 检查FFmpeg是否安装
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ FFmpeg未安装！"
    echo "请先运行 安装FFmpeg.command 安装FFmpeg"
    echo "或者手动安装：brew install ffmpeg"
    read -p "按回车键退出..."
    exit 1
fi

echo "✅ FFmpeg已安装"

# 停止可能运行的后端进程
pkill -f "ai-audio2note-backend" 2>/dev/null || true

echo "正在启动后端服务..."
./ai-audio2note-backend &
sleep 3

echo "正在打开浏览器..."
open "http://localhost:8001"

echo "应用已启动！"
echo "请在浏览器中使用应用"
echo "按 Ctrl+C 停止服务"
""")
    os.chmod(startup_script, 0o755)
    
    # 创建说明文件
    readme_file = package_dir / "使用说明.txt"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write("""AI Audio2Note - 视频音频提取工具

使用说明：
1. 首次使用：双击"安装FFmpeg.command"安装FFmpeg
2. 启动应用：双击"启动AI_Audio2Note.command"启动应用
3. 应用会自动在浏览器中打开
4. 在应用界面中输入视频链接
5. 选择下载文件夹
6. 点击开始下载

支持平台：
- B站 (bilibili.com)
- YouTube (youtube.com)

系统要求：
- macOS 10.14+
- 已安装FFmpeg
- 现代浏览器（Chrome、Safari、Firefox等）

安装步骤：
1. 安装FFmpeg：双击"安装FFmpeg.command"或运行 brew install ffmpeg

注意事项：
- 首次使用需要安装FFmpeg
- 应用在浏览器中运行，无需安装额外软件
- 确保网络连接正常
- 视频链接必须是公开可访问的

如有问题，请查看项目文档。
""")
    
    print(f"✅ Mac分发包创建完成: {package_dir}")
    return True

def main():
    """主函数"""
    print("🚀 AI Audio2Note 快速构建")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        print("❌ 依赖检查失败")
        sys.exit(1)
    
    # 构建后端
    if not build_backend():
        print("❌ 后端构建失败")
        sys.exit(1)
    
    # 构建前端
    if not build_frontend():
        print("❌ 前端构建失败")
        sys.exit(1)
    
    # 创建分发包
    if not create_package():
        print("❌ 分发包创建失败")
        sys.exit(1)
    
    print("\n🎉 构建完成！")
    print("📦 分发包位于 dist/ 目录")
    print("📖 查看 BUILD_GUIDE.md 了解详细说明")

if __name__ == "__main__":
    main()