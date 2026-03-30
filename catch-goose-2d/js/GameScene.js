class GameScene extends Phaser.Scene {
    constructor() {
        super({ key: 'GameScene' });
    }

    init() {
        // 游戏状态
        this.items = [];
        this.slots = [];
        this.matchedCount = 0;
        this.timeLeft = 60;
        this.gameActive = false;
        
        // 物品配置（2D 简化版，用颜色块代替图片）
        this.itemTypes = [
            { color: 0xFF6B6B, emoji: '🦢' },
            { color: 0x4ECDC4, emoji: '🐥' },
            { color: 0x45B7D1, emoji: '🐰' },
            { color: 0xF7B731, emoji: '🐱' },
            { color: 0xA3CB38, emoji: '🐶' },
            { color: 0xD980FA, emoji: '🐸' }
        ];
        
        this.slotCapacity = 7;
    }

    create() {
        // 创建 UI 场景引用
        this.uiScene = this.scene.get('UIScene');
        
        // 游戏区域
        this.createGameArea();
        
        // 槽位区域
        this.createSlotBar();
        
        // 开始按钮
        this.createStartButton();
        
        // 初始不生成物品
    }

    createGameArea() {
        // 游戏背景区域
        this.gameArea = this.add.rectangle(225, 350, 400, 500, 0xffffff)
            .setOrigin(0.5)
            .setStrokeStyle(3, 0x667eea);
        
        // 标题
        this.add.text(225, 50, '抓大鹅 2D', {
            fontSize: '36px',
            fontStyle: 'bold',
            color: '#667eea'
        }).setOrigin(0.5);
    }

    createSlotBar() {
        // 槽位背景
        this.slotBarBg = this.add.rectangle(225, 720, 420, 70, 0x333333)
            .setOrigin(0.5)
            .setAlpha(0.8);
        
        // 创建 7 个槽位
        this.slots = [];
        for (let i = 0; i < this.slotCapacity; i++) {
            const x = 65 + i * 55;
            const slot = this.add.rectangle(x, 720, 50, 50, 0xffffff)
                .setOrigin(0.5)
                .setStrokeStyle(2, 0x667eea);
            
            this.slots.push({
                rect: slot,
                item: null,
                isEmpty: true
            });
        }
    }

    createStartButton() {
        this.startBtn = this.add.rectangle(225, 650, 200, 60, 0xFF6B6B)
            .setOrigin(0.5)
            .setInteractive({ useHandCursor: true });
        
        this.startBtnText = this.add.text(225, 650, '▶️ 开始游戏', {
            fontSize: '24px',
            fontStyle: 'bold',
            color: '#ffffff'
        }).setOrigin(0.5);
        
        this.startBtn.on('pointerdown', () => this.startGame());
        this.startBtn.on('pointerover', () => this.startBtn.setFillStyle(0xff8e53));
        this.startBtn.on('pointerout', () => this.startBtn.setFillStyle(0xFF6B6B));
    }

    startGame() {
        this.gameActive = true;
        this.timeLeft = 60;
        this.matchedCount = 0;
        this.items = [];
        
        // 清空槽位
        this.slots.forEach(slot => {
            if (slot.item) {
                slot.item.destroy();
                slot.item = null;
                slot.isEmpty = true;
            }
        });
        
        // 隐藏开始按钮
        this.startBtn.setVisible(false);
        this.startBtnText.setVisible(false);
        
        // 生成物品（3 层堆叠）
        this.generateItems(3, 5);
        
        // 启动倒计时
        this.startTimer();
        
        // 通知 UI 场景更新
        this.events.emit('gameStart', {
            timeLeft: this.timeLeft,
            matched: this.matchedCount
        });
    }

    generateItems(layers, typesCount) {
        const selectedTypes = this.itemTypes.slice(0, typesCount);
        
        for (let layer = 0; layer < layers; layer++) {
            selectedTypes.forEach(itemType => {
                const count = 3 + Phaser.Math.Between(0, 2); // 每个类型 3-5 个
                
                for (let i = 0; i < count; i++) {
                    const x = Phaser.Math.Between(80, 370);
                    const y = Phaser.Math.Between(100 + layer * 30, 550 + layer * 30);
                    
                    this.createItem(x, y, itemType, layer);
                }
            });
        }
    }

    createItem(x, y, itemType, layer) {
        // 创建物品容器
        const container = this.add.container(x, y);
        
        // 背景矩形
        const bg = this.add.rectangle(0, 0, 50, 50, itemType.color)
            .setStrokeStyle(2, 0xffffff);
        
        // Emoji 文字
        const emoji = this.add.text(0, 0, itemType.emoji, {
            fontSize: '28px'
        }).setOrigin(0.5);
        
        container.add([bg, emoji]);
        container.setSize(50, 50);
        container.setInteractive({ useHandCursor: true });
        
        // 保存物品数据
        const itemData = {
            container: container,
            type: itemType,
            layer: layer,
            isSelected: false,
            isMatched: false
        };
        
        this.items.push(itemData);
        
        // 点击事件
        container.on('pointerdown', () => this.selectItem(itemData));
        
        // 悬停效果
        container.on('pointerover', () => {
            if (this.gameActive && !itemData.isSelected) {
                container.setScale(1.1);
            }
        });
        
        container.on('pointerout', () => {
            if (!itemData.isSelected) {
                container.setScale(1);
            }
        });
    }

    selectItem(item) {
        if (!this.gameActive || item.isSelected || item.isMatched) return;
        
        // 查找空槽位
        const emptySlotIndex = this.slots.findIndex(slot => slot.isEmpty);
        if (emptySlotIndex === -1) {
            // 槽位已满，游戏结束
            this.gameOver(false);
            return;
        }
        
        // 放入槽位
        item.isSelected = true;
        item.container.setScale(0.8);
        
        this.slots[emptySlotIndex].item = item;
        this.slots[emptySlotIndex].isEmpty = false;
        
        // 播放音效（可选）
        // this.sound.play('select', { volume: 0.3 });
        
        // 检查匹配
        this.checkMatch();
    }

    checkMatch() {
        // 检查是否有 3 个连续相同物品
        for (let i = 2; i < this.slotCapacity; i++) {
            const slot1 = this.slots[i - 2];
            const slot2 = this.slots[i - 1];
            const slot3 = this.slots[i];
            
            if (slot1.item && slot2.item && slot3.item &&
                !slot1.isEmpty && !slot2.isEmpty && !slot3.isEmpty &&
                slot1.item.type.color === slot2.item.type.color &&
                slot2.item.type.color === slot3.item.type.color) {
                
                // 匹配成功！
                this.handleMatch([slot1, slot2, slot3]);
                return;
            }
        }
    }

    handleMatch(slots) {
        // 延迟一点让玩家看到匹配
        this.time.delayedCall(300, () => {
            slots.forEach(slot => {
                const item = slot.item;
                if (item) {
                    // 消除动画
                    this.tweens.add({
                        targets: item.container,
                        scale: 0,
                        alpha: 0,
                        duration: 300,
                        onComplete: () => {
                            item.container.destroy();
                            item.isMatched = true;
                        }
                    });
                    
                    slot.item = null;
                    slot.isEmpty = true;
                }
            });
            
            this.matchedCount += 3;
            this.events.emit('matchMade', { count: this.matchedCount });
            
            // 检查胜利条件
            this.checkWin();
        });
    }

    checkWin() {
        const remainingItems = this.items.filter(item => !item.isMatched && !item.isSelected).length;
        
        if (remainingItems === 0) {
            // 胜利！
            this.gameOver(true);
        } else if (this.slots.filter(slot => !slot.isEmpty).length === this.slotCapacity) {
            // 槽位已满，检查是否还有可消除的
            const hasMatch = this.checkForPossibleMatch();
            if (!hasMatch) {
                this.gameOver(false);
            }
        }
    }

    checkForPossibleMatch() {
        // 简化版：检查槽位中是否有 3 个相同
        const colorCount = {};
        this.slots.forEach(slot => {
            if (slot.item && !slot.isEmpty) {
                const color = slot.item.type.color;
                colorCount[color] = (colorCount[color] || 0) + 1;
            }
        });
        
        return Object.values(colorCount).some(count => count >= 3);
    }

    startTimer() {
        this.timerEvent = this.time.addEvent({
            delay: 1000,
            callback: () => {
                this.timeLeft--;
                this.events.emit('timerUpdate', { timeLeft: this.timeLeft });
                
                if (this.timeLeft <= 0) {
                    this.gameOver(false);
                }
            },
            repeat: 59
        });
    }

    gameOver(isWin) {
        this.gameActive = false;
        
        if (this.timerEvent) {
            this.timerEvent.remove();
        }
        
        // 显示结果
        if (isWin) {
            this.showResult('🎉 胜利！', `消除 ${this.matchedCount} 个物品`);
        } else {
            this.showResult('😢 游戏结束', '再来一次吧！');
        }
    }

    showResult(title, message) {
        // 半透明背景
        const overlay = this.add.rectangle(225, 400, 400, 800, 0x000000)
            .setAlpha(0.7)
            .setInteractive();
        
        // 结果框
        const resultBox = this.add.rectangle(225, 400, 350, 200, 0xffffff)
            .setOrigin(0.5);
        
        // 标题
        this.add.text(225, 350, title, {
            fontSize: '32px',
            fontStyle: 'bold',
            color: '#333'
        }).setOrigin(0.5);
        
        // 消息
        this.add.text(225, 420, message, {
            fontSize: '20px',
            color: '#666'
        }).setOrigin(0.5);
        
        // 重玩按钮
        const replayBtn = this.add.rectangle(225, 500, 150, 50, 0x4ECDC4)
            .setOrigin(0.5)
            .setInteractive({ useHandCursor: true });
        
        this.add.text(225, 500, '🔄 再玩一次', {
            fontSize: '18px',
            fontStyle: 'bold',
            color: '#fff'
        }).setOrigin(0.5);
        
        replayBtn.on('pointerdown', () => {
            overlay.destroy();
            resultBox.destroy();
            this.startBtn.setVisible(true);
            this.startBtnText.setVisible(true);
            this.scene.restart();
        });
    }
}
