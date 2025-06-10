from sqlalchemy.orm import Session
from models.network_segment import NetworkSegment
from schemas.network_segment import NetworkSegmentCreate, NetworkSegmentUpdate
from datetime import datetime

class NetworkSegmentService:
    def __init__(self, db: Session):
        self.db = db

    def create_network_segment(self, network_segment: NetworkSegmentCreate):
        """
        创建新网络段
        
        Args:
            network_segment: 网络段创建数据
            
        Returns:
            NetworkSegment: 创建的网络段对象
        """
        # 创建网络段实例
        db_network_segment = NetworkSegment(
            name=network_segment.name,
            network=network_segment.network,
            gateway=network_segment.gateway,
            dns=network_segment.dns,
            description=network_segment.description,
            
            # 审计信息
            created_by="system",  # TODO: 从当前用户获取
            created_date=datetime.now(),
            last_modified_by="system",  # TODO: 从当前用户获取
            last_modified_date=datetime.now(),
            is_valid=True
        )
        
        # 保存到数据库
        self.db.add(db_network_segment)
        self.db.commit()
        self.db.refresh(db_network_segment)
        
        return db_network_segment

    def get_network_segments(self, skip: int = 0, limit: int = 100):
        """
        获取网络段列表
        
        Args:
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            List[NetworkSegment]: 网络段列表
        """
        return self.db.query(NetworkSegment).offset(skip).limit(limit).all()

    def get_network_segment(self, network_segment_id: int):
        """
        获取指定网络段
        
        Args:
            network_segment_id: 网络段ID
            
        Returns:
            NetworkSegment: 网络段对象
            
        Raises:
            ValueError: 当网络段不存在时抛出
        """
        network_segment = self.db.query(NetworkSegment).filter(NetworkSegment.id == network_segment_id).first()
        if not network_segment:
            raise ValueError(f"网络段 ID {network_segment_id} 不存在")
        return network_segment

    def update_network_segment(self, network_segment_id: int, network_segment: NetworkSegmentUpdate):
        """
        更新网络段信息
        
        Args:
            network_segment_id: 网络段ID
            network_segment: 网络段更新数据
            
        Returns:
            NetworkSegment: 更新后的网络段对象
            
        Raises:
            ValueError: 当网络段不存在时抛出
        """
        db_network_segment = self.get_network_segment(network_segment_id)
        
        # 更新字段
        update_data = network_segment.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_network_segment, field, value)
        
        # 更新审计信息
        db_network_segment.last_modified_by = "system"  # TODO: 从当前用户获取
        db_network_segment.last_modified_date = datetime.now()
        
        # 保存到数据库
        self.db.commit()
        self.db.refresh(db_network_segment)
        
        return db_network_segment

    def delete_network_segment(self, network_segment_id: int):
        """
        删除网络段
        
        Args:
            network_segment_id: 网络段ID
            
        Raises:
            ValueError: 当网络段不存在时抛出
        """
        db_network_segment = self.get_network_segment(network_segment_id)
        
        # 软删除
        db_network_segment.is_valid = False
        db_network_segment.last_modified_by = "system"  # TODO: 从当前用户获取
        db_network_segment.last_modified_date = datetime.now()
        
        # 保存到数据库
        self.db.commit() 