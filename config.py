import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Reddit API 配置
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "跨境电商监控 v1.0")

# OpenAI API 配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 产品配置
PRODUCT_NAME = "Anker PowerCore 20100"  # 示例产品名称
TIME_RANGE = "week"  # 时间范围：hour, day, week, month, year, all
LIMIT = 50  # 采集帖子数量限制
