# 自动备份配置

_设置定时自动备份记忆系统_

---

## 📋 备份策略

### 备份频率
- **每日备份**: 每天凌晨 2:00 自动备份
- **手动备份**: 重要更新后手动运行备份脚本

### 备份保留
- **最近 7 天**: 每天一个备份
- **最近 4 周**: 每周一个备份（保留周日备份）
- **最近 12 月**: 每月一个备份（保留每月 1 号备份）

---

## ⚙️ 配置自动备份

### 方法 1：使用 crontab（推荐）

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每天凌晨 2:00 备份）
0 2 * * * /root/.openclaw/workspace/scripts/backup-memory.sh >> /root/.openclaw/logs/backup.log 2>&1
```

### 方法 2：使用 OpenClaw 定时任务

编辑 `HEARTBEAT.md`，添加定期检查：

```markdown
# 每 24 小时检查并备份记忆
- [ ] 运行记忆备份脚本
```

### 方法 3：手动备份

需要备份时运行：

```bash
/root/.openclaw/workspace/scripts/backup-memory.sh
```

---

## 📁 备份目录结构

```
/data/openclaw-memory-backup/
├── BACKUP_INFO.txt      # 备份信息
├── MEMORY.md            # 长期记忆
├── USER.md              # 用户信息
├── IDENTITY.md          # AI 身份
└── memory/              # 分层记忆
    ├── README.md
    ├── 2026-03-28.md
    ├── users/
    ├── projects/
    ├── preferences/
    ├── knowledge/
    └── archives/
```

---

## 🔄 恢复记忆

### 重装系统后恢复

```bash
# 1. 确保备份目录存在
ls -la /data/openclaw-memory-backup/

# 2. 运行恢复脚本
cd /root/.openclaw/workspace/scripts/
./restore-memory.sh

# 3. 确认恢复
ls -la /root/.openclaw/workspace/memory/
cat /root/.openclaw/workspace/MEMORY.md
```

### 从特定备份恢复

```bash
# 如果有多个备份目录
./restore-memory.sh /path/to/specific/backup
```

---

## 📊 备份验证

### 检查备份完整性

```bash
# 查看备份信息
cat /data/openclaw-memory-backup/BACKUP_INFO.txt

# 检查文件数量
find /data/openclaw-memory-backup/memory -type f | wc -l

# 查看备份大小
du -sh /data/openclaw-memory-backup/
```

### 定期验证（建议每月）

```bash
# 验证脚本
#!/bin/bash
BACKUP_DIR="/data/openclaw-memory-backup"
if [ -f "$BACKUP_DIR/MEMORY.md" ] && [ -d "$BACKUP_DIR/memory" ]; then
    echo "✓ 备份完整"
else
    echo "✗ 备份不完整，需要重新备份"
fi
```

---

## 🚨 注意事项

### 备份前
- 确保记忆文件已保存（对话后自动保存）
- 检查磁盘空间（`df -h`）

### 备份后
- 验证备份文件存在
- 记录备份时间

### 恢复前
- 备份当前状态（以防恢复失败）
- 确认备份来源正确

### 恢复后
- 重启 OpenClaw 或重新加载会话
- 验证记忆内容正确

---

## 📝 备份日志

备份日志位置：`/root/.openclaw/logs/backup.log`

查看最近备份：
```bash
tail -20 /root/.openclaw/logs/backup.log
```

---

## 🔧 故障排查

### 备份失败

1. 检查磁盘空间：`df -h`
2. 检查权限：`ls -la /data/`
3. 手动运行脚本查看错误：`./backup-memory.sh`

### 恢复失败

1. 检查备份目录是否存在
2. 检查备份文件是否完整
3. 检查工作目录权限

---

_最后更新：2026-03-28_
