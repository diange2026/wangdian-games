# 每日进展汇报系统配置指南

## 概述

已成功配置每日三次进展汇报系统，执行时间：
- **早上 8:00** - 开始新的一天工作
- **中午 12:00** - 上午工作已过半
- **下午 17:00** - 即将结束今日工作

## 当前配置状态

✅ **已完成配置：**
1. 脚本创建：`/root/.openclaw/workspace/scripts/progress-report-weixin.sh`
2. 定时任务：已添加到 crontab（8:00, 12:00, 17:00）
3. 日志系统：`/root/.openclaw/logs/progress-report-weixin.log`
4. 测试运行：脚本已测试，消息构建正常

⚠️ **待完成配置：**
- 微信消息自动发送功能

## 微信消息发送配置方法

### 方法一：使用 OpenClaw message 工具（推荐）

在 `progress-report-weixin.sh` 脚本中添加以下代码：

```bash
# 在脚本末尾添加发送消息的代码
MESSAGE_CONTENT="这里放构建的消息内容"

# 发送消息到微信
message action=send \
  channel=openclaw-weixin \
  to="o9cq8002wI7v_8qzHYnYxS5S1ofc@im.wechat" \
  accountId="f04f071547d9-im-bot" \
  message="$MESSAGE_CONTENT"
```

### 方法二：手动配置步骤

1. **检查当前微信配置：**
```bash
openclaw config --get openclaw-weixin
```

2. **确保微信通道已正确配置**
3. **测试消息发送：**
```bash
openclaw weixin send --to "典哥微信ID" --message "测试消息"
```

### 方法三：使用 wecom_mcp 工具

如果配置了企业微信 MCP，可以使用：
```bash
# 先检查可用的工具
wecom_mcp list message

# 然后调用相应的发送方法
```

## 脚本功能说明

### 汇报内容
1. **系统状态概览**
   - OpenClaw Gateway 状态
   - 内存使用情况
   - 磁盘使用情况
   - Git 待提交文件数量

2. **系统链接**
   - GitHub 仓库链接
   - 本地工作空间路径
   - 日志目录位置

3. **当日计划提醒**
   - 根据星期几的提醒（周一升级、周日清理等）
   - 根据时间的提醒（早上计划、中午检查、下午汇总）

### 日志查看
```bash
# 查看最近汇报日志
tail -f /root/.openclaw/logs/progress-report-weixin.log

# 查看完整日志
cat /root/.openclaw/logs/progress-report-weixin.log
```

### 手动测试
```bash
# 手动运行汇报脚本
/root/.openclaw/workspace/scripts/progress-report-weixin.sh
```

## 定时任务管理

### 查看当前定时任务
```bash
crontab -l
```

### 编辑定时任务
```bash
crontab -e
```

### 定时任务条目
```
0 8 * * * /root/.openclaw/workspace/scripts/progress-report-weixin.sh
0 12 * * * /root/.openclaw/workspace/scripts/progress-report-weixin.sh  
0 17 * * * /root/.openclaw/workspace/scripts/progress-report-weixin.sh
```

## 故障排除

### 1. 脚本无法执行
```bash
# 检查脚本权限
chmod +x /root/.openclaw/workspace/scripts/progress-report-weixin.sh

# 检查脚本语法
bash -n /root/.openclaw/workspace/scripts/progress-report-weixin.sh
```

### 2. 定时任务不执行
```bash
# 检查 cron 服务状态
systemctl status cron

# 查看 cron 日志
grep CRON /var/log/syslog
```

### 3. 消息发送失败
- 检查微信通道配置
- 检查账户权限
- 查看 OpenClaw Gateway 日志

## 自定义配置

### 修改汇报时间
编辑 crontab：
```bash
crontab -e
```

### 修改汇报内容
编辑脚本文件：
```bash
nano /root/.openclaw/workspace/scripts/progress-report-weixin.sh
```

### 添加更多系统检查
在脚本中添加自定义检查函数。

---

**最后更新：2026-04-22**
**配置完成状态：90%（仅缺微信消息发送配置）**