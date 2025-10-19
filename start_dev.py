"""
开发环境启动脚本
同时启动后端和前端服务
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def start_backend():
    """启动后端服务"""
    print("🚀 启动后端服务...")
    backend_dir = Path("backend")
    
    # 检查依赖是否安装
    try:
        import fastapi
        import uvicorn
    except ImportError:
        print("📦 安装后端依赖...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=backend_dir)
    
    # 启动后端
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
            print(f"Node.js检查结果: {node_result.returncode}")
            print(f"npm检查结果: {npm_result.returncode}")
            return None
        else:
            print(f"✅ Node.js版本: {node_result.stdout.strip()}")
            print(f"✅ npm版本: {npm_result.stdout.strip()}")
    except Exception as e:
        print(f"❌ 检查Node.js和npm时出错: {e}")
        return None
    
    # 检查并安装前端依赖
    node_modules_path = frontend_dir / "node_modules"
    if not node_modules_path.exists():
        print("📦 安装前端依赖...")
        try:
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ 前端依赖安装失败: {e}")
            return None
    else:
        print("✅ 前端依赖已存在，跳过安装")
    
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
    print("🎵 AI Audio2Note 开发环境启动")
    print("=" * 50)
    
    backend_process = None
    frontend_process = None
    
    try:
        # 启动后端
        backend_process = start_backend()
        time.sleep(3)  # 等待后端启动
        
        # 启动前端
        frontend_process = start_frontend()
        
        print("\n✅ 服务启动完成！")
        print("🌐 后端API: http://localhost:8000")
        print("🖥️  前端应用: 将自动打开")
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
