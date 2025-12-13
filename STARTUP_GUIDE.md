# 🚀 Code Agent 启动指南和代码生成位置

## 快速答案

**启动方式：**
- 推荐：`./cli.sh`（自动管理虚拟环境）
- 直接：`python3 interactive_cli.py`
- 演示：`python3 demo_interactive.py`

**生成的代码位置：**
- **`workspace/` 目录** ← 所有生成的代码文件都保存在这里

---

## 🚀 三种启动方式

### 方式 1：一键启动脚本（推荐 ⭐️）

```bash
./cli.sh
```

**工作流程：**
1. 检查虚拟环境 `.venv` 是否存在
2. 如不存在，自动创建
3. 激活虚拟环境
4. 自动安装依赖（从 `requirements.txt`）
5. 启动交互式 CLI

**优点：**
- ✅ 完全自动化
- ✅ 环境隔离
- ✅ 一键启动

### 方式 2：直接运行 Python

```bash
python3 interactive_cli.py
```

**前置要求：**
- 虚拟环境已激活
- 依赖已安装

```bash
# 手动设置虚拟环境
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 启动
python3 interactive_cli.py
```

### 方式 3：查看演示

```bash
python3 demo_interactive.py
```

运行完整的演示脚本，展示系统的核心功能。

---

## 📁 生成的代码文件位置

所有生成的代码自动保存到：

```
workspace/
├── app.py                    ← 生成的应用文件
├── models.py                 ← 生成的数据模型
├── requirements.txt          ← 依赖列表
├── config.py                 ← 配置文件
├── utils.py                  ← 工具函数
├── static/                   ← 静态文件（CSS、JS、图片等）
├── templates/                ← HTML 模板
├── src/                      ← 源代码目录
│   ├── main.py
│   └── ...
└── ...                       ← 其他生成的文件
```

### 配置位置

在 `config.py` 中定义：

```python
from pathlib import Path

class Config:
    PROJECT_ROOT = Path(__file__).parent
    WORKSPACE_DIR = PROJECT_ROOT / "workspace"
```

也就是：
```
/Users/hushuai/Desktop/项目/code_agent/workspace/
```

---

## 🔄 代码生成完整流程

### 1️⃣ 用户输入（交互式 CLI）

```
👤 You: 生成一个 Flask REST API 用于用户管理

🤖 Thinking...
```

### 2️⃣ PlannerAgent 规划阶段

- 解析用户需求
- 生成项目结构
- 生成文件清单和开发任务

**输出示例：**
```json
{
  "project_name": "user-management-api",
  "project_description": "Flask REST API for user management",
  "files": [
    {
      "filename": "app.py",
      "purpose": "Main Flask application"
    },
    {
      "filename": "models.py",
      "purpose": "Database models"
    },
    {
      "filename": "requirements.txt",
      "purpose": "Python dependencies"
    }
  ]
}
```

### 3️⃣ CoderAgent 代码生成阶段

对每个文件：
1. 调用 LLM 生成代码
2. 验证代码
3. 保存到 `workspace/`

**日志输出：**
```
✓ Code generated and saved for: app.py
✓ Code generated and saved for: models.py
✓ Code generated and saved for: requirements.txt
```

### 4️⃣ FileTools 文件保存

```python
# 在 tools/file_tools.py 中实现

FileTools.save_code(
    filename="app.py",
    code="from flask import Flask\n..."
)

# 自动：
# 1. 创建必要的目录结构
# 2. 写入文件内容
# 3. 返回完整路径
# 4. 打印成功信息
```

---

## 📂 完整项目目录结构

```
code_agent/
├── 📄 启动脚本和配置
│   ├── cli.sh                          ← ⭐️ 推荐启动脚本
│   ├── activate.sh                     ← 激活虚拟环境
│   ├── interactive_cli.py              ← 主 CLI 程序
│   ├── demo_interactive.py             ← 演示脚本
│   ├── config.py                       ← 配置管理
│   ├── requirements.txt                ← 项目依赖
│   ├── .env                            ← 本地配置（API Key，.gitignore 保护）
│   └── .env.example                    ← 配置模板
│
├── 👥 核心 Agent 模块
│   └── agents/
│       ├── conversation_manager.py     ← 对话历史管理
│       ├── planner.py                  ← 项目规划 Agent
│       ├── coder.py                    ← 代码生成 Agent
│       └── __init__.py
│
├── 🛠️ 工具和工具函数
│   ├── tools/
│   │   ├── file_tools.py               ← 文件操作工具 ⭐️
│   │   └── __init__.py
│   └── utils/
│       ├── llm_client.py               ← LLM API 客户端
│       └── __init__.py
│
├── 💾 生成的代码存储位置
│   └── workspace/                      ← ⭐️ **所有生成的代码都在这里**
│       ├── app.py
│       ├── models.py
│       ├── requirements.txt
│       ├── static/
│       ├── templates/
│       └── ... (其他生成的文件)
│
├── 💬 对话历史
│   └── .conversation_history/
│       └── (自动保存的对话记录)
│
├── 📚 虚拟环境
│   └── .venv/
│       └── (Python 包和环境)
│
├── 📖 文档
│   ├── README.md                      ← 完整文档
│   ├── QUICKSTART.md                  ← 快速开始
│   ├── INTERACTIVE_TUTORIAL.md         ← 交互式教程
│   └── PROJECT_SUMMARY.md              ← 项目总结
│
└── 🧪 测试文件
    ├── test_connection.py
    ├── test_planner.py
    ├── test_coder.py
    ├── test_file_tools.py
    └── test_agent_integration.py
```

---

## 🔐 API Key 配置步骤

### 第 1 步：复制模板

```bash
cp .env.example .env
```

### 第 2 步：编辑 .env

```bash
nano .env  # 或 vim, VS Code 等编辑器
```

或在 VS Code 中直接编辑 `.env` 文件。

### 第 3 步：填入实际值

修改这一行：
```
LLM_API_KEY=sk-your-actual-api-key-here
```

改为你的实际 API Key：
```
LLM_API_KEY=sk-12345...
```

### 获取 API Key

- **DeepSeek**: https://platform.deepseek.com/api_keys
- **OpenAI**: https://platform.openai.com/api-keys

### 安全性说明

✅ `.env` 文件在 `.gitignore` 中，不会被提交到 GitHub
✅ 只有 `.env.example` 会公开分享
✅ 你的实际 API Key 永远保存在本地

---

## ⚙️ 配置文件说明

### config.py（自动读取 .env）

```python
from config import Config

Config.LLM_PROVIDER          # "deepseek"
Config.LLM_API_KEY           # 从 .env 读取
Config.LLM_MODEL             # "deepseek-chat"
Config.LLM_BASE_URL          # "https://api.deepseek.com"
Config.PROJECT_ROOT          # /Users/hushuai/Desktop/项目/code_agent
Config.WORKSPACE_DIR         # /Users/hushuai/Desktop/项目/code_agent/workspace
Config.PLANNER_MODEL         # Agent 特定模型
Config.CODER_MODEL           # Agent 特定模型
Config.REVIEWER_MODEL        # Agent 特定模型
Config.LOG_LEVEL             # "INFO"
```

---

## 🎯 第一次启动（完整步骤）

```bash
# 1. 进入项目目录
cd /Users/hushuai/Desktop/项目/code_agent

# 2. 配置 API Key
cp .env.example .env
nano .env  # 编辑并填入真实的 API Key

# 3. 启动（自动创建虚拟环境、安装依赖）
./cli.sh

# 4. 在交互式 CLI 中输入提示
👤 You: 生成一个简单的 Python Hello World 程序

# 5. 等待代码生成完成
🤖 Thinking...
   Planning...
   Generating...
   ✓ Saved file: workspace/hello.py
   
# 6. 查看生成的文件
ls workspace/
cat workspace/hello.py
```

---

## 📊 使用示例

### 示例 1：生成 Flask Web 应用

```
👤 You: 生成一个 Flask Web 应用，包括用户注册和登录功能

🤖 Agent:
   [规划中...]
   ✓ Project planned with 6 files
   
   [生成代码...]
   ✓ Saved file: workspace/app.py
   ✓ Saved file: workspace/models.py
   ✓ Saved file: workspace/forms.py
   ✓ Saved file: workspace/requirements.txt
   ✓ Saved file: workspace/templates/login.html
   ✓ Saved file: workspace/templates/register.html

# 现在你可以使用生成的代码
cd workspace
pip install -r requirements.txt
python app.py
```

### 示例 2：修改生成的代码

```
👤 You: 给 Flask 应用添加数据库支持

🤖 Agent:
   [根据 workspace/ 中的现有代码进行修改...]
   ✓ Updated file: workspace/models.py
   ✓ Updated file: workspace/requirements.txt
```

### 示例 3：生成多种语言代码

```
👤 You: 生成一个 REST API，用 Python 和 JavaScript 实现客户端

🤖 Agent:
   [规划...]
   [生成 Python 服务器代码...]
   ✓ Saved file: workspace/server.py
   
   [生成 JavaScript 客户端...]
   ✓ Saved file: workspace/client.js
```

---

## 🐛 常见问题

### Q: 生成的文件在哪里？
**A:** 在 `workspace/` 目录中。所有生成的代码都会自动保存到这里。

### Q: 如何修改生成代码的位置？
**A:** 编辑 `config.py` 中的 `WORKSPACE_DIR`：
```python
WORKSPACE_DIR = Path("/path/to/your/directory")
```

### Q: 如何清除已生成的文件？
**A:** 
```bash
# 清空 workspace 目录（谨慎操作）
rm -rf workspace/*

# 或保留结构
find workspace -type f -delete
```

### Q: 虚拟环境出问题如何重新创建？
**A:**
```bash
# 删除旧的虚拟环境
rm -rf .venv

# 重新启动脚本会自动创建
./cli.sh
```

### Q: API Key 不正确怎么办？
**A:**
1. 检查 `.env` 文件中的 `LLM_API_KEY` 值
2. 确保 API Key 有效（去 DeepSeek/OpenAI 官网检查）
3. 重新启动程序：`./cli.sh`

### Q: 生成的代码可以直接使用吗？
**A:** 是的！生成的代码遵循最佳实践，可以直接在 `workspace/` 中运行：
```bash
cd workspace
pip install -r requirements.txt
python app.py
```

---

## 💡 最佳实践

### ✅ 推荐做法

1. **使用启动脚本**
   ```bash
   ./cli.sh  # 完全自动化
   ```

2. **定期检查 workspace 目录**
   ```bash
   ls -la workspace/
   ```

3. **保存重要的生成代码**
   ```bash
   cp -r workspace/ workspace_backup_$(date +%Y%m%d)
   ```

4. **使用对话历史进行迭代**
   - Agent 会记住之前的对话
   - 可以要求修改或改进之前生成的代码

### ❌ 避免做法

1. ❌ 直接编辑 `.env`（使用 `cp .env.example .env`）
2. ❌ 提交 `.env` 到 Git（已在 .gitignore 中）
3. ❌ 删除 `.venv` 目录（除非重新创建）
4. ❌ 在 workspace 外部保存生成的代码

---

## 📞 获取帮助

- 查看完整文档：`README.md`
- 快速入门指南：`QUICKSTART.md`
- 交互式教程：`INTERACTIVE_TUTORIAL.md`
- 项目统计：`PROJECT_SUMMARY.md`

---

**现在你已经完全了解如何启动 Code Agent 并在哪里找到生成的代码！** 🎉
