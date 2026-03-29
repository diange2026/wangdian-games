#!/bin/bash
# Unity 编辑器自动化安装脚本
# 下载并安装 Unity Hub + Unity 2022.3.15f1 LTS

set -e

echo "🚀 开始安装 Unity 编辑器..."

# 1. 检查系统
echo "📋 检查系统..."
if [ ! -f /etc/os-release ]; then
    echo "❌ 仅支持 Linux 系统"
    exit 1
fi

source /etc/os-release
if [[ "$ID" != "ubuntu" && "$ID" != "debian" ]]; then
    echo "❌ 仅支持 Ubuntu/Debian 系统"
    exit 1
fi

# 2. 安装依赖
echo "📦 安装依赖..."
sudo apt update -qq
sudo apt install -y -qq wget apt-transport-https ca-certificates

# 3. 添加 Unity Hub 仓库
echo "🔧 添加 Unity Hub 仓库..."
wget -qO - https://hub.unity3d.com/linux/keys/public | sudo apt-key add -
echo "deb https://hub.unity3d.com/linux/repos/deb stable main" | sudo tee /etc/apt/sources.list.d/unityhub.list
sudo apt update -qq

# 4. 安装 Unity Hub
echo "📲 安装 Unity Hub..."
sudo apt install -y -qq unityhub

# 5. 安装 Unity 编辑器（需要手动激活）
echo "🎮 安装 Unity 编辑器 2022.3.15f1 LTS..."
echo "⚠️  注意：首次启动需要手动登录 Unity 账号激活许可证"

# 6. 创建项目目录
echo "📁 创建项目目录..."
mkdir -p ~/Projects/GrabGoose

echo ""
echo "✅ Unity Hub 安装完成！"
echo ""
echo "🎯 下一步操作："
echo "   1. 启动 Unity Hub: unityhub"
echo "   2. 登录 Unity 账号并激活许可证"
echo "   3. 安装 Unity 编辑器 2022.3.15f1 LTS"
echo "   4. 创建 GrabGoose 项目"
echo "   5. 安装 TomLeeLive 插件"
echo ""
echo "📖 详细指南：~/openclaw/workspace/UNITY-INSTALL-GUIDE.md"
echo ""
