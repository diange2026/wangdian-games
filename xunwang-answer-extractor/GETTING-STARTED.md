# 讯网答案提取器插件 - 快速开始指南

## 🚀 快速体验

### 1. 立即测试插件

如果你已经安装了ImageMagick，可以运行打包脚本：

```bash
cd /root/.openclaw/workspace/xunwang-answer-extractor
./package.sh
```

如果还没有ImageMagick，可以手动测试：

```bash
# 打开Chrome浏览器
# 访问: chrome://extensions/
# 打开"开发者模式"
# 点击"加载已解压的扩展程序"
# 选择: /root/.openclaw/workspace/xunwang-answer-extractor
```

### 2. 测试步骤

1. **安装插件**
   - 按照上述步骤加载插件
   - 确认插件已激活

2. **访问讯网平台**
   ```
   网址: https://www.whxunw.com/exam/login.thtml
   账号: 014325210588
   密码: 6W7EjZ>M
   ```

3. **测试功能**
   - 登录后导航到答案页面
   - 点击插件图标
   - 测试"一键提取答案"
   - 测试导出功能

## 📁 项目文件结构

```
xunwang-answer-extractor/
├── manifest.json          # 插件配置文件 (必需)
├── background.js         # 后台服务脚本 (必需)
├── content.js           # 核心提取脚本 (必需)
├── utils.js             # 工具函数库 (必需)
├── popup/               # 弹出窗口界面
│   ├── popup.html      # 主界面HTML
│   ├── popup.css       # 样式文件
│   └── popup.js        # 交互逻辑
├── options/            # 设置页面
│   ├── options.html   # 设置界面HTML
│   ├── options.css    # 设置样式
│   └── options.js     # 设置逻辑
├── icons/             # 图标目录
│   ├── icon16.png    # 16x16图标 (必需)
│   ├── icon48.png    # 48x48图标 (必需)
│   └── icon128.png   # 128x128图标 (必需)
├── package.sh         # 打包脚本
└── 各种说明文档
```

## 🛠️ 开发环境设置

### 必需工具
1. **Chrome浏览器** (88+版本)
2. **文本编辑器** (推荐VS Code)
3. **基本命令行工具**

### 可选工具
1. **Git** - 版本控制
2. **ImageMagick** - 图标处理
3. **npm** - 包管理（用于xlsx.js）

## 🔧 插件开发流程

### 1. 代码修改
```bash
# 编辑文件
code content.js        # 修改提取逻辑
code popup/popup.js    # 修改界面交互
code background.js     # 修改后台服务
```

### 2. 测试修改
```bash
# 在Chrome中重新加载插件
1. 打开 chrome://extensions/
2. 找到"讯网答案提取器"
3. 点击刷新按钮 🔄
4. 测试新功能
```

### 3. 打包发布
```bash
# 使用打包脚本
./package.sh 1.1.0

# 或手动打包
zip -r xunwang-extractor-v1.1.0.zip *
```

## 🎨 图标要求

### 必需文件
1. **icon16.png** - 16x16像素，浏览器工具栏图标
2. **icon48.png** - 48x48像素，扩展管理页面图标
3. **icon128.png** - 128x128像素，应用商店图标

### 设计建议
- 主题色：蓝色 (#4a6ee0) + 紫色渐变
- 元素：书本📚 + 放大镜🔍
- 风格：现代扁平化设计

### 临时图标方案
1. 下载开源图标作为占位
2. 使用字母组合（如"XW"）
3. 单色简单图标

## 📋 功能测试清单

### 核心功能
- [ ] 插件安装成功
- [ ] 弹出窗口正常显示
- [ ] 设置页面正常显示
- [ ] 页面类型识别正确
- [ ] 答案提取功能正常
- [ ] 数据导出功能正常

### 用户体验
- [ ] 界面响应流畅
- [ ] 错误提示清晰
- [ ] 进度反馈及时
- [ ] 主题切换正常

### 数据管理
- [ ] 本地存储正常
- [ ] 数据导出完整
- [ ] 历史记录保存
- [ ] 备份恢复功能

## ⚡ 快速开发技巧

### 1. 调试技巧
```javascript
// Content Script 调试
console.log('提取结果:', data);

// Popup 调试
// 右键点击插件图标 → "审查弹出内容"

// Background 调试
// 扩展管理页面 → "service worker"
```

### 2. 常用命令
```bash
# 重新加载插件
# chrome://extensions/ → 点击刷新按钮

# 查看插件日志
# 按F12打开开发者工具 → Console面板

# 清除插件数据
chrome.storage.local.clear()
```

### 3. 快速测试
```html
<!-- 测试页面 -->
<!DOCTYPE html>
<html>
<body>
    <div class="question-item">题目1: 什么是AI？答案: 人工智能</div>
    <div class="question-item">题目2: 1+1=? 答案: 2</div>
</body>
</html>
```

## 🔍 常见问题解决

### Q: 插件无法安装
**解决方案：**
1. 确保使用Chrome 88+版本
2. 打开"开发者模式"
3. 选择正确的目录

### Q: 无法提取答案
**解决方案：**
1. 确认在正确的页面（答案详情页）
2. 检查网络连接
3. 刷新页面重试

### Q: 导出文件打不开
**解决方案：**
1. 确认文件格式正确
2. 使用正确软件打开
3. 检查文件完整性

### Q: 图标不显示
**解决方案：**
1. 确认PNG格式
2. 确认正确尺寸
3. 重新加载插件

## 🚀 下一步行动

### 短期目标
1. **设计专业图标**
   - 制作16x16, 48x48, 128x128 PNG图标

2. **集成Excel导出**
   - 安装xlsx.js库
   - 实现美化导出功能

3. **完善自动登录**
   - 安全存储账号密码
   - 自动登录逻辑

### 中期目标
1. **发布到应用商店**
   - 准备宣传材料
   - 提交审核
   - 发布推广

2. **用户反馈收集**
   - 建立反馈渠道
   - 收集改进建议
   - 迭代优化

### 长期目标
1. **商业化实现**
   - 付费功能开发
   - 支付系统集成
   - 客户支持体系

2. **产品扩展**
   - 多平台支持
   - 功能丰富
   - 生态系统建设

## 📞 支持与资源

### 文档资源
- [设计文档](xunwang-answer-extractor-design.md) - 完整功能设计
- [部署指南](DEPLOYMENT.md) - 发布和推广指南
- [使用说明](README.md) - 用户使用手册

### 开发资源
- [Chrome扩展API文档](https://developer.chrome.com/docs/extensions/)
- [Manifest V3指南](https://developer.chrome.com/docs/extensions/mv3/intro/)
- [示例项目](https://github.com/GoogleChrome/chrome-extensions-samples)

### 图标资源
- [Flaticon](https://www.flaticon.com/) - 免费图标库
- [Icons8](https://icons8.com/) - 高质量图标
- [FontAwesome](https://fontawesome.com/) - 矢量图标库

## 🎯 成功指标

### 技术指标
- [ ] 插件稳定运行无崩溃
- [ ] 数据提取准确率 >95%
- [ ] 用户界面响应时间 <100ms

### 用户指标
- [ ] 安装用户 >1000人
- [ ] 活跃用户 >200人
- [ ] 用户满意度 >4.5/5

### 商业指标
- [ ] 付费用户转化率 >5%
- [ ] 月度收入 >5000元
- [ ] 用户留存率 >60%

---

**开始行动吧！**
1. 立即测试插件功能
2. 设计或获取专业图标
3. 开始收集用户反馈
4. 准备发布计划

**成功的第一步是从现在开始！** 🚀