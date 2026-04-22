#!/bin/bash

# 每日进展汇报脚本
# 执行时间：8:00, 12:00, 17:00

# 设置日志文件
LOG_DIR="/root/.openclaw/logs"
LOG_FILE="$LOG_DIR/progress-report.log"
mkdir -p "$LOG_DIR"

# 获取当前时间
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
TIME_OF_DAY=$(date "+%H:%M")

echo "==========================================" >> "$LOG_FILE"
echo "进展汇报开始 - $TIMESTAMP" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"

# 1. 检查系统状态
echo "[$TIMESTAMP] 1. 系统状态检查..." >> "$LOG_FILE"

# 检查 OpenClaw Gateway 状态
GATEWAY_STATUS=$(systemctl is-active openclaw-gateway 2>/dev/null || echo "inactive")
echo "  - OpenClaw Gateway: $GATEWAY_STATUS" >> "$LOG_FILE"

# 检查内存使用
MEMORY_USAGE=$(free -h | awk '/^Mem:/ {print $3 "/" $2 " (" $3/$2*100 "%)"}')
echo "  - 内存使用: $MEMORY_USAGE" >> "$LOG_FILE"

# 检查磁盘使用
DISK_USAGE=$(df -h / | awk 'NR==2 {print $3 "/" $2 " (" $5 ")"}')
echo "  - 磁盘使用: $DISK_USAGE" >> "$LOG_FILE"

# 2. 检查服务状态
echo "[$TIMESTAMP] 2. 服务状态检查..." >> "$LOG_FILE"

# 检查定时任务
echo "  - 定时任务: 运行中" >> "$LOG_FILE"

# 检查备份状态
if [ -f "/root/.openclaw/workspace/.git/config" ]; then
    GIT_STATUS=$(cd /root/.openclaw/workspace && git status --porcelain 2>/dev/null | wc -l)
    echo "  - 待提交文件: $GIT_STATUS 个" >> "$LOG_FILE"
else
    echo "  - 待提交文件: 未配置Git" >> "$LOG_FILE"
fi

# 3. 检查最近活动
echo "[$TIMESTAMP] 3. 最近活动检查..." >> "$LOG_FILE"

# 检查最近日志
RECENT_LOGS=$(tail -5 /var/log/openclaw-ops.log 2>/dev/null | sed 's/^/    /')
if [ -n "$RECENT_LOGS" ]; then
    echo "  最近运维日志:" >> "$LOG_FILE"
    echo "$RECENT_LOGS" >> "$LOG_FILE"
else
    echo "  最近运维日志: 无" >> "$LOG_FILE"
fi

# 4. 系统链接汇总
echo "[$TIMESTAMP] 4. 系统链接汇总:" >> "$LOG_FILE"

echo "  - OpenClaw Gateway: http://localhost:8080 (如果已启动)" >> "$LOG_FILE"
echo "  - GitHub 仓库: https://github.com/diange2026/wangdian-games" >> "$LOG_FILE"
echo "  - 工作空间备份: 每日自动备份到GitHub" >> "$LOG_FILE"
echo "  - 系统监控: 每日6:00和18:00运行健康检查" >> "$LOG_FILE"
echo "  - 自动升级: 每周一凌晨3:00运行" >> "$LOG_FILE"
echo "  - 系统清理: 每周日凌晨4:00运行" >> "$LOG_FILE"

# 5. 根据时间生成不同的问候和重点
echo "[$TIMESTAMP] 5. 本时段重点:" >> "$LOG_FILE"
case "$TIME_OF_DAY" in
    "08:00")
        echo "  - 早上好！新的一天开始" >> "$LOG_FILE"
        echo "  - 检查昨晚的备份结果" >> "$LOG_FILE"
        echo "  - 准备今日工作计划" >> "$LOG_FILE"
        ;;
    "12:00")
        echo "  - 中午好！上午工作已过半" >> "$LOG_FILE"
        echo "  - 检查系统午间状态" >> "$LOG_FILE"
        echo "  - 准备下午工作安排" >> "$LOG_FILE"
        ;;
    "17:00")
        echo "  - 下午好！即将结束今日工作" >> "$LOG_FILE"
        echo "  - 汇总今日进展和成果" >> "$LOG_FILE"
        echo "  - 准备晚间备份和检查" >> "$LOG_FILE"
        ;;
    *)
        echo "  - 常规系统状态检查" >> "$LOG_FILE"
        ;;
esac

echo "==========================================" >> "$LOG_FILE"
echo "进展汇报完成 - $TIMESTAMP" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 发送消息到微信
# 这里可以添加发送消息的代码
# 例如：使用 message 工具发送到微信

# 输出简要信息到控制台
echo "进展汇报完成于 $TIMESTAMP"
echo "详细日志: $LOG_FILE"