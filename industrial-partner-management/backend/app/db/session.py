from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from app.core.config import settings
import redis

# 创建SQLAlchemy引擎
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,
    echo=settings.APP_DEBUG
)

# 创建Session工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建Redis连接池
redis_pool = None
if settings.REDIS_URL:
    redis_pool = redis.ConnectionPool.from_url(
        settings.REDIS_URL,
        password=settings.REDIS_PASSWORD,
        max_connections=settings.REDIS_MAX_CONNECTIONS,
        decode_responses=True
    )

# 声明基类
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    获取数据库会话
    使用示例：
        db = next(get_db())
        # 使用db进行数据库操作
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis():
    """
    获取Redis连接
    """
    if redis_pool:
        return redis.Redis(connection_pool=redis_pool)
    return None


def init_db():
    """
    初始化数据库，创建所有表
    """
    from app.models.company import Company, CompanyCertificate
    from app.models.alert import CertificateAlert, CertificateAlertLog
    from app.models.file import FileStorage
    
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建完成")


def drop_db():
    """
    删除所有表（开发环境使用）
    """
    Base.metadata.drop_all(bind=engine)
    print("⚠️ 数据库表已删除")


if __name__ == "__main__":
    # 测试数据库连接
    try:
        db = next(get_db())
        print("✅ 数据库连接成功")
        db.close()
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
    
    # 测试Redis连接
    if redis_pool:
        try:
            r = get_redis()
            r.ping()
            print("✅ Redis连接成功")
        except Exception as e:
            print(f"❌ Redis连接失败: {e}")