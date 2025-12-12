# Code Agent 交互式 CLI - 完整使用指南

## 目录
1. [快速开始](#快速开始)
2. [命令系统](#命令系统)
3. [实际使用案例](#实际使用案例)
4. [对话记忆机制](#对话记忆机制)
5. [常见问题](#常见问题)

---

## 快速开始

### 第一步：启动 CLI

```bash
# 方式 1：使用启动脚本（推荐）
./cli.sh

# 方式 2：直接运行 Python
python3 interactive_cli.py

# 方式 3：使用 uv 运行
uv run python3 interactive_cli.py
```

### 第二步：输入命令

CLI 启动后，你会看到：
```
🚀 Code Agent - Interactive Multi-Turn Conversation Mode
======================================================================

Welcome! I can generate code, modify files, and remember our conversation.
Type 'help' for commands or start chatting!

👤 You: _
```

### 第三步：对话交互

直接输入你的需求，就像与 ChatGPT 对话一样：

```
👤 You: 生成一个 Flask API
🤖 Agent: [自动规划和生成代码]
```

---

## 命令系统

### 1. 代码生成命令

用于创建新项目或组件。

**关键词识别：** `generate`, `create`, `build`, `make`

**示例：**
```
👤 You: Generate a Flask REST API for user management
👤 You: Create a React dashboard with TypeScript
👤 You: Build a Django e-commerce platform
👤 You: Make a Python CLI tool for file processing
```

**工作流：**
1. Agent 理解需求
2. 使用 PlannerAgent 生成项目规划
3. 使用 CoderAgent 生成代码文件
4. 文件自动保存到 `workspace/` 目录

**示例响应：**
```
🔄 Generating project based on your request...

📝 Planning phase...
💻 Generating code...

📋 **Project Plan:**
- Name: User Management API
- Files to generate: 8
- Tech Stack: Python, Flask, SQLAlchemy

✅ **Generated 5 files successfully!**
📁 Check the workspace folder for generated files.
```

### 2. 代码修改命令

用于改进或修复已生成的代码。

**关键词识别：** `modify`, `change`, `improve`, `fix`, `update`

**示例：**
```
👤 You: Add JWT authentication to the API
👤 You: Improve error handling in app.py
👤 You: Fix the database validation logic
👤 You: Update the config file for production
```

**工作流：**
1. Agent 理解修改需求和之前的对话
2. 分析现有代码
3. 生成改进后的版本
4. 保存修改

### 3. 信息查询命令

用于查看当前项目状态。

**关键词识别：** `status`, `info`, `show`, `list`, `what`

**示例：**
```
👤 You: Show status
👤 You: What files have been generated?
👤 You: List the workspace files
👤 You: What's been done so far?
👤 You: Information about current project
```

**示例响应：**
```
📊 **Project Information:**

Conversation Summary:
- Messages: 5
- Project: Task Management API
- Files Generated: 3
- Last Updated: 2024-01-15 10:35:20

📁 **Workspace Files (21 total):**
  - app.py
  - models.py
  - config.py
  - requirements.txt
  ... and 17 more files
```

### 4. 系统管理命令

用于控制 CLI 的运行。

| 命令 | 效果 |
|------|------|
| `help` 或 `?` | 显示帮助信息 |
| `clear` 或 `reset` | 清空对话历史，开始新的对话 |
| `quit` 或 `exit` | 退出程序 |

**示例：**
```
👤 You: help
# 显示完整的命令列表

👤 You: clear
# 清空历史，消息计数重置为 0

👤 You: quit
# 退出程序，对话自动保存
```

---

## 实际使用案例

### 案例 1：从零开始构建 Flask API

```
👤 You: 生成一个 Flask REST API，支持用户注册、登录、个人信息管理
🤖 Agent: 我将为你创建一个完整的 Flask REST API...
[生成 app.py, models.py, config.py 等]

👤 You: 能否添加 JWT 令牌认证？
🤖 Agent: 基于我们之前生成的 Flask 应用，我将添加 JWT 认证...
[修改 app.py，添加认证中间件]

👤 You: 加入数据验证和错误处理
🤖 Agent: 我将改进错误处理逻辑...
[优化代码结构]

👤 You: 生成数据库迁移脚本
🤖 Agent: 基于当前的模型定义，生成迁移脚本...
[添加 migration 相关文件]

👤 You: 显示当前项目状态
🤖 Agent: 📊 项目信息...
```

**关键点：**
- 每一步都基于之前的对话和生成的代码
- Agent 记住了所有的需求和决策
- 可以渐进式地完善项目

### 案例 2：优化现有代码

```
👤 You: 改进 models.py 中的数据库模型性能
🤖 Agent: 我分析了当前的模型定义，将添加数据库索引和查询优化...
[提供优化后的 models.py]

👤 You: 添加数据缓存层
🤖 Agent: 我将添加 Redis 缓存...
[生成 cache.py]

👤 You: 性能优化完成，现在需要添加单元测试
🤖 Agent: 基于当前的代码，我将生成完整的测试套件...
[生成 tests/ 目录结构]
```

### 案例 3：多语言项目

```
👤 You: 生成前后端分离的项目：Flask 后端 + React 前端
🤖 Agent: 我将创建完整的项目结构...
[生成 backend/ 和 frontend/ 目录]

👤 You: 后端加入 WebSocket 支持
🤖 Agent: 我将在 Flask 应用中添加 WebSocket...
[修改后端代码]

👤 You: 前端连接到 WebSocket
🤖 Agent: 我将生成 React 的 WebSocket 客户端...
[生成 React 组件]

👤 You: 显示整个项目结构
🤖 Agent: 📊 项目信息...
```

---

## 对话记忆机制

### 🧠 记忆的工作原理

1. **实时保存**：每条消息都立即保存到 JSON 文件
2. **上下文管理**：自动从最近的对话中提取上下文
3. **项目追踪**：记录项目名称、生成的文件数等
4. **时间戳**：每条消息都有时间戳便于追踪

### 📁 历史文件位置

```
.conversation_history/
└── current_session.json    # 当前对话的所有消息
```

### 📋 历史文件结构

```json
{
  "messages": [
    {
      "role": "user",
      "content": "生成一个 Flask API",
      "timestamp": "2024-01-15T10:30:45.123456"
    },
    {
      "role": "assistant",
      "content": "我将为你创建...",
      "timestamp": "2024-01-15T10:30:50.234567"
    }
  ],
  "project_context": {
    "project_name": "Task Management API",
    "files_generated": 5,
    "tech_stack": ["Python", "Flask", "SQLAlchemy"],
    "last_updated": "2024-01-15T10:35:20"
  }
}
```

### 🔄 对话恢复

程序启动时自动加载 `current_session.json`：

```bash
$ python3 interactive_cli.py

# 程序检测到之前的对话
✓ Loaded 5 previous messages
✓ Project context: Task Management API
✓ Ready to continue...
```

### 💾 手动管理历史

```bash
# 查看当前对话
cat .conversation_history/current_session.json | jq

# 清空对话（使用 CLI 命令）
👤 You: clear

# 导出对话记录
cat .conversation_history/current_session.json > my_project_history.json
```

---

## 常见问题

### Q1: 对话历史会丢失吗？

**A:** 不会。所有对话都自动保存到 `.conversation_history/current_session.json`。
- 程序崩溃也能恢复
- 只有你执行 `clear` 命令才会清空
- 可以手动备份 JSON 文件

### Q2: 如何重新开始新项目？

**A:** 有两个方式：

```bash
# 方式 1：使用 CLI 命令
👤 You: clear
# 这会清空对话历史，但保留已生成的文件

# 方式 2：手动删除历史文件
rm -rf .conversation_history/current_session.json
```

### Q3: 如何导出生成的代码？

**A:** 生成的代码已经保存在 `workspace/` 目录：

```bash
# 查看生成的文件
ls workspace/

# 复制到其他位置
cp -r workspace/ ~/my-project

# 打包下载
tar -czf my-project.tar.gz workspace/
```

### Q4: Agent 忘记了之前的需求怎么办？

**A:** 可以显式提醒 Agent：

```
👤 You: 还记得我们之前提到的 JWT 认证吗？我们还需要实现...
```

或者：
```
👤 You: 基于之前生成的 Flask 应用，现在添加...
```

### Q5: 如何查看完整的对话历史？

**A:**
```bash
# 方式 1：查看 JSON 文件
cat .conversation_history/current_session.json

# 方式 2：使用 Python
python3 -c "
import json
with open('.conversation_history/current_session.json') as f:
    data = json.load(f)
    for msg in data['messages']:
        print(f\"{msg['role'].upper()}: {msg['content'][:100]}...\")
"
```

### Q6: 如何在不同项目间切换对话？

**A:** 目前系统使用单一的 `current_session.json`。如果要管理多个项目：

```bash
# 保存当前项目对话
cp .conversation_history/current_session.json .conversation_history/project1.json

# 清空当前对话
👤 You: clear

# 之后可以手动恢复
cp .conversation_history/project1.json .conversation_history/current_session.json
```

### Q7: 生成的代码直接可用吗？

**A:** 大部分可用，但需要：

1. **安装依赖**：
   ```bash
   cd workspace
   pip install -r requirements.txt
   ```

2. **配置环境**：
   ```bash
   # 复制示例配置
   cp config.example.py config.py
   # 编辑 config.py 添加必要的配置
   ```

3. **运行应用**：
   ```bash
   # Flask 应用
   flask run
   
   # Django 应用
   python manage.py runserver
   
   # Python CLI
   python app.py
   ```

### Q8: 能否并行生成多个项目？

**A:** 可以。打开多个终端窗口：

```bash
# 终端 1
./cli.sh

# 终端 2
./cli.sh

# 每个终端有独立的对话历史和项目上下文
```

---

## 高级用法

### 链式生成

```
# 第一步：生成基础项目
👤 You: 生成一个 Flask 项目框架

# 第二步：逐步添加功能
👤 You: 添加数据库支持
👤 You: 添加用户认证
👤 You: 添加 API 文档
👤 You: 添加单元测试
👤 You: 生成 Docker 配置
```

### 对话式开发

```
# 讨论设计
👤 You: 应该用什么数据库？MongoDB 还是 PostgreSQL？
🤖 Agent: 根据你的需求...

# 基于讨论生成
👤 You: 好的，就用 PostgreSQL，现在生成代码
🤖 Agent: 我将使用 PostgreSQL 生成...

# 继续迭代
👤 You: 觉得这个设计如何？
```

### 学习模式

```
# 请求解释
👤 You: 解释一下生成的代码中的设计模式

# 请求优化建议
👤 You: 有什么方式可以优化这个 API 的性能？

# 请求最佳实践
👤 You: 遵循了哪些 Flask 最佳实践？
```

---

## 性能提示

1. **批量生成**：一次请求生成所有相关文件，比分次生成效率高
2. **上下文长度**：保持对话相关的消息在 50 条以内效果最佳
3. **API 调用**：尽可能减少不必要的查询，整合需求后再请求

---

## 故障排除

### CLI 无法启动

```bash
# 1. 检查 Python 版本
python3 --version  # 需要 3.9+

# 2. 检查依赖
pip list | grep -E 'openai|pydantic'

# 3. 验证 API Key
echo $LLM_API_KEY
```

### 生成代码失败

```bash
# 1. 检查 API 连接
python3 test_connection.py

# 2. 查看详细日志
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from interactive_cli import InteractiveCodeAgent
agent = InteractiveCodeAgent()
"

# 3. 检查 DeepSeek API 状态
curl https://api.deepseek.com/models \
  -H 'Authorization: Bearer $LLM_API_KEY'
```

### 对话历史损坏

```bash
# 备份损坏的文件
cp .conversation_history/current_session.json \
   .conversation_history/current_session.backup.json

# 清空重新开始
rm .conversation_history/current_session.json

# 重启 CLI
./cli.sh
```

---

## 最佳实践

✅ **DO:**
- 详细描述需求，提供背景信息
- 一步步地提出需求而不是一次性大量需求
- 在修改前检查当前状态
- 定期保存/导出重要的对话记录

❌ **DON'T:**
- 频繁切换主题（保持对话连贯）
- 一次性要求完成太复杂的任务
- 忽视生成代码的质量检查
- 泄露 API Key 到公开仓库

---

## 快捷参考

| 命令 | 效果 |
|------|------|
| `generate [description]` | 生成项目 |
| `create [description]` | 创建项目 |
| `improve [file]` | 改进文件 |
| `fix [issue]` | 修复问题 |
| `show status` | 查看状态 |
| `list files` | 列出文件 |
| `help` | 显示帮助 |
| `clear` | 清空历史 |
| `quit` | 退出 |

---

**现在开始使用 Code Agent 吧！** 🚀

```bash
./cli.sh
```

Happy coding! 💻
