from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from models.server import Server
from schemas.server import ServerCreate, ServerUpdate, ConflictError
from schemas.query import ServerQueryConfig, QueryGroup, QueryCondition, SERVER_QUERY_CONFIG
from datetime import datetime
from typing import Union, Optional
from schemas.query import FieldType
import traceback

from schemas.requests import ServerQueryRequest

class ServerService:
    def __init__(self, db: Session):
        self.db = db

    def create_server(self, server: ServerCreate):
        """
        创建新服务器
        
        Args:
            server: 服务器创建数据
            
        Returns:
            Server: 创建的服务器对象
            
        Raises:
            ConflictError: 当 service_tag 已存在时抛出
        """
        # 检查 service_tag 是否已存在
        existing_server = self.db.query(Server).filter(Server.service_tag == server.service_tag).first()
        if existing_server:
            raise ConflictError(f"service_tag '{server.service_tag}' 已存在")
            
        # 创建服务器实例
        db_server = Server(
            # 必填字段
            network_segment_id=server.network_segment_id,
            service_tag=server.service_tag,
            
            # 可选字段
            description=server.description,
            name=server.name,
            agent_name=server.agent_name,
            primary_ip=server.primary_ip,
            agent_ip=server.agent_ip,
            other_ip=server.other_ip,
            port=server.port,
            manage_card_ip=server.manage_card_ip,
            manage_card_mac=server.manage_card_mac,
            manage_card_version=server.manage_card_version,
            bios_version=server.bios_version,
            raid_fw_version=server.raid_fw_version,
            agent_version=server.agent_version,
            agent_kernel=server.agent_kernel,
            use_status=server.use_status,
            service_level=server.service_level,
            is_installing=server.is_installing,
            install_status=server.install_status,
            lock_status=server.lock_status,
            is_vm=server.is_vm,
            real_server_id=server.real_server_id,
            vm_type=server.vm_type,
            vm_network_type=server.vm_network_type,
            instance_name=server.instance_name,
            cpu_amount=server.cpu_amount,
            cpu_cores=server.cpu_cores,
            cpu_kernel_number=server.cpu_kernel_number,
            ram_amount=server.ram_amount,
            ram_size=server.ram_size,
            nic_amount=server.nic_amount,
            storage_amount=server.storage_amount,
            storage_info=server.storage_info,
            filesystem_disk_space=server.filesystem_disk_space,
            device_id=server.device_id,
            group_id=server.group_id,
            agent_os_id=server.agent_os_id,
            template_id=server.template_id,
            image_id=server.image_id,
            owner=server.owner,
            label=server.label,
            
            # 审计信息
            created_by="system",  # TODO: 从当前用户获取
            created_date=datetime.now(),
            last_modified_by="system",  # TODO: 从当前用户获取
            last_modified_date=datetime.now(),
            is_valid=True
        )
        
        # 保存到数据库
        self.db.add(db_server)
        self.db.commit()
        self.db.refresh(db_server)
        
        return db_server

    def build_query(self, query: Union[QueryGroup, QueryCondition], db_query):
        print(f"[build_query] called with: query={query}, type={type(query)}")
        if isinstance(query, QueryCondition):
            query.validate_field(SERVER_QUERY_CONFIG)
            field_config = SERVER_QUERY_CONFIG.get_field(query.field)
            field = getattr(Server, query.field)
            print(f"[build_query] field={query.field}, field_config.type={field_config.type}, operator={query.operator}, value={query.value}")
            # 根据字段类型和操作符构建查询
            if field_config.type == FieldType.STRING:
                if query.operator == "like":
                    print(f"[build_query] return: {field}.like(%{query.value}%)")
                    return field.like(f"%{query.value}%")
                elif query.operator == "in":
                    print(f"[build_query] return: {field}.in_({query.value})")
                    return field.in_(query.value)
                elif query.operator == "=":
                    print(f"[build_query] return: {field} == {query.value}")
                    return field == query.value
                elif query.operator == "!=":
                    print(f"[build_query] return: {field} != {query.value}")
                    return field != query.value
            
            elif field_config.type == FieldType.INTEGER:
                if query.operator == "in":
                    print(f"[build_query] return: {field}.in_({query.value})")
                    return field.in_(query.value)
                elif query.operator == "=":
                    print(f"[build_query] return: {field} == {query.value}")
                    return field == query.value
                elif query.operator == "!=":
                    print(f"[build_query] return: {field} != {query.value}")
                    return field != query.value
                elif query.operator == ">":
                    print(f"[build_query] return: {field} > {query.value}")
                    return field > query.value
                elif query.operator == "<":
                    print(f"[build_query] return: {field} < {query.value}")
                    return field < query.value
                elif query.operator == ">=":
                    print(f"[build_query] return: {field} >= {query.value}")
                    return field >= query.value
                elif query.operator == "<=":
                    print(f"[build_query] return: {field} <= {query.value}")
                    return field <= query.value

            elif field_config.type == FieldType.FLOAT:
                if query.operator == "in":
                    print(f"[build_query] return: {field}.in_({query.value})")
                    return field.in_(query.value)
                elif query.operator == "=":
                    print(f"[build_query] return: {field} == {query.value}")
                    return field == query.value
                elif query.operator == "!=":
                    print(f"[build_query] return: {field} != {query.value}")
                    return field != query.value
                elif query.operator == ">":
                    print(f"[build_query] return: {field} > {query.value}")
                    return field > query.value
                elif query.operator == "<":
                    print(f"[build_query] return: {field} < {query.value}")
                    return field < query.value
                elif query.operator == ">=":
                    print(f"[build_query] return: {field} >= {query.value}")
                    return field >= query.value
                elif query.operator == "<=":
                    print(f"[build_query] return: {field} <= {query.value}")
                    return field <= query.value

            elif field_config.type == FieldType.BOOLEAN:
                if query.operator == "=":
                    print(f"[build_query] return: {field} == {query.value}")
                    return field == query.value
                elif query.operator == "!=":
                    print(f"[build_query] return: {field} != {query.value}")
                    return field != query.value
            
            elif field_config.type == FieldType.DATETIME:
                if query.operator == "=":
                    print(f"[build_query] return: {field} == {query.value}")
                    return field == query.value
                elif query.operator == "!=":
                    print(f"[build_query] return: {field} != {query.value}")
                    return field != query.value
                elif query.operator == ">":
                    print(f"[build_query] return: {field} > {query.value}")
                    return field > query.value
                elif query.operator == "<":
                    print(f"[build_query] return: {field} < {query.value}")
                    return field < query.value
                elif query.operator == ">=":
                    print(f"[build_query] return: {field} >= {query.value}")
                    return field >= query.value
                elif query.operator == "<=":
                    print(f"[build_query] return: {field} <= {query.value}")
                    return field <= query.value
            
            elif field_config.type in [FieldType.ENUM, FieldType.MULTI_SELECT]:
                if query.operator == "in":
                    print(f"[build_query] return: {field}.in_({query.value})")
                    return field.in_(query.value)
                elif query.operator == "=":
                    print(f"[build_query] return: {field} == {query.value}")
                    return field == query.value
                elif query.operator == "!=":
                    print(f"[build_query] return: {field} != {query.value}")
                    return field != query.value
            # 新增异常抛出
            raise ValueError(f"不支持的字段类型或操作符: {query.field} {query.operator}")
        
        elif isinstance(query, QueryGroup):
            print(f"[build_query] QueryGroup: {query.conditions}")
            conditions = []
            for condition in query.conditions:
                cond = self.build_query(condition, db_query)
                print(f"[build_query] QueryGroup condition: {cond}")
                conditions.append(cond)
            
            if query.operator == "AND":
                print(f"[build_query] return: and_({conditions})")
                return and_(*conditions)
            else:  # OR
                print(f"[build_query] return: or_({conditions})")
                return or_(*conditions)
        # 新增异常抛出
        raise ValueError(f"不支持的查询类型: {type(query)}")

    def get_servers(self, server_query: ServerQueryRequest, sort_field: Optional[str] = None, sort_order: Optional[str] = None):
        """
        获取服务器列表，支持条件查询、排序和分页
        
        Args:
            server_query: 查询参数 (包含查询条件, 分页信息)
            sort_field: 排序字段
            sort_order: 排序顺序 ('asc' 或 'desc')
            
        Returns:
            dict: 包含服务器列表和总数的字典
        """
        try:
            # 构建基础查询
            db_query = self.db.query(Server)
            
            # 处理查询条件
            if server_query.query:
                query_condition = self.build_query(server_query.query, db_query)
                db_query = db_query.filter(query_condition) # 应用查询条件
            
            # 处理排序
            # 从方法参数中获取排序信息
            # sort_field = server_query.sort_field # Remove this line
            # sort_order = server_query.sort_order # Remove this line

            if sort_field:
                # 确保排序字段在 Server 模型中存在
                if not hasattr(Server, sort_field):
                     # 可以选择忽略排序，或者抛出错误
                     print(f"WARNING: Invalid sort field: {sort_field}. Ignoring sorting.")
                     # raise ValueError(f"不支持的排序字段: {sort_field}") # 如果选择抛出错误
                     pass # 忽略无效排序字段
                else:
                    field = getattr(Server, sort_field)
                    if sort_order and sort_order.lower() == 'desc':
                        db_query = db_query.order_by(field.desc())
                    else:
                        db_query = db_query.order_by(field.asc())
            
            # 获取总数
            total = db_query.count()
            
            # 处理分页
            if not server_query.query_all and server_query.pagination:
                db_query = db_query.offset((server_query.pagination.page - 1) * server_query.pagination.page_size).limit(server_query.pagination.page_size)
            
            # 执行查询
            servers = db_query.all()
            
            return {
                'items': servers,
                'total': total
            }
        except Exception as e:
            # 打印详细错误信息
            print('ERROR in get_servers:', str(e))
            print('TRACEBACK:', traceback.format_exc())
            raise # 重新抛出异常，让路由层处理

    def update_server(self, server_id: int, server: ServerUpdate):
        """
        更新服务器信息
        
        Args:
            server_id: 服务器ID
            server: 更新后的服务器信息
            
        Returns:
            Server: 更新后的服务器对象
            
        Raises:
            ValueError: 当服务器不存在或 service_tag 已存在时抛出
        """
        # 获取要更新的服务器
        db_server = self.db.query(Server).filter(Server.id == server_id).first()
        if not db_server:
            raise ValueError(f"服务器ID {server_id} 不存在")
            
        # 如果要更新 service_tag,需要检查唯一性
        if server.service_tag and server.service_tag != db_server.service_tag:
            existing_server = self.db.query(Server).filter(
                Server.service_tag == server.service_tag,
                Server.id != server_id  # 排除当前服务器
            ).first()
            if existing_server:
                raise ValueError(f"service_tag '{server.service_tag}' 已存在")
        
        # 更新服务器信息
        server_data = server.model_dump(exclude_unset=True)
        if not server_data:
            raise ValueError("没有提供任何要更新的字段")
            
        print(f"正在更新服务器 {server_id}，更新字段: {server_data}")  # 添加日志
        
        for key, value in server_data.items():
            if value is not None:  # 只更新非空值
                setattr(db_server, key, value)
                print(f"更新字段 {key}: {value}")  # 添加日志
            
        # 更新审计信息
        db_server.last_modified_by = "system"  # TODO: 从当前用户获取
        db_server.last_modified_date = datetime.now()
        
        try:
            # 保存更改
            self.db.commit()
            self.db.refresh(db_server)
            print(f"服务器 {server_id} 更新成功")  # 添加日志
            return db_server
        except Exception as e:
            self.db.rollback()  # 发生错误时回滚
            print(f"更新服务器 {server_id} 时发生错误: {str(e)}")  # 添加日志
            raise ValueError(f"更新服务器失败: {str(e)}")

    def delete_server(self, server_id: int) -> None:
        """删除服务器（物理删除）
        
        Args:
            server_id: 服务器ID
            
        Raises:
            ValueError: 当服务器不存在时
        """
        server = self.db.query(Server).filter(Server.id == server_id).first()
        if not server:
            raise ValueError(f"服务器ID {server_id} 不存在")
        
        # 物理删除：直接从数据库移除
        self.db.delete(server)
        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"删除服务器失败: {str(e)}")