# Code Agent - Multi-Agent Collaborative Software Development System

一个能够进行**多轮对话交互**、具有**完整记忆机制**的智能代码生成系统。类似于 ChatGPT 的对话方式，但专门优化用于软件开发。

> **核心能力**: 接收自然语言需求 → 自动规划 → 生成完整代码 → 记忆迭代 → 基于反馈改进

## 🎯 快速开始

### 1️⃣ 方式一：交互式 CLI（推荐）

**进行多轮对话，就像在聊天一样！**

```bash
# 启动交互式命令行界面
./cli.sh

# 或直接运行
python3 interactive_cli.py
```

**对话示例：**
```
👤 You: 给我生成一个 Flask REST API，用于用户管理
🤖 Agent: [生成代码和规划]

👤 You: 能加上 JWT 认证吗？
🤖 Agent: [根据之前的对话历史修改代码]

👤 You: 显示当前状态
🤖 Agent: [显示项目信息和生成的文件]

👤 You: 改进一下数据验证逻辑
🤖 Agent: [基于整个对话上下文改进代码]
```

### 2️⃣ 方式二：一次性生成

```bash
# 生成完整项目
python3 main.py
```

## 💡 交互式 CLI 命令

### 生成代码
```
👤 You: Generate a Flask REST API for task management
👤 You: Create a React todo app with TypeScript
👤 You: Build a Django e-commerce platform
```

### 修改代码
```
👤 You: Add JWT authentication
👤 You: Improve error handling in app.py
👤 You: Fix the database validation
```

### 查看信息
```
👤 You: Show status
👤 You: List files
👤 You: What's been done?
```

### 系统命令
```
👤 You: Help              # 显示帮助
👤 You: Clear             # 清空历史
👤 You: Status            # 项目状态
👤 You: Quit              # 退出
```

## 🏗️ 系统架构

```
┌─────────────────────────────────────────┐
│   Interactive CLI (interactive_cli.py)  │
│   ↓ Multi-turn conversation interface   │
├─────────────────────────────────────────┤
│   Conversation Manager (memory layer)   │
│   ↓ Maintains full conversation history │
├─────────────────────────────────────────┤
│   Three-Phase Orchestrator (main.py)    │
│   ├─ Phase 1: PlannerAgent (规划)      │
│   ├─ Phase 2: CoderAgent (代码生成)    │
│   └─ Phase 3: Summary (总结)           │
├─────────────────────────────────────────┤
│   LLM Client (utils/llm_client.py)      │
│   ↓ DeepSeek API Integration            │
├─────────────────────────────────────────┤
│   File Tools (tools/file_tools.py)      │
│   ↓ Workspace management & persistence  │
└─────────────────────────────────────────┘
```

## 📦 核心组件

| 组件 | 职责 | 特点 |
|------|------|------|
| **PlannerAgent** | 将需求转化为结构化项目规划 | 生成 JSON 格式的项目计划 |
| **CoderAgent** | 根据规划生成完整的可执行代码 | 支持多种编程语言，Markdown 提取 |
| **ConversationManager** | 管理多轮对话历史和上下文 | JSON 持久化，完整记忆 |
| **LLMClient** | 统一的 LLM API 接口 | DeepSeek 集成，错误处理 |
| **FileTools** | 工作空间文件管理 | 安全隔离，版本跟踪 |

## 🔄 对话流程

```
用户输入
    ↓
对话管理器保存 & 提取历史
    ↓
意图识别 (生成/修改/查询/系统命令)
    ↓
┌─ 生成请求 → PlannerAgent → CoderAgent → 生成代码
├─ 修改请求 → 根据历史改进代码
├─ 查询请求 → 显示项目状态
└─ 系统命令 → 清空/重置/帮助
    ↓
对话管理器保存响应
    ↓
显示给用户 + 保存到文件
```

## ⚙️ 环境设置

```bash
# 1. 创建虚拟环境 (使用 uv)
uv venv

# 2. 激活虚拟环境
source .venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置 API Key
cp .env.example .env
# 编辑 .env，添加你的 DeepSeek API Key
# LLM_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

## 📁 项目结构

```
code_agent/
├── interactive_cli.py          # 交互式命令行界面 🆕
├── cli.sh                      # CLI 启动脚本 🆕
├── main.py                     # 一次性项目生成
├── config.py                   # 配置管理
├── agents/
│   ├── planner.py             # 规划 Agent
│   ├── coder.py               # 代码生成 Agent
│   └── conversation_manager.py # 对话管理（记忆层）
├── tools/
│   └── file_tools.py          # 文件操作工具
├── utils/
│   └── llm_client.py          # LLM 客户端
├── workspace/                 # 生成的代码存放处
├── .conversation_history/     # 对话历史保存 🆕
├── requirements.txt           # Python 依赖
└── .gitignore                # Git 忽略配置
```

## 🚀 使用示例

### 示例 1：交互式生成 Flask API

```bash
$ ./cli.sh

🚀 Code Agent - Interactive Multi-Turn Conversation Mode
======================================================================

Welcome! I can generate code, modify files, and remember our conversation.
Type 'help' for commands or start chatting!

👤 You: 生成一个 Flask REST API 用来管理用户

🤖 Agent: 我将为你创建一个完整的 Flask REST API 实现，包括 CRUD 操作...
[生成代码]

👤 You: 能否添加 JWT 认证？

🤖 Agent: 基于我们之前的对话，我将添加 JWT 认证功能...
[修改代码]

👤 You: 显示状态

🤖 Agent: 📊 **项目信息:**
- 消息数: 3
- 文件生成: 2
- 工作空间文件: 23
```

### 示例 2：一次性项目生成

```bash
$ python3 main.py

[Phase 1: Planning]
📋 Generate project plan...
✅ Plan created: 11 files planned

[Phase 2: Code Generation]
💻 Generating code...
✅ 11/11 files generated successfully

[Phase 3: Summary]
📊 Statistics:
- Files Planned: 11
- Files Generated: 11
- Total Size: 262 KB
```

## 📊 对话历史管理

对话历史自动保存到 `.conversation_history/current_session.json`：

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
      "content": "我将生成完整的 Flask API...",
      "timestamp": "2024-01-15T10:30:50.234567"
    }
  ],
  "project_context": {
    "project_name": "Task Management API",
    "files_generated": 5,
    "tech_stack": ["Python", "Flask", "SQLAlchemy"]
  }
}
```

## 🔑 配置 API Key

1. **获取 DeepSeek API Key**：访问 https://platform.deepseek.com
2. **创建 `.env` 文件**：
   ```
   LLM_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
   LLM_MODEL=deepseek-chat
   LLM_BASE_URL=https://api.deepseek.com
   WORKSPACE_DIR=./workspace
   ```
3. **验证连接**：
   ```bash
   python3 -c "from config import Config; c = Config(); print('✓ API Key validated')"
   ```

## ✨ 主要特性

✅ **多轮对话**：像聊天一样与 AI 交互  
✅ **完整记忆**：保存所有对话历史和上下文  
✅ **智能规划**：自动生成项目结构和文件列表  
✅ **代码生成**：从 Markdown 提取代码，支持多种语言  
✅ **意图识别**：自动识别用户命令（生成/修改/查询）  
✅ **持久化**：JSON 格式保存对话和项目状态  
✅ **安全隔离**：工作空间隔离，避免覆盖重要文件  
✅ **错误恢复**：完整的异常处理和恢复机制  

## 🧪 测试验证

```bash
# 运行连接测试
python3 test_connection.py

# 运行规划 Agent 测试
python3 test_planner.py

# 运行代码生成测试
python3 test_coder.py

# 运行文件工具测试
python3 test_file_tools.py

# 运行集成测试
python3 test_agent_integration.py
```

## 🛠️ 技术栈

- **Python 3.11+**
- **OpenAI SDK** (DeepSeek API 兼容)
- **Pydantic** (数据验证)
- **python-dotenv** (环境配置)
- **Flask** (生成的项目框架)

## 📝 对话记忆的工作原理

1. **消息存储**：每条用户/AI 消息都带时间戳保存
2. **上下文提取**：最近 10 条消息 + 项目上下文传给 LLM
3. **意图识别**：根据关键词识别用户意图
4. **持久化**：JSON 文件自动保存，支持对话恢复
5. **上下文感知**：Agent 能引用之前的决策和生成的代码

## 🐛 故障排除

### API 连接失败
```bash
# 检查 API Key
echo $LLM_API_KEY

# 验证网络
curl https://api.deepseek.com/chat/completions -H "Authorization: Bearer $LLM_API_KEY"
```

### 对话历史丢失
```bash
# 检查历史文件
ls -la .conversation_history/

# 查看最近的对话
cat .conversation_history/current_session.json
```

### 代码生成失败
- 检查 Markdown 格式是否正确
- 确保 LLM 响应包含代码块
- 查看日志输出了解详细错误

## 🎓 学习资源

- [DeepSeek API 文档](https://platform.deepseek.com/docs)
- [OpenAI SDK 参考](https://github.com/openai/openai-python)
- [Pydantic 数据验证](https://docs.pydantic.dev/)

## 📄 许可证

MIT License - 自由使用和修改

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**Made with ❤️ for AI-Powered Software Development**

**现在就开始吧！** 🚀
```bash
./cli.sh
```
