import requests

# 检查最新的收益率数据
def check_latest_yields():
    print("检查最新的收益率数据...")
    
    response = requests.get('http://localhost:5000/api/yields')
    if response.status_code == 200:
        result = response.json()
        if result['status'] == 'success':
            data = result['data']
            print('最新收益率数据:')
            for fund in data[:4]:  # 只显示最新的4条数据
                print(f'基金代码: {fund["fund_code"]}, 买入收益率: {fund["yield_rate_buy"]:.4f}%, 卖出收益率: {fund["yield_rate_sell"]:.4f}%, 日期: {fund["yield_date"]}')
        else:
            print("获取数据失败: 响应状态不是success")
    else:
        print(f"获取数据失败: {response.status_code}")

if __name__ == "__main__":
    check_latest_yields()