import praw
from datetime import datetime
from typing import List, Dict, Any
import config


class RedditCollector:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=config.REDDIT_CLIENT_ID,
            client_secret=config.REDDIT_CLIENT_SECRET,
            user_agent=config.REDDIT_USER_AGENT
        )
    
    def fetch_mentions(self, product_name: str, time_range: str = "week", limit: int = 50) -> List[Dict[str, Any]]:
        """
        从Reddit获取产品提及的帖子和评论
        
        Args:
            product_name: 产品名称
            time_range: 时间范围 (hour, day, week, month, year, all)
            limit: 帖子数量限制
        
        Returns:
            包含帖子和评论信息的列表
        """
        results = []
        
        try:
            # 搜索所有subreddit中提及产品的帖子
            for post in self.reddit.subreddit("all").search(
                product_name, 
                time_filter=time_range, 
                limit=limit
            ):
                # 获取帖子的评论
                post.comments.replace_more(limit=0)  # 不加载更多评论
                comments = []
                
                for comment in post.comments[:20]:  # 只获取前20条评论
                    comments.append({
                        "id": comment.id,
                        "author": str(comment.author) if comment.author else "Unknown",
                        "body": comment.body,
                        "score": comment.score,
                        "created_utc": datetime.fromtimestamp(comment.created_utc).isoformat()
                    })
                
                # 构建帖子信息
                post_info = {
                    "id": post.id,
                    "title": post.title,
                    "content": post.selftext,
                    "author": str(post.author) if post.author else "Unknown",
                    "score": post.score,
                    "url": post.url,
                    "subreddit": post.subreddit.display_name,
                    "created_utc": datetime.fromtimestamp(post.created_utc).isoformat(),
                    "num_comments": post.num_comments,
                    "comments": comments
                }
                
                results.append(post_info)
            
            print(f"成功获取 {len(results)} 条关于 '{product_name}' 的帖子")
            return results
        
        except Exception as e:
            print(f"获取Reddit数据时出错: {e}")
            return []
    
    def collect_product_data(self, product_name: str = None) -> Dict[str, Any]:
        """
        收集产品的Reddit数据
        
        Args:
            product_name: 产品名称，如果为None则使用配置中的默认值
        
        Returns:
            包含产品数据和元信息的字典
        """
        if product_name is None:
            product_name = config.PRODUCT_NAME
        
        print(f"开始收集关于 '{product_name}' 的Reddit数据...")
        
        posts = self.fetch_mentions(
            product_name,
            time_range=config.TIME_RANGE,
            limit=config.LIMIT
        )
        
        # 计算统计信息
        total_posts = len(posts)
        total_comments = sum(post["num_comments"] for post in posts)
        avg_score = sum(post["score"] for post in posts) / total_posts if total_posts > 0 else 0
        
        # 提取所有评论内容用于分析
        all_comments = []
        for post in posts:
            all_comments.extend([c["body"] for c in post["comments"]])
        
        return {
            "product_name": product_name,
            "time_range": config.TIME_RANGE,
            "collection_time": datetime.now().isoformat(),
            "statistics": {
                "total_posts": total_posts,
                "total_comments": total_comments,
                "avg_score": avg_score
            },
            "posts": posts,
            "all_comments": all_comments
        }


if __name__ == "__main__":
    # 测试代码
    collector = RedditCollector()
    data = collector.collect_product_data()
    print(f"收集完成，共 {data['statistics']['total_posts']} 条帖子")
