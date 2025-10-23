#!/usr/bin/env python3
"""
使用浏览器启动应用（替代Electron）
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

def start_browser():
    """启动浏览器"""
    print("🌐 启动浏览器...")
    
    # 等待后端启动
    time.sleep(3)
    
    # 打开浏览器
    frontend_path = Path("frontend/index_browser_final.html").absolute()
    webbrowser.open(f"file://{frontend_path}")
    
    print("✅ 浏览器已打开应用")

def main():
    """主函数"""
    print("🎵 AI Audio2Note 浏览器版本启动")
    print("=" * 50)
    
    backend_process = None
    
    try:
        # 启动后端
        backend_process = start_backend()
        
        # 启动浏览器
        start_browser()
        
        print("\n✅ 服务启动完成！")
        print("🌐 后端API: http://localhost:8001")
        print("🖥️  前端应用: 已在浏览器中打开")
        print("\n按 Ctrl+C 停止服务")
        
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
        
        print("👋 再见！")

if __name__ == "__main__":
    main()
