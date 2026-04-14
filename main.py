from reddit_collector import RedditCollector
from pullpush_collector import PullPushCollector
from ai_analyzer import AIAnalyzer
from html_generator import HTMLGenerator
import config
import argparse


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='跨境电商竞品评论监控系统')
    parser.add_argument('--product', type=str, help='产品名称')
    parser.add_argument('--time-range', type=str, default='week', 
                        choices=['hour', 'day', 'week', 'month', 'year', 'all'],
                        help='时间范围')
    parser.add_argument('--limit', type=int, default=50, help='采集帖子数量限制')
    parser.add_argument('--output', type=str, help='输出HTML文件路径')
    parser.add_argument('--collector', type=str, default='pullpush', 
                        choices=['official', 'pullpush'],
                        help='数据采集方式：official（官方API，需要申请）或 pullpush（免费第三方API，无需注册）')
    
    args = parser.parse_args()
    
    # 更新配置
    if args.product:
        config.PRODUCT_NAME = args.product
    if args.time_range:
        config.TIME_RANGE = args.time_range
    if args.limit:
        config.LIMIT = args.limit
    
    # 步骤1：采集Reddit数据
    print("=" * 50)
    print("步骤1：采集Reddit数据")
    print("=" * 50)
    
    # 选择采集器
    if args.collector == 'official':
        print("使用官方API采集数据（需要配置Reddit API密钥）")
        collector = RedditCollector()
    else:
        print("使用PullPush API采集数据（免费，无需注册）")
        collector = PullPushCollector()
    
    product_data = collector.collect_product_data()
    
    if product_data['statistics']['total_posts'] == 0:
        print("警告：未采集到任何帖子数据，程序退出")
        return
    
    # 步骤2：AI分析
    print("\n" + "=" * 50)
    print("步骤2：AI分析")
    print("=" * 50)
    
    analyzer = AIAnalyzer()
    analysis_result = analyzer.analyze_product(product_data)
    
    # 步骤3：生成HTML报告
    print("\n" + "=" * 50)
    print("步骤3：生成HTML报告")
    print("=" * 50)
    
    generator = HTMLGenerator()
    output_path = generator.generate_report(analysis_result, args.output)
    
    print("\n" + "=" * 50)
    print("分析完成！")
    print("=" * 50)
    print(f"产品名称：{product_data['product_name']}")
    print(f"采集帖子数：{product_data['statistics']['total_posts']}")
    print(f"采集评论数：{product_data['statistics']['total_comments']}")
    print(f"正面率：{analysis_result['sentiment_analysis']['positive_rate']}%")
    print(f"报告路径：{output_path}")


if __name__ == "__main__":
    main()
