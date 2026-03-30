// 等待 DOM 加载完成
window.addEventListener('DOMContentLoaded', () => {
    const config = {
        type: Phaser.AUTO,
        parent: 'game-container',
        width: 450,
        height: 800,
        backgroundColor: '#f0f0f0',
        scale: {
            mode: Phaser.Scale.FIT,
            autoCenter: Phaser.Scale.CENTER_BOTH
        },
        scene: [BootScene, GameScene, UIScene],
        physics: {
            default: 'arcade',
            arcade: {
                gravity: { y: 0 },
                debug: false
            }
        },
        callbacks: {
            postBoot: () => {
                document.getElementById('loading').style.display = 'none';
            }
        }
    };

    const game = new Phaser.Game(config);
    
    // 错误处理
    window.addEventListener('error', (e) => {
        console.error('游戏加载错误:', e.message);
        document.getElementById('loading').innerHTML = '加载失败，请刷新重试<br><small>' + e.message + '</small>';
    });
});
