// 讯网答案提取器 - 内容脚本
// 在讯网教学云平台页面中运行

class XunWangAnswerExtractor {
    constructor() {
        this.init();
        this.setupMessageListener();
    }

    init() {
        console.log('讯网答案提取器已加载');
        
        // 检查当前页面类型
        this.pageType = this.detectPageType();
        
        // 如果是答案页面，注入提取按钮
        if (this.pageType === 'answer-detail') {
            this.injectExtractButton();
        }
    }

    // 检测页面类型
    detectPageType() {
        const url = window.location.href;
        
        // 登录页面
        if (url.includes('/exam/login.thtml')) {
            return 'login';
        }
        
        // 答案详情页面
        if (url.includes('assignments-detail')) {
            return 'answer-detail';
        }
        
        // 作业记录页面
        if (url.includes('assignments') && !url.includes('detail')) {
            return 'assignments-list';
        }
        
        // 课程学习页面
        if (url.includes('courseware-study')) {
            return 'course-study';
        }
        
        return 'unknown';
    }

    // 注入提取按钮到页面
    injectExtractButton() {
        // 创建提取按钮容器
        const buttonContainer = document.createElement('div');
        buttonContainer.id = 'xunwang-extractor-container';
        buttonContainer.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            z-index: 999999;
            background: white;
            border-radius: 12px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            padding: 15px;
            min-width: 200px;
            border: 1px solid #e0e0e0;
        `;

        // 创建标题
        const title = document.createElement('div');
        title.style.cssText = `
            font-size: 14px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
            padding-bottom: 8px;
            border-bottom: 1px solid #eee;
            display: flex;
            align-items: center;
            gap: 8px;
        `;
        title.innerHTML = `
            <span style="color: #4a6ee0; font-size: 16px;">📚</span>
            <span>讯网答案提取器</span>
        `;

        // 创建提取按钮
        const extractBtn = document.createElement('button');
        extractBtn.id = 'xunwang-extract-btn';
        extractBtn.style.cssText = `
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #4a6ee0 0%, #6a11cb 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: all 0.3s ease;
            margin-bottom: 10px;
        `;
        extractBtn.innerHTML = `
            <span>🔍</span>
            <span>一键提取答案</span>
        `;
        extractBtn.onmouseenter = () => {
            extractBtn.style.transform = 'translateY(-2px)';
            extractBtn.style.boxShadow = '0 6px 20px rgba(74, 110, 224, 0.4)';
        };
        extractBtn.onmouseleave = () => {
            extractBtn.style.transform = 'translateY(0)';
            extractBtn.style.boxShadow = 'none';
        };
        extractBtn.onclick = () => this.extractAnswers();

        // 创建状态显示
        const statusDiv = document.createElement('div');
        statusDiv.id = 'xunwang-extractor-status';
        statusDiv.style.cssText = `
            font-size: 12px;
            color: #666;
            margin-top: 8px;
            padding-top: 8px;
            border-top: 1px solid #eee;
            display: flex;
            justify-content: space-between;
        `;
        statusDiv.innerHTML = `
            <span>检测题目：<span id="detected-count">0</span></span>
            <span>状态：<span id="extractor-status">就绪</span></span>
        `;

        // 组装容器
        buttonContainer.appendChild(title);
        buttonContainer.appendChild(extractBtn);
        buttonContainer.appendChild(statusDiv);
        
        // 添加到页面
        document.body.appendChild(buttonContainer);

        // 添加拖拽功能
        this.makeDraggable(buttonContainer);
        
        // 自动检测题目数量
        setTimeout(() => this.updateDetectedCount(), 1000);
    }

    // 使容器可拖拽
    makeDraggable(element) {
        let isDragging = false;
        let offsetX, offsetY;

        const title = element.querySelector('div');
        
        title.style.cursor = 'move';
        
        title.addEventListener('mousedown', (e) => {
            isDragging = true;
            offsetX = e.clientX - element.offsetLeft;
            offsetY = e.clientY - element.offsetTop;
            element.style.cursor = 'grabbing';
            e.preventDefault();
        });

        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            
            const x = e.clientX - offsetX;
            const y = e.clientY - offsetY;
            
            // 限制在窗口范围内
            const maxX = window.innerWidth - element.offsetWidth;
            const maxY = window.innerHeight - element.offsetHeight;
            
            element.style.left = Math.min(Math.max(x, 10), maxX) + 'px';
            element.style.top = Math.min(Math.max(y, 10), maxY) + 'px';
        });

        document.addEventListener('mouseup', () => {
            isDragging = false;
            element.style.cursor = 'default';
        });
    }

    // 更新检测到的题目数量
    updateDetectedCount() {
        const questions = this.findQuestions();
        const count = questions.length;
        
        const countElement = document.getElementById('detected-count');
        if (countElement) {
            countElement.textContent = count;
            countElement.style.color = count > 0 ? '#2ecc71' : '#e74c3c';
        }
        
        return count;
    }

    // 查找题目元素
    findQuestions() {
        // 这里需要根据实际页面结构来定位题目
        // 以下是几种可能的定位方式
        
        let questions = [];
        
        // 方式1：通过特定class查找
        questions = [...document.querySelectorAll('.question-item, .exercise-item, .question-container')];
        
        // 方式2：通过包含特定文字的div查找
        if (questions.length === 0) {
            questions = [...document.querySelectorAll('div')].filter(div => {
                const text = div.textContent;
                return text.includes('题') && text.includes('答案');
            });
        }
        
        // 方式3：查找包含序号和答案的表格行
        if (questions.length === 0) {
            const tables = document.querySelectorAll('table');
            for (const table of tables) {
                const rows = table.querySelectorAll('tr');
                if (rows.length > 2) { // 假设至少有标题行和数据行
                    const firstRowText = rows[0].textContent;
                    if (firstRowText.includes('序号') || firstRowText.includes('题号')) {
                        questions = Array.from(rows).slice(1); // 排除标题行
                        break;
                    }
                }
            }
        }
        
        return questions;
    }

    // 提取答案数据
    async extractAnswers() {
        const statusElement = document.getElementById('extractor-status');
        const extractBtn = document.getElementById('xunwang-extract-btn');
        
        if (statusElement) {
            statusElement.textContent = '提取中...';
            statusElement.style.color = '#f39c12';
        }
        
        if (extractBtn) {
            extractBtn.disabled = true;
            extractBtn.innerHTML = '<span>⏳</span><span>提取中...</span>';
            extractBtn.style.opacity = '0.7';
        }
        
        try {
            // 查找所有题目
            const questionElements = this.findQuestions();
            
            if (questionElements.length === 0) {
                throw new Error('未找到题目元素');
            }
            
            // 提取每道题目的数据
            const extractedData = [];
            
            for (let i = 0; i < questionElements.length; i++) {
                const element = questionElements[i];
                const questionData = this.parseQuestionElement(element, i + 1);
                
                if (questionData) {
                    extractedData.push(questionData);
                }
                
                // 更新进度
                this.updateProgress(i, questionElements.length);
            }
            
            // 验证提取的数据
            if (extractedData.length === 0) {
                throw new Error('未提取到有效数据');
            }
            
            // 更新状态
            if (statusElement) {
                statusElement.textContent = '提取成功';
                statusElement.style.color = '#2ecc71';
            }
            
            // 发送消息给background script
            const response = await chrome.runtime.sendMessage({
                action: 'extractComplete',
                data: extractedData
            });
            
            return {
                success: true,
                data: extractedData,
                message: `成功提取 ${extractedData.length} 条答案数据`
            };
            
        } catch (error) {
            console.error('提取答案错误:', error);
            
            if (statusElement) {
                statusElement.textContent = '提取失败';
                statusElement.style.color = '#e74c3c';
            }
            
            return {
                success: false,
                message: error.message || '提取答案失败'
            };
            
        } finally {
            // 重置按钮状态
            if (extractBtn) {
                setTimeout(() => {
                    extractBtn.disabled = false;
                    extractBtn.innerHTML = '<span>🔍</span><span>一键提取答案</span>';
                    extractBtn.style.opacity = '1';
                    
                    if (statusElement) {
                        statusElement.textContent = '就绪';
                        statusElement.style.color = '#666';
                    }
                }, 2000);
            }
        }
    }

    // 解析单个题目元素
    parseQuestionElement(element, index) {
        try {
            const elementText = element.textContent.trim();
            
            // 提取题目内容
            let question = '';
            let answer = '';
            let userAnswer = '';
            let isCorrect = false;
            let score = 0;
            let knowledge = '';
            
            // 尝试不同的解析策略
            
            // 策略1：查找包含"答案："或"正确答案："的文本
            const answerMatch = elementText.match(/[答案|正确答案][：:]\s*([^\n]+)/i);
            if (answerMatch) {
                answer = answerMatch[1].trim();
            }
            
            // 策略2：查找包含"题目："或"试题："的文本
            const questionMatch = elementText.match(/[题目|试题|问题][：:]\s*([^\n]+)/i);
            if (questionMatch) {
                question = questionMatch[1].trim();
            } else {
                // 如果没有明确标识，取第一行作为题目
                const lines = elementText.split('\n').filter(line => line.trim());
                if (lines.length > 0) {
                    question = lines[0].trim();
                }
            }
            
            // 策略3：查找用户答案
            const userAnswerMatch = elementText.match(/[你的答案|用户答案][：:]\s*([^\n]+)/i);
            if (userAnswerMatch) {
                userAnswer = userAnswerMatch[1].trim();
            }
            
            // 策略4：查找是否正确
            const correctMatch = elementText.match(/[状态|结果][：:]\s*([正确|错误]+)/i);
            if (correctMatch) {
                isCorrect = correctMatch[1].includes('正确');
            }
            
            // 策略5：查找分值
            const scoreMatch = elementText.match(/(\d+(\.\d+)?)\s*分/);
            if (scoreMatch) {
                score = parseFloat(scoreMatch[1]);
            }
            
            // 生成题目ID
            const questionId = this.generateQuestionId(element, index);
            
            return {
                index: index,
                questionId: questionId,
                question: question || `题目 ${index}`,
                answer: answer || '未提取到答案',
                userAnswer: userAnswer,
                isCorrect: isCorrect,
                score: score,
                knowledge: knowledge,
                elementText: elementText.substring(0, 200) + '...',
                rawHtml: element.outerHTML.substring(0, 500)
            };
            
        } catch (error) {
            console.error('解析题目元素错误:', error, element);
            return null;
        }
    }

    // 生成题目ID
    generateQuestionId(element, index) {
        // 尝试从元素属性中获取ID
        if (element.id) {
            return element.id;
        }
        
        // 尝试从data属性中获取
        const dataId = element.getAttribute('data-id') || 
                      element.getAttribute('data-question-id') ||
                      element.getAttribute('data-index');
        
        if (dataId) {
            return dataId;
        }
        
        // 生成基于内容和位置的哈希ID
        const text = element.textContent.trim();
        const position = this.getElementPosition(element);
        const hash = this.simpleHash(text + position + index);
        
        return `question_${hash}`;
    }

    // 获取元素位置
    getElementPosition(element) {
        const rect = element.getBoundingClientRect();
        return `${Math.round(rect.top)}_${Math.round(rect.left)}`;
    }

    // 简单哈希函数
    simpleHash(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // 转换为32位整数
        }
        return Math.abs(hash).toString(36).substring(0, 8);
    }

    // 更新进度
    updateProgress(current, total) {
        const statusElement = document.getElementById('extractor-status');
        if (statusElement) {
            const percent = Math.round((current + 1) / total * 100);
            statusElement.textContent = `提取中 ${percent}%`;
        }
    }

    // 设置消息监听器
    setupMessageListener() {
        chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
            switch (message.action) {
                case 'extractAnswers':
                    this.extractAnswers().then(result => {
                        sendResponse(result);
                    }).catch(error => {
                        sendResponse({
                            success: false,
                            message: error.message || '提取失败'
                        });
                    });
                    return true; // 保持消息通道开放
                    
                case 'getPageInfo':
                    const pageInfo = {
                        pageType: this.pageType,
                        url: window.location.href,
                        title: document.title,
                        detectedQuestions: this.updateDetectedCount()
                    };
                    sendResponse(pageInfo);
                    break;
                    
                case 'ping':
                    sendResponse({ alive: true, version: '1.0.0' });
                    break;
            }
        });
    }
}

// 启动提取器
if (window.location.href.includes('whxunw.com')) {
    // 等待页面加载完成
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            new XunWangAnswerExtractor();
        });
    } else {
        new XunWangAnswerExtractor();
    }
}

// 导出给其他脚本使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = XunWangAnswerExtractor;
}