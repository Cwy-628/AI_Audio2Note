#!/usr/bin/env python3
"""
启动带有原生文件夹选择器的版本
支持Electron原生文件夹选择器
"""

import subprocess
import time
import sys
import webbrowser
from pathlib import Path

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

def start_native_frontend():
    """启动原生文件夹选择版本"""
    print("🌐 启动原生文件夹选择版本...")
    
    # 等待后端启动
    time.sleep(3)
    
    # 检查是否可以使用Electron
    try:
        # 尝试启动Electron版本
        frontend_dir = Path("frontend")
        electron_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待一下看看是否有错误
        time.sleep(3)
        
        # 检查进程是否还在运行
        if electron_process.poll() is not None:
            stdout, stderr = electron_process.communicate()
            print(f"❌ Electron启动失败，使用浏览器版本:")
            print(f"stdout: {stdout}")
            print(f"stderr: {stderr}")
            return start_browser_fallback()
        
        print("✅ Electron应用启动成功")
        return electron_process
        
    except Exception as e:
        print(f"❌ Electron启动失败: {e}")
        return start_browser_fallback()

def start_browser_fallback():
    """浏览器版本回退"""
    print("🌐 启动浏览器版本...")
    
    # 打开浏览器
    frontend_path = Path("frontend/index_electron_native.html").absolute()
    webbrowser.open(f"file://{frontend_path}")
    
    print("✅ 浏览器版本已打开")
    return None

def main():
    """主函数"""
    print("🎵 AI Audio2Note 原生文件夹选择版本启动")
    print("=" * 60)
    
    backend_process = None
    frontend_process = None
    
    try:
        # 启动后端
        backend_process = start_backend()
        time.sleep(3)  # 等待后端启动
        
        # 启动前端
        frontend_process = start_native_frontend()
        
        print("\n✅ 服务启动完成！")
        print("🌐 后端API: http://localhost:8001")
        print("🖥️  前端应用: 已打开")
        print("\n💡 文件夹选择功能:")
        print("   • Electron版本: 原生系统文件夹选择器")
        print("   • 浏览器版本: 改进的输入对话框")
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
