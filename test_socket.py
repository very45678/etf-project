#!/usr/bin/env python3
# test_socket.py - 测试端口5000是否开放

import socket

try:
    # 创建socket对象
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置超时时间为2秒
    s.settimeout(2)
    # 尝试连接到本地端口5000
    result = s.connect_ex(('localhost', 5000))
    if result == 0:
        print("端口5000开放")
    else:
        print(f"端口5000未开放，错误码: {result}")
    # 关闭连接
    s.close()
except Exception as e:
    print(f"错误: {e}")