#!/usr/bin/env python3
"""
Interactive Code Agent - Demo Script
演示交互式 CLI 的核心功能
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from interactive_cli import InteractiveCodeAgent
from tools.file_tools import FileTools


def print_header(title):
    """打印标题"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def demo_conversation():
    """演示多轮对话功能"""
    print_header("🎬 Code Agent 交互式 CLI 演示")
    
    print("初始化 Code Agent...")
    agent = InteractiveCodeAgent()
    print("✓ 初始化完成！\n")
    
    # 模拟对话
    demo_messages = [
        {
            "user": "生成一个 Flask REST API，用于任务管理系统",
            "description": "【第一步】生成基础项目"
        },
        {
            "user": "显示当前项目状态",
            "description": "【第二步】查看项目信息"
        },
        {
            "user": "能否添加数据库支持？",
            "description": "【第三步】请求功能改进"
        },
        {
            "user": "添加用户认证功能",
            "description": "【第四步】继续添加功能"
        },
        {
            "user": "显示工作区文件列表",
            "description": "【第五步】查看生成的文件"
        },
    ]
    
    for i, msg_data in enumerate(demo_messages, 1):
        print(f"\n{msg_data['description']}")
        print(f"{'─'*70}")
        
        user_msg = msg_data["user"]
        print(f"👤 You: {user_msg}")
        
        try:
            response = agent.process_user_input(user_msg)
            
            # 截断长响应用于演示
            display_response = response
            if len(response) > 300:
                display_response = response[:300] + "\n... (response truncated for demo) ..."
            
            print(f"\n🤖 Agent:\n{display_response}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")
    
    # 显示最终统计
    print_header("📊 对话统计")
    print(agent.conversation_manager.get_summary())
    
    # 显示工作区信息
    print_header("📁 工作区信息")
    workspace_info = FileTools.get_workspace_info()
    print(f"✓ 工作区路径: {workspace_info.get('workspace_dir', 'unknown')}")
    print(f"✓ 文件总数: {workspace_info.get('file_count', 0)}")
    print(f"\n生成的文件样本:")
    files = workspace_info.get('files', [])
    for file in files[:5]:
        print(f"  - {file}")
    if len(files) > 5:
        print(f"  ... 和 {len(files) - 5} 个其他文件")
    
    # 显示对话历史
    print_header("💬 完整对话历史")
    messages = agent.conversation_manager.messages
    for msg in messages:
        role = msg["role"].upper()
        content = msg["content"]
        if len(content) > 100:
            content = content[:100] + "..."
        print(f"{role}: {content}")
    
    # 显示功能说明
    print_header("✨ 核心功能演示总结")
    print("""
✅ 【多轮对话】
   - 每条消息都被记录和保存
   - Agent 能够理解对话上下文
   - 支持渐进式需求提升

✅ 【意图识别】
   - 自动识别用户命令类型
   - 路由到适当的处理器
   - 灵活的自然语言理解

✅ 【完整记忆】
   - 所有对话保存到 JSON
   - 支持对话恢复和导出
   - 项目上下文自动追踪

✅ 【代码生成】
   - 基于历史生成代码
   - 支持修改和改进
   - 自动文件保存到工作区

✅ 【状态管理】
   - 项目信息实时更新
   - 文件计数和统计
   - 对话历史完整记录
    """)
    
    # 显示使用提示
    print_header("🚀 开始使用")
    print("""
启动交互式 CLI:
  ./cli.sh
  或
  python3 interactive_cli.py

对话示例:
  👤 You: 生成一个 Python 爬虫项目
  👤 You: 添加代理支持
  👤 You: 显示当前进度
  👤 You: 改进错误处理
  👤 You: quit

查看详细文档:
  - README_INTERACTIVE.md (功能和架构)
  - INTERACTIVE_TUTORIAL.md (完整使用指南)
    """)
    
    print(f"\n{'='*70}")
    print("✅ 演示完成！现在你可以开始使用交互式 Code Agent 了。")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    try:
        demo_conversation()
    except KeyboardInterrupt:
        print("\n\n👋 演示被中断")
    except Exception as e:
        print(f"\n❌ 演示出错: {e}")
        import traceback
        traceback.print_exc()
