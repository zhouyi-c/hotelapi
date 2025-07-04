from models.hotel_model import get_hotels
from langchain.tools import BaseTool


class HotelSearchTool(BaseTool):
    name: str = "hotel_search"
    description: str = (
        "根据价格范围(min_price和max_price)和日期(date)查询酒店信息。"
        "参数要求：min_price为整数（最低价格），max_price为整数（最高价格），date为字符串（格式YYYY-MM-DD）。"
        "返回匹配的酒店列表或空列表。"
    )

    def _run(self, min_price: int, max_price: int, date: str = None):
        hotels = [h.to_dict() for h in get_hotels()]
        results = [h for h in hotels if min_price <= h["price"] <= max_price]
        if date:
            results = [h for h in results if h["date"] == date]

        return {
            "match_criteria": {"min_price": min_price, "max_price": max_price, "date": date},
            "result_count": len(results),
            "results": results
        }