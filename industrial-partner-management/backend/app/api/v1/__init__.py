"""
API v1 路由模块
"""
from fastapi import APIRouter
from app.api.v1.endpoints import companies, certificates, alerts, stats, health

# 创建主路由器
api_router = APIRouter()

# 注册子路由
api_router.include_router(companies.router, prefix="/companies", tags=["单位管理"])
api_router.include_router(certificates.router, prefix="/certificates", tags=["证照管理"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["预警管理"])
api_router.include_router(stats.router, prefix="/stats", tags=["统计分析"])
api_router.include_router(health.router, prefix="/health", tags=["健康检查"])

__all__ = ["api_router"]