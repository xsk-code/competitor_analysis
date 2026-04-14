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
# OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
# OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

# 硅基流动 API 配置（兼容OpenAI格式）
# 示例：
OPENAI_BASE_URL=https://api.siliconflow.cn/v1
OPENAI_MODEL=deepseek-ai/DeepSeek-V3.2

# 产品配置
PRODUCT_NAME = "Anker PowerCore 20100"  # 示例产品名称
TIME_RANGE = "week"  # 时间范围：hour, day, week, month, year, all
LIMIT = 50  # 采集帖子数量限制
