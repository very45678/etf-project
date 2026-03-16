# test_notification.py
import unittest
from notification import send_arb_alert

class TestNotification(unittest.TestCase):
    def test_send_arb_alert(self):
        """测试发送套利提醒"""
        result = send_arb_alert("511880", "银华日利", 0.035, 0.032, 100.01, 99.99, 100.00)
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()