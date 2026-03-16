# check_511880_prices.py
import requests

# 获取511880基金的价格数据
response = requests.get('http://localhost:5000/api/prices?fund_code=511880')
data = response.json()

print('最新价格数据:')
for item in data['data'][:5]:  # 只显示前5条数据
    print(item)