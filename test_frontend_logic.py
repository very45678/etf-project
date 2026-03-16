import json

# 模拟后端返回的数据
nav_data = {
    "data": [
        {"fund_code": "511880", "nav": 1.0000, "nav_date": "2026-03-12"},
        {"fund_code": "511990", "nav": 1.0000, "nav_date": "2026-03-12"}
    ]
}

prices_data = {
    "data": [
        {"fund_code": "511880", "buy_price": 1.0001, "sell_price": 0.9999, "price_date": "2026-03-12"},
        {"fund_code": "511990", "buy_price": 1.0002, "sell_price": 0.9998, "price_date": "2026-03-12"}
    ]
}

yields_data = {
    "data": [
        {"fund_code": "511880", "yield_rate_buy": 2.0598, "yield_rate_sell": 2.4321, "yield_date": "2026-03-12"},
        {"fund_code": "511990", "yield_rate_buy": 0.3657, "yield_rate_sell": 0.0, "yield_date": "2026-03-12"}
    ]
}

# 模拟前端的selectedFunds数组
selectedFunds = ['511880', '511990']

# 模拟前端的数据处理逻辑
def simulate_frontend_logic():
    # 过滤只显示指定的基金
    filteredNav = [nav for nav in nav_data['data'] if nav['fund_code'] in selectedFunds]
    filteredPrices = [price for price in prices_data['data'] if price['fund_code'] in selectedFunds]
    filteredYields = [yieldData for yieldData in yields_data['data'] if yieldData['fund_code'] in selectedFunds]
    
    # 整合数据
    overview = []
    for fundCode in selectedFunds:
        # 找到最新的净值数据
        nav = None
        for n in filteredNav:
            if n['fund_code'] == fundCode:
                nav = n
                break
        
        # 找到最新的价格数据
        price = None
        for p in filteredPrices:
            if p['fund_code'] == fundCode:
                price = p
                break
        
        # 找到最新的收益率数据
        yieldData = None
        for y in filteredYields:
            if y['fund_code'] == fundCode:
                yieldData = y
                break
        
        # 构建综合数据
        overview.append({
            'fund_code': fundCode,
            'nav': nav['nav'] if nav else '-',
            'buy_price': price['buy_price'] if price else '-',
            'yield_rate_buy': yieldData['yield_rate_buy'] if yieldData else '-',
            'sell_price': price['sell_price'] if price else '-',
            'yield_rate_sell': yieldData['yield_rate_sell'] if yieldData else '-'
        })
    
    return overview

# 运行模拟
result = simulate_frontend_logic()
print("模拟前端数据处理结果:")
print(json.dumps(result, indent=2, ensure_ascii=False))