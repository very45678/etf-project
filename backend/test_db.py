import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(__file__))

from data_store import get_funds

def test_get_funds():
    """
    测试get_funds函数
    """
    try:
        funds = get_funds()
        print(f"获取到的基金数量: {len(funds)}")
        for fund in funds:
            print(f"基金: {fund}")
    except Exception as e:
        print(f"测试get_funds失败: {str(e)}")

if __name__ == '__main__':
    test_get_funds()