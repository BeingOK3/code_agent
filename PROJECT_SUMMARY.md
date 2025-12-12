# Code Agent - 交互式 AI 代码生成系统 🚀

> **一个能够进行多轮对话的智能代码生成系统，像 ChatGPT 一样交互，但专门用于软件开发**

## ⭐ 项目完成度：100%

### ✅ 已实现功能

**核心功能**
- ✅ 多轮对话交互界面（CLI）
- ✅ 完整对话记忆和持久化
- ✅ 智能意图识别和路由
- ✅ 自动代码规划和生成
- ✅ 支持多种编程语言

**代理系统**
- ✅ PlannerAgent - 项目规划
- ✅ CoderAgent - 代码生成
- ✅ ConversationManager - 对话管理
- ✅ Orchestrator - 系统协调

**开发者工具**
- ✅ LLMClient - 统一 LLM 接口
- ✅ FileTools - 文件管理
- ✅ Config - 配置管理
- ✅ 完整的测试套件

**文档**
- ✅ QUICKSTART.md - 5分钟快速开始
- ✅ INTERACTIVE_TUTORIAL.md - 完整使用指南
- ✅ README_INTERACTIVE.md - 功能说明
- ✅ demo_interactive.py - 交互演示

---

## 🎯 快速开始（3 步）

### 1️⃣ 启动 CLI
```bash
./cli.sh
# 或
python3 interactive_cli.py
```

### 2️⃣ 开始对话
```
👤 You: 生成一个 Flask REST API 用于用户管理
🤖 Agent: [自动规划和生成代码]

👤 You: 添加数据库支持
🤖 Agent: [根据历史改进代码]
```

### 3️⃣ 查看生成的文件
```bash
ls workspace/
# 所有生成的代码都在这里
```

---

## 📁 项目结构

```
code_agent/
├── 📄 核心应用
│   ├── main.py                    # 一次性项目生成 Orchestrator
│   ├── interactive_cli.py         # 🆕 交互式多轮对话界面
│   ├── config.py                  # 配置管理
│   └── cli.sh                     # 🆕 启动脚本
│
├── 🤖 代理模块 (agents/)
│   ├── planner.py                 # 项目规划 Agent
│   ├── coder.py                   # 代码生成 Agent
│   └── conversation_manager.py    # 🆕 对话管理（记忆层）
│
├── 🔧 工具模块 (tools/)
│   └── file_tools.py              # 文件管理工具
│
├── 🛠️ 工具类 (utils/)
│   ├── llm_client.py              # LLM API 客户端
│   └── examples.py                # 使用示例
│
├── 🧪 测试 (5 个完整测试)
│   ├── test_connection.py
│   ├── test_planner.py
│   ├── test_coder.py
│   ├── test_file_tools.py
│   └── test_agent_integration.py
│
├── 📚 文档
│   ├── QUICKSTART.md              # 🆕 快速开始指南
│   ├── INTERACTIVE_TUTORIAL.md    # 🆕 完整使用教程
│   └── README_INTERACTIVE.md      # 🆕 功能说明
│
├── 📊 演示
│   └── demo_interactive.py        # 🆕 交互式演示
│
└── 💾 工作空间 (workspace/)
    └── [21 个生成的文件]          # 自动生成的代码
```

---

## 💡 核心特性

| 特性 | 说明 |
|------|------|
| **多轮对话** | 像聊天一样交互，支持无限轮次 |
| **完整记忆** | 每条消息都被保存和记忆 |
| **意图识别** | 自动识别生成/修改/查询命令 |
| **智能规划** | 自动生成项目结构和文件列表 |
| **代码生成** | 生成生产级别的完整代码 |
| **渐进改进** | 基于反馈逐步完善代码 |
| **多语言支持** | Python, JavaScript, Java, Go 等 |
| **生产就绪** | 符合最佳实践的代码生成 |

---

## 🔄 工作流程

```
┌─ 用户输入 ─┐
│  (自然语言) │
└──────┬──────┘
       │
       ▼
  对话管理器
  (保存和提取历史)
       │
       ▼
   意图识别
   ├─ 生成? → PlannerAgent → CoderAgent → 文件
   ├─ 修改? → 根据历史改进代码 → 文件
   ├─ 查询? → 显示状态/文件/历史
   └─ 系统? → 清空/帮助/退出
       │
       ▼
  保存响应到历史
       │
       ▼
  显示给用户
```

---

## 📊 项目统计

- **代码文件**: 10 个 Python 模块
- **测试覆盖**: 5 个完整测试文件
- **文档**: 3 个 Markdown 文档 + 演示脚本
- **生成文件**: 21 个示例生成文件在 workspace/
- **代码行数**: 2000+ 行生产级代码
- **Git 提交**: 10+ 次有意义的提交
- **API 集成**: DeepSeek (OpenAI 兼容)

---

## 🚀 使用示例

### 示例 1：生成 Flask API
```
👤 You: 生成一个 Flask REST API，支持用户认证和任务管理

🤖 Agent: 我将为你创建...
[自动规划 8 个文件]
[自动生成代码]
✅ 5 个文件生成成功

👤 You: 添加 JWT 认证

🤖 Agent: 基于之前的代码...
[改进代码添加认证]

👤 You: 生成测试代码

🤖 Agent: 我将生成单元测试...
[生成测试套件]

👤 You: 显示状态

🤖 Agent: 📊 项目信息:
- 消息: 4 条
- 文件: 8 个生成
- 大小: 89 KB
```

### 示例 2：优化现有代码
```
👤 You: 改进数据库查询性能

🤖 Agent: 我将添加数据库索引和缓存...

👤 You: 添加错误处理

🤖 Agent: 我将改进异常处理...

👤 You: 生成 API 文档

🤖 Agent: 我将添加 Swagger/OpenAPI 文档...
```

---

## 📝 命令参考

### 生成命令
```
生成 [项目描述]
创建 [项目描述]
构建 [项目描述]
```

### 修改命令
```
添加 [功能描述]
改进 [文件/功能]
修复 [问题描述]
优化 [组件名称]
```

### 查询命令
```
显示状态
列出文件
显示进度
```

### 系统命令
```
help  # 帮助
clear # 清空历史
quit  # 退出
```

---

## 🧠 对话记忆机制

### 自动保存
- 每条消息都有时间戳
- JSON 格式持久化
- 位置：`.conversation_history/current_session.json`

### 上下文管理
- 最近 10 条消息用于 LLM 上下文
- 项目信息自动追踪
- 支持对话恢复

### 使用场景
- 多个对话 session 管理
- 项目进度追踪
- 决策历史记录

---

## 🔐 安全性

✅ API Key 管理
- `.env` 文件存储（已添加到 .gitignore）
- 环境变量隔离
- 不公开提交

✅ 文件隔离
- 生成代码在 workspace/ 内
- 不会覆盖重要文件
- 版本控制友好

✅ 错误处理
- 完整的异常捕获
- 用户友好的错误消息
- 日志记录

---

## 🛠️ 技术栈

- **Python**: 3.11+
- **LLM**: DeepSeek API (OpenAI 兼容)
- **框架**: OpenAI Python SDK
- **验证**: Pydantic
- **存储**: JSON 文件
- **环境**: python-dotenv

---

## 📖 文档

| 文档 | 内容 |
|------|------|
| **QUICKSTART.md** | 5 分钟快速开始 |
| **INTERACTIVE_TUTORIAL.md** | 完整使用指南（100+ 示例） |
| **README_INTERACTIVE.md** | 功能和架构说明 |
| **demo_interactive.py** | 运行演示：`python3 demo_interactive.py` |

---

## 🚀 现在就开始！

### 方式 1：一键启动（推荐）
```bash
./cli.sh
```

### 方式 2：直接运行
```bash
python3 interactive_cli.py
```

### 方式 3：查看演示
```bash
python3 demo_interactive.py
```

---

## 📊 完成情况检查清单

- ✅ 项目 scaffolding 完成
- ✅ 环境配置完成
- ✅ LLM 集成完成
- ✅ PlannerAgent 实现完成
- ✅ CoderAgent 实现完成
- ✅ 文件管理工具完成
- ✅ 系统 Orchestrator 完成
- ✅ 测试套件完成
- ✅ Git 集成完成
- ✅ 交互式 CLI 完成 🆕
- ✅ 对话管理系统完成 🆕
- ✅ 完整文档完成 🆕

**总体完成度: 100%** ✨

---

## 🎓 学习资源

- [DeepSeek API 文档](https://platform.deepseek.com/docs)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [Pydantic 文档](https://docs.pydantic.dev/)

---

## 📞 需要帮助？

1. **快速问题**: 查看 `QUICKSTART.md`
2. **详细教程**: 查看 `INTERACTIVE_TUTORIAL.md`
3. **功能说明**: 查看 `README_INTERACTIVE.md`
4. **看演示**: 运行 `python3 demo_interactive.py`
5. **在 CLI 内**: 输入 `help` 获取帮助

---

## 🎉 准备好了吗？

```bash
./cli.sh
```

**现在就开始你的 AI 驱动的代码生成之旅吧！** 🚀

---

**Made with ❤️ for AI-Powered Software Development**

*最后更新: 2024-01-15*  
*版本: 1.0 (完整版)*
