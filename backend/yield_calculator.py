# yield_calculator.py
import logging
from datetime import datetime, timedelta
from data_store import get_prices, get_nav, insert_yield, get_yields, get_funds
from notification import send_arb_alert

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('yield_calculator')

def calculate_annualized_yield(buy_price, nav, days_held=1):
    """
    计算年化收益率（基于买入价格和赎回净值）
    :param buy_price: 买入价格
    :param nav: 赎回净值
    :param days_held: 持有天数
    :return: 年化收益率（百分比）
    """
    try:
        if buy_price <= 0:
            logger.warning(f"买入价格无效: {buy_price}")
            return 0.0
        if nav <= 0:
            logger.warning(f"净值数据无效: {nav}")
            return 0.0
        
        # 计算单期收益率：使用实际的净值数据，不考虑滞后情况
        # 正常情况：赎回净值相对于买入价格的收益率
        single_period_yield = (nav - buy_price) / buy_price
        
        # 计算年化收益率
        if days_held > 0:
            annualized_yield = (1 + single_period_yield) ** (365 / days_held) - 1
        else:
            annualized_yield = single_period_yield
        
        # 转换为百分比
        annualized_yield_percent = annualized_yield * 100
        logger.info(f"计算年化收益率: 买入价={buy_price}, 净值={nav}, 持有天数={days_held}, 年化收益率={annualized_yield_percent:.4f}%")
        
        return annualized_yield_percent
    except Exception as e:
        logger.error(f"计算年化收益率失败: {e}")
        return 0.0

def calculate_yield_for_fund(fund_code, price_date=None):
    """
    为指定基金计算两种买入方式的收益率
    :param fund_code: 基金代码
    :param price_date: 价格日期（默认为最新日期）
    :return: 是否计算成功
    """
    try:
        logger.info(f"开始为基金 {fund_code} 计算两种买入方式的收益率")
        
        # 获取最新的价格数据
        prices = get_prices(fund_code=fund_code, limit=1)
        if not prices:
            logger.warning(f"未找到基金 {fund_code} 的价格数据")
            return False
        
        latest_price = prices[0]
        buy_price = latest_price[3] if latest_price[3] else latest_price[2]  # 买入价，如果没有则用最新价
        sell_price = latest_price[4] if latest_price[4] else latest_price[2]  # 卖出价，如果没有则用最新价
        price_date = latest_price[5]   # price_date字段
        
        # 获取对应日期的净值数据
        nav_data = get_nav(fund_code=fund_code, limit=10)
        if not nav_data:
            logger.warning(f"未找到基金 {fund_code} 的净值数据")
            return False
        
        # 查找与价格日期匹配的净值数据
        target_nav = None
        for nav in nav_data:
            nav_date = nav[3]  # nav_date字段
            if nav_date == price_date:
                target_nav = nav
                break
        
        # 如果没有完全匹配的日期，使用最新的净值数据
        if not target_nav:
            target_nav = nav_data[0]
            logger.info(f"使用最新净值数据计算收益率: {target_nav[3]}")
        
        nav_value = target_nav[2]  # nav字段
        nav_date = target_nav[3]   # nav_date字段
        
        # 计算持有天数（考虑节假日和周末）
        try:
            price_dt = datetime.strptime(price_date, '%Y-%m-%d')
            nav_dt = datetime.strptime(nav_date, '%Y-%m-%d')
            
            # 计算实际天数差
            days_held = abs((nav_dt - price_dt).days)
            
            # 对于ETF基金，净值数据通常滞后一天，所以需要调整持有天数
            if fund_code == '511880':
                # 如果价格日期是交易日，而净值日期是前一天，持有天数应为1
                if days_held == 1:
                    days_held = 1
                # 如果是周末，需要调整持有天数
                price_weekday = price_dt.weekday()  # 0=周一, 6=周日
                nav_weekday = nav_dt.weekday()  # 0=周一, 6=周日
                
                # 周一的价格，使用周五的净值，持有天数应为3天（周末）
                if price_weekday == 0 and nav_weekday == 4:
                    days_held = 3
                # 其他情况，默认持有1天
                else:
                    days_held = 1
            else:
                # 对于其他基金，使用原来的逻辑
                # 检查价格日期是星期几
                price_weekday = price_dt.weekday()  # 0=周一, 6=周日
                
                # 周五：默认持有3天（周五、周六、周日）
                if price_weekday == 4:  # 周五
                    days_held = 3
                # 周六：默认持有2天（周六、周日）
                elif price_weekday == 5:  # 周六
                    days_held = 2
                # 周日：默认持有1天（周日）
                elif price_weekday == 6:  # 周日
                    days_held = 1
                # 工作日：默认持有1天
                else:
                    days_held = 1
        except Exception:
            days_held = 1  # 日期解析失败时默认持有1天
        
        # 计算两种买入方式的年化收益率
        yield_rate_buy = calculate_annualized_yield(buy_price, nav_value, days_held)  # 以买入价买入
        yield_rate_sell = calculate_annualized_yield(sell_price, nav_value, days_held)  # 以卖出价买入
        
        # 存储两种收益率数据
        success = insert_yield(fund_code, yield_rate_buy, yield_rate_sell, price_date)
        if success:
            logger.info(f"基金 {fund_code} 收益率计算完成: 买入价收益率={yield_rate_buy:.4f}%, 卖出价收益率={yield_rate_sell:.4f}%")
            
            # 检查套利机会并发送通知
            check_arb_opportunity(fund_code, yield_rate_buy, yield_rate_sell, buy_price, sell_price, nav_value)
            
            return True
        else:
            logger.error(f"存储基金 {fund_code} 收益率数据失败")
            return False
            
    except Exception as e:
        logger.error(f"为基金 {fund_code} 计算收益率失败: {e}")
        return False

def calculate_yields_for_all_funds():
    """
    为所有基金计算收益率
    :return: 成功计算的基金数量
    """
    try:
        logger.info("开始为所有基金计算收益率")
        
        # 只计算目标基金的收益率
        target_funds = ['511880', '511990']
        
        # 获取所有基金代码（从价格数据中获取）
        prices = get_prices(limit=100)
        if not prices:
            logger.warning("未找到任何价格数据")
            return 0
        
        # 提取唯一的基金代码并过滤出目标基金
        fund_codes = list(set([price[1] for price in prices if price[1] in target_funds]))
        
        success_count = 0
        for fund_code in fund_codes:
            if calculate_yield_for_fund(fund_code):
                success_count += 1
        
        logger.info(f"收益率计算完成，成功计算 {success_count}/{len(fund_codes)} 只基金")
        return success_count
        
    except Exception as e:
        logger.error(f"为所有基金计算收益率失败: {e}")
        return 0

def get_latest_yields(fund_code=None, limit=10):
    """
    获取最新的收益率数据
    :param fund_code: 基金代码，None表示所有基金
    :param limit: 返回数据条数
    :return: 收益率数据列表
    """
    try:
        yields_data = get_yields(fund_code=fund_code, limit=limit)
        return yields_data
    except Exception as e:
        logger.error(f"获取收益率数据失败: {e}")
        return []

def analyze_yield_trend(fund_code, days=30):
    """
    分析收益率趋势
    :param fund_code: 基金代码
    :param days: 分析天数
    :return: 趋势分析结果
    """
    try:
        yields_data = get_yields(fund_code=fund_code, limit=days)
        if not yields_data:
            return {"error": "未找到收益率数据"}
        
        # 调试：打印第一条数据的字段结构
        if yields_data:
            logger.info(f"基金 {fund_code} 收益率数据字段结构:")
            for i, field in enumerate(yields_data[0]):
                logger.info(f"  索引 {i}: {field} (类型: {type(field)})")
        
        # 提取收益率数据
        yield_rates = []
        
        for yield_data in yields_data:
            try:
                # 直接使用索引2访问收益率数据
                yield_rate = float(yield_data[2])
                yield_rates.append(yield_rate)
            except (ValueError, IndexError) as e:
                logger.error(f"无法解析收益率数据: {e}")
                continue
        
        if not yield_rates:
            return {"error": "无法解析任何收益率数据"}
        
        # 计算收益率的统计指标
        current_yield = yield_rates[0] if yield_rates else 0
        avg_yield = sum(yield_rates) / len(yield_rates) if yield_rates else 0
        max_yield = max(yield_rates) if yield_rates else 0
        min_yield = min(yield_rates) if yield_rates else 0
        
        # 判断收益率趋势
        if len(yield_rates) >= 2:
            trend = "上升" if yield_rates[0] > yield_rates[1] else "下降"
        else:
            trend = "稳定"
        
        return {
            "fund_code": fund_code,
            "current_yield": current_yield,
            "avg_yield": avg_yield,
            "max_yield": max_yield,
            "min_yield": min_yield,
            "trend": trend,
            "data_points": len(yield_rates)
        }
    except Exception as e:
        logger.error(f"分析收益率趋势失败: {e}")
        return {"error": str(e)}

def check_arb_opportunity(fund_code, buy_yield, sell_yield, buy_price, sell_price, nav):
    """
    检查套利机会并发送通知
    :param fund_code: 基金代码
    :param buy_yield: 买入价收益率
    :param sell_yield: 卖出价收益率
    :param buy_price: 买入价格
    :param sell_price: 卖出价格
    :param nav: 净值
    :return: 是否存在套利机会
    """
    try:
        # 套利阈值（年化收益率）
        ARB_THRESHOLD = 1.0  # 1%以上的年化收益率认为有套利机会
        
        # 获取基金名称
        funds = get_funds(fund_code=fund_code)
        fund_name = funds[0][2] if funds else fund_code
        
        # 检查是否存在套利机会
        if buy_yield > ARB_THRESHOLD or sell_yield > ARB_THRESHOLD:
            logger.info(f"发现套利机会: 基金 {fund_name}({fund_code})，买入收益率={buy_yield:.4f}%，卖出收益率={sell_yield:.4f}%")
            
            # 发送套利提醒
            send_arb_alert(fund_code, fund_name, buy_yield, sell_yield, buy_price, sell_price, nav)
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"检查套利机会失败: {e}")
        return False

def check_arb_opportunities_for_all_funds():
    """
    检查所有基金的套利机会
    :return: 发现套利机会的基金数量
    """
    try:
        logger.info("开始检查所有基金的套利机会")
        
        # 只检查目标基金
        target_funds = ['511880', '511990']
        
        # 获取所有基金代码
        funds = get_funds()
        if not funds:
            logger.warning("未找到任何基金数据")
            return 0
        
        arb_count = 0
        for fund in funds:
            fund_code = fund[1]
            if fund_code not in target_funds:
                continue
                
            # 获取最新的收益率数据
            yields = get_yields(fund_code=fund_code, limit=1)
            if yields:
                yield_data = yields[0]
                try:
                    buy_yield = float(yield_data[2])
                    sell_yield = float(yield_data[3])
                    
                    # 获取最新的价格和净值数据
                    prices = get_prices(fund_code=fund_code, limit=1)
                    nav_data = get_nav(fund_code=fund_code, limit=1)
                    
                    if prices and nav_data:
                        price_data = prices[0]
                        nav_value = nav_data[0][2]
                        buy_price = price_data[3] if price_data[3] else price_data[2]
                        sell_price = price_data[4] if price_data[4] else price_data[2]
                        
                        if check_arb_opportunity(fund_code, buy_yield, sell_yield, buy_price, sell_price, nav_value):
                            arb_count += 1
                except (ValueError, IndexError) as e:
                    logger.error(f"解析基金 {fund_code} 数据失败: {e}")
        
        logger.info(f"套利机会检查完成，发现 {arb_count} 只基金存在套利机会")
        return arb_count
    except Exception as e:
        logger.error(f"检查所有基金套利机会失败: {e}")
        return 0