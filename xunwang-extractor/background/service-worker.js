/**
 * 讯网题目答案提取器 - Service Worker
 * 后台脚本，负责消息中转、数据存储和导出功能
 */

class XunwangBackgroundService {
  constructor() {
    this.config = {
      storageKey: 'xunwang_extractor_data',
      maxHistoryItems: 50,
      exportFormats: ['excel', 'csv', 'json']
    };
    
    this.dataCache = new Map();
    this.init();
  }

  init() {
    this.log('背景服务初始化');
    this.setupMessageHandlers();
    this.setupStorageListeners();
    this.restoreCache();
  }

  log(...args) {
    console.log('[XunwangBackground]', ...args);
  }

  error(...args) {
    console.error('[XunwangBackground]', ...args);
  }

  // 设置消息处理器
  setupMessageHandlers() {
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      this.log('收到消息:', request, '来自:', sender.tab?.url);
      
      // 处理来自弹出窗口的消息
      if (sender.tab?.id === undefined) {
        return this.handlePopupMessage(request, sendResponse);
      }
      
      // 处理来自内容脚本的消息
      return this.handleContentScriptMessage(request, sender, sendResponse);
    });

    // 监听标签页更新
    chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
      if (changeInfo.status === 'complete' && tab.url?.includes('whxunw.com')) {
        this.log('讯网页面加载完成:', tab.url);
        this.notifyPopup('page_ready', { url: tab.url, tabId });
      }
    });
  }

  // 处理弹出窗口消息
  handlePopupMessage(request, sendResponse) {
    switch (request.action) {
      case 'getStatus':
        this.getSystemStatus().then(status => 
          sendResponse({ success: true, data: status })
        );
        return true;

      case 'extractFromCurrentTab':
        this.extractFromCurrentTab().then(data =>
          sendResponse({ success: true, data })
        ).catch(error =>
          sendResponse({ success: false, error: error.message })
        );
        return true;

      case 'getHistory':
        this.getExtractionHistory().then(history =>
          sendResponse({ success: true, data: history })
        );
        return true;

      case 'exportData':
        this.exportData(request.data, request.format).then(result =>
          sendResponse({ success: true, data: result })
        ).catch(error =>
          sendResponse({ success: false, error: error.message })
        );
        return true;

      case 'clearCache':
        this.clearCache().then(() =>
          sendResponse({ success: true })
        );
        return true;

      case 'getSettings':
        this.getSettings().then(settings =>
          sendResponse({ success: true, data: settings })
        );
        return true;

      case 'updateSettings':
        this.updateSettings(request.settings).then(() =>
          sendResponse({ success: true })
        );
        return true;

      default:
        sendResponse({ success: false, error: '未知操作' });
        return false;
    }
  }

  // 处理内容脚本消息
  handleContentScriptMessage(request, sender, sendResponse) {
    switch (request.action) {
      case 'dataExtracted':
        this.saveExtractedData(request.data, sender.tab.id).then(() => {
          sendResponse({ success: true });
          this.notifyPopup('data_ready', { tabId: sender.tab.id });
        });
        return true;

      case 'ping':
        sendResponse({ status: 'connected', version: '1.0.0' });
        return true;

      default:
        sendResponse({ success: false, error: '未知操作' });
        return false;
    }
  }

  // 获取系统状态
  async getSystemStatus() {
    const [tabs, storage, settings] = await Promise.all([
      this.getWhxunwTabs(),
      this.getStorageInfo(),
      this.getSettings()
    ]);

    return {
      version: '1.0.0',
      timestamp: new Date().toISOString(),
      tabs: {
        total: tabs.length,
        active: tabs.filter(t => t.active).length,
        urls: tabs.map(t => t.url)
      },
      storage: {
        used: storage.bytesUsed,
        quota: storage.quota,
        items: storage.items
      },
      settings,
      cacheSize: this.dataCache.size
    };
  }

  // 获取讯网标签页
  async getWhxunwTabs() {
    const tabs = await chrome.tabs.query({ url: '*://*.whxunw.com/*' });
    return tabs.map(tab => ({
      id: tab.id,
      url: tab.url,
      title: tab.title,
      active: tab.active,
      windowId: tab.windowId
    }));
  }

  // 获取存储信息
  async getStorageInfo() {
    const data = await chrome.storage.local.get(null);
    const items = Object.keys(data).length;
    const bytesUsed = JSON.stringify(data).length;
    
    // 获取配额信息
    const quota = chrome.storage.local.QUOTA_BYTES || 5242880; // 5MB
    
    return { items, bytesUsed, quota };
  }

  // 从当前标签页提取数据
  async extractFromCurrentTab() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    if (!tab?.url?.includes('whxunw.com')) {
      throw new Error('当前标签页不是讯网教学云平台');
    }

    this.log(`从标签页 ${tab.id} 提取数据`);
    
    try {
      // 注入内容脚本（如果尚未注入）
      await this.ensureContentScriptInjected(tab.id);
      
      // 发送提取命令
      const response = await chrome.tabs.sendMessage(tab.id, { action: 'extractAll' });
      
      if (!response.success) {
        throw new Error(response.error || '提取失败');
      }
      
      // 保存数据
      await this.saveExtractedData(response.data, tab.id);
      
      return response.data;
    } catch (error) {
      this.error('提取失败:', error);
      
      // 如果消息发送失败，可能是内容脚本未加载
      if (error.message.includes('Could not establish connection')) {
        throw new Error('请刷新讯网页面后重试');
      }
      
      throw error;
    }
  }

  // 确保内容脚本已注入
  async ensureContentScriptInjected(tabId) {
    try {
      // 尝试发送ping消息检查内容脚本是否已加载
      await chrome.tabs.sendMessage(tabId, { action: 'ping' });
      return true;
    } catch (error) {
      this.log('内容脚本未加载，尝试注入');
      
      // 注入内容脚本
      await chrome.scripting.executeScript({
        target: { tabId },
        files: ['content/content-script.js']
      });
      
      // 等待内容脚本初始化
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      return true;
    }
  }

  // 保存提取的数据
  async saveExtractedData(data, tabId) {
    const key = `extraction_${Date.now()}`;
    const extractionRecord = {
      key,
      data,
      tabId,
      timestamp: new Date().toISOString(),
      url: data.url,
      courseName: data.courseInfo?.courseName || '未知课程',
      assignmentName: data.courseInfo?.assignmentName || '未知作业',
      questionCount: data.questions?.length || 0
    };

    // 保存到缓存
    this.dataCache.set(key, extractionRecord);
    
    // 保存到存储
    await chrome.storage.local.set({
      [key]: extractionRecord,
      last_extraction: extractionRecord
    });

    // 更新历史记录
    await this.updateHistory(extractionRecord);

    this.log(`数据已保存: ${key}, 题目数: ${extractionRecord.questionCount}`);
    
    return extractionRecord;
  }

  // 更新历史记录
  async updateHistory(record) {
    const history = await this.getExtractionHistory();
    
    // 添加新记录到开头
    history.unshift(record);
    
    // 限制历史记录数量
    if (history.length > this.config.maxHistoryItems) {
      history.length = this.config.maxHistoryItems;
    }
    
    // 保存历史记录
    await chrome.storage.local.set({ extraction_history: history });
    
    return history;
  }

  // 获取提取历史
  async getExtractionHistory() {
    const result = await chrome.storage.local.get('extraction_history');
    return result.extraction_history || [];
  }

  // 导出数据
  async exportData(data, format = 'excel') {
    this.log(`导出数据为 ${format} 格式`);
    
    switch (format.toLowerCase()) {
      case 'excel':
        return this.exportToExcel(data);
      case 'csv':
        return this.exportToCSV(data);
      case 'json':
        return this.exportToJSON(data);
      default:
        throw new Error(`不支持的导出格式: ${format}`);
    }
  }

  // 导出为Excel
  async exportToExcel(data) {
    // 这里需要加载 SheetJS 库
    // 在实际实现中，需要动态加载 xlsx.min.js
    // 简化版本：导出为CSV，用户可以用Excel打开
    
    const csvContent = this.convertToCSV(data);
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    
    const filename = `讯网答案_${data.courseInfo?.courseName || '未命名'}_${new Date().toISOString().slice(0, 10)}.csv`;
    
    // 使用 downloads API 下载文件
    await chrome.downloads.download({
      url: url,
      filename: filename,
      saveAs: true
    });

    // 清理URL
    setTimeout(() => URL.revokeObjectURL(url), 1000);

    return { 
      success: true, 
      filename, 
      format: 'csv',
      note: '完整Excel导出功能需要加载SheetJS库' 
    };
  }

  // 导出为CSV
  async exportToCSV(data) {
    const csvContent = this.convertToCSV(data);
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    
    const filename = `讯网答案_${data.courseInfo?.courseName || '未命名'}_${new Date().toISOString().slice(0, 10)}.csv`;
    
    await chrome.downloads.download({
      url: url,
      filename: filename,
      saveAs: true
    });

    setTimeout(() => URL.revokeObjectURL(url), 1000);

    return { success: true, filename, format: 'csv' };
  }

  // 导出为JSON
  async exportToJSON(data) {
    const jsonContent = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonContent], { type: 'application/json;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    
    const filename = `讯网答案_${data.courseInfo?.courseName || '未命名'}_${new Date().toISOString().slice(0, 10)}.json`;
    
    await chrome.downloads.download({
      url: url,
      filename: filename,
      saveAs: true
    });

    setTimeout(() => URL.revokeObjectURL(url), 1000);

    return { success: true, filename, format: 'json' };
  }

  // 转换为CSV格式
  convertToCSV(data) {
    const headers = ['序号', '题目内容', '题目类型', '选项A', '选项B', '选项C', '选项D', '正确答案'];
    const rows = [headers];

    data.questions?.forEach((question, index) => {
      const row = [
        question.number || question.id,
        `"${question.content.replace(/"/g, '""')}"`,
        question.type,
        ...this.formatOptionsForCSV(question.options),
        question.answer || '未知'
      ];
      rows.push(row);
    });

    // 添加元数据
    const metaRows = [
      [],
      ['讯网题目答案提取报告'],
      [`提取时间: ${data.extractedAt}`],
      [`课程名称: ${data.courseInfo?.courseName || '未知'}`],
      [`作业名称: ${data.courseInfo?.assignmentName || '未知'}`],
      [`题目总数: ${data.questions?.length || 0}`],
      []
    ];

    return [...metaRows, ...rows].map(row => row.join(',')).join('\n');
  }

  // 格式化选项为CSV
  formatOptionsForCSV(options) {
    const formatted = ['', '', '', ''];
    
    options?.forEach((opt, index) => {
      if (index < 4) {
        const prefix = opt.isCorrect ? '✓ ' : '';
        formatted[index] = `"${prefix}${opt.letter}. ${opt.text.replace(/"/g, '""')}"`;
      }
    });
    
    return formatted;
  }

  // 清理缓存
  async clearCache() {
    this.dataCache.clear();
    await chrome.storage.local.clear();
    this.log('缓存已清理');
    return true;
  }

  // 获取设置
  async getSettings() {
    const result = await chrome.storage.local.get('settings');
    const defaultSettings = {
      autoExtract: false,
      autoSave: true,
      exportFormat: 'excel',
      maxHistory: 50,
      notifications: true,
      debugMode: false
    };
    
    return { ...defaultSettings, ...result.settings };
  }

  // 更新设置
  async updateSettings(newSettings) {
    const currentSettings = await this.getSettings();
    const updatedSettings = { ...currentSettings, ...newSettings };
    
    await chrome.storage.local.set({ settings: updatedSettings });
    this.log('设置已更新:', updatedSettings);
    
    return updatedSettings;
  }

  // 通知弹出窗口
  notifyPopup(event, data) {
    // 在实际实现中，这里可以使用chrome.runtime.sendMessage
    // 或者存储事件数据供弹出窗口轮询
    this.log(`发送通知: ${event}`, data);
    
    // 存储最新事件
    chrome.storage.local.set({ last_event: { event, data, timestamp: Date.now() } });
  }

  // 设置存储监听器
  setupStorageListeners() {
    chrome.storage.onChanged.addListener((changes, namespace) => {
      if (namespace === 'local') {
        this.log('存储发生变化:', Object.keys(changes));
      }
    });
  }

  // 恢复缓存
  async restoreCache() {
    const data = await chrome.storage.local.get(null);
    
    Object.entries(data).forEach(([key, value]) => {
      if (key.startsWith('extraction_')) {
        this.dataCache.set(key, value);
      }
    });
    
    this.log(`缓存已恢复, ${this.dataCache.size} 条记录`);
  }
}

// 初始化服务
const service = new XunwangBackgroundService();

// 导出全局对象供调试
window.xunwangService = service;