#!/usr/bin/env python3
"""
AI Audio2Note 跨平台构建脚本
支持 Mac (.app) 和 Windows (.exe) 打包
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

class CrossPlatformBuilder:
    def __init__(self):
        self.system = platform.system().lower()
        self.project_root = Path(__file__).parent
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "frontend"
        self.dist_dir = self.project_root / "dist"
        
    def check_dependencies(self):
        """检查构建依赖"""
        print("🔍 检查构建依赖...")
        
        # 检查Python依赖
        try:
            import PyInstaller
            print("✅ PyInstaller 已安装")
        except ImportError:
            print("❌ PyInstaller 未安装，正在安装...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            
        # 检查Node.js依赖
        try:
            subprocess.run(["node", "--version"], check=True, capture_output=True)
            print("✅ Node.js 已安装")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Node.js 未安装，请先安装 Node.js")
            return False
            
        # 检查npm
        try:
            subprocess.run(["npm", "--version"], check=True, capture_output=True)
            print("✅ npm 已安装")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ npm 未安装，请先安装 npm")
            return False
            
        return True
    
    def build_backend(self):
        """构建后端可执行文件"""
        print("🔨 构建后端可执行文件...")
        
        if self.system == "windows":
            return self.build_windows_backend()
        elif self.system == "darwin":  # macOS
            return self.build_mac_backend()
        else:
            print(f"❌ 不支持的操作系统: {self.system}")
            return False
    
    def build_windows_backend(self):
        """构建Windows后端"""
        print("🪟 构建Windows后端...")
        
        cmd = [
            "pyinstaller",
            "--onefile",
            "--name", "ai-audio2note-backend",
            "--add-data", "services;services",
            "--hidden-import", "uvicorn",
            "--hidden-import", "uvicorn.loops",
            "--hidden-import", "uvicorn.loops.auto",
            "--hidden-import", "uvicorn.protocols",
            "--hidden-import", "uvicorn.protocols.http",
            "--hidden-import", "uvicorn.protocols.http.auto",
            "--hidden-import", "uvicorn.protocols.websockets",
            "--hidden-import", "uvicorn.protocols.websockets.auto",
            "--hidden-import", "uvicorn.lifespan",
            "--hidden-import", "uvicorn.lifespan.on",
            "--hidden-import", "fastapi",
            "--hidden-import", "fastapi.applications",
            "--hidden-import", "fastapi.routing",
            "--hidden-import", "fastapi.middleware",
            "--hidden-import", "fastapi.middleware.cors",
            "--hidden-import", "pydantic",
            "--hidden-import", "starlette",
            "--hidden-import", "starlette.applications",
            "--hidden-import", "starlette.routing",
            "--hidden-import", "starlette.middleware",
            "--hidden-import", "starlette.middleware.cors",
            "--hidden-import", "yt_dlp",
            "--hidden-import", "yt_dlp.extractor",
            "--hidden-import", "yt_dlp.extractor.bilibili",
            "--hidden-import", "yt_dlp.extractor.youtube",
            "--hidden-import", "yt_dlp.downloader",
            "--hidden-import", "yt_dlp.downloader.http",
            "--hidden-import", "yt_dlp.postprocessor",
            "--hidden-import", "yt_dlp.postprocessor.ffmpeg",
            "--hidden-import", "ffmpeg",
            "--console",
            "main.py"
        ]
        
        try:
            subprocess.run(cmd, cwd=self.backend_dir, check=True)
            print("✅ Windows后端构建完成")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Windows后端构建失败: {e}")
            return False
    
    def build_mac_backend(self):
        """构建Mac后端"""
        print("🍎 构建Mac后端...")
        
        cmd = [
            "pyinstaller",
            "--onefile",
            "--name", "ai-audio2note-backend",
            "--add-data", "services:services",
            "--hidden-import", "uvicorn",
            "--hidden-import", "uvicorn.loops",
            "--hidden-import", "uvicorn.loops.auto",
            "--hidden-import", "uvicorn.protocols",
            "--hidden-import", "uvicorn.protocols.http",
            "--hidden-import", "uvicorn.protocols.http.auto",
            "--hidden-import", "uvicorn.protocols.websockets",
            "--hidden-import", "uvicorn.protocols.websockets.auto",
            "--hidden-import", "uvicorn.lifespan",
            "--hidden-import", "uvicorn.lifespan.on",
            "--hidden-import", "fastapi",
            "--hidden-import", "fastapi.applications",
            "--hidden-import", "fastapi.routing",
            "--hidden-import", "fastapi.middleware",
            "--hidden-import", "fastapi.middleware.cors",
            "--hidden-import", "pydantic",
            "--hidden-import", "starlette",
            "--hidden-import", "starlette.applications",
            "--hidden-import", "starlette.routing",
            "--hidden-import", "starlette.middleware",
            "--hidden-import", "starlette.middleware.cors",
            "--hidden-import", "yt_dlp",
            "--hidden-import", "yt_dlp.extractor",
            "--hidden-import", "yt_dlp.extractor.bilibili",
            "--hidden-import", "yt_dlp.extractor.youtube",
            "--hidden-import", "yt_dlp.downloader",
            "--hidden-import", "yt_dlp.downloader.http",
            "--hidden-import", "yt_dlp.postprocessor",
            "--hidden-import", "yt_dlp.postprocessor.ffmpeg",
            "--hidden-import", "ffmpeg",
            "--console",
            "main.py"
        ]
        
        try:
            subprocess.run(cmd, cwd=self.backend_dir, check=True)
            print("✅ Mac后端构建完成")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Mac后端构建失败: {e}")
            return False
    
    def build_electron_app(self):
        """构建Electron应用"""
        print("⚡ 构建Electron应用...")
        
        # 安装Electron依赖
        try:
            subprocess.run(["npm", "install"], cwd=self.frontend_dir, check=True)
            print("✅ Electron依赖安装完成")
        except subprocess.CalledProcessError as e:
            print(f"❌ Electron依赖安装失败: {e}")
            return False
        
        # 构建Electron应用
        if self.system == "windows":
            return self.build_windows_electron()
        elif self.system == "darwin":
            return self.build_mac_electron()
        else:
            print(f"❌ 不支持的操作系统: {self.system}")
            return False
    
    def build_windows_electron(self):
        """构建Windows Electron应用"""
        print("🪟 构建Windows Electron应用...")
        
        try:
            # 使用electron-builder构建
            subprocess.run(["npm", "run", "build:win"], cwd=self.frontend_dir, check=True)
            print("✅ Windows Electron应用构建完成")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Windows Electron应用构建失败: {e}")
            return False
    
    def build_mac_electron(self):
        """构建Mac Electron应用"""
        print("🍎 构建Mac Electron应用...")
        
        try:
            # 使用electron-builder构建
            subprocess.run(["npm", "run", "build:mac"], cwd=self.frontend_dir, check=True)
            print("✅ Mac Electron应用构建完成")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Mac Electron应用构建失败: {e}")
            return False
    
    def create_package(self):
        """创建最终的分发包"""
        print("📦 创建分发包...")
        
        # 创建分发目录
        self.dist_dir.mkdir(exist_ok=True)
        
        if self.system == "windows":
            return self.create_windows_package()
        elif self.system == "darwin":
            return self.create_mac_package()
        else:
            print(f"❌ 不支持的操作系统: {self.system}")
            return False
    
    def create_windows_package(self):
        """创建Windows分发包"""
        print("🪟 创建Windows分发包...")
        
        package_dir = self.dist_dir / "AI_Audio2Note_Windows"
        package_dir.mkdir(exist_ok=True)
        
        # 复制后端可执行文件
        backend_exe = self.backend_dir / "dist" / "ai-audio2note-backend.exe"
        if backend_exe.exists():
            shutil.copy2(backend_exe, package_dir / "ai-audio2note-backend.exe")
            print("✅ 后端可执行文件已复制")
        else:
            print("❌ 后端可执行文件不存在")
            return False
        
        # 复制Electron应用
        electron_dir = self.frontend_dir / "dist" / "win-unpacked"
        if electron_dir.exists():
            shutil.copytree(electron_dir, package_dir / "AI_Audio2Note", dirs_exist_ok=True)
            print("✅ Electron应用已复制")
        else:
            print("❌ Electron应用不存在")
            return False
        
        # 创建启动脚本
        startup_script = package_dir / "启动AI_Audio2Note.bat"
        with open(startup_script, 'w', encoding='utf-8') as f:
            f.write("""@echo off
echo 启动AI Audio2Note...
echo 正在启动后端服务...
start /B ai-audio2note-backend.exe
timeout /t 3 /nobreak >nul
echo 正在启动桌面应用...
start AI_Audio2Note\\AI_Audio2Note.exe
echo 应用已启动！
pause
""")
        
        # 创建说明文件
        readme_file = package_dir / "使用说明.txt"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write("""AI Audio2Note - 视频音频提取工具

使用说明：
1. 双击"启动AI_Audio2Note.bat"启动应用
2. 在应用界面中输入视频链接
3. 选择下载文件夹
4. 点击开始下载

支持平台：
- B站 (bilibili.com)
- YouTube (youtube.com)

系统要求：
- Windows 10/11
- 已安装FFmpeg

注意事项：
- 首次使用需要安装FFmpeg
- 确保网络连接正常
- 视频链接必须是公开可访问的

如有问题，请查看项目文档。
""")
        
        print(f"✅ Windows分发包创建完成: {package_dir}")
        return True
    
    def create_mac_package(self):
        """创建Mac分发包"""
        print("🍎 创建Mac分发包...")
        
        package_dir = self.dist_dir / "AI_Audio2Note_Mac"
        package_dir.mkdir(exist_ok=True)
        
        # 复制后端可执行文件
        backend_exe = self.backend_dir / "dist" / "ai-audio2note-backend"
        if backend_exe.exists():
            shutil.copy2(backend_exe, package_dir / "ai-audio2note-backend")
            # 添加执行权限
            os.chmod(package_dir / "ai-audio2note-backend", 0o755)
            print("✅ 后端可执行文件已复制")
        else:
            print("❌ 后端可执行文件不存在")
            return False
        
        # 复制Electron应用
        electron_app = self.frontend_dir / "dist" / "AI_Audio2Note.app"
        if electron_app.exists():
            shutil.copytree(electron_app, package_dir / "AI_Audio2Note.app", dirs_exist_ok=True)
            print("✅ Electron应用已复制")
        else:
            print("❌ Electron应用不存在")
            return False
        
        # 创建启动脚本
        startup_script = package_dir / "启动AI_Audio2Note.command"
        with open(startup_script, 'w', encoding='utf-8') as f:
            f.write("""#!/bin/bash
echo "启动AI Audio2Note..."
echo "正在启动后端服务..."
./ai-audio2note-backend &
sleep 3
echo "正在启动桌面应用..."
open AI_Audio2Note.app
echo "应用已启动！"
""")
        
        # 添加执行权限
        os.chmod(startup_script, 0o755)
        
        # 创建说明文件
        readme_file = package_dir / "使用说明.txt"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write("""AI Audio2Note - 视频音频提取工具

使用说明：
1. 双击"启动AI_Audio2Note.command"启动应用
2. 在应用界面中输入视频链接
3. 选择下载文件夹
4. 点击开始下载

支持平台：
- B站 (bilibili.com)
- YouTube (youtube.com)

系统要求：
- macOS 10.14+
- 已安装FFmpeg

安装FFmpeg：
brew install ffmpeg

注意事项：
- 首次使用需要安装FFmpeg
- 确保网络连接正常
- 视频链接必须是公开可访问的

如有问题，请查看项目文档。
""")
        
        print(f"✅ Mac分发包创建完成: {package_dir}")
        return True
    
    def build_all(self):
        """执行完整构建流程"""
        print("🚀 开始跨平台构建...")
        print(f"🖥️  目标系统: {self.system}")
        
        # 检查依赖
        if not self.check_dependencies():
            return False
        
        # 构建后端
        if not self.build_backend():
            return False
        
        # 构建Electron应用
        if not self.build_electron_app():
            return False
        
        # 创建分发包
        if not self.create_package():
            return False
        
        print("🎉 构建完成！")
        print(f"📦 分发包位置: {self.dist_dir}")
        return True

def main():
    """主函数"""
    builder = CrossPlatformBuilder()
    success = builder.build_all()
    
    if success:
        print("\n✅ 构建成功！")
        print("📦 分发包已创建，可以直接分发给用户使用")
    else:
        print("\n❌ 构建失败！")
        sys.exit(1)

if __name__ == "__main__":
    main()