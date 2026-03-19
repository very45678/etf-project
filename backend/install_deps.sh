#!/bin/bash
# PythonAnywhere 依赖安装脚本

echo "开始安装依赖..."

pip install --user \
    Flask==3.0.0 \
    flask-cors==4.0.0 \
    apscheduler==3.10.4 \
    requests==2.31.0 \
    beautifulsoup4==4.12.2 \
    lxml==4.9.3 \
    akshare==1.16.72 \
    pandas==2.1.4 \
    numpy==1.26.4

echo "依赖安装完成！"
