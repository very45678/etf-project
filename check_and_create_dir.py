#!/usr/bin/env python3
# check_and_create_dir.py - 检查并创建backend目录

import os
import sys

# 打印当前工作目录
print(f"当前工作目录: {os.getcwd()}")

# 检查backend目录是否存在
backend_dir = 'backend'
print(f"检查backend目录是否存在: {os.path.exists(backend_dir)}")

# 尝试创建backend目录
if not os.path.exists(backend_dir):
    print(f"创建backend目录...")
    try:
        os.makedirs(backend_dir)
        print(f"成功创建backend目录: {backend_dir}")
    except Exception as e:
        print(f"创建backend目录失败: {e}")
        sys.exit(1)
else:
    print(f"backend目录已存在: {backend_dir}")

# 检查backend目录的权限
print(f"backend目录权限: {oct(os.stat(backend_dir).st_mode)[-3:]}")

# 尝试在backend目录中创建一个测试文件
test_file = os.path.join(backend_dir, 'test.txt')
print(f"尝试创建测试文件: {test_file}")
try:
    with open(test_file, 'w') as f:
        f.write('test')
    print(f"成功创建测试文件: {test_file}")
    os.remove(test_file)
    print(f"成功删除测试文件: {test_file}")
except Exception as e:
    print(f"创建测试文件失败: {e}")
    sys.exit(1)

print("检查完成，backend目录可正常访问和写入！")