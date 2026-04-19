// 讯网答案提取器 - 弹出窗口逻辑
class XunWangExtractorPopup {
    constructor() {
        this.initElements();
        this.bindEvents();
        this.init();
    }

    // 初始化DOM元素
    initElements() {
        // 状态显示元素
        this.currentPageElement = document.getElementById('current-page');
        this.loginStatusElement = document.getElementById('login-status');
        this.questionCountElement = document.getElementById('question-count');
        
        // 按钮元素
        this.extractBtn = document.getElementById('extract-btn');
        this.exportExcelBtn = document.getElementById('export-excel-btn');
        this.exportCsvBtn = document.getElementById('export-csv-btn');
        this.saveLocalBtn = document.getElementById('save-local-btn');
        this.clearResultBtn = document.getElementById('clear-result-btn');
        
        // 设置相关按钮
        this.settingsBtn = document.getElementById('settings-btn');
        this.helpBtn = document.getElementById('help-btn');
        this.aboutBtn = document.getElementById('about-btn');
        
        // 结果区域
        this.resultSection = document.getElementById('result-section');
        this.resultList = document.getElementById('result-list');
        
        // 进度区域
        this.progressSection = document.getElementById('progress-section');
        this.progressFill = document.getElementById('progress-fill');
        this.progressText = document.getElementById('progress-text');
        
        // 存储变量
        this.extractedData = [];
        this.currentTabId = null;
    }

    // 绑定事件监听器
    bindEvents() {
        // 提取答案按钮
        this.extractBtn.addEventListener('click', () => this.extractAnswers());
        
        // 导出按钮
        this.exportExcelBtn.addEventListener('click', () => this.exportData('excel'));
        this.exportCsvBtn.addEventListener('click', () => this.exportData('csv'));
        
        // 保存到本地题库
        this.saveLocalBtn.addEventListener('click', () => this.saveToLocal());
        
        // 清空结果
        this.clearResultBtn.addEventListener('click', () => this.clearResults());
        
        // 设置相关
        this.settingsBtn.addEventListener('click', (e) => {
            e.preventDefault();
            this.openSettings();
        });
        
        this.helpBtn.addEventListener('click', (e) => {
            e.preventDefault();
            this.openHelp();
        });
        
        this.aboutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            this.openAbout();
        });
    }

    // 初始化
    async init() {
        // 获取当前标签页信息
        const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
        if (tabs.length > 0) {
            this.currentTabId = tabs[0].id;
            this.checkPageStatus(tabs[0].url);
        }
        
        // 加载存储的数据
        await this.loadStoredData();
        
        // 更新按钮状态
        this.updateButtonStates();
    }

    // 检查页面状态
    checkPageStatus(url) {
        const isXunWangPage = url && url.includes('whxunw.com');
        const isAnswerPage = url && url.includes('assignments-detail');
        
        if (isXunWangPage) {
            this.currentPageElement.textContent = '讯网教学平台';
            this.currentPageElement.style.color = '#2ecc71';
            
            if (isAnswerPage) {
                this.currentPageElement.textContent = '答案详情页面';
                this.extractBtn.disabled = false;
            } else {
                this.currentPageElement.textContent = '其他页面';
                this.extractBtn.disabled = true;
            }
        } else {
            this.currentPageElement.textContent = '未检测到讯网页面';
            this.currentPageElement.style.color = '#e74c3c';
            this.extractBtn.disabled = true;
        }
        
        // 模拟检测题目数量
        this.questionCountElement.textContent = isAnswerPage ? '检测中...' : '0 题';
        
        // 模拟登录状态
        this.loginStatusElement.textContent = isXunWangPage ? '已登录' : '未登录';
        this.loginStatusElement.style.color = isXunWangPage ? '#2ecc71' : '#e74c3c';
    }

    // 提取答案
    async extractAnswers() {
        if (!this.currentTabId) {
            this.showMessage('未找到有效标签页', 'error');
            return;
        }

        // 显示进度条
        this.showProgress('正在提取答案...', 0);
        
        try {
            // 发送消息给content script
            const response = await chrome.tabs.sendMessage(this.currentTabId, {
                action: 'extractAnswers'
            });
            
            if (response && response.success) {
                this.extractedData = response.data;
                this.showProgress('提取完成', 100);
                
                // 更新UI
                this.updateQuestionCount(this.extractedData.length);
                this.displayResults(this.extractedData);
                this.updateButtonStates();
                
                // 保存到存储
                await this.saveExtractedData();
                
                this.showMessage(`成功提取 ${this.extractedData.length} 条答案`, 'success');
            } else {
                this.showProgress('提取失败', 100);
                this.showMessage(response?.message || '提取答案失败', 'error');
            }
        } catch (error) {
            console.error('提取答案错误:', error);
            this.showProgress('提取失败', 100);
            this.showMessage('提取过程中发生错误', 'error');
        } finally {
            // 隐藏进度条
            setTimeout(() => {
                this.hideProgress();
            }, 1500);
        }
    }

    // 导出数据
    async exportData(format) {
        if (this.extractedData.length === 0) {
            this.showMessage('没有可导出的数据', 'warning');
            return;
        }

        this.showProgress(`正在导出${format.toUpperCase()}...`, 0);
        
        try {
            // 根据格式处理数据
            let dataToExport;
            let filename = `讯网答案_${this.getCurrentDate()}`;
            
            if (format === 'excel') {
                dataToExport = this.prepareExcelData();
                filename += '.xlsx';
            } else {
                dataToExport = this.prepareCsvData();
                filename += '.csv';
            }
            
            // 创建Blob并下载
            const blob = new Blob([dataToExport], { 
                type: format === 'excel' 
                    ? 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
                    : 'text/csv;charset=utf-8;' 
            });
            
            const url = URL.createObjectURL(blob);
            chrome.downloads.download({
                url: url,
                filename: filename,
                saveAs: true
            });
            
            this.showProgress('导出完成', 100);
            this.showMessage(`数据已导出为 ${filename}`, 'success');
            
        } catch (error) {
            console.error('导出数据错误:', error);
            this.showProgress('导出失败', 100);
            this.showMessage('导出过程中发生错误', 'error');
        } finally {
            setTimeout(() => {
                this.hideProgress();
            }, 1500);
        }
    }

    // 保存到本地题库
    async saveToLocal() {
        if (this.extractedData.length === 0) {
            this.showMessage('没有可保存的数据', 'warning');
            return;
        }

        this.showProgress('正在保存到本地题库...', 0);
        
        try {
            // 获取现有题库数据
            const storage = await chrome.storage.local.get(['questionBank']);
            let questionBank = storage.questionBank || [];
            
            // 添加新数据（去重）
            const newData = this.extractedData.filter(item => {
                return !questionBank.some(existing => 
                    existing.questionId === item.questionId
                );
            });
            
            questionBank = [...questionBank, ...newData];
            
            // 保存到存储
            await chrome.storage.local.set({ questionBank });
            
            this.showProgress('保存完成', 100);
            this.showMessage(`成功保存 ${newData.length} 条新题目到本地题库`, 'success');
            
        } catch (error) {
            console.error('保存到本地题库错误:', error);
            this.showProgress('保存失败', 100);
            this.showMessage('保存过程中发生错误', 'error');
        } finally {
            setTimeout(() => {
                this.hideProgress();
            }, 1500);
        }
    }

    // 清空结果
    clearResults() {
        this.extractedData = [];
        this.resultList.innerHTML = '';
        this.resultSection.style.display = 'none';
        this.updateQuestionCount(0);
        this.updateButtonStates();
        this.showMessage('结果已清空', 'info');
    }

    // 打开设置页面
    openSettings() {
        chrome.runtime.openOptionsPage();
    }

    // 打开帮助页面
    openHelp() {
        // 这里可以打开帮助文档或教程
        window.open('https://github.com/diange2026/xunwang-extractor/wiki', '_blank');
    }

    // 打开关于页面
    openAbout() {
        this.showMessage('讯网答案提取器 v1.0.0\n© 2026 讯网助手团队', 'info');
    }

    // 显示进度条
    showProgress(text, percent) {
        this.progressText.textContent = text;
        this.progressFill.style.width = `${percent}%`;
        this.progressSection.style.display = 'block';
    }

    // 隐藏进度条
    hideProgress() {
        this.progressSection.style.display = 'none';
        this.progressFill.style.width = '0%';
    }

    // 显示消息
    showMessage(message, type = 'info') {
        // 创建消息元素
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = message;
        
        // 添加到页面
        const container = document.querySelector('.container');
        container.insertBefore(messageDiv, container.firstChild);
        
        // 自动移除
        setTimeout(() => {
            messageDiv.classList.add('fade-out');
            setTimeout(() => {
                messageDiv.remove();
            }, 300);
        }, 3000);
    }

    // 更新题目数量
    updateQuestionCount(count) {
        this.questionCountElement.textContent = `${count} 题`;
        this.questionCountElement.style.color = count > 0 ? '#2ecc71' : '#495057';
    }

    // 显示结果
    displayResults(data) {
        this.resultList.innerHTML = '';
        
        if (data.length === 0) {
            this.resultSection.style.display = 'none';
            return;
        }
        
        data.forEach((item, index) => {
            const resultItem = document.createElement('div');
            resultItem.className = `result-item ${item.isCorrect ? 'result-correct' : 'result-incorrect'}`;
            resultItem.innerHTML = `
                <span class="result-number">${index + 1}</span>
                <span class="result-question" title="${item.question}">${item.question}</span>
                <span class="result-answer">${item.answer}</span>
            `;
            this.resultList.appendChild(resultItem);
        });
        
        this.resultSection.style.display = 'block';
    }

    // 更新按钮状态
    updateButtonStates() {
        const hasData = this.extractedData.length > 0;
        this.exportExcelBtn.disabled = !hasData;
        this.exportCsvBtn.disabled = !hasData;
        this.saveLocalBtn.disabled = !hasData;
        this.clearResultBtn.disabled = !hasData;
    }

    // 加载存储的数据
    async loadStoredData() {
        try {
            const storage = await chrome.storage.local.get(['extractedData']);
            if (storage.extractedData) {
                this.extractedData = storage.extractedData;
                this.displayResults(this.extractedData);
                this.updateQuestionCount(this.extractedData.length);
            }
        } catch (error) {
            console.error('加载存储数据错误:', error);
        }
    }

    // 保存提取的数据
    async saveExtractedData() {
        try {
            await chrome.storage.local.set({
                extractedData: this.extractedData
            });
        } catch (error) {
            console.error('保存提取数据错误:', error);
        }
    }

    // 准备Excel数据（简化版）
    prepareExcelData() {
        // 这里应该使用xlsx库来生成Excel文件
        // 为了简化，我们生成一个简化版的CSV
        return this.prepareCsvData();
    }

    // 准备CSV数据
    prepareCsvData() {
        const headers = ['序号', '题目', '标准答案', '用户答案', '是否正确', '分值', '知识点'];
        const rows = this.extractedData.map((item, index) => [
            index + 1,
            `"${item.question.replace(/"/g, '""')}"`, // 处理引号
            `"${item.answer.replace(/"/g, '""')}"`,
            `"${item.userAnswer || ''}"`,
            item.isCorrect ? '是' : '否',
            item.score || 0,
            `"${item.knowledge || ''}"`
        ]);
        
        return [headers, ...rows]
            .map(row => row.join(','))
            .join('\n');
    }

    // 获取当前日期
    getCurrentDate() {
        const now = new Date();
        return `${now.getFullYear()}${(now.getMonth() + 1).toString().padStart(2, '0')}${now.getDate().toString().padStart(2, '0')}_${now.getHours().toString().padStart(2, '0')}${now.getMinutes().toString().padStart(2, '0')}`;
    }
}

// 添加消息样式
const style = document.createElement('style');
style.textContent = `
    .message {
        position: fixed;
        top: 10px;
        left: 50%;
        transform: translateX(-50%);
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: 500;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: slideIn 0.3s ease-out;
        max-width: 80%;
        text-align: center;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-50%) translateY(-20px); }
        to { opacity: 1; transform: translateX(-50%) translateY(0); }
    }
    
    .message.info {
        background: #d1ecf1;
        color: #0c5460;
        border: 1px solid #bee5eb;
    }
    
    .message.success {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .message.warning {
        background: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    
    .message.error {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    .fade-out {
        animation: fadeOut 0.3s ease-out forwards;
    }
    
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; transform: translateX(-50%) translateY(-10px); }
    }
`;
document.head.appendChild(style);

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    new XunWangExtractorPopup();
});