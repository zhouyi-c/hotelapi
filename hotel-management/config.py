import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Config:
    # 千帆API配置
    QIANFAN_API_KEY = os.getenv("QIANFAN_API_KEY")
    QIANFAN_BASE_URL = "https://qianfan.baidubce.com/v2"
    QIANFAN_MODEL = "ernie-4.0-8k"

    # 数据库配置
    DB_PATH = "data/hotels.json"

    # 验证配置
    if not QIANFAN_API_KEY:
        raise ValueError("请设置QIANFAN_API_KEY环境变量")