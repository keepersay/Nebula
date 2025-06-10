class Config:
    # JWT配置
    SECRET_KEY = 'your-secret-key-here'  # 请在生产环境中修改为安全的密钥
    
    # 数据库配置
    DATABASE_URL = "mysql+pymysql://root:123456@localhost/cmdb"
    
    # 其他配置
    DEBUG = True 