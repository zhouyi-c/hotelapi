from typing import List, Optional
import copy

class Room:
    def __init__(self, id: int, hotel_id: int, room_type: str, price: int, date: str, available: bool = True):
        self.id = id
        self.hotel_id = hotel_id
        self.room_type = room_type
        self.price = price
        self.date = date
        self.available = available

    def to_dict(self):
        return {
            "id": self.id,
            "hotel_id": self.hotel_id,
            "room_type": self.room_type,
            "price": self.price,
            "date": self.date,
            "available": self.available
        }

class Hotel:
    def __init__(self, id: int, name: str, rooms: List[Room]):
        self.id = id
        self.name = name
        self.rooms = rooms

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "rooms": [r.to_dict() for r in self.rooms]
        }

# 静态模拟数据（可扩展为数据库）
_hotels = [
    Hotel(1, "四季酒店", [
        Room(101, 1, "大床房", 800, "2025-07-10", True),
        Room(102, 1, "双床房", 850, "2025-07-10", True),
        Room(103, 1, "豪华套房", 1200, "2025-07-10", True)
    ]),
    Hotel(2, "如家快捷", [
        Room(201, 2, "大床房", 200, "2025-07-12", True),
        Room(202, 2, "双床房", 220, "2025-07-12", True),
        Room(203, 2, "家庭房", 300, "2025-07-12", True)
    ])
]

# 提供酒店列表（无房间明细）
def get_hotels():
    return [Hotel(h.id, h.name, copy.deepcopy(h.rooms)) for h in _hotels]

# 按条件检索可用房间
def search_rooms(min_price: int, max_price: int, date: Optional[str] = None, hotel_id: Optional[int] = None, room_type: Optional[str] = None):
    # 先查完全匹配
    rooms = []
    for hotel in _hotels:
        if hotel_id and hotel.id != hotel_id:
            continue
        for room in hotel.rooms:
            if not room.available:
                continue
            if min_price <= room.price <= max_price:
                if date and room.date != date:
                    continue
                if room_type and room.room_type != room_type:
                    continue
                rooms.append(room)
    if rooms:
        return rooms
    # 若无完全匹配，推荐其它日期的同价位房间
    fallback_rooms = []
    for hotel in _hotels:
        if hotel_id and hotel.id != hotel_id:
            continue
        for room in hotel.rooms:
            if not room.available:
                continue
            if min_price <= room.price <= max_price:
                if room_type and room.room_type != room_type:
                    continue
                fallback_rooms.append(room)
    # 给推荐房间打上推荐标签（可在to_dict中扩展）
    for room in fallback_rooms:
        room.recommend_reason = "推荐：其它日期可用房间"
    return fallback_rooms

# 预订房间（将房间状态置为不可用）
def book_room(room_id: int) -> Optional[Room]:
    for hotel in _hotels:
        for room in hotel.rooms:
            if room.id == room_id and room.available:
                room.available = False
                return room
    return None

# 换房逻辑：查找同酒店可用且同价位或更高的房型
def change_room(current_room_id: int) -> Optional[Room]:
    for hotel in _hotels:
        for room in hotel.rooms:
            if room.id == current_room_id:
                current_type = room.room_type
                current_price = room.price
                hotel_id = room.hotel_id
                date = room.date
                break
        else:
            continue
        break
    else:
        return None
    # 查找同酒店可用、同价位或升级房
    candidates = [r for r in hotel.rooms if r.available and r.price >= current_price and r.id != current_room_id]
    if candidates:
        candidates.sort(key=lambda r: r.price)
        candidates[0].available = False
        return candidates[0]
    return None