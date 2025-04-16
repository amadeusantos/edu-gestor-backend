import math
from typing import List

from sqlalchemy.orm import Query

from api.schemas import PaginationSchema

def pagination(query: Query, page: int, size: int, filters: List, orders: List) -> PaginationSchema:
    query = query.where(*filters).order_by(*orders)
    total_items = query.count()
    total_pages = math.ceil(total_items / size)
    results = query.offset((page - 1) * size).limit(size).all()

    return {"total_items":total_items, "total_pages": total_pages, "page": page, "size": size, "results": results}
