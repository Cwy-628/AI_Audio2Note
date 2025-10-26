# 🎵 AI Audio2Note

一个强大的视频音频提取工具，支持从B站和YouTube下载视频并提取音频。

## ✨ 功能特点

- 🎬 **多平台支持**：支持B站(bilibili.com)和YouTube视频下载
- 🎵 **音频提取**：自动提取视频中的音频并转换为MP3格式
- 📁 **原生文件夹选择**：使用系统原生文件夹选择器选择下载路径
- 🖥️ **跨平台桌面应用**：基于Electron的现代化桌面应用
- ⚡ **快速下载**：优化的下载引擎，支持大文件下载
- 📱 **现代化界面**：简洁美观的用户界面

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- FFmpeg

### 安装依赖

1. **安装Python依赖**
```bash
pip install -r requirements.txt
```

2. **安装Node.js依赖**
```bash
cd frontend
npm install
```

3. **安装FFmpeg**
```bash
# macOS (使用Homebrew)
brew install ffmpeg

# Windows (使用Chocolatey)
choco install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install ffmpeg
```

### 启动应用

```bash
python start_native.py
```

应用将自动启动后端服务和Electron桌面应用。

## 📖 使用指南

### 基本使用

1. **输入视频链接**：在输入框中粘贴B站或YouTube视频链接
2. **选择下载路径**：点击"选择下载文件夹"按钮，使用系统原生文件夹选择器
3. **开始下载**：点击"开始下载"按钮开始下载和音频提取
4. **查看结果**：下载完成后，音频文件将保存在指定文件夹中

### 支持的链接格式

**B站链接**：
- `https://www.bilibili.com/video/BV1xxxxx`
- `https://www.bilibili.com/bangumi/play/xxxxx`
- 支持带参数的链接（自动清理跟踪参数）

**YouTube链接**：
- `https://www.youtube.com/watch?v=xxxxx`
- `https://youtu.be/xxxxx`
- `https://www.youtube.com/shorts/xxxxx`
- 支持移动端和嵌入链接

### 高级功能

- **分P下载**：对于B站多P视频，可以指定下载特定分P
- **下载历史**：自动保存下载历史，方便重复下载
- **进度显示**：实时显示下载进度
- **错误处理**：智能错误提示和重试机制

## 🏗️ 项目结构

```
AI_Audio2Note/
├── backend/                 # 后端服务
│   ├── main.py             # FastAPI主服务
│   ├── services/           # 核心服务模块
│   │   ├── audio_downloader.py    # 音频下载器
│   │   └── process_service.py     # 处理服务
│   ├── build_exe.py        # Windows打包脚本
│   └── requirements.txt    # Python依赖
├── frontend/               # 前端应用
│   ├── main.js            # Electron主进程
│   ├── renderer.js        # 渲染进程
│   ├── index.html         # 主页面
│   ├── styles.css         # 样式文件
│   ├── package.json       # Node.js依赖
│   └── node_modules/      # 依赖包
├── start_native.py        # 启动脚本
├── requirements.txt       # 项目依赖
└── README.md             # 项目说明
```

## 🔧 开发说明

### 后端技术栈

- **FastAPI**：现代化的Python Web框架
- **yt-dlp**：强大的视频下载工具
- **FFmpeg**：音视频处理工具

### 前端技术栈

- **Electron**：跨平台桌面应用框架
- **原生HTML/CSS/JavaScript**：轻量级前端
- **系统API**：原生文件夹选择器

### 核心功能实现

1. **视频下载**：使用yt-dlp处理各种视频平台
2. **音频提取**：FFmpeg转换音频格式
3. **文件管理**：智能文件命名和目录管理
4. **用户界面**：响应式设计，支持原生系统功能

## 📦 打包发布

### 快速构建分发包

为没有代码基础的用户创建开箱即用的分发包：

```bash
# 一键构建所有平台
python build_all.py

# 或使用快速构建
python build_quick.py
```

### 构建要求

- **Python 3.8+**
- **Node.js 16+**
- **FFmpeg** (用户端需要)

### 分发包结构

构建完成后，会在`dist/`目录生成分发包：

**Windows分发包**：
```
AI_Audio2Note_Windows/
├── ai-audio2note-backend.exe    # 后端服务
├── AI_Audio2Note/               # Electron应用
├── 启动AI_Audio2Note.bat        # 启动脚本
└── 使用说明.txt                 # 用户说明
```

**macOS分发包**：
```
AI_Audio2Note_Mac/
├── ai-audio2note-backend        # 后端服务
├── AI_Audio2Note.app/           # Electron应用
├── 启动AI_Audio2Note.command    # 启动脚本
└── 使用说明.txt                 # 用户说明
```

### 用户使用

用户只需要：
1. 下载对应的分发包
2. 安装FFmpeg：`python install_ffmpeg.py`
3. 运行启动脚本即可使用

### 跨平台支持

- **Windows**：支持.exe打包和分发包
- **macOS**：支持.app打包和分发包
- **Linux**：支持Electron应用

### 详细构建指南

查看 `BUILD_GUIDE.md` 了解完整的构建和分发流程。

## 🐛 故障排除

### 常见问题

1. **FFmpeg未找到**
   - 确保FFmpeg已正确安装并在PATH中
   - 重启终端或IDE

2. **YouTube下载失败**
   - 更新yt-dlp到最新版本：`pip install --upgrade yt-dlp`
   - 检查网络连接

3. **B站链接无法识别**
   - 确保链接格式正确
   - 尝试清理链接中的跟踪参数

4. **文件夹选择器不工作**
   - 确保在Electron环境中运行
   - 检查系统权限设置

### 调试模式

启动时添加调试信息：
```bash
DEBUG=1 python start_native.py
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 📄 许可证

MIT License - 详见LICENSE文件

## 🙏 致谢

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - 强大的视频下载工具
- [Electron](https://electronjs.org/) - 跨平台桌面应用框架
- [FastAPI](https://fastapi.tiangolo.com/) - 现代Python Web框架

---

**AI Audio2Note** - 让视频音频提取变得简单高效！ 🎵