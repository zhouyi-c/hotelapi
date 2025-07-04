from fastapi import HTTPException
from models.hotel_model import get_hotels

def filter_hotels(min_price: int, max_price: int, date: str = None):
    """根据价格和日期过滤酒店"""
    try:
        hotels = [h.to_dict() for h in get_hotels()]
        results = [h for h in hotels if min_price <= h["price"] <= max_price]
        if date:
            results = [h for h in results if h["date"] == date]
        return {"hotels": results}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"酒店查询失败: {str(e)}"
        )