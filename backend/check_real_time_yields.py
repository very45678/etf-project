import requests
import time

# 测试收益率数据的实时更新
def test_real_time_yields():
    print("开始测试收益率数据的实时更新...")
    
    # 第一次获取数据
    response = requests.get('http://localhost:5000/api/yields')
    if response.status_code == 200:
        try:
            result1 = response.json()
            if result1["status"] == "success":
                data1 = result1["data"]
                print("第一次获取的收益率数据:")
                for fund in data1[:4]:  # 只显示最新的4条数据
                    print(f'基金代码: {fund["fund_code"]}, 买入收益率: {fund["yield_rate_buy"]:.4f}%, 卖出收益率: {fund["yield_rate_sell"]:.4f}%, 日期: {fund["yield_date"]}')
                
                # 等待一段时间后再次获取
                print("\n等待30秒后再次获取数据...")
                time.sleep(30)
                
                response2 = requests.get('http://localhost:5000/api/yields')
                if response2.status_code == 200:
                    result2 = response2.json()
                    if result2["status"] == "success":
                        data2 = result2["data"]
                        print("\n第二次获取的收益率数据:")
                        for fund in data2[:4]:  # 只显示最新的4条数据
                            print(f'基金代码: {fund["fund_code"]}, 买入收益率: {fund["yield_rate_buy"]:.4f}%, 卖出收益率: {fund["yield_rate_sell"]:.4f}%, 日期: {fund["yield_date"]}')
                        
                        # 比较两次数据
                        print("\n数据更新情况:")
                        # 创建基金代码到收益率数据的映射
                        fund_map1 = {fund["fund_code"]: (fund["yield_rate_buy"], fund["yield_rate_sell"]) for fund in data1[:4]}
                        fund_map2 = {fund["fund_code"]: (fund["yield_rate_buy"], fund["yield_rate_sell"]) for fund in data2[:4]}
                        
                        for fund_code in fund_map1:
                            if fund_code in fund_map2:
                                if fund_map1[fund_code] != fund_map2[fund_code]:
                                    print(f'基金 {fund_code} 收益率数据已更新')
                                else:
                                    print(f'基金 {fund_code} 收益率数据未更新')
                            else:
                                print(f'基金 {fund_code} 未在第二次数据中找到')
                    else:
                        print("第二次获取数据失败: 响应状态不是success")
                else:
                    print(f"第二次获取数据失败: {response2.status_code}")
            else:
                print("第一次获取数据失败: 响应状态不是success")
        except Exception as e:
            print(f"解析JSON失败: {e}")
    else:
        print(f"获取数据失败: {response.status_code}")

if __name__ == "__main__":
    test_real_time_yields()