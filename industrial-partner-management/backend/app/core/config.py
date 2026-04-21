from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, field_validator, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "工贸企业相关方全流程管理系统"
    APP_VERSION: str = "1.0.0"
    APP_ENVIRONMENT: str = "development"
    APP_DEBUG: bool = False
    
    # API配置
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://partner_app:AppPassword@2024@localhost:3306/industrial_partner_management"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_PASSWORD: Optional[str] = None
    REDIS_MAX_CONNECTIONS: int = 20
    
    # JWT配置
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # 文件存储配置
    FILE_STORAGE_TYPE: str = "local"  # local, s3, oss, cos
    FILE_UPLOAD_DIR: str = "./uploads"
    FILE_MAX_SIZE_MB: int = 50
    FILE_ALLOWED_EXTENSIONS: List[str] = [".pdf", ".jpg", ".jpeg", ".png", ".doc", ".docx", ".xls", ".xlsx"]
    
    # 邮件配置
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_USE_TLS: bool = True
    EMAIL_FROM: Optional[str] = None
    
    # 证书预警配置
    CERTIFICATE_ALERT_DAYS: List[int] = [30, 15, 7]
    CERTIFICATE_ALERT_CRON: str = "0 9 * * *"  # 每天9点执行
    
    # 安全配置
    SECURITY_BCRYPT_ROUNDS: int = 12
    SECURITY_SALT_LENGTH: int = 32
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()