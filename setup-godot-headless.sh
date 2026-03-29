#!/bin/bash
# Godot 无头模式安装和场景创建脚本
# Godot 支持命令行无头运行，适合服务器环境

set -e

echo "🚀 安装 Godot 引擎（无头模式）..."

# 1. 下载 Godot 4.2（支持无头模式）
echo "📦 下载 Godot 4.2..."
cd /tmp
wget -q https://github.com/godotengine/godot/releases/download/4.2-stable/Godot_v4.2-stable_linux.x86_64.zip -O godot.zip
unzip -q godot.zip
chmod +x Godot_v4.2-stable_linux.x86_64
mv Godot_v4.2-stable_linux.x86_64 /usr/local/bin/godot

echo "✅ Godot 安装完成！"
godot --version

# 2. 创建项目
echo "📁 创建 GrabGoose 项目..."
mkdir -p ~/Projects/GrabGoose/{scenes,scripts,assets}
cd ~/Projects/GrabGoose

# 3. 创建项目配置文件
cat > project.godot << 'EOF'
; Engine configuration file.
; It's best edited using the editor UI and not directly,
; but it can also be edited manually.

config_version=5

[application]

config/name="GrabGoose"
run/main_scene="res://scenes/MainGame.tscn"
config/features=PackedStringArray("4.2", "Forward Plus")
config/icon="res://icon.svg"

[rendering]

renderer/rendering_method="gl_compatibility"
EOF

# 4. 创建基础场景（GDScript）
cat > scenes/MainGame.tscn << 'EOF'
[gd_scene load_steps=3 format=3 uid="uid://main_game"]

[ext_resource type="Script" path="res://scripts/GameController.gd" id="1_controller"]

[node name="MainGame" type="Node3D"]
script = ExtResource("1_controller")

[node name="GameContainer" type="Node3D"]
position = Vector3(0, 0, 0)

[node name="ItemPool" type="MeshInstance3D" parent="GameContainer"]
position = Vector3(0, -3, 0)
scale = Vector3(10, 0.5, 10)
mesh = SubResource("BoxMesh_pool")

[sub_resource type="BoxMesh" uid="uid://pool_mesh"]
size = Vector3(10, 0.5, 10)

[node name="MainCamera" type="Camera3D" parent="GameContainer"]
position = Vector3(0, 15, 0)
rotation = Vector3(1.5708, 0, 0)  # 90 degrees in radians
fov = 75.0
size = 8.0

[node name="DirectionalLight" type="DirectionalLight3D" parent="GameContainer"]
rotation = Vector3(0.8727, -0.5236, 0)  # 50, -30 degrees
light_energy = 1.2

[node name="WorldEnvironment" type="WorldEnvironment"]
environment = SubResource("Environment_default")

[sub_resource type="Environment" uid="uid://env_default"]
ambient_light_source = 2
ambient_light_color = Color(0.2, 0.2, 0.2, 1)
EOF

# 5. 创建游戏控制器脚本
cat > scripts/GameController.gd << 'EOF'
extends Node3D

@export var item_count: int = 20
@export var item_types: Array[String] = ["🦢", "🐥", "🥕", "🥚", "🌽"]

func _ready():
	print("✅ GrabGoose 游戏已启动！")
	print(f"📊 物品数量：{item_count}")
	print(f"🎨 物品种类：{item_types.size()}")
	spawn_items()

func spawn_items():
	print("🎮 正在生成物品...")
	for i in range(item_count):
		var item_type = item_types[randi() % item_types.size()]
		var x = randf_range(-4, 4)
		var y = randf_range(-2, 2)
		var z = randf_range(-4, 4)
		print(f"  生成物品 {i+1}: {item_type} @ ({x:.1f}, {y:.1f}, {z:.1f})")
	print("✅ 物品生成完成！")
EOF

echo "✅ 项目创建完成！"
echo ""
echo "📂 项目位置：~/Projects/GrabGoose"
echo ""
echo "🎮 运行游戏（无头模式）："
echo "   godot --headless --path ~/Projects/GrabGoose"
echo ""
echo "📸 渲染截图："
echo "   godot --headless --path ~/Projects/GrabGoose --screenshot"
echo ""

# 6. 测试运行
echo "🎮 测试运行游戏..."
godot --headless --path ~/Projects/GrabGoose --quit 2>&1 | head -20

echo ""
echo "✅ Godot 无头模式设置完成！"
