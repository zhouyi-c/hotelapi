class Hotel:
    def __init__(self, id: int, name: str, price: int, date: str):
        self.id = id
        self.name = name
        self.price = price
        self.date = date

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "date": self.date
        }

# 模拟数据库
def get_hotels():
    return [
        Hotel(1, "四季酒店", 800, "2025-07-10"),
        Hotel(2, "如家快捷", 200, "2025-07-12")
    ]