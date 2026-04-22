#!/bin/bash

# 🚀 工贸企业相关方全流程管理系统 - GitHub 部署脚本
# 请在你的电脑上运行此脚本

echo "🏭 工贸企业相关方全流程管理系统 - GitHub 部署"
echo "============================================"
echo ""

# 设置颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}[1/6] 检查环境...${NC}"
echo ""

# 检查必要的工具
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}❌ 未安装 $1${NC}"
        echo "请先安装 $1，然后重新运行脚本。"
        exit 1
    fi
    echo -e "${GREEN}✅ $1 已安装${NC}"
}

check_command "git"
check_command "curl"

echo ""
echo -e "${BLUE}[2/6] 配置 GitHub...${NC}"
echo ""

# 配置 GitHub 用户名和仓库
GITHUB_USERNAME="diange2026"
REPO_NAME="industrial-partner-management"
DEPLOY_DIR="deploy-package"

echo "GitHub 用户名: $GITHUB_USERNAME"
echo "仓库名称: $REPO_NAME"
echo "部署目录: $DEPLOY_DIR"
echo ""

echo -e "${BLUE}[3/6] 创建仓库...${NC}"
echo ""

# 检查仓库是否已存在
if curl -s "https://api.github.com/repos/$GITHUB_USERNAME/$REPO_NAME" | grep -q "Not Found"; then
    echo "❌ 仓库不存在，需要创建"
    echo "请手动创建仓库: https://github.com/new"
    echo ""
    echo "仓库配置:"
    echo "- 所有者: $GITHUB_USERNAME"
    echo "- 仓库名: $REPO_NAME"
    echo "- 描述: 工贸企业相关方全流程管理系统"
    echo "- 公开 (Public)"
    echo ""
    echo "创建完成后，请按 Enter 继续..."
    read
else
    echo -e "${GREEN}✅ 仓库已存在${NC}"
fi

echo ""
echo -e "${BLUE}[4/6] 初始化本地仓库...${NC}"
echo ""

# 创建临时工作目录
WORK_DIR="/tmp/industrial-partner-deploy-$(date +%s)"
mkdir -p $WORK_DIR
cd $WORK_DIR

echo "工作目录: $WORK_DIR"

# 初始化 git 仓库
git init
git checkout -b main

echo ""
echo -e "${GREEN}✅ 本地仓库初始化完成${NC}"

echo ""
echo -e "${BLUE}[5/6] 复制文件...${NC}"
echo ""

# 复制部署文件
SOURCE_DIR="/root/.openclaw/workspace/industrial-partner-management/$DEPLOY_DIR"
cp -r "$SOURCE_DIR"/* .

echo "已复制文件:"
ls -la

echo ""
echo -e "${BLUE}[6/6] 部署到 GitHub...${NC}"
echo ""

# 添加文件
git add .

# 提交
git commit -m "🚀 工贸企业相关方全流程管理系统 - 部署版本 $(date +%Y-%m-%d)"

# 连接到远程仓库
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

echo ""
echo "📋 手动部署步骤:"
echo ""
echo "1. 将工作目录中的文件上传到 GitHub 仓库:"
echo "   工作目录: $WORK_DIR"
echo ""
echo "2. 上传方法:"
echo "   A. 通过 GitHub 网页:"
echo "      - 访问 https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo "      - 点击 'Add file' → 'Upload files'"
echo "      - 上传所有文件 (index.html, README.md, DEPLOY-GUIDE.md)"
echo ""
echo "   B. 通过命令行:"
echo "      # 复制到你的工作目录"
echo "      cp -r $WORK_DIR/* ~/projects/industrial-partner/"
echo "      cd ~/projects/industrial-partner"
echo "      git add ."
echo "      git commit -m '🚀 部署系统'"
echo "      git push origin main"
echo ""
echo "3. 开启 GitHub Pages:"
echo "   - 进入仓库 Settings → Pages"
echo "   - Source: Deploy from a branch"
echo "   - Branch: main"
echo "   - Folder: / (根目录)"
echo "   - Save"
echo ""
echo "4. 访问系统:"
echo "   https://$GITHUB_USERNAME.github.io/$REPO_NAME/"
echo ""

echo "🎯 快速部署链接:"
echo ""
echo "1. 创建新仓库:"
echo "   ${BLUE}https://github.com/new?name=$REPO_NAME${NC}"
echo ""
echo "2. 上传文件:"
echo "   ${BLUE}https://github.com/$GITHUB_USERNAME/$REPO_NAME/upload/main${NC}"
echo ""
echo "3. 开启 Pages:"
echo "   ${BLUE}https://github.com/$GITHUB_USERNAME/$REPO_NAME/settings/pages${NC}"
echo ""

# 清理
cd ..
rm -rf $WORK_DIR

echo -e "${GREEN}✅ 部署脚本执行完成！${NC}"
echo ""
echo "📋 接下来:"
echo "1. 按照上面的步骤手动部署"
echo "2. 访问你的系统"
echo "3. 开始使用工贸企业相关方全流程管理系统"
echo ""
echo "🎉 祝你好运！"