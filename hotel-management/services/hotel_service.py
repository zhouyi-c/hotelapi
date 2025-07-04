from fastapi import HTTPException
from models.hotel_model import get_hotels, search_rooms, book_room, change_room
from pydantic import BaseModel
from typing import Optional

# 未来可切换为数据库ORM查询

class HotelRoom(BaseModel):
    id: int
    hotel_id: int
    room_type: str
    price: int
    date: str
    available: bool

# 获取所有酒店及其房间简要信息
def get_hotels_data(min_price: int, max_price: int, date: str = None):
    """
    查询所有酒店下满足条件的可用房间。
    """
    hotels = get_hotels()
    data = []
    for hotel in hotels:
        rooms = [r for r in hotel.rooms if r.available and min_price <= r.price <= max_price]
        if date:
            rooms = [r for r in rooms if r.date == date]
        if rooms:
            data.append({
                "hotel_id": hotel.id,
                "hotel_name": hotel.name,
                "rooms": [r.to_dict() for r in rooms]
            })
    return {"hotels": data}

# 获取某酒店所有可用房间
def get_hotel_rooms(hotel_id: int, min_price: int = 0, max_price: int = 10000, date: Optional[str] = None):
    rooms = search_rooms(min_price, max_price, date, hotel_id=hotel_id)
    return [r.to_dict() for r in rooms]

# 预订房间
def book_room_service(room_id: int) -> Optional[dict]:
    room = book_room(room_id)
    return room.to_dict() if room else None

# 换房服务
def change_room_service(current_room_id: int) -> Optional[dict]:
    room = change_room(current_room_id)
    return room.to_dict() if room else None