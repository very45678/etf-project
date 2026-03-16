#!/usr/bin/env python3
# test_port_and_api.py - 测试端口5000是否开放，以及API是否可以访问

import socket
import requests

def test_port():
    """测试端口5000是否开放"""
    print("测试端口5000是否开放...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        result = s.connect_ex(('localhost', 5000))
        if result == 0:
            print("端口5000已开放")
        else:
            print(f"端口5000未开放，错误码: {result}")
        s.close()
        return result == 0
    except Exception as e:
        print(f"测试端口失败: {e}")
        return False

def test_api():
    """测试API是否可以访问"""
    print("测试API是否可以访问...")
    try:
        response = requests.get('http://localhost:5000/api/funds', timeout=5)
        print(f"API响应状态码: {response.status_code}")
        print(f"API响应内容: {response.json()}")
        return True
    except Exception as e:
        print(f"测试API失败: {e}")
        return False

if __name__ == "__main__":
    print("开始测试...")
    port_open = test_port()
    if port_open:
        test_api()
    print("测试完成")