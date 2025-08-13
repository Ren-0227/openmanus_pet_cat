项目介绍
OpenManus 桌面宠物是基于 OpenManus 智能体框架开发的交互式桌面宠物应用。它将强大的 AI 智能体能力与可爱的桌面宠物形象相结合，为用户提供既有趣又实用的桌面交互体验。

通过这个应用，你可以：

与桌面宠物进行自然语言对话
让 AI 智能体帮你完成各种任务（编程、信息检索、文件处理等）
与宠物进行互动（喂食、换装等）
享受生动的宠物动画效果

功能特点
智能交互
基于 OpenManus 框架的强大 AI 能力
支持多工具调用（Python 执行、网页浏览、文件操作、谷歌搜索等）
能理解并执行复杂任务
宠物互动
可爱的动画效果（眨眼、呼吸、摆尾等）
互动功能：喂食、换装等
实时反馈和状态变化

安装指南
后端安装（OpenManus 智能体）
方法一：使用 conda
创建并激活虚拟环境：

conda create -n open_manus python=3.12
conda activate open_manus

克隆仓库并安装依赖：
git clone https://github.com/mannaandpoem/OpenManus.git
cd OpenManus
pip install -r requirements.txt

方法二：使用 uv（推荐）
安装 uv：
curl -LsSf https://astral.sh/uv/install.sh | sh

克隆仓库并设置环境：
git clone https://github.com/mannaandpoem/OpenManus.git
cd OpenManus
uv venv
source .venv/bin/activate  # Unix/macOS
# 或在 Windows 上：.venv\Scripts\activate
uv pip install -r requirements.txt

桌面宠物前端安装
进入桌面宠物目录：
cd my-desktop-pet

安装依赖：
npm install
配置说明
配置 LLM API：

cp config/config.example.toml config/config.toml

编辑配置文件，添加你的 API 密钥：

toml
[llm]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # 替换为你的 API 密钥
max_tokens = 4096
temperature = 0.0
快速启动
启动后端服务：

python main.py


启动桌面宠物（新终端）：

bash
cd my-desktop-pet
npm start


与你的桌面宠物互动吧！可以通过输入框发送指令，或使用互动按钮进行喂食、换装等操作。
