const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const axios = require('axios');

// 后端API地址
const API_BASE_URL = 'http://localhost:8001';

let mainWindow;

function createWindow() {
  console.log('Creating window...');
  
  // 创建浏览器窗口
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true,
      webSecurity: false // 允许跨域请求
    },
    // icon: path.join(__dirname, 'assets/icon.png'), // 暂时注释掉，因为图标文件不存在
    title: 'AI Audio2Note',
    show: true, // 立即显示窗口
    center: true, // 居中显示
    resizable: true,
    minimizable: true,
    maximizable: true,
    closable: true,
    alwaysOnTop: false, // 不要总是在最前面
    skipTaskbar: false, // 在任务栏中显示
    fullscreenable: true,
    frame: true // 显示窗口框架
  });

  console.log('Window created, loading HTML...');

  // 加载应用
  mainWindow.loadFile('index.html').then(() => {
    console.log('HTML loaded successfully');
    mainWindow.show(); // 确保窗口显示
    mainWindow.focus(); // 聚焦到窗口
    console.log('Window should be visible now');
  }).catch((error) => {
    console.error('Failed to load HTML:', error);
    // 即使加载失败也显示窗口，这样用户可以看到错误
    mainWindow.show();
  });

  // 开发模式下可以选择是否打开开发者工具
  // 如果需要调试，可以取消下面的注释
  // if (process.argv.includes('--dev')) {
  //   mainWindow.webContents.openDevTools();
  // }

  // 当窗口被关闭时
  mainWindow.on('closed', () => {
    console.log('Window closed');
    mainWindow = null;
  });

  // 监听窗口显示事件
  mainWindow.on('show', () => {
    console.log('Window is now visible');
  });

  // 监听窗口隐藏事件
  mainWindow.on('hide', () => {
    console.log('Window is now hidden');
  });

  // 监听窗口错误
  mainWindow.webContents.on('did-fail-load', (event, errorCode, errorDescription) => {
    console.error('Failed to load:', errorCode, errorDescription);
  });

  // 监听页面加载完成
  mainWindow.webContents.on('did-finish-load', () => {
    console.log('Page finished loading');
  });

  // 监听页面开始加载
  mainWindow.webContents.on('did-start-loading', () => {
    console.log('Page started loading');
  });

  console.log('Window setup complete');
}

// 当 Electron 完成初始化并准备创建浏览器窗口时调用此方法
app.whenReady().then(() => {
  createWindow();
  // 由于现在使用直接API调用，不需要复杂的IPC处理器
  setupIpcHandlers();
});

// 当所有窗口都被关闭时退出应用
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// IPC 处理程序设置函数
function setupIpcHandlers() {
  // 只保留必要的IPC处理器，视频处理现在直接通过API调用
  
  ipcMain.handle('check-backend-health', async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`);
      return { status: 'healthy', data: response.data };
    } catch (error) {
      return { status: 'error', error: error.message };
    }
  });

  ipcMain.handle('select-download-folder', async () => {
    try {
      const result = await dialog.showOpenDialog(mainWindow, {
        properties: ['openDirectory'],
        title: '选择下载文件夹',
        buttonLabel: '选择此文件夹',
        message: '请选择用于保存下载文件的文件夹'
      });
      
      if (!result.canceled && result.filePaths.length > 0) {
        console.log('用户选择的文件夹:', result.filePaths[0]);
        return result.filePaths[0];
      }
      return null;
    } catch (error) {
      console.error('文件夹选择错误:', error);
      return null;
    }
  });

  ipcMain.handle('show-message-box', async (event, { type, title, message }) => {
    const result = await dialog.showMessageBox(mainWindow, {
      type: type || 'info',
      title: title || 'AI Audio2Note',
      message: message || '',
      buttons: ['确定']
    });
    return result;
  });
}
