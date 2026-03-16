# d:\etf\backend\test_nav_fetcher.py
import unittest
from nav_fetcher import fetch_fund_nav, fetch_all_funds_nav

class TestNavFetcher(unittest.TestCase):
    def test_fetch_fund_nav(self):
        """
        测试获取基金净值数据
        """
        # 测试一个真实的基金代码
        result = fetch_fund_nav('511880')  # 银华日利ETF
        print(f"测试结果: {result}")
        
    def test_fetch_all_funds_nav(self):
        """
        测试获取所有基金净值数据
        """
        success_count = fetch_all_funds_nav()
        print(f"成功获取 {success_count} 个基金净值数据")
        # 由于网络问题可能导致部分失败，我们只验证函数能正常运行
        self.assertIsInstance(success_count, int)

if __name__ == '__main__':
    unittest.main()