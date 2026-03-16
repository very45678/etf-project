import unittest
import os
import sys
from data_store import (
    insert_fund, insert_price, insert_nav, insert_yield, insert_alert, insert_error,
    get_funds, get_prices, get_nav, get_yields, get_alerts, get_errors
)

class TestDataStore(unittest.TestCase):
    def test_insert_fund(self):
        """
        测试插入基金信息
        """
        result = insert_fund('000001', '华夏成长混合')
        self.assertTrue(result)
    
    def test_insert_price(self):
        """
        测试插入价格数据
        """
        # 先插入基金信息
        insert_fund('000001', '华夏成长混合')
        # 插入价格数据
        result = insert_price('000001', 1.0, '2023-01-01')
        self.assertTrue(result)
    
    def test_insert_nav(self):
        """
        测试插入净值数据
        """
        # 先插入基金信息
        insert_fund('000001', '华夏成长混合')
        # 插入净值数据
        result = insert_nav('000001', 1.0, '2023-01-01')
        self.assertTrue(result)
    
    def test_insert_yield(self):
        """
        测试插入收益率数据
        """
        # 先插入基金信息
        insert_fund('000001', '华夏成长混合')
        # 插入收益率数据
        result = insert_yield('000001', 0.05, '2023-01-01')
        self.assertTrue(result)
    
    def test_insert_alert(self):
        """
        测试插入提醒记录
        """
        result = insert_alert('000001', '华夏成长混合', 0.05)
        self.assertTrue(result)
    
    def test_insert_error(self):
        """
        测试插入错误记录
        """
        result = insert_error('测试错误', '这是一条测试错误信息')
        self.assertTrue(result)
    
    def test_get_funds(self):
        """
        测试获取基金列表
        """
        # 先插入基金信息
        insert_fund('000001', '华夏成长混合')
        funds = get_funds()
        self.assertGreater(len(funds), 0)
    
    def test_get_prices(self):
        """
        测试获取价格数据
        """
        # 先插入基金信息和价格数据
        insert_fund('000001', '华夏成长混合')
        insert_price('000001', 1.0, '2023-01-01')
        prices = get_prices('000001')
        self.assertGreater(len(prices), 0)
    
    def test_get_nav(self):
        """
        测试获取净值数据
        """
        # 先插入基金信息和净值数据
        insert_fund('000001', '华夏成长混合')
        insert_nav('000001', 1.0, '2023-01-01')
        nav_data = get_nav('000001')
        self.assertGreater(len(nav_data), 0)
    
    def test_get_yields(self):
        """
        测试获取收益率数据
        """
        # 先插入基金信息和收益率数据
        insert_fund('000001', '华夏成长混合')
        insert_yield('000001', 0.05, '2023-01-01')
        yields_data = get_yields('000001')
        self.assertGreater(len(yields_data), 0)
    
    def test_get_alerts(self):
        """
        测试获取提醒记录
        """
        # 先插入提醒记录
        insert_alert('000001', '华夏成长混合', 0.05)
        alerts = get_alerts()
        self.assertGreater(len(alerts), 0)
    
    def test_get_errors(self):
        """
        测试获取错误记录
        """
        # 先插入错误记录
        insert_error('测试错误', '这是一条测试错误信息')
        errors = get_errors()
        self.assertGreater(len(errors), 0)

if __name__ == '__main__':
    unittest.main()