from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
import logging

# 日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 数据库连接
DATABASE_URL = "mysql+pymysql://root:9i2TFyoVnIxjrLW@localhost/cmdb?charset=utf8mb4"

try:
    # 创建引擎
    engine = create_engine(
        DATABASE_URL,
        echo=True,
        pool_pre_ping=True
    )
    
    # 创建会话工厂
    SessionLocal = sessionmaker(autoflush=False, bind=engine)

    #  创建基类，所有模型都继承自Base
    Base = declarative_base()

    # 获取数据库会话
    def get_db():
        """
        获取数据库会话的生成器函数
        
        Returns:
            Session: 数据库会话对象
        """
        db = SessionLocal()
        try:
            return db
        except Exception as e:
            logger.error(f"数据库会话出错: {str(e)}")
            db.rollback()  # 发生错误时回滚事务
            raise  # 重新抛出异常以便上层处理
        finally:
            db.close()

    # 自动建表
    # def init_db():
    #     """
    #     自动创建所有模型对应的表结构
    #     """
    #     Base.metadata.create_all(bind=engine)

except Exception as e:
    logger.error(f"数据库连接失败: {e}")
    raise e
