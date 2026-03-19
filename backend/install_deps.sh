#!/bin/bash
# PythonAnywhere 依赖安装脚本

echo "开始安装依赖..."

pip install --user \
    Flask==3.0.0 \
    flask-cors==4.0.0 \
    apscheduler==3.10.4 \
    requests==2.31.0 \
    beautifulsoup4==4.12.2 \
    Werkzeug==3.0.1

echo "依赖安装完成！"
