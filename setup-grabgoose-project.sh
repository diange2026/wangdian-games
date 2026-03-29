#!/bin/bash
# GrabGoose Unity Project Setup Script
# 自动创建 Unity 项目结构并安装 TomLeeLive 插件

set -e

PROJECT_NAME="GrabGoose"
PROJECT_ROOT="$HOME/Projects/$PROJECT_NAME"
PLUGIN_URL="https://github.com/TomLeeLive/openclaw-unity-plugin.git"

echo "🚀 开始设置 $PROJECT_NAME 项目..."

# 1. 创建项目目录结构
echo "📁 创建项目目录结构..."
mkdir -p "$PROJECT_ROOT"/{Assets/{Plugins,Scenes,Scripts,Materials,Textures,Models,Animations,Audio,Prefabs},Packages,ProjectSettings}

# 2. 克隆 TomLeeLive 插件
echo "🔌 克隆 TomLeeLive 插件..."
cd /tmp
if [ -d "openclaw-unity-plugin" ]; then
    rm -rf openclaw-unity-plugin
fi
git clone "$PLUGIN_URL"
cp -r openclaw-unity-plugin "$PROJECT_ROOT/Assets/Plugins/"

# 3. 创建项目配置文件
echo "📝 创建项目配置..."
cat > "$PROJECT_ROOT/ProjectSettings/ProjectVersion.txt" << EOF
m_EditorVersion: 2022.3.15f1
m_EditorVersionWithRevision: 2022.3.15f1 (fb119bb5d4f0)
EOF

# 4. 创建 README
cat > "$PROJECT_ROOT/README.md" << EOF
# $PROJECT_NAME

《抓抓抓 3D》游戏项目 - Unity 版本

## 系统要求

- Unity 2022.3.15f1 LTS 或更高版本
- TomLeeLive OpenClaw Unity Plugin

## 项目结构

\`\`\`
Assets/
├── Plugins/
│   └── openclaw-unity-plugin/  # TomLeeLive 插件
├── Scenes/                      # 场景文件
├── Scripts/                     # C# 脚本
├── Materials/                   # 材质
├── Textures/                    # 贴图
├── Models/                      # 3D 模型
├── Animations/                  # 动画
├── Audio/                       # 音频
└── Prefabs/                     # 预制体
\`\`\`

## 安装步骤

1. 打开 Unity Hub
2. 点击 **Open** → 选择此项目文件夹
3. 等待导入完成
4. 打开 **Window** → **Package Manager**
5. 验证 **openclaw-unity-plugin** 已安装

## 玩法说明

- 点击 3D 堆叠中的物品
- 放入底部槽位
- 集齐 3 个相同物品即消除
- 消除所有物品即可通关

## 开发团队

典哥的游戏乐园

## 许可证

MIT License
EOF

# 5. 创建 .gitignore
cat > "$PROJECT_ROOT/.gitignore" << EOF
[Ll]ibrary/
[Tt]emp/
[Oo]bj/
[Bb]uild/
[Bb]uildScript/
[Uu]ser[Ss]ettings/
.vs/
*.csproj
*.unityproj
*.sln
*.suo
*.tmp
*.pidb
*.user
*.db
*.opendb
*.VC.db
*.pidb.meta
*.unityproj.meta
*.sln.meta
*.suo.meta
*.tmp.meta
*.db.meta
*.opendb.meta
*.VC.db.meta
EOF

echo "✅ 项目设置完成！"
echo ""
echo "📂 项目位置：$PROJECT_ROOT"
echo ""
echo "🎮 下一步："
echo "   1. 打开 Unity Hub"
echo "   2. 点击 Open → 选择 $PROJECT_ROOT"
echo "   3. 等待导入完成"
echo "   4. 开始开发！"
echo ""
