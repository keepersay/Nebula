from typing import Dict, Type
from .base import BaseQueryConfig
from .server import SERVER_QUERY_CONFIG

class QueryConfigFactory:
    """查询配置工厂"""
    _configs: Dict[str, BaseQueryConfig] = {
        "server": SERVER_QUERY_CONFIG,
        # 在这里添加其他模型的查询配置
        # "app": APP_QUERY_CONFIG,
        # "idc": IDC_QUERY_CONFIG,
        # "rack": RACK_QUERY_CONFIG,
    }
    
    @classmethod
    def get_config(cls, model_name: str) -> BaseQueryConfig:
        """获取指定模型的查询配置"""
        if model_name not in cls._configs:
            raise ValueError(f"不支持的模型: {model_name}")
        return cls._configs[model_name]
    
    @classmethod
    def register_config(cls, model_name: str, config: BaseQueryConfig):
        """注册新的查询配置"""
        cls._configs[model_name] = config
    
    @classmethod
    def get_all_configs(cls) -> Dict[str, BaseQueryConfig]:
        """获取所有查询配置"""
        return cls._configs 