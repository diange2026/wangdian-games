# 🚀 企业级单位资质管理系统 - 部署指南

## 📋 系统概述

**企业级单位资质管理系统**是一个全方位、全生命周期、全景式的单位资质管理平台，提供从单位注册到资质注销的全流程数字化管理。

### ✨ 核心功能

- **🏢 单位信息全维度管理** - 全方位信息采集和展示
- **📋 资质证照全生命周期** - 从申请到吊销的完整流程
- **⚠️ 智能预警与风险监控** - 实时风险识别和告警
- **📊 大数据分析与报表** - 多维度统计和可视化分析
- **🔧 多平台多终端支持** - 桌面、移动端、API接口

---

## 🛠️ 系统架构

```
系统架构图
├── 前端层 (Frontend)
│   ├── Vue 3 + TypeScript
│   ├── Element Plus UI
│   ├── Pinia 状态管理
│   └── Vite 构建工具
├── API网关层 (API Gateway)
│   ├── Nginx 反向代理
│   ├── JWT 认证
│   └── 请求限流
├── 后端服务层 (Backend)
│   ├── FastAPI 框架
│   ├── SQLAlchemy ORM
│   ├── MySQL 数据库
│   └── Redis 缓存
├── 文件存储层 (Storage)
│   ├── 本地文件存储
│   └── 云存储 (可选)
└── 监控告警层 (Monitoring)
    ├── Prometheus 监控
    ├── Grafana 可视化
    └── 告警系统
```

---

## 📦 环境要求

### **1. 基础环境**
- **操作系统**: Ubuntu 20.04+ / CentOS 8+ / Windows Server 2019+
- **内存**: 8GB+ (生产环境建议16GB+)
- **存储**: 50GB+ (根据数据量调整)
- **网络**: 稳定的网络连接

### **2. 软件依赖**
- **Python**: 3.8+
- **Node.js**: 16+
- **MySQL**: 8.0+
- **Redis**: 6.0+
- **Nginx**: 1.18+

### **3. 端口要求**
- **80/443**: HTTP/HTTPS 访问
- **8000**: FastAPI 后端服务
- **3000**: 前端开发服务器
- **3306**: MySQL 数据库
- **6379**: Redis 缓存

---

## 🚀 快速部署指南

### **1. 一键部署脚本**

```bash
# 下载部署脚本
git clone https://github.com/diange2026/wangdian-games.git
cd wangdian-games/industrial-partner-management

# 执行部署脚本
chmod +x deploy.sh
./deploy.sh
```

### **2. 手动部署步骤**

#### **步骤1: 安装依赖**

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python
sudo apt install python3 python3-pip python3-venv -y

# 安装 Node.js 和 npm
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install nodejs -y

# 安装 MySQL
sudo apt install mysql-server -y

# 安装 Redis
sudo apt install redis-server -y

# 安装 Nginx
sudo apt install nginx -y
```

#### **步骤2: 数据库配置**

```bash
# 登录 MySQL
sudo mysql

# 创建数据库和用户
CREATE DATABASE industrial_partner_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ipm_user'@'localhost' IDENTIFIED BY 'YourSecurePassword123!';
GRANT ALL PRIVILEGES ON industrial_partner_management.* TO 'ipm_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# 导入数据库结构
mysql -u ipm_user -p industrial_partner_management < database/schema.sql
```

#### **步骤3: 后端服务部署**

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置数据库连接等信息

# 运行数据库迁移
alembic upgrade head

# 启动后端服务
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### **步骤4: 前端部署**

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 构建生产版本
npm run build

# 启动开发服务器（开发环境）
npm run serve

# 或者使用 Nginx 服务生产版本
```

#### **步骤5: Nginx 配置**

创建 `/etc/nginx/sites-available/industrial-partner-management`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/frontend/dist;
    index index.html;

    # 前端静态文件
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 文件上传目录
    location /uploads {
        alias /path/to/uploads;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

启用配置:
```bash
sudo ln -s /etc/nginx/sites-available/industrial-partner-management /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### **步骤6: 配置 HTTPS (可选但推荐)**

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期测试
sudo certbot renew --dry-run
```

---

## 🔧 生产环境高级配置

### **1. 系统服务配置**

创建后端服务文件 `/etc/systemd/system/ipm-backend.service`:

```ini
[Unit]
Description=Industrial Partner Management Backend
After=network.target mysql.service redis.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/industrial-partner-management/backend
Environment="PATH=/opt/industrial-partner-management/backend/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=/opt/industrial-partner-management/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ipm-backend
sudo systemctl start ipm-backend
```

### **2. 数据库备份配置**

创建备份脚本 `/opt/backup/backup-db.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/opt/backup/database"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="industrial_partner_management"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
mysqldump -u ipm_user -p'YourPassword' $DB_NAME > $BACKUP_DIR/${DB_NAME}_${DATE}.sql

# 压缩备份
gzip $BACKUP_DIR/${DB_NAME}_${DATE}.sql

# 保留最近30天的备份
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

添加到 crontab:
```bash
0 2 * * * /opt/backup/backup-db.sh
```

### **3. 监控配置**

安装 Prometheus 和 Grafana:

```bash
# 安装 Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.30.3/prometheus-2.30.3.linux-amd64.tar.gz
tar xvfz prometheus-2.30.3.linux-amd64.tar.gz
cd prometheus-2.30.3.linux-amd64

# 配置 prometheus.yml
# 添加系统和服务监控目标

# 启动 Prometheus
./prometheus --config.file=prometheus.yml
```

### **4. 日志管理**

配置日志轮转 `/etc/logrotate.d/ipm-logs`:

```bash
/opt/industrial-partner-management/backend/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 www-data www-data
}
```

---

## 🐳 Docker 部署

### **1. Docker Compose 配置**

创建 `docker-compose.yml`:

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name: ipm-mysql
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: industrial_partner_management
      MYSQL_USER: ipm_user
      MYSQL_PASSWORD: userpassword
    volumes:
      - mysql_data:/var/lib/mysql
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "3306:3306"
    networks:
      - ipm-network

  redis:
    image: redis:6-alpine
    container_name: ipm-redis
    ports:
      - "6379:6379"
    networks:
      - ipm-network

  backend:
    build: ./backend
    container_name: ipm-backend
    depends_on:
      - mysql
      - redis
    environment:
      DATABASE_URL: mysql+pymysql://ipm_user:userpassword@mysql:3306/industrial_partner_management
      REDIS_URL: redis://redis:6379/0
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - uploads_data:/app/uploads
    networks:
      - ipm-network

  frontend:
    build: ./frontend
    container_name: ipm-frontend
    depends_on:
      - backend
    ports:
      - "3000:80"
    networks:
      - ipm-network

  nginx:
    image: nginx:alpine
    container_name: ipm-nginx
    depends_on:
      - frontend
      - backend
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    networks:
      - ipm-network

volumes:
  mysql_data:
  uploads_data:

networks:
  ipm-network:
    driver: bridge
```

### **2. 构建和启动**

```bash
# 构建所有服务
docker-compose build

# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

---

## 🌐 云平台部署

### **1. 腾讯云部署**

```bash
# 使用 CloudBase CLI
npm install -g @cloudbase/cli

# 初始化项目
tcb init

# 部署后端云函数
tcb functions:deploy --all

# 部署前端静态网站
tcb hosting:deploy frontend/dist -e your-env-id
```

### **2. AWS 部署**

```bash
# 安装 AWS CLI
pip install awscli

# 配置 AWS
aws configure

# 部署到 S3 + CloudFront
aws s3 sync frontend/dist s3://your-bucket-name
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

### **3. 阿里云部署**

```bash
# 使用 OSS
ossutil cp frontend/dist oss://your-bucket-name --recursive

# 配置 CDN
# 在阿里云控制台配置 CDN 加速
```

---

## 🔐 安全配置

### **1. 防火墙配置**

```bash
# 启用防火墙
sudo ufw enable

# 开放必要端口
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 8000/tcp  # 后端 API

# 拒绝其他端口
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

### **2. 数据库安全**

```sql
-- 限制用户权限
REVOKE ALL PRIVILEGES ON *.* FROM 'ipm_user'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON industrial_partner_management.* TO 'ipm_user'@'localhost';

-- 启用 SSL 连接
ALTER USER 'ipm_user'@'localhost' REQUIRE SSL;

-- 定期更改密码
ALTER USER 'ipm_user'@'localhost' IDENTIFIED BY 'NewSecurePassword456!';
```

### **3. API 安全配置**

```python
# 环境变量配置
SECRET_KEY = "your-very-secure-secret-key-change-this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 启用 CORS 白名单
CORS_ALLOW_ORIGINS = [
    "https://your-domain.com",
    "https://admin.your-domain.com"
]

# 启用速率限制
RATE_LIMIT_PER_MINUTE = 60
```

---

## 📊 系统监控和维护

### **1. 健康检查脚本**

创建 `/opt/check-system-health.sh`:

```bash
#!/bin/bash

# 检查服务状态
check_service() {
    service=$1
    if systemctl is-active --quiet $service; then
        echo "✅ $service is running"
    else
        echo "❌ $service is NOT running"
        return 1
    fi
}

# 检查磁盘空间
check_disk() {
    usage=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ $usage -gt 80 ]; then
        echo "⚠️  Disk usage is high: ${usage}%"
        return 1
    else
        echo "✅ Disk usage: ${usage}%"
    fi
}

# 检查内存使用
check_memory() {
    usage=$(free | grep Mem | awk '{print $3/$2 * 100.0}')
    if (( $(echo "$usage > 80" | bc -l) )); then
        echo "⚠️  Memory usage is high: ${usage}%"
        return 1
    else
        echo "✅ Memory usage: ${usage}%"
    fi
}

# 执行所有检查
check_service nginx
check_service ipm-backend
check_service mysql
check_service redis
check_disk
check_memory
```

### **2. 性能监控**

```bash
# 安装性能监控工具
sudo apt install htop iotop nmon -y

# 实时监控
htop              # 系统资源
iotop             # 磁盘 IO
nmon              # 综合性能
```

### **3. 日志监控**

```bash
# 查看实时日志
sudo journalctl -f -u ipm-backend

# 查看错误日志
sudo tail -f /opt/industrial-partner-management/backend/logs/error.log

# 分析访问日志
sudo goaccess /var/log/nginx/access.log --log-format=COMBINED
```

---

## 🔄 更新和升级

### **1. 更新后端**

```bash
cd /opt/industrial-partner-management/backend

# 备份当前版本
git tag backup-$(date +%Y%m%d)
git push origin backup-$(date +%Y%m%d)

# 拉取最新代码
git pull origin main

# 更新依赖
source venv/bin/activate
pip install -r requirements.txt

# 运行数据库迁移
alembic upgrade head

# 重启服务
sudo systemctl restart ipm-backend
```

### **2. 更新前端**

```bash
cd /opt/industrial-partner-management/frontend

# 拉取最新代码
git pull origin main

# 安装依赖
npm install

# 构建
npm run build

# 复制到 Nginx 目录
sudo cp -r dist/* /var/www/html/
```

### **3. 回滚操作**

```bash
# 回滚到指定版本
git checkout v1.2.3

# 回滚数据库
alembic downgrade -1

# 重新启动
sudo systemctl restart ipm-backend
```

---

## 🆘 故障排除

### **常见问题**

#### **1. 数据库连接失败**
```bash
# 检查 MySQL 服务状态
sudo systemctl status mysql

# 检查连接配置
mysql -u ipm_user -p -h localhost -P 3306

# 检查防火墙
sudo ufw status
```

#### **2. 前端无法访问后端 API**
```bash
# 检查网络连接
curl http://localhost:8000/api/health

# 检查 CORS 配置
# 查看后端日志中的 CORS 错误

# 检查 Nginx 配置
sudo nginx -t
```

#### **3. 文件上传失败**
```bash
# 检查权限
sudo chown -R www-data:www-data /opt/industrial-partner-management/backend/uploads

# 检查磁盘空间
df -h

# 检查 Nginx 配置
# 确认 client_max_body_size 设置正确
```

#### **4. 性能问题**
```bash
# 检查慢查询
sudo mysqldumpslow /var/log/mysql/mysql-slow.log

# 检查内存使用
free -h

# 检查进程状态
ps aux --sort=-%mem | head -10
```

### **紧急恢复**

创建紧急恢复脚本 `/opt/recovery.sh`:

```bash
#!/bin/bash

echo "🚨 Starting emergency recovery..."

# 停止所有服务
sudo systemctl stop ipm-backend nginx

# 恢复数据库备份
if [ -f "/opt/backup/database/latest_backup.sql.gz" ]; then
    gunzip -c /opt/backup/database/latest_backup.sql.gz | mysql -u ipm_user -p industrial_partner_management
fi

# 重启服务
sudo systemctl start nginx ipm-backend

echo "✅ Recovery completed"
```

---

## 📞 支持与帮助

### **获取帮助**

1. **查看日志**: 所有日志文件位于 `/opt/industrial-partner-management/logs/`
2. **检查文档**: 详细文档位于 `docs/` 目录
3. **在线支持**: 访问我们的支持页面

### **报告问题**

```bash
# 收集诊断信息
./scripts/diagnostics.sh > diagnostics_$(date +%Y%m%d).txt

# 包含以下信息:
# - 系统日志
# - 应用日志
# - 配置文件 (脱敏后)
# - 错误截图
```

### **社区支持**

- **GitHub Issues**: 提交问题和功能请求
- **Discord**: 加入社区讨论
- **邮件支持**: support@your-domain.com

---

## 🎯 最佳实践

### **1. 安全最佳实践**
- 定期更新系统和软件
- 使用强密码和双因素认证
- 定期备份数据
- 启用安全审计

### **2. 性能优化**
- 使用 CDN 加速静态资源
- 启用数据库查询缓存
- 优化图片和文件大小
- 使用负载均衡

### **3. 数据管理**
- 定期清理过期数据
- 压缩备份文件
- 验证备份完整性
- 制定灾难恢复计划

### **4. 监控告警**
- 设置关键指标告警
- 定期查看系统日志
- 监控用户行为
- 分析系统性能趋势

---

## 🚀 后续步骤

### **1. 系统验收**
1. ✅ 检查所有服务是否正常运行
2. ✅ 测试所有核心功能
3. ✅ 验证数据备份和恢复
4. ✅ 确认安全配置

### **2. 用户培训**
1. 📚 提供用户手册
2. 🎥 创建培训视频
3. 🤝 举办培训会议
4. 📞 建立支持渠道

### **3. 性能优化**
1. 🚀 启用缓存策略
2. 📊 监控系统性能
3. 🔧 定期优化数据库
4. 🌐 配置 CDN 加速

### **4. 持续改进**
1. 🔄 定期更新系统
2. 📈 收集用户反馈
3. 🎯 优化用户体验
4. 🔒 增强安全措施

---

**🎉 恭喜！你的企业级单位资质管理系统已经成功部署！**

现在可以访问 `https://your-domain.com` 开始使用系统。如需进一步帮助，请参考文档或联系支持团队。