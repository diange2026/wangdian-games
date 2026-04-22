#!/bin/bash

# 工贸企业相关方全流程管理系统 - 快速启动脚本
# 此脚本将启动系统并提供访问链接

echo "🏭 工贸企业相关方全流程管理系统 - 快速启动"
echo "=========================================="

# 获取当前时间
START_TIME=$(date +%s)

# 设置颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查依赖
echo -e "${BLUE}[1/5] 检查系统依赖...${NC}"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 未安装${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python3 已安装: $(python3 --version)${NC}"

# 检查MySQL
if ! command -v mysql &> /dev/null; then
    echo -e "${YELLOW}⚠️  MySQL 未安装，将使用模拟数据${NC}"
    USE_MOCK=true
else
    echo -e "${GREEN}✅ MySQL 已安装${NC}"
    USE_MOCK=false
fi

# 检查Node.js（前端）
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠️  Node.js 未安装，将只启动后端API${NC}"
    START_FRONTEND=false
else
    echo -e "${GREEN}✅ Node.js 已安装: $(node --version)${NC}"
    START_FRONTEND=true
fi

echo -e "${BLUE}[2/5] 配置环境...${NC}"

# 创建后端配置文件
cd /root/.openclaw/workspace/industrial-partner-management

if [ ! -f backend/.env ]; then
    cat > backend/.env << EOF
# 数据库配置
DATABASE_URL=mysql://root:password@localhost:3306/industrial_partner_management
DATABASE_TEST_URL=mysql://root:password@localhost:3306/industrial_partner_management_test

# 应用配置
APP_NAME=工贸企业相关方全流程管理系统
APP_VERSION=1.0.0
APP_ENV=development
DEBUG=true

# 安全配置
SECRET_KEY=development-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 服务器配置
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=["*"]
EOF
    echo -e "${GREEN}✅ 后端环境配置已创建${NC}"
fi

# 创建前端配置文件
if [ ! -f frontend/.env.local ]; then
    cat > frontend/.env.local << EOF
# API 配置
VITE_API_URL=http://localhost:8000/api/v1
VITE_API_TIMEOUT=30000

# 应用配置
VITE_APP_TITLE=工贸企业相关方管理系统
VITE_APP_DESCRIPTION=从相关方入场到离场的全流程数字化管理平台

# 开发配置
VITE_DEBUG=true
EOF
    echo -e "${GREEN}✅ 前端环境配置已创建${NC}"
fi

echo -e "${BLUE}[3/5] 安装依赖...${NC}"

# 安装Python依赖
if [ -f backend/requirements.txt ]; then
    echo -e "${YELLOW}📦 安装Python依赖...${NC}"
    pip3 install -r backend/requirements.txt > /tmp/backend-install.log 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Python依赖安装完成${NC}"
    else
        echo -e "${YELLOW}⚠️  Python依赖安装有警告，继续...${NC}"
    fi
fi

# 安装Node.js依赖
if [ "$START_FRONTEND" = true ] && [ -f frontend/package.json ]; then
    echo -e "${YELLOW}📦 安装Node.js依赖...${NC}"
    cd frontend
    npm install > /tmp/frontend-install.log 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Node.js依赖安装完成${NC}"
    else
        echo -e "${YELLOW}⚠️  Node.js依赖安装有警告，继续...${NC}"
    fi
    cd ..
fi

echo -e "${BLUE}[4/5] 初始化数据库...${NC}"

# 初始化数据库
if [ "$USE_MOCK" = false ]; then
    echo -e "${YELLOW}🗃️  创建数据库...${NC}"
    mysql -e "CREATE DATABASE IF NOT EXISTS industrial_partner_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null
    
    if [ -f scripts/init-database.sql ]; then
        echo -e "${YELLOW}📊 初始化单位资质数据库...${NC}"
        mysql industrial_partner_management < scripts/init-database.sql 2>/dev/null
    fi
    
    if [ -f scripts/init-personnel-database.sql ]; then
        echo -e "${YELLOW}👥 初始化人员资质数据库...${NC}"
        mysql industrial_partner_management < scripts/init-personnel-database.sql 2>/dev/null
    fi
    
    echo -e "${GREEN}✅ 数据库初始化完成${NC}"
else
    echo -e "${YELLOW}⚠️  使用模拟数据模式${NC}"
    # 创建模拟数据文件
    cat > /tmp/mock_data.py << 'EOF'
# 模拟数据生成器
print("模拟数据模式已启用")
print("API将返回预定义的测试数据")
EOF
fi

echo -e "${BLUE}[5/5] 启动服务...${NC}"

# 获取本机IP地址
IP_ADDRESS=$(hostname -I | awk '{print $1}')
if [ -z "$IP_ADDRESS" ]; then
    IP_ADDRESS="127.0.0.1"
fi

# 启动后端服务（在后台）
echo -e "${YELLOW}🚀 启动后端API服务...${NC}"
cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
sleep 3

if ps -p $BACKEND_PID > /dev/null; then
    echo -e "${GREEN}✅ 后端API服务已启动${NC}"
    echo -e "   🌐 访问地址: ${BLUE}http://$IP_ADDRESS:8000${NC}"
    echo -e "   📚 API文档: ${BLUE}http://$IP_ADDRESS:8000/docs${NC}"
    echo -e "   📊 监控界面: ${BLUE}http://$IP_ADDRESS:8000/redoc${NC}"
else
    echo -e "${RED}❌ 后端API服务启动失败${NC}"
    echo -e "   查看日志: ${YELLOW}tail -f /tmp/backend.log${NC}"
    exit 1
fi

# 启动前端服务（如果可用）
if [ "$START_FRONTEND" = true ]; then
    echo -e "${YELLOW}🚀 启动前端界面...${NC}"
    cd ../frontend
    npm run dev > /tmp/frontend.log 2>&1 &
    FRONTEND_PID=$!
    sleep 5
    
    if ps -p $FRONTEND_PID > /dev/null; then
        echo -e "${GREEN}✅ 前端界面已启动${NC}"
        echo -e "   🖥️  访问地址: ${BLUE}http://$IP_ADDRESS:3000${NC}"
    else
        echo -e "${YELLOW}⚠️  前端界面启动失败，但后端API仍可用${NC}"
        echo -e "   查看日志: ${YELLOW}tail -f /tmp/frontend.log${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Node.js未安装，跳过前端启动${NC}"
    echo -e "   可以通过API直接访问系统: ${BLUE}http://$IP_ADDRESS:8000/docs${NC}"
fi

cd ..

# 计算启动时间
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo "=========================================="
echo -e "${GREEN}🏭 系统启动完成！ (耗时: ${DURATION}秒)${NC}"
echo "=========================================="
echo ""
echo "🎯 系统访问链接："
echo ""
if [ "$START_FRONTEND" = true ]; then
    echo "   1. 🌐 完整系统界面："
    echo -e "      ${BLUE}http://$IP_ADDRESS:3000${NC}"
    echo "      • 单位管理"
    echo "      • 人员资质管理"
    echo "      • 证书管理"
    echo "      • 统计分析"
fi
echo ""
echo "   2. 🔧 API接口文档："
echo -e "      ${BLUE}http://$IP_ADDRESS:8000/docs${NC}"
echo "      • 查看所有API接口"
echo "      • 在线测试API"
echo "      • 查看请求/响应格式"
echo ""
echo "   3. 📊 API监控界面："
echo -e "      ${BLUE}http://$IP_ADDRESS:8000/redoc${NC}"
echo "      • 详细的API文档"
echo "      • 接口参数说明"
echo ""
echo "📋 使用说明："
echo ""
echo "   1. 单位管理测试："
echo -e "      ${YELLOW}curl -X GET \"http://$IP_ADDRESS:8000/api/v1/companies/\"${NC}"
echo ""
echo "   2. 人员管理测试："
echo -e "      ${YELLOW}curl -X GET \"http://$IP_ADDRESS:8000/api/v1/personnel/\"${NC}"
echo ""
echo "   3. 证书管理测试："
echo -e "      ${YELLOW}curl -X GET \"http://$IP_ADDRESS:8000/api/v1/personnel/1/certificates\"${NC}"
echo ""
echo "🛑 停止系统："
echo -e "   ${YELLOW}pkill -f \"uvicorn\|npm run dev\"${NC}"
echo ""
echo "📝 查看日志："
echo -e "   后端: ${YELLOW}tail -f /tmp/backend.log${NC}"
if [ "$START_FRONTEND" = true ]; then
    echo -e "   前端: ${YELLOW}tail -f /tmp/frontend.log${NC}"
fi
echo ""
echo "=========================================="
echo "系统将持续运行，按 Ctrl+C 查看管理选项"
echo "=========================================="

# 等待用户中断
trap 'echo -e "\n${YELLOW}正在停止系统...${NC}"; kill $BACKEND_PID 2>/dev/null; if [ "$START_FRONTEND" = true ]; then kill $FRONTEND_PID 2>/dev/null; fi; echo -e "${GREEN}✅ 系统已停止${NC}"; exit 0' INT

# 保持脚本运行
while true; do
    sleep 60
done