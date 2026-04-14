# 跨境电商竞品评论监控 MVP 方案

## 1. 需求概述

跨境电商卖家需要自动化监控竞品在亚马逊、Instagram、Reddit 的用户评论和反馈，并生成产品改进建议报告，推送至即时通讯群。

**核心需求**：
- 平台：亚马逊 + Instagram + Reddit
- 规模：10 个以内 ASIN/产品
- 频率：每 2-3 天生成报告
- 输出：钉钉/飞书群通知

---

## 2. MVP 技术架构

### 2.1 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                      数据采集层                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  亚马逊   │    │ Instagram │    │  Reddit  │              │
│  │ Jungle Scout │  │ Graph API │    │   PRAW   │              │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘              │
└───────┼──────────────┼──────────────┼──────────────────────┘
        │              │              │
        ▼              ▼              ▼
┌─────────────────────────────────────────────────────────────┐
│                      数据处理层                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ 数据清洗  │───▶│ 存储到   │───▶│ AI 情感  │              │
│  │ & 格式化 │    │ Notion   │    │  分析    │              │
│  └──────────┘    └──────────┘    └────┬─────┘              │
└────────────────────────────────────────┼────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      输出层                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ GPT-4    │───▶│ 改进建议  │───▶│ 钉钉/飞书 │              │
│  │ 生成报告  │    │ 格式化   │    │ Webhook  │              │
│  └──────────┘    └──────────┘    └──────────┘              │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 技术栈

| 层级 | 工具/服务 | 月费用 | 说明 |
|-----|----------|-------|------|
| 爬虫/采集 | Jungle Scout API | ¥200-400 | 亚马逊评论采集 |
| 爬虫/采集 | Instagram Graph API | 免费 | 需 Business 账号 |
| 爬虫/采集 | Reddit PRAW | 免费 | Reddit 评论 |
| 数据存储 | Notion | 免费 | 基础版够用 |
| AI 分析 | OpenAI GPT-4 | ¥100-200 | 按量计费 |
| 自动化调度 | Make (原 Integromat) | 免费 | 每月 1000 次 |
| 消息推送 | 钉钉/飞书 Webhook | 免费 | 官方支持 |

**MVP 月费用估算：¥300-600**

---

## 3. 数据采集方案

### 3.1 亚马逊评论

**工具**：Jungle Scout API（推荐）

**采集字段**：
- 评论内容、评分、日期
- 评论者是否购买
- 有用票数

**API 示例**：
```python
import requests

def fetch_amazon_reviews(asin, api_key):
    url = f"https://api.junglescout.com/v1/reviews"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"asin": asin, "max_results": 50}
    response = requests.get(url, headers=headers, params=params)
    return response.json()
```

**替代方案**：
- Helium 10 API（$37/月）
- Keepa API（$25/月）

---

### 3.2 Instagram 帖子

**工具**：Instagram Graph API（官方免费）

**前置条件**：
- Instagram 商业账号
- Facebook 页面绑定
- Meta Business 验证

**采集字段**：
- 帖子内容、图片、点赞数
- 评论内容、回复

**API 端点**：
```
GET /{instagram-business-account}/media
GET /{instagram-media-id}/comments
```

---

### 3.3 Reddit 评论

**工具**：PRAW（Python Reddit API Wrapper）

**采集字段**：
- 帖子标题、内容
- 评论内容、分数
-  subreddit 归属

**代码示例**：
```python
import praw

reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="跨境电商监控 v1.0"
)

def fetch_reddit_mentions(product_name):
    results = []
    for post in reddit.subreddit("all").search(product_name, limit=50):
        results.append({
            "title": post.title,
            "content": post.selftext,
            "comments": [c.body for c in post.comments[:20]],
            "score": post.score,
            "url": post.url
        })
    return results
```

---

## 4. AI 分析流程

### 4.1 情感分析

将采集的评论按情感分为：正面、中性、负面

**提示词模板**：
```
你是一个跨境电商评论分析师。请分析以下评论的情感倾向：

评论：{comment_text}

请输出：
1. 情感标签：正面/中性/负面
2. 情感分值：1-10分
3. 关键感受：简短概括
```

### 4.2 产品改进建议生成

**提示词模板**：
```
你是跨境电商产品经理。请基于以下竞品评论，生成产品改进建议：

【亚马逊评论汇总】
{amazon_reviews_summary}

【Instagram 评论汇总】
{instagram_comments_summary}

【Reddit 评论汇总】
{reddit_comments_summary}

请输出：
1. 主要抱怨点（Top 3）
2. 用户最关注的功能（Top 3）
3. 具体改进建议（每条建议说明优先级：高/中/低）
4. 竞品亮点分析
```

---

## 5. 自动化流程

### 5.1 Make 自动化配置

```
触发器：定时（每3天）
  │
  ▼
动作1：调用 Python Webhook（采集数据）
  │
  ▼
动作2：存储到 Notion 数据库
  │
  ▼
动作3：调用 OpenAI API（分析评论）
  │
  ▼
动作4：格式化报告内容
  │
  ▼
动作5：发送钉钉/飞书 Webhook 消息
```

### 5.2 报告推送格式

```
📊 竞品监控周报 | 2026-04-13

🏆 亚马逊竞品 A 评分：4.2 ⭐（较上周 ↓0.1）

📉 负面评论关键词：
• 电池续航不足（12次）
• 包装破损（8次）

💡 Top 改进建议：
1. [高] 改进电池容量 - 用户反馈频繁
2. [中] 优化包装设计 - 物流损坏率高
3. [低] 增加配色选项 - 小众需求

📱 Instagram 热度：23条提及 | 正面率 65%
💬 Reddit 讨论：8条帖子 | 情感偏中性
```

---

## 6. 风险与应对

| 风险 | 等级 | 应对策略 |
|-----|------|---------|
| 亚马逊 API 费用涨价 | 中 | 预留备选工具（Keepa/Helium10） |
| Instagram API 权限申请被拒 | 高 | 准备第三方工具 Phantombuster |
| Reddit 爬虫被限制 | 中 | 使用付费 Reddit Premium 提升配额 |
| AI 分析费用超预算 | 低 | 设置 GPT-4 调用次数上限 |
| 数据隐私合规 | 中 | 本地存储，不存储原始评论到第三方 |

---

## 7. MVP 快速启动清单

### 第一天：账号准备
- [ ] 注册 Jungle Scout 试用账号
- [ ] 申请 Instagram Business 账号
- [ ] 创建 Reddit Developer 账号
- [ ] 注册 Make 免费账号
- [ ] 申请 OpenAI API Key

### 第二天：数据采集
- [ ] 配置亚马逊评论采集脚本
- [ ] 配置 Instagram 帖子采集
- [ ] 配置 Reddit 评论采集
- [ ] 测试数据写入 Notion

### 第三天：AI 分析
- [ ] 编写情感分析提示词
- [ ] 编写改进建议生成提示词
- [ ] 测试 GPT-4 输出质量

### 第四天：自动化 & 推送
- [ ] 配置 Make 定时任务
- [ ] 配置钉钉/飞书 Webhook
- [ ] 测试完整流程

---

## 8. 后续扩展方向

MVP 验证可行后，可扩展：

1. **增加平台**：TikTok、Twitter、Shopify 评论
2. **增加功能**：竞品价格监控、评分趋势图、竞品对比分析
3. **提升频率**：从每3天改为每天推送
4. **多语言支持**：支持日语、德语、法语等多语言评论分析
5. **BI 看板**：接入 Tableau/Metabase 生成可视化报表

---

## 9. 联系方式

如需进一步技术支持或定制开发，可联系开发者。
