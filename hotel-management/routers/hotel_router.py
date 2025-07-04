from fastapi import APIRouter
from services.hotel_service import filter_hotels
from services.attraction_service import recommend_attractions
from models.schemas import HotelQuery, AttractionRequest

router = APIRouter()

@router.get("/hotels")
async def get_hotels_endpoint(min_price: int = 0, max_price: int = 1000, date: str = None):
    return filter_hotels(min_price, max_price, date)

@router.post("/attraction_recommend")
async def recommend_attractions_endpoint(request: AttractionRequest):
    return recommend_attractions(request.radius)