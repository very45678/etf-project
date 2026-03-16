import requests

# 测试测试API端点
print("测试 /api/test 端点")
try:
    response = requests.get('http://localhost:5000/api/test', timeout=5)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
except Exception as e:
    print(f"错误: {e}")