from langchain.tools import BaseTool


class AttractionRecommendTool(BaseTool):
    name: str = "attraction_recommend"
    description: str = "推荐酒店周边的景点，参数为范围半径（整数公里数）"

    def _run(self, radius: int):
        attractions = [
            {"name": "故宫", "distance": "1.2km", "type": "文化遗址"},
            {"name": "颐和园", "distance": "8.5km", "type": "皇家园林"},
            {"name": "798艺术区", "distance": "12km", "type": "艺术展览"}
        ]

        filtered = [a for a in attractions if float(a["distance"].replace("km", "")) <= radius]
        return {
            "radius_km": radius,
            "attractions": filtered
        }