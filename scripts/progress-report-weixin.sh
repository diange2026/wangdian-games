#!/bin/bash

# 每日进展汇报脚本 - 微信版本
# 执行时间：8:00, 12:00, 17:00
# 直接发送消息到微信

# 设置日志文件
LOG_DIR="/root/.openclaw/logs"
LOG_FILE="$LOG_DIR/progress-report-weixin.log"
mkdir -p "$LOG_DIR"

# 获取当前时间
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
TIME_OF_DAY=$(date "+%H:%M")
WEEKDAY=$(date "+%u")

echo "==========================================" >> "$LOG_FILE"
echo "微信进展汇报开始 - $TIMESTAMP" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"

# 根据时间生成不同的问候
case "$TIME_OF_DAY" in
    "08:00")
        GREETING="🌅 早上好典哥！新的一天开始啦"
        EMOJI="☀️"
        ;;
    "12:00")
        GREETING="🌞 中午好典哥！上午工作已过半"
        EMOJI="🍱"
        ;;
    "17:00")
        GREETING="🌇 下午好典哥！即将结束今日工作"
        EMOJI="📊"
        ;;
    *)
        GREETING="🤖 系统状态报告"
        EMOJI="📋"
        ;;
esac

# 获取系统状态信息
GATEWAY_STATUS=$(systemctl is-active openclaw-gateway 2>/dev/null || echo "未运行")
MEMORY_USAGE=$(free -h | awk '/^Mem:/ {print $3 "/" $2}')
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}')
GIT_CHANGES=$(cd /root/.openclaw/workspace && git status --porcelain 2>/dev/null | wc -l)

# 构建消息内容
MESSAGE="$EMOJI $GREETING $EMOJI
----------------------------
📊 系统状态概览：

• OpenClaw Gateway: $GATEWAY_STATUS
• 内存使用: $MEMORY_USAGE
• 磁盘使用: $DISK_USAGE
• Git 待提交: $GIT_CHANGES 个文件

🔗 系统链接：

• GitHub 仓库: https://github.com/diange2026/wangdian-games
• 本地工作空间: /root/.openclaw/workspace
• 日志目录: /root/.openclaw/logs/

⏰ 今日计划提醒：

"

# 根据星期和时间添加不同的提醒
case "$WEEKDAY" in
    "1")  # 周一
        MESSAGE="$MESSAGE• 周一：系统自动升级检查"
        ;;
    "7")  # 周日
        MESSAGE="$MESSAGE• 周日：系统清理和整理"
        ;;
esac

case "$TIME_OF_DAY" in
    "08:00")
        MESSAGE="$MESSAGE• 检查昨日备份结果
• 今日工作计划安排"
        ;;
    "12:00")
        MESSAGE="$MESSAGE• 午间系统状态检查
• 下午工作计划确认"
        ;;
    "17:00")
        MESSAGE="$MESSAGE• 今日工作汇总
• 晚间备份准备
• 明日计划预览"
        ;;
esac

MESSAGE="$MESSAGE

----------------------------
🤖 汇报时间: $TIMESTAMP
📅 系统运行正常，持续为您服务！"

echo "[$TIMESTAMP] 构建消息完成" >> "$LOG_FILE"
echo "消息内容:" >> "$LOG_FILE"
echo "$MESSAGE" >> "$LOG_FILE"

# 尝试发送消息到微信
# 注意：这里需要你的微信用户ID和AccountId
# 由于安全原因，我无法直接获取这些信息
# 你需要根据实际情况配置以下参数

WECHAT_USER_ID="o9cq8002wI7v_8qzHYnYxS5S1ofc@im.wechat"
WECHAT_ACCOUNT_ID="f04f071547d9-im-bot"

echo "[$TIMESTAMP] 准备发送消息到微信..." >> "$LOG_FILE"

# 微信配置参数
WECHAT_USER_ID="o9cq8002wI7v_8qzHYnYxS5S1ofc@im.wechat"
WECHAT_ACCOUNT_ID="f04f071547d9-im-bot"

# 尝试通过 message 工具发送微信消息
echo "[$TIMESTAMP] 尝试通过 message 工具发送微信消息..." >> "$LOG_FILE"

# 使用 openclaw CLI 发送消息
OPENCLAW_PATH="/root/.local/share/pnpm/openclaw"
MESSAGE_RESULT=$("$OPENCLAW_PATH" message action=send channel=openclaw-weixin to="$WECHAT_USER_ID" accountId="$WECHAT_ACCOUNT_ID" message="$MESSAGE" 2>&1)

if echo "$MESSAGE_RESULT" | grep -q "messageId"; then
    echo "[$TIMESTAMP] ✅ 微信消息发送成功" >> "$LOG_FILE"
    MESSAGE_ID=$(echo "$MESSAGE_RESULT" | grep -o '"messageId":"[^"]*' | cut -d'"' -f4)
    echo "[$TIMESTAMP] 消息ID: $MESSAGE_ID" >> "$LOG_FILE"
elif [ $? -eq 0 ]; then
    echo "[$TIMESTAMP] ✅ 微信消息发送成功（未获取到消息ID）" >> "$LOG_FILE"
else
    echo "[$TIMESTAMP] ❌ 微信消息发送失败" >> "$LOG_FILE"
    echo "[$TIMESTAMP] 错误信息: $MESSAGE_RESULT" >> "$LOG_FILE"
    
    # 备用方案：保存到待发送文件
    echo "[$TIMESTAMP] 尝试备用发送方案..." >> "$LOG_FILE"
    
    PENDING_FILE="/root/.openclaw/logs/pending-messages.log"
    echo "[$TIMESTAMP] $MESSAGE" >> "$PENDING_FILE"
    echo "[$TIMESTAMP] 消息已保存到待发送文件: $PENDING_FILE" >> "$LOG_FILE"
fi

echo "==========================================" >> "$LOG_FILE"
echo "微信进展汇报完成 - $TIMESTAMP" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 输出到控制台
echo "✅ 微信进展汇报脚本执行完成"
echo "📝 消息已构建，需要配置微信发送"
echo "📋 消息内容预览："
echo "----------------------------------------"
echo "$MESSAGE"
echo "----------------------------------------"
echo "📁 详细日志: $LOG_FILE"