# 货币基金套利提示系统 - 项目总结

## 项目概述

**项目名称**: 货币基金套利提示系统  
**项目目标**: 监控银华日利（511880）和华宝添益（511990）的买入赎回收益率，及时提醒套利机会  
**技术栈**: Vue.js 3 + Vite + Element Plus + Python + FastAPI + SQLite  
**部署平台**: PythonAnywhere（免费版）+ Vercel（前端）

---

## 核心功能

### 1. 数据采集
- **价格数据**: 每5分钟采集一次ETF的买一/卖一价格
- **净值数据**: 每天9:30采集基金净值（511990使用固定净值100）
- **数据来源**: 腾讯财经接口（稳定可靠）

### 2. 收益率计算
- **计算公式**: `[(净值 - 价格) / 价格] × 365 × 100%`
- **计算频率**: 每10分钟计算一次
- **显示精度**: 保留2位小数

### 3. 套利提醒
- **提醒阈值**: 年化收益率 ≥ 1.5%
- **提醒方式**: 企业微信机器人
- **检查频率**: 交易时段（9:30-15:00）每15分钟检查一次

### 4. 数据展示
- **综合数据**: 显示净值、买入/卖出价格、收益率、价格日期
- **历史趋势**: 支持查看历史价格和收益率走势
- **提醒记录**: 记录所有套利提醒
- **错误日志**: 记录数据采集和处理错误

---

## 技术架构

### 后端架构
```
backend/
├── api.py              # Flask API 主入口
├── wsgi.py             # WSGI 配置（PythonAnywhere）
├── data_store.py       # 数据库操作
├── price_fetcher.py    # 价格数据采集（腾讯接口）
├── nav_fetcher.py      # 净值数据采集
├── yield_calculator.py # 收益率计算
├── scheduler.py        # 定时任务调度
├── notification.py     # 企业微信通知
└── fund_arb.db         # SQLite 数据库
```

### 前端架构
```
frontend/
├── src/
│   ├── App.vue         # 主应用组件
│   └── main.js         # 入口文件
├── index.html
└── vite.config.js
```

### 数据库表结构
- **funds**: 基金信息表
- **prices**: 价格数据表（含买一/卖一价格）
- **navs**: 净值数据表
- **yields**: 收益率数据表
- **alerts**: 提醒记录表
- **errors**: 错误记录表

---

## 关键技术点

### 1. 数据采集优化
**问题**: AKShare 在 PythonAnywhere 上连接不稳定  
**解决方案**: 改用腾讯财经接口直接获取数据
```python
# 腾讯财经接口
url = f"https://qt.gtimg.cn/q=sh{fund_code}"
# 返回格式: v_sh511880="1~银华日利~511880~100.035~..."
```

### 2. 时间戳精度
**需求**: 价格数据需要精确到分钟  
**实现**: 使用 `datetime.datetime.now().strftime('%Y-%m-%d %H:%M')`

### 3. 定时任务调度
**工具**: APScheduler  
**任务配置**:
- 价格采集: 每5分钟
- 净值采集: 每天9:30
- 收益率计算: 每10分钟
- 套利检查: 交易时段每15分钟
- 数据清理: 每5天

### 4. 免费部署方案
**后端**: PythonAnywhere（免费账户）
- 限制: 每天最多100秒CPU时间
- 解决: 使用 UptimeRobot 定时访问保持活跃

**前端**: Vercel（免费）
- 自动部署 GitHub 代码
- 全球 CDN 加速

---

## 项目文件清单

### 配置文件
- `requirements.txt`: Python 依赖
- `runtime.txt`: Python 版本（3.9）
- `Procfile`: 进程配置
- `wsgi.py`: WSGI 入口
- `.env.example`: 环境变量示例

### 部署文档
- `DEPLOY_PYTHONANYWHERE.md`: PythonAnywhere 部署指南
- `DEPLOY_VERCEL.md`: Vercel 部署指南
- `install_deps.sh`: 依赖安装脚本

### 开发文档
- `.trae/rules/ALIGNMENT_货币基金套利的提示.md`: 需求对齐文档
- `.trae/rules/DESIGN_货币基金套利的提示.md`: 架构设计文档
- `AGENTS.md`: 项目总结（本文档）

---

## 使用说明

### 本地开发
```bash
# 后端
cd backend
pip install -r requirements.txt
python api.py

# 前端
cd frontend
npm install
npm run dev
```

### 线上部署
1. **PythonAnywhere**: 按照 `DEPLOY_PYTHONANYWHERE.md` 操作
2. **Vercel**: 连接 GitHub 仓库自动部署
3. **UptimeRobot**: 配置定时访问 `/api/cron` 保持服务活跃

### 企业微信配置
1. 创建企业微信群
2. 添加群机器人
3. 复制 Webhook 地址
4. 设置环境变量 `WECOM_WEBHOOK_URL`

---

## 注意事项

1. **免费版限制**: PythonAnywhere 免费账户每天最多100秒CPU时间，需要优化代码效率
2. **数据存储**: 历史数据只保留5天，自动清理过期数据
3. **网络问题**: 腾讯财经接口偶尔会有访问限制，已实现备用接口
4. **时区问题**: PythonAnywhere 使用 UTC 时区，已配置为北京时间

---

## 后续优化方向

1. **数据持久化**: 考虑使用免费云数据库替代 SQLite
2. **监控告警**: 增加系统健康状态监控
3. **多基金支持**: 扩展支持更多货币基金
4. **自动交易**: 接入券商API实现自动套利（需谨慎）
5. **移动端**: 开发小程序或App版本

---

## 项目统计

- **开发周期**: 约2周
- **代码行数**: 约3000行（Python + Vue.js）
- **API接口**: 8个
- **数据库表**: 6个
- **定时任务**: 5个

---

## 联系方式

如有问题或建议，请通过以下方式联系：
- GitHub Issues: https://github.com/very45678/etf-project/issues
- 企业微信: 配置机器人后可接收系统通知

---

**项目完成日期**: 2026年3月20日  
**版本**: v1.0.0
