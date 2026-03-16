from data_store import get_nav

# 获取511880基金的净值数据
navs = get_nav(fund_code='511880', limit=10)
print('511880基金的净值数据:')
for nav in navs:
    print(f'日期: {nav[3]}, 净值: {nav[2]}')