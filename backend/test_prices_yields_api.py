import requests

def test_prices_api():
    """
    测试价格数据API
    """
    try:
        response = requests.get('http://localhost:5000/api/prices')
        print(f"价格数据API响应状态码: {response.status_code}")
        data = response.json()
        print(f"价格数据API响应状态: {data['status']}")
        print(f"价格数据API返回数据条数: {len(data['data'])}")
        if data['data']:
            print(f"价格数据API返回第一条数据: {data['data'][0]}")
    except Exception as e:
        print(f"测试价格数据API失败: {str(e)}")

def test_yields_api():
    """
    测试收益率数据API
    """
    try:
        response = requests.get('http://localhost:5000/api/yields')
        print(f"收益率数据API响应状态码: {response.status_code}")
        data = response.json()
        print(f"收益率数据API响应状态: {data['status']}")
        print(f"收益率数据API返回数据条数: {len(data['data'])}")
        if data['data']:
            print(f"收益率数据API返回第一条数据: {data['data'][0]}")
    except Exception as e:
        print(f"测试收益率数据API失败: {str(e)}")

if __name__ == '__main__':
    print("测试价格数据API:")
    test_prices_api()
    print("\n测试收益率数据API:")
    test_yields_api()