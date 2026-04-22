#!/bin/bash

# 🚀 集成系统启动脚本
# 启动完整的智能体团队管理系统（包含新技能）

echo "🏭 智能体团队管理系统（增强版）"
echo "==============================="
echo ""

echo "⏰ 启动时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

echo "🔍 检查系统组件..."
echo ""

# 检查核心智能体
echo "🎯 核心智能体状态:"
for skill in agent-autopilot self-improving-agent-cn agent-memory agent-browser-clawdbot; do
    if [ -d "/root/.openclaw/workspace/skills/$skill" ]; then
        echo "  ✅ $skill"
    else
        echo "  ⚠️  $skill (未安装)"
    fi
done

echo ""

# 检查新技能
echo "🆕 新集成技能:"
for skill in openclaw-team-builder team-communication; do
    if [ -d "/root/.openclaw/workspace/skills/$skill" ]; then
        echo "  ✅ $skill"
    else
        echo "  ❌ $skill (未安装)"
    fi
done

echo ""

echo "🚀 启动团队构建器..."
/root/.openclaw/workspace/agent-team-management/scripts/team-builder-interface.sh "工贸企业相关方全流程管理系统" 4 "开发,测试,部署,文档"

echo ""

echo "💬 启动团队沟通系统..."
/root/.openclaw/workspace/agent-team-management/scripts/team-communication-interface.sh broadcast "工贸企业团队"

echo ""

echo "📊 启动监控系统..."
/root/.openclaw/workspace/agent-team-management/scripts/agent-monitor.sh

echo ""

echo "🔧 系统配置检查..."
echo "  集成配置文件: /root/.openclaw/workspace/agent-team-management/integration-config.yml"
echo "  团队配置文件: /root/.openclaw/workspace/agent-team-management/teams/工贸企业相关方全流程管理系统-team.yml"
echo "  沟通日志文件: /root/.openclaw/workspace/agent-team-management/logs/communication.log"
echo "  任务队列文件: /root/.openclaw/workspace/agent-team-management/tasks/task-queue.txt"

echo ""

echo "🎯 可用命令:"
echo ""
echo "  团队构建:"
echo "    ./scripts/team-builder-interface.sh <项目> [规模] [角色]"
echo ""
echo "  团队沟通:"
echo "    ./scripts/team-communication-interface.sh <动作> <团队> [消息]"
echo ""
echo "  任务管理:"
echo "    ./scripts/assign-task.sh <项目> <任务> [优先级]"
echo ""
echo "  系统监控:"
echo "    ./scripts/agent-monitor.sh"
echo ""
echo "  报告生成:"
echo "    ./scripts/generate-team-report.sh"

echo ""

echo "📁 系统目录:"
echo "  /root/.openclaw/workspace/agent-team-management/"
echo "  ├── scripts/          # 管理脚本"
echo "  ├── tasks/           # 任务存储"
echo "  ├── reports/         # 报告存储"
echo "  ├── teams/           # 团队配置"
echo "  └── logs/            # 系统日志"

echo ""

echo "=========================================="
echo "✅ 智能体团队管理系统（增强版）启动完成！"
echo "=========================================="
echo ""
echo "🎉 系统现在包含:"
echo "  • 4个核心智能体"
echo "  • 2个新团队管理技能"
echo "  • 完整的团队构建功能"
echo "  • 实时的团队沟通系统"
echo "  • 自动化任务管理"
echo "  • 实时监控和报告"
echo ""
echo "🚀 现在可以开始使用增强版的智能体团队管理系统了！"
