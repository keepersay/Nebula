from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class NetworkSegmentBase(BaseModel):
    """网络段基本信息"""
    name: str = Field(description="网络段名称")
    network: str = Field(description="网段地址")
    gateway: str = Field(description="网关地址")
    dns: str = Field(description="DNS服务器")
    description: str = Field(default="", description="描述")

class NetworkSegmentCreate(NetworkSegmentBase):
    """创建网络段时的请求数据"""
    pass

class NetworkSegmentUpdate(BaseModel):
    """更新网络段时的请求数据"""
    name: Optional[str] = None
    network: Optional[str] = None
    gateway: Optional[str] = None
    dns: Optional[str] = None
    description: Optional[str] = None

class NetworkSegment(NetworkSegmentBase):
    """网络段响应数据"""
    id: int
    created_by: str
    created_date: datetime
    last_modified_by: str
    last_modified_date: datetime
    is_valid: bool

    class Config:
        from_attributes = True 