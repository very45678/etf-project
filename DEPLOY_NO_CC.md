# 完全免费部署方案 (无需信用卡)

如果 Render 需要验证信用卡，我们可以使用 **PythonAnywhere** 来部署后端。它对学生非常友好，完全免费，且不需要信用卡。

---

## 方案概览

1.  **后端**: 部署在 **PythonAnywhere** (免费，无需信用卡)。
2.  **前端**: 部署在 **Vercel** (免费，无需信用卡)。
3.  **定时任务**: 使用 **UptimeRobot** (免费) 每5分钟访问一次后端，触发数据抓取。

---

## 第一步：准备代码 (同之前)

确保你已经把代码上传到了 GitHub (参考之前的教程第一步)。

---

## 第二步：部署后端 (PythonAnywhere)

1.  **注册账号**:
    - 访问 [www.pythonanywhere.com](https://www.pythonanywhere.com/)。
    - 点击 **Pricing & Signup** -> **Create a Beginner account**。
    - 填写用户名、邮箱、密码，点击注册。**记住你的用户名**，比如叫 `zhangsan`，那你的网站就是 `zhangsan.pythonanywhere.com`。

2.  **上传代码**:
    - 登录后，点击右上角的 **Consoles** -> **Bash**。
    - 在黑色的命令行里输入以下命令（把链接换成你的 GitHub 仓库地址）：
      ```bash
      git clone https://github.com/你的用户名/etf-project.git
      ```
    - 等待下载完成。

3.  **安装依赖**:
    - 继续在命令行输入：
      ```bash
      cd etf-project/backend
      pip install --user -r requirements.txt
      ```
    - *注意：这一步可能需要几分钟，请耐心等待。如果提示 akshare 安装慢，可以多试几次。*

4.  **配置 Web 应用**:
    - 点击页面顶部的 **Web** 标签。
    - 点击 **Add a new web app** -> **Next**。
    - 选择 **Flask** -> **Python 3.9** (或 3.10)。
    - **Path**: 填 `/home/你的用户名/etf-project/backend/api.py` (注意把“你的用户名”换成真实的)。
      - *如果不确定路径，可以先填默认的，稍后修改。*
    - 点击 **Next** 完成创建。

5.  **修改配置**:
    - 在 Web 页面下，找到 **Source code** 部分，填入：
      `/home/你的用户名/etf-project/backend`
    - 找到 **WSGI configuration file**，点击那个链接。
    - 删除里面的所有内容，替换为以下内容（注意替换用户名）：
      ```python
      import sys
      import os
      
      # 把后端目录加入系统路径
      path = '/home/你的用户名/etf-project/backend'
      if path not in sys.path:
          sys.path.append(path)
      
      from api import app as application
      ```
    - 点击 **Save**，然后回到 Web 页面。

6.  **重启服务**:
    - 点击绿色的 **Reload** 按钮。
    - 访问 `https://你的用户名.pythonanywhere.com/api/test`，如果能看到数据，说明后端部署成功！

---

## 第三步：部署前端 (Vercel)

这一步和之前的教程几乎一样，只是后端地址变了。

1.  登录 Vercel，导入 `etf-project`。
2.  **Root Directory** 依然选 `frontend`。
3.  **Environment Variables**:
    - Key: `VITE_API_URL`
    - Value: `https://你的用户名.pythonanywhere.com/api` (注意是 pythonanywhere 的地址)。
4.  点击 **Deploy**。

---

## 第四步：设置定时任务 (UptimeRobot)

因为 PythonAnywhere 免费版不支持后台自动运行程序，我们需要用 UptimeRobot 来“手动”触发它。

1.  登录 UptimeRobot。
2.  **Add New Monitor**:
    - **Type**: `HTTP(s)`
    - **Name**: `ETF Cron`
    - **URL**: `https://你的用户名.pythonanywhere.com/api/cron` 
      - **注意！这里是 `/api/cron`，不是 `/api/test`。**
      - 我们专门加了这个接口，每次访问它，系统就会去抓取一次最新价格。
    - **Interval**: `5 minutes`。
3.  点击 **Create Monitor**。

**完成！** 现在 UptimeRobot 会每 5 分钟帮我们“按一下开关”，让系统去抓取数据。
