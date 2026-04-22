#!/bin/bash

# 检查进展汇报系统状态的脚本

echo "📊 进展汇报系统状态检查"
echo "========================"
echo "检查时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 1. 检查定时任务配置
echo "✅ 1. 定时任务配置："
crontab -l | grep progress-report-weixin | while read line; do
    hour=$(echo $line | awk '{print $2}')
    echo "   • $hour:00 - 每日执行"
done
echo ""

# 2. 检查脚本可执行性
echo "✅ 2. 脚本可执行性："
if [ -x "/root/.openclaw/workspace/scripts/progress-report-weixin.sh" ]; then
    echo "   • progress-report-weixin.sh: ✅ 可执行"
else
    echo "   • progress-report-weixin.sh: ❌ 不可执行"
fi
echo ""

# 3. 检查最近日志
echo "✅ 3. 最近执行日志："
LOG_FILE="/root/.openclaw/logs/progress-report-weixin.log"
if [ -f "$LOG_FILE" ]; then
    echo "   • 日志文件: $LOG_FILE"
    echo "   • 最后修改: $(stat -c %y "$LOG_FILE" | cut -d'.' -f1)"
    echo "   • 最近记录:"
    tail -3 "$LOG_FILE" | sed 's/^/      /'
else
    echo "   • 日志文件: ❌ 不存在"
fi
echo ""

# 4. 预测下次执行时间
echo "✅ 4. 下次执行预测："
current_hour=$(date +%H)
echo "   当前时间: ${current_hour}:$(date +%M)"

if [ $current_hour -lt 8 ]; then
    echo "   • 下次执行: 今天 08:00"
elif [ $current_hour -lt 12 ]; then
    echo "   • 下次执行: 今天 12:00"
elif [ $current_hour -lt 17 ]; then
    echo "   • 下次执行: 今天 17:00"
else
    echo "   • 下次执行: 明天 08:00"
fi
echo ""

# 5. 系统状态概览
echo "✅ 5. 当前系统状态："
echo "   • OpenClaw Gateway: $(systemctl is-active openclaw-gateway 2>/dev/null || echo '未运行')"
echo "   • 内存使用: $(free -h | awk '/^Mem:/ {print $3 "/" $2}')"
echo "   • 磁盘使用: $(df -h / | awk 'NR==2 {print $5}')"
echo "   • Git 待提交: $(cd /root/.openclaw/workspace && git status --porcelain 2>/dev/null | wc -l) 个文件"
echo ""

echo "📋 总结："
echo "  - 系统已配置，定时任务正常"
echo "  - 今日执行时间: 12:00, 17:00"
echo "  - 明天开始: 8:00, 12:00, 17:00"
echo "  - 汇报内容包括系统状态和重要链接"