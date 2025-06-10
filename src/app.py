from flask import Flask, request
from flask_restx import Api, Resource, fields
from routes.server import router as server_router, api as server_api
from routes.auth import router as auth_router, api as auth_api
# from routes.network_segment import router as network_segment_router
# from init.database import init_db

app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='CMDB API',
    description='CMDB系统API文档',
    doc='/api/docs'
)

# 注册API命名空间
api.add_namespace(server_api, path='/api/server')
api.add_namespace(auth_api, path='/api/auth')

# 注册路由
app.register_blueprint(server_router, url_prefix='/api/server')
app.register_blueprint(auth_router, url_prefix='/api/auth')
# app.register_blueprint(network_segment_router, url_prefix='/api/network_segment')

# 初始化数据库
# init_db()

if __name__ == '__main__':
    app.run(debug=True, port=8081)
