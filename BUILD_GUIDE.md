# 🏗️ AI Audio2Note 构建指南

本指南将帮助您构建跨平台的AI Audio2Note分发包，让没有代码基础的用户也能开箱即用。

## 📋 构建要求

### 系统要求
- **Python 3.8+**
- **Node.js 16+**
- **FFmpeg** (用户端需要)

### 开发环境
- **Windows**: Visual Studio Build Tools
- **macOS**: Xcode Command Line Tools
- **Linux**: build-essential

## 🚀 快速构建

### 一键构建所有平台

```bash
python build_all.py
```

这个脚本会自动：
1. 检查构建依赖
2. 构建后端可执行文件
3. 构建Electron桌面应用
4. 创建分发包

### 手动构建步骤

#### 1. 安装依赖

```bash
# 安装Python依赖
pip install -r requirements.txt
pip install pyinstaller

# 安装Node.js依赖
cd frontend
npm install
```

#### 2. 构建后端

**Windows:**
```bash
cd backend
python build_exe.py
```

**macOS:**
```bash
cd backend
pyinstaller --onefile --name ai-audio2note-backend main.py
```

#### 3. 构建Electron应用

```bash
cd frontend

# Windows
npm run build:win

# macOS
npm run build:mac

# Linux
npm run build:linux
```

## 📦 分发包结构

构建完成后，会在`dist/`目录下生成分发包：

### Windows分发包
```
AI_Audio2Note_Windows/
├── ai-audio2note-backend.exe    # 后端服务
├── AI_Audio2Note/               # Electron应用
├── 启动AI_Audio2Note.bat        # 启动脚本
└── 使用说明.txt                 # 用户说明
```

### macOS分发包
```
AI_Audio2Note_Mac/
├── ai-audio2note-backend        # 后端服务
├── AI_Audio2Note.app/           # Electron应用
├── 启动AI_Audio2Note.command    # 启动脚本
└── 使用说明.txt                 # 用户说明
```

## 🎯 用户使用指南

### Windows用户

1. **下载分发包**：解压`AI_Audio2Note_Windows.zip`
2. **安装FFmpeg**：
   ```bash
   # 使用Chocolatey
   choco install ffmpeg
   
   # 或下载安装包
   # https://ffmpeg.org/download.html
   ```
3. **启动应用**：双击`启动AI_Audio2Note.bat`

### macOS用户

1. **下载分发包**：解压`AI_Audio2Note_Mac.zip`
2. **安装FFmpeg**：
   ```bash
   brew install ffmpeg
   ```
3. **启动应用**：双击`启动AI_Audio2Note.command`

## 🔧 高级配置

### 自定义图标

将图标文件放在`frontend/assets/`目录：
- `icon.ico` - Windows图标
- `icon.icns` - macOS图标
- `icon.png` - Linux图标

### 修改应用信息

编辑`frontend/package.json`：
```json
{
  "name": "ai-audio2note-frontend",
  "version": "1.0.0",
  "description": "AI Audio2Note - 视频音频提取工具",
  "author": "Your Name",
  "license": "MIT"
}
```

### 添加代码签名

**Windows:**
```json
"win": {
  "certificateFile": "path/to/certificate.p12",
  "certificatePassword": "password"
}
```

**macOS:**
```json
"mac": {
  "identity": "Developer ID Application: Your Name"
}
```

## 🐛 故障排除

### 常见问题

1. **PyInstaller构建失败**
   - 确保所有依赖已安装
   - 检查Python版本兼容性
   - 清理构建缓存：`rm -rf build/ dist/`

2. **Electron构建失败**
   - 确保Node.js版本正确
   - 清理node_modules：`rm -rf node_modules && npm install`
   - 检查网络连接

3. **FFmpeg未找到**
   - 确保FFmpeg在PATH中
   - 重启终端/命令提示符
   - 检查安装路径

### 调试模式

启用详细日志：
```bash
DEBUG=1 python build_all.py
```

## 📝 发布清单

发布前请检查：

- [ ] 所有平台构建成功
- [ ] 分发包包含所有必要文件
- [ ] 启动脚本工作正常
- [ ] 用户说明文档完整
- [ ] 图标和元数据正确
- [ ] 代码签名（如需要）

## 🎉 发布

构建完成后，分发包位于`dist/`目录：

```
dist/
├── AI_Audio2Note_Windows/    # Windows分发包
└── AI_Audio2Note_Mac/        # macOS分发包
```

将这些文件夹压缩为ZIP文件，即可分发给用户使用！

---

**构建成功！** 🎉 用户现在可以开箱即用地使用AI Audio2Note了！