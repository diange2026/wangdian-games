/**
 * 讯网题目答案提取器 - 内容脚本
 * 在讯网教学云平台页面运行，负责提取题目和答案数据
 */

class XunwangAnswerExtractor {
  constructor() {
    this.config = {
      debug: true,
      maxRetries: 3,
      retryDelay: 1000
    };
    
    this.data = {
      platform: '讯网教学云平台',
      url: window.location.href,
      extractedAt: new Date().toISOString(),
      courseInfo: {},
      questions: []
    };
    
    this.init();
  }

  init() {
    this.log('讯网答案提取器初始化');
    this.setupMessageListener();
    this.observePageChanges();
  }

  log(...args) {
    if (this.config.debug) {
      console.log('[XunwangExtractor]', ...args);
    }
  }

  error(...args) {
    console.error('[XunwangExtractor]', ...args);
  }

  // 设置消息监听器
  setupMessageListener() {
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      this.log('收到消息:', request);
      
      switch (request.action) {
        case 'ping':
          sendResponse({ status: 'ready', version: '1.0.0' });
          break;
          
        case 'extractPageInfo':
          this.extractPageInfo()
            .then(info => sendResponse({ success: true, data: info }))
            .catch(err => sendResponse({ success: false, error: err.message }));
          break;
          
        case 'extractQuestions':
          this.extractAllQuestions()
            .then(questions => sendResponse({ success: true, data: questions }))
            .catch(err => sendResponse({ success: false, error: err.message }));
          break;
          
        case 'extractAll':
          this.extractAllData()
            .then(data => sendResponse({ success: true, data }))
            .catch(err => sendResponse({ success: false, error: err.message }));
          break;
          
        default:
          sendResponse({ success: false, error: '未知操作' });
      }
      
      return true; // 保持消息通道开放
    });
  }

  // 观察页面变化
  observePageChanges() {
    const observer = new MutationObserver((mutations) => {
      mutations.forEach(mutation => {
        if (mutation.addedNodes.length > 0) {
          this.log('页面DOM发生变化');
          // 可以在这里触发自动提取逻辑
        }
      });
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }

  // 提取页面基本信息
  async extractPageInfo() {
    this.log('开始提取页面信息');
    
    const info = {
      title: document.title,
      url: window.location.href,
      timestamp: new Date().toISOString()
    };

    // 尝试提取课程信息
    const courseSelectors = [
      '.course-name',
      '.course-title',
      '[class*="course"] h1',
      '[class*="course"] h2',
      '.ant-page-header-heading-title'
    ];

    for (const selector of courseSelectors) {
      const element = document.querySelector(selector);
      if (element && element.textContent.trim()) {
        info.courseName = element.textContent.trim();
        break;
      }
    }

    // 尝试提取作业信息
    const assignmentSelectors = [
      '.assignment-title',
      '.paper-title',
      '.exam-title',
      '.title',
      'h1',
      'h2',
      'h3'
    ];

    for (const selector of assignmentSelectors) {
      const element = document.querySelector(selector);
      if (element && element.textContent.trim() && element.textContent !== info.courseName) {
        info.assignmentName = element.textContent.trim();
        break;
      }
    }

    // 提取页面关键元素数量
    info.questionCount = this.countQuestions();
    info.hasAnswers = this.checkIfAnswersVisible();

    this.data.courseInfo = info;
    return info;
  }

  // 计算题目数量
  countQuestions() {
    const questionSelectors = [
      '.question-item',
      '.question-container',
      '.exam-question',
      '.topic-item',
      '[class*="question"]',
      '[class*="topic"]',
      'li:has(input[type="radio"])',
      'li:has(input[type="checkbox"])'
    ];

    let count = 0;
    questionSelectors.forEach(selector => {
      count += document.querySelectorAll(selector).length;
    });

    return count;
  }

  // 检查答案是否可见
  checkIfAnswersVisible() {
    const answerIndicators = [
      '.answer',
      '.correct-answer',
      '.answer-key',
      '.right-answer',
      '[class*="answer"]',
      '.option.correct',
      '.option.right',
      'input:checked',
      '[data-correct="true"]'
    ];

    return answerIndicators.some(selector => 
      document.querySelectorAll(selector).length > 0
    );
  }

  // 提取所有题目
  async extractAllQuestions() {
    this.log('开始提取所有题目');
    
    const questions = [];
    const questionElements = this.findQuestionElements();
    
    this.log(`找到 ${questionElements.length} 个题目元素`);
    
    for (let i = 0; i < questionElements.length; i++) {
      try {
        const question = await this.extractQuestion(questionElements[i], i + 1);
        if (question) {
          questions.push(question);
        }
        
        // 添加延迟，避免过快请求
        if (i < questionElements.length - 1) {
          await this.delay(100);
        }
      } catch (error) {
        this.error(`提取第 ${i + 1} 题失败:`, error);
      }
    }
    
    this.data.questions = questions;
    return questions;
  }

  // 查找题目元素
  findQuestionElements() {
    const selectors = [
      // 结构化题目元素
      '.question-item',
      '.question-container',
      '.exam-question',
      '.topic-item',
      '.question-box',
      '.question-card',
      
      // 通用选择器
      'div[class*="question"]',
      'li[class*="question"]',
      'div[class*="topic"]',
      'li[class*="topic"]',
      
      // 列表项中的题目
      'li:has(> input[type="radio"])',
      'li:has(> input[type="checkbox"])',
      'li:has(> label:has(input[type="radio"]))',
      'li:has(> label:has(input[type="checkbox"]))',
      
      // 题目编号
      'div:has(> span:matches(\\d+[\.\\)]))',
      'li:has(> span:matches(\\d+[\.\\)]))'
    ];

    const elements = [];
    const seen = new Set();

    selectors.forEach(selector => {
      try {
        const found = document.querySelectorAll(selector);
        found.forEach(el => {
          if (!seen.has(el)) {
            seen.add(el);
            elements.push(el);
          }
        });
      } catch (e) {
        // 忽略选择器错误
      }
    });

    // 如果没有找到，尝试更通用的方法
    if (elements.length === 0) {
      this.log('使用通用方法查找题目');
      return this.findQuestionsByPattern();
    }

    return elements;
  }

  // 通过模式匹配查找题目
  findQuestionsByPattern() {
    const elements = [];
    const patterns = [
      /\d+[\.\)]\s+/,          // 1. 或 1)
      /第\s*\d+\s*题/,         // 第1题
      /Q\d+/i,                 // Q1
      /题目\s*\d+/,            // 题目1
      /[一二三四五六七八九十]+、/ // 一、
    ];

    // 遍历所有文本节点
    const walker = document.createTreeWalker(
      document.body,
      NodeFilter.SHOW_TEXT,
      null,
      false
    );

    let node;
    while ((node = walker.nextNode())) {
      const text = node.textContent.trim();
      if (text.length > 10) { // 排除太短的文本
        for (const pattern of patterns) {
          if (pattern.test(text)) {
            let parent = node.parentElement;
            // 向上查找包含性元素
            while (parent && parent !== document.body) {
              if (parent.textContent.length > 50) { // 认为是题目容器
                elements.push(parent);
                break;
              }
              parent = parent.parentElement;
            }
            break;
          }
        }
      }
    }

    return [...new Set(elements)]; // 去重
  }

  // 提取单个题目
  async extractQuestion(element, index) {
    const question = {
      id: index,
      number: this.extractQuestionNumber(element),
      content: this.extractQuestionContent(element),
      type: this.detectQuestionType(element),
      options: this.extractOptions(element),
      answer: this.extractCorrectAnswer(element),
      elementText: element.textContent.substring(0, 200),
      html: element.innerHTML.substring(0, 500)
    };

    this.log(`提取题目 ${index}: ${question.number || question.id}`);
    return question;
  }

  // 提取题目序号
  extractQuestionNumber(element) {
    const numberPatterns = [
      /(\d+)[\.\)]\s*/,        // 1. 或 1)
      /第\s*(\d+)\s*题/,       // 第1题
      /Q(\d+)/i,               // Q1
      /题目\s*(\d+)/,          // 题目1
      /[（(](\d+)[）)]/        // (1) 或 （1）
    ];

    const text = element.textContent;
    
    for (const pattern of numberPatterns) {
      const match = text.match(pattern);
      if (match && match[1]) {
        return match[1];
      }
    }

    // 尝试从元素属性或类名中提取
    const classNumber = element.className.match(/\bq(\d+)\b/i);
    if (classNumber) return classNumber[1];

    const idNumber = element.id.match(/\bq(\d+)\b/i);
    if (idNumber) return idNumber[1];

    return String(this.id);
  }

  // 提取题目内容
  extractQuestionContent(element) {
    // 尝试找到题目文本元素
    const contentSelectors = [
      '.question-text',
      '.question-content',
      '.question-stem',
      '.stem',
      '.content',
      '.text',
      'p',
      'div:first-child'
    ];

    for (const selector of contentSelectors) {
      const found = element.querySelector(selector);
      if (found && found.textContent.trim().length > 10) {
        return found.textContent.trim();
      }
    }

    // 如果没有找到特定元素，提取整个元素的文本
    let text = element.textContent.trim();
    
    // 移除选项部分（如果能够识别）
    text = this.removeOptionsFromText(text);
    
    // 移除序号部分
    text = text.replace(/^\d+[\.\)]\s*/, '')
               .replace(/^第\s*\d+\s*题\s*/, '')
               .replace(/^Q\d+\s*/i, '')
               .trim();

    return text || element.textContent.substring(0, 300).trim();
  }

  // 从文本中移除选项部分
  removeOptionsFromText(text) {
    const optionPatterns = [
      /\s*[A-D][\.\)].*$/i,      // A. 选项内容
      /\s*[①②③④].*$/,           // ① 选项内容
      /\s*[1-4][\.\)].*$/,       // 1. 选项内容
      /\s*（\s*[A-D]\s*）.*$/i   // （A）选项内容
    ];

    let result = text;
    optionPatterns.forEach(pattern => {
      result = result.replace(pattern, '');
    });

    return result.trim();
  }

  // 检测题目类型
  detectQuestionType(element) {
    const text = element.textContent.toLowerCase();
    
    if (text.includes('单选') || this.hasSingleChoice(element)) {
      return 'single_choice';
    }
    if (text.includes('多选') || this.hasMultipleChoice(element)) {
      return 'multiple_choice';
    }
    if (text.includes('判断') || text.includes('对错')) {
      return 'true_false';
    }
    if (text.includes('填空')) {
      return 'fill_blank';
    }
    if (text.includes('简答') || text.includes('问答')) {
      return 'short_answer';
    }
    if (this.hasRadioButtons(element)) {
      return 'single_choice';
    }
    if (this.hasCheckboxes(element)) {
      return 'multiple_choice';
    }
    
    return 'unknown';
  }

  hasSingleChoice(element) {
    return element.querySelectorAll('input[type="radio"]').length > 0;
  }

  hasMultipleChoice(element) {
    return element.querySelectorAll('input[type="checkbox"]').length > 0;
  }

  hasRadioButtons(element) {
    return this.hasSingleChoice(element);
  }

  hasCheckboxes(element) {
    return this.hasMultipleChoice(element);
  }

  // 提取选项
  extractOptions(element) {
    const options = [];
    
    // 查找选项容器
    const optionContainers = [
      '.options-container',
      '.option-list',
      '.choices',
      '.answer-options',
      'ul',
      'ol'
    ];

    let optionContainer = null;
    for (const selector of optionContainers) {
      const container = element.querySelector(selector);
      if (container) {
        optionContainer = container;
        break;
      }
    }

    // 如果没有找到容器，直接查找选项元素
    const optionElements = optionContainer 
      ? optionContainer.querySelectorAll('.option, .choice-item, li, div[class*="option"], div[class*="choice"]')
      : element.querySelectorAll('.option, .choice-item, li, div[class*="option"], div[class*="choice"]');

    if (optionElements.length === 0) {
      // 尝试查找输入框和标签
      const inputs = element.querySelectorAll('input[type="radio"], input[type="checkbox"]');
      inputs.forEach((input, index) => {
        const label = input.nextElementSibling?.tagName === 'LABEL' 
          ? input.nextElementSibling 
          : document.querySelector(`label[for="${input.id}"]`);
        
        options.push({
          letter: String.fromCharCode(65 + index), // A, B, C, D
          text: label?.textContent.trim() || `选项 ${index + 1}`,
          isCorrect: input.checked || input.getAttribute('data-correct') === 'true',
          element: input
        });
      });
    } else {
      optionElements.forEach((opt, index) => {
        options.push({
          letter: this.extractOptionLetter(opt, index),
          text: this.extractOptionText(opt),
          isCorrect: this.isOptionCorrect(opt),
          element: opt
        });
      });
    }

    return options;
  }

  // 提取选项字母
  extractOptionLetter(element, index) {
    const letterMatch = element.textContent.match(/^([A-D])[\.\)]/i);
    if (letterMatch) return letterMatch[1].toUpperCase();

    const chineseMatch = element.textContent.match(/^([①②③④])/);
    if (chineseMatch) {
      const chineseToLetter = { '①': 'A', '②': 'B', '③': 'C', '④': 'D' };
      return chineseToLetter[chineseMatch[1]] || String.fromCharCode(65 + index);
    }

    return String.fromCharCode(65 + index); // 默认 A, B, C, D
  }

  // 提取选项文本
  extractOptionText(element) {
    // 移除字母标记
    let text = element.textContent.trim();
    text = text.replace(/^[A-D][\.\)]\s*/i, '')
               .replace(/^[①②③④]\s*/, '')
               .replace(/^[1-4][\.\)]\s*/, '')
               .trim();
    
    return text || element.textContent.trim();
  }

  // 检查选项是否正确
  isOptionCorrect(element) {
    return element.classList.contains('correct') ||
           element.classList.contains('right') ||
           element.getAttribute('data-correct') === 'true' ||
           element.querySelector('input:checked') !== null ||
           element.querySelector('input[data-correct="true"]') !== null;
  }

  // 提取正确答案
  extractCorrectAnswer(element) {
    // 查找明确的答案元素
    const answerElements = [
      '.answer',
      '.correct-answer',
      '.answer-key',
      '.right-answer',
      '.solution',
      '.explanation'
    ];

    for (const selector of answerElements) {
      const answerEl = element.querySelector(selector);
      if (answerEl) {
        return answerEl.textContent.trim();
      }
    }

    // 从选项中提取正确答案
    const options = this.extractOptions(element);
    const correctOptions = options.filter(opt => opt.isCorrect);
    
    if (correctOptions.length > 0) {
      return correctOptions.map(opt => opt.letter).join(', ');
    }

    // 尝试从文本中提取答案模式
    const text = element.textContent;
    const answerPatterns = [
      /答案[：:]\s*([A-D, ]+)/i,
      /正确答案[：:]\s*([A-D, ]+)/i,
      /标准答案[：:]\s*([A-D, ]+)/i,
      /answer[：:]\s*([A-D, ]+)/i,
      /\b([A-D])\b.*[是对√]/i
    ];

    for (const pattern of answerPatterns) {
      const match = text.match(pattern);
      if (match && match[1]) {
        return match[1].trim();
      }
    }

    return '';
  }

  // 提取所有数据
  async extractAllData() {
    this.log('开始提取所有数据');
    
    await this.extractPageInfo();
    await this.extractAllQuestions();
    
    return {
      ...this.data,
      summary: {
        totalQuestions: this.data.questions.length,
        questionsWithAnswers: this.data.questions.filter(q => q.answer).length,
        questionTypes: this.data.questions.reduce((acc, q) => {
          acc[q.type] = (acc[q.type] || 0) + 1;
          return acc;
        }, {})
      }
    };
  }

  // 延迟函数
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // 获取当前数据
  getCurrentData() {
    return this.data;
  }
}

// 初始化提取器
window.xunwangExtractor = new XunwangAnswerExtractor();

// 导出全局函数供调试
window.extractXunwangData = () => window.xunwangExtractor.extractAllData();
window.getXunwangData = () => window.xunwangExtractor.getCurrentData();

this.log('讯网题目答案提取器已加载');