from fastapi import APIRouter
from services.hotel_service import filter_hotels
from services.attraction_service import recommend_attractions
from models.schemas import HotelQuery, AttractionRequest

# 创建API路由器
router = APIRouter()

# 酒店筛选API
@router.get("/hotels")
async def get_hotels_endpoint(min_price: int = 0, max_price: int = 1000, date: str = None):
    """
    酒店筛选API
    参数：
        min_price: 最低价
        max_price: 最高价
        date: 入住日期（可选）
    返回：筛选结果（dict）
    """
    # 调用酒店服务进行筛选
    return filter_hotels(min_price, max_price, date)

# 景点推荐API
@router.post("/attraction_recommend")
async def recommend_attractions_endpoint(request: AttractionRequest):
    """
    景点推荐API
    参数：
        request: AttractionRequest，包含radius字段
    返回：推荐景点（dict）
    """
    # 调用景点服务进行推荐
    return recommend_attractions(request.radius)