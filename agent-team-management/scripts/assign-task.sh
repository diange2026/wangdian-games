#!/bin/bash

# 🎯 智能体任务分配脚本
# 将任务分配给智能体团队

echo "📋 智能体任务分配系统"
echo "===================="
echo ""

# 检查参数
if [ $# -lt 2 ]; then
    echo "使用方法: $0 <项目名称> <任务描述> [优先级]"
    echo ""
    echo "示例:"
    echo "  $0 \"工贸企业相关方全流程管理系统\" \"开发手续文档管理模块\""
    echo "  $0 \"智能体团队管理\" \"配置代码审查系统\" \"高\""
    echo ""
    exit 1
fi

PROJECT_NAME="$1"
TASK_DESCRIPTION="$2"
PRIORITY="${3:-中}"  # 默认优先级为中

echo "🎯 任务详情："
echo "  项目: $PROJECT_NAME"
echo "  任务: $TASK_DESCRIPTION"
echo "  优先级: $PRIORITY"
echo "  时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 可用的智能体列表
AGENTS=(
    "agent-autopilot:自动驾驶核心;开发、部署、项目管理"
    "self-improving-agent-cn:自我改进;学习、优化、经验积累"
    "agent-memory:记忆系统;知识管理、避免重复错误"
    "agent-browser:浏览器自动化;网页操作、数据采集"
)

echo "🤖 可用的智能体："
echo "-----------------"

for agent_info in "${AGENTS[@]}"; do
    IFS=':' read -r agent_name agent_desc agent_capabilities <<< "$agent_info"
    echo "  • $agent_name - $agent_desc"
    echo "    能力: $agent_capabilities"
done

echo ""

# 根据任务类型选择合适的智能体
echo "🔍 智能体推荐："
echo "----------------"

case "$TASK_DESCRIPTION" in
    *开发*|*编码*|*编程*)
        RECOMMENDED_AGENT="agent-autopilot"
        REASON="开发任务适合自动驾驶智能体"
        ;;
    *学习*|*优化*|*改进*)
        RECOMMENDED_AGENT="self-improving-agent-cn"
        REASON="学习改进任务适合自我改进智能体"
        ;;
    *记忆*|*知识*|*经验*)
        RECOMMENDED_AGENT="agent-memory"
        REASON="知识管理任务适合记忆系统"
        ;;
    *网页*|*浏览器*|*数据采集*)
        RECOMMENDED_AGENT="agent-browser-clawdbot"
        REASON="网页操作任务适合浏览器自动化"
        ;;
    *)
        RECOMMENDED_AGENT="agent-autopilot"
        REASON="默认分配给自动驾驶智能体"
        ;;
esac

echo "  推荐智能体: $RECOMMENDED_AGENT"
echo "  推荐理由: $REASON"
echo ""

# 分配任务
echo "📝 任务分配："
echo "--------------"

# 任务ID
TASK_ID="TASK-$(date +%Y%m%d-%H%M%S)"

# 任务文件
TASK_DIR="/root/.openclaw/workspace/agent-team-management/tasks"
mkdir -p "$TASK_DIR"

TASK_FILE="$TASK_DIR/$TASK_ID.task"

# 创建任务文件
cat > "$TASK_FILE" << EOF
# 任务ID: $TASK_ID
# 创建时间: $(date '+%Y-%m-%d %H:%M:%S')
# 项目: $PROJECT_NAME
# 任务描述: $TASK_DESCRIPTION
# 优先级: $PRIORITY
# 分配的智能体: $RECOMMENDED_AGENT
# 状态: 待执行

## 任务详情
$TASK_DESCRIPTION

## 智能体能力要求
- 任务类型: 根据描述自动判断
- 所需技能: 根据智能体能力匹配
- 预计耗时: 待评估

## 进度跟踪
- [ ] 任务已接收
- [ ] 任务分析完成
- [ ] 执行计划制定
- [ ] 任务执行中
- [ ] 任务完成
- [ ] 成果验证
- [ ] 任务关闭

## 记录
$(date '+%Y-%m-%d %H:%M:%S') - 任务创建
EOF

echo "✅ 任务创建成功！"
echo ""
echo "📁 任务信息："
echo "  任务ID: $TASK_ID"
echo "  任务文件: $TASK_FILE"
echo "  分配的智能体: $RECOMMENDED_AGENT"
echo "  状态: 待执行"
echo ""

# 添加到任务队列
TASK_QUEUE="$TASK_DIR/task-queue.txt"
echo "$(date '+%Y-%m-%d %H:%M:%S') | $TASK_ID | $PROJECT_NAME | $TASK_DESCRIPTION | $PRIORITY | $RECOMMENDED_AGENT | 待执行" >> "$TASK_QUEUE"

echo "📋 任务队列状态："
echo "-----------------"
if [ -f "$TASK_QUEUE" ]; then
    echo "任务ID         | 项目                 | 状态"
    echo "-------------|---------------------|----------"
    tail -5 "$TASK_QUEUE" | while read line; do
        IFS='|' read -r timestamp task_id project_name task_desc priority agent status <<< "$line"
        echo "$task_id | $project_name | $status"
    done
else
    echo "暂无任务在队列中"
fi

echo ""
echo "🎯 下一步操作："
echo "  1. 智能体将自动开始执行任务"
echo "  2. 查看任务进度: ./task-status.sh $TASK_ID"
echo "  3. 查看所有任务: ./list-tasks.sh"
echo ""

# 记录到历史
TASK_HISTORY="/root/.openclaw/workspace/task-history.log"
echo "$(date '+%Y-%m-%d %H:%M:%S') - 分配任务: $TASK_ID - $PROJECT_NAME - $TASK_DESCRIPTION" >> "$TASK_HISTORY"

echo "✅ 任务分配完成！"
echo "=============================="
echo ""