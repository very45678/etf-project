# PythonAnywhere 部署指南

## 概述
PythonAnywhere 是一个免费的 Python 托管平台，无需信用卡即可使用。

## 部署步骤

### 第一步：注册账号

1. 访问 https://www.pythonanywhere.com
2. 点击 "Start running Python online in less than a minute"
3. 填写注册信息：
   - Username: 你的用户名（记住这个，后面会用到）
   - Email: 你的邮箱
   - Password: 密码
4. 点击 "Create account"
5. 去邮箱验证账号

### 第二步：上传代码

#### 方法1：通过 Git 克隆（推荐）

1. 登录 PythonAnywhere
2. 点击顶部的 "Consoles" 标签
3. 点击 "Bash" 打开终端
4. 运行以下命令：

```bash
# 克隆你的 GitHub 仓库
cd ~
git clone https://github.com/very45678/etf-project.git

# 进入项目目录
cd etf-project
```

#### 方法2：通过 ZIP 上传

1. 在本地将项目打包为 ZIP
2. 点击 "Files" 标签
3. 点击 "Upload a file"
4. 上传 ZIP 文件
5. 在 Bash 终端解压：

```bash
cd ~
unzip etf-project.zip -d etf-project
```

### 第三步：安装依赖

在 Bash 终端运行：

```bash
cd ~/etf-project/backend

# 安装依赖
pip install --user Flask==3.0.0 flask-cors==4.0.0 apscheduler==3.10.4 requests==2.31.0 beautifulsoup4==4.12.2 lxml==4.9.3 akshare==1.16.72 pandas==2.1.4 numpy==1.26.4
```

### 第四步：创建 Web 应用

1. 点击顶部的 "Web" 标签
2. 点击 "Add a new web app"
3. 选择 "Manual configuration"
4. 选择 "Python 3.9"
5. 点击 "Next"

### 第五步：配置 Web 应用

在 Web 应用配置页面，设置以下选项：

#### Source code:
```
/home/你的用户名/etf-project/backend
```

#### Working directory:
```
/home/你的用户名/etf-project/backend
```

#### WSGI configuration file:
点击链接编辑，删除所有内容，替换为：

```python
import sys
import os

# 添加项目路径
path = '/home/你的用户名/etf-project/backend'
if path not in sys.path:
    sys.path.insert(0, path)

# 设置环境变量
os.environ['FLASK_ENV'] = 'production'

# 导入 Flask 应用
from api import app as application
```

**注意**：将 "你的用户名" 替换为你的 PythonAnywhere 用户名

### 第六步：配置静态文件（前端）

1. 在 Web 配置页面，找到 "Static files" 部分
2. 点击 "Add a new static files entry"
3. URL: `/`
4. Directory: `/home/你的用户名/etf-project/frontend/dist`

### 第七步：重新加载应用

点击页面顶部的绿色 "Reload" 按钮

### 第八步：访问网站

你的应用将会运行在：
```
https://你的用户名.pythonanywhere.com
```

### 第九步：配置定时任务

1. 点击 "Tasks" 标签
2. 点击 "Create a new task"
3. 设置时间（例如每5分钟）：
   ```
   */5 * * * *
   ```
4. Command:
   ```
   cd /home/你的用户名/etf-project/backend && python -c "from price_fetcher import fetch_all_funds; fetch_all_funds()"
   ```
5. 点击 "Create"

再创建一个任务用于采集净值数据（每天一次）：

1. 点击 "Create a new task"
2. 设置时间（每天上午9点）：
   ```
   0 9 * * *
   ```
3. Command:
   ```
   cd /home/你的用户名/etf-project/backend && python -c "from nav_fetcher import fetch_all_funds_nav; fetch_all_funds_nav()"
   ```
4. 点击 "Create"

## 保持活跃

PythonAnywhere 免费账户需要每3个月点击一次 "Run until 3 months from today" 按钮来延长任务运行时间。

## 调试

如果应用无法正常运行：

1. 查看错误日志：点击 "Web" 标签 → "Error log"
2. 查看访问日志：点击 "Web" 标签 → "Access log"
3. 在 Bash 终端测试：
   ```bash
   cd ~/etf-project/backend
   python -c "from api import app; print('OK')"
   ```

## 更新代码

当代码有更新时：

```bash
cd ~/etf-project
git pull origin main
```

然后点击 "Reload" 重新加载应用。
