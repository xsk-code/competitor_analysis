from html_generator import HTMLGenerator
from datetime import datetime

test_data = {
    "product_data": {
        "product_name": "Anker PowerCore 20100",
        "time_range": "week",
        "collection_time": datetime.now().isoformat(),
        "statistics": {
            "total_posts": 47,
            "total_comments": 234,
            "avg_score": 156.8
        },
        "posts": [
            {
                "id": "abc123",
                "title": "Anker PowerCore 20100 - 我的旅行必备神器",
                "content": "这款充电宝真的太棒了！我已经用了两年，每次旅行都带着它。20000mAh的容量足够给我的iPhone充电5次，而且充电速度也很快。唯一的小缺点是重量稍微有点重，但考虑到容量，这是可以接受的。",
                "author": "tech_lover_2024",
                "score": 342,
                "url": "https://www.reddit.com/r/backpacking/comments/abc123/anker_powercore_20100_my_travel_essential/",
                "subreddit": "backpacking",
                "created_utc": "2024-01-15T08:30:00",
                "num_comments": 45,
                "comments": [
                    {
                        "id": "def456",
                        "author": "travel_guru",
                        "body": "完全同意！我也有一个，已经用了三年了，电池依然很耐用。",
                        "score": 89,
                        "created_utc": "2024-01-15T09:15:00"
                    },
                    {
                        "id": "ghi789",
                        "author": "gadget_reviewer",
                        "body": "重量确实是个问题，但对于长途旅行来说，容量更重要。如果你只是日常使用，可以考虑更小的型号。",
                        "score": 56,
                        "created_utc": "2024-01-15T10:00:00"
                    }
                ]
            },
            {
                "id": "xyz789",
                "title": "有人遇到Anker充电宝充电慢的问题吗？",
                "content": "我最近买了Anker PowerCore 20100，但发现给它自身充电需要整整10个小时，这比我预期的要慢很多。我用的是原装充电器，有人有同样的问题吗？",
                "author": "frustrated_user",
                "score": 178,
                "url": "https://www.reddit.com/r/Anker/comments/xyz789/anyone_experiencing_slow_charging_with_powercore/",
                "subreddit": "Anker",
                "created_utc": "2024-01-14T14:20:00",
                "num_comments": 32,
                "comments": [
                    {
                        "id": "jkl012",
                        "author": "anker_expert",
                        "body": "这是正常的，20000mAh的大容量本身就需要较长时间充电。建议使用18W以上的PD充电器，可以稍微快一点。",
                        "score": 123,
                        "created_utc": "2024-01-14T15:00:00"
                    }
                ]
            },
            {
                "id": "mno345",
                "title": "对比评测：Anker vs Aukey 充电宝",
                "content": "我最近测试了Anker PowerCore 20100和Aukey的同类产品。Anker的做工明显更好，而且有更多的安全保护功能。Aukey虽然便宜一点，但充电速度较慢，而且没有Anker那样的质保。",
                "author": "review_pro",
                "score": 256,
                "url": "https://www.reddit.com/r/UsbCHardware/comments/mno345/comparison_anker_vs_aukey_power_banks/",
                "subreddit": "UsbCHardware",
                "created_utc": "2024-01-13T11:45:00",
                "num_comments": 67,
                "comments": []
            }
        ],
        "all_comments": [
            "这款充电宝真的太棒了！",
            "完全同意！我也有一个，已经用了三年了",
            "重量确实是个问题",
            "有人遇到充电慢的问题吗？",
            "这是正常的，大容量需要较长时间充电"
        ]
    },
    "sentiment_analysis": {
        "positive": 35,
        "neutral": 12,
        "negative": 8,
        "total": 55,
        "positive_rate": 63.6,
        "key_points": {
            "positive_keywords": ["耐用", "容量大", "质量好", "性价比高", "充电快"],
            "negative_keywords": ["重量重", "充电慢", "价格贵", "体积大"],
            "main_complaints": ["自身充电时间长", "重量偏重"],
            "top_features": ["大容量", "多端口充电", "便携性"]
        }
    },
    "improvement_suggestions": {
        "top_complaints": [
            {
                "rank": 1,
                "description": "自身充电时间过长，需要10小时以上才能充满",
                "frequency": "高"
            },
            {
                "rank": 2,
                "description": "产品重量偏重，不适合日常携带",
                "frequency": "中"
            },
            {
                "rank": 3,
                "description": "价格相对竞品较高",
                "frequency": "低"
            }
        ],
        "top_features": [
            {
                "rank": 1,
                "description": "20000mAh大容量，满足多设备充电需求",
                "attention": "高"
            },
            {
                "rank": 2,
                "description": "多端口同时充电功能",
                "attention": "高"
            },
            {
                "rank": 3,
                "description": "优秀的产品质量和耐用性",
                "attention": "中"
            }
        ],
        "improvement_suggestions": [
            {
                "priority": "高",
                "suggestion": "升级快充协议，支持PD 3.0或更高功率的输入充电",
                "expected_effect": "将自身充电时间缩短至4-6小时，大幅提升用户体验"
            },
            {
                "priority": "中",
                "suggestion": "推出轻量化版本，使用更高密度的电池芯",
                "expected_effect": "满足日常通勤用户的需求，扩大目标用户群体"
            },
            {
                "priority": "低",
                "suggestion": "考虑推出入门级产品线，提供更具竞争力的价格",
                "expected_effect": "吸引价格敏感型用户，提升市场份额"
            }
        ],
        "competitor_analysis": "用户多次提到Aukey、Baseus等品牌作为对比。竞品的主要优势在于价格较低，部分型号支持更快的输入充电。但用户普遍认为Anker在产品质量、安全性和售后服务方面更胜一筹。特别是Anker的18个月质保政策被多次提及为重要购买因素。",
        "overall_evaluation": "Anker PowerCore 20100在Reddit社区的整体口碑偏正面，正面率达到63.6%。用户最认可的是产品的大容量、优秀的做工和耐用性。主要的抱怨点集中在自身充电速度较慢和产品重量偏重。建议在下一代产品中重点提升快充能力，并考虑推出不同容量/重量的产品线以满足不同用户群体的需求。"
    }
}

if __name__ == "__main__":
    generator = HTMLGenerator()
    output_path = generator.generate_report(test_data)
    print(f"\n测试报告已生成：{output_path}")
    print("请在浏览器中打开此文件查看效果")
