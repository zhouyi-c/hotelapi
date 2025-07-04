from tools.attraction_tool import AttractionRecommendTool

from tools.attraction_tool import AttractionRecommendTool

def get_attractions_data(radius: int) -> dict:
    """
    仅做底层景点数据查询，供Agent和Tool调用。
    :param radius: 半径（公里）
    :return: 景点列表dict
    """
    tool = AttractionRecommendTool()
    return tool._run(radius)
