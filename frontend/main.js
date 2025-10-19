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
    show: false // 先不显示，等加载完成后再显示
  });

  console.log('Window created, loading HTML...');

  // 加载应用
  mainWindow.loadFile('index.html').then(() => {
    console.log('HTML loaded successfully');
    mainWindow.show(); // 加载完成后显示窗口
  }).catch((error) => {
    console.error('Failed to load HTML:', error);
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

  // 监听窗口错误
  mainWindow.webContents.on('did-fail-load', (event, errorCode, errorDescription) => {
    console.error('Failed to load:', errorCode, errorDescription);
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
    const result = await dialog.showOpenDialog(mainWindow, {
      properties: ['openDirectory'],
      title: '选择下载文件夹'
    });
    
    if (!result.canceled) {
      return result.filePaths[0];
    }
    return null;
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
