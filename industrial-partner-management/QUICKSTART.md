# 工贸企业相关方全流程管理系统 - 快速启动指南

## 🚀 项目概览
这是一个全流程的工贸企业相关方管理平台，基于现代技术栈构建，支持从单位资质管理到全流程管控的完整功能。

## 📁 项目结构
```
industrial-partner-management/
├── frontend/          # Vue 3 前端项目
├── backend/           # FastAPI 后端项目
├── docker/            # Docker 配置文件
├── docs/              # 设计文档
├── scripts/           # 部署和数据库脚本
└── tests/            # 测试文件
```

## ⚡ 快速启动

### 1. 启动后端服务
```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
python -m app.main
```

后端服务将在 `http://localhost:8000` 启动
- API 文档：`http://localhost:8000/docs`
- 健康检查：`http://localhost:8000/health`

### 2. 初始化数据库
```bash
# 确保 MySQL 服务正在运行
# 执行初始化脚本
mysql -u root -p < scripts/init-database.sql
```

这将创建：
- `industrial_partner_management` 数据库
- 所有核心业务表
- 默认预警配置
- 测试数据

### 3. 启动前端服务
```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 `http://localhost:3000` 启动

## 🔧 技术栈
- **前端**: Vue 3 + TypeScript + Element Plus + ECharts
- **后端**: Python FastAPI + SQLAlchemy + MySQL
- **数据库**: MySQL 8.0 + Redis (可选)
- **部署**: Docker + Docker Compose

## 🌐 访问地址
- 前端: `http://localhost:3000`
- 后端 API: `http://localhost:8000`
- API 文档: `http://localhost:8000/docs`
- 文件上传: `http://localhost:8000/uploads`

## 📊 默认账户
- **应用数据库用户**: `partner_app`
- **密码**: `AppPassword@2024`
- **只读数据库用户**: `partner_readonly`
- **密码**: `Readonly@2024`

## 🚀 已完成功能
### ✅ 第一阶段：基础档案与资质管理
1. ✅ **单位资质管理模块**
   - 数据库设计完成
   - 后端 API 完成（CRUD、查询、统计）
   - 前端界面完成（列表、详情、表单）

2. 🔄 **人员资质管理模块**
   - 数据库设计（待完成）
   - 后端 API（待完成）
   - 前端界面（待完成）

3. ⏳ **手续文档管理**
   - 数据库设计（待完成）
   - 后端 API（待完成）
   - 前端界面（待完成）

## 🔧 开发环境设置

### 1. Python 环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows



# 安装依赖
pip install -r requirements.txt
```

### 2. Node.js 环境
```bash
# 安装 Node.js（推荐 18+）
# 验证安装
node --version
npm --version



# 安装依赖
npm install
```

### 3. 数据库环境
```bash
# 安装 MySQL 8.0
# 启动 MySQL 服务
sudo systemctl start mysql  # Linux
# 或使用 brew services start mysql  # Mac



# 验证连接
mysql --version
```

## 🐳 Docker 部署（可选）

### 1. 构建和运行
```bash
# 构建所有服务
docker-compose build



# 启动服务
docker-compose up -d



# 查看日志
docker-compose logs -f
```

### 2. 停止服务
```bash
# 停止服务
docker-compose down



# 停止并删除卷
docker-compose down -v
```

## 🧪 测试

### 1. 后端测试
```bash
# 运行所有测试
pytest



# 运行特定测试
pytest tests/ -v



# 生成测试覆盖率报告
pytest --cov=app tests/
```

### 2. 前端测试
```bash
# 运行单元测试
npm test



# 运行端到端测试
npm run test:e2e
```

## 🔍 API 使用示例

### 1. 获取单位列表
```bash
curl -X GET "http://localhost:8000/api/v1/companies/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 2. 创建新单位
```bash
curl -X POST "http://localhost:8000/api/v1/companies/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "company_code": "TEST001",
    "company_name": "测试公司",
    "company_type": "supplier",
    "contact_person": "张三",
    "contact_phone": "13800138000"
  }'
```

## 📈 开发进度
- **总体进度**: 15%
- **第一阶段**: 33% 完成
- **计划完成时间**: 30天

## 📞 支持
- 问题报告：在仓库中创建 Issue
- 开发讨论：项目文档或开发群组
- 紧急问题：直接联系开发团队

## 🔄 持续集成
项目配置了自动化：
- 代码质量检查（linting）
- 单元测试自动化
- 构建和部署流水线

---

**提示**: 开发过程中请定期提交代码并更新文档。确保测试覆盖率维持在 80% 以上。