#!/bin/bash
# OpenClaw Workspace Git 自动备份脚本
# 用途：将 workspace 变更提交并推送到 GitHub
# 使用：./git-backup.sh

set -e

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="/var/log/openclaw-git-backup.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

cd "$WORKSPACE"

log "=========================================="
log "  Git 自动备份开始"
log "=========================================="

# 检查是否有变更
git add -A 2>/dev/null
CHANGES=$(git status --porcelain 2>/dev/null | wc -l)

if [ "$CHANGES" -eq 0 ]; then
    log "✅ 无变更，跳过备份"
    exit 0
fi

log "📝 发现 $CHANGES 个文件变更"

# 提交变更
COMMIT_MSG="chore: 自动备份 - $(date '+%Y-%m-%d %H:%M')"
git commit -m "$COMMIT_MSG" 2>/dev/null && log "✅ 提交成功：$COMMIT_MSG" || {
    log "⚠️ 提交失败（可能无变更）"
    exit 0
}

# 推送到远程
log "🚀 推送到 GitHub..."
git push origin main 2>/dev/null && log "✅ 推送成功" || {
    log "❌ 推送失败，检查网络连接"
    exit 1
}

log "=========================================="
log "  Git 备份完成"
log "=========================================="

# 显示最新提交
git log -1 --format="%h %ai %s" | tee -a "$LOG_FILE"
