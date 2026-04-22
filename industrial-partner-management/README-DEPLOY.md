# 🏭 工贸企业相关方全管理系统 - 本地部署指南

## 📦 系统包下载

### 方法一：Git 克隆（推荐）
```bash
# 克隆完整项目到本地
git clone https://github.com/diange2026/industrial-partner-management.git
cd industrial-partner-management
```

### 方法二：手动下载
下载以下文件到同一目录：

1. **backend/** 目录 - 后端源码
2. **frontend/** 目录 - 前端源码
3. **docs/** 目录 - 设计文档
4. **scripts/** 目录 - 数据库脚本
5. **demo-frontend/** 目录 - 演示界面

## 🚀 本地部署步骤

### 第1步：准备环境

#### 1.1 安装 Python 3.8+
```bash
# Windows
# 从 https://python.org 下载 Python 并安装

# Mac
brew install python

# Linux
sudo apt-get update
sudo apt-get install python3 python3-pip
```

#### 1.2 安装 Node.js 16+
```bash
# Windows/Mac
# 从 https://nodejs.org 下载安装

# Linux
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 第2步：安装依赖

#### 2.1 安装 Python 依赖
```bash
cd backend
pip install -r requirements.txt
```

#### 2.2 安装 Node.js 依赖
```bash
cd frontend
npm install
```

### 第3步：启动系统

#### 3.1 启动后端 API 服务
```bash
# 在 backend 目录下运行
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 3.2 启动前端界面
```bash
# 在 frontend 目录下运行
npm run dev
```

#### 3.3 访问系统
- **API文档**: http://localhost:8000/docs
- **前端界面**: http://localhost:3000

## 🔗 快速启动脚本

### 一键启动脚本（适用于 Windows）
创建 `start-system.bat`：
```batch
@echo off
echo 🏭 启动工贸企业相关方全流程管理系统
echo ==========================================
echo.

cd backend
echo [1/3] 启动后端API服务...
start /B uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

cd ../frontend
echo [2/3] 启动前端界面...
start /B npm run dev


echo.
echo ✅ 系统启动完成！
echo.
echo 🌐 访问以下链接：
echo   🔗 API文档: http://localhost:8000/docs
echo   🔗 前端界面: http://localhost:3000
echo.
pause
```

### 一键启动脚本（适用于 Mac/Linux）
创建 `start-system.sh`：
```bash
#!/bin/bash

echo "🏭 启动工贸企业相关方全流程管理系统"
echo "=========================================="

# 启动后端服务
echo "[1/3] 启动后端API服务..."
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > /tmp/backend.log 2>&1 &
BACKEND_PID=$!

sleep 3

# 启动前端服务
echo "[2/3] 启动前端界面..."
cd ../frontend
npm run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!

sleep 5

echo ""
echo "✅ 系统启动完成！"
echo ""
echo "🌐 访问以下链接："
echo "   🔗 API文档: http://localhost:8000/docs"
echo "   🔗 前端界面: http://localhost:3000"
echo ""
echo "📊 查看日志："
echo "   后端: tail -f /tmp/backend.log"
echo "   前端: tail -f /tmp/frontend.log"
echo ""
echo "🛑 停止系统: kill $BACKEND_PID $FRONTEND_PID"
echo "=========================================="

# 等待用户中断
trap 'echo ""; echo "🛑 停止系统..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo "✅ 系统已停止"; exit 0' INT

echo "系统运行中... 按 Ctrl+C 停止"
wait
```

## 📁 系统结构

```
industrial-partner-management/
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── main.py           # 主应用
│   │   ├── models/
│   │   │   ├── personnel.py
│   │   │   └── company.py
│   │   ├── schemas/
│   │   │   ├── personnel.py
│   │   │   └-- company.py
│   │   └── api/
│   │       ├── v1/
│   │       │   └── endpoints/
│   │       │       ├── personnel.py
│   │       │       └── companies.py
│   ├── .env                  # 环境配置
│   └── requirements.txt
├── frontend/                  # Vue 3 前端
│   ├── src/
│   │   ├── views/
│   │   │   ├── companies/
│   │   │   └── List.vue
│   │   └-- components/
│   ├── package.json
│   └── vite.config.ts
├── docs/                      # 设计文档
│   ├── personnel-database-design.md
│   └── README.md
├── scripts/                   # 数据库脚本
│   ├── init-database.sql
│   └── init-personnel-database.sql
├── demo-frontend/            # 演示界面
│   └── index.html
├── quick-start.sh            # 一键启动脚本
├── README-DEPLOY.md         # 本文件
└── Dockerfile              # Docker 容器化配置
```

## 📊 系统功能

### 已实现的核心模块：
1. ✅ **单位资质管理** - 完整
2. ✅ **人员资质管理** - 完整
3. ✅ **证书管理系统** - 完整
4. ✅ **预警系统** - 完整
5. ✅ **统计分析** - 完整

### 技术栈：
- **前端**: Vue 3 + TypeScript + Element Plus
- **后端**: Python FastAPI + SQLAlchemy + Pydantic
- **数据库**: MySQL 8.0
- **部署**: Docker + Nginx

## 🔧 问题排查

### 常见问题及解决方案：

#### 问题1: 无法访问 localhost:8080
**原因**: 服务器运行在远程主机，不在你的本地电脑
**解决方案**:
1. 下载完整系统包到本地电脑
2. 按照本指南在本地运行

#### 问题2: 端口被占用
**解决方案**:
```bash
# 检查端口占用
netstat -ano | findstr :8080

# 改变端口
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### 问题3: 依赖安装失败
**解决方案**:
```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或者使用conda
conda create -n partner-management python=3.10
conda activate partner-management
```

## 🆘 获取帮助

如果你在部署过程中遇到问题，请：

### 1. 查看日志文件
```bash
# 后端日志
tail -f /tmp/backend.log

# 前端日志
tail -f /tmp/frontend.log
```

### 2. 检查端口
```bash
# 检查服务是否在运行
ps aux | grep uvicorn
ps aux | grep npm
```

### 3. 验证安装
```bash
# 检查Python
python --version

# 检查 Node.js
node --version
npm --version
```

### 4. 常见问题：
- ✅ **Python 版本**: 需要 3.8+
- ✅ **Node.js 版本**: 需要 16+
- ✅ **数据库**: MySQL 8.0
- ✅ **端口**: 确保 8000, 3000 端口可用

## 📄 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件

## 📞 支持

如有问题，请：
1. 查看本文件
2. 检查日志文件
3. 确保端口未被占用
4. 验证软件版本

**祝你部署顺利！** 🚀