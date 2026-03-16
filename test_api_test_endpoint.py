#!/usr/bin/env python3
# test_api_test_endpoint.py - 测试测试API端点

import requests

print("测试测试API端点...")
try:
    # 测试/api/test端点
    response = requests.get('http://localhost:5000/api/test', timeout=5)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    print("测试API端点测试成功！")
except Exception as e:
    print(f"测试API端点测试失败: {e}")