from pydantic import BaseModel, Field
from typing import Optional
from .query import QueryGroup, Pagination

class ServerQueryRequest(BaseModel):
    query: QueryGroup
    pagination: Pagination
    query_all: Optional[bool] = Field(default=False, description="是否查询全部数据，忽略分页")
    # Add other fields if necessary, like sort_field and sort_order if they are part of the payload 