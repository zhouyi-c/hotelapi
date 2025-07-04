from fastapi import HTTPException
from models.hotel_model import get_hotels

def get_hotels_data(min_price: int, max_price: int, date: str = None):
    """
    仅做底层酒店数据查询，供Agent和Tool调用。
    :param min_price: 最低价
    :param max_price: 最高价
    :param date: 可选，入住日期
    :return: 酒店列表dict
    """
    hotels = [h.to_dict() for h in get_hotels()]
    results = [h for h in hotels if min_price <= h["price"] <= max_price]
    if date:
        results = [h for h in results if h["date"] == date]
    return {"hotels": results}