from tools.attraction_tool import AttractionRecommendTool

from models.attraction_model import get_attractions

# 未来可切换为数据库ORM查询

def get_attractions_data(hotel_id: int = None, radius: float = 1.0) -> dict:
    """
    仅做底层景点数据查询，供Agent和Tool调用。
    :param hotel_id: 关联酒店ID（可选）
    :param radius: 半径（公里）
    :return: 景点列表dict
    """
    attractions = [a.to_dict() for a in get_attractions()]
    if hotel_id:
        attractions = [a for a in attractions if a["hotel_id"] == hotel_id and a["distance"] <= radius]
    else:
        attractions = [a for a in attractions if a["distance"] <= radius]
    return {"attractions": attractions}
