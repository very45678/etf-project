import requests

# 检查基金列表
try:
    r = requests.get('http://127.0.0.1:5001/api/funds')
    print('基金列表:', r.json())
except Exception as e:
    print('基金列表API错误:', e)

# 检查价格数据
try:
    r = requests.get('http://127.0.0.1:5001/api/prices?fund_code=511880&limit=1')
    print('价格数据:', r.json())
except Exception as e:
    print('价格API错误:', e)

# 检查净值数据
try:
    r = requests.get('http://127.0.0.1:5001/api/nav?fund_code=511880&limit=1')
    print('净值数据:', r.json())
except Exception as e:
    print('净值API错误:', e)
