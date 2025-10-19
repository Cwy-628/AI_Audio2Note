# 🎵 AI Audio2Note

一个现代化的视频下载与音频提取工具，支持B站和YouTube平台，使用FastAPI后端和Electron前端构建。

## ✨ 特性

- 🎬 支持B站和YouTube视频下载
- 🎵 自动提取音频为MP3格式
- 🖥️ 现代化的Electron桌面应用界面
- ⚡ 高性能FastAPI后端服务
- 📦 支持打包为独立exe文件
- 🔧 支持分P视频下载
- 📱 响应式设计，支持多种屏幕尺寸

## 🏗️ 项目结构

```
AI_audio2note/
├── backend/                 # FastAPI后端
│   ├── main.py             # 主应用文件
│   ├── services/           # 服务层
│   │   ├── audio_downloader.py
│   │   └── process_service.py
│   ├── requirements.txt    # 后端依赖
│   └── build_exe.py        # 后端打包脚本
├── frontend/               # Electron前端
│   ├── main.js            # Electron主进程
│   ├── index.html         # 主页面
│   ├── styles.css         # 样式文件
│   ├── renderer.js        # 渲染进程逻辑
│   ├── package.json       # 前端依赖
│   └── assets/            # 资源文件
├── docs/                  # 文档目录
├── build.py              # 构建脚本
├── start_dev.py          # 开发环境启动脚本
└── requirements.txt      # 项目依赖
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn
- FFmpeg (用于音频处理)

### 安装依赖

1. **安装Python依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **安装前端依赖**
   ```bash
   cd frontend
   npm install
   ```

### 开发环境运行

1. **智能启动（推荐）**
   ```bash
   python start_dev_smart.py
   ```
   自动检查依赖，只在必要时安装，避免重复安装。

2. **快速启动**
   ```bash
   python start_quick.py
   ```
   直接启动服务，不检查依赖（适合依赖已安装的情况）。

3. **原始启动**
   ```bash
   python start_dev.py
   ```
   每次都检查并安装依赖。

4. **手动启动**
   
   启动后端：
   ```bash
   cd backend
   python main.py
   ```
   
   启动前端：
   ```bash
   cd frontend
   npm run dev
   ```

### 生产环境打包

1. **构建整个应用**
   ```bash
   python build.py
   ```

2. **单独构建后端exe**
   ```bash
   cd backend
   python build_exe.py
   ```

3. **单独构建前端应用**
   ```bash
   cd frontend
   npm run build-win
   ```

## 📖 使用说明

### 基本使用

1. 启动应用后，在输入框中粘贴视频链接
2. 可选择指定分P编号（留空则下载所有分P）
3. 点击"开始下载"按钮
4. 等待下载完成，文件将保存到temp目录

### 支持的平台

- **B站 (bilibili.com)**: 支持所有公开视频
- **YouTube (youtube.com)**: 支持所有公开视频

### 功能特性

- **URL验证**: 自动验证链接格式和平台支持
- **分P下载**: 支持多P视频的指定分P下载
- **进度显示**: 实时显示下载进度
- **历史记录**: 自动保存下载历史，支持快速重新下载
- **错误处理**: 完善的错误提示和处理机制

## 🔧 技术栈

### 后端
- **FastAPI**: 现代、快速的Web框架
- **uvicorn**: ASGI服务器
- **yt-dlp**: 视频下载库
- **Pydantic**: 数据验证

### 前端
- **Electron**: 跨平台桌面应用框架
- **HTML5/CSS3**: 现代化界面
- **JavaScript ES6+**: 现代JavaScript特性
- **Axios**: HTTP客户端

## 📦 打包说明

### 后端打包
使用PyInstaller将Python后端打包为exe文件：
```bash
cd backend
python build_exe.py
```

### 前端打包
使用electron-builder打包Electron应用：
```bash
cd frontend
npm run build-win
```

### 完整应用打包
使用构建脚本打包整个应用：
```bash
python build.py
```

## 🛠️ 开发指南

### 添加新的视频平台

1. 在`backend/services/audio_downloader.py`中添加新的域名到`supported_domains`列表
2. 测试新平台的URL验证和下载功能

### 修改前端界面

1. 编辑`frontend/index.html`修改页面结构
2. 编辑`frontend/styles.css`修改样式
3. 编辑`frontend/renderer.js`修改交互逻辑

### 添加新的API接口

1. 在`backend/main.py`中添加新的路由
2. 在`frontend/renderer.js`中添加对应的API调用
3. 更新前端界面以支持新功能

## 🐛 故障排除

### 常见问题

1. **后端启动失败**
   - 检查Python版本是否为3.8+
   - 确认所有依赖已正确安装
   - 检查端口8000是否被占用

2. **前端启动失败**
   - 检查Node.js版本是否为16+
   - 确认npm依赖已正确安装
   - 检查后端服务是否正在运行

3. **视频下载失败**
   - 确认网络连接正常
   - 检查FFmpeg是否正确安装
   - 验证视频链接是否有效

4. **打包失败**
   - 确认所有依赖已安装
   - 检查PyInstaller和electron-builder是否正确安装
   - 查看错误日志获取详细信息

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 支持

如有问题，请提交Issue或联系开发团队。
