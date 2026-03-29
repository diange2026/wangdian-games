#!/bin/bash
# 系统运维脚本 - 用于日常维护和故障处理
# 用法：./ops-maintenance.sh [check|clean|restart|report]

set -e

LOG_FILE="/var/log/openclaw-ops.log"
WORKSPACE="/root/.openclaw/workspace"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 系统资源检查
check_resources() {
    log "=== 系统资源检查 ==="
    
    # 内存
    MEM_USED=$(free | grep Mem | awk '{printf "%.2f", $3/$2 * 100.0}')
    log "内存使用率：${MEM_USED}%"
    
    # 磁盘
    DISK_USED=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    log "磁盘使用率：${DISK_USED}%"
    
    # CPU 负载
    LOAD=$(uptime | awk -F'load average:' '{print $2}' | cut -d, -f1 | xargs)
    log "CPU 负载：${LOAD}"
    
    # 告警阈值
    if (( $(echo "$MEM_USED > 80" | bc -l 2>/dev/null || echo 0) )); then
        log "⚠️ 警告：内存使用率超过 80%"
    fi
    
    if [ "$DISK_USED" -gt 80 ]; then
        log "⚠️ 警告：磁盘使用率超过 80%"
    fi
}

# 服务状态检查
check_services() {
    log "=== 服务状态检查 ==="
    
    # OpenClaw Gateway
    if systemctl is-active --quiet openclaw-gateway 2>/dev/null; then
        log "✅ OpenClaw Gateway: 运行中"
    else
        log "❌ OpenClaw Gateway: 未运行"
    fi
    
    # 进程数
    PROC_COUNT=$(pgrep -f openclaw | wc -l)
    log "OpenClaw 进程数：${PROC_COUNT}"
}

# 自动升级软件
upgrade_system() {
    log "=== 自动升级软件 ==="
    
    # 更新软件源
    log "🔄 更新软件源..."
    apt-get update -qq 2>/dev/null && log "✅ 软件源已更新" || log "⚠️ 软件源更新失败"
    
    # 升级系统软件
    log "🔄 升级系统软件..."
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y -qq 2>/dev/null && log "✅ 系统软件已升级" || log "⚠️ 系统软件升级失败"
    
    # 清理升级缓存
    apt-get autoremove -y -qq 2>/dev/null && log "✅ 升级缓存已清理" || log "⚠️ 缓存清理失败"
    
    # 升级 npm 全局包
    log "🔄 升级 npm 全局包..."
    npm update -g --silent 2>/dev/null && log "✅ npm 全局包已升级" || log "⚠️ npm 包升级失败"
    
    # 升级 pnpm 全局包
    log "🔄 升级 pnpm 全局包..."
    pnpm update -g --silent 2>/dev/null && log "✅ pnpm 全局包已升级" || log "⚠️ pnpm 包升级失败"
    
    # 升级 OpenClaw 技能
    log "🔄 升级 OpenClaw 技能..."
    cd "$WORKSPACE" && openclaw skills update --all --silent 2>/dev/null && log "✅ OpenClaw 技能已升级" || log "⚠️ OpenClaw 技能升级失败"
    
    log "✅ 系统升级完成"
}

# 清理操作
clean_system() {
    log "=== 系统清理 ==="
    
    # apt 缓存
    apt-get clean -y 2>/dev/null && log "✅ apt 缓存已清理"
    
    # journal 日志
    journalctl --vacuum-size=100M 2>/dev/null && log "✅ journal 日志已清理"
    
    # tmp 文件
    find /tmp -type f -atime +7 -delete 2>/dev/null && log "✅ 7 天以上临时文件已清理"
    
    # 旧的内核（保留最近 2 个）
    # apt-get autoremove -y 2>/dev/null && log "✅ 旧内核已清理"
    
    # 系统垃圾清理
    log "🗑️ 清理系统垃圾..."
    
    # 浏览器缓存
    rm -rf ~/.cache/* 2>/dev/null && log "✅ 浏览器缓存已清理"
    
    # npm 缓存
    npm cache clean --force 2>/dev/null && log "✅ npm 缓存已清理"
    
    # pnpm 缓存
    pnpm store prune --silent 2>/dev/null && log "✅ pnpm 缓存已清理"
    
    # Git 垃圾
    cd "$WORKSPACE" && git gc --prune=now --quiet 2>/dev/null && log "✅ Git 垃圾已清理"
    
    # 日志文件清理（保留最近 7 天）
    find /var/log -type f -name "*.log" -mtime +7 -delete 2>/dev/null && log "✅ 7 天前日志已清理"
    
    # 回收站清理
    rm -rf ~/.local/share/Trash/* 2>/dev/null && log "✅ 回收站已清理"
    
    log "✅ 系统清理完成"
}

# 重启服务
restart_services() {
    log "=== 重启服务 ==="
    
    systemctl restart openclaw-gateway 2>/dev/null && log "✅ OpenClaw Gateway 已重启"
    
    sleep 5
    
    if systemctl is-active --quiet openclaw-gateway 2>/dev/null; then
        log "✅ 服务重启成功"
    else
        log "❌ 服务重启失败"
        exit 1
    fi
}

# 备份验证
verify_backup() {
    log "=== 备份验证 ==="
    
    cd "$WORKSPACE"
    
    # git 状态
    git fetch origin 2>/dev/null
    LOCAL=$(git rev-parse HEAD 2>/dev/null)
    REMOTE=$(git rev-parse origin/main 2>/dev/null)
    
    if [ "$LOCAL" = "$REMOTE" ]; then
        log "✅ 备份同步：本地与远程一致"
    else
        log "⚠️ 备份不同步：本地 ${LOCAL:0:7} vs 远程 ${REMOTE:0:7}"
    fi
    
    # 最后提交时间
    LAST_COMMIT=$(git log -1 --format=%ci)
    log "最后备份时间：${LAST_COMMIT}"
}

# 网络检查
check_network() {
    log "=== 网络检查 ==="
    
    # 外网连通性
    if ping -c1 -W1 8.8.8.8 >/dev/null 2>&1; then
        log "✅ 外网连通性：正常"
    else
        log "❌ 外网连通性：异常"
    fi
    
    # GitHub 连通性
    if ping -c1 -W1 github.com >/dev/null 2>&1; then
        log "✅ GitHub 连通性：正常"
    else
        log "⚠️ GitHub 连通性：异常（可能影响备份）"
    fi
}

# 生成完整报告
generate_report() {
    log "=========================================="
    log "     系统运维报告 - $(date '+%Y-%m-%d %H:%M')"
    log "=========================================="
    
    check_resources
    check_services
    check_network
    verify_backup
    
    log "=========================================="
    log "检查完成！"
    log "=========================================="
}

# 主程序
case "${1:-report}" in
    check)
        check_resources
        check_services
        check_network
        ;;
    clean)
        clean_system
        ;;
    restart)
        restart_services
        ;;
    verify)
        verify_backup
        ;;
    upgrade)
        upgrade_system
        ;;
    report|*)
        generate_report
        ;;
esac

# 重启 Gateway 服务（清理缓存）
restart_gateway() {
    log "=== 重启 Gateway 服务 ==="
    
    # 检查 Gateway 状态
    if systemctl is-active --quiet openclaw-gateway 2>/dev/null; then
        systemctl restart openclaw-gateway 2>/dev/null && log "✅ Gateway 已重启" || log "⚠️ Gateway 重启失败"
    else
        systemctl start openclaw-gateway 2>/dev/null && log "✅ Gateway 已启动" || log "⚠️ Gateway 启动失败"
    fi
    
    # 等待服务就绪
    sleep 5
    
    # 验证服务状态
    if systemctl is-active --quiet openclaw-gateway 2>/dev/null; then
        log "✅ Gateway 服务运行正常"
    else
        log "❌ Gateway 服务异常"
    fi
}
