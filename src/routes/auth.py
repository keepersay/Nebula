from flask import Blueprint, request
from flask_restx import Resource, fields, Namespace
from init.database import get_db
from services.auth_service import AuthService

router = Blueprint('auth', __name__)
api = Namespace('auth', description='认证相关接口')

# 定义API模型
login_model = api.model('Login', {
    'username': fields.String(required=True, description='用户名'),
    'password': fields.String(required=True, description='密码')
})

@api.route('/login')
class Login(Resource):
    @api.doc('用户登录')
    @api.expect(login_model)
    @api.response(200, '登录成功')
    @api.response(401, '登录失败')
    def post(self):
        """用户登录接口"""
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return {
                    'code': 401,
                    'message': '用户名和密码不能为空'
                }, 401
            
            db = get_db()
            try:
                auth_service = AuthService(db)
                result = auth_service.login(username, password)
                
                if result:
                    return {
                        'code': 200,
                        'message': '登录成功',
                        'data': result
                    }
                else:
                    return {
                        'code': 401,
                        'message': '用户名或密码错误'
                    }, 401
            finally:
                db.close()
                
        except Exception as e:
            return {
                'code': 500,
                'message': f'登录失败: {str(e)}'
            }, 500 