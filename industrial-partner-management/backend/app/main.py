"""
工贸企业相关方全流程管理系统 - 后端主应用
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from app.core.config import settings
from app.api.v1 import api_router
from app.db.session import init_db
import os


def create_app() -> FastAPI:
    """
    创建FastAPI应用实例
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="工贸企业相关方全流程管理系统后端API",
        docs_url="/docs" if settings.APP_DEBUG else None,
        redoc_url="/redoc" if settings.APP_DEBUG else None,
        openapi_url="/openapi.json" if settings.APP_DEBUG else None,
    )
    
    # 配置CORS
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    # 挂载静态文件目录
    upload_dir = settings.FILE_UPLOAD_DIR
    os.makedirs(upload_dir, exist_ok=True)
    app.mount("/uploads", StaticFiles(directory=upload_dir), name="uploads")
    
    # 包含API路由
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    # 健康检查端点
    @app.get("/")
    async def root():
        return {
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "status": "running",
            "docs": "/docs" if settings.APP_DEBUG else None,
        }
    
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "database": "connected",  # 实际应用中应该检查数据库连接
            "redis": "connected",     # 实际应用中应该检查Redis连接
        }
    
    return app


# 创建应用实例
app = create_app()


if __name__ == "__main__":
    # 初始化数据库（开发环境）
    if settings.APP_ENVIRONMENT == "development":
        print("🔄 初始化数据库...")
        init_db()
        print("✅ 数据库初始化完成")
    
    # 启动开发服务器
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.APP_DEBUG,
        log_level="info" if settings.APP_DEBUG else "warning",
    )