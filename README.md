# 货币基金套利提示系统

## 项目简介
本项目是一个用于监控银华日利（511880）和华宝添益（511990）两支货币基金套利机会的系统。通过定时采集价格和净值数据，计算年化收益率，并在收益率达到设定阈值（1.5%）时通过方糖盒子（Server酱）发送提醒。

## 功能特性
- **实时监控**：每5分钟采集一次价格数据。
- **自动计算**：自动计算买入和卖出价格的年化收益率。
- **套利提醒**：当年化收益率 >= 1.5% 时，通过微信（方糖盒子）发送通知。
- **数据展示**：提供Web界面展示实时数据、历史记录和错误日志。
- **自动维护**：每日自动清理5天前的过期数据。

## 技术栈
- **前端**：Vue 3 + Element Plus + Vite
- **后端**：Python + Flask + SQLite
- **调度**：APScheduler
- **通知**：ServerChan (方糖盒子)

## 安装说明

### 前置条件
- Python 3.9+
- Node.js 16+
- Git

### 1. 克隆项目
```bash
git clone <repository_url>
cd etf
```

### 2. 初始化后端
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
# source venv/bin/activate

pip install -r requirements.txt
```
*(如果没有 requirements.txt，可以手动安装依赖: flask flask-cors apscheduler requests beautifulsoup4 lxml akshare)*

### 3. 初始化前端
```bash
cd frontend
npm install
```

## 使用说明

### 一键启动 (Windows)
在项目根目录下双击运行 `start_system.bat`。

### 手动启动

1. **启动后端 API**
```bash
cd backend
venv\Scripts\activate
python api.py
```
API 服务将运行在 `http://localhost:5001`

2. **启动调度器**
```bash
cd backend
venv\Scripts\activate
python run_scheduler.py
```
调度器将在后台运行，负责数据采集和计算。

3. **启动前端**
```bash
cd frontend
npm run dev
```
前端页面将运行在 `http://localhost:5173`

## 配置说明
- **通知配置**：修改 `backend/config.py` 中的 `FTQQ_SEND_KEY` 为你的方糖盒子 SendKey。
- **数据库**：数据存储在 `backend/fund_arb.db` (SQLite)。

## 维护说明
- **日志**：后端日志文件位于 `backend/scheduler.log`。
- **数据清理**：系统每天凌晨 2:00 自动清理 5 天前的数据。
- **错误排查**：可以通过前端界面的"错误记录"查看系统运行错误。

## API 文档
- `GET /api/funds`: 获取基金列表
- `GET /api/prices`: 获取价格数据
- `GET /api/nav`: 获取净值数据
- `GET /api/yields`: 获取收益率数据
- `GET /api/alerts`: 获取提醒记录
- `GET /api/errors`: 获取错误记录
