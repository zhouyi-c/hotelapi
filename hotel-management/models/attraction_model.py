class Attraction:
    def __init__(self, id: int, name: str, distance: float, hotel_id: int):
        self.id = id
        self.name = name
        self.distance = distance  # 距离酒店距离，单位公里
        self.hotel_id = hotel_id  # 关联酒店ID

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "distance": self.distance,
            "hotel_id": self.hotel_id
        }

# 模拟数据库
# 每个景点都与某个酒店关联

def get_attractions():
    return [
        Attraction(1, "人民公园", 0.3, 1),
        Attraction(2, "博物馆", 0.8, 1),
        Attraction(3, "商业街", 0.5, 2),
        Attraction(4, "美食广场", 1.2, 2)
    ]
