// 讯网答案提取器 - 工具函数库

class XunWangUtils {
    // 格式化日期时间
    static formatDateTime(date = new Date(), format = 'YYYY-MM-DD HH:mm:ss') {
        const pad = (n) => n.toString().padStart(2, '0');
        
        const replacements = {
            'YYYY': date.getFullYear(),
            'MM': pad(date.getMonth() + 1),
            'DD': pad(date.getDate()),
            'HH': pad(date.getHours()),
            'mm': pad(date.getMinutes()),
            'ss': pad(date.getSeconds())
        };
        
        return format.replace(/YYYY|MM|DD|HH|mm|ss/g, match => replacements[match]);
    }

    // 生成唯一ID
    static generateId(prefix = '') {
        const timestamp = Date.now().toString(36);
        const random = Math.random().toString(36).substring(2, 8);
        return `${prefix}${timestamp}${random}`;
    }

    // 安全获取对象属性
    static safeGet(obj, path, defaultValue = null) {
        try {
            const keys = path.split('.');
            let result = obj;
            
            for (const key of keys) {
                if (result === null || result === undefined) {
                    return defaultValue;
                }
                result = result[key];
            }
            
            return result === undefined ? defaultValue : result;
        } catch (error) {
            return defaultValue;
        }
    }

    // 深度克隆对象
    static deepClone(obj) {
        if (obj === null || typeof obj !== 'object') {
            return obj;
        }
        
        if (obj instanceof Date) {
            return new Date(obj.getTime());
        }
        
        if (obj instanceof Array) {
            return obj.map(item => this.deepClone(item));
        }
        
        if (typeof obj === 'object') {
            const cloned = {};
            for (const key in obj) {
                if (obj.hasOwnProperty(key)) {
                    cloned[key] = this.deepClone(obj[key]);
                }
            }
            return cloned;
        }
        
        return obj;
    }

    // 防抖函数
    static debounce(func, wait = 300) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // 节流函数
    static throttle(func, limit = 300) {
        let inThrottle;
        return function executedFunction(...args) {
            if (!inThrottle) {
                func(...args);
                inThrottle = true;
                setTimeout(() => (inThrottle = false), limit);
            }
        };
    }

    // 数据验证
    static validateQuestionData(data) {
        const requiredFields = ['questionId', 'question', 'answer'];
        const errors = [];
        
        // 检查必需字段
        for (const field of requiredFields) {
            if (!data[field]) {
                errors.push(`缺少必需字段: ${field}`);
            }
        }
        
        // 验证题目ID格式
        if (data.questionId && !/^question_[a-z0-9]+$/.test(data.questionId)) {
            errors.push('题目ID格式不正确');
        }
        
        // 验证答案长度
        if (data.answer && data.answer.length > 1000) {
            errors.push('答案长度超过限制');
        }
        
        // 验证分数范围
        if (data.score !== undefined && (data.score < 0 || data.score > 100)) {
            errors.push('分数必须在0-100之间');
        }
        
        return {
            isValid: errors.length === 0,
            errors: errors
        };
    }

    // 数据清理和格式化
    static cleanData(data) {
        const cleaned = { ...data };
        
        // 去除字符串两端的空白字符
        const stringFields = ['question', 'answer', 'userAnswer', 'knowledge'];
        stringFields.forEach(field => {
            if (cleaned[field]) {
                cleaned[field] = cleaned[field].trim();
            }
        });
        
        // 转换布尔值
        if (cleaned.isCorrect !== undefined) {
            cleaned.isCorrect = Boolean(cleaned.isCorrect);
        }
        
        // 转换数字
        if (cleaned.score !== undefined) {
            cleaned.score = parseFloat(cleaned.score) || 0;
        }
        
        // 生成短摘要
        if (cleaned.question) {
            cleaned.summary = cleaned.question.substring(0, 50) + 
                            (cleaned.question.length > 50 ? '...' : '');
        }
        
        // 添加时间戳
        if (!cleaned.extractedAt) {
            cleaned.extractedAt = Date.now();
        }
        
        return cleaned;
    }

    // 数据分组
    static groupBy(array, key) {
        return array.reduce((result, item) => {
            const groupKey = item[key];
            if (!result[groupKey]) {
                result[groupKey] = [];
            }
            result[groupKey].push(item);
            return result;
        }, {});
    }

    // 数据去重
    static deduplicate(array, key = 'questionId') {
        const seen = new Set();
        return array.filter(item => {
            const identifier = item[key];
            if (seen.has(identifier)) {
                return false;
            }
            seen.add(identifier);
            return true;
        });
    }

    // CSV转义
    static escapeCsvValue(value) {
        if (value === null || value === undefined) {
            return '';
        }
        
        const stringValue = String(value);
        
        // 如果包含逗号、换行符或双引号，需要转义
        if (stringValue.includes(',') || 
            stringValue.includes('\n') || 
            stringValue.includes('\r') || 
            stringValue.includes('"')) {
            
            // 转义双引号：将 " 替换为 ""
            const escaped = stringValue.replace(/"/g, '""');
            return `"${escaped}"`;
        }
        
        return stringValue;
    }

    // 生成CSV行
    static generateCsvRow(data, headers) {
        return headers.map(header => {
            const value = this.safeGet(data, header, '');
            return this.escapeCsvValue(value);
        }).join(',');
    }

    // 生成CSV文件
    static generateCsv(data, headers = null) {
        if (!data || data.length === 0) {
            return '';
        }
        
        // 如果没有指定headers，使用第一个对象的keys
        if (!headers) {
            headers = Object.keys(data[0]);
        }
        
        // 生成CSV内容
        const csvRows = [];
        
        // 添加标题行
        csvRows.push(headers.join(','));
        
        // 添加数据行
        data.forEach(item => {
            csvRows.push(this.generateCsvRow(item, headers));
        });
        
        return csvRows.join('\n');
    }

    // 生成文件名
    static generateFilename(prefix = 'xunwang', extension = 'csv', includeTimestamp = true) {
        const parts = [prefix];
        
        if (includeTimestamp) {
            const timestamp = this.formatDateTime(new Date(), 'YYYYMMDD_HHmmss');
            parts.push(timestamp);
        }
        
        parts.push(extension);
        return parts.join('.');
    }

    // 存储管理
    static async storageGet(keys) {
        try {
            const result = await chrome.storage.local.get(keys);
            return result;
        } catch (error) {
            console.error('存储读取失败:', error);
            return {};
        }
    }

    static async storageSet(data) {
        try {
            await chrome.storage.local.set(data);
            return true;
        } catch (error) {
            console.error('存储写入失败:', error);
            return false;
        }
    }

    static async storageRemove(keys) {
        try {
            await chrome.storage.local.remove(keys);
            return true;
        } catch (error) {
            console.error('存储删除失败:', error);
            return false;
        }
    }

    // 日志记录
    static log(level, message, data = null) {
        const timestamp = this.formatDateTime();
        const logEntry = {
            timestamp,
            level,
            message,
            data
        };
        
        // 控制台输出
        const consoleMethod = level === 'error' ? console.error : 
                             level === 'warn' ? console.warn : 
                             level === 'info' ? console.info : console.log;
        
        consoleMethod(`[${timestamp}] [${level.toUpperCase()}] ${message}`, data || '');
        
        // 保存到存储（可选）
        this.saveLogEntry(logEntry);
    }

    static async saveLogEntry(logEntry) {
        try {
            const storage = await this.storageGet(['logs']);
            const logs = storage.logs || [];
            
            logs.push(logEntry);
            
            // 限制日志数量
            if (logs.length > 1000) {
                logs.splice(0, logs.length - 1000);
            }
            
            await this.storageSet({ logs });
        } catch (error) {
            console.error('保存日志失败:', error);
        }
    }

    // 错误处理
    static handleError(error, context = '') {
        const errorInfo = {
            message: error.message,
            stack: error.stack,
            context: context,
            timestamp: Date.now()
        };
        
        this.log('error', `错误: ${error.message}`, { context, stack: error.stack });
        
        // 保存错误记录
        this.saveError(errorInfo);
        
        return {
            success: false,
            error: error.message,
            context: context
        };
    }

    static async saveError(errorInfo) {
        try {
            const storage = await this.storageGet(['errors']);
            const errors = storage.errors || [];
            
            errors.push(errorInfo);
            
            // 限制错误数量
            if (errors.length > 100) {
                errors.splice(0, errors.length - 100);
            }
            
            await this.storageSet({ errors });
        } catch (error) {
            console.error('保存错误记录失败:', error);
        }
    }

    // 加密函数（简单版）
    static simpleEncrypt(text, key = 'xunwang2026') {
        try {
            let result = '';
            for (let i = 0; i < text.length; i++) {
                const charCode = text.charCodeAt(i) ^ key.charCodeAt(i % key.length);
                result += String.fromCharCode(charCode);
            }
            return btoa(result);
        } catch (error) {
            return text;
        }
    }

    static simpleDecrypt(encryptedText, key = 'xunwang2026') {
        try {
            const decoded = atob(encryptedText);
            let result = '';
            for (let i = 0; i < decoded.length; i++) {
                const charCode = decoded.charCodeAt(i) ^ key.charCodeAt(i % key.length);
                result += String.fromCharCode(charCode);
            }
            return result;
        } catch (error) {
            return encryptedText;
        }
    }

    // 性能监控
    static createPerformanceMonitor(name) {
        const startTime = performance.now();
        
        return {
            end: () => {
                const endTime = performance.now();
                const duration = endTime - startTime;
                this.log('info', `性能监控 [${name}]: ${duration.toFixed(2)}ms`);
                return duration;
            }
        };
    }

    // 数据统计
    static calculateStatistics(data) {
        if (!data || data.length === 0) {
            return {
                total: 0,
                correctCount: 0,
                incorrectCount: 0,
                averageScore: 0,
                scoreDistribution: {}
            };
        }
        
        const total = data.length;
        const correctCount = data.filter(item => item.isCorrect).length;
        const incorrectCount = total - correctCount;
        
        const scores = data.map(item => item.score || 0);
        const totalScore = scores.reduce((sum, score) => sum + score, 0);
        const averageScore = total > 0 ? totalScore / total : 0;
        
        // 分数分布
        const scoreDistribution = {};
        scores.forEach(score => {
            const range = Math.floor(score / 10) * 10;
            scoreDistribution[range] = (scoreDistribution[range] || 0) + 1;
        });
        
        return {
            total,
            correctCount,
            incorrectCount,
            correctRate: total > 0 ? (correctCount / total * 100).toFixed(1) + '%' : '0%',
            averageScore: averageScore.toFixed(1),
            scoreDistribution
        };
    }
}

// 导出工具类
if (typeof module !== 'undefined' && module.exports) {
    module.exports = XunWangUtils;
}

// 全局可用
window.XunWangUtils = XunWangUtils;