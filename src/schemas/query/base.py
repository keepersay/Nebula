from enum import Enum
from typing import List, Union, Literal, Optional, Dict, Type
from pydantic import BaseModel, Field
from datetime import datetime

class FieldType(str, Enum):
    STRING = "string"      # 字符串，支持 =, !=, like, in
    INTEGER = "integer"    # 整数，支持 =, !=, >, <, >=, <=, in
    FLOAT = "float"        # 浮点数，支持 =, !=, >, <, >=, <=, in
    BOOLEAN = "boolean"    # 布尔值，只支持 =, !=
    DATETIME = "datetime"  # 日期时间，支持 =, !=, >, <, >=, <=
    MULTI_SELECT = "multi_select"  # 多选，支持 in, =, !=
    ENUM = "enum"         # 枚举，支持 =, !=, in

class FieldConfig(BaseModel):
    """字段配置"""
    name: str
    type: FieldType
    description: str
    operators: List[str]  # 支持的操作符
    is_multi_select: bool = False  # 是否支持多选
    enum_values: Optional[List[str]] = None  # 如果是枚举类型，可选的值

class BaseQueryConfig:
    """基础查询配置类"""
    def __init__(self):
        self.fields: Dict[str, FieldConfig] = {}
    
    def add_field(self, name: str, field_config: FieldConfig):
        """添加字段配置"""
        self.fields[name] = field_config
    
    def get_field(self, name: str) -> FieldConfig:
        """获取字段配置"""
        if name not in self.fields:
            raise ValueError(f"不支持的字段: {name}")
        return self.fields[name]
    
    def get_all_fields(self) -> Dict[str, FieldConfig]:
        """获取所有字段配置"""
        return self.fields

class QueryCondition(BaseModel):
    """查询条件"""
    field: str
    operator: str
    value: Union[str, int, float, bool, List[Union[str, int, float]]]

    def validate_field(self, query_config: BaseQueryConfig):
        """验证字段和操作符"""
        field_config = query_config.get_field(self.field)
        if self.operator not in field_config.operators:
            raise ValueError(f"字段 {self.field} 不支持操作符: {self.operator}")
        
        # 验证值类型
        if field_config.type == FieldType.BOOLEAN:
            if not isinstance(self.value, bool):
                raise ValueError(f"字段 {self.field} 必须是布尔值")
        
        elif field_config.type == FieldType.INTEGER:
            if not isinstance(self.value, (int, list)):
                raise ValueError(f"字段 {self.field} 必须是整数或整数列表")
        
        elif field_config.type == FieldType.ENUM:
            if isinstance(self.value, list):
                if not all(v in field_config.enum_values for v in self.value):
                    raise ValueError(f"字段 {self.field} 的值必须是: {field_config.enum_values}")
            else:
                if self.value not in field_config.enum_values:
                    raise ValueError(f"字段 {self.field} 的值必须是: {field_config.enum_values}")
        
        # 验证多选
        if not field_config.is_multi_select and isinstance(self.value, list):
            raise ValueError(f"字段 {self.field} 不支持多选")

class QueryGroup(BaseModel):
    """查询条件组"""
    operator: Literal["AND", "OR"]
    conditions: List[Union["QueryGroup", QueryCondition]]

class Pagination(BaseModel):
    """分页参数"""
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=1000)

class BaseQuery(BaseModel):
    """基础查询参数"""
    query: Union[QueryGroup, QueryCondition]
    pagination: Pagination = Pagination()
    query_all: bool = False

class ServerQuery(BaseQuery):
    """服务器查询参数"""
    sort_field: Optional[str] = Field(default=None, description="排序字段")
    sort_order: Optional[Literal["asc", "desc"]] = Field(default="asc", description="排序顺序，asc 或 desc") 