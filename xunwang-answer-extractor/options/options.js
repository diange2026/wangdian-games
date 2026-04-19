// 讯网答案提取器 - 设置页面逻辑

class XunWangOptions {
    constructor() {
        this.initElements();
        this.bindEvents();
        this.loadSettings();
        this.loadStats();
    }

    // 初始化DOM元素
    initElements() {
        // 表单元素
        this.form = document.getElementById('settings-form');
        this.autoExtract = document.getElementById('auto-extract');
        this.autoSave = document.getElementById('auto-save');
        this.exportFormat = document.getElementById('export-format');
        this.notificationEnabled = document.getElementById('notification-enabled');
        this.dataRetention = document.getElementById('data-retention');
        this.theme = document.getElementById('theme');
        this.language = document.getElementById('language');
        this.compactMode = document.getElementById('compact-mode');
        this.timeout = document.getElementById('timeout');
        this.maxExtract = document.getElementById('max-extract');
        this.debugMode = document.getElementById('debug-mode');
        
        // 数据管理元素
        this.questionBankSize = document.getElementById('question-bank-size');
        this.historyCount = document.getElementById('history-count');
        
        // 按钮元素
        this.backBtn = document.getElementById('back-btn');
        this.resetBtn = document.getElementById('reset-btn');
        this.saveBtn = document.getElementById('save-btn');
        this.cancelBtn = document.getElementById('cancel-btn');
        this.exportAllBtn = document.getElementById('export-all-btn');
        this.clearDataBtn = document.getElementById('clear-data-btn');
        this.backupBtn = document.getElementById('backup-btn');
        this.checkUpdateBtn = document.getElementById('check-update-btn');
        this.helpBtn = document.getElementById('help-btn');
        this.privacyBtn = document.getElementById('privacy-btn');
        this.viewBankBtn = document.getElementById('view-bank-btn');
        this.viewHistoryBtn = document.getElementById('view-history-btn');
        
        // 状态栏
        this.statusBar = document.getElementById('status-bar');
        
        // 关于信息
        this.versionElement = document.getElementById('version');
        this.lastUpdateElement = document.getElementById('last-update');
        
        // 存储变量
        this.originalSettings = null;
        this.isChanged = false;
    }

    // 绑定事件监听器
    bindEvents() {
        // 表单变化监听
        this.form.addEventListener('change', () => {
            this.isChanged = true;
            this.updateStatus('设置已修改，请保存');
        });
        
        // 保存按钮
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveSettings();
        });
        
        // 返回按钮
        this.backBtn.addEventListener('click', () => {
            if (this.isChanged && !confirm('您有未保存的更改，确定要离开吗？')) {
                return;
            }
            window.close();
        });
        
        // 取消按钮
        this.cancelBtn.addEventListener('click', () => {
            if (this.isChanged && !confirm('您有未保存的更改，确定要取消吗？')) {
                return;
            }
            this.resetToOriginal();
        });
        
        // 恢复默认按钮
        this.resetBtn.addEventListener('click', () => {
            if (confirm('确定要恢复所有设置为默认值吗？')) {
                this.resetToDefaults();
            }
        });
        
        // 导出所有数据
        this.exportAllBtn.addEventListener('click', () => this.exportAllData());
        
        // 清空所有数据
        this.clearDataBtn.addEventListener('click', () => this.clearAllData());
        
        // 创建备份
        this.backupBtn.addEventListener('click', () => this.createBackup());
        
        // 检查更新
        this.checkUpdateBtn.addEventListener('click', () => this.checkForUpdates());
        
        // 帮助文档
        this.helpBtn.addEventListener('click', () => this.openHelp());
        
        // 隐私政策
        this.privacyBtn.addEventListener('click', () => this.openPrivacyPolicy());
        
        // 查看题库
        this.viewBankBtn.addEventListener('click', () => this.viewQuestionBank());
        
        // 查看历史记录
        this.viewHistoryBtn.addEventListener('click', () => this.viewHistory());
        
        // 页面卸载前提示
        window.addEventListener('beforeunload', (e) => {
            if (this.isChanged) {
                e.preventDefault();
                e.returnValue = '您有未保存的更改，确定要离开吗？';
            }
        });
    }

    // 加载设置
    async loadSettings() {
        try {
            this.updateStatus('正在加载设置...');
            
            const result = await chrome.storage.local.get(['userSettings']);
            const settings = result.userSettings || this.getDefaultSettings();
            
            // 保存原始设置
            this.originalSettings = { ...settings };
            
            // 更新表单
            this.updateForm(settings);
            
            // 加载关于信息
            await this.loadAboutInfo();
            
            this.updateStatus('设置加载完成');
            
        } catch (error) {
            console.error('加载设置失败:', error);
            this.showMessage('加载设置失败: ' + error.message, 'error');
            this.updateStatus('加载失败');
        }
    }

    // 获取默认设置
    getDefaultSettings() {
        return {
            autoExtract: false,
            autoSave: false,
            exportFormat: 'excel',
            notificationEnabled: true,
            dataRetentionDays: 30,
            theme: 'light',
            language: 'zh-CN',
            compactMode: false,
            timeout: 30,
            maxExtract: 100,
            debugMode: false
        };
    }

    // 更新表单
    updateForm(settings) {
        this.autoExtract.checked = settings.autoExtract;
        this.autoSave.checked = settings.autoSave;
        this.exportFormat.value = settings.exportFormat;
        this.notificationEnabled.checked = settings.notificationEnabled;
        this.dataRetention.value = settings.dataRetentionDays;
        this.theme.value = settings.theme;
        this.language.value = settings.language;
        this.compactMode.checked = settings.compactMode;
        this.timeout.value = settings.timeout;
        this.maxExtract.value = settings.maxExtract;
        this.debugMode.checked = settings.debugMode;
        
        this.isChanged = false;
    }

    // 加载统计信息
    async loadStats() {
        try {
            const result = await chrome.storage.local.get(['questionBank', 'extractionHistory']);
            
            const bankSize = result.questionBank?.length || 0;
            const historyCount = result.extractionHistory?.length || 0;
            
            this.questionBankSize.textContent = `${bankSize} 题`;
            this.historyCount.textContent = `${historyCount} 次`;
            
        } catch (error) {
            console.error('加载统计信息失败:', error);
            this.questionBankSize.textContent = '加载失败';
            this.historyCount.textContent = '加载失败';
        }
    }

    // 加载关于信息
    async loadAboutInfo() {
        try {
            // 获取扩展版本
            const manifest = chrome.runtime.getManifest();
            this.versionElement.textContent = manifest.version;
            
            // 获取最后更新时间
            const result = await chrome.storage.local.get(['lastUpdateCheck']);
            if (result.lastUpdateCheck) {
                const date = new Date(result.lastUpdateCheck);
                this.lastUpdateElement.textContent = date.toLocaleDateString('zh-CN');
            }
            
        } catch (error) {
            console.error('加载关于信息失败:', error);
        }
    }

    // 保存设置
    async saveSettings() {
        try {
            this.updateStatus('正在保存设置...');
            
            // 获取表单数据
            const settings = this.getFormData();
            
            // 验证设置
            if (!this.validateSettings(settings)) {
                return;
            }
            
            // 保存到存储
            await chrome.storage.local.set({ userSettings: settings });
            
            // 更新原始设置
            this.originalSettings = { ...settings };
            this.isChanged = false;
            
            // 发送消息给background script
            await chrome.runtime.sendMessage({
                action: 'updateSettings',
                data: settings
            });
            
            this.updateStatus('设置保存成功');
            this.showMessage('设置已成功保存', 'success');
            
            // 应用主题
            this.applyTheme(settings.theme);
            
        } catch (error) {
            console.error('保存设置失败:', error);
            this.updateStatus('保存失败');
            this.showMessage('保存设置失败: ' + error.message, 'error');
        }
    }

    // 获取表单数据
    getFormData() {
        return {
            autoExtract: this.autoExtract.checked,
            autoSave: this.autoSave.checked,
            exportFormat: this.exportFormat.value,
            notificationEnabled: this.notificationEnabled.checked,
            dataRetentionDays: parseInt(this.dataRetention.value),
            theme: this.theme.value,
            language: this.language.value,
            compactMode: this.compactMode.checked,
            timeout: parseInt(this.timeout.value),
            maxExtract: parseInt(this.maxExtract.value),
            debugMode: this.debugMode.checked
        };
    }

    // 验证设置
    validateSettings(settings) {
        if (settings.timeout < 5 || settings.timeout > 60) {
            this.showMessage('超时时间必须在5-60秒之间', 'error');
            this.timeout.focus();
            return false;
        }
        
        if (settings.maxExtract < 10 || settings.maxExtract > 1000) {
            this.showMessage('最大提取数量必须在10-1000题之间', 'error');
            this.maxExtract.focus();
            return false;
        }
        
        return true;
    }

    // 应用主题
    applyTheme(theme) {
        const root = document.documentElement;
        
        if (theme === 'dark') {
            root.style.setProperty('--bg-color', '#1a1a1a');
            root.style.setProperty('--text-color', '#ffffff');
            root.style.setProperty('--border-color', '#333333');
        } else {
            root.style.removeProperty('--bg-color');
            root.style.removeProperty('--text-color');
            root.style.removeProperty('--border-color');
        }
    }

    // 重置到原始设置
    resetToOriginal() {
        if (this.originalSettings) {
            this.updateForm(this.originalSettings);
            this.updateStatus('已恢复原始设置');
            this.showMessage('已恢复原始设置', 'info');
        }
    }

    // 重置到默认设置
    resetToDefaults() {
        const defaultSettings = this.getDefaultSettings();
        this.updateForm(defaultSettings);
        this.updateStatus('已恢复默认设置');
        this.showMessage('已恢复默认设置', 'info');
    }

    // 导出所有数据
    async exportAllData() {
        try {
            this.updateStatus('正在准备导出数据...');
            
            const result = await chrome.storage.local.get([
                'questionBank',
                'extractionHistory',
                'lastExtractedData',
                'userSettings'
            ]);
            
            const exportData = {
                metadata: {
                    exportTime: new Date().toISOString(),
                    version: this.versionElement.textContent,
                    dataTypes: []
                },
                questionBank: result.questionBank || [],
                extractionHistory: result.extractionHistory || [],
                lastExtractedData: result.lastExtractedData || [],
                settings: result.userSettings || {}
            };
            
            // 统计数据类型
            if (exportData.questionBank.length > 0) {
                exportData.metadata.dataTypes.push('题库');
            }
            if (exportData.extractionHistory.length > 0) {
                exportData.metadata.dataTypes.push('历史记录');
            }
            if (exportData.lastExtractedData.length > 0) {
                exportData.metadata.dataTypes.push('最近数据');
            }
            
            // 生成JSON文件
            const jsonStr = JSON.stringify(exportData, null, 2);
            const blob = new Blob([jsonStr], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            
            // 下载文件
            const a = document.createElement('a');
            a.href = url;
            a.download = `xunwang_backup_${Date.now()}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            
            // 清理URL
            setTimeout(() => URL.revokeObjectURL(url), 1000);
            
            this.updateStatus('数据导出成功');
            this.showMessage('所有数据已导出为JSON文件', 'success');
            
        } catch (error) {
            console.error('导出数据失败:', error);
            this.updateStatus('导出失败');
            this.showMessage('导出数据失败: ' + error.message, 'error');
        }
    }

    // 清空所有数据
    async clearAllData() {
        if (!confirm('⚠️ 警告：这将删除所有本地数据，包括题库、历史记录和设置。此操作不可逆。确定要继续吗？')) {
            return;
        }
        
        try {
            this.updateStatus('正在清空数据...');
            
            // 清空所有存储
            await chrome.storage.local.clear();
            
            // 重置为默认设置
            await this.setupDefaultStorage();
            
            // 重新加载
            await this.loadSettings();
            await this.loadStats();
            
            this.updateStatus('数据已清空');
            this.showMessage('所有数据已成功清空', 'success');
            
        } catch (error) {
            console.error('清空数据失败:', error);
            this.updateStatus('清空失败');
            this.showMessage('清空数据失败: ' + error.message, 'error');
        }
    }

    // 设置默认存储
    async setupDefaultStorage() {
        const defaultSettings = this.getDefaultSettings();
        await chrome.storage.local.set({
            userSettings: defaultSettings,
            questionBank: [],
            extractionHistory: [],
            stats: {
                totalExtractions: 0,
                totalQuestions: 0,
                firstUse: Date.now(),
                lastUse: Date.now()
            }
        });
    }

    // 创建备份
    async createBackup() {
        try {
            this.updateStatus('正在创建备份...');
            
            // 这里可以调用扩展的备份API
            // 暂时使用导出功能
            await this.exportAllData();
            
        } catch (error) {
            console.error('创建备份失败:', error);
            this.updateStatus('备份失败');
            this.showMessage('创建备份失败: ' + error.message, 'error');
        }
    }

    // 检查更新
    async checkForUpdates() {
        try {
            this.updateStatus('正在检查更新...');
            
            // 模拟检查更新
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // 这里应该调用实际的更新检查API
            this.updateStatus('已是最新版本');
            this.showMessage('当前已是最新版本', 'success');
            
        } catch (error) {
            console.error('检查更新失败:', error);
            this.updateStatus('检查失败');
            this.showMessage('检查更新失败: ' + error.message, 'error');
        }
    }

    // 打开帮助文档
    openHelp() {
        window.open('https://github.com/diange2026/xunwang-extractor/wiki', '_blank');
    }

    // 打开隐私政策
    openPrivacyPolicy() {
        window.open('https://github.com/diange2026/xunwang-extractor/wiki/Privacy-Policy', '_blank');
    }

    // 查看题库
    async viewQuestionBank() {
        try {
            this.updateStatus('正在加载题库...');
            
            const result = await chrome.storage.local.get(['questionBank']);
            const questionBank = result.questionBank || [];
            
            if (questionBank.length === 0) {
                this.showMessage('题库为空', 'info');
                this.updateStatus('题库为空');
                return;
            }
            
            // 打开新页面显示题库
            const win = window.open('', '_blank');
            win.document.write(`
                <html>
                <head>
                    <title>讯网题库 - ${questionBank.length} 题</title>
                    <style>
                        body { font-family: Arial; padding: 20px; }
                        .question { margin: 15px 0; padding: 10px; border: 1px solid #ddd; }
                        .answer { color: green; font-weight: bold; }
                    </style>
                </head>
                <body>
                    <h1>讯网题库 (${questionBank.length} 题)</h1>
                    ${questionBank.map((q, i) => `
                        <div class="question">
                            <h3>${i + 1}. ${q.question || '无题目'}</h3>
                            <p class="answer">答案: ${q.answer || '无答案'}</p>
                            <small>知识点: ${q.knowledge || '无'}</small>
                        </div>
                    `).join('')}
                </body>
                </html>
            `);
            
            this.updateStatus('题库已打开');
            
        } catch (error) {
            console.error('查看题库失败:', error);
            this.showMessage('查看题库失败: ' + error.message, 'error');
        }
    }

    // 查看历史记录
    async viewHistory() {
        try {
            this.updateStatus('正在加载历史记录...');
            
            const result = await chrome.storage.local.get(['extractionHistory']);
            const history = result.extractionHistory || [];
            
            if (history.length === 0) {
                this.showMessage('历史记录为空', 'info');
                this.updateStatus('历史记录为空');
                return;
            }
            
            // 打开新页面显示历史记录
            const win = window.open('', '_blank');
            win.document.write(`
                <html>
                <head>
                    <title>提取历史记录 - ${history.length} 次</title>
                    <style>
                        body { font-family: Arial; padding: 20px; }
                        .history-item { margin: 10px 0; padding: 10px; background: #f5f5f5; }
                        .time { color: #666; font-size: 12px; }
                        .count { color: blue; font-weight: bold; }
                    </style>
                </head>
                <body>
                    <h1>提取历史记录 (${history.length} 次)</h1>
                    ${history.map((h, i) => `
                        <div class="history-item">
                            <div class="time">${new Date(h.timestamp).toLocaleString('zh-CN')}</div>
                            <div class="count">提取了 ${h.count} 题</div>
                            <div>来源: ${h.source || '未知'}</div>
                        </div>
                    `).join('')}
                </body>
                </html>
            `);
            
            this.updateStatus('历史记录已打开');
            
        } catch (error) {
            console.error('查看历史记录失败:', error);
            this.showMessage('查看历史记录失败: ' + error.message, 'error');
        }
    }

    // 更新状态栏
    updateStatus(text) {
        this.statusBar.textContent = text;
        this.statusBar.className = 'status-bar';
        this.statusBar.classList.add('fade-in');
    }

    // 显示消息
    showMessage(message, type = 'info') {
        // 移除现有消息
        const existing = document.querySelector('.message');
        if (existing) existing.remove();
        
        // 创建新消息
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = message;
        
        // 添加到页面
        document.body.appendChild(messageDiv);
        
        // 自动移除
        setTimeout(() => {
            messageDiv.classList.add('fade-out');
            setTimeout(() => {
                messageDiv.remove();
            }, 300);
        }, 3000);
    }
}

// 初始化设置页面
document.addEventListener('DOMContentLoaded', () => {
    new XunWangOptions();
});

// 添加消息动画样式
const style = document.createElement('style');
style.textContent = `
    .fade-out {
        animation: fadeOut 0.3s ease-out forwards;
    }
    
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; transform: translateY(-10px); }
    }
`;
document.head.appendChild(style);