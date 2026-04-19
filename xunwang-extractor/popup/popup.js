/**
 * 讯网题目答案提取器 - 弹出窗口主逻辑
 * 负责用户交互、数据展示和后台通信
 */

class XunwangPopupApp {
  constructor() {
    this.state = {
      isReady: false,
      hasWhxunwTab: false,
      currentTab: null,
      currentData: null,
      extractionHistory: [],
      settings: {},
      isExtracting: false,
      extractionProgress: 0
    };
    
    this.uiElements = {};
    this.init();
  }

  async init() {
    this.log('弹出窗口初始化');
    
    // 初始化UI引用
    this.initUIElements();
    
    // 初始化事件监听
    this.initEventListeners();
    
    // 加载初始数据
    await this.loadInitialData();
    
    // 更新UI状态
    this.updateUI();
    
    this.state.isReady = true;
    this.log('弹出窗口初始化完成');
  }

  log(...args) {
    console.log('[XunwangPopup]', ...args);
  }

  error(...args) {
    console.error('[XunwangPopup]', ...args);
  }

  // 初始化UI元素引用
  initUIElements() {
    // 状态显示
    this.uiElements.platformIndicator = document.getElementById('platformIndicator');
    this.uiElements.platformText = document.getElementById('platformText');
    this.uiElements.pageIndicator = document.getElementById('pageIndicator');
    this.uiElements.pageText = document.getElementById('pageText');
    this.uiElements.cacheIndicator = document.getElementById('cacheIndicator');
    this.uiElements.cacheText = document.getElementById('cacheText');
    
    // 课程信息
    this.uiElements.courseInfoCard = document.getElementById('courseInfoCard');
    this.uiElements.courseName = document.getElementById('courseName');
    this.uiElements.assignmentName = document.getElementById('assignmentName');
    this.uiElements.questionCount = document.getElementById('questionCount');
    this.uiElements.extractTime = document.getElementById('extractTime');
    
    // 操作按钮
    this.uiElements.extractBtn = document.getElementById('extractBtn');
    this.uiElements.exportBtn = document.getElementById('exportBtn');
    this.uiElements.historyBtn = document.getElementById('historyBtn');
    this.uiElements.settingsBtn = document.getElementById('settingsBtn');
    
    // 进度显示
    this.uiElements.progressCard = document.getElementById('progressCard');
    this.uiElements.progressFill = document.getElementById('progressFill');
    this.uiElements.progressText = document.getElementById('progressText');
    this.uiElements.progressDetails = document.getElementById('progressDetails');
    
    // 预览区域
    this.uiElements.previewCard = document.getElementById('previewCard');
    this.uiElements.previewContent = document.getElementById('previewContent');
    this.uiElements.emptyPreview = document.getElementById('emptyPreview');
    this.uiElements.previewTable = document.getElementById('previewTable');
    this.uiElements.previewTableBody = document.getElementById('previewTableBody');
    this.uiElements.togglePreview = document.getElementById('togglePreview');
    this.uiElements.viewAllBtn = document.getElementById('viewAllBtn');
    this.uiElements.clearPreviewBtn = document.getElementById('clearPreviewBtn');
    
    // 底部信息
    this.uiElements.lastUpdate = document.getElementById('lastUpdate');
    this.uiElements.dataCount = document.getElementById('dataCount');
    
    // 链接按钮
    this.uiElements.helpBtn = document.getElementById('helpBtn');
    this.uiElements.feedbackBtn = document.getElementById('feedbackBtn');
    this.uiElements.aboutBtn = document.getElementById('aboutBtn');
    
    // 通知区域
    this.uiElements.notificationArea = document.getElementById('notificationArea');
  }

  // 初始化事件监听器
  initEventListeners() {
    // 主操作按钮
    this.uiElements.extractBtn.addEventListener('click', () => this.startExtraction());
    this.uiElements.exportBtn.addEventListener('click', () => this.exportData());
    this.uiElements.historyBtn.addEventListener('click', () => this.showHistory());
    this.uiElements.settingsBtn.addEventListener('click', () => this.showSettings());
    
    // 预览区域控制
    this.uiElements.togglePreview.addEventListener('click', () => this.togglePreview());
    this.uiElements.viewAllBtn.addEventListener('click', () => this.showFullData());
    this.uiElements.clearPreviewBtn.addEventListener('click', () => this.clearPreview());
    
    // 底部链接
    this.uiElements.helpBtn.addEventListener('click', (e) => {
      e.preventDefault();
      this.showHelp();
    });
    
    this.uiElements.feedbackBtn.addEventListener('click', (e) => {
      e.preventDefault();
      this.showFeedback();
    });
    
    this.uiElements.aboutBtn.addEventListener('click', (e) => {
      e.preventDefault();
      this.showAbout();
    });
    
    // 监听来自后台的消息
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      this.handleBackgroundMessage(request, sendResponse);
    });
  }

  // 加载初始数据
  async loadInitialData() {
    try {
      // 检查当前标签页
      await this.checkCurrentTab();
      
      // 获取系统状态
      const status = await this.sendMessage({ action: 'getStatus' });
      if (status.success) {
        this.state.systemStatus = status.data;
      }
      
      // 获取历史记录
      const history = await this.sendMessage({ action: 'getHistory' });
      if (history.success) {
        this.state.extractionHistory = history.data;
      }
      
      // 获取设置
      const settings = await this.sendMessage({ action: 'getSettings' });
      if (settings.success) {
        this.state.settings = settings.data;
      }
      
      // 获取最近一次提取的数据
      if (this.state.extractionHistory.length > 0) {
        const latest = this.state.extractionHistory[0];
        this.state.currentData = latest.data;
        this.updateDataPreview(latest.data);
      }
      
    } catch (error) {
      this.error('加载初始数据失败:', error);
    }
  }

  // 检查当前标签页
  async checkCurrentTab() {
    try {
      const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
      
      if (tabs.length > 0) {
        this.state.currentTab = tabs[0];
        this.state.hasWhxunwTab = tabs[0].url?.includes('whxunw.com') || false;
      }
      
      return this.state.currentTab;
    } catch (error) {
      this.error('检查标签页失败:', error);
      return null;
    }
  }

  // 发送消息到后台
  async sendMessage(message) {
    return new Promise((resolve, reject) => {
      chrome.runtime.sendMessage(message, (response) => {
        if (chrome.runtime.lastError) {
          reject(new Error(chrome.runtime.lastError.message));
        } else {
          resolve(response);
        }
      });
    });
  }

  // 处理后台消息
  handleBackgroundMessage(request, sendResponse) {
    this.log('收到后台消息:', request);
    
    switch (request.event) {
      case 'page_ready':
        this.onPageReady(request.data);
        break;
        
      case 'data_ready':
        this.onDataReady(request.data);
        break;
    }
    
    sendResponse({ received: true });
  }

  // 页面就绪事件
  onPageReady(data) {
    this.log('讯网页面已就绪:', data);
    this.state.hasWhxunwTab = true;
    this.updateUI();
  }

  // 数据就绪事件
  async onDataReady(data) {
    this.log('新数据已就绪');
    
    // 重新加载历史记录
    const history = await this.sendMessage({ action: 'getHistory' });
    if (history.success) {
      this.state.extractionHistory = history.data;
      const latest = this.state.extractionHistory[0];
      this.state.currentData = latest.data;
      this.updateDataPreview(latest.data);
      this.showNotification('数据提取完成', 'success');
    }
    
    // 结束提取状态
    this.state.isExtracting = false;
    this.updateUI();
  }

  // 开始提取
  async startExtraction() {
    if (this.state.isExtracting) {
      this.showNotification('正在提取中，请稍候...', 'info');
      return;
    }

    if (!this.state.hasWhxunwTab) {
      this.showNotification('请先打开讯网教学云平台页面', 'warning');
      return;
    }

    try {
      this.state.isExtracting = true;
      this.state.extractionProgress = 0;
      this.updateUI();
      
      this.showProgress('正在连接页面...', 10);
      
      // 开始提取
      const result = await this.sendMessage({ action: 'extractFromCurrentTab' });
      
      if (result.success) {
        this.showProgress('数据处理中...', 80);
        
        // 等待数据保存完成
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        this.showProgress('完成', 100);
        
        // 更新预览
        this.updateDataPreview(result.data);
        this.showNotification('提取成功！', 'success');
        
      } else {
        this.showNotification(`提取失败: ${result.error}`, 'error');
      }
      
    } catch (error) {
      this.error('提取过程中出错:', error);
      this.showNotification(`提取失败: ${error.message}`, 'error');
      
    } finally {
      // 延迟隐藏进度条
      setTimeout(() => {
        this.state.isExtracting = false;
        this.updateUI();
      }, 1000);
    }
  }

  // 显示进度
  showProgress(text, percent) {
    this.state.extractionProgress = percent;
    this.uiElements.progressText.textContent = text;
    this.uiElements.progressFill.style.width = `${percent}%`;
    
    if (percent === 100) {
      this.uiElements.progressDetails.textContent = '准备就绪';
    }
  }

  // 导出数据
  async exportData() {
    if (!this.state.currentData) {
      this.showNotification('没有可导出的数据', 'warning');
      return;
    }

    try {
      this.showNotification('正在准备导出...', 'info');
      
      // 默认导出为Excel
      const result = await this.sendMessage({
        action: 'exportData',
        data: this.state.currentData,
        format: 'excel'
      });
      
      if (result.success) {
        this.showNotification(`导出成功: ${result.data.filename}`, 'success');
      } else {
        this.showNotification(`导出失败: ${result.error}`, 'error');
      }
      
    } catch (error) {
      this.error('导出失败:', error);
      this.showNotification(`导出失败: ${error.message}`, 'error');
    }
  }

  // 显示历史记录
  async showHistory() {
    try {
      const history = await this.sendMessage({ action: 'getHistory' });
      
      if (history.success && history.data.length > 0) {
        // 创建历史记录模态框
        this.showModal({
          title: '提取历史记录',
          content: this.renderHistoryList(history.data),
          size: 'large'
        });
      } else {
        this.showNotification('暂无历史记录', 'info');
      }
      
    } catch (error) {
      this.error('获取历史记录失败:', error);
      this.showNotification('获取历史记录失败', 'error');
    }
  }

  // 渲染历史记录列表
  renderHistoryList(history) {
    const list = document.createElement('div');
    list.className = 'history-list';
    
    history.forEach((record, index) => {
      const item = document.createElement('div');
      item.className = 'history-item';
      item.innerHTML = `
        <div class="history-header">
          <span class="history-index">#${index + 1}</span>
          <span class="history-course">${record.courseName}</span>
          <span class="history-time">${new Date(record.timestamp).toLocaleString()}</span>
        </div>
        <div class="history-details">
          <span>作业: ${record.assignmentName}</span>
          <span>题目: ${record.questionCount} 题</span>
          <button class="btn-small load-history-btn" data-key="${record.key}">
            <i class="fas fa-eye"></i> 查看
          </button>
        </div>
      `;
      
      list.appendChild(item);
    });
    
    // 添加加载按钮事件
    setTimeout(() => {
      list.querySelectorAll('.load-history-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
          const key = e.target.dataset.key;
          this.loadHistoryRecord(key);
        });
      });
    }, 100);
    
    return list;
  }

  // 加载历史记录
  async loadHistoryRecord(key) {
    // 在实际实现中，需要从存储中获取数据
    this.showNotification('加载历史记录功能开发中...', 'info');
  }

  // 显示设置
  async showSettings() {
    try {
      const settings = await this.sendMessage({ action: 'getSettings' });
      
      if (settings.success) {
        this.showModal({
          title: '插件设置',
          content: this.renderSettingsForm(settings.data),
          onConfirm: (data) => this.saveSettings(data)
        });
      }
      
    } catch (error) {
      this.error('获取设置失败:', error);
    }
  }

  // 渲染设置表单
  renderSettingsForm(settings) {
    const form = document.createElement('form');
    form.className = 'settings-form';
    form.innerHTML = `
      <div class="form-group">
        <label>
          <input type="checkbox" name="autoExtract" ${settings.autoExtract ? 'checked' : ''}>
          自动提取（页面加载时）
        </label>
      </div>
      
      <div class="form-group">
        <label>
          <input type="checkbox" name="autoSave" ${settings.autoSave ? 'checked' : ''}>
          自动保存提取数据
        </label>
      </div>
      
      <div class="form-group">
        <label>
          <input type="checkbox" name="notifications" ${settings.notifications ? 'checked' : ''}>
          显示通知
        </label>
      </div>
      
      <div class="form-group">
        <label>
          <input type="checkbox" name="debugMode" ${settings.debugMode ? 'checked' : ''}>
          调试模式
        </label>
      </div>
      
      <div class="form-group">
        <label>导出格式:</label>
        <select name="exportFormat">
          <option value="excel" ${settings.exportFormat === 'excel' ? 'selected' : ''}>Excel (.xlsx)</option>
          <option value="csv" ${settings.exportFormat === 'csv' ? 'selected' : ''}>CSV (.csv)</option>
          <option value="json" ${settings.exportFormat === 'json' ? 'selected' : ''}>JSON (.json)</option>
        </select>
      </div>
      
      <div class="form-group">
        <label>历史记录保留:</label>
        <input type="number" name="maxHistory" value="${settings.maxHistory}" min="10" max="1000">
        <span class="form-hint">条</span>
      </div>
    `;
    
    return form;
  }

  // 保存设置
  async saveSettings(data) {
    try {
      const result = await this.sendMessage({
        action: 'updateSettings',
        settings: data
      });
      
      if (result.success) {
        this.state.settings = { ...this.state.settings, ...data };
        this.showNotification('设置已保存', 'success');
      }
      
    } catch (error) {
      this.error('保存设置失败:', error);
      this.showNotification('保存设置失败', 'error');
    }
  }

  // 切换预览区域
  togglePreview() {
    const isExpanded = this.uiElements.previewContent.style.maxHeight !== '0px';
    
    if (isExpanded) {
      this.uiElements.previewContent.style.maxHeight = '0px';
      this.uiElements.togglePreview.innerHTML = '<i class="fas fa-chevron-down"></i>';
    } else {
      this.uiElements.previewContent.style.maxHeight = '500px';
      this.uiElements.togglePreview.innerHTML = '<i class="fas fa-chevron-up"></i>';
    }
  }

  // 更新数据预览
  updateDataPreview(data) {
    if (!data || !data.questions || data.questions.length === 0) {
      this.uiElements.emptyPreview.style.display = 'block';
      this.uiElements.previewTable.style.display = 'none';
      this.uiElements.courseInfoCard.style.display = 'none';
      return;
    }

    // 显示课程信息
    this.uiElements.courseName.textContent = data.courseInfo?.courseName || '未知课程';
    this.uiElements.assignmentName.textContent = data.courseInfo?.assignmentName || '未知作业';
    this.uiElements.questionCount.textContent = data.questions.length;
    this.uiElements.extractTime.textContent = new Date(data.extractedAt).toLocaleString();
    this.uiElements.courseInfoCard.style.display = 'block';

    // 生成预览表格
    this.renderPreviewTable(data.questions.slice(0, 5)); // 只显示前5条
    
    // 更新UI状态
    this.uiElements.emptyPreview.style.display = 'none';
    this.uiElements.previewTable.style.display = 'block';
    this.uiElements.exportBtn.disabled = false;
    
    // 更新底部信息
    this.uiElements.dataCount.textContent = `数据: ${data.questions.length} 条`;
    this.uiElements.lastUpdate.textContent = `最后更新: ${new Date().toLocaleTimeString()}`;
  }

  // 渲染预览表格
  renderPreviewTable(questions) {
    const tbody = this.uiElements.previewTableBody;
    tbody.innerHTML = '';
    
    questions.forEach((question, index) => {
      const row = document.createElement('tr');
      
      const content = question.content.length > 50 
        ? question.content.substring(0, 50) + '...' 
        : question.content;
      
      row.innerHTML = `
        <td>${question.number || question.id}</td>
        <td title="${question.content}">${content}</td>
        <td>${question.answer || '未提取'}</td>
      `;
      
      tbody.appendChild(row);
    });
  }

  // 显示完整数据
  showFullData() {
    if (!this.state.currentData) return;
    
    this.showModal({
      title: `完整数据 - ${this.state.currentData.questions.length} 条题目`,
      content: this.renderFullDataTable(this.state.currentData.questions),
      size: 'extra-large'
    });
  }

  // 渲染完整数据表格
  renderFullDataTable(questions) {
    const container = document.createElement('div');
    container.className = 'full-data-table';
    
    const table = document.createElement('table');
    table.innerHTML = `
      <thead>
        <tr>
          <th>序号</th>
          <th>题目内容</th>
          <th>题目类型</th>
          <th>选项A</th>
          <th>选项B</th>
          <th>选项C</th>
          <th>选项D</th>
          <th>正确答案</th>
        </tr>
      </thead>
      <tbody>
        ${questions.map((question, index) => `
          <tr>
            <td>${question.number || question.id}</td>
            <td title="${question.content}">${question.content.substring(0, 100)}...</td>
            <td>${question.type}</td>
            <td>${question.options[0]?.text || ''}</td>
            <td>${question.options[1]?.text || ''}</td>
            <td>${question.options[2]?.text || ''}</td>
            <td>${question.options[3]?.text || ''}</td>
            <td><strong>${question.answer || ''}</strong></td>
          </tr>
        `).join('')}
      </tbody>
    `;
    
    container.appendChild(table);
    return container;
  }

  // 清空预览
  clearPreview() {
    this.state.currentData = null;
    this.updateDataPreview(null);
    this.showNotification('预览已清空', 'info');
  }

  // 显示帮助
  showHelp() {
    this.showModal({
      title: '使用帮助',
      content: `
        <div class="help-content">
          <h4>使用步骤:</h4>
          <ol>
            <li>登录讯网教学云平台</li>
            <li>进入【网络助学 → 平时作业 → 作业记录 → 详情】</li>
            <li>点击"一键提取答案"按钮</li>
            <li>等待提取完成，查看预览数据</li>
            <li>点击"导出数据"保存为Excel/CSV格式</li>
          </ol>
          
          <h4>常见问题:</h4>
          <ul>
            <li><strong>提取不到数据？</strong> 确保页面完全加载，刷新后重试</li>
            <li><strong>答案不完整？</strong> 部分题目可能需要手动查看</li>
            <li><strong>导出失败？</strong> 检查文件保存权限</li>
          </ul>
          
          <h4>注意事项:</h4>
          <ul>
            <li>本插件仅用于学习目的</li>
            <li>请遵守平台使用规则</li>
            <li>数据仅存储在本地，不会上传</li>
          </ul>
        </div>
      `
    });
  }

  // 显示反馈
  showFeedback() {
    this.showModal({
      title: '问题反馈',
      content: `
        <div class="feedback-content">
          <p>如果您在使用过程中遇到问题，或者有改进建议，请通过以下方式反馈:</p>
          
          <div class="contact-info">
            <p><i class="fas fa-envelope"></i> 邮箱: feedback@example.com</p>
            <p><i class="fas fa-comment"></i> 用户群: 扫描二维码加入</p>
            <div class="qr-code-placeholder">
              <div style="width: 150px; height: 150px; background: #f0f0f0; display: flex; align-items: center; justify-content: center; margin: 10px auto;">
                <span style="color: #666;">QQ群二维码</span>
              </div>
            </div>
          </div>
          
          <div class="feedback-form">
            <h4>快速反馈:</h4>
            <textarea placeholder="请描述您遇到的问题或建议..." rows="4" style="width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ddd;"></textarea>
            <button class="btn-primary" style="margin-top: 10px;">提交反馈</button>
          </div>
        </div>
      `
    });
  }

  // 显示关于
  showAbout() {
    this.showModal({
      title: '关于插件',
      content: `
        <div class="about-content">
          <div class="about-header">
            <div class="about-logo" style="width: 80px; height: 80px; background: linear-gradient(135deg, #2563eb, #8b5cf6); border-radius: 16px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px;">
              <i class="fas fa-graduation-cap" style="color: white; font-size: 40px;"></i>
            </div>
            <h3 style="text-align: center; margin-bottom: 5px;">讯网题目答案提取器</h3>
            <p style="text-align: center; color: #666; margin-bottom: 20px;">v1.0.0</p>
          </div>
          
          <div class="about-info">
            <p><strong>插件功能:</strong> 一键提取讯网教学云平台的题目和标准答案，支持导出为多种格式。</p>
            
            <p><strong>适用场景:</strong></p>
            <ul>
              <li>学习复习</li>
              <li>补考准备</li>
              <li>题库整理</li>
            </ul>
            
            <p><strong>技术特点:</strong></p>
            <ul>
              <li>本地数据存储，保护隐私</li>
              <li>支持多种题目类型</li>
              <li>智能数据解析</li>
              <li>批量导出功能</li>
            </ul>
            
            <p><strong>免责声明:</strong> 本插件仅供学习使用，请遵守平台规定，合理使用。</p>
            
            <p style="text-align: center; margin-top: 20px; color: #888; font-size: 12px;">
              © 2026 讯网答案提取器 | 典哥AI助手开发
            </p>
          </div>
        </div>
      `
    });
  }

  // 显示通知
  showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
      <div class="notification-content">
        <i class="fas ${this.getNotificationIcon(type)}"></i>
        <span>${message}</span>
      </div>
    `;
    
    this.uiElements.notificationArea.appendChild(notification);
    
    // 自动消失
    setTimeout(() => {
      notification.style.opacity = '0';
      notification.style.transform = 'translateY(-10px)';
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification);
        }
      }, 300);
    }, 3000);
  }

  // 获取通知图标
  getNotificationIcon(type) {
    const icons = {
      success: 'fa-check-circle',
      error: 'fa-exclamation-circle',
      warning: 'fa-exclamation-triangle',
      info: 'fa-info-circle'
    };
    return icons[type] || 'fa-info-circle';
  }

  // 显示模态框
  showModal(options) {
    // 在实际实现中，这里需要创建模态框DOM
    this.log('显示模态框:', options);
    this.showNotification(`功能开发中: ${options.title}`, 'info');
  }

  // 更新UI状态
  updateUI() {
    // 更新平台状态
    this.updatePlatformStatus();
    
    // 更新页面状态
    this.updatePageStatus();
    
    // 更新缓存状态
    this.updateCacheStatus();
    
    // 更新按钮状态
    this.updateButtonStates();
    
    // 更新进度显示
    this.updateProgressDisplay();
  }

  // 更新平台状态
  updatePlatformStatus() {
    const isConnected = this.state.isReady;
    this.uiElements.platformIndicator.className = 'status-indicator';
    this.uiElements.platformIndicator.classList.add(isConnected ? 'success' : 'warning');
    this.uiElements.platformText.textContent = isConnected ? '已连接' : '初始化中';
  }

  // 更新页面状态
  updatePageStatus() {
    const hasPage = this.state.hasWhxunwTab;
    this.uiElements.pageIndicator.className = 'status-indicator';
    this.uiElements.pageIndicator.classList.add(hasPage ? 'success' : 'warning');
    this.uiElements.pageText.textContent = hasPage 
      ? '检测到讯网页面' 
      : '请打开讯网页面';
  }

  // 更新缓存状态
  updateCacheStatus() {
    const count = this.state.extractionHistory.length;
    this.uiElements.cacheIndicator.className = 'status-indicator';
    this.uiElements.cacheIndicator.classList.add(count > 0 ? 'success' : 'info');
    this.uiElements.cacheText.textContent = `${count} 条记录`;
  }

  // 更新按钮状态
  updateButtonStates() {
    const { hasWhxunwTab, isExtracting, currentData } = this.state;
    
    // 提取按钮
    this.uiElements.extractBtn.disabled = isExtracting || !hasWhxunwTab;
    
    // 导出按钮
    this.uiElements.exportBtn.disabled = !currentData || isExtracting;
    
    // 如果正在提取，显示进度卡片
    if (isExtracting) {
      this.uiElements.progressCard.style.display = 'block';
    } else {
      this.uiElements.progressCard.style.display = 'none';
    }
  }

  // 更新进度显示
  updateProgressDisplay() {
    if (this.state.isExtracting) {
      this.uiElements.progressFill.style.width = `${this.state.extractionProgress}%`;
    }
  }
}

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
  window.xunwangApp = new XunwangPopupApp();
});