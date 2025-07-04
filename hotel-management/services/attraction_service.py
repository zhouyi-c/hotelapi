from tools.attraction_tool import AttractionRecommendTool

def recommend_attractions(radius: int):
    """直接调用景点推荐工具"""
    tool = AttractionRecommendTool()
    return tool.run(radius)