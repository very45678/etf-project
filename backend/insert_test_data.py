import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(__file__))

from data_store import insert_fund

def insert_test_funds():
    """
    插入测试基金数据
    """
    test_funds = [
        ('000001', '华夏成长混合'),
        ('000002', '华夏成长混合A'),
        ('000003', '华夏成长混合B'),
        ('000004', '华夏成长混合C'),
        ('000005', '华夏成长混合D'),
        ('511880', '银华日利ETF'),
        ('511990', '华宝添益ETF'),
        ('511800', '博时货币ETF'),
        ('511850', '工银瑞信货币ETF')
    ]
    
    for fund_code, fund_name in test_funds:
        result = insert_fund(fund_code, fund_name)
        if result:
            print(f"插入基金成功: {fund_code} - {fund_name}")
        else:
            print(f"插入基金失败: {fund_code} - {fund_name}")

if __name__ == '__main__':
    insert_test_funds()
    print("测试数据插入完成")