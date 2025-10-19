# 开发文档

## 项目架构

### 后端架构 (FastAPI)

```
backend/
├── main.py                 # 应用入口，路由定义
├── services/              # 业务逻辑层
│   ├── audio_downloader.py    # 音频下载核心逻辑
│   └── process_service.py     # 视频处理服务
└── requirements.txt       # 依赖管理
```

**设计模式**:
- 服务层模式：将业务逻辑封装在services目录中
- 依赖注入：使用FastAPI的依赖注入系统
- 异步处理：支持异步请求处理

### 前端架构 (Electron)

```
frontend/
├── main.js               # Electron主进程
├── index.html            # 应用界面
├── styles.css            # 样式定义
├── renderer.js           # 渲染进程逻辑
└── package.json          # 依赖和构建配置
```

**设计模式**:
- 主进程/渲染进程分离
- IPC通信：主进程与渲染进程间通信
- 模块化：JavaScript代码模块化组织

## API接口文档

### 基础信息
- 基础URL: `http://localhost:8000`
- 内容类型: `application/json`

### 接口列表

#### 1. 健康检查
```
GET /health
```
**响应**:
```json
{
  "status": "healthy"
}
```

#### 2. 视频处理
```
POST /api/process/video
```
**请求体**:
```json
{
  "url": "https://www.bilibili.com/video/BV1xxx",
  "page_number": 1
}
```
**响应**:
```json
{
  "success": true,
  "files": ["/path/to/file1.mp3", "/path/to/file2.mp3"],
  "session_folder": "/path/to/session",
  "video_title": "视频标题"
}
```

## 开发环境设置

### 1. 克隆项目
```bash
git clone <repository-url>
cd AI_audio2note
```

### 2. 设置Python环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 设置Node.js环境
```bash
cd frontend
npm install
```

### 4. 安装FFmpeg
- Windows: 下载FFmpeg并添加到PATH
- Linux: `sudo apt install ffmpeg`
- Mac: `brew install ffmpeg`

## 开发工作流

### 1. 启动开发环境
```bash
python start_dev.py
```

### 2. 代码修改
- 后端修改：自动重载
- 前端修改：需要重启Electron

### 3. 测试
```bash
# 后端测试
cd backend
python -m pytest

# 前端测试
cd frontend
npm test
```

### 4. 构建
```bash
# 开发构建
python build.py

# 生产构建
python build.py --production
```

## 代码规范

### Python代码规范
- 使用PEP 8代码风格
- 类型提示：使用typing模块
- 文档字符串：使用Google风格
- 错误处理：使用try-except块

### JavaScript代码规范
- 使用ES6+语法
- 使用const/let替代var
- 使用箭头函数
- 使用模板字符串

### 命名规范
- 文件名：使用下划线分隔 (snake_case)
- 类名：使用大驼峰命名 (PascalCase)
- 函数名：使用下划线分隔 (snake_case)
- 变量名：使用下划线分隔 (snake_case)

## 调试指南

### 后端调试
1. 使用print语句或logging模块
2. 使用FastAPI的自动文档：`http://localhost:8000/docs`
3. 使用调试器：在IDE中设置断点

### 前端调试
1. 使用console.log输出调试信息
2. 使用Electron开发者工具
3. 使用Chrome DevTools

### 常见调试技巧
1. 检查控制台错误信息
2. 检查网络请求状态
3. 检查文件权限
4. 检查依赖版本

## 性能优化

### 后端优化
1. 使用异步处理
2. 缓存频繁访问的数据
3. 优化数据库查询
4. 使用连接池

### 前端优化
1. 使用虚拟滚动
2. 懒加载组件
3. 优化图片资源
4. 减少DOM操作

## 安全考虑

### 后端安全
1. 输入验证：使用Pydantic模型
2. 错误处理：不暴露敏感信息
3. CORS配置：限制允许的域名
4. 文件路径：防止路径遍历攻击

### 前端安全
1. 内容安全策略(CSP)
2. 输入验证：客户端验证
3. XSS防护：转义用户输入
4. 文件下载：验证文件类型

## 部署指南

### 开发环境部署
1. 克隆代码
2. 安装依赖
3. 启动服务

### 生产环境部署
1. 构建应用
2. 配置环境变量
3. 启动服务
4. 配置反向代理（可选）

### Docker部署（可选）
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

## 监控和日志

### 日志配置
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 监控指标
1. API响应时间
2. 错误率
3. 内存使用
4. CPU使用

## 版本控制

### Git工作流
1. 主分支：main
2. 开发分支：develop
3. 功能分支：feature/xxx
4. 修复分支：hotfix/xxx

### 提交规范
```
type(scope): description

feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试
chore: 构建过程或辅助工具的变动
```

## 测试策略

### 单元测试
- 后端：使用pytest
- 前端：使用Jest

### 集成测试
- API接口测试
- 端到端测试

### 测试覆盖率
- 目标：80%以上
- 工具：coverage.py

## 持续集成

### GitHub Actions配置
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
```
