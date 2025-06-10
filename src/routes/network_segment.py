from flask import Blueprint, jsonify, request
from init.database import get_db
from services.network_segment_service import NetworkSegmentService
from schemas.network_segment import NetworkSegmentCreate, NetworkSegmentUpdate, NetworkSegment as NetworkSegmentSchema

router = Blueprint('network_segment', __name__)

@router.route('/', methods=['POST'])
def create_network_segment():
    """
    创建新网络段
    请求体示例：
    {
        "name": "测试网络段1",
        "network": "192.168.1.0/24",
        "gateway": "192.168.1.1",
        "dns": "8.8.8.8,8.8.4.4",
        "description": "测试用网络段"
    }
    """
    try:
        # 获取请求数据
        data = request.get_json()
        
        # 创建网络段数据模型
        network_segment_data = NetworkSegmentCreate(**data)
        
        # 创建网络段
        db = get_db()
        try:
            network_segment_service = NetworkSegmentService(db)
            network_segment = network_segment_service.create_network_segment(network_segment_data)
            
            # 返回创建结果
            return jsonify({
                "code": 200,
                "message": "创建成功",
                "data": NetworkSegmentSchema.model_validate(network_segment).model_dump()
            })
        finally:
            db.close()
            
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"创建失败: {str(e)}"
        }), 500

@router.route('/', methods=['GET'])
def get_network_segments():
    """
    获取网络段列表
    支持分页：/api/network_segment/?page=1&page_size=20
    """
    # 分页参数
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
    except Exception:
        return jsonify({"code": 400, "message": "分页参数格式错误"}), 400
    
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 20
    if page_size > 1000:
        page_size = 1000
    
    # 计算偏移量
    skip = (page - 1) * page_size
    
    # 获取网络段列表
    db = get_db()
    try:
        network_segment_service = NetworkSegmentService(db)
        network_segments = network_segment_service.get_network_segments(skip=skip, limit=page_size)
        
        # 返回结果
        return jsonify({
            "code": 200,
            "message": "success",
            "data": [NetworkSegmentSchema.model_validate(ns).model_dump() for ns in network_segments],
            "page": page,
            "page_size": page_size
        })
    finally:
        db.close()

@router.route('/<int:network_segment_id>', methods=['GET'])
def get_network_segment(network_segment_id: int):
    """
    获取指定网络段
    """
    db = get_db()
    try:
        network_segment_service = NetworkSegmentService(db)
        network_segment = network_segment_service.get_network_segment(network_segment_id)
        
        # 返回结果
        return jsonify({
            "code": 200,
            "message": "success",
            "data": NetworkSegmentSchema.model_validate(network_segment).model_dump()
        })
    except ValueError as e:
        return jsonify({
            "code": 400,
            "message": str(e)
        }), 400
    finally:
        db.close()

@router.route('/<int:network_segment_id>', methods=['PUT'])
def update_network_segment(network_segment_id: int):
    """
    更新网络段信息
    请求体示例：
    {
        "name": "更新后的网络段名称",
        "description": "更新后的描述"
    }
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({"code": 400, "message": "请求体不能为空"}), 400
            
        # 验证请求数据
        if not isinstance(data, dict):
            return jsonify({"code": 400, "message": "请求体必须是JSON对象"}), 400
            
        # 检查是否至少提供了一个要更新的字段
        if not any(data.values()):
            return jsonify({"code": 400, "message": "至少需要提供一个要更新的字段"}), 400
            
        # 创建更新数据模型
        try:
            network_segment_data = NetworkSegmentUpdate(**data)
        except Exception as e:
            return jsonify({
                "code": 400,
                "message": f"请求数据格式错误: {str(e)}"
            }), 400
        
        # 更新网络段
        db = get_db()
        try:
            network_segment_service = NetworkSegmentService(db)
            network_segment = network_segment_service.update_network_segment(network_segment_id, network_segment_data)
            
            # 返回更新结果
            return jsonify({
                "code": 200,
                "message": "更新成功",
                "data": NetworkSegmentSchema.model_validate(network_segment).model_dump()
            })
        finally:
            db.close()
            
    except ValueError as e:
        # 处理网络段不存在的错误
        return jsonify({
            "code": 400,
            "message": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"更新失败: {str(e)}"
        }), 500

@router.route('/<int:network_segment_id>', methods=['DELETE'])
def delete_network_segment(network_segment_id: int):
    """
    删除网络段
    """
    db = get_db()
    try:
        network_segment_service = NetworkSegmentService(db)
        network_segment_service.delete_network_segment(network_segment_id)
        
        return jsonify({
            "code": 200,
            "message": "删除成功"
        })
    except ValueError as e:
        return jsonify({
            "code": 400,
            "message": str(e)
        }), 400
    finally:
        db.close() 