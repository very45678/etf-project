#!/usr/bin/env python3
"""
系统启动脚本
功能：初始化数据库、启动后端服务和定时任务
"""

import os
import sys
import subprocess
import time
import threading

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(PROJECT_ROOT, 'backend')
FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')

def run_command(command, cwd=None, shell=True, daemon=False):
    """运行命令"""
    print(f"执行命令: {command}")
    if daemon:
        # 后台运行
        process = subprocess.Popen(command, cwd=cwd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    else:
        # 前台运行
        result = subprocess.run(command, cwd=cwd, shell=shell, capture_output=True, text=True)
        print(f"命令执行结果: {result.returncode}")
        if result.stdout:
            print(f"标准输出: {result.stdout}")
        if result.stderr:
            print(f"标准错误: {result.stderr}")
        return result

def init_database():
    """初始化数据库"""
    print("\n=== 初始化数据库 ===")
    # 进入backend目录
    os.chdir(BACKEND_DIR)
    
    # 运行数据库初始化脚本
    result = run_command('python init_db.py')
    if result.returncode != 0:
        print("数据库初始化失败！")
        return False
    
    # 插入测试数据
    result = run_command('python insert_test_data.py')
    if result.returncode != 0:
        print("插入测试数据失败！")
        return False
    
    print("数据库初始化成功！")
    return True

def start_backend_service():
    """启动后端服务"""
    print("\n=== 启动后端服务 ===")
    # 进入backend目录
    os.chdir(BACKEND_DIR)
    
    # 启动后端服务
    process = run_command('python api.py', daemon=True)
    print("后端服务已启动，运行在 http://localhost:5000")
    return process

def start_scheduler():
    """启动定时任务"""
    print("\n=== 启动定时任务 ===")
    # 进入backend目录
    os.chdir(BACKEND_DIR)
    
    # 启动定时任务
    process = run_command('python run_scheduler.py', daemon=True)
    print("定时任务已启动")
    return process

def start_frontend_service():
    """启动前端服务"""
    print("\n=== 启动前端服务 ===")
    # 进入frontend目录
    os.chdir(FRONTEND_DIR)
    
    # 启动前端服务
    process = run_command('npm run dev', daemon=True)
    print("前端服务已启动，运行在 http://localhost:5173")
    return process

def main():
    """主函数"""
    print("=== 货币基金套利提示系统启动脚本 ===")
    
    # 初始化数据库
    if not init_database():
        sys.exit(1)
    
    # 启动后端服务
    backend_process = start_backend_service()
    time.sleep(2)  # 等待后端服务启动
    
    # 启动定时任务
    scheduler_process = start_scheduler()
    time.sleep(1)  # 等待定时任务启动
    
    # 启动前端服务
    frontend_process = start_frontend_service()
    time.sleep(3)  # 等待前端服务启动
    
    print("\n=== 系统启动完成 ===")
    print("后端服务: http://localhost:5000")
    print("前端服务: http://localhost:5173")
    print("\n按 Ctrl+C 停止所有服务")
    
    # 等待用户输入
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n=== 停止所有服务 ===")
        # 停止所有进程
        if 'backend_process' in locals():
            backend_process.terminate()
        if 'scheduler_process' in locals():
            scheduler_process.terminate()
        if 'frontend_process' in locals():
            frontend_process.terminate()
        print("所有服务已停止")

if __name__ == "__main__":
    main()