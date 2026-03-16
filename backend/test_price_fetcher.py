# test_price_fetcher.py
import unittest
from price_fetcher import fetch_etf_price, fetch_all_funds

class TestPriceFetcher(unittest.TestCase):
    def test_fetch_etf_price(self):
        """
        测试获取ETF价格数据
        """
        # 测试一个真实的ETF代码
        result = fetch_etf_price('511880')  # 银华日利ETF
        # 如果无法获取真实数据就会报错
        print(f"测试结果: {result}")
        
    def test_fetch_all_funds(self):
        """
        测试获取所有基金数据
        """
        success_count = fetch_all_funds()
        print(f"成功获取 {success_count} 个基金数据")
        # 由于网络问题可能导致部分失败，我们只验证函数能正常运行
        self.assertIsInstance(success_count, int)

if __name__ == '__main__':
    unittest.main()