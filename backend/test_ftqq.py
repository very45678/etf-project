# test_ftqq.py
from notification import send_ftqq_message

def test_ftqq_message():
    """测试方糖消息发送"""
    try:
        title = "测试消息"
        content = "这是一条测试消息，用于验证方糖配置是否正确。"
        success = send_ftqq_message(title, content)
        if success:
            print("方糖消息发送成功！")
        else:
            print("方糖消息发送失败！")
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    test_ftqq_message()