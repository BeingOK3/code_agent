#!/usr/bin/env python3
"""Test interactive CLI workflow"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from interactive_cli import InteractiveCodeAgent

print("=" * 80)
print("🧪 测试交互式 CLI 代码生成流程")
print("=" * 80)

agent = InteractiveCodeAgent()

print("\n" + "=" * 80)
print("📝 第一个请求：生成快速排序代码")
print("=" * 80)

response1 = agent.process_user_input("生成一个快速排序算法的完整实现")
print("\n🤖 Agent 响应:")
print(response1)

print("\n" + "=" * 80)
print("📋 检查生成的文件...")
print("=" * 80)

import os
workspace_dir = Path("/Users/hushuai/Desktop/项目/code_agent/workspace")

# 列出最近的会话目录
session_dirs = [d for d in workspace_dir.iterdir() if d.is_dir() and d.name.startswith("20")]
if session_dirs:
    latest_session = sorted(session_dirs)[-1]
    print(f"\n最新的会话: {latest_session.name}")
    print(f"路径: {latest_session}")
    
    # 列出文件
    files = list(latest_session.glob("**/*"))
    files = [f for f in files if f.is_file()]
    
    if files:
        print(f"\n生成的文件数: {len(files)}")
        for f in files:
            rel = f.relative_to(latest_session)
            size = f.stat().st_size
            print(f"  ✓ {rel} ({size} 字节)")
            
            # 显示前几行代码
            if f.suffix in ['.py']:
                with open(f, 'r') as file:
                    lines = file.readlines()[:3]
                    print(f"    预览:")
                    for line in lines:
                        print(f"      {line.rstrip()}")
    else:
        print("✗ 没有找到生成的文件!")
else:
    print("✗ 没有找到会话目录!")

print("\n" + "=" * 80)
print("✅ CLI 测试完成")
print("=" * 80)
