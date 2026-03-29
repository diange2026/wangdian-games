# Unity Hub + Unity 编辑器安装指南

## 📋 系统要求

- **操作系统**: Ubuntu 20.04+ / Windows 10+ / macOS 10.13+
- **CPU**: SSE2 指令集支持
- **内存**: 至少 8GB RAM
- **磁盘**: 至少 30GB 可用空间
- **显卡**: 支持 DirectX 10 / OpenGL 3.3+

---

## 🚀 安装步骤

### 方法 1: Ubuntu/Debian Linux

#### 1. 添加 Unity Hub 官方仓库

```bash
# 添加 Unity GPG 密钥
wget -qO - https://hub.unity3d.com/linux/keys/public | sudo apt-key add -

# 添加仓库
echo "deb https://hub.unity3d.com/linux/repos/deb stable main" | sudo tee /etc/apt/sources.list.d/unityhub.list

# 更新并安装
sudo apt update
sudo apt install unityhub
```

#### 2. 启动 Unity Hub

```bash
unityhub
```

#### 3. 激活许可证

- 首次启动需要登录 Unity 账号
- 可选择 Personal（免费）或 Professional 许可证

#### 4. 安装 Unity 编辑器

- 打开 Unity Hub → Installs → Install Editor
- 推荐版本：**2022.3.15f1 LTS**
- 选择模块：
  - ✅ Unity Hub
  - ✅ Documentation
  - ✅ Android Build Support (可选)
  - ✅ iOS Build Support (可选)
  - ✅ Linux Build Support (可选)

---

### 方法 2: Windows

#### 1. 下载安装程序

访问：https://unity.com/download

#### 2. 运行安装程序

- 下载 `UnityHubSetup.exe`
- 双击运行，按提示安装

#### 3. 安装 Unity 编辑器

- 打开 Unity Hub → Installs → Install Editor
- 选择版本和模块

---

### 方法 3: macOS

#### 1. 下载安装程序

访问：https://unity.com/download

#### 2. 安装

- 下载 `UnityHub.dmg`
- 拖拽到 Applications 文件夹

---

## 🎮 创建 GrabGoose 项目

### 1. 启动 Unity Hub

```bash
unityhub
```

### 2. 新建项目

- 点击 **Projects** → **New project**
- 选择模板：**3D Core**
- 项目名称：`GrabGoose`
- 安装位置：`/home/user/Projects/GrabGoose`
- 点击 **Create project**

### 3. 等待导入完成

- 首次打开需要 5-10 分钟导入资源

---

## 🔌 安装 TomLeeLive 插件

### 方法 1: 通过 Package Manager（推荐）

1. 打开 Unity 编辑器
2. 菜单栏：**Window** → **Package Manager**
3. 点击 **+** 按钮 → **Add package from git URL**
4. 输入：
   ```
   https://github.com/TomLeeLive/openclaw-unity-plugin.git
   ```
5. 点击 **Add**
6. 等待安装完成

### 方法 2: 手动安装

```bash
cd /tmp
git clone https://github.com/TomLeeLive/openclaw-unity-plugin.git
cp -r openclaw-unity-plugin /path/to/GrabGoose/Assets/Plugins/
```

---

## ✅ 验证安装

### 1. 检查 Unity 版本

```bash
unityhub --version
```

### 2. 检查项目结构

```
GrabGoose/
├── Assets/
│   ├── Plugins/
│   │   └── openclaw-unity-plugin/
│   ├── Scenes/
│   │   └── SampleScene.unity
│   └── Scripts/
├── Packages/
├── ProjectSettings/
└── UnityPackageManager/
```

### 3. 在 Unity 中验证

- 打开 Unity 编辑器
- 查看 **Package Manager** 中是否显示 `openclaw-unity-plugin`
- 检查 **Console** 是否有错误

---

## 🛠️ 常见问题

### Q1: Unity Hub 无法启动（Linux）

**解决方案**：
```bash
# 安装依赖
sudo apt install libfuse2 libxcb-xtest0

# 使用包装脚本
/opt/unityhub/unityhub --no-sandbox
```

### Q2: Git URL 无法添加

**解决方案**：
```bash
# 检查 Git 是否安装
git --version

# 如果没有，安装 Git
sudo apt install git

# 重试添加
```

### Q3: 许可证激活失败

**解决方案**：
- 检查网络连接
- 登录 Unity 账号：https://id.unity.com
- 重新激活许可证

---

## 📞 技术支持

- Unity 官方文档：https://docs.unity3d.com
- Unity 论坛：https://forum.unity.com
- TomLeeLive 插件：https://github.com/TomLeeLive/openclaw-unity-plugin

---

## 🎯 下一步

1. ✅ 安装 Unity Hub
2. ✅ 安装 Unity 编辑器 2022.3.15f1 LTS
3. ✅ 创建 GrabGoose 项目
4. ✅ 安装 TomLeeLive 插件
5. 🎮 开始开发《抓抓抓 3D》游戏！

---

_最后更新：2026-03-29_
