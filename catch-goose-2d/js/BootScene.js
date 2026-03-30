class BootScene extends Phaser.Scene {
    constructor() {
        super({ key: 'BootScene' });
    }

    preload() {
        // 加载界面
        const progressBar = this.add.graphics();
        const progressBox = this.add.graphics();
        progressBox.fillStyle(0xffffff, 0.5);
        progressBox.fillRect(175, 380, 100, 30);
        
        const loadingText = this.add.text(225, 350, '加载中...', {
            fontSize: '20px',
            color: '#ffffff'
        }).setOrigin(0.5);
        
        this.load.on('progress', (value) => {
            progressBar.clear();
            progressBar.fillStyle(0xffffff, 1);
            progressBar.fillRect(185, 390, 80 * value, 10);
        });
        
        // 这里可以添加图片资源加载
        // this.load.image('goose', 'assets/items/goose.png');
    }

    create() {
        this.scene.start('GameScene');
        this.scene.launch('UIScene');
    }
}
