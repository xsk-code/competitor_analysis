from datetime import datetime, timedelta
from html_generator import HTMLGenerator
import os


def generate_demo_data():
    """
    生成演示数据
    """
    product_name = "Anker PowerCore 20100"
    
    # 模拟帖子数据
    posts = [
        {
            "id": "post1",
            "title": "Anker PowerCore 20100 - 我的旅行必备神器",
            "content": "我已经使用这个充电宝一年了，每次旅行都带着它。容量足够大，可以给我的iPhone充电5次以上。唯一的缺点是有点重，但考虑到容量，这是可以接受的。",
            "author": "travel_lover",
            "score": 156,
            "url": "https://www.reddit.com/r/backpacking/comments/abc123/anker_powercore_20100/",
            "subreddit": "backpacking",
            "created_utc": (datetime.now() - timedelta(days=3)).isoformat(),
            "num_comments": 23,
            "comments": [
                {
                    "id": "c1",
                    "author": "tech_guy",
                    "body": "同意！我也有一个，确实很耐用。",
                    "score": 45,
                    "created_utc": (datetime.now() - timedelta(days=2)).isoformat()
                },
                {
                    "id": "c2",
                    "author": "frequent_flyer",
                    "body": "重量确实是个问题，尤其是当你已经背着很多东西的时候。",
                    "score": 23,
                    "created_utc": (datetime.now() - timedelta(days=2)).isoformat()
                }
            ]
        },
        {
            "id": "post2",
            "title": "Anker vs Aukey - 哪个充电宝更好？",
            "content": "我正在考虑买一个大容量充电宝，在Anker PowerCore 20100和Aukey 20000mAh之间纠结。Anker的价格贵一些，但品牌更知名。有没有人用过这两个产品？",
            "author": "shopping_help",
            "score": 89,
            "url": "https://www.reddit.com/r/techsupport/comments/def456/anker_vs_aukey/",
            "subreddit": "techsupport",
            "created_utc": (datetime.now() - timedelta(days=5)).isoformat(),
            "num_comments": 45,
            "comments": [
                {
                    "id": "c3",
                    "author": "anker_fan",
                    "body": "我选Anker。虽然贵一点，但质量和售后服务都更好。我用了两年，一点问题都没有。",
                    "score": 67,
                    "created_utc": (datetime.now() - timedelta(days=4)).isoformat()
                },
                {
                    "id": "c4",
                    "author": "budget_buyer",
                    "body": "Aukey性价比更高。我有一个，用了一年也没什么问题。",
                    "score": 34,
                    "created_utc": (datetime.now() - timedelta(days=4)).isoformat()
                }
            ]
        },
        {
            "id": "post3",
            "title": "Anker PowerCore 20100 充电速度测试",
            "content": "我做了一个测试，用Anker PowerCore 20100给我的MacBook Pro充电。从20%到80%用了大约2小时。考虑到这是一个充电宝，这个速度还可以接受。给iPhone充电就快多了，从0到100%大约1.5小时。",
            "author": "test_geek",
            "score": 234,
            "url": "https://www.reddit.com/r/UsbCHardware/comments/ghi789/anker_powercore_20100_test/",
            "subreddit": "UsbCHardware",
            "created_utc": (datetime.now() - timedelta(days=2)).isoformat(),
            "num_comments": 56,
            "comments": [
                {
                    "id": "c5",
                    "author": "speed_demon",
                    "body": "这个速度确实一般。现在很多新的充电宝支持更快的充电协议。",
                    "score": 45,
                    "created_utc": (datetime.now() - timedelta(days=1)).isoformat()
                },
                {
                    "id": "c6",
                    "author": "practical_user",
                    "body": "对我来说够用了。主要是容量大，速度是次要考虑。",
                    "score": 23,
                    "created_utc": (datetime.now() - timedelta(days=1)).isoformat()
                }
            ]
        }
    ]
    
    # 提取所有评论
    all_comments = []
    for post in posts:
        all_comments.extend([c["body"] for c in post["comments"]])
    
    # 构建产品数据
    product_data = {
        "product_name": product_name,
        "time_range": "week",
        "collection_time": datetime.now().isoformat(),
        "statistics": {
            "total_posts": len(posts),
            "total_comments": sum(post["num_comments"] for post in posts),
            "avg_score": sum(post["score"] for post in posts) / len(posts)
        },
        "posts": posts,
        "all_comments": all_comments
    }
    
    # 构建情感分析结果
    sentiment_analysis = {
        "positive": 12,
        "neutral": 5,
        "negative": 3,
        "total": 20,
        "positive_rate": 60.0,
        "key_points": {
            "positive_keywords": ["容量大", "耐用", "品牌可靠", "充电稳定", "性价比"],
            "negative_keywords": ["重量大", "充电速度慢", "价格高"],
            "main_complaints": ["重量偏大，不适合长时间携带", "充电速度一般，不支持最新的快充协议", "价格相对竞品较高"],
            "top_features": ["大容量", "品牌可靠性", "多设备兼容性"]
        }
    }
    
    # 构建改进建议
    improvement_suggestions = {
        "top_complaints": [
            {
                "rank": 1,
                "description": "重量偏大，不适合长时间携带",
                "frequency": "高"
            },
            {
                "rank": 2,
                "description": "充电速度一般，不支持最新的快充协议",
                "frequency": "中"
            },
            {
                "rank": 3,
                "description": "价格相对竞品较高",
                "frequency": "中"
            }
        ],
        "top_features": [
            {
                "rank": 1,
                "description": "大容量（20100mAh）",
                "attention": "高"
            },
            {
                "rank": 2,
                "description": "品牌可靠性和售后服务",
                "attention": "高"
            },
            {
                "rank": 3,
                "description": "多设备兼容性",
                "attention": "中"
            }
        ],
        "improvement_suggestions": [
            {
                "priority": "高",
                "suggestion": "推出轻量化版本，使用更高密度的电池材料",
                "expected_effect": "提升便携性，吸引更多需要轻装出行的用户"
            },
            {
                "priority": "高",
                "suggestion": "升级充电协议，支持PD 3.0或更高版本的快充",
                "expected_effect": "提升充电速度，满足现代设备的快充需求"
            },
            {
                "priority": "中",
                "suggestion": "考虑推出不同容量版本，提供更多价格选择",
                "expected_effect": "覆盖更广泛的预算区间，提升市场竞争力"
            },
            {
                "priority": "低",
                "suggestion": "增加无线充电功能",
                "expected_effect": "提升使用便利性，吸引无线充电用户"
            }
        ],
        "competitor_analysis": "用户提到Aukey作为主要竞品，其优势在于价格更低。Anker的优势在于品牌知名度和产品质量。部分用户认为Anker的高价是合理的，因为质量和售后服务更好。",
        "overall_evaluation": "Anker PowerCore 20100在Reddit上的口碑整体偏正面。用户主要赞赏其大容量和品牌可靠性，但也对重量和充电速度提出了一些抱怨。产品定位清晰，主要面向需要大容量充电宝的用户，但在便携性和快充方面有改进空间。"
    }
    
    return {
        "product_data": product_data,
        "sentiment_analysis": sentiment_analysis,
        "improvement_suggestions": improvement_suggestions
    }


def main():
    print("=" * 50)
    print("跨境电商竞品评论监控系统 - 演示模式")
    print("=" * 50)
    
    # 生成演示数据
    print("\n正在生成演示数据...")
    demo_data = generate_demo_data()
    
    # 生成HTML报告
    print("正在生成HTML报告...")
    generator = HTMLGenerator()
    
    # 确定输出路径
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
    os.makedirs(reports_dir, exist_ok=True)
    output_path = os.path.join(reports_dir, "demo_report.html")
    
    # 生成报告
    output_path = generator.generate_report(demo_data, output_path)
    
    print("\n" + "=" * 50)
    print("演示完成！")
    print("=" * 50)
    print(f"产品名称：{demo_data['product_data']['product_name']}")
    print(f"模拟帖子数：{demo_data['product_data']['statistics']['total_posts']}")
    print(f"模拟评论数：{demo_data['product_data']['statistics']['total_comments']}")
    print(f"正面率：{demo_data['sentiment_analysis']['positive_rate']}%")
    print(f"报告路径：{output_path}")
    print("\n提示：请在浏览器中打开上述HTML文件查看报告效果。")


if __name__ == "__main__":
    main()
