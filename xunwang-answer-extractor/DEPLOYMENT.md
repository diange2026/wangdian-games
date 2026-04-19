# 讯网答案提取器插件部署指南

## 📦 打包准备

### 1. 版本更新
在打包前，请确保：
- 更新 `manifest.json` 中的版本号
- 更新 `README.md` 中的版本信息
- 检查所有依赖项

### 2. 文件结构检查
确保以下文件存在且正确：

```
必需文件：
- manifest.json
- background.js
- content.js
- popup/popup.html
- popup/popup.js
- popup/popup.css
- options/options.html
- options/options.js
- options/options.css
- icons/icon16.png
- icons/icon48.png
- icons/icon128.png

可选文件：
- README.md
- DEPLOYMENT.md
- LICENSE
```

### 3. 图标准备
需要准备三种尺寸的图标：
- **16x16** - 工具栏图标
- **48x48** - 扩展管理页面图标
- **128x128** - Chrome应用商店图标

图标要求：
- PNG格式
- 透明背景
- 清晰可识别
- 品牌一致性

## 🛠️ 本地打包

### 方法一：手动打包
1. 创建打包目录
   ```bash
   mkdir xunwang-extractor-v1.0.0
   ```

2. 复制必要文件
   ```bash
   cp -r manifest.json *.js popup/ options/ icons/ xunwang-extractor-v1.0.0/
   ```

3. 创建ZIP文件
   ```bash
   zip -r xunwang-extractor-v1.0.0.zip xunwang-extractor-v1.0.0/
   ```

### 方法二：使用构建脚本
创建 `build.js` 脚本：

```javascript
const fs = require('fs');
const path = require('path');
const archiver = require('archiver');

const version = '1.0.0';
const packageName = `xunwang-extractor-v${version}`;
const output = fs.createWriteStream(`${packageName}.zip`);
const archive = archiver('zip', { zlib: { level: 9 } });

// 需要包含的文件和目录
const filesToInclude = [
  'manifest.json',
  'background.js',
  'content.js',
  'popup/',
  'options/',
  'icons/'
];

output.on('close', () => {
  console.log(`打包完成: ${packageName}.zip (${archive.pointer()} bytes)`);
});

archive.on('error', (err) => {
  throw err;
});

archive.pipe(output);

filesToInclude.forEach(file => {
  const stat = fs.statSync(file);
  if (stat.isDirectory()) {
    archive.directory(file, file);
  } else {
    archive.file(file, { name: file });
  }
});

archive.finalize();
```

运行构建脚本：
```bash
node build.js
```

## 🚀 发布到Chrome应用商店

### 1. 开发者账户注册
1. 访问 [Chrome Web Store 开发者控制台](https://chrome.google.com/webstore/devconsole)
2. 使用Google账户登录
3. 支付一次性开发者注册费（$5）

### 2. 准备发布材料

#### 应用商店列表内容
- **标题**: 讯网题目答案提取器
- **简短描述**: 专为讯网教学云平台设计的答案提取工具
- **详细描述**: 提供完整功能描述、使用场景、特色功能等
- **类别**: 生产力工具 > 教育
- **语言**: 简体中文

#### 截图要求
- 尺寸: 1280x800 或 640x400
- 格式: PNG或JPEG
- 最少3张，最多5张
- 展示核心功能

#### 宣传图片
- 小图标: 440x280
- 大图标: 920x680
- 主图: 2560x1280

### 3. 提交审核
1. 上传ZIP包
2. 填写所有必需信息
3. 设置隐私政策链接
4. 选择发布范围（测试/公开）
5. 提交审核

### 审核时间
- 通常需要1-3个工作日
- 审核通过后自动发布

## 🔐 隐私政策要求

Chrome应用商店要求提供隐私政策，特别是：
- 数据收集说明
- 数据使用方式
- 用户权利
- 联系方式

示例隐私政策页面：
```html
<!DOCTYPE html>
<html>
<head>
    <title>隐私政策 - 讯网答案提取器</title>
</head>
<body>
    <h1>隐私政策</h1>
    <p>我们尊重并保护您的隐私...</p>
    <!-- 详细隐私政策内容 -->
</body>
</html>
```

## 📊 发布后监控

### 1. 用户反馈
- 定期查看应用商店评论
- 收集用户反馈
- 及时回复用户问题

### 2. 使用统计
- 通过Google Analytics跟踪使用情况
- 分析用户行为
- 识别问题区域

### 3. 崩溃报告
- 集成错误监控
- 自动收集崩溃信息
- 及时修复问题

## 🔄 版本更新流程

### 1. 开发新版本
```bash
# 更新版本号
npm version patch  # 或 minor, major

# 测试新功能
# 修复bug
```

### 2. 更新发布材料
- 更新截图
- 更新描述
- 更新变更日志

### 3. 提交更新
- 打包新版本
- 上传到开发者控制台
- 提交审核

## ⚠️ 常见问题

### Q: 审核被拒绝怎么办？
**常见原因：**
1. 权限过多或不合理
2. 隐私政策不完整
3. 功能描述不清晰
4. 违反平台政策

**解决方案：**
1. 查看审核反馈
2. 修改对应问题
3. 重新提交

### Q: 如何推广插件？
**推广渠道：**
1. 教育相关论坛
2. 社交媒体
3. SEO优化
4. 合作伙伴推广

### Q: 如何收集用户反馈？
**反馈渠道：**
1. 应用商店评论
2. 插件内置反馈表单
3. 技术支持邮箱
4. 用户调查

## 📈 商业化策略

### 1. 免费增值模式
- 基础功能免费
- 高级功能付费
- 试用期优惠

### 2. 定价策略
- 月度订阅: ¥19.9/月
- 年度订阅: ¥199/年（节省16%）
- 团队套餐: ¥99.9/月/5用户

### 3. 支付集成
- 使用Stripe或支付宝接口
- 支持多种支付方式
- 自动续费管理

## 🛡️ 安全考虑

### 1. 代码安全
- 代码混淆（可选）
- 敏感信息加密
- 防止逆向工程

### 2. 用户数据安全
- 本地数据加密
- 安全传输协议
- 定期安全审计

### 3. 合规性
- 遵守GDPR
- 遵守CCPA
- 遵守中国网络安全法

## 🌐 国际化

### 支持语言
- 简体中文（主要）
- 英语（未来计划）
- 其他语言（按需求添加）

### 国际化文件结构
```
locales/
  ├── zh_CN/
  │   └── messages.json
  └── en/
      └── messages.json
```

## 📝 变更日志模板

```markdown
## [版本号] - 发布日期

### 新增功能
- 功能1描述
- 功能2描述

### 功能改进
- 改进1描述
- 改进2描述

### Bug修复
- 修复问题1
- 修复问题2

### 已知问题
- 问题1描述
- 问题2描述
```

---

**最后更新：2026-04-19**
**版本：1.0.0**
**部署指南版本：1.0**