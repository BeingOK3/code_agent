# 📖 Code Agent CLI 完整使用指南

## 🎯 快速开始

### 1. 启动 Agent
```bash
./cli.sh
```

### 2. 请求代码生成

Agent 会自动识别以下类型的请求为**代码生成**：

#### ✅ 包含生成动词的请求
```
👤 You: 生成一个快速排序算法
👤 You: 创建一个 Flask Web 应用
👤 You: 编写一个登录系统
👤 You: 实现一个计算器
👤 You: 构建一个 REST API
👤 You: 开发一个聊天机器人

👤 You: Generate a binary search algorithm
👤 You: Create a Python web scraper
👤 You: Write a todo app
👤 You: Implement a chat system
```

#### ✅ 不包含动词但包含代码术语的请求（新增功能！）
```
👤 You: 快速排序算法
👤 You: Flask Web 应用
👤 You: 登录系统
👤 You: 二进制搜索
👤 You: REST API
👤 You: Python 爬虫
👤 You: 排序算法
```

#### ✅ 支持的代码相关术语
- 中文：算法、代码、函数、类、方法、API、库、框架、应用、应用程序、系统、工具
- 英文：code、algorithm、function、class、method、api、library、framework、app、system、tool

### 3. 查看生成的代码

```bash
# 查看所有生成的项目
ls workspace/

# 进入最新的生成会话
cd workspace/20251213_221953_Python_QuickSort_Algorithm_Imp/

# 列出生成的文件
ls -la

# 查看代码内容
cat src/quicksort.py
```

### 4. 运行生成的代码

```bash
# 进入项目目录
cd workspace/20251213_221953_Python_QuickSort_Algorithm_Imp/

# 安装依赖（如果需要）
pip install -r requirements.txt

# 运行代码
python src/quicksort.py
```

---

## 🏗️ 文件夹结构

每次生成会自动创建一个时间戳文件夹：

```
workspace/
├── 20251213_220934_QuickSort_Algorithm/
│   ├── quick_sort.py
│   └── ...
│
├── 20251213_221953_Python_QuickSort_Algorithm_Imp/
│   ├── src/
│   │   ├── quicksort.py
│   │   └── visualizer.py
│   ├── tests/
│   └── requirements.txt
│
└── 其他生成的项目...
```

### 文件夹名称规则

```
YYYYmmdd_HHmmss_ProjectName

例：20251213_221953_Python_QuickSort_Algorithm_Imp
    ├─ 20251213    (2025年12月13日)
    ├─ 221953      (22时19分53秒)
    └─ Python_QuickSort_Algorithm_Imp (项目名称)
```

---

## 💡 使用示例

### 示例 1：快速排序算法

**请求：**
```
👤 You: 快速排序算法
```

**系统响应：**
```
🤖 Agent:
   📋 Project Plan:
   - Name: QuickSort Algorithm
   - Files to generate: 3
   - Tech Stack: Python
   
   📁 New generation session: 20251213_221953_QuickSort_Algorithm
      Location: workspace/20251213_221953_QuickSort_Algorithm
   
   💻 Generating code...
   ✓ Saved file: workspace/20251213_221953_QuickSort_Algorithm/quicksort.py
   ✓ Saved file: workspace/20251213_221953_QuickSort_Algorithm/test_quicksort.py
   
   ✅ Generated 2 files successfully!
   📁 Files saved to: `workspace/QuickSort_Algorithm/`
```

**查看文件：**
```bash
$ ls workspace/20251213_221953_QuickSort_Algorithm/
quicksort.py         test_quicksort.py

$ cat workspace/20251213_221953_QuickSort_Algorithm/quicksort.py
# 快速排序实现...
```

### 示例 2：Flask Web 应用

**请求：**
```
👤 You: 创建一个 Flask Web 应用，包括用户认证和数据库
```

**系统会自动：**
1. 生成项目计划
2. 创建会话文件夹（如 `20251213_2220_Flask_Web_App`）
3. 生成多个文件（app.py, models.py, requirements.txt 等）
4. 保存到会话文件夹中

### 示例 3：二进制搜索

**请求：**
```
👤 You: 二进制搜索
```

**系统会识别为代码生成请求，并生成相关代码。**

---

## ❓ 常见问题

### Q: 我的代码在哪里？
**A:** 在 `workspace/` 目录中，具体位置是：
```
workspace/YYYYmmdd_HHmmss_ProjectName/
```

### Q: 为什么我看不到生成的代码？
**A:** 可能的原因：
1. 代码还在生成中（看进度提示）
2. 生成出错（查看错误信息）
3. 看错了文件夹（确保看的是时间戳文件夹）

**解决方法：**
```bash
# 列出所有生成的项目
ls -lt workspace/ | grep "^d" | head -5

# 查看最新项目的文件
ls workspace/$(ls -t workspace/ | grep "^20" | head -1)/
```

### Q: 可以生成多个项目吗？
**A:** 可以！每次生成都会创建一个新的时间戳文件夹，所以：
- ✅ 可以生成多个不同的项目
- ✅ 不会相互覆盖
- ✅ 可以并行请求多个生成
- ✅ 所有代码都保存在 workspace 中

### Q: 如何清理旧的生成文件？
**A:** 
```bash
# 删除特定的生成会话
rm -rf workspace/20251213_220934_QuickSort_Algorithm/

# 删除 7 天前的所有生成（谨慎操作）
find workspace -maxdepth 1 -type d -name "20*" -mtime +7 -exec rm -rf {} \;
```

### Q: 可以修改已生成的代码吗？
**A:** 可以！有两种方式：

**方式 1：直接编辑文件**
```bash
# 编辑生成的代码
nano workspace/20251213_221953_QuickSort_Algorithm/quicksort.py

# 保存修改
```

**方式 2：请求 Agent 修改**
```
👤 You: 改进快速排序的性能
👤 You: 在之前的代码基础上添加错误处理
```

---

## 🎓 意图识别规则

Agent 使用以下规则识别你的请求：

### 规则 1：生成动词关键词
**触发词：** generate, create, build, make, write, implement, 生成, 创建, 编写, 实现, 构建, 开发

```
"生成一个快速排序" ✅ → 代码生成
"创建一个 Web 应用" ✅ → 代码生成
"写一个登录系统" ✅ → 代码生成
```

### 规则 2：代码相关术语检测
**触发词：** 算法、代码、函数、类、方法、API、库、框架、应用等

```
"快速排序" ✅ → 代码生成（包含"算法"的同义词）
"Flask Web 应用" ✅ → 代码生成（包含"应用"）
"REST API" ✅ → 代码生成（包含"API"）
```

### 规则 3：修改动词
**触发词：** modify, change, improve, fix, update

```
"修改之前的代码" → 代码修改请求
"改进性能" → 代码修改请求
```

### 规则 4：查询信息
**触发词：** status, info, show, list, what

```
"显示项目状态" → 信息查询
"列出生成的文件" → 信息查询
```

---

## 📋 命令参考

| 操作 | 命令 |
|------|------|
| 启动 Agent | `./cli.sh` |
| 查看所有生成 | `ls workspace/` |
| 进入最新项目 | `cd workspace/$(ls -t workspace \| grep "^20" \| head -1)/` |
| 查看文件列表 | `ls workspace/20251213_221953_QuickSort_Algorithm/` |
| 运行生成的代码 | `python workspace/20251213_221953_QuickSort_Algorithm/quicksort.py` |
| 删除一个生成 | `rm -rf workspace/20251213_221953_QuickSort_Algorithm/` |
| 最近的 5 个生成 | `ls -lt workspace/ \| grep "^d" \| head -5` |

---

## ✨ 新功能

### 改进的意图识别（最新更新 🆕）

现在 Agent 可以识别：

1. **明确的生成请求**
   ```
   "生成快速排序" → ✅ 自动生成代码
   ```

2. **隐含的生成请求**
   ```
   "快速排序" → ✅ 检测到代码术语，自动生成
   "Flask 应用" → ✅ 检测到应用术语，自动生成
   "算法实现" → ✅ 检测到算法术语，自动生成
   ```

3. **多语言支持**
   ```
   "生成快速排序" (中文) → ✅ 生成
   "Generate QuickSort" (英文) → ✅ 生成
   ```

---

## 🚀 最佳实践

### ✅ 推荐做法
1. 使用清晰的描述（越具体越好）
   ```
   ✅ "生成一个快速排序算法，包括单元测试"
   ✓ "快速排序算法"
   ```

2. 说明需求和约束
   ```
   ✅ "生成一个 Python 计算器，支持加减乘除"
   ✓ "计算器"
   ```

3. 查看生成的代码再使用
   ```bash
   ✅ 查看文件 → 检查代码 → 运行测试 → 使用代码
   ```

### ❌ 避免做法
1. ❌ 太模糊的描述
   ```
   "程序" (太模糊)
   "东西" (太模糊)
   ```

2. ❌ 不说明技术栈
   ```
   "web 应用" (应该说 Flask/Django/React)
   ```

3. ❌ 期望一行命令生成整个项目
   ```
   "整个电商系统" (可以，但会很复杂，建议分步骤)
   ```

---

## 📱 完整工作流示例

```bash
# 1. 启动 Agent
$ ./cli.sh

Code Agent initialized (conversation-aware mode)

# 2. 请求第一个生成
👤 You: 生成一个快速排序算法

🤖 Agent:
   📁 New generation session: 20251213_221953_QuickSort_Algorithm
   ✓ Saved file: workspace/20251213_221953_QuickSort_Algorithm/quicksort.py
   ✅ Generated 1 files successfully!

# 3. 请求第二个生成
👤 You: 二进制搜索实现

🤖 Agent:
   📁 New generation session: 20251213_221954_Binary_Search
   ✓ Saved file: workspace/20251213_221954_Binary_Search/binary_search.py
   ✅ Generated 1 files successfully!

# 4. 查看生成的项目
👤 You: 显示生成的项目

🤖 Agent:
   已生成的项目：
   - 20251213_221953_QuickSort_Algorithm
   - 20251213_221954_Binary_Search

# 5. 在终端中检查文件
$ ls workspace/
20251213_221953_QuickSort_Algorithm/
20251213_221954_Binary_Search/

$ cat workspace/20251213_221953_QuickSort_Algorithm/quicksort.py
# 快速排序实现...

# 6. 运行代码
$ python workspace/20251213_221953_QuickSort_Algorithm/quicksort.py
# 程序运行...
```

---

## 🔧 故障排除

### 问题：代码没有保存
**检查清单：**
1. ✓ 确保 workspace 目录存在
2. ✓ 检查是否有文件夹被创建（ls workspace/）
3. ✓ 查看是否有错误信息
4. ✓ 检查磁盘空间

### 问题：生成速度慢
**原因可能：**
- LLM API 响应慢（网络问题）
- 生成任务太复杂
- 系统资源不足

**解决方法：**
- 请求更简单的代码
- 检查网络连接
- 使用更快的模型

### 问题：生成的代码有错误
**处理步骤：**
1. 查看生成的代码
2. 在 CLI 中请求改进
3. 运行修复后的代码

```
👤 You: 修复之前生成的快速排序代码中的错误
```

---

## 📞 需要帮助？

查看这些文档：
- **README.md** - 项目完整文档
- **STARTUP_GUIDE.md** - 启动指南
- **SESSION_GENERATION_GUIDE.md** - 会话化代码生成说明
- **IMPLEMENTATION_SUMMARY.md** - 实现总结

或者在 CLI 中输入：
```
👤 You: help
```

---

**现在你已经准备好使用 Code Agent 了！开始请求代码生成吧！** 🚀
