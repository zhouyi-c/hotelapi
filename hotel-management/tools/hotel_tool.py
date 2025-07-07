import random

from services.hotel_service import get_hotels_data
from langchain.tools import BaseTool

class HotelSearchTool(BaseTool):
    name: str = "hotel_search"
    description: str = (
        "根据价格范围(min_price和max_price)和日期(date)查询酒店房间信息。"
        "参数要求：min_price为整数（最低价格），max_price为整数（最高价格），date为字符串（格式YYYY-MM-DD）。"
        "返回匹配的酒店及房间详细列表。"
    )

    def _run(self, min_price: int, max_price: int, date: str = None):
        data = get_hotels_data(min_price, max_price, date)
        # 如果用户未指定日期，或者查无结果，直接返回所有可用房间信息（不限定日期）
        if (not date or not data.get('hotels')):
            # 重新查所有日期的房间
            data = get_hotels_data(min_price, max_price, None)
            # 给房间加推荐标签
            for hotel in data.get('hotels', []):
                for room in hotel.get('rooms', []):
                    room['recommend_reason'] = '未指定日期，推荐所有可用房间'
        return data



class HotelBookingTool(BaseTool):
    name:str = "HotelBookingTool"
    description:str = (
    "用于执行酒店房间预订，需要按顺序提供以下参数："
    "1. 入住日期 (格式: YYYY-MM-DD), "
    "2. 离店日期 (格式: YYYY-MM-DD), "
    "3. 房型 (如: 豪华大床房), "
    "4. 客户姓名"
)

    def _run(self, check_in_date: str, check_out_date: str, room_type: str, guest_name: str) -> str:
        # 模拟预订逻辑
        booking_id = random.randint(1000, 9999)
        return f"预订成功！您的预订号：{booking_id}，{room_type}，入住：{check_in_date}，离店：{check_out_date}，客户：{guest_name}"