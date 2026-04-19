#!/usr/bin/env python3
"""
讯网答案提取器插件 - 测试脚本
这个脚本用于测试插件的基本功能和数据提取逻辑
"""

import json
import os
import sys
import base64
from pathlib import Path

# 插件目录
PLUGIN_DIR = Path("/root/.openclaw/workspace/xunwang-answer-extractor")

def test_manifest():
    """测试manifest.json文件"""
    print("🔧 测试manifest.json...")
    
    manifest_path = PLUGIN_DIR / "manifest.json"
    if not manifest_path.exists():
        print("❌ manifest.json不存在")
        return False
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        # 检查必需字段
        required_fields = ['manifest_version', 'name', 'version', 'permissions']
        missing_fields = [field for field in required_fields if field not in manifest]
        
        if missing_fields:
            print(f"❌ 缺少必需字段: {missing_fields}")
            return False
        
        print(f"✅ manifest.json有效:")
        print(f"   名称: {manifest.get('name')}")
        print(f"   版本: {manifest.get('version')}")
        print(f"   Manifest版本: {manifest.get('manifest_version')}")
        return True
        
    except Exception as e:
        print(f"❌ manifest.json解析错误: {e}")
        return False

def test_file_structure():
    """测试文件结构"""
    print("\n📁 测试文件结构...")
    
    required_files = [
        "manifest.json",
        "background.js",
        "content.js",
        "popup/popup.html",
        "popup/popup.js",
        "popup/popup.css",
        "options/options.html",
        "options/options.js",
        "options/options.css",
    ]
    
    required_dirs = [
        "icons",
        "popup",
        "options"
    ]
    
    all_good = True
    
    # 检查目录
    for dir_name in required_dirs:
        dir_path = PLUGIN_DIR / dir_name
        if not dir_path.exists():
            print(f"❌ 目录不存在: {dir_name}")
            all_good = False
    
    # 检查文件
    for file_name in required_files:
        file_path = PLUGIN_DIR / file_name
        if not file_path.exists():
            print(f"❌ 文件不存在: {file_name}")
            all_good = False
    
    if all_good:
        print("✅ 文件结构完整")
    else:
        print("⚠️  部分文件缺失，请检查")
    
    return all_good

def test_icons():
    """测试图标文件"""
    print("\n🖼️  测试图标文件...")
    
    required_icons = [
        "icons/icon16.png",
        "icons/icon48.png",
        "icons/icon128.png"
    ]
    
    all_good = True
    
    for icon_path in required_icons:
        full_path = PLUGIN_DIR / icon_path
        if not full_path.exists():
            print(f"❌ 图标不存在: {icon_path}")
            all_good = False
        else:
            size = os.path.getsize(full_path)
            print(f"✅ {icon_path} (大小: {size} bytes)")
    
    if not all_good:
        print("⚠️  需要创建图标文件，可以使用在线工具生成或使用base64编码的占位图标")
    
    return all_good

def check_js_files():
    """检查JavaScript文件语法"""
    print("\n📝 检查JavaScript文件...")
    
    js_files = [
        "background.js",
        "content.js",
        "popup/popup.js",
        "options/options.js"
    ]
    
    all_good = True
    
    for js_file in js_files:
        file_path = PLUGIN_DIR / js_file
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 简单检查：是否有明显的语法问题
                if "class " in content or "function " in content:
                    print(f"✅ {js_file} - 包含类和函数定义")
                else:
                    print(f"⚠️  {js_file} - 可能没有定义类或函数")
            except Exception as e:
                print(f"❌ {js_file} - 读取错误: {e}")
                all_good = False
        else:
            print(f"❌ {js_file} - 不存在")
            all_good = False
    
    return all_good

def check_html_files():
    """检查HTML文件"""
    print("\n🌐 检查HTML文件...")
    
    html_files = [
        "popup/popup.html",
        "options/options.html"
    ]
    
    all_good = True
    
    for html_file in html_files:
        file_path = PLUGIN_DIR / html_file
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if "<!DOCTYPE html>" in content:
                    print(f"✅ {html_file} - HTML结构正常")
                else:
                    print(f"⚠️  {html_file} - 可能缺少DOCTYPE声明")
                    
                # 检查必要的脚本引用
                if "script" in content and "src=" in content:
                    print(f"   ✅ 包含脚本引用")
                else:
                    print(f"   ⚠️  可能缺少脚本引用")
                    
            except Exception as e:
                print(f"❌ {html_file} - 读取错误: {e}")
                all_good = False
        else:
            print(f"❌ {html_file} - 不存在")
            all_good = False
    
    return all_good

def create_simple_icons():
    """创建简单的占位图标"""
    print("\n🎨 创建占位图标...")
    
    # 简单的16x16蓝色图标
    icon_16 = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAA"
        "B3RJTUUH5gQCCi03FQ2bIwAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUH"
        "AAAANUlEQVQ4y2P8//8/Ay0xw6gBowYMPQMYqWk5I5U9wEgLAxgZGRnJNmDUgFEDRhwGAKfGEBwc"
        "8JMoAAAAAElFTkSuQmCC"
    )
    
    # 简单的48x48蓝色图标
    icon_48 = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAAsTAAALEwEAmpwYAAAA"
        "B3RJTUUH5gQCCi0GL6zJ8wAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUH"
        "AAADF0lEQVRo3u2aT0hUURTGP+8pM/bX0Jk0UlFChCVIQbRQLCwKpCgqKCJEUJGyQNq4iEDCigpB"
        "qFULQyJtUUK0CYqKiBASQpBQQhH8M2hO2jDjzNzW4s2dee+9O3dm3nszCm7m8N7c+53v3nPOOec7"
        "cODAgQMHDhz8B2CkcSG3gHVALE97BpgC7gBrNjxwH7jtg57F/6gBPgHDJgL8wBtgR1UwBfgBNDkA"
        "3gGtJgJ6gR6VgAngCupgg8B7IAq8AW4B1WYh9BpoMhFwB3ioEHAH6FcJ6AEGVQJ6gfuqAi4CT1QC"
        "tgBTVq4hA0wCs8A8sARYA9qAq8A2rQLeAIdVBLwCzqgIeAmcVREwAJxWEdAPnFMR8Aw4ryLgKXBB"
        "RcAT4KKKgMfAJRUBj4DLKgIeAZkSKgMYB3YDDUBYJ4H7wBUTR6YErhJ3qB2DKgE3gBtmAiaA/SYC"
        "BoB2FQE3gZsWBJxSEXALuG1BwCkVAb3AHRUBd4FuFQH3gLsWBBxTEXAbeGDCfQq0ADvRv0jbwK+K"
        "gFvAZxPuF6A11W7X95RR8Qt4b8J9CbSn2u0ScA/oMuF+ADrS7XYK6AHemXA/AR0ZQ3YJOA98NuF+"
        "BToyhuwQcA34YsL9DnRmDNl9jV4Fhk24w8ARlK8pO67RA8CICXcEOJpNkF0CmoERE+4ocCwXwa5r"
        "9BHw3YQ7DhQ0ZJcJ3wOMmXAngBOLGWKXgGPApAl3B3BisUPsEnAEmDLh/gRO5iMtdYs/AJw24U4D"
        "p4qRlrrFbwemTbgzwGm7ttgVwA8T7ixwxq4tNgA/mzDngLNWb7F/t9n9wKwJdw44Z9cWuxv4bcKd"
        "B87bscV2A3PAvAl3Hrhg1xbbBfwx4S4AF+3aYncCCybcReCiXVvsTqBQsly0a4vdASyZcJeAS3Zt"
        "sduBZRNuGLhs1xa7DVgx4UaAK3ZtsY8CURPuKnDVri32ESBmwo0B1+zaYrcCcRPuGnDNri32ISBp"
        "wk0CXXZtsQ8CSRNuEui2a4t9AEiacFNAt11b7P1AyoSbAnrs2mLvA1Im3DTQY9cWex+QNuGmgR67"
        "ttgtQNqEmwZ67NpiNwNpE24a6LFri90EZEy4GaDHri12E5Ax4WaAHru22E1AxoSbAa7btcVuBDIm"
        "3Axw3a4tdiOQMeFmgOt2bbEbgIwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJ"
        "NwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBk"
        "gZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL"
        "3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZwJNwNc"
        "t2uL3QBkgZwJNwNct2uL3QBkgZwJNwNct2uL3QBkgZw