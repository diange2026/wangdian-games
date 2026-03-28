# 分层记忆系统

_小 Q 的记忆系统 - 结构化、可备份、可持续_

---

## 📚 记忆层级结构

```
memory/
├── README.md              # 本文件 - 记忆系统说明
├── YYYY-MM-DD.md          # 每日对话日志（按日期）
├── users/                 # 用户信息层
│   └── 王典.md            # 典哥的详细信息
├── projects/              # 项目记忆层
│   ├── 猜数字游戏.md       # 游戏项目记录
│   └── TEMPLATE.md        # 新项目模板
├── preferences/           # 偏好设置层
│   └── 沟通偏好.md         # 沟通风格、服务偏好等
├── knowledge/             # 知识技能层
│   ├── 可用工具.md         # 我会用的工具清单
│   └── 已知问题.md         # 系统问题记录
└── archives/              # 归档层（过时但保留的记忆）
    └── .gitkeep
```

---

## 🎯 各层级说明

### 1️⃣ 每日日志层 (`YYYY-MM-DD.md`)
- **用途**: 记录每天的对话要点、事件、决定
- **更新频率**: 每天自动创建/更新
- **保留策略**: 永久保留，定期归档

### 2️⃣ 用户信息层 (`users/`)
- **用途**: 记录用户详细信息（姓名、称呼、背景、目标等）
- **更新频率**: 有新信息时更新
- **文件命名**: `用户名.md`

### 3️⃣ 项目记忆层 (`projects/`)
- **用途**: 记录进行中的项目、已完成的项目
- **更新频率**: 项目有进展时更新
- **文件命名**: `项目名.md`

### 4️⃣ 偏好设置层 (`preferences/`)
- **用途**: 记录用户偏好（沟通风格、服务偏好、禁忌等）
- **更新频率**: 发现新偏好时更新
- **文件命名**: `偏好类别.md`

### 5️⃣ 知识技能层 (`knowledge/`)
- **用途**: 记录我会的工具、已知问题、解决方案
- **更新频率**: 学习新东西时更新
- **文件命名**: `主题.md`

### 6️⃣ 归档层 (`archives/`)
- **用途**: 存放过时的记忆（删除可惜，但不再活跃）
- **更新频率**: 定期整理
- **文件命名**: `原文件名_归档日期.md`

---

## 🔄 记忆更新流程

### 每次对话后
1. 更新当日日志 (`YYYY-MM-DD.md`)
2. 如有新信息，更新相应用户/项目/偏好文件
3. 重要决定同步到 `MEMORY.md`（长期记忆）

### 每周回顾
1. 检查是否有过时信息需要归档
2. 整理项目状态（进行中 → 已完成 → 归档）
3. 更新知识技能层

### 每月清理
1. 将早期日志移动到 `archives/`
2. 精简 `MEMORY.md`，保留核心信息

---

## 💾 备份策略

### 备份位置
- **主备份**: `/data/openclaw-memory-backup/`
- **备份频率**: 每次重要更新后自动备份
- **备份脚本**: `/root/.openclaw/workspace/scripts/backup-memory.sh`

### 备份内容
- `memory/` 全部文件
- `MEMORY.md`
- `USER.md`
- `IDENTITY.md`

### 恢复方法
```bash
# 从备份恢复
cp -r /data/openclaw-memory-backup/memory/* /root/.openclaw/workspace/memory/
cp /data/openclaw-memory-backup/MEMORY.md /root/.openclaw/workspace/
cp /data/openclaw-memory-backup/USER.md /root/.openclaw/workspace/
cp /data/openclaw-memory-backup/IDENTITY.md /root/.openclaw/workspace/
```

---

## 📝 使用指南

### 创建新项目记忆
```bash
# 复制模板
cp memory/projects/TEMPLATE.md memory/projects/新项目名.md
# 编辑内容
```

### 添加用户信息
```bash
# 创建或更新用户文件
# memory/users/用户名.md
```

### 归档旧记忆
```bash
# 移动到归档目录
mv memory/YYYY-MM-DD.md memory/archives/YYYY-MM-DD_归档日期.md
```

---

_最后更新：2026-03-28_
