#!/bin/bash

# 测试 cron 是否正常工作的脚本
TEST_LOG="/root/.openclaw/logs/test-cron.log"

echo "==========================================" >> "$TEST_LOG"
echo "Cron 测试执行 - $(date '+%Y-%m-%d %H:%M:%S')" >> "$TEST_LOG"
echo "脚本路径: $0" >> "$TEST_LOG"
echo "当前用户: $(whoami)" >> "$TEST_LOG"
echo "当前目录: $(pwd)" >> "$TEST_LOG"
echo "==========================================" >> "$TEST_LOG"
echo "" >> "$TEST_LOG"

echo "✅ Cron 测试脚本执行成功！"
echo "📝 日志已写入: $TEST_LOG"