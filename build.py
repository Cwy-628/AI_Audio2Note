"""
AI Audio2Note 构建脚本
用于打包整个应用为可执行文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, cwd=None):
    """运行命令并处理错误"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
        print(f"✅ 命令执行成功: {command}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {command}")
        print(f"错误信息: {e.stderr}")
        return None

def build_backend():
    """构建后端"""
    print("🔧 构建后端...")
    
    # 安装后端依赖
    print("📦 安装后端依赖...")
    result = run_command("pip install -r requirements.txt", cwd="backend")
    if not result:
        return False
    
    return True

def build_frontend():
    """构建前端"""
    print("🔧 构建前端...")
    
    # 安装前端依赖
    print("📦 安装前端依赖...")
    result = run_command("npm install", cwd="frontend")
    if not result:
        return False
    
    return True

def create_distribution():
    """创建发布版本"""
    print("📦 创建发布版本...")
    
    # 创建dist目录
    dist_dir = Path("dist")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()
    
    # 复制后端文件
    backend_dist = dist_dir / "backend"
    shutil.copytree("backend", backend_dist)
    
    # 复制前端文件
    frontend_dist = dist_dir / "frontend"
    shutil.copytree("frontend", frontend_dist)
    
    # 创建启动脚本
    create_start_scripts(dist_dir)
    
    print("✅ 发布版本创建完成")
    return True

def create_start_scripts(dist_dir):
    """创建启动脚本"""
    
    # Windows启动脚本
    start_script = dist_dir / "start.bat"
    with open(start_script, 'w', encoding='utf-8') as f:
        f.write("""@echo off
echo 启动AI Audio2Note...
echo.

echo 启动后端服务...
cd backend
start /B python main.py
timeout /t 3 /nobreak > nul

echo 启动前端应用...
cd ..\\frontend
start /B npm start

echo.
echo 应用已启动！
echo 后端服务: http://localhost:8000
echo 前端应用: 将自动打开
echo.
pause
""")
    
    # Linux/Mac启动脚本
    start_script = dist_dir / "start.sh"
    with open(start_script, 'w', encoding='utf-8') as f:
        f.write("""#!/bin/bash
echo "启动AI Audio2Note..."
echo

echo "启动后端服务..."
cd backend
python main.py &
BACKEND_PID=$!

sleep 3

echo "启动前端应用..."
cd ../frontend
npm start &
FRONTEND_PID=$!

echo
echo "应用已启动！"
echo "后端服务: http://localhost:8000"
echo "前端应用: 将自动打开"
echo
echo "按Ctrl+C停止所有服务"
echo

# 等待用户中断
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
""")
    
    # 设置执行权限
    if os.name != 'nt':
        os.chmod(start_script, 0o755)

def build_electron_app():
    """构建Electron应用"""
    print("🔧 构建Electron应用...")
    
    # 构建Electron应用
    result = run_command("npm run build-win", cwd="frontend")
    if not result:
        return False
    
    print("✅ Electron应用构建完成")
    return True

def main():
    """主函数"""
    print("🚀 AI Audio2Note 构建脚本")
    print("=" * 50)
    
    # 检查Python环境
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8或更高版本")
        return False
    
    # 检查Node.js环境
    result = run_command("node --version")
    if not result:
        print("❌ 需要安装Node.js")
        return False
    
    # 检查npm
    result = run_command("npm --version")
    if not result:
        print("❌ 需要安装npm")
        return False
    
    # 构建后端
    if not build_backend():
        print("❌ 后端构建失败")
        return False
    
    # 构建前端
    if not build_frontend():
        print("❌ 前端构建失败")
        return False
    
    # 创建发布版本
    if not create_distribution():
        print("❌ 发布版本创建失败")
        return False
    
    # 构建Electron应用
    if not build_electron_app():
        print("❌ Electron应用构建失败")
        return False
    
    print("🎉 构建完成！")
    print("📁 发布文件位于: dist/")
    print("📁 Electron应用位于: frontend/dist/")
    print("🚀 运行 start.bat (Windows) 或 start.sh (Linux/Mac) 启动应用")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
