# 🛠️ 系统运维能力说明

## 📋 自动化任务列表

| 任务名称 | 执行时间 | 说明 | 状态 |
|---------|---------|------|------|
| **每日自动备份 workspace** | 凌晨 2:00 | Git 自动 commit + push | ✅ 已启用 |
| **每日中午备份 workspace** | 中午 12:30 | Git 自动 commit + push | ✅ 已启用 |
| **每日系统健康检查与维护** | 早上 6:00 | 系统检查 + 清理 + 报告 | ✅ 已启用 |

---

## 🔧 运维脚本

### 脚本位置
```
/root/.openclaw/workspace/scripts/ops-maintenance.sh
```

### 使用方法

```bash
# 完整报告
./ops-maintenance.sh report

# 快速检查
./ops-maintenance.sh check

# 系统清理
./ops-maintenance.sh clean

# 重启服务
./ops-maintenance.sh restart

# 备份验证
./ops-maintenance.sh verify
```

### 功能说明

| 命令 | 功能 |
|------|------|
| `report` | 生成完整运维报告（默认） |
| `check` | 快速检查资源、服务、网络 |
| `clean` | 清理 apt 缓存、journal 日志、临时文件 |
| `restart` | 重启 OpenClaw Gateway 服务 |
| `verify` | 验证 Git 备份状态 |

---

## 📊 监测指标

### 系统资源
- ✅ 内存使用率（告警阈值：80%）
- ✅ 磁盘使用率（告警阈值：80%）
- ✅ CPU 负载
- ✅ CPU 核心数

### 服务状态
- ✅ OpenClaw Gateway 运行状态
- ✅ OpenClaw 进程数

### 网络检查
- ✅ 外网连通性（8.8.8.8）
- ✅ GitHub 连通性

### 备份验证
- ✅ Git 本地/远程同步状态
- ✅ 最后提交时间

---

## ⚠️ 告警机制

当检测到以下情况时，会在报告中显示告警：

1. **内存使用率 > 80%** - 需要关注内存泄漏或优化
2. **磁盘使用率 > 80%** - 需要清理空间或扩容
3. **服务未运行** - 尝试自动重启
4. **网络异常** - 可能影响备份和外网访问
5. **备份不同步** - 需要手动检查 Git 状态

---

## 📝 日志位置

运维日志保存在：
```
/var/log/openclaw-ops.log
```

查看最新日志：
```bash
tail -50 /var/log/openclaw-ops.log
```

---

## 🔄 手动触发

### 立即执行系统检查
```bash
/root/.openclaw/workspace/scripts/ops-maintenance.sh report
```

### 立即执行备份
```bash
cd /root/.openclaw/workspace
git add .
git commit -m "手动备份：$(date +%Y-%m-%d %H:%M)"
git push origin main
```

### 查看 cron 任务状态
```bash
# 在 OpenClaw 中查询 cron 列表
```

---

## 📅 下次执行时间

- **系统检查**: 明天早上 6:00
- **凌晨备份**: 明天凌晨 2:00
- **中午备份**: 明天中午 12:30

---

## 🎯 运维目标

1. **数据安全性** - 每日两次备份，确保数据不丢失
2. **系统稳定性** - 每日健康检查，及时发现和修复问题
3. **资源优化** - 自动清理无用文件，保持系统整洁
4. **可观测性** - 详细日志和报告，方便问题排查

---

_最后更新：2026-03-28_
