import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any
import config


class PullPushCollector:
    def __init__(self):
        self.base_url = "https://api.pullpush.io/reddit"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def search_posts(self, keyword: str, time_range: str = "week", limit: int = 50, use_historical: bool = True) -> List[Dict[str, Any]]:
        """
        使用PullPush API搜索Reddit帖子
        
        Args:
            keyword: 搜索关键词
            time_range: 时间范围 (hour, day, week, month, year)
            limit: 返回结果数量限制
            use_historical: 是否使用历史数据（如果为True，不进行时间过滤）
        
        Returns:
            帖子列表
        """
        # 首先尝试不使用时间限制获取数据（PullPush的数据可能有延迟）
        url = f"{self.base_url}/search/submission/"
        params = {
            "q": keyword,
            "size": limit,
            "sort": "desc",
            "sort_type": "created_utc"  # 按创建时间排序，获取最新的
        }
        
        try:
            print(f"正在搜索Reddit帖子，关键词: {keyword}")
            response = requests.get(url, params=params, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            posts = data.get("data", [])
            
            # 如果指定了时间范围且不使用历史数据，在本地过滤
            if time_range and posts and not use_historical:
                after_timestamp = self._get_after_param(time_range)
                filtered_posts = [
                    post for post in posts 
                    if post.get("created_utc", 0) >= after_timestamp
                ]
                print(f"成功获取 {len(posts)} 条帖子，过滤后剩余 {len(filtered_posts)} 条（时间范围: {time_range}）")
                
                # 如果过滤后没有数据，提示用户
                if len(filtered_posts) == 0:
                    print(f"警告：PullPush API的数据可能有延迟（最新数据约为11个月前）。")
                    print(f"建议：使用 use_historical=True 参数获取历史数据，或申请官方Reddit API获取实时数据。")
                
                return filtered_posts
            
            print(f"成功获取 {len(posts)} 条帖子（使用历史数据）")
            return posts
        
        except Exception as e:
            print(f"搜索帖子时出错: {e}")
            return []
    
    def search_comments(self, keyword: str, time_range: str = "week", limit: int = 100, use_historical: bool = True) -> List[Dict[str, Any]]:
        """
        使用PullPush API搜索Reddit评论
        
        Args:
            keyword: 搜索关键词
            time_range: 时间范围 (hour, day, week, month, year)
            limit: 返回结果数量限制
            use_historical: 是否使用历史数据（如果为True，不进行时间过滤）
        
        Returns:
            评论列表
        """
        # 首先尝试不使用时间限制获取数据
        url = f"{self.base_url}/search/comment/"
        params = {
            "q": keyword,
            "size": limit,
            "sort": "desc",
            "sort_type": "created_utc"
        }
        
        try:
            print(f"正在搜索Reddit评论，关键词: {keyword}")
            response = requests.get(url, params=params, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            comments = data.get("data", [])
            
            # 如果指定了时间范围且不使用历史数据，在本地过滤
            if time_range and comments and not use_historical:
                after_timestamp = self._get_after_param(time_range)
                filtered_comments = [
                    comment for comment in comments 
                    if comment.get("created_utc", 0) >= after_timestamp
                ]
                print(f"成功获取 {len(comments)} 条评论，过滤后剩余 {len(filtered_comments)} 条（时间范围: {time_range}）")
                return filtered_comments
            
            print(f"成功获取 {len(comments)} 条评论（使用历史数据）")
            return comments
        
        except Exception as e:
            print(f"搜索评论时出错: {e}")
            return []
    
    def get_post_comments(self, post_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        获取特定帖子的评论
        
        Args:
            post_id: 帖子ID
            limit: 评论数量限制
        
        Returns:
            评论列表
        """
        url = f"{self.base_url}/search/comment/"
        params = {
            "link_id": post_id,
            "size": limit,
            "sort": "desc",
            "sort_type": "score"
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            comments = data.get("data", [])
            
            return comments
        
        except Exception as e:
            print(f"获取帖子评论时出错: {e}")
            return []
    
    def _get_after_param(self, time_range: str) -> int:
        """
        根据时间范围计算after参数（epoch时间戳）
        
        Args:
            time_range: 时间范围
        
        Returns:
            epoch时间戳（整数）
        """
        now = datetime.now()
        
        if time_range == "hour":
            after_time = now - timedelta(hours=1)
        elif time_range == "day":
            after_time = now - timedelta(days=1)
        elif time_range == "week":
            after_time = now - timedelta(weeks=1)
        elif time_range == "month":
            after_time = now - timedelta(days=30)
        elif time_range == "year":
            after_time = now - timedelta(days=365)
        else:
            after_time = now - timedelta(weeks=1)  # 默认一周
        
        # 转换为epoch时间戳（整数）
        return int(after_time.timestamp())
    
    def collect_product_data(self, product_name: str = None, use_historical: bool = True) -> Dict[str, Any]:
        """
        收集产品的Reddit数据
        
        Args:
            product_name: 产品名称，如果为None则使用配置中的默认值
            use_historical: 是否使用历史数据（如果为True，不进行时间过滤）
        
        Returns:
            包含产品数据和元信息的字典
        """
        if product_name is None:
            product_name = config.PRODUCT_NAME
        
        print(f"开始收集关于 '{product_name}' 的Reddit数据（使用PullPush API）...")
        
        # 搜索帖子
        posts = self.search_posts(
            product_name,
            time_range=config.TIME_RANGE,
            limit=config.LIMIT,
            use_historical=use_historical
        )
        
        # 搜索评论
        comments = self.search_comments(
            product_name,
            time_range=config.TIME_RANGE,
            limit=config.LIMIT * 2,
            use_historical=use_historical
        )
        
        # 处理帖子数据，转换为统一格式
        processed_posts = []
        for post in posts:
            # 获取帖子的评论
            post_comments = self.get_post_comments(post.get("id"), limit=20)
            
            processed_comments = []
            for comment in post_comments:
                processed_comments.append({
                    "id": comment.get("id"),
                    "author": comment.get("author", "Unknown"),
                    "body": comment.get("body", ""),
                    "score": comment.get("score", 0),
                    "created_utc": datetime.fromtimestamp(comment.get("created_utc", 0)).isoformat() if comment.get("created_utc") else None
                })
            
            # 构建帖子信息
            post_info = {
                "id": post.get("id"),
                "title": post.get("title", ""),
                "content": post.get("selftext", ""),
                "author": post.get("author", "Unknown"),
                "score": post.get("score", 0),
                "url": post.get("url", ""),
                "subreddit": post.get("subreddit", ""),
                "created_utc": datetime.fromtimestamp(post.get("created_utc", 0)).isoformat() if post.get("created_utc") else None,
                "num_comments": post.get("num_comments", 0),
                "comments": processed_comments
            }
            
            processed_posts.append(post_info)
        
        # 提取所有评论内容用于分析
        all_comments = []
        for post in processed_posts:
            all_comments.extend([c["body"] for c in post["comments"]])
        
        # 添加直接搜索到的评论
        for comment in comments:
            all_comments.append(comment.get("body", ""))
        
        # 计算统计信息
        total_posts = len(processed_posts)
        total_comments_count = sum(post["num_comments"] for post in processed_posts) + len(comments)
        avg_score = sum(post["score"] for post in processed_posts) / total_posts if total_posts > 0 else 0
        
        return {
            "product_name": product_name,
            "time_range": config.TIME_RANGE,
            "collection_time": datetime.now().isoformat(),
            "statistics": {
                "total_posts": total_posts,
                "total_comments": total_comments_count,
                "avg_score": avg_score
            },
            "posts": processed_posts,
            "all_comments": all_comments
        }


if __name__ == "__main__":
    # 测试代码
    collector = PullPushCollector()
    data = collector.collect_product_data()
    print(f"收集完成，共 {data['statistics']['total_posts']} 条帖子")
