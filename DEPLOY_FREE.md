# 零基础免费云端部署教程 (保姆级)

你好！这份教程是专门为你准备的。哪怕你从来没有“部署”过代码，只要跟着做，也能把你的货币基金套利系统发布到互联网上，让大家都能访问！

我们要做的事情就像盖房子：
1. **GitHub**: 相当于把你的“设计图纸”（代码）存到云端仓库。
2. **Render**: 相当于租一台免费的服务器（电脑）来运行你的 Python 后端程序。
3. **Vercel**: 相当于租一个免费的展示柜，用来展示你的网页（前端）。
4. **UptimeRobot**: 相当于一个闹钟，防止免费的服务器“偷懒睡觉”。

---

## 准备工作

*   你需要一个 **GitHub 账号** (去 [github.com](https://github.com/) 注册，记得验证邮箱)。
*   你需要一个 **邮箱** (用来注册其他账号)。
*   保持耐心，遇到不懂的英文单词不要怕，跟着教程点就行。

---

## 第一步：把代码传到 GitHub

我们要先把电脑上的代码上传到 GitHub 仓库。

1.  **创建仓库**：
    - 登录 GitHub，点击右上角的 **+** 号，选择 **New repository**。
    - **Repository name** 填 `etf-project` (或者你喜欢的名字)。
    - 选中 **Public** (公开)。
    - 点击最下面的 **Create repository** 绿色按钮。
    - 创建好后，页面不要关，你会看到一个以 `.git` 结尾的链接（比如 `https://github.com/你的名字/etf-project.git`），复制它。

2.  **上传代码**：
    - 回到你的 IDE (代码编辑器)，打开终端 (Terminal)。
    - **依次复制并执行**下面的命令（一行一行执行，按回车）：

    ```bash
    # 1. 初始化（告诉电脑这里要用 Git 管理）
    git init

    # 2. 把所有文件放入暂存区
    git add .

    # 3. 提交文件（给这次上传起个名字）
    git commit -m "first commit"

    # 4. 把当前分支改名为 main
    git branch -M main

    # 5. 连接到你刚才创建的 GitHub 仓库
    # ⚠️注意！把下面的链接换成你刚才复制的那个链接！
    git remote add origin https://github.com/你的用户名/etf-project.git

    # 6. 推送到云端
    git push -u origin main
    ```
    *(如果在第6步报错，可能是需要登录。根据提示操作，或者搜索“Git如何配置SSH”)*

3.  **检查**：刷新 GitHub 网页，如果能看到你的代码文件（backend, frontend 等），就成功了！

---

## 第二步：部署后端 (Render)

Render 是一个提供免费服务器的网站，我们要把 Python 后端放在这里运行。

1.  **注册账号**：
    - 打开 [Render.com](https://render.com/)，点击 **Get Started for Free**。
    - 强烈建议选择 **GitHub** 图标登录，这样可以直接读取你的代码。

2.  **创建服务**：
    - 登录后，点击右上角的 **New +** 按钮，选择 **Web Service**。
    - 在列表中找到你刚才上传的 `etf-project`，点击右边的 **Connect**。

3.  **填写配置** (这一步最重要，不要填错)：
    - **Name**: `etf-backend` (随便填，名字而已)
    - **Region**: 选 `Singapore` (新加坡) 也就是离我们最近的，速度快点。
    - **Branch**: `main`
    - **Root Directory** (根目录): 必须填 **`backend`** (因为我们的 Python 代码在这个文件夹里)。
    - **Runtime**: 选 **`Python 3`**。
    - **Build Command**: 默认可能是 `pip install -r requirements.txt`，**不用改**，对的。
    - **Start Command**: 填 **`gunicorn api:app`** (这是启动命令)。
    - **Instance Type**: 选 **Free** (免费版)。

4.  **添加环境变量** (让 Python 版本正确)：
    - 向下滚动，找到 **Environment Variables**，点击 **Add Environment Variable**。
    - **Key** 填: `PYTHON_VERSION`
    - **Value** 填: `3.9.0`

5.  **开始部署**：
    - 点击最下面的 **Create Web Service** 按钮。
    - 此时你会看到黑色框框里在跑代码，这是它在安装依赖。
    - 等几分钟，直到看到绿色的 **Live** 字样。
    - 在左上角名字下方，有一个链接（比如 `https://etf-backend-xxxx.onrender.com`），**复制这个链接**，这是你的**后端地址**。

---

## 第三步：部署前端 (Vercel)

Vercel 是专门用来放网页的，速度很快且免费。

1.  **注册账号**：
    - 打开 [Vercel.com](https://vercel.com/)，点击 **Sign Up**。
    - 同样选择 **Continue with GitHub**。

2.  **导入项目**：
    - 在主页点击 **Add New...** -> **Project**。
    - 在左侧列表里找到 `etf-project`，点击 **Import**。

3.  **配置项目**：
    - **Framework Preset**: 它应该自动识别出 `Vite`，如果不是，手动选 Vite。
    - **Root Directory**: 点击 **Edit**，选择 **`frontend`** 文件夹 (因为网页代码在这里)。
    - **Environment Variables** (环境变量): 点击展开。
      - **Key** 填: `VITE_API_URL`
      - **Value** 填: 粘贴**上一步复制的后端地址**，并在末尾加上 `/api`。
        - 正确示例: `https://etf-backend-xxxx.onrender.com/api`
        - 错误示例: `https://etf-backend-xxxx.onrender.com` (少/api)
        - 错误示例: `https://etf-backend-xxxx.onrender.com/` (少api)
      - 点击 **Add**。

4.  **开始部署**：
    - 点击 **Deploy** 按钮。
    - 屏幕会放烟花庆祝，等待几十秒。
    - 完成后，点击图片或者 **Visit** 按钮，你就能看到你的网站了！**复制这个网站地址**，发给你的朋友吧！

---

## 第四步：防止服务器“睡觉” (UptimeRobot)

Render 的免费服务器有一个缺点：如果 15 分钟没人访问，它就会自动“休眠”省电。一旦休眠，你的**定时抓取数据**任务就会停止。我们需要用工具每隔几分钟“戳”它一下。

1.  **注册**：打开 [UptimeRobot.com](https://uptimerobot.com/)，注册一个免费账号。
2.  **添加监控**：
    - 点击左上角的 **+ Add New Monitor**。
    - **Monitor Type**: 选 `HTTP(s)`。
    - **Friendly Name**: 随便填，比如 `ETF Backend`。
    - **URL (or IP)**: 填你的**后端地址**，并在后面加上 `/api/test`。
      - 例如: `https://etf-backend-xxxx.onrender.com/api/test`
      - (为什么要加 /api/test？因为这是我们专门留的一个测试接口，访问它不会消耗太多资源，但能唤醒服务器)
    - **Monitoring Interval**: 把滑块拖到 **5 minutes** (每5分钟)。
3.  **保存**：点击 **Create Monitor**。

**大功告成！** 
现在，你的系统会 24 小时自动运行，每 5 分钟抓取一次数据，并且你可以随时通过 Vercel 的网址访问它。

---

## 常见疑问

**Q: 我第二天早上起来，发现昨天的数据都不见了？**
A: 这是正常的。Render 的免费服务器就像网吧的电脑，重启后会还原。它每天可能会自动重启一次，这时候存在里面的 SQLite 数据库文件就会被重置。
**影响大吗？** 不大。因为这个系统主要是看**实时套利机会**。数据丢了，系统会自动重新抓取最新的实时价格，不影响你判断现在能不能买。

**Q: 网页打开显示“获取数据失败”？**
A: 可能是服务器刚才睡着了，正在被唤醒（冷启动）。Render 免费版唤醒需要 50 秒左右。耐心等一分钟，刷新页面通常就好了。
