import openai
from typing import List, Dict, Any
import config


class AIAnalyzer:
    def __init__(self):
        # 构建OpenAI客户端参数
        client_kwargs = {
            "api_key": config.OPENAI_API_KEY
        }
        
        # 如果配置了base_url，使用自定义的API端点（如硅基流动）
        if config.OPENAI_BASE_URL:
            client_kwargs["base_url"] = config.OPENAI_BASE_URL
            print(f"使用自定义API端点: {config.OPENAI_BASE_URL}")
            print(f"使用模型: {config.OPENAI_MODEL}")
        
        self.client = openai.OpenAI(**client_kwargs)
        self.model = config.OPENAI_MODEL
    
    def analyze_sentiment(self, comments: List[str]) -> Dict[str, Any]:
        """
        分析评论的情感倾向
        
        Args:
            comments: 评论列表
        
        Returns:
            包含情感分析结果的字典
        """
        if not comments:
            return {
                "positive": 0,
                "neutral": 0,
                "negative": 0,
                "total": 0,
                "positive_rate": 0,
                "key_points": []
            }
        
        # 准备提示词
        comments_text = "\n".join([f"{i+1}. {comment}" for i, comment in enumerate(comments[:50])])
        
        prompt = f"""你是一个跨境电商评论分析师。请分析以下关于产品的评论，进行情感分析：

【评论列表】
{comments_text}

请输出以下信息（请严格按照JSON格式输出，不要包含其他内容）：
1. 情感统计：
   - positive: 正面评论数量
   - neutral: 中性评论数量
   - negative: 负面评论数量
2. 正面率：positive / total * 100（保留一位小数）
3. 关键点：
   - 正面关键词（最多5个）
   - 负面关键词（最多5个）
   - 主要抱怨点（最多3个）
   - 用户最关注的功能（最多3个）

输出格式示例：
{{
  "positive": 10,
  "neutral": 5,
  "negative": 3,
  "total": 18,
  "positive_rate": 55.6,
  "key_points": {{
    "positive_keywords": ["耐用", "性价比高", "质量好"],
    "negative_keywords": ["价格贵", "包装差", "续航短"],
    "main_complaints": ["电池续航不足", "包装容易破损"],
    "top_features": ["便携性", "充电速度", "容量"]
  }}
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的跨境电商评论分析师，擅长分析用户评论并提取有价值的信息。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            # 解析响应
            result_text = response.choices[0].message.content.strip()
            # 尝试提取JSON部分
            import json
            import re
            
            # 查找JSON格式的内容
            json_match = re.search(r'\{[\s\S]*\}', result_text)
            if json_match:
                result = json.loads(json_match.group())
            else:
                # 如果没有找到JSON，尝试直接解析
                result = json.loads(result_text)
            
            return result
        
        except Exception as e:
            print(f"情感分析时出错: {e}")
            # 返回默认值
            total = len(comments)
            return {
                "positive": 0,
                "neutral": total,
                "negative": 0,
                "total": total,
                "positive_rate": 0,
                "key_points": {
                    "positive_keywords": [],
                    "negative_keywords": [],
                    "main_complaints": [],
                    "top_features": []
                }
            }
    
    def generate_improvement_suggestions(self, product_data: Dict[str, Any], sentiment_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成产品改进建议
        
        Args:
            product_data: 产品数据
            sentiment_result: 情感分析结果
        
        Returns:
            包含改进建议的字典
        """
        # 准备提示词
        posts_summary = ""
        for i, post in enumerate(product_data.get("posts", [])[:10]):
            posts_summary += f"帖子{i+1}：{post['title']}\n"
            if post['content']:
                posts_summary += f"内容：{post['content'][:200]}...\n"
            posts_summary += f"评论数：{post['num_comments']}，分数：{post['score']}\n\n"
        
        comments_summary = "\n".join([f"- {comment}" for comment in product_data.get("all_comments", [])[:30]])
        
        prompt = f"""你是一个经验丰富的跨境电商产品经理。请基于以下产品的Reddit讨论数据和情感分析结果，生成产品改进建议。

【产品名称】
{product_data.get('product_name', '未知产品')}

【Reddit讨论摘要】
{posts_summary}

【评论摘要】
{comments_summary}

【情感分析结果】
- 正面评论：{sentiment_result.get('positive', 0)}条
- 中性评论：{sentiment_result.get('neutral', 0)}条
- 负面评论：{sentiment_result.get('negative', 0)}条
- 正面率：{sentiment_result.get('positive_rate', 0)}%

【关键点】
- 正面关键词：{', '.join(sentiment_result.get('key_points', {}).get('positive_keywords', []))}
- 负面关键词：{', '.join(sentiment_result.get('key_points', {}).get('negative_keywords', []))}
- 主要抱怨点：{'; '.join(sentiment_result.get('key_points', {}).get('main_complaints', []))}
- 用户最关注的功能：{'; '.join(sentiment_result.get('key_points', {}).get('top_features', []))}

请输出以下信息（请严格按照JSON格式输出，不要包含其他内容）：
1. 主要抱怨点（Top 3）：每个抱怨点包含描述和出现频率估计
2. 用户最关注的功能（Top 3）：每个功能包含描述和用户关注度
3. 具体改进建议：每条建议包含优先级（高/中/低）、建议内容、预期效果
4. 竞品亮点分析：如果有提到竞品，请分析竞品的优点
5. 整体评价：对产品在Reddit上的口碑进行总结

输出格式示例：
{{
  "top_complaints": [
    {{
      "rank": 1,
      "description": "电池续航不足",
      "frequency": "高"
    }}
  ],
  "top_features": [
    {{
      "rank": 1,
      "description": "便携性",
      "attention": "高"
    }}
  ],
  "improvement_suggestions": [
    {{
      "priority": "高",
      "suggestion": "改进电池容量，使用更高密度的电池",
      "expected_effect": "提升用户满意度，减少负面评论"
    }}
  ],
  "competitor_analysis": "用户提到竞品X的电池续航更长，这是我们需要改进的方向",
  "overall_evaluation": "产品在Reddit上的口碑整体偏正面，用户主要关注便携性和充电速度，但电池续航是主要抱怨点"
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个经验丰富的跨境电商产品经理，擅长基于用户反馈生成产品改进建议。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )
            
            # 解析响应
            result_text = response.choices[0].message.content.strip()
            # 尝试提取JSON部分
            import json
            import re
            
            # 查找JSON格式的内容
            json_match = re.search(r'\{[\s\S]*\}', result_text)
            if json_match:
                result = json.loads(json_match.group())
            else:
                # 如果没有找到JSON，尝试直接解析
                result = json.loads(result_text)
            
            return result
        
        except Exception as e:
            print(f"生成改进建议时出错: {e}")
            # 返回默认值
            return {
                "top_complaints": [],
                "top_features": [],
                "improvement_suggestions": [],
                "competitor_analysis": "无法分析竞品信息",
                "overall_evaluation": "无法生成整体评价"
            }
    
    def analyze_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        完整分析产品数据
        
        Args:
            product_data: 产品数据
        
        Returns:
            包含完整分析结果的字典
        """
        print("开始进行情感分析...")
        sentiment_result = self.analyze_sentiment(product_data.get("all_comments", []))
        print(f"情感分析完成，正面率：{sentiment_result.get('positive_rate', 0)}%")
        
        print("开始生成产品改进建议...")
        suggestions = self.generate_improvement_suggestions(product_data, sentiment_result)
        print("产品改进建议生成完成")
        
        return {
            "product_data": product_data,
            "sentiment_analysis": sentiment_result,
            "improvement_suggestions": suggestions
        }


if __name__ == "__main__":
    # 测试代码
    analyzer = AIAnalyzer()
    # 这里需要实际的产品数据才能测试
    print("AI分析器初始化完成")
