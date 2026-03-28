#!/bin/bash
# OpenClaw 记忆系统恢复脚本
# 用途：从备份恢复记忆文件
# 使用：./restore-memory.sh [备份目录]

set -e

# 配置
WORKSPACE="/root/.openclaw/workspace"
BACKUP_DIR="${1:-/data/openclaw-memory-backup}"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}  OpenClaw 记忆系统恢复${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

# 检查备份目录
if [ ! -d "$BACKUP_DIR" ]; then
    echo -e "${RED}错误：备份目录不存在 $BACKUP_DIR${NC}"
    echo -e "${YELLOW}用法：./restore-memory.sh [备份目录]${NC}"
    exit 1
fi

# 确认恢复
echo -e "${YELLOW}警告：此操作将覆盖现有记忆文件！${NC}"
echo "备份来源：$BACKUP_DIR"
echo "恢复目标：$WORKSPACE"
echo ""
read -p "确定要恢复吗？(y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}已取消恢复${NC}"
    exit 0
fi

# 恢复记忆文件
echo -e "${YELLOW}[1/4] 恢复记忆目录...${NC}"
if [ -d "$BACKUP_DIR/memory" ]; then
    rm -rf "$WORKSPACE/memory"
    cp -r "$BACKUP_DIR/memory" "$WORKSPACE/"
    echo -e "${GREEN}✓ 记忆目录恢复完成${NC}"
else
    echo -e "${RED}✗ 备份中没有 memory 目录${NC}"
fi

# 恢复 MEMORY.md
echo -e "${YELLOW}[2/4] 恢复 MEMORY.md...${NC}"
if [ -f "$BACKUP_DIR/MEMORY.md" ]; then
    cp "$BACKUP_DIR/MEMORY.md" "$WORKSPACE/"
    echo -e "${GREEN}✓ MEMORY.md 恢复完成${NC}"
else
    echo -e "${YELLOW}⚠ 备份中没有 MEMORY.md${NC}"
fi

# 恢复 USER.md
echo -e "${YELLOW}[3/4] 恢复 USER.md...${NC}"
if [ -f "$BACKUP_DIR/USER.md" ]; then
    cp "$BACKUP_DIR/USER.md" "$WORKSPACE/"
    echo -e "${GREEN}✓ USER.md 恢复完成${NC}"
else
    echo -e "${YELLOW}⚠ 备份中没有 USER.md${NC}"
fi

# 恢复 IDENTITY.md
echo -e "${YELLOW}[4/4] 恢复 IDENTITY.md...${NC}"
if [ -f "$BACKUP_DIR/IDENTITY.md" ]; then
    cp "$BACKUP_DIR/IDENTITY.md" "$WORKSPACE/"
    echo -e "${GREEN}✓ IDENTITY.md 恢复完成${NC}"
else
    echo -e "${YELLOW}⚠ 备份中没有 IDENTITY.md${NC}"
fi

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}  恢复完成！${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "请重启 OpenClaw 或重新加载会话以应用恢复的记忆。"
