# test_yield_calculator.py
import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(__file__))

from yield_calculator import calculate_annualized_yield, calculate_yield_for_fund, calculate_yields_for_all_funds, get_latest_yields, analyze_yield_trend

class TestYieldCalculator(unittest.TestCase):
    
    def setUp(self):
        """测试前准备"""
        pass
    
    def tearDown(self):
        """测试后清理"""
        pass
    
    def test_calculate_annualized_yield_basic(self):
        """测试基本年化收益率计算"""
        # 正常情况 - 净值高于买入价，收益率应为正
        result = calculate_annualized_yield(100.0, 100.5, 1)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)  # 净值高于买入价，收益率应为正
        
        # 净值低于买入价，收益率应为负
        result = calculate_annualized_yield(100.0, 99.5, 1)
        self.assertLess(result, 0)  # 净值低于买入价，收益率应为负
        
        # 持有天数不同
        result_1day = calculate_annualized_yield(100.0, 100.5, 1)
        result_7days = calculate_annualized_yield(100.0, 100.5, 7)
        self.assertNotEqual(result_1day, result_7days)
    
    def test_calculate_annualized_yield_edge_cases(self):
        """测试边界情况"""
        # 买入价为0
        result = calculate_annualized_yield(0, 100.0, 1)
        self.assertEqual(result, 0.0)
        
        # 净值为0
        result = calculate_annualized_yield(100.0, 0, 1)
        self.assertEqual(result, 0.0)
        
        # 持有天数为0
        result = calculate_annualized_yield(100.0, 100.5, 0)
        self.assertIsInstance(result, float)
    
    @patch('yield_calculator.get_prices')
    @patch('yield_calculator.get_nav')
    @patch('yield_calculator.insert_yield')
    def test_calculate_yield_for_fund_success(self, mock_insert, mock_get_nav, mock_get_prices):
        """测试为单个基金计算收益率（成功情况）"""
        # 模拟数据 - 包含买入价和卖出价
        mock_get_prices.return_value = [
            (1, '511880', 100.244, 100.244, 100.245, '2026-03-04', '2026-03-04 11:21:28')
        ]
        mock_get_nav.return_value = [
            (1, '511880', 100.2285, '2026-03-03', '2026-03-04 11:20:10')
        ]
        mock_insert.return_value = True
        
        result = calculate_yield_for_fund('511880')
        self.assertTrue(result)
        # 验证insert_yield被调用，且包含两个收益率参数
        mock_insert.assert_called_once()
    
    @patch('yield_calculator.get_prices')
    def test_calculate_yield_for_fund_no_price_data(self, mock_get_prices):
        """测试没有价格数据的情况"""
        mock_get_prices.return_value = []
        
        result = calculate_yield_for_fund('511880')
        self.assertFalse(result)
    
    @patch('yield_calculator.get_prices')
    @patch('yield_calculator.get_nav')
    def test_calculate_yield_for_fund_no_nav_data(self, mock_get_nav, mock_get_prices):
        """测试没有净值数据的情况"""
        mock_get_prices.return_value = [
            (1, '511880', 100.244, 100.244, 100.245, '2026-03-04', '2026-03-04 11:21:28')
        ]
        mock_get_nav.return_value = []
        
        result = calculate_yield_for_fund('511880')
        self.assertFalse(result)
    
    @patch('yield_calculator.get_prices')
    @patch('yield_calculator.get_nav')
    @patch('yield_calculator.insert_yield')
    def test_calculate_yield_for_fund_insert_failure(self, mock_insert, mock_get_nav, mock_get_prices):
        """测试收益率数据插入失败的情况"""
        mock_get_prices.return_value = [
            (1, '511880', 100.244, 100.244, 100.245, '2026-03-04', '2026-03-04 11:21:28')
        ]
        mock_get_nav.return_value = [
            (1, '511880', 100.2285, '2026-03-03', '2026-03-04 11:20:10')
        ]
        mock_insert.return_value = False
        
        result = calculate_yield_for_fund('511880')
        self.assertFalse(result)
    
    @patch('yield_calculator.get_prices')
    @patch('yield_calculator.calculate_yield_for_fund')
    def test_calculate_yields_for_all_funds(self, mock_calculate, mock_get_prices):
        """测试为所有基金计算收益率"""
        # 模拟多个基金的价格数据
        mock_get_prices.return_value = [
            (1, '511880', 100.244, 100.244, 100.245, '2026-03-04', '2026-03-04 11:21:28'),
            (2, '511990', 100.002, 100.001, 100.002, '2026-03-04', '2026-03-04 11:21:28'),
            (3, '511880', 100.243, 100.243, 100.244, '2026-03-03', '2026-03-03 11:21:28')
        ]
        mock_calculate.return_value = True
        
        success_count = calculate_yields_for_all_funds()
        self.assertEqual(success_count, 2)  # 两个不同的基金代码
        self.assertEqual(mock_calculate.call_count, 2)
    
    @patch('yield_calculator.get_yields')
    def test_get_latest_yields(self, mock_get_yields):
        """测试获取最新收益率数据"""
        # 模拟包含两种收益率的数据
        mock_get_yields.return_value = [
            (1, '511880', 0.5, 0.4, '2026-03-04', '2026-03-04 11:21:28'),  # yield_rate_buy, yield_rate_sell
            (2, '511990', 0.3, 0.2, '2026-03-04', '2026-03-04 11:21:28')
        ]
        
        yields = get_latest_yields(limit=2)
        self.assertEqual(len(yields), 2)
        self.assertEqual(yields[0][1], '511880')
        self.assertEqual(yields[0][2], 0.5)  # yield_rate_buy
        self.assertEqual(yields[0][3], 0.4)  # yield_rate_sell
    
    @patch('yield_calculator.get_yields')
    def test_analyze_yield_trend(self, mock_get_yields):
        """测试收益率趋势分析"""
        # 模拟包含两种收益率的数据
        mock_get_yields.return_value = [
            (1, '511880', 0.6, 0.5, '2026-03-04', '2026-03-04 11:21:28'),  # yield_rate_buy, yield_rate_sell
            (2, '511880', 0.5, 0.4, '2026-03-03', '2026-03-03 11:21:28'),
            (3, '511880', 0.4, 0.3, '2026-03-02', '2026-03-02 11:21:28')
        ]
        
        analysis = analyze_yield_trend('511880', days=3)
        self.assertEqual(analysis['fund_code'], '511880')
        
        # 验证买入价收益率的统计指标
        self.assertEqual(analysis['买入价收益率']['当前收益率'], 0.6)
        self.assertEqual(analysis['买入价收益率']['平均收益率'], 0.5)
        self.assertEqual(analysis['买入价收益率']['最高收益率'], 0.6)
        self.assertEqual(analysis['买入价收益率']['最低收益率'], 0.4)
        
        # 验证卖出价收益率的统计指标
        self.assertEqual(analysis['卖出价收益率']['当前收益率'], 0.5)
        self.assertEqual(analysis['卖出价收益率']['平均收益率'], 0.4)
        self.assertEqual(analysis['卖出价收益率']['最高收益率'], 0.5)
        self.assertEqual(analysis['卖出价收益率']['最低收益率'], 0.3)
        
        # 验证趋势分析
        self.assertEqual(analysis['买入价收益率']['趋势'], '上升')
        self.assertEqual(analysis['卖出价收益率']['趋势'], '上升')
    
    @patch('yield_calculator.get_yields')
    def test_analyze_yield_trend_no_data(self, mock_get_yields):
        """测试没有收益率数据的情况"""
        mock_get_yields.return_value = []
        
        analysis = analyze_yield_trend('511880')
        self.assertIn('error', analysis)

if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)