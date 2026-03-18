import akshare as ak
import datetime

# 获取开放式基金数据
df = ak.fund_open_fund_daily_em()
row = df[df['基金代码'] == '511880'].iloc[0]

print("基金代码:", row['基金代码'])
print("基金简称:", row['基金简称'])
print("\n净值相关字段:")
for col in df.columns:
    if '净值' in col:
        print(f"  {col}: {row[col]}")

print("\n今天日期:", datetime.date.today().strftime('%Y-%m-%d'))
