# run_scheduler.py
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(__file__))

from scheduler import main

if __name__ == '__main__':
    print("启动基金数据定时任务调度器...")
    print("价格数据采集：每5分钟执行一次")
    print("净值数据采集：每天9:30执行")
    print("数据清理任务：每天2:00执行")
    print("按 Ctrl+C 停止调度器")
    print("-" * 50)
    
    main()