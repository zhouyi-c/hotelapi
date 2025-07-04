from fastapi import HTTPException
from models.hotel_model import get_hotels
from pydantic import BaseModel

# 未来可切换为数据库ORM查询

class HotelRoom(BaseModel):
    id: int
    hotel_id: int
    room_type: str
    price: int
    date: str

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

def get_hotel_rooms(hotel_id: int):
    """
    获取酒店房间数据
    :param hotel_id: 酒店ID
    :return: 酒店房间列表
    """
    # TODO: 实现酒店房间数据查询
    pass