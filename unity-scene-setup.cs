// Unity 编辑器自动化脚本 - 创建基础场景与物品系统
// 使用方法：在 Unity 中创建新 C# 脚本，粘贴此代码，然后运行

using UnityEngine;
using UnityEditor;

public class GrabGooseSceneSetup : EditorWindow
{
    [MenuItem("Tools/GrabGoose/创建基础场景")]
    public static void CreateBaseScene()
    {
        // 1. 创建新场景
        Scene newScene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene);
        newScene.name = "MainGame";
        
        // 2. 创建 GameContainer
        GameObject gameContainer = new GameObject("GameContainer");
        gameContainer.transform.position = Vector3.zero;
        gameContainer.transform.rotation = Quaternion.identity;
        
        // 3. 创建 ItemPool
        GameObject itemPool = GameObject.CreatePrimitive(PrimitiveType.Cube);
        itemPool.name = "ItemPool";
        itemPool.transform.parent = gameContainer.transform;
        itemPool.transform.localScale = new Vector3(10, 0.5f, 10);
        itemPool.transform.position = new Vector3(0, -3, 0);
        
        // 4. 创建正交相机
        Camera mainCamera = Camera.main;
        if (mainCamera == null)
        {
            mainCamera = new GameObject("MainCamera").AddComponent<Camera>();
        }
        mainCamera.name = "MainCamera";
        mainCamera.orthographic = true;
        mainCamera.orthographicSize = 8;
        mainCamera.transform.position = new Vector3(0, 15, 0);
        mainCamera.transform.rotation = Quaternion.Euler(90, 0, 0);
        
        // 5. 创建方向光
        DirectionalLight light = FindObjectOfType<DirectionalLight>();
        if (light == null)
        {
            GameObject lightObj = new GameObject("Directional Light");
            light = lightObj.AddComponent<DirectionalLight>();
        }
        light.transform.rotation = Quaternion.Euler(50, -30, 0);
        light.intensity = 1.2f;
        
        // 6. 保存场景
        string scenePath = "Assets/Scenes/MainGame.unity";
        System.IO.Directory.CreateDirectory("Assets/Scenes");
        EditorSceneManager.SaveScene(newScene, scenePath);
        
        Debug.Log("✅ 基础场景创建完成！");
        Debug.Log($"📁 场景已保存到：{scenePath}");
        
        // 7. 截图（可选）
        CaptureScreenshot();
    }
    
    static void CaptureScreenshot()
    {
        string screenshotPath = "Assets/Screenshots/scene_setup_" + System.DateTime.Now.ToString("yyyyMMdd_HHmmss") + ".png";
        System.IO.Directory.CreateDirectory("Assets/Screenshots");
        
        // 等待一帧后截图
        EditorApplication.delayCall += () =>
        {
            Texture2D screenshot = ScreenCapture.CaptureScreenshotAsTexture();
            byte[] bytes = screenshot.EncodeToPNG();
            System.IO.File.WriteAllBytes(screenshotPath, bytes);
            Debug.Log($"📸 截图已保存：{screenshotPath}");
        };
    }
}
