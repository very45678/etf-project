import os

# 数据库文件路径
DB_PATH = os.path.join('backend', 'fund_arb.db')

# 写入结果到文件
with open('db_check_result.txt', 'w') as f:
    f.write(f"检查数据库文件: {DB_PATH}\n")
    f.write(f"文件是否存在: {os.path.exists(DB_PATH)}\n")
    f.write(f"当前工作目录: {os.getcwd()}\n")
    f.write(f"backend目录是否存在: {os.path.exists('backend')}\n")
    
    # 列出backend目录下的文件
    if os.path.exists('backend'):
        f.write("backend目录下的文件:\n")
        for file in os.listdir('backend'):
            f.write(f"  - {file}\n")

print("检查完成，结果已写入 db_check_result.txt 文件")