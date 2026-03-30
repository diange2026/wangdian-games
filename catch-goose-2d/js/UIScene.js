class UIScene extends Phaser.Scene {
    constructor() {
        super({ key: 'UIScene' });
    }

    create() {
        // 倒计时显示
        this.timerText = this.add.text(380, 30, '⏱️ 60s', {
            fontSize: '24px',
            fontStyle: 'bold',
            color: '#ffffff',
            stroke: '#000000',
            strokeThickness: 4
        }).setOrigin(1, 0);
        
        // 消除计数
        this.matchText = this.add.text(70, 30, '🎯 0', {
            fontSize: '24px',
            fontStyle: 'bold',
            color: '#ffffff',
            stroke: '#000000',
            strokeThickness: 4
        }).setOrigin(0, 0);
        
        // 监听 GameScene 事件
        const gameScene = this.scene.get('GameScene');
        gameScene.events.on('timerUpdate', (data) => {
            this.timerText.setText(`⏱️ ${data.timeLeft}s`);
            
            // 时间不足时变红
            if (data.timeLeft <= 10) {
                this.timerText.setColor('#ff0000');
            }
        });
        
        gameScene.events.on('matchMade', (data) => {
            this.matchText.setText(`🎯 ${data.count}`);
        });
        
        gameScene.events.on('gameStart', () => {
            // 游戏开始，可以在这里添加音效
        });
    }
}
