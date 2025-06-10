from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from init.database import Base

class NetworkSegment(Base):
    """
    网络段信息模型类
    用于存储和管理网络段的基本信息
    """
    __tablename__ = "network_segment"  # 数据库表名

    # 基本信息
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)  # 主键ID
    name: Mapped[str] = mapped_column(String(100), default="")  # 网络段名称
    network: Mapped[str] = mapped_column(String(100), default="")  # 网段地址
    gateway: Mapped[str] = mapped_column(String(100), default="")  # 网关地址
    dns: Mapped[str] = mapped_column(String(200), default="")  # DNS服务器
    description: Mapped[str] = mapped_column(Text)  # 描述

    # 审计信息
    created_by: Mapped[str] = mapped_column(String(20), default="")  # 创建人
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)  # 创建时间
    last_modified_by: Mapped[str] = mapped_column(String(20), default="")  # 最后修改人
    last_modified_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)  # 最后修改时间
    is_valid: Mapped[bool] = mapped_column(Boolean, default=True)  # 是否有效

    def __repr__(self):
        return f"<NetworkSegment(id={self.id}, name={self.name})>" 