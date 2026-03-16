# notification.py
import requests
import time
from config import FTQQ_SEND_KEY

def send_ftqq_message(title, content):
    """发送消息到方糖盒子（微信）"""
    send_key = FTQQ_SEND_KEY
    url = f"https://sctapi.ftqq.com/{send_key}.send"
    data = {
        "title": title,
        "desp": content
    }
    
    response = requests.post(url, data=data)
    result = response.json()
    if result.get("code") == 0:
        print("消息发送成功")
        return True
    else:
        print(f"消息发送失败: {result}")
        return False

def send_arb_alert(fund_code, fund_name, buy_yield, sell_yield, buy_price, sell_price, nav):
    """发送套利提醒"""
    title = f"ETF套利提醒 - {fund_name}({fund_code})"
    content = f"""
基金代码: {fund_code}
基金名称: {fund_name}
买入收益率: {buy_yield:.4%}
卖出收益率: {sell_yield:.4%}
买入价格: {buy_price}
卖出价格: {sell_price}
净值: {nav}
发送时间: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
    return send_ftqq_message(title, content)