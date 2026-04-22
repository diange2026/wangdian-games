#!/bin/bash

# 📊 任务状态查看脚本
# 查看智能体任务执行状态

echo "📋 智能体任务状态监控"
echo "===================="
echo ""

# 检查参数
if [ $# -eq 0 ]; then
    echo "使用方法:"
    echo "  $0 <任务ID>              # 查看特定任务状态"
    echo "  $0 all                  # 查看所有任务状态"
    echo "  $0 queue                # 查看任务队列"
    echo ""
    exit 1
fi

TASK_ID="$1"
TASK_DIR="/root/.openclaw/workspace/agent-team-management/tasks"
TASK_QUEUE="$TASK_DIR/task-queue.txt"

echo "⏰ 查询时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

if [ "$TASK_ID" = "all" ]; then
    echo "📊 所有任务状态"
    echo "--------------"
    
    if [ -f "$TASK_QUEUE" ]; then
        echo "任务ID         | 项目                 | 任务描述           | 智能体         | 状态    | 优先级"
        echo "-------------|---------------------|-------------------|---------------|--------|-------"
        cat "$TASK_QUEUE" | while read line; do
            IFS='|' read -r timestamp task_id project_name task_desc priority agent status <<< "$line"
            # 简化显示
            short_project=$(echo "$project_name" | cut -c1-20)
            short_desc=$(echo "$task_desc" | cut -c1-18)
            short_agent=$(echo "$agent" | cut -c1-12)
            echo "$task_id | $short_project | $short_desc | $short_agent | $status | $priority"
        done
    else
        echo "暂无任务记录"
    fi
    
elif [ "$TASK_ID" = "queue" ]; then
    echo "📋 任务队列状态"
    echo "--------------"
    
    if [ -f "$TASK_QUEUE" ]; then
        # 统计各类状态
        TOTAL=$(wc -l < "$TASK_QUEUE")
        PENDING=$(grep -c "待执行" "$TASK_QUEUE" || echo "0")
        RUNNING=$(grep -c "执行中" "$TASK_QUEUE" || echo "0")
        COMPLETED=$(grep -c "已完成" "$TASK_QUEUE" || echo "0")
        
        echo "📈 队列统计:"
        echo "  总任务数: $TOTAL"
        echo "  待执行: $PENDING"
        echo "  执行中: $RUNNING"
        echo "  已完成: $COMPLETED"
        echo ""
        
        echo "📋 详细队列:"
        grep -n "待执行\|执行中" "$TASK_QUEUE" 2>/dev/null || echo "  无待处理任务"
    else
        echo "暂无任务队列"
    fi
    
else
    # 查看特定任务
    echo "🔍 任务详情: $TASK_ID"
    echo "--------------"
    
    TASK_FILE="$TASK_DIR/$TASK_ID.task"
    
    if [ -f "$TASK_FILE" ]; then
        # 显示任务基本信息
        echo "📋 任务基本信息:"
        echo "---------------"
        
        grep -E "^# (任务ID|创建时间|项目|任务描述|优先级|分配的智能体|状态):" "$TASK_FILE" | while read line; do
            echo "$line" | sed 's/^# //'
        done
        
        echo ""
        
        # 显示进度跟踪
        echo "📊 任务进度跟踪:"
        echo "---------------"
        
        grep -E "^- \[[ x]\]" "$TASK_FILE" | while read line; do
            echo "$line"
        done
        
        echo ""
        
        # 显示任务记录
        echo "📝 任务记录:"
        echo "-----------"
        
        grep -E "^[0-9]{4}-[0-9]{2}-[0-9]{2}" "$TASK_FILE" | tail -10 | while read line; do
            echo "  • $line"
        done
        
        # 检查任务状态文件
        STATUS_FILE="$TASK_DIR/$TASK_ID.status"
        if [ -f "$STATUS_FILE" ]; then
            echo ""
            echo "🚀 任务执行状态:"
            echo "--------------"
            cat "$STATUS_FILE"
        fi
        
    else
        echo "❌ 任务不存在: $TASK_ID"
        echo ""
        echo "📋 可用的任务ID:"
        echo "--------------"
        if [ -f "$TASK_QUEUE" ]; then
            cat "$TASK_QUEUE" | awk -F'|' '{print $2}' | sort | uniq
        else
            echo "暂无任务记录"
        fi
    fi
fi

echo ""
echo "=============================="
echo "🎯 任务状态查询完成"
echo "=============================="
echo ""