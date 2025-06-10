from flask import Blueprint, request
from flask_restx import Resource, fields, Namespace
from init.database import get_db
from services.server_service import ServerService
from schemas.server import ServerCreate, ServerUpdate, Server as ServerSchema
from schemas.query import QueryCondition, QueryGroup, Pagination, ServerQueryConfig
from schemas.requests import ServerQueryRequest
from pydantic import BaseModel, ValidationError
import traceback
from datetime import datetime

class Sort(BaseModel):
    field: str
    order: str

router = Blueprint('server', __name__)
api = Namespace('server', description='服务器管理接口')

# 定义API模型
server_model = api.model('Server', {
    'id': fields.Integer(description='服务器ID'),
    'hostname': fields.String(required=True, description='主机名'),
    'ip_address': fields.String(required=True, description='IP地址'),
    'os_type': fields.String(required=True, description='操作系统类型'),
    'os_version': fields.String(required=True, description='操作系统版本'),
    'cpu_cores': fields.Integer(required=True, description='CPU核心数'),
    'memory_size': fields.Integer(required=True, description='内存大小(GB)'),
    'disk_size': fields.Integer(required=True, description='磁盘大小(GB)'),
    'status': fields.String(required=True, description='服务器状态'),
    'description': fields.String(description='描述'),
    'created_date': fields.DateTime(description='创建时间'),
    'last_modified_date': fields.DateTime(description='最后修改时间')
})

server_create_model = api.model('ServerCreate', {
    'service_tag': fields.String(required=True, description='设备序列号'),
    'name': fields.String(description='服务器名'),
    'primary_ip': fields.String(description='主IP'),
    'agent_ip': fields.String(description='Agent抓取IP'),
    'ram_size': fields.Integer(description='内存大小(G)'),
    'cpu_cores': fields.Integer(description='CPU物理核总数'),
    'storage_info': fields.String(description='存储配置'),
    'description': fields.String(description='描述')
})

server_update_model = api.model('ServerUpdate', {
    'service_tag': fields.String(description='设备序列号'),
    'name': fields.String(description='服务器名'),
    'primary_ip': fields.String(description='主IP'),
    'agent_ip': fields.String(description='Agent抓取IP'),
    'ram_size': fields.Integer(description='内存大小(G)'),
    'cpu_cores': fields.Integer(description='CPU物理核总数'),
    'storage_info': fields.String(description='存储配置'),
    'description': fields.String(description='描述')
})

query_model = api.model('Query', {
    'operator': fields.String(required=True, description='操作符', enum=['AND', 'OR']),
    'conditions': fields.List(fields.Nested(api.model('Condition', {
        'field': fields.String(required=True, description='字段名'),
        'operator': fields.String(required=True, description='操作符'),
        'value': fields.Raw(required=True, description='值')
    })))
})

pagination_model = api.model('Pagination', {
    'page': fields.Integer(required=True, description='页码'),
    'page_size': fields.Integer(required=True, description='每页条数')
})

server_query_model = api.model('ServerQuery', {
    'query': fields.Nested(query_model, required=True, description='查询条件'),
    'pagination': fields.Nested(pagination_model, required=True, description='分页信息')
})

@api.route('/')
class ServerList(Resource):
    @api.doc('获取服务器列表')
    @api.param('page', '页码', type=int, default=1)
    @api.param('page_size', '每页数量', type=int, default=10)
    @api.param('sort_field', '排序字段')
    @api.param('sort_order', '排序顺序', enum=['asc', 'desc'])
    @api.response(200, '成功')
    def get(self):
        """获取服务器列表"""
        try:
            page = int(request.args.get('page', 1))
            page_size = int(request.args.get('page_size', 10))
            sort_field = request.args.get('sort_field')
            sort_order = request.args.get('sort_order', 'asc')

            # 构建查询条件 (从URL参数中提取简单过滤条件)
            conditions = []
            for key, value in request.args.items():
                if key not in ['page', 'page_size', 'sort_field', 'sort_order']:
                    conditions.append(QueryCondition(field=key, operator='=', value=value))

            query_group = QueryGroup(operator='AND', conditions=conditions)
            pagination = Pagination(page=page, page_size=page_size)

            # 构建 ServerQueryRequest 对象
            server_query_obj = ServerQueryRequest(
                query=query_group,
                pagination=pagination,
            )

            db = get_db()
            try:
                server_service = ServerService(db)
                # 将 ServerQueryRequest 对象以及 sort_field 和 sort_order 传给 service
                # Note: The get_servers method in service layer might need to be updated
                # to accept ServerQueryRequest instead of ServerQueryConfig.
                result = server_service.get_servers(server_query_obj, sort_field=sort_field, sort_order=sort_order)

                return {
                    'code': 200,
                    'message': 'success',
                    'data': to_serializable([ServerSchema.model_validate(server).model_dump() for server in result['items']]),
                    'total': result['total'],
                    'page': page,
                    'page_size': page_size
                }
            finally:
                # 恢复数据库连接关闭
                db.close()

        except Exception as e:
            # 打印详细错误信息
            print('ERROR in GET /api/server/query:', str(e))
            print('TRACEBACK:', traceback.format_exc())
            return {
                'code': 500,
                'message': f'获取服务器列表失败: {str(e)}'
            }, 500

    @api.doc('创建服务器')
    @api.expect(server_create_model)
    @api.response(201, '创建成功')
    def post(self):
        """创建服务器"""
        try:
            data = request.get_json()
            # 使用 ServerCreate 模型验证和解析输入数据
            server_data = ServerCreate(**data)

            db = get_db()
            try:
                server_service = ServerService(db)
                # 将解析后的 ServerCreate 模型实例传递给 service 层
                server = server_service.create_server(server_data)
                db.commit() # 在这里提交事务
                return {
                    'code': 201,
                    'message': '创建成功',
                    'data': to_serializable(ServerSchema.model_validate(server).model_dump())
                }, 201
            except Exception as e:
                db.rollback() # 回滚事务
                # 记录详细错误日志
                print('ERROR creating server (DB transaction error):', str(e))
                print('TRACEBACK:', traceback.format_exc())
                return {
                    'code': 500,
                    'message': f'创建服务器失败: {str(e)}'
                }, 500
            finally:
                db.close()

        except ValidationError as e:
            # 输入数据验证失败
            print('ERROR creating server (Validation Error):', str(e))
            print('TRACEBACK:', traceback.format_exc())
            return {
                'code': 400,
                'message': f'请求数据验证失败: {e}'
            }, 400
        except ConflictError as e:
            # 资源冲突错误
            print('ERROR creating server (Conflict Error):', str(e))
            print('TRACEBACK:', traceback.format_exc())
            return {
                'code': 409,
                'message': str(e)
            }, 409
        except Exception as e:
            # 捕获其他潜在的异常
            print('ERROR creating server (Unexpected Error):', str(e))
            print('TRACEBACK:', traceback.format_exc())
            return {
                'code': 500,
                'message': f'创建服务器失败: {str(e)}'
            }, 500

@api.route('/<int:id>')
@api.param('id', '服务器ID')
class Server(Resource):
    @api.doc('获取服务器详情')
    @api.response(200, '成功')
    @api.response(404, '服务器不存在')
    def get(self, id):
        """获取服务器详情"""
        try:
            db = get_db()
            try:
                server_service = ServerService(db)
                
                # 构建 ServerQueryRequest 对象 for fetching by ID
                query_condition = QueryCondition(field='id', operator='=', value=id)
                server_query_obj = ServerQueryRequest(
                    query=QueryGroup(operator="AND", conditions=[query_condition]), # Wrap condition in QueryGroup
                    pagination=Pagination(page=1, page_size=1)
                )
                
                # 调用 get_servers 方法，并期望返回一条记录
                # Note: The get_servers method in service layer might need to be updated
                # to accept ServerQueryRequest instead of ServerQueryConfig.
                result = server_service.get_servers(server_query_obj)
                server = result['items'][0] if result['items'] else None
                
                if server:
                    return {
                        'code': 200,
                        'message': 'success',
                        'data': to_serializable(ServerSchema.model_validate(server).model_dump())
                    }
                else:
                    return {
                        'code': 404,
                        'message': '服务器不存在'
                    }, 404
            finally:
                db.close()
                
        except Exception as e:
            # 打印详细错误信息
            print('ERROR in GET /api/server/<int:id>:', str(e))
            print('TRACEBACK:', traceback.format_exc())
            return {
                'code': 500,
                'message': f'获取服务器详情失败: {str(e)}'
            }, 500

    @api.doc('更新服务器')
    @api.expect(server_update_model)
    @api.response(200, '更新成功')
    @api.response(404, '服务器不存在')
    def put(self, id):
        """更新服务器"""
        try:
            data = request.get_json()
            # 使用 ServerUpdate 模型验证和解析输入数据
            server_data = ServerUpdate(**data)
            
            db = get_db()
            try:
                server_service = ServerService(db)
                server = server_service.update_server(id, server_data)
                
                if server:
                    return {
                        'code': 200,
                        'message': '更新成功',
                        'data': to_serializable(ServerSchema.model_validate(server).model_dump())
                    }
                else:
                    return {
                        'code': 404,
                        'message': '服务器不存在'
                    }, 404
            finally:
                db.close()
                
        except ValidationError as e:
            # 输入数据验证失败
            print('ERROR updating server (Validation Error):', str(e))
            print('TRACEBACK:', traceback.format_exc())
            return {
                'code': 400,
                'message': f'请求数据验证失败: {e}'
            }, 400
        except ValueError as e:
            # 业务逻辑错误
            print('ERROR updating server (Value Error):', str(e))
            print('TRACEBACK:', traceback.format_exc())
            return {
                'code': 400,
                'message': str(e)
            }, 400
        except Exception as e:
            # 捕获其他潜在的异常
            print('ERROR updating server (Unexpected Error):', str(e))
            print('TRACEBACK:', traceback.format_exc())
            return {
                'code': 500,
                'message': f'更新服务器失败: {str(e)}'
            }, 500

    @api.doc('删除服务器')
    @api.response(200, '删除成功')
    @api.response(404, '服务器不存在')
    @api.response(500, '删除失败')
    def delete(self, id):
        """删除服务器"""
        db = get_db()
        try:
            server_service = ServerService(db)
            server_service.delete_server(id)
            return {
                'code': 200,
                'message': '删除成功'
            }
        except ValueError as e:
            print('ERROR deleting server (Value Error):', str(e))
            print('TRACEBACK:', traceback.format_exc())
            if "服务器ID" in str(e) and "不存在" in str(e):
                 return {
                    'code': 404,
                    'message': str(e)
                }, 404
            else:
                return {
                    'code': 400,
                    'message': f'删除服务器失败: {str(e)}'
                }, 400
        except Exception as e:
            print('ERROR deleting server (Unexpected Error):', str(e))
            print('TRACEBACK:', traceback.format_exc())
            return {
                'code': 500,
                'message': f'删除服务器失败: {str(e)}'
            }, 500
        finally:
            db.close()

@api.route('/fields')
class ServerFields(Resource):
    @api.doc('获取字段配置')
    @api.response(200, '获取成功')
    def get(self):
        """获取字段配置信息"""
        fields_dict = ServerQueryConfig().get_all_fields()
        # Convert FieldConfig objects to dictionaries
        serialized_fields = {name: field.model_dump() for name, field in fields_dict.items()}
        return {
            "code": 200,
            "message": "成功",
            "data": serialized_fields
        }, 200

@api.route('/query')
class ServerQueryResource(Resource):
    @api.doc('高级查询')
    # Use the ServerQueryRequest model for validation
    @api.expect(api.model('ServerQuery', {
        'query': fields.Nested(api.model('Query', {
            'operator': fields.String(required=True, description='操作符', enum=['AND', 'OR']),
            'conditions': fields.List(fields.Nested(api.model('Condition', {
                'field': fields.String(required=True, description='字段名'),
                'operator': fields.String(required=True, description='操作符'),
                'value': fields.Raw(required=True, description='值')
            })))
        })),
        'pagination': fields.Nested(api.model('Pagination', {
            'page': fields.Integer(required=True, description='页码'),
            'page_size': fields.Integer(required=True, description='每页条数')
        }))
    })) # Keep flask_restx model for API documentation
    @api.response(200, '查询成功')
    @api.response(500, '查询失败')
    def post(self):
        """高级查询"""
        try:
            data = request.get_json()
            # Validate input data using the Pydantic model
            query_request = ServerQueryRequest(**data)

            db = get_db()
            try:
                server_service = ServerService(db)
                # Pass the validated ServerQueryRequest object to the service
                # Note: The get_servers method in service layer might need to be updated
                # to accept ServerQueryRequest instead of ServerQueryConfig.
                result = server_service.get_servers(query_request)

                return {
                    'code': 200,
                    'message': 'success',
                    'data': to_serializable([ServerSchema.model_validate(server).model_dump() for server in result['items']]),
                    'total': result['total'],
                    'page': query_request.pagination.page,
                    'page_size': query_request.pagination.page_size
                }
            finally:
                db.close()
                
        except ValidationError as e:
            # 输入数据验证失败
            print('ERROR in POST /api/server/query (Validation Error):', str(e))
            print('TRACEBACK:', traceback.format_exc())
            return {
                'code': 400,
                'message': f'请求数据验证失败: {e}'
            }, 400
        except Exception as e:
            # 捕获其他潜在的异常
            print('ERROR in POST /api/server/query (Unexpected Error):', str(e))
            print('TRACEBACK:', traceback.format_exc())
            return {
                'code': 500,
                'message': f'高级查询失败: {str(e)}'
            }, 500

def to_serializable(obj):
    if isinstance(obj, dict):
        return {k: to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_serializable(i) for i in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return obj


