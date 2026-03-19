"""
WSGI 配置文件 - 用于 PythonAnywhere 部署
"""
import sys
import os

# 添加项目路径
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

# 设置环境变量
os.environ['FLASK_ENV'] = 'production'

# 导入 Flask 应用
from api import app as application
