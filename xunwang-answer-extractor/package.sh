#!/bin/bash

# 讯网答案提取器插件打包脚本
# 使用方法: ./package.sh [版本号]

set -e

# 默认参数
VERSION=${1:-1.0.0}
PROJECT_NAME="xunwang-answer-extractor"
PACKAGE_NAME="${PROJECT_NAME}-v${VERSION}"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== 讯网答案提取器插件打包工具 ===${NC}"
echo -e "版本: ${GREEN}${VERSION}${NC}"
echo -e "包名: ${YELLOW}${PACKAGE_NAME}${NC}"
echo

# 检查必需文件
check_required_files() {
    echo -e "${BLUE}[1/5] 检查必需文件...${NC}"
    
    local required_files=(
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
        "icons/icon16.png"
        "icons/icon48.png"
        "icons/icon128.png"
    )
    
    local missing_files=()
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ] && [ ! -d "$file" ]; then
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -gt 0 ]; then
        echo -e "${RED}错误: 缺少必需文件:${NC}"
        for file in "${missing_files[@]}"; do
            echo -e "  ${RED}✗${NC} $file"
        done
        return 1
    else
        echo -e "${GREEN}✓ 所有必需文件都存在${NC}"
        return 0
    fi
}

# 更新版本号
update_version() {
    echo -e "${BLUE}[2/5] 更新版本号...${NC}"
    
    # 更新manifest.json中的版本号
    if [ -f "manifest.json" ]; then
        sed -i "s/\"version\": \".*\"/\"version\": \"${VERSION}\"/g" manifest.json
        echo -e "${GREEN}✓ 更新 manifest.json 版本号${NC}"
    fi
    
    # 更新其他文件中的版本号（如果有）
    if [ -f "popup/popup.html" ]; then
        sed -i "s/v[0-9]\+\.[0-9]\+\.[0-9]\+/v${VERSION}/g" popup/popup.html
        echo -e "${GREEN}✓ 更新 popup.html 版本号${NC}"
    fi
    
    if [ -f "options/options.html" ]; then
        sed -i "s/v[0-9]\+\.[0-9]\+\.[0-9]\+/v${VERSION}/g" options/options.html
        echo -e "${GREEN}✓ 更新 options.html 版本号${NC}"
    fi
}

# 创建临时目录
create_temp_dir() {
    echo -e "${BLUE}[3/5] 创建临时目录...${NC}"
    
    # 清理旧目录
    if [ -d "temp_package" ]; then
        rm -rf temp_package
    fi
    
    if [ -d "${PACKAGE_NAME}" ]; then
        rm -rf "${PACKAGE_NAME}"
    fi
    
    # 创建新目录结构
    mkdir -p temp_package
    mkdir -p temp_package/popup
    mkdir -p temp_package/options
    mkdir -p temp_package/icons
    mkdir -p temp_package/libs
    
    echo -e "${GREEN}✓ 临时目录创建完成${NC}"
}

# 复制文件
copy_files() {
    echo -e "${BLUE}[4/5] 复制文件...${NC}"
    
    # 复制核心文件
    cp manifest.json temp_package/
    cp background.js temp_package/
    cp content.js temp_package/
    cp utils.js temp_package/
    
    # 复制popup文件
    cp popup/popup.html temp_package/popup/
    cp popup/popup.js temp_package/popup/
    cp popup/popup.css temp_package/popup/
    
    # 复制options文件
    cp options/options.html temp_package/options/
    cp options/options.js temp_package/options/
    cp options/options.css temp_package/options/
    
    # 复制图标
    cp icons/icon16.png temp_package/icons/
    cp icons/icon48.png temp_package/icons/
    cp icons/icon128.png temp_package/icons/
    
    # 复制其他文件（如果有）
    if [ -f "README.md" ]; then
        cp README.md temp_package/
    fi
    
    if [ -f "LICENSE" ]; then
        cp LICENSE temp_package/
    fi
    
    echo -e "${GREEN}✓ 文件复制完成${NC}"
}

# 创建ZIP包
create_zip() {
    echo -e "${BLUE}[5/5] 创建ZIP包...${NC}"
    
    # 重命名目录
    mv temp_package "${PACKAGE_NAME}"
    
    # 创建ZIP文件
    if command -v zip &> /dev/null; then
        zip -r "${PACKAGE_NAME}.zip" "${PACKAGE_NAME}" -x "*.DS_Store" "*.git*" "*.svn*"
        echo -e "${GREEN}✓ ZIP包创建完成: ${PACKAGE_NAME}.zip${NC}"
        
        # 显示文件大小
        local file_size=$(du -h "${PACKAGE_NAME}.zip" | cut -f1)
        echo -e "${YELLOW}文件大小: ${file_size}${NC}"
    else
        echo -e "${RED}错误: zip命令未找到${NC}"
        echo -e "${YELLOW}请手动打包: tar -czf ${PACKAGE_NAME}.tar.gz ${PACKAGE_NAME}${NC}"
        return 1
    fi
}

# 清理临时文件
cleanup() {
    echo -e "\n${BLUE}清理临时文件...${NC}"
    
    if [ -d "${PACKAGE_NAME}" ]; then
        rm -rf "${PACKAGE_NAME}"
        echo -e "${GREEN}✓ 清理临时目录${NC}"
    fi
    
    if [ -d "temp_package" ]; then
        rm -rf temp_package
    fi
}

# 显示安装说明
show_instructions() {
    echo -e "\n${GREEN}=== 安装说明 ===${NC}"
    echo -e "1. 打开Chrome浏览器"
    echo -e "2. 在地址栏输入: ${YELLOW}chrome://extensions/${NC}"
    echo -e "3. 打开右上角的${YELLOW}'开发者模式'${NC}"
    echo -e "4. 点击${YELLOW}'加载已解压的扩展程序'${NC}"
    echo -e "5. 选择目录: ${YELLOW}${PACKAGE_NAME}${NC}"
    echo -e "6. 插件安装完成！🎉"
    echo
    echo -e "${BLUE}测试建议:${NC}"
    echo -e "1. 访问讯网平台: ${YELLOW}https://www.whxunw.com/exam/login.thtml${NC}"
    echo -e "2. 登录账号: ${YELLOW}014325210588${NC}"
    echo -e "3. 密码: ${YELLOW}6W7EjZ>M${NC}"
    echo -e "4. 进入答案页面测试提取功能"
}

# 主执行函数
main() {
    echo -e "${BLUE}开始打包...${NC}"
    echo
    
    # 执行各个步骤
    check_required_files || exit 1
    update_version
    create_temp_dir
    copy_files
    create_zip || exit 1
    cleanup
    
    echo -e "\n${GREEN}=== 打包完成 ===${NC}"
    echo -e "插件包: ${YELLOW}${PACKAGE_NAME}.zip${NC}"
    echo -e "解压目录: ${YELLOW}${PACKAGE_NAME}${NC}"
    
    show_instructions
}

# 错误处理
trap 'echo -e "\n${RED}打包过程中断${NC}"; cleanup; exit 1' INT TERM

# 运行主函数
main