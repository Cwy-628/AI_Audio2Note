const { ipcRenderer } = require('electron');

class AudioDownloaderApp {
    constructor() {
        this.downloadDir = null; // 存储用户选择的下载目录
        this.initializeElements();
        this.bindEvents();
        this.loadHistory();
        this.checkBackendHealth();
    }

    initializeElements() {
        this.videoUrlInput = document.getElementById('videoUrl');
        this.pageNumberInput = document.getElementById('pageNumber');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.selectFolderBtn = document.getElementById('selectFolderBtn');
        this.statusMessage = document.getElementById('statusMessage');
        this.progressBar = document.getElementById('progressBar');
        this.resultSection = document.getElementById('resultSection');
        this.resultContent = document.getElementById('resultContent');
        this.historyList = document.getElementById('historyList');
        this.downloadDirInfo = document.getElementById('downloadDirInfo');
        this.currentDownloadDir = document.getElementById('currentDownloadDir');
    }

    bindEvents() {
        this.downloadBtn.addEventListener('click', () => this.handleDownload());
        this.selectFolderBtn.addEventListener('click', () => this.handleSelectFolder());
        
        // 回车键下载
        this.videoUrlInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.handleDownload();
            }
        });
    }

    async checkBackendHealth() {
        try {
            const result = await ipcRenderer.invoke('check-backend-health');
            if (result.status === 'error') {
                this.showStatus('后端服务未启动，请先启动后端服务', 'error');
            }
        } catch (error) {
            this.showStatus('无法连接到后端服务', 'error');
        }
    }

    async handleDownload() {
        console.log('开始下载处理...');
        
        const url = this.videoUrlInput.value.trim();
        const pageNumber = this.pageNumberInput.value ? parseInt(this.pageNumberInput.value) : null;

        console.log('URL:', url);
        console.log('Page Number:', pageNumber);

        if (!url) {
            console.log('URL为空');
            this.showStatus('请输入视频链接', 'error');
            return;
        }

        if (!this.isValidUrl(url)) {
            console.log('URL格式无效');
            this.showStatus('请输入有效的视频链接', 'error');
            return;
        }

        console.log('开始设置加载状态...');
        this.setLoading(true);
        this.showStatus('正在下载视频...', 'info');
        this.showProgress(true);

        try {
            console.log('直接调用后端API...');
            
            // 直接在前端调用后端API，避免IPC阻塞
            const response = await fetch('http://localhost:8001/api/process/video', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url: url,
                    page_number: pageNumber,
                    download_dir: this.downloadDir
                })
            });

            console.log('API响应状态:', response.status);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const result = await response.json();
            console.log('API调用结果:', result);

            if (result.success) {
                this.showStatus('下载完成！', 'success');
                this.showResult(result);
                this.addToHistory(url, result.video_title);
            } else {
                this.showStatus(`下载失败: ${result.error}`, 'error');
            }
        } catch (error) {
            console.error('下载过程中发生错误:', error);
            this.showStatus(`下载失败: ${error.message}`, 'error');
        } finally {
            console.log('清理加载状态...');
            this.setLoading(false);
            this.showProgress(false);
        }
    }

    async handleSelectFolder() {
        try {
            const folderPath = await ipcRenderer.invoke('select-download-folder');
            if (folderPath) {
                this.downloadDir = folderPath;
                this.currentDownloadDir.textContent = folderPath;
                this.downloadDirInfo.style.display = 'block';
                this.showStatus(`已选择下载文件夹: ${folderPath}`, 'info');
            }
        } catch (error) {
            this.showStatus(`选择文件夹失败: ${error.message}`, 'error');
        }
    }

    isValidUrl(url) {
        const urlPattern = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;
        return urlPattern.test(url);
    }

    setLoading(loading) {
        this.downloadBtn.disabled = loading;
        const btnText = this.downloadBtn.querySelector('.btn-text');
        const btnLoading = this.downloadBtn.querySelector('.btn-loading');
        
        if (loading) {
            btnText.style.display = 'none';
            btnLoading.style.display = 'inline';
        } else {
            btnText.style.display = 'inline';
            btnLoading.style.display = 'none';
        }
    }

    showStatus(message, type) {
        this.statusMessage.textContent = message;
        this.statusMessage.className = `status-message ${type}`;
        this.statusMessage.style.display = 'block';
        
        // 3秒后自动隐藏成功和错误消息
        if (type === 'success' || type === 'error') {
            setTimeout(() => {
                this.statusMessage.style.display = 'none';
            }, 3000);
        }
    }

    showProgress(show) {
        this.progressBar.style.display = show ? 'block' : 'none';
        if (show) {
            // 显示不确定进度条
            const progressFill = this.progressBar.querySelector('.progress-fill');
            progressFill.style.width = '100%';
            progressFill.style.animation = 'pulse 2s infinite';
        } else {
            // 停止动画
            const progressFill = this.progressBar.querySelector('.progress-fill');
            progressFill.style.animation = 'none';
        }
    }

    showResult(result) {
        this.resultSection.style.display = 'block';
        
        // 创建更友好的结果显示
        let resultText = `下载完成！\n\n`;
        resultText += `视频标题: ${result.video_title}\n`;
        resultText += `保存目录: ${result.session_folder}\n\n`;
        resultText += `下载的文件:\n`;
        
        result.files.forEach((file, index) => {
            resultText += `${index + 1}. ${file}\n`;
        });
        
        resultText += `\n完整结果:\n${JSON.stringify(result, null, 2)}`;
        
        this.resultContent.textContent = resultText;
    }

    addToHistory(url, title) {
        const history = this.getHistory();
        const newItem = {
            url: url,
            title: title || '未知标题',
            timestamp: new Date().toLocaleString()
        };
        
        // 避免重复添加
        const exists = history.some(item => item.url === url);
        if (!exists) {
            history.unshift(newItem);
            // 只保留最近20条记录
            if (history.length > 20) {
                history.splice(20);
            }
            this.saveHistory(history);
            this.renderHistory();
        }
    }

    getHistory() {
        const history = localStorage.getItem('downloadHistory');
        return history ? JSON.parse(history) : [];
    }

    saveHistory(history) {
        localStorage.setItem('downloadHistory', JSON.stringify(history));
    }

    loadHistory() {
        this.renderHistory();
    }

    renderHistory() {
        const history = this.getHistory();
        
        if (history.length === 0) {
            this.historyList.innerHTML = '<p class="no-history">暂无下载记录</p>';
            return;
        }

        this.historyList.innerHTML = history.map(item => `
            <div class="history-item" data-url="${item.url}">
                <div class="title">${item.title}</div>
                <div class="url">${item.url}</div>
                <div class="timestamp">${item.timestamp}</div>
            </div>
        `).join('');

        // 添加点击事件
        this.historyList.querySelectorAll('.history-item').forEach(item => {
            item.addEventListener('click', () => {
                const url = item.dataset.url;
                this.videoUrlInput.value = url;
                this.videoUrlInput.focus();
            });
        });
    }
}

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    new AudioDownloaderApp();
});
