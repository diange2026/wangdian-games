// 讯网答案提取器 - 后台服务脚本

class XunWangBackgroundService {
    constructor() {
        this.init();
        this.setupEventListeners();
        this.currentData = null;
        this.userSettings = {};
    }

    // 初始化
    async init() {
        console.log('讯网答案提取器后台服务启动');
        
        // 加载用户设置
        await this.loadSettings();
        
        // 检查更新
        await this.checkForUpdates();
        
        // 初始化数据存储
        await this.initializeStorage();
    }

    // 设置事件监听器
    setupEventListeners() {
        // 监听扩展安装/更新
        chrome.runtime.onInstalled.addListener((details) => {
            this.onInstalled(details);
        });

        // 监听来自popup的消息
        chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
            this.handleMessage(message, sender, sendResponse);
        });

        // 监听页面导航
        chrome.webNavigation.onCompleted.addListener((details) => {
            this.onPageLoaded(details);
        });

        // 监听标签页更新
        chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
            this.onTabUpdated(tabId, changeInfo, tab);
        });
    }

    // 扩展安装/更新处理
    onInstalled(details) {
        console.log('扩展安装/更新:', details.reason);
        
        if (details.reason === 'install') {
            // 首次安装
            this.showWelcomePage();
            this.setupDefaultSettings();
        } else if (details.reason === 'update') {
            // 更新版本
            this.showUpdateNotification();
        }
    }

    // 处理消息
    handleMessage(message, sender, sendResponse) {
        const { action, data } = message;
        
        switch (action) {
            case 'extractComplete':
                this.handleExtractComplete(data, sender.tab?.id);
                sendResponse({ success: true });
                break;
                
            case 'getStoredData':
                this.getStoredData().then(data => {
                    sendResponse(data);
                });
                return true; // 异步响应
                
            case 'saveData':
                this.saveData(data).then(success => {
                    sendResponse({ success });
                });
                return true;
                
            case 'exportData':
                this.exportData(data).then(result => {
                    sendResponse(result);
                });
                return true;
                
            case 'getSettings':
                sendResponse({ settings: this.userSettings });
                break;
                
            case 'updateSettings':
                this.updateSettings(data).then(success => {
                    sendResponse({ success });
                });
                return true;
                
            case 'ping':
                sendResponse({ alive: true, timestamp: Date.now() });
                break;
                
            default:
                console.warn('未知消息类型:', action);
                sendResponse({ error: '未知操作' });
        }
    }

    // 处理提取完成
    async handleExtractComplete(data, tabId) {
        console.log('收到提取数据:', data.length, '条');
        
        // 保存数据
        this.currentData = data;
        await this.saveCurrentData();
        
        // 发送通知
        this.showExtractionNotification(data.length);
        
        // 如果标签页存在，可以发送消息给content script
        if (tabId) {
            chrome.tabs.sendMessage(tabId, {
                action: 'extractionSuccess',
                count: data.length
            });
        }
    }

    // 页面加载完成处理
    onPageLoaded(details) {
        const url = details.url;
        
        if (url.includes('whxunw.com')) {
            // 检测是否为目标页面
            if (this.isTargetPage(url)) {
                this.logPageVisit(url);
            }
        }
    }

    // 标签页更新处理
    onTabUpdated(tabId, changeInfo, tab) {
        if (changeInfo.status === 'complete' && tab.url?.includes('whxunw.com')) {
            // 页面加载完成，可以注入content script或执行其他操作
            if (this.isTargetPage(tab.url)) {
                // 这里可以发送消息给content script
                setTimeout(() => {
                    chrome.tabs.sendMessage(tabId, {
                        action: 'pageReady',
                        url: tab.url
                    });
                }, 1000);
            }
        }
    }

    // 判断是否为目标页面
    isTargetPage(url) {
        const targetPatterns = [
            '/assignments-detail',
            '/exam/',
            'courseware-study',
            'assignments'
        ];
        
        return targetPatterns.some(pattern => url.includes(pattern));
    }

    // 加载设置
    async loadSettings() {
        try {
            const result = await chrome.storage.local.get(['userSettings']);
            this.userSettings = result.userSettings || this.getDefaultSettings();
        } catch (error) {
            console.error('加载设置失败:', error);
            this.userSettings = this.getDefaultSettings();
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
            language: 'zh-CN'
        };
    }

    // 设置默认设置
    async setupDefaultSettings() {
        const defaultSettings = this.getDefaultSettings();
        await chrome.storage.local.set({ userSettings: defaultSettings });
        this.userSettings = defaultSettings;
    }

    // 更新设置
    async updateSettings(newSettings) {
        try {
            this.userSettings = { ...this.userSettings, ...newSettings };
            await chrome.storage.local.set({ userSettings: this.userSettings });
            return true;
        } catch (error) {
            console.error('更新设置失败:', error);
            return false;
        }
    }

    // 保存当前数据
    async saveCurrentData() {
        if (!this.currentData) return;
        
        try {
            // 保存到本地存储
            await chrome.storage.local.set({
                lastExtractedData: this.currentData,
                lastExtractionTime: Date.now()
            });
            
            // 如果启用了自动保存，保存到历史记录
            if (this.userSettings.autoSave) {
                await this.addToHistory(this.currentData);
            }
            
            console.log('数据保存成功');
        } catch (error) {
            console.error('保存数据失败:', error);
        }
    }

    // 获取存储的数据
    async getStoredData() {
        try {
            const result = await chrome.storage.local.get([
                'lastExtractedData',
                'extractionHistory',
                'questionBank'
            ]);
            
            return {
                lastData: result.lastExtractedData || [],
                history: result.extractionHistory || [],
                questionBank: result.questionBank || [],
                lastUpdate: result.lastExtractionTime || null
            };
        } catch (error) {
            console.error('获取存储数据失败:', error);
            return { lastData: [], history: [], questionBank: [] };
        }
    }

    // 保存数据
    async saveData(data) {
        try {
            this.currentData = data;
            await this.saveCurrentData();
            return true;
        } catch (error) {
            console.error('保存数据失败:', error);
            return false;
        }
    }

    // 导出数据
    async exportData({ data, format, filename }) {
        try {
            // 这里应该实现实际的导出逻辑
            // 为了简化，我们只返回成功状态
            console.log(`导出数据: ${data.length}条, 格式: ${format}, 文件名: ${filename}`);
            
            // 模拟导出成功
            return {
                success: true,
                message: `已导出 ${data.length} 条数据`,
                filename: filename || `xunwang_export_${Date.now()}.${format}`
            };
        } catch (error) {
            console.error('导出数据失败:', error);
            return {
                success: false,
                message: '导出失败: ' + error.message
            };
        }
    }

    // 添加到历史记录
    async addToHistory(data) {
        try {
            const result = await chrome.storage.local.get(['extractionHistory']);
            let history = result.extractionHistory || [];
            
            const historyItem = {
                timestamp: Date.now(),
                count: data.length,
                data: data.slice(0, 10), // 只保存前10条作为预览
                source: window.location?.href || 'unknown'
            };
            
            history.unshift(historyItem); // 添加到开头
            
            // 限制历史记录数量
            if (history.length > 50) {
                history = history.slice(0, 50);
            }
            
            await chrome.storage.local.set({ extractionHistory: history });
        } catch (error) {
            console.error('添加到历史记录失败:', error);
        }
    }

    // 初始化存储
    async initializeStorage() {
        const defaultStorage = {
            questionBank: [],
            extractionHistory: [],
            userSettings: this.userSettings,
            stats: {
                totalExtractions: 0,
                totalQuestions: 0,
                firstUse: Date.now(),
                lastUse: Date.now()
            }
        };
        
        // 检查并初始化必要的存储项
        const current = await chrome.storage.local.get(null);
        const toSet = {};
        
        for (const [key, defaultValue] of Object.entries(defaultStorage)) {
            if (current[key] === undefined) {
                toSet[key] = defaultValue;
            }
        }
        
        if (Object.keys(toSet).length > 0) {
            await chrome.storage.local.set(toSet);
        }
    }

    // 显示欢迎页面
    showWelcomePage() {
        chrome.tabs.create({
            url: chrome.runtime.getURL('welcome/welcome.html')
        });
    }

    // 显示更新通知
    showUpdateNotification() {
        if (this.userSettings.notificationEnabled) {
            chrome.notifications.create({
                type: 'basic',
                iconUrl: chrome.runtime.getURL('icons/icon128.png'),
                title: '讯网答案提取器已更新',
                message: '新版本已安装，点击查看更新内容',
                priority: 2
            });
        }
    }

    // 显示提取成功通知
    showExtractionNotification(count) {
        if (this.userSettings.notificationEnabled && count > 0) {
            chrome.notifications.create({
                type: 'basic',
                iconUrl: chrome.runtime.getURL('icons/icon128.png'),
                title: '答案提取完成',
                message: `成功提取 ${count} 条题目答案`,
                priority: 1
            });
        }
    }

    // 记录页面访问
    logPageVisit(url) {
        // 这里可以记录用户访问统计
        console.log('访问讯网页面:', url);
    }

    // 检查更新
    async checkForUpdates() {
        // 这里可以实现检查插件更新的逻辑
        // 为了简化，我们只记录检查时间
        await chrome.storage.local.set({
            lastUpdateCheck: Date.now()
        });
    }
}

// 启动后台服务
const backgroundService = new XunWangBackgroundService();

// 导出给测试使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = XunWangBackgroundService;
}

// 错误处理
window.addEventListener('error', (event) => {
    console.error('后台脚本错误:', event.error);
    
    // 可以在这里添加错误上报逻辑
    chrome.storage.local.get(['errorLogs']).then(result => {
        const errorLogs = result.errorLogs || [];
        errorLogs.push({
            timestamp: Date.now(),
            error: event.error?.message || 'Unknown error',
            stack: event.error?.stack
        });
        
        // 限制错误日志数量
        if (errorLogs.length > 100) {
            errorLogs.splice(0, errorLogs.length - 100);
        }
        
        chrome.storage.local.set({ errorLogs });
    });
});

// 卸载清理
chrome.runtime.onSuspend.addListener(() => {
    console.log('后台服务即将挂起');
    // 执行清理操作
});

console.log('讯网答案提取器后台服务已启动');