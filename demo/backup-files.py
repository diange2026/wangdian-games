#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件备份小工具 - 小 Q 出品
用途：把一个文件夹里的所有文件复制到另一个文件夹
用法：python backup-files.py
"""

import os
import shutil
from datetime import datetime

def backup_files(source_folder, backup_folder):
    """
    备份文件函数
    source_folder: 要备份的文件夹
    backup_folder: 备份到的文件夹
    """
    print("=" * 50)
    print("📦 文件备份小工具")
    print("=" * 50)
    
    # 检查源文件夹是否存在
    if not os.path.exists(source_folder):
        print(f"❌ 错误：源文件夹不存在：{source_folder}")
        return
    
    # 创建备份文件夹（如果不存在）
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
        print(f"✅ 创建备份文件夹：{backup_folder}")
    
    # 获取当前时间（用于备份文件名）
    time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 统计文件数量
    file_count = 0
    
    # 遍历源文件夹
    print(f"\n📂 开始备份：{source_folder}")
    print(f"📁 备份到：{backup_folder}\n")
    
    for filename in os.listdir(source_folder):
        source_file = os.path.join(source_folder, filename)
        backup_file = os.path.join(backup_folder, f"{time_str}_{filename}")
        
        # 跳过文件夹，只备份文件
        if os.path.isfile(source_file):
            shutil.copy2(source_file, backup_file)
            file_count += 1
            print(f"  ✅ {filename}")
    
    print("\n" + "=" * 50)
    print(f"🎉 备份完成！共备份 {file_count} 个文件")
    print("=" * 50)

if __name__ == "__main__":
    # 示例用法
    print("\n欢迎使用文件备份小工具！\n")
    print("这个脚本可以帮你把文件从一个地方复制到另一个地方。")
    print("适合用来做重要文件的备份。\n")
    
    # 你可以修改下面的路径来备份你的文件
    # 比如：备份你的文档到 U 盘
    source = input("请输入要备份的文件夹路径（直接回车使用示例路径）：").strip()
    backup = input("请输入备份到的文件夹路径（直接回车使用示例路径）：").strip()
    
    # 如果没输入，使用示例路径
    if not source:
        source = "./documents"  # 示例：当前目录下的 documents 文件夹
    if not backup:
        backup = "./backup"     # 示例：当前目录下的 backup 文件夹
    
    backup_files(source, backup)
    
    print("\n💡 提示：")
    print("   - 可以修改上面的路径来备份你的文件")
    print("   - 建议定期备份重要文件")
    print("   - 备份到 U 盘或云盘更安全\n")
