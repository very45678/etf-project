#!/usr/bin/env python3
# test_api_simple.py - 简单测试API是否可以访问

import requests

print("测试后端API...")
try:
    # 测试/api/funds端点
    response = requests.get('http://localhost:5001/api/funds', timeout=5)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    print("API测试成功！")
except Exception as e:
    print(f"API测试失败: {e}")