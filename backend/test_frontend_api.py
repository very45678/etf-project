import requests

# 测试API调用
print('测试API调用 - 获取511880基金的收益率数据')
response = requests.get('http://localhost:5000/api/yields', params={'fund_code': '511880', 'limit': 5})

if response.status_code == 200:
    data = response.json()
    print('API调用成功')
    print('状态:', data['status'])
    print('消息:', data['message'])
    print('数据数量:', len(data['data']))
    print('\n第一条数据:')
    if data['data']:
        first_item = data['data'][0]
        print(f'基金代码: {first_item["fund_code"]}')
        print(f'收益率: {first_item["yield_rate"]:.4f}%')
        print(f'买入收益率: {first_item["yield_rate_buy"]:.4f}%')
        print(f'卖出收益率: {first_item["yield_rate_sell"]:.4f}%')
        print(f'日期: {first_item["yield_date"]}')
else:
    print('API调用失败')
    print('状态码:', response.status_code)
    print('响应内容:', response.text)