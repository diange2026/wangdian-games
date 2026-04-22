# 🚀 工贸企业相关方全流程管理系统 - 部署指南

## 📊 **部署方案对比**

| 方案 | 费用 | 访问速度 | 技术要求 | 适合场景 |
|------|------|----------|----------|----------|
| **腾讯云 COS** | ¥0.5-2/月 | 国内极快 | 简单 | 正式部署、国内用户 |
| **GitHub Pages** | 免费 | 全球中等 | 中等 | 演示、开源项目 |
| **本地运行** | 免费 | 极快 | 较高 | 开发测试 |

---

## 📦 **方案一：腾讯云 COS 部署（推荐）**

### **步骤 1：准备腾讯云资源**

1. **注册腾讯云账号**
   - 访问 https://cloud.tencent.com
   - 完成实名认证

2. **创建 COS 存储桶**
   ```bash
   存储桶名称: industrial-partner-management-你的名字
   所属地域: 北京/上海/广州
   访问权限: 公有读私有写
   静态网站: 开启
   ```

3. **获取访问信息**
   ```
   存储桶域名: industrial-partner-management-你的名字.cos.ap-beijing.myqcloud.com
   ```

### **步骤 2：上传系统文件**

#### **方法 A：使用 COS Browser（图形化）**
1. 下载 COS Browser：https://www.tencentcloud.com/document/product/436/11366
2. 配置访问密钥
3. 上传文件夹结构：
   ```
   deploy-for-web/
   ├── index.html          ← 上传到根目录
   ├── css/
   ├── js/
   └── api/
   ```

#### **方法 B：使用命令行**
```bash
# 安装 COS CLI
pip install coscmd

# 配置
coscmd config -a AKIDxxxxxxxxxx -s SKxxxxxxxxxxxx -b industrial-partner-management-你的名字 -r ap-beijing

# 上传整个目录
coscmd upload -r ./deploy-for-web/ /
```

### **步骤 3：访问系统**

**访问链接：**
```
https://industrial-partner-management-你的名字.cos.ap-beijing.myqcloud.com/index.html
```

### **步骤 4：可选优化**

#### **配置 CDN 加速**
1. 在 CDN 控制台添加域名
2. 源站选择 COS 存储桶
3. 配置 HTTPS 证书

#### **自定义域名**
```
https://partner.yourcompany.com
```

### **费用估算**
| 项目 | 用量 | 费用 |
|------|------|------|
| COS 存储 | 1GB | ¥0.12/月 |
| 流量 | 10GB | ¥0.5/月 |
| 请求数 | 100万次 | ¥0.2/月 |
| **总计** | - | **¥0.82/月** |

---

## 🔗 **方案二：GitHub Pages 部署**

### **步骤 1：准备 GitHub 仓库**

1. **创建新仓库**
   ```bash
   仓库名: industrial-partner-management
   权限: Public
   初始化: 不要添加文件
   ```

2. **上传代码**
   ```bash
   # 克隆仓库
   git clone https://github.com/你的用户名/industrial-partner-management.git
   
   # 复制文件
   cp -r ./deploy-for-web/* industrial-partner-management/
   
   # 提交
   cd industrial-partner-management
   git add .
   git commit -m "工贸企业相关方全流程管理系统"
   git push -u origin main
   ```

### **步骤 2：开启 GitHub Pages**

1. 进入仓库 → Settings → Pages
2. 配置：
   ```
   Source: Deploy from a branch
   Branch: main
   Folder: /
   ```

3. **等待部署完成**（约 1-3 分钟）

### **步骤 3：访问系统**

**访问链接：**
```
https://你的用户名.github.io/industrial-partner-management/
```

### **步骤 4：可选优化**

#### **自定义域名**
1. 在 GitHub Pages 设置中添加域名
2. 在域名服务商添加 CNAME 记录

#### **HTTPS 强制**
- GitHub Pages 自动提供 HTTPS

### **优势**
- ✅ 完全免费
- ✅ 自动 HTTPS
- ✅ 支持自定义域名
- ✅ 版本控制历史

---

## 🖥️ **方案三：本地部署（开发测试）**

### **步骤 1：下载完整系统包**

#### **下载链接：**
```
https://raw.githubusercontent.com/diange2026/wangdian-games/main/workspace/industrial-partner-management/
```

#### **文件清单：**
1. `backend/` - 完整后端代码
2. `frontend/` - 前端源码
3. `docs/` - 设计文档
4. `scripts/` - 数据库脚本
5. `demo-frontend/` - 演示界面

### **步骤 2：本地运行**

#### **方法 A：使用 Python HTTP 服务器**
```bash
# 进入演示目录
cd deploy-for-web

# 启动服务器
python -m http.server 8000

# 访问
http://localhost:8000
```

#### **方法 B：完整系统运行**
```bash
# 1. 安装依赖
cd backend
pip install -r requirements.txt

# 2. 启动后端
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 3. 启动前端
cd ../frontend
npm install
npm run dev

# 4. 访问
# API文档: http://localhost:8000/docs
# 前端界面: http://localhost:3000
```

---

## 📱 **移动端访问**

### **扫码访问**
1. 获取部署链接
2. 使用二维码生成器
3. 手机扫码直接访问

### **响应式设计**
- ✅ 手机适配
- ✅ 平板适配
- ✅ PC 桌面适配

---

## 🔧 **系统功能验证**

### **验证步骤：**
1. **访问首页** - 确认界面正常加载
2. **功能测试** - 点击所有按钮
3. **数据录入** - 测试表单提交
4. **API 调用** - 测试后端接口

### **测试用例：**
```javascript
// 1. 访问系统
// 预期：页面正常加载，所有组件显示

// 2. 点击"单位管理"
// 预期：显示单位列表，可操作按钮

// 3. 点击"添加新单位"
// 预期：弹出对话框，可输入信息

// 4. 提交表单
// 预期：提示成功信息，数据更新
```

---

## 🛠️ **问题排查**

### **常见问题：**

#### **问题 1：无法访问链接**
**解决方案：**
1. 检查网络连接
2. 确认防火墙设置
3. 验证链接正确性

#### **问题 2：页面显示异常**
**解决方案：**
1. 清除浏览器缓存
2. 检查浏览器兼容性
3. 验证文件完整性

#### **问题 3：API 调用失败**
**解决方案：**
1. 检查 CORS 配置
2. 验证网络策略
3. 测试 API 接口

### **调试工具：**
1. **浏览器开发者工具**（F12）
2. **网络请求查看器**
3. **JavaScript 控制台**

---

## 📈 **系统扩展**

### **后续开发方向：**
1. **手续文档管理模块**
2. **审批流程系统**
3. **移动端应用**
4. **数据导入导出**

### **性能优化：**
1. **CDN 加速**
2. **数据库索引优化**
3. **前端代码压缩**
4. **缓存策略**

---

## 📞 **技术支持**

### **获取帮助：**
1. **部署问题** - 参考本指南
2. **功能问题** - 查看系统文档
3. **技术问题** - 查看源代码

### **联系信息：**
- **GitHub**: diange2026
- **项目仓库**: https://github.com/diange2026/wangdian-games

---

## 🎉 **部署成功标志**

✅ **系统可正常访问**  
✅ **所有功能按钮可点击**  
✅ **数据录入正常**  
✅ **API 接口响应正常**  
✅ **移动端适配正常**

**恭喜！系统已成功部署并可以正常使用！** 🚀