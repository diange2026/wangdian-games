#!/bin/bash
# OpenClaw 记忆系统备份脚本
# 用途：将记忆文件备份到 /data/openclaw-memory-backup/
# 使用：./backup-memory.sh

set -e

# 配置
WORKSPACE="/root/.openclaw/workspace"
BACKUP_DIR="/data/openclaw-memory-backup"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}  OpenClaw 记忆系统备份${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

# 检查源目录
if [ ! -d "$WORKSPACE/memory" ]; then
    echo -e "${RED}错误：记忆目录不存在 $WORKSPACE/memory${NC}"
    exit 1
fi

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 备份记忆文件
echo -e "${YELLOW}[1/5] 备份记忆目录...${NC}"
if [ -d "$BACKUP_DIR/memory" ]; then
    rm -rf "$BACKUP_DIR/memory"
fi
cp -r "$WORKSPACE/memory" "$BACKUP_DIR/"
echo -e "${GREEN}✓ 记忆目录备份完成${NC}"

# 备份 MEMORY.md
echo -e "${YELLOW}[2/5] 备份 MEMORY.md...${NC}"
if [ -f "$WORKSPACE/MEMORY.md" ]; then
    cp "$WORKSPACE/MEMORY.md" "$BACKUP_DIR/"
    echo -e "${GREEN}✓ MEMORY.md 备份完成${NC}"
else
    echo -e "${YELLOW}⚠ MEMORY.md 不存在，跳过${NC}"
fi

# 备份 USER.md
echo -e "${YELLOW}[3/5] 备份 USER.md...${NC}"
if [ -f "$WORKSPACE/USER.md" ]; then
    cp "$WORKSPACE/USER.md" "$BACKUP_DIR/"
    echo -e "${GREEN}✓ USER.md 备份完成${NC}"
else
    echo -e "${YELLOW}⚠ USER.md 不存在，跳过${NC}"
fi

# 备份 IDENTITY.md
echo -e "${YELLOW}[4/5] 备份 IDENTITY.md...${NC}"
if [ -f "$WORKSPACE/IDENTITY.md" ]; then
    cp "$WORKSPACE/IDENTITY.md" "$BACKUP_DIR/"
    echo -e "${GREEN}✓ IDENTITY.md 备份完成${NC}"
else
    echo -e "${YELLOW}⚠ IDENTITY.md 不存在，跳过${NC}"
fi

# 创建备份清单
echo -e "${YELLOW}[5/5] 创建备份清单...${NC}"
cat > "$BACKUP_DIR/BACKUP_INFO.txt" << EOF
OpenClaw 记忆系统备份
====================
备份时间：$(date '+%Y-%m-%d %H:%M:%S')
时间戳：$TIMESTAMP
源目录：$WORKSPACE
备份目录：$BACKUP_DIR

备份内容:
$(ls -la "$BACKUP_DIR" | grep -v "^d" | grep -v "^total")

记忆文件数量：$(find "$BACKUP_DIR/memory" -type f 2>/dev/null | wc -l)
EOF
echo -e "${GREEN}✓ 备份清单创建完成${NC}"

# 显示备份统计
echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}  备份完成！${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "备份位置：$BACKUP_DIR"
echo "备份时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "备份内容:"
ls -lh "$BACKUP_DIR" | grep -v "^d" | grep -v "^total"
echo ""
echo "记忆文件:"
find "$BACKUP_DIR/memory" -type f -exec ls -lh {} \; | awk '{print $9, $5}'
echo ""
echo -e "${YELLOW}提示：重装系统后，将 $BACKUP_DIR 目录复制回原位置即可恢复记忆${NC}"
