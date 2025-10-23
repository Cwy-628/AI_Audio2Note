const { app, BrowserWindow } = require('electron');

let mainWindow;

function createWindow() {
  console.log('Creating test window...');
  
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    },
    title: 'AI Audio2Note Test',
    show: true,
    center: true
  });

  // 加载一个简单的HTML页面
  mainWindow.loadURL('data:text/html,<html><body><h1>Hello from Electron!</h1><p>If you can see this, Electron is working.</p></body></html>');
  
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
  
  console.log('Test window created');
}

app.whenReady().then(createWindow);

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
