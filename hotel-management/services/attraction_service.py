from tools.attraction_tool import AttractionRecommendTool

def recommend_attractions(radius: int) -> dict:
    """
    景点推荐服务：根据半径推荐酒店周边景点。
    建议仅作为业务调度层，将具体推荐逻辑下沉到工具或Agent层。
    :param radius: 半径（int，公里）
    :return: dict，包含推荐景点
    """
    tool = AttractionRecommendTool()
    return tool._run(radius)
    return tool.run(radius)