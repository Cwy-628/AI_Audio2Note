"""
智能开发环境启动脚本
只在必要时安装依赖，避免重复安装
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def check_dependencies():
    """检查依赖是否已安装"""
    frontend_dir = Path("frontend")
    backend_dir = Path("backend")
    
    # 检查前端依赖
    frontend_deps_ok = (frontend_dir / "node_modules").exists()
    
    # 检查后端依赖
    try:
        import fastapi
        import uvicorn
        import yt_dlp
        backend_deps_ok = True
    except ImportError:
        backend_deps_ok = False
    
    return frontend_deps_ok, backend_deps_ok

def install_backend_deps():
    """安装后端依赖"""
    print("📦 安装后端依赖...")
    backend_dir = Path("backend")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      cwd=backend_dir, check=True)
        print("✅ 后端依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 后端依赖安装失败: {e}")
        return False

def install_frontend_deps():
    """安装前端依赖"""
    print("📦 安装前端依赖...")
    frontend_dir = Path("frontend")
    try:
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True, shell=True)
        print("✅ 前端依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 前端依赖安装失败: {e}")
        return False

def start_backend():
    """启动后端服务"""
    print("🚀 启动后端服务...")
    backend_dir = Path("backend")
    
    backend_process = subprocess.Popen(
        [sys.executable, "main.py"],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    return backend_process

def start_frontend():
    """启动前端服务"""
    print("🚀 启动前端服务...")
    frontend_dir = Path("frontend")
    
    # 检查Node.js和npm
    try:
        node_result = subprocess.run(["node", "--version"], capture_output=True, text=True, shell=True)
        npm_result = subprocess.run(["npm", "--version"], capture_output=True, text=True, shell=True)
        
        if node_result.returncode != 0 or npm_result.returncode != 0:
            print("❌ 请先安装Node.js和npm")
            return None
    except Exception as e:
        print(f"❌ 检查Node.js和npm时出错: {e}")
        return None
    
    # 启动前端
    print("🖥️ 启动Electron应用...")
    try:
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )
        
        # 等待一下看看是否有错误
        time.sleep(3)
        
        # 检查进程是否还在运行
        if frontend_process.poll() is not None:
            stdout, stderr = frontend_process.communicate()
            print(f"❌ 前端启动失败:")
            print(f"stdout: {stdout}")
            print(f"stderr: {stderr}")
            return None
        
        print("✅ 前端应用启动成功")
        return frontend_process
        
    except Exception as e:
        print(f"❌ 启动前端时发生错误: {e}")
        return None

def main():
    """主函数"""
    print("🎵 AI Audio2Note 智能开发环境启动")
    print("=" * 50)
    
    # 检查依赖
    frontend_deps_ok, backend_deps_ok = check_dependencies()
    
    print(f"📋 依赖检查结果:")
    print(f"   后端依赖: {'✅ 已安装' if backend_deps_ok else '❌ 需要安装'}")
    print(f"   前端依赖: {'✅ 已安装' if frontend_deps_ok else '❌ 需要安装'}")
    
    # 安装缺失的依赖
    if not backend_deps_ok:
        if not install_backend_deps():
            print("❌ 无法启动，后端依赖安装失败")
            return
    
    if not frontend_deps_ok:
        if not install_frontend_deps():
            print("❌ 无法启动，前端依赖安装失败")
            return
    
    backend_process = None
    frontend_process = None
    
    try:
        # 启动后端
        backend_process = start_backend()
        time.sleep(3)  # 等待后端启动
        
        # 启动前端
        frontend_process = start_frontend()
        
        if frontend_process is None:
            print("❌ 前端启动失败")
            return
        
        print("\n✅ 服务启动完成！")
        print("🌐 后端API: http://localhost:8000")
        print("🖥️  前端应用: 已打开")
        print("\n按 Ctrl+C 停止所有服务")
        
        # 等待用户中断
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 正在停止服务...")
        
    finally:
        # 清理进程
        if backend_process:
            backend_process.terminate()
            print("✅ 后端服务已停止")
        
        if frontend_process:
            frontend_process.terminate()
            print("✅ 前端服务已停止")
        
        print("👋 再见！")

if __name__ == "__main__":
    main()
