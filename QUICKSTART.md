# 🚀 Code Agent - 5 分钟快速开始

## 什么是 Code Agent？

Code Agent 是一个**多轮对话的 AI 代码生成系统**，可以：
- 💬 **像 ChatGPT 一样对话**：自然语言输入，AI 帮你规划和生成代码
- 🧠 **记住整个对话**：每条信息都被保存，支持渐进式改进
- 🎯 **自动意图识别**：自动判断你是要生成、修改还是查看项目
- 📦 **完整代码生成**：生成可直接使用的、生产级别的代码

## 开始使用（3 步）

### ✅ 第一步：准备环境（1 分钟）

```bash
# 1. 进入项目目录
cd /Users/hushuai/Desktop/项目/code_agent

# 2. 确保已安装依赖
pip install -r requirements.txt

# 3. 检查 API Key 配置
cat .env
# 应该看到：LLM_API_KEY=sk-xxxxxxxx
```

### ✅ 第二步：启动 CLI（10 秒）

**方式 1：一键启动（推荐）**
```bash
./cli.sh
```

**方式 2：直接运行**
```bash
python3 interactive_cli.py
```

### ✅ 第三步：开始对话（2 分钟）

启动后你会看到：
```
🚀 Code Agent - Interactive Multi-Turn Conversation Mode
======================================================================

Welcome! I can generate code, modify files, and remember our conversation.
Type 'help' for commands or start chatting!

👤 You: _
```

现在就开始输入命令！👇

---

## 常用命令（复制粘贴就用）

### 📝 生成代码
```
生成一个 Flask REST API 用于用户管理
创建一个 React 待办事项应用
构建一个 Django 博客平台
```

### ✏️ 修改代码
```
添加 JWT 认证功能
改进错误处理
优化数据库性能
```

### 📊 查看信息
```
显示项目状态
列出已生成的文件
显示对话历史
```

### 🔧 系统命令
```
help          # 显示帮助
clear         # 清空对话
status        # 查看进度
quit          # 退出程序
```

---

## 🎬 完整对话示例

```
👤 You: 生成一个 Python Flask API，支持用户认证和任务管理

🤖 Agent: 我将为你创建一个完整的 Flask REST API...
[自动规划和生成代码]

👤 You: 能添加数据库支持吗？

🤖 Agent: 基于之前的代码，我将添加数据库支持...
[自动修改和增强代码]

👤 You: 显示当前状态

🤖 Agent: 📊 项目信息...
- 消息数: 4
- 文件生成: 5
- 总大小: 45 KB

👤 You: quit

👋 Goodbye! Your conversation has been saved.
```

---

## 💡 核心特性

| 特性 | 说明 |
|------|------|
| **多轮对话** | 像聊天一样交互，支持数十轮问答 |
| **完整记忆** | 所有对话都保存在 `.conversation_history/` |
| **智能意图** | 自动识别你的意图（生成/修改/查询） |
| **代码生成** | 生成可直接运行的完整项目 |
| **渐进改进** | 基于反馈逐步完善代码 |
| **生产级** | 生成的代码符合最佳实践 |

---

## 📁 生成的文件在哪里？

所有生成的代码保存在 `workspace/` 目录：

```bash
# 查看生成的文件
ls workspace/

# 进入工作空间
cd workspace

# 安装依赖（如果有 requirements.txt）
pip install -r requirements.txt

# 运行应用
python3 app.py
```

---

## 🆘 遇到问题？

### ❌ CLI 无法启动

```bash
# 检查 Python 版本
python3 --version

# 检查依赖
pip list | grep openai

# 验证 API Key
echo $LLM_API_KEY
```

### ❌ API 连接失败

```bash
# 测试连接
python3 test_connection.py

# 查看详细错误
python3 -c "
from config import Config
from utils.llm_client import LLMClient
c = Config()
llm = LLMClient(config=c)
print(llm.chat([{'role': 'user', 'content': 'hi'}]))
"
```

### ❌ 对话记录丢失

```bash
# 查看历史文件
ls .conversation_history/

# 查看内容
cat .conversation_history/current_session.json
```

---

## 🎓 更多资源

| 文档 | 内容 |
|------|------|
| **README_INTERACTIVE.md** | 详细功能说明和架构 |
| **INTERACTIVE_TUTORIAL.md** | 完整使用教程和案例 |
| **demo_interactive.py** | 运行演示 `python3 demo_interactive.py` |

---

## ⚡ 高级技巧

### 链式生成
```
生成基础项目
→ 添加认证
→ 添加数据库
→ 添加测试
→ 完成！
```

### 学习模式
```
生成代码
→ 问：这个设计为什么这样？
→ 问：有没有更好的方式？
→ 问：最佳实践是什么？
```

### 多项目管理
```bash
# 保存当前项目
cp .conversation_history/current_session.json project1.json

# 清空继续新项目
# 在 CLI 中输入: clear

# 恢复之前的项目
cp project1.json .conversation_history/current_session.json
```

---

## 📊 工作流程

```
你的需求
    ↓
Natural Language Input
    ↓
Intent Recognition (生成/修改/查询?)
    ↓
┌─ 生成 → Planner (规划) → Coder (代码) → 文件
├─ 修改 → 基于历史改进代码 → 文件
└─ 查询 → 显示状态/文件/历史
    ↓
结果展示 + 保存到文件 + 记录对话
```

---

## 🎯 下一步

1. **现在就开始**：运行 `./cli.sh`
2. **随意尝试**：输入任何需求，AI 会帮你规划和生成
3. **迭代改进**：提供反馈，AI 会改进代码
4. **导出项目**：生成的代码在 `workspace/` 目录

---

## 💬 示例需求（复制即用）

```
# 简单项目
生成一个 Python 命令行工具，用于转换图片格式

# Web 应用
创建一个 Flask 后台管理系统
Create a React dashboard for analytics

# 复杂项目
构建一个电商平台，包含用户系统、商品管理、订单处理
Build a microservices architecture with FastAPI

# 学习场景
生成一个 REST API 并解释设计模式
生成测试代码并说明如何运行
```

---

## 🚀 现在就开始吧！

```bash
./cli.sh
```

输入你的第一个需求，享受 AI 驱动的代码生成！

---

**需要帮助？** 查看详细文档：
- 📖 [README_INTERACTIVE.md](README_INTERACTIVE.md) - 完整功能说明
- 📚 [INTERACTIVE_TUTORIAL.md](INTERACTIVE_TUTORIAL.md) - 使用教程

**想看演示？**
```bash
python3 demo_interactive.py
```

**Happy Coding! 🎉**
