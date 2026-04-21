"""
API依赖项
"""
from typing import Generator, Dict, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.db.session import get_db
from app.core.config import settings

# HTTP Bearer认证
security = HTTPBearer()


def get_db_dependency() -> Generator[Session, None, None]:
    """
    获取数据库会话依赖项
    """
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """
    验证JWT Token
    """
    if credentials.scheme != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(payload: Dict = Depends(verify_token)) -> Dict:
    """
    获取当前用户
    """
    # 这里可以添加更多的用户验证逻辑
    # 例如：检查用户是否在数据库中，是否被禁用等
    
    # 模拟用户数据，实际应用中应从数据库获取
    user = {
        "id": payload.get("sub", 1),
        "username": payload.get("username", "admin"),
        "email": payload.get("email", "admin@example.com"),
        "roles": payload.get("roles", ["admin"]),
        "permissions": payload.get("permissions", []),
    }
    
    return user


def get_current_active_user(current_user: Dict = Depends(get_current_user)) -> Dict:
    """
    获取当前活跃用户
    """
    # 这里可以检查用户状态，例如是否被禁用
    # 示例：if not current_user["is_active"]: raise HTTPException(...)
    
    return current_user


def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security, use_cache=False)
) -> Optional[Dict]:
    """
    可选获取当前用户（如果提供了Token）
    """
    if credentials is None:
        return None
    
    try:
        return get_current_user(credentials)
    except HTTPException:
        return None


# 权限检查装饰器
class PermissionChecker:
    """
    权限检查器
    """
    def __init__(self, required_permissions: list):
        self.required_permissions = required_permissions
    
    def __call__(self, current_user: Dict = Depends(get_current_active_user)):
        """
        检查用户是否有指定权限
        """
        user_permissions = current_user.get("permissions", [])
        
        # 检查是否有管理员角色
        if "admin" in current_user.get("roles", []):
            return current_user
        
        # 检查是否有足够的权限
        for permission in self.required_permissions:
            if permission not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"缺少权限: {permission}"
                )
        
        return current_user


# 常用的权限检查器
require_admin = PermissionChecker(["admin"])
require_company_read = PermissionChecker(["company:read"])
require_company_write = PermissionChecker(["company:write"])
require_certificate_read = PermissionChecker(["certificate:read"])
require_certificate_write = PermissionChecker(["certificate:write"])
require_alert_read = PermissionChecker(["alert:read"])
require_alert_write = PermissionChecker(["alert:write"])
require_report_read = PermissionChecker(["report:read"])


__all__ = [
    "get_db_dependency",
    "verify_token",
    "get_current_user",
    "get_current_active_user",
    "get_current_user_optional",
    "PermissionChecker",
    "require_admin",
    "require_company_read",
    "require_company_write",
    "require_certificate_read",
    "require_certificate_write",
    "require_alert_read",
    "require_alert_write",
    "require_report_read",
]