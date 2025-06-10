from datetime import datetime, timedelta
import jwt
from config import Config

class AuthService:
    def __init__(self, db):
        self.db = db
    
    def login(self, username: str, password: str) -> dict:
        """
        用户登录
        :param username: 用户名
        :param password: 密码
        :return: 登录成功返回token和用户信息，失败返回None
        """
        # TODO: 从数据库验证用户名和密码
        # 这里暂时使用硬编码的测试账号
        if username == 'admin' and password == 'admin':
            # 生成token
            token = self._generate_token(username)
            return {
                'token': token,
                'user': {
                    'username': username,
                    'role': 'admin'
                }
            }
        return None
    
    def _generate_token(self, username: str) -> str:
        """
        生成JWT token
        :param username: 用户名
        :return: token字符串
        """
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(days=1)  # token有效期1天
        }
        return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256') 