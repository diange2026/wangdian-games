#!/bin/bash

# 讯网答案提取器插件 - 安装与测试脚本

echo "================================================"
echo "      讯网答案提取器插件安装与测试"
echo "================================================"
echo ""

# 1. 检查目录结构
echo "📁 检查插件目录结构..."
if [ -d "/root/.openclaw/workspace/xunwang-answer-extractor" ]; then
    echo "✅ 插件目录存在"
    cd "/root/.openclaw/workspace/xunwang-answer-extractor"
    
    # 检查必需文件
    echo ""
    echo "📄 检查必需文件..."
    
    REQUIRED_FILES=(
        "manifest.json"
        "background.js"
        "content.js"
        "utils.js"
        "popup/popup.html"
        "popup/popup.js"
        "popup/popup.css"
        "options/options.html"
        "options/options.js"
        "options/options.css"
    )
    
    all_files_exist=true

    for file in "${REQUIRED_FILES[@]}"; do
        if [ ! -f "$file" ]; then
            echo "❌ 缺少文件: $file"
            all_files_exist=false
        else
            echo "✅ $file"
        fi
    done
    
    if [ "$all_files_exist" = false ]; then
        echo ""
        echo "⚠️  部分必需文件缺失，可能导致插件功能不完整"
    else
        echo ""
        echo "✅ 所有必需文件都存在"
    fi
    
    # 2. 检查图标
    echo ""
    echo "🖼️  检查图标文件..."
    
    if [ -f "icons/icon16.png" ]; then
        echo "✅ icon16.png 存在"
    else

        echo "❌ icon16.png 缺失"
        echo "   创建简单占位图标..."
        # 创建一个简单的16x16蓝色图标
        echo "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAA
B3RJTUUH5gQCCi03FQ2bIwAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUH
AAAANUlEQVQ4y2P8//8/Ay0xw6gBowYMPQMYqWk5I5U9wEgLAwgZGRnJNmDUgFEDRhwGAKfGEBwc
8JMoAAAAAElFTkSuQmCC" | base64 -d > icons/icon16.png
        echo "   使用base64占位图标"
    fi
    
    if [ -f "icons/icon48.png" ]; then
        echo "✅ icon48.png 存在"
    else
        echo "❌ icon48.png 缺失"
        # 这里可以创建占位图标
    fi
    
    if [ -f "icons/icon128.png" ]; then
        echo "✅ icon128.png 存在"
    else
        echo "❌ icon128.png 缺失"
        # 这里可以创建占位图标
    fi
    
    # 3. 显示插件信息
    echo ""
    echo "🔧 插件基本信息..."
    
    if [ -f "manifest.json" ]; then
        echo "版本: $(grep '"version"' manifest.json | head -1 | cut -d'"' -f4)"
        echo "名称: $(grep '"name"' manifest.json | head -1 | cut -d'"' -f4)"
    fi
    
    # 4. 测试页面创建
    echo ""
    echo "🌐 创建测试页面..."
    
    if [ -f "/root/.openclaw/workspace/xunwang-test-page.html" ]; then
        echo "✅ 测试页面已存在"
    else

        echo "创建测试页面..."
        cat > /root/.openclaw/workspace/xunwang-test-page.html << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>讯网答案页面测试</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        .question { border: 1px solid #ddd; padding: 15px; margin: 10px 0; background: #f9f9f9; }
        .answer { color: green; font-weight: bold; }
    </style>
</head>
<body>
    <h1>讯网答案测试页面</h1>
    <p>这是一个用于测试插件的模拟答案页面</p>
    <div class="question">
        <h3>1. 什么是经济学？</h3>
        <p class="answer">答案：研究资源分配的科学</p>
    </div>

    <div class="question">
        <h3>2. GDP的定义？</h3>
        <p class="answer">答案：国内生产总值</p>
    </div>

    <div class="question">
        <h3>3. 市场失灵的原因？</h3>
        <p class="answer">答案：信息不对称、外部性、垄断</p>
    </div>
</body>
</html>
EOF
        echo "✅ 测试页面创建完成"
    fi
    
    # 5. 测试功能
    echo ""
    echo "🧪 准备测试..."
    echo ""
    echo "📋 你可以进行以下测试："
    echo ""
    echo "1. 手动安装插件："
    echo "   1) 打开 Chrome 浏览器"
    echo "   2) 访问 chrome://extensions/"
    echo "   3) 打开 '开发者模式'"
    echo "   4) 点击 '加载已解压的扩展程序'"
    echo "   5) 选择目录: /root/.openclaw/workspace/xunwang-answer-extractor"
    echo ""
    echo "2. 测试页面："
    echo "   1) 打开测试页面: /root/.openclaw/workspace/xunwang-test-page.html"
    echo "   2) 刷新页面"
    echo "   3) 点击插件图标"
    echo "   4) 测试提取功能"
    echo ""
    echo "3. 测试导出功能："
    echo "   1) 点击 '导出Excel' 或 '导出CSV'"
    echo "   2) 检查生成的文件"
    echo ""
    echo "4. 测试本地存储："
    echo "   1) 提取答案"
    echo "   2) 保存到本地题库"
    echo "   3) 检查存储的数据"
    
    echo ""
    echo "🔧 插件安装测试完成！"
    echo ""
    echo "📚 资源信息："
    echo "   设计文档: /root/.openclaw/workspace/xunwang-answer-extractor-design.md"
    echo "   测试页面: /root/.openclaw/workspace/xunwang-test-page.html"
    echo "   插件目录: /root/.openclaw/workspace/xunwang-answer-extractor"
    echo ""
    echo "📖 使用说明请参考 README.md 文件"
    
else
    echo "❌ 插件目录不存在"
    echo "请确保插件目录位置正确"
    echo "当前路径: /root/.openclaw/workspace"
    echo ""
    echo "📁 目录列表:"
    ls -la /root/.openclaw/workspace/
fi

echo ""
echo "================================================"
echo "           测试脚本执行完毕"
echo "================================================"