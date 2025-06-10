import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy import inspect
from src.init.database import engine

def show_table_structure():
    inspector = inspect(engine)
    columns = inspector.get_columns('server')
    
    print("服务器表结构：")
    print("-" * 80)
    for column in columns:
        print(f"字段名: {column['name']}")
        print(f"类型: {column['type']}")
        print(f"可空: {column['nullable']}")
        print(f"默认值: {column['default']}")
        print("-" * 80)

if __name__ == "__main__":
    show_table_structure() 