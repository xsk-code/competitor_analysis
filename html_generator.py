from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from typing import Dict, Any
import os


class HTMLGenerator:
    def __init__(self):
        # 获取当前文件所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 创建Jinja2环境
        self.env = Environment(loader=FileSystemLoader(current_dir))
    
    def generate_report(self, analysis_result: Dict[str, Any], output_path: str = None) -> str:
        """
        生成HTML报告
        
        Args:
            analysis_result: 分析结果
            output_path: 输出路径，如果为None则使用默认路径
        
        Returns:
            生成的HTML文件路径
        """
        product_data = analysis_result.get("product_data", {})
        sentiment_analysis = analysis_result.get("sentiment_analysis", {})
        improvement_suggestions = analysis_result.get("improvement_suggestions", {})
        
        # 准备模板变量
        template_vars = {
            "product_name": product_data.get("product_name", "未知产品"),
            "report_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "time_range": product_data.get("time_range", "week"),
            "statistics": product_data.get("statistics", {}),
            "sentiment_analysis": sentiment_analysis,
            "improvement_suggestions": improvement_suggestions,
            "posts": product_data.get("posts", [])[:10]  # 只显示前10条帖子
        }
        
        # 生成HTML
        html_content = self._render_template(template_vars)
        
        # 确定输出路径
        if output_path is None:
            # 使用默认路径：reports目录下，文件名包含产品名和日期
            reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
            os.makedirs(reports_dir, exist_ok=True)
            safe_product_name = product_data.get("product_name", "unknown").replace(" ", "_")
            date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(reports_dir, f"{safe_product_name}_report_{date_str}.html")
        
        # 写入文件
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"HTML报告已生成：{output_path}")
        return output_path
    
    def _render_template(self, vars: Dict[str, Any]) -> str:
        """
        渲染HTML模板
        
        Args:
            vars: 模板变量
        
        Returns:
            渲染后的HTML内容
        """
        # 内联模板，避免依赖外部模板文件
        template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ product_name }} - Reddit 竞品分析报告</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            font-size: 28px;
            margin-bottom: 10px;
        }
        .header .meta {
            font-size: 14px;
            opacity: 0.9;
        }
        .content {
            padding: 30px;
        }
        .section {
            margin-bottom: 30px;
        }
        .section h2 {
            font-size: 22px;
            color: #2c3e50;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #eee;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .stat-card {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }
        .stat-card .value {
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }
        .stat-card .label {
            font-size: 14px;
            color: #666;
        }
        .sentiment-bar {
            display: flex;
            height: 30px;
            border-radius: 15px;
            overflow: hidden;
            margin-bottom: 10px;
        }
        .sentiment-bar .positive {
            background-color: #10b981;
            height: 100%;
        }
        .sentiment-bar .neutral {
            background-color: #f59e0b;
            height: 100%;
        }
        .sentiment-bar .negative {
            background-color: #ef4444;
            height: 100%;
        }
        .sentiment-legend {
            display: flex;
            justify-content: center;
            gap: 20px;
            font-size: 14px;
        }
        .sentiment-legend .item {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .sentiment-legend .color {
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }
        .list-group {
            list-style: none;
        }
        .list-group-item {
            padding: 15px;
            border-bottom: 1px solid #eee;
        }
        .list-group-item:last-child {
            border-bottom: none;
        }
        .priority-high {
            border-left: 4px solid #ef4444;
            padding-left: 15px;
        }
        .priority-medium {
            border-left: 4px solid #f59e0b;
            padding-left: 15px;
        }
        .priority-low {
            border-left: 4px solid #10b981;
            padding-left: 15px;
        }
        .post-card {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
        }
        .post-card .title {
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .post-card .meta {
            font-size: 12px;
            color: #666;
            margin-bottom: 10px;
        }
        .post-card .comments {
            font-size: 14px;
            color: #555;
        }
        .badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            margin-right: 5px;
        }
        .badge-positive {
            background-color: #d1fae5;
            color: #065f46;
        }
        .badge-neutral {
            background-color: #fef3c7;
            color: #92400e;
        }
        .badge-negative {
            background-color: #fee2e2;
            color: #991b1b;
        }
        .footer {
            background-color: #f8f9fa;
            padding: 20px;
            text-align: center;
            font-size: 14px;
            color: #666;
            border-top: 1px solid #eee;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ product_name }} - Reddit 竞品分析报告</h1>
            <div class="meta">
                报告生成时间：{{ report_date }} | 时间范围：{{ time_range }}</div>
        </div>
        
        <div class="content">
            <!-- 统计概览 -->
            <div class="section">
                <h2>📊 统计概览</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="value">{{ statistics.total_posts }}</div>
                        <div class="label">帖子数量</div>
                    </div>
                    <div class="stat-card">
                        <div class="value">{{ statistics.total_comments }}</div>
                        <div class="label">评论数量</div>
                    </div>
                    <div class="stat-card">
                        <div class="value">{{ "%.1f"|format(statistics.avg_score) }}</div>
                        <div class="label">平均分数</div>
                    </div>
                    <div class="stat-card">
                        <div class="value">{{ "%.1f"|format(sentiment_analysis.positive_rate) }}%</div>
                        <div class="label">正面率</div>
                    </div>
                </div>
            </div>
            
            <!-- 情感分析 -->
            <div class="section">
                <h2>🎭 情感分析</h2>
                <div class="sentiment-bar">
                    <div class="positive" style="width: {{ sentiment_analysis.positive / sentiment_analysis.total * 100 if sentiment_analysis.total > 0 else 0 }}%"></div>
                    <div class="neutral" style="width: {{ sentiment_analysis.neutral / sentiment_analysis.total * 100 if sentiment_analysis.total > 0 else 0 }}%"></div>
                    <div class="negative" style="width: {{ sentiment_analysis.negative / sentiment_analysis.total * 100 if sentiment_analysis.total > 0 else 0 }}%"></div>
                </div>
                <div class="sentiment-legend">
                    <div class="item">
                        <span class="color" style="background-color: #10b981;"></span>
                        <span>正面 ({{ sentiment_analysis.positive }})</span>
                    </div>
                    <div class="item">
                        <span class="color" style="background-color: #f59e0b;"></span>
                        <span>中性 ({{ sentiment_analysis.neutral }})</span>
                    </div>
                    <div class="item">
                        <span class="color" style="background-color: #ef4444;"></span>
                        <span>负面 ({{ sentiment_analysis.negative }})</span>
                    </div>
                </div>
                
                <h3 style="margin-top: 20px; margin-bottom: 10px;">关键词分析</h3>
                <div style="margin-bottom: 15px;">
                    <strong>正面关键词：</strong>
                    {% for keyword in sentiment_analysis.key_points.positive_keywords %}
                        <span class="badge badge-positive">{{ keyword }}</span>
                    {% endfor %}
                </div>
                <div style="margin-bottom: 15px;">
                    <strong>负面关键词：</strong>
                    {% for keyword in sentiment_analysis.key_points.negative_keywords %}
                        <span class="badge badge-negative">{{ keyword }}</span>
                    {% endfor %}
                </div>
            </div>
            
            <!-- 主要抱怨点 -->
            <div class="section">
                <h2>😤 主要抱怨点 (Top 3)</h2>
                <ul class="list-group">
                    {% for complaint in improvement_suggestions.top_complaints %}
                        <li class="list-group-item">
                            <strong>{{ complaint.rank }}. {{ complaint.description }}</strong>
                            <br>
                            <span style="color: #666; font-size: 14px;">出现频率：{{ complaint.frequency }}</span>
                        </li>
                    {% else %}
                        <li class="list-group-item">暂无抱怨点数据</li>
                    {% endfor %}
                </ul>
            </div>
            
            <!-- 用户最关注的功能 -->
            <div class="section">
                <h2>🔍 用户最关注的功能 (Top 3)</h2>
                <ul class="list-group">
                    {% for feature in improvement_suggestions.top_features %}
                        <li class="list-group-item">
                            <strong>{{ feature.rank }}. {{ feature.description }}</strong>
                            <br>
                            <span style="color: #666; font-size: 14px;">用户关注度：{{ feature.attention }}</span>
                        </li>
                    {% else %}
                        <li class="list-group-item">暂无功能关注数据</li>
                    {% endfor %}
                </ul>
            </div>
            
            <!-- 改进建议 -->
            <div class="section">
                <h2>💡 产品改进建议</h2>
                <ul class="list-group">
                    {% for suggestion in improvement_suggestions.improvement_suggestions %}
                        <li class="list-group-item priority-{{ suggestion.priority|lower }}">
                            <strong>[{{ suggestion.priority }}] {{ suggestion.suggestion }}</strong>
                            <br>
                            <span style="color: #666; font-size: 14px;">预期效果：{{ suggestion.expected_effect }}</span>
                        </li>
                    {% else %}
                        <li class="list-group-item">暂无改进建议</li>
                    {% endfor %}
                </ul>
            </div>
            
            <!-- 竞品分析 -->
            <div class="section">
                <h2>🏆 竞品亮点分析</h2>
                <p style="padding: 15px; background-color: #f8f9fa; border-radius: 8px;">
                    {{ improvement_suggestions.competitor_analysis }}
                </p>
            </div>
            
            <!-- 整体评价 -->
            <div class="section">
                <h2>📝 整体评价</h2>
                <p style="padding: 15px; background-color: #f8f9fa; border-radius: 8px;">
                    {{ improvement_suggestions.overall_evaluation }}
                </p>
            </div>
            
            <!-- 热门帖子 -->
            <div class="section">
                <h2>🔥 热门帖子 (Top 10)</h2>
                {% for post in posts %}
                    <div class="post-card">
                        <div class="title">{{ post.title }}</div>
                        <div class="meta">
                            <span>作者：{{ post.author }}</span> | 
                            <span>Subreddit：{{ post.subreddit }}</span> | 
                            <span>分数：{{ post.score }}</span> | 
                            <span>评论数：{{ post.num_comments }}</span>
                        </div>
                        {% if post.comments %}
                            <div class="comments">
                                <strong>部分评论：</strong>
                                <ul style="margin-top: 5px; padding-left: 20px;">
                                    {% for comment in post.comments[:3] %}
                                        <li style="margin-bottom: 5px;">{{ comment.body[:100] }}{% if comment.body|length > 100 %}...{% endif %}</li>
                                    {% endfor %}
                                </ul>
                            </div>
                        {% endif %}
                    </div>
                {% else %}
                    <p style="padding: 15px; background-color: #f8f9fa; border-radius: 8px;">
                        暂无帖子数据
                    </p>
                {% endfor %}
            </div>
        </div>
        
        <div class="footer">
            <p>本报告由跨境电商竞品监控系统自动生成</p>
        </div>
    </div>
</body>
</html>
"""
        # 渲染模板
        return self.env.from_string(template).render(vars)


if __name__ == "__main__":
    # 测试代码
    generator = HTMLGenerator()
    # 这里需要实际的分析结果才能测试
    print("HTML生成器初始化完成")
