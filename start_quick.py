"""
快速启动脚本 - 不检查依赖，直接启动
"""

import subprocess
import time
import sys
from pathlib import Path

def main():
    """主函数"""
    print("🚀 AI Audio2Note 快速启动")
    print("=" * 30)
    
    backend_process = None
    frontend_process = None
    
    try:
        # 启动后端
        print("🚀 启动后端服务...")
        backend_dir = Path("backend")
        backend_process = subprocess.Popen(
            [sys.executable, "main.py"],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        time.sleep(2)  # 等待后端启动
        
        # 启动前端
        print("🚀 启动前端应用...")
        frontend_dir = Path("frontend")
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir,
            shell=True
        )
        
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
