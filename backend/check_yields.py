import sqlite3
import os

# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'fund_arb.db')

# 连接数据库
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row  # 使用Row对象，可以通过字段名访问
cursor = conn.cursor()

# 查询511880基金的收益率数据
print('511880基金的收益率数据:')
cursor.execute('SELECT * FROM yields WHERE fund_code = ? ORDER BY yield_date DESC, id DESC LIMIT 10', ('511880',))
yields = cursor.fetchall()
for yield_data in yields:
    print('ID: {}, 日期: {}, 收益率: {}, 买入收益率: {}, 卖出收益率: {}'.format(
        yield_data['id'], yield_data['yield_date'], yield_data['yield_rate'],
        yield_data['yield_rate_buy'], yield_data['yield_rate_sell']
    ))

# 关闭连接
conn.close()