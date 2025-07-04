from agents.base_agent import BaseAgent
from tools.hotel_tool import HotelSearchTool
from tools.attraction_tool import AttractionRecommendTool

class ToolAgent(BaseAgent):
    def __init__(self):
        tools = [HotelSearchTool(), AttractionRecommendTool()]
        super().__init__(tools)