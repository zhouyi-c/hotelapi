from fastapi import HTTPException
from models.hotel_model import get_hotels

def filter_hotels(min_price: int, max_price: int, date: str = None):
    """
    酒店筛选服务：根据价格区间和日期过滤酒店。
    建议仅作为业务调度层，将具体查询逻辑下沉到工具或Agent层。
    :param min_price: 最低价（int）
    :param max_price: 最高价（int）
    :param date: 可选，入住日期（str，格式YYYY-MM-DD）
    :return: dict，包含筛选结果
    """
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