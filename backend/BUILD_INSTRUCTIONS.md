# 构建说明文档

本文档说明如何为不同平台构建AI Audio2Note后端程序。

## 支持的平台

- **Windows**: 生成 `.exe` 文件
- **Mac**: 生成可执行文件或 `.app` 应用程序包
- **Linux**: 生成可执行文件

## 构建脚本说明

### 1. 原始Windows构建脚本
- **文件**: `build_exe.py`
- **用途**: 专门为Windows系统构建exe文件
- **运行**: `python build_exe.py`

### 2. Mac可执行文件构建脚本
- **文件**: `build_mac.py`
- **用途**: 为Mac系统构建可执行文件
- **运行**: `python build_mac.py`

### 3. Mac应用程序包构建脚本
- **文件**: `build_mac_app.py`
- **用途**: 为Mac系统构建.app应用程序包
- **运行**: `python build_mac_app.py`

### 4. 跨平台构建脚本（推荐）
- **文件**: `build_cross_platform.py`
- **用途**: 自动检测平台或指定平台进行构建
- **运行**: 
  - `python build_cross_platform.py` (自动检测当前平台)
  - `python build_cross_platform.py windows` (构建Windows版本)
  - `python build_cross_platform.py mac` (构建Mac版本)
  - `python build_cross_platform.py linux` (构建Linux版本)

## 使用步骤

### 1. 安装依赖
```bash
# 确保已安装PyInstaller
pip install pyinstaller

# 安装项目依赖
pip install -r requirements.txt
```

### 2. 构建可执行文件

#### 方法一：使用跨平台脚本（推荐）
```bash
# 自动检测当前平台并构建
python build_cross_platform.py

# 或指定目标平台
python build_cross_platform.py mac
```

#### 方法二：使用专用脚本
```bash
# 构建Mac可执行文件
python build_mac.py

# 构建Mac应用程序包
python build_mac_app.py
```

### 3. 输出文件位置
构建完成后，可执行文件将位于：
- `dist/ai-audio2note-backend` (Mac/Linux)
- `dist/ai-audio2note-backend.exe` (Windows)
- `dist/AI-Audio2Note-Backend.app` (Mac应用程序包)

## 平台特定说明

### Mac系统
- **可执行文件**: 生成无扩展名的可执行文件
- **应用程序包**: 生成标准的Mac应用程序包，可以双击运行
- **路径分隔符**: 使用冒号(`:`)而不是分号(`;`)

### Windows系统
- **可执行文件**: 生成`.exe`文件
- **路径分隔符**: 使用分号(`;`)

### Linux系统
- **可执行文件**: 生成无扩展名的可执行文件
- **路径分隔符**: 使用冒号(`:`)

## 运行构建后的程序

### Mac/Linux
```bash
# 直接运行
./dist/ai-audio2note-backend

# 或运行应用程序包
open dist/AI-Audio2Note-Backend.app
```

### Windows
```bash
# 直接运行
dist\ai-audio2note-backend.exe
```

## 故障排除

### 常见问题

1. **PyInstaller未安装**
   ```bash
   pip install pyinstaller
   ```

2. **依赖缺失**
   ```bash
   pip install -r requirements.txt
   ```

3. **权限问题（Mac/Linux）**
   ```bash
   chmod +x dist/ai-audio2note-backend
   ```

4. **路径问题**
   - Windows使用分号(`;`)分隔路径
   - Mac/Linux使用冒号(`:`)分隔路径

### 构建优化

1. **减小文件大小**
   - 使用`--exclude-module`排除不需要的模块
   - 使用`--strip`去除调试信息

2. **提高启动速度**
   - 使用`--onedir`模式而不是`--onefile`
   - 预编译Python字节码

## 注意事项

1. **跨平台兼容性**: 在Mac上构建的Mac版本只能在Mac上运行
2. **依赖管理**: 确保目标系统有必要的运行时依赖
3. **文件权限**: Mac/Linux系统可能需要设置执行权限
4. **代码签名**: 生产环境建议对Mac应用程序进行代码签名

## 开发建议

1. **使用虚拟环境**: 避免依赖冲突
2. **测试构建**: 在目标平台上测试构建结果
3. **版本管理**: 为不同平台维护不同的构建脚本
4. **自动化**: 考虑使用CI/CD自动化构建流程
