from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from typing import Dict, Any
import os


class HTMLGenerator:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.env = Environment(loader=FileSystemLoader(current_dir))
    
    def generate_report(self, analysis_result: Dict[str, Any], output_path: str = None) -> str:
        product_data = analysis_result.get("product_data", {})
        sentiment_analysis = analysis_result.get("sentiment_analysis", {})
        improvement_suggestions = analysis_result.get("improvement_suggestions", {})
        
        all_posts = product_data.get("posts", [])
        sorted_posts = sorted(all_posts, key=lambda x: x.get("score", 0), reverse=True)
        
        template_vars = {
            "product_name": product_data.get("product_name", "未知产品"),
            "report_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "time_range": product_data.get("time_range", "week"),
            "statistics": product_data.get("statistics", {}),
            "sentiment_analysis": sentiment_analysis,
            "improvement_suggestions": improvement_suggestions,
            "posts": sorted_posts[:10],
            "all_posts_count": len(all_posts)
        }
        
        html_content = self._render_template(template_vars)
        
        if output_path is None:
            reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
            os.makedirs(reports_dir, exist_ok=True)
            safe_product_name = product_data.get("product_name", "unknown").replace(" ", "_")
            date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(reports_dir, f"{safe_product_name}_report_{date_str}.html")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"HTML报告已生成：{output_path}")
        return output_path
    
    def _render_template(self, vars: Dict[str, Any]) -> str:
        template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ product_name }} - Reddit 竞品分析报告</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --ink: oklch(0.18 0.02 270);
            --ink-light: oklch(0.35 0.02 270);
            --ink-muted: oklch(0.55 0.02 270);
            --paper: oklch(0.98 0.005 90);
            --paper-warm: oklch(0.96 0.01 80);
            --accent: oklch(0.55 0.18 250);
            --accent-light: oklch(0.85 0.08 250);
            --positive: oklch(0.55 0.15 145);
            --positive-light: oklch(0.90 0.05 145);
            --neutral: oklch(0.65 0.12 85);
            --neutral-light: oklch(0.92 0.04 85);
            --negative: oklch(0.55 0.18 25);
            --negative-light: oklch(0.90 0.05 25);
            --border-subtle: oklch(0.90 0.01 270);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.7;
            color: var(--ink);
            background-color: var(--paper);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        .container {
            max-width: 1100px;
            margin: 0 auto;
            padding: 0 24px;
        }

        /* Header */
        .header {
            padding: 80px 0 60px;
            border-bottom: 1px solid var(--border-subtle);
            margin-bottom: 60px;
        }

        .header__eyebrow {
            font-family: 'Inter', sans-serif;
            font-size: 12px;
            font-weight: 500;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: var(--ink-muted);
            margin-bottom: 16px;
        }

        .header__title {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: clamp(2.5rem, 5vw, 4rem);
            font-weight: 600;
            line-height: 1.1;
            color: var(--ink);
            margin-bottom: 24px;
        }

        .header__meta {
            display: flex;
            flex-wrap: wrap;
            gap: 24px;
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            color: var(--ink-muted);
        }

        .header__meta-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .header__meta-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background-color: var(--accent);
        }

        /* Navigation */
        .nav {
            position: sticky;
            top: 0;
            background: var(--paper);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border-subtle);
            z-index: 100;
            margin: -60px 0 60px;
        }

        .nav__list {
            display: flex;
            gap: 32px;
            list-style: none;
            padding: 16px 0;
            overflow-x: auto;
            scrollbar-width: none;
        }

        .nav__list::-webkit-scrollbar {
            display: none;
        }

        .nav__link {
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            font-weight: 500;
            color: var(--ink-muted);
            text-decoration: none;
            white-space: nowrap;
            padding: 8px 0;
            position: relative;
            transition: color 0.3s ease;
        }

        .nav__link:hover {
            color: var(--ink);
        }

        .nav__link::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 0;
            height: 2px;
            background: var(--accent);
            transition: width 0.3s ease;
        }

        .nav__link:hover::after {
            width: 100%;
        }

        /* Section */
        .section {
            margin-bottom: 80px;
            opacity: 0;
            transform: translateY(20px);
            animation: fadeInUp 0.6s ease forwards;
        }

        @keyframes fadeInUp {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .section:nth-child(1) { animation-delay: 0.1s; }
        .section:nth-child(2) { animation-delay: 0.2s; }
        .section:nth-child(3) { animation-delay: 0.3s; }
        .section:nth-child(4) { animation-delay: 0.4s; }
        .section:nth-child(5) { animation-delay: 0.5s; }

        .section__header {
            display: flex;
            align-items: baseline;
            gap: 16px;
            margin-bottom: 40px;
        }

        .section__number {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 14px;
            font-weight: 600;
            color: var(--accent);
        }

        .section__title {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: clamp(1.5rem, 3vw, 2rem);
            font-weight: 600;
            color: var(--ink);
        }

        .section__subtitle {
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            color: var(--ink-muted);
            margin-top: 8px;
        }

        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 24px;
        }

        .stat-card {
            background: var(--paper-warm);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 32px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .stat-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 40px -20px rgba(0, 0, 0, 0.1);
        }

        .stat-card__value {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 3rem;
            font-weight: 600;
            color: var(--ink);
            line-height: 1;
            margin-bottom: 8px;
        }

        .stat-card__label {
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            font-weight: 500;
            color: var(--ink-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .stat-card__trend {
            font-family: 'Inter', sans-serif;
            font-size: 12px;
            color: var(--positive);
            margin-top: 12px;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        /* Sentiment Section */
        .sentiment-container {
            background: var(--paper-warm);
            border: 1px solid var(--border-subtle);
            border-radius: 20px;
            padding: 40px;
        }

        .sentiment-bar {
            display: flex;
            height: 48px;
            border-radius: 24px;
            overflow: hidden;
            margin-bottom: 32px;
            box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.05);
        }

        .sentiment-bar__segment {
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.5s ease;
            position: relative;
        }

        .sentiment-bar__segment:hover {
            filter: brightness(1.05);
        }

        .sentiment-bar__segment--positive {
            background: linear-gradient(135deg, var(--positive), oklch(0.60 0.15 145));
        }

        .sentiment-bar__segment--neutral {
            background: linear-gradient(135deg, var(--neutral), oklch(0.70 0.12 85));
        }

        .sentiment-bar__segment--negative {
            background: linear-gradient(135deg, var(--negative), oklch(0.60 0.18 25));
        }

        .sentiment-bar__label {
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            font-weight: 600;
            color: white;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
        }

        .sentiment-legend {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 24px;
        }

        .sentiment-legend__item {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .sentiment-legend__dot {
            width: 16px;
            height: 16px;
            border-radius: 50%;
        }

        .sentiment-legend__dot--positive { background: var(--positive); }
        .sentiment-legend__dot--neutral { background: var(--neutral); }
        .sentiment-legend__dot--negative { background: var(--negative); }

        .sentiment-legend__text {
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            color: var(--ink);
        }

        .sentiment-legend__count {
            font-weight: 600;
            color: var(--ink);
        }

        /* Keywords */
        .keywords-section {
            margin-top: 40px;
            padding-top: 40px;
            border-top: 1px solid var(--border-subtle);
        }

        .keywords-title {
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--ink-muted);
            margin-bottom: 16px;
        }

        .keywords-cloud {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .keyword-tag {
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            padding: 10px 18px;
            border-radius: 24px;
            transition: all 0.3s ease;
            cursor: default;
        }

        .keyword-tag--positive {
            background: var(--positive-light);
            color: oklch(0.35 0.12 145);
        }

        .keyword-tag--negative {
            background: var(--negative-light);
            color: oklch(0.35 0.12 25);
        }

        .keyword-tag:hover {
            transform: scale(1.05);
        }

        /* Lists */
        .list-group {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .list-item {
            background: var(--paper-warm);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 28px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .list-item::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
        }

        .list-item--high::before { background: var(--negative); }
        .list-item--medium::before { background: var(--neutral); }
        .list-item--low::before { background: var(--positive); }

        .list-item:hover {
            transform: translateX(4px);
            box-shadow: 0 8px 24px -12px rgba(0, 0, 0, 0.1);
        }

        .list-item__rank {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 14px;
            font-weight: 600;
            color: var(--accent);
            margin-bottom: 8px;
        }

        .list-item__title {
            font-family: 'Inter', sans-serif;
            font-size: 16px;
            font-weight: 600;
            color: var(--ink);
            margin-bottom: 8px;
        }

        .list-item__meta {
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            color: var(--ink-muted);
        }

        .list-item__priority {
            display: inline-block;
            font-family: 'Inter', sans-serif;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 4px 10px;
            border-radius: 12px;
            margin-bottom: 12px;
        }

        .list-item__priority--high {
            background: var(--negative-light);
            color: var(--negative);
        }

        .list-item__priority--medium {
            background: var(--neutral-light);
            color: var(--neutral);
        }

        .list-item__priority--low {
            background: var(--positive-light);
            color: var(--positive);
        }

        /* Analysis Box */
        .analysis-box {
            background: var(--paper-warm);
            border: 1px solid var(--border-subtle);
            border-radius: 20px;
            padding: 40px;
            position: relative;
        }

        .analysis-box::before {
            content: '"';
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 120px;
            line-height: 1;
            color: var(--accent-light);
            position: absolute;
            top: 20px;
            left: 24px;
            opacity: 0.5;
        }

        .analysis-box__content {
            position: relative;
            z-index: 1;
            font-family: 'Inter', sans-serif;
            font-size: 15px;
            line-height: 1.9;
            color: var(--ink-light);
        }

        /* Posts Section */
        .posts-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 32px;
        }

        .posts-count {
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            color: var(--ink-muted);
        }

        .post-card {
            background: var(--paper-warm);
            border: 1px solid var(--border-subtle);
            border-radius: 20px;
            padding: 32px;
            margin-bottom: 24px;
            transition: all 0.3s ease;
        }

        .post-card:hover {
            border-color: var(--accent-light);
            box-shadow: 0 12px 32px -16px rgba(0, 0, 0, 0.1);
        }

        .post-card__title {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 1.25rem;
            font-weight: 600;
            line-height: 1.4;
            color: var(--ink);
            margin-bottom: 16px;
        }

        .post-card__title-link {
            color: var(--ink);
            text-decoration: none;
            transition: color 0.3s ease;
        }

        .post-card__title-link:hover {
            color: var(--accent);
        }

        .post-card__meta {
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            margin-bottom: 20px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border-subtle);
        }

        .post-card__meta-item {
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            color: var(--ink-muted);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .post-card__meta-icon {
            width: 16px;
            height: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .post-card__score {
            font-weight: 600;
            color: var(--accent);
        }

        .post-card__link {
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            color: var(--accent);
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: gap 0.3s ease;
        }

        .post-card__link:hover {
            gap: 10px;
        }

        .post-card__content {
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            line-height: 1.8;
            color: var(--ink-light);
            margin-bottom: 20px;
        }

        .post-card__comments {
            background: var(--paper);
            border-radius: 12px;
            padding: 20px;
        }

        .post-card__comments-title {
            font-family: 'Inter', sans-serif;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--ink-muted);
            margin-bottom: 12px;
        }

        .post-card__comment {
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            line-height: 1.7;
            color: var(--ink-light);
            padding: 12px 0;
            border-bottom: 1px solid var(--border-subtle);
        }

        .post-card__comment:last-child {
            border-bottom: none;
            padding-bottom: 0;
        }

        .post-card__comment-author {
            font-weight: 500;
            color: var(--ink);
            margin-right: 8px;
        }

        /* Footer */
        .footer {
            padding: 60px 0;
            border-top: 1px solid var(--border-subtle);
            margin-top: 80px;
        }

        .footer__content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }

        .footer__text {
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            color: var(--ink-muted);
        }

        .footer__logo {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 14px;
            font-weight: 600;
            color: var(--ink);
        }

        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            background: var(--paper-warm);
            border: 1px solid var(--border-subtle);
            border-radius: 20px;
        }

        .empty-state__icon {
            font-size: 48px;
            margin-bottom: 16px;
        }

        .empty-state__text {
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            color: var(--ink-muted);
        }

        /* Responsive */
        @media (max-width: 768px) {
            .header {
                padding: 48px 0 40px;
                margin-bottom: 40px;
            }

            .section {
                margin-bottom: 48px;
            }

            .sentiment-container,
            .analysis-box {
                padding: 24px;
            }

            .post-card {
                padding: 24px;
            }

            .nav__list {
                gap: 20px;
            }

            .stats-grid {
                grid-template-columns: 1fr 1fr;
            }

            .stat-card {
                padding: 24px;
            }

            .stat-card__value {
                font-size: 2.5rem;
            }
        }

        @media (max-width: 480px) {
            .stats-grid {
                grid-template-columns: 1fr;
            }

            .sentiment-bar {
                height: 40px;
            }

            .sentiment-bar__label {
                font-size: 11px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header class="header">
            <div class="header__eyebrow">Reddit 竞品分析报告</div>
            <h1 class="header__title">{{ product_name }}</h1>
            <div class="header__meta">
                <div class="header__meta-item">
                    <span class="header__meta-dot"></span>
                    <span>生成时间：{{ report_date }}</span>
                </div>
                <div class="header__meta-item">
                    <span class="header__meta-dot"></span>
                    <span>时间范围：{{ time_range }}</span>
                </div>
                <div class="header__meta-item">
                    <span class="header__meta-dot"></span>
                    <span>共 {{ all_posts_count }} 条帖子</span>
                </div>
            </div>
        </header>

        <!-- Navigation -->
        <nav class="nav">
            <div class="container">
                <ul class="nav__list">
                    <li><a href="#overview" class="nav__link">统计概览</a></li>
                    <li><a href="#sentiment" class="nav__link">情感分析</a></li>
                    <li><a href="#complaints" class="nav__link">用户抱怨</a></li>
                    <li><a href="#features" class="nav__link">关注功能</a></li>
                    <li><a href="#suggestions" class="nav__link">改进建议</a></li>
                    <li><a href="#posts" class="nav__link">热门帖子</a></li>
                </ul>
            </div>
        </nav>

        <!-- Overview Section -->
        <section id="overview" class="section">
            <div class="section__header">
                <span class="section__number">01</span>
                <div>
                    <h2 class="section__title">统计概览</h2>
                    <p class="section__subtitle">基于 Reddit 讨论数据的核心指标</p>
                </div>
            </div>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-card__value">{{ statistics.total_posts }}</div>
                    <div class="stat-card__label">帖子数量</div>
                    <div class="stat-card__trend">
                        <span>↑</span>
                        <span>活跃讨论</span>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-card__value">{{ statistics.total_comments }}</div>
                    <div class="stat-card__label">评论数量</div>
                    <div class="stat-card__trend">
                        <span>💬</span>
                        <span>用户参与度</span>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-card__value">{{ "%.1f"|format(statistics.avg_score) }}</div>
                    <div class="stat-card__label">平均分数</div>
                    <div class="stat-card__trend">
                        <span>⭐</span>
                        <span>社区评价</span>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-card__value">{{ "%.1f"|format(sentiment_analysis.positive_rate) }}%</div>
                    <div class="stat-card__label">正面率</div>
                    <div class="stat-card__trend">
                        <span>😊</span>
                        <span>用户满意度</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- Sentiment Section -->
        <section id="sentiment" class="section">
            <div class="section__header">
                <span class="section__number">02</span>
                <div>
                    <h2 class="section__title">情感分析</h2>
                    <p class="section__subtitle">用户评论的情感倾向分布</p>
                </div>
            </div>
            <div class="sentiment-container">
                <div class="sentiment-bar">
                    {% set total = sentiment_analysis.total or 1 %}
                    {% set positive_pct = (sentiment_analysis.positive / total * 100) if total > 0 else 0 %}
                    {% set neutral_pct = (sentiment_analysis.neutral / total * 100) if total > 0 else 0 %}
                    {% set negative_pct = (sentiment_analysis.negative / total * 100) if total > 0 else 0 %}
                    
                    {% if positive_pct > 0 %}
                    <div class="sentiment-bar__segment sentiment-bar__segment--positive" style="width: {{ positive_pct }}%">
                        {% if positive_pct > 15 %}
                        <span class="sentiment-bar__label">正面 {{ "%.0f"|format(positive_pct) }}%</span>
                        {% endif %}
                    </div>
                    {% endif %}
                    {% if neutral_pct > 0 %}
                    <div class="sentiment-bar__segment sentiment-bar__segment--neutral" style="width: {{ neutral_pct }}%">
                        {% if neutral_pct > 15 %}
                        <span class="sentiment-bar__label">中性 {{ "%.0f"|format(neutral_pct) }}%</span>
                        {% endif %}
                    </div>
                    {% endif %}
                    {% if negative_pct > 0 %}
                    <div class="sentiment-bar__segment sentiment-bar__segment--negative" style="width: {{ negative_pct }}%">
                        {% if negative_pct > 15 %}
                        <span class="sentiment-bar__label">负面 {{ "%.0f"|format(negative_pct) }}%</span>
                        {% endif %}
                    </div>
                    {% endif %}
                </div>
                <div class="sentiment-legend">
                    <div class="sentiment-legend__item">
                        <span class="sentiment-legend__dot sentiment-legend__dot--positive"></span>
                        <span class="sentiment-legend__text">
                            <span class="sentiment-legend__count">{{ sentiment_analysis.positive }}</span> 条正面评论
                        </span>
                    </div>
                    <div class="sentiment-legend__item">
                        <span class="sentiment-legend__dot sentiment-legend__dot--neutral"></span>
                        <span class="sentiment-legend__text">
                            <span class="sentiment-legend__count">{{ sentiment_analysis.neutral }}</span> 条中性评论
                        </span>
                    </div>
                    <div class="sentiment-legend__item">
                        <span class="sentiment-legend__dot sentiment-legend__dot--negative"></span>
                        <span class="sentiment-legend__text">
                            <span class="sentiment-legend__count">{{ sentiment_analysis.negative }}</span> 条负面评论
                        </span>
                    </div>
                </div>

                {% if sentiment_analysis.key_points %}
                <div class="keywords-section">
                    <div class="keywords-title">正面关键词</div>
                    <div class="keywords-cloud">
                        {% for keyword in sentiment_analysis.key_points.positive_keywords %}
                        <span class="keyword-tag keyword-tag--positive">{{ keyword }}</span>
                        {% else %}
                        <span class="empty-state__text">暂无正面关键词数据</span>
                        {% endfor %}
                    </div>
                    
                    <div class="keywords-title" style="margin-top: 24px;">负面关键词</div>
                    <div class="keywords-cloud">
                        {% for keyword in sentiment_analysis.key_points.negative_keywords %}
                        <span class="keyword-tag keyword-tag--negative">{{ keyword }}</span>
                        {% else %}
                        <span class="empty-state__text">暂无负面关键词数据</span>
                        {% endfor %}
                    </div>
                </div>
                {% endif %}
            </div>
        </section>

        <!-- Complaints Section -->
        <section id="complaints" class="section">
            <div class="section__header">
                <span class="section__number">03</span>
                <div>
                    <h2 class="section__title">主要抱怨点</h2>
                    <p class="section__subtitle">用户最常提及的问题与不满</p>
                </div>
            </div>
            <div class="list-group">
                {% for complaint in improvement_suggestions.top_complaints %}
                <div class="list-item list-item--high">
                    <div class="list-item__rank">#{{ complaint.rank }}</div>
                    <div class="list-item__title">{{ complaint.description }}</div>
                    <div class="list-item__meta">出现频率：{{ complaint.frequency }}</div>
                </div>
                {% else %}
                <div class="empty-state">
                    <div class="empty-state__icon">📋</div>
                    <div class="empty-state__text">暂无抱怨点数据</div>
                </div>
                {% endfor %}
            </div>
        </section>

        <!-- Features Section -->
        <section id="features" class="section">
            <div class="section__header">
                <span class="section__number">04</span>
                <div>
                    <h2 class="section__title">用户关注功能</h2>
                    <p class="section__subtitle">用户最关心的产品特性</p>
                </div>
            </div>
            <div class="list-group">
                {% for feature in improvement_suggestions.top_features %}
                <div class="list-item list-item--medium">
                    <div class="list-item__rank">#{{ feature.rank }}</div>
                    <div class="list-item__title">{{ feature.description }}</div>
                    <div class="list-item__meta">用户关注度：{{ feature.attention }}</div>
                </div>
                {% else %}
                <div class="empty-state">
                    <div class="empty-state__icon">✨</div>
                    <div class="empty-state__text">暂无功能关注数据</div>
                </div>
                {% endfor %}
            </div>
        </section>

        <!-- Suggestions Section -->
        <section id="suggestions" class="section">
            <div class="section__header">
                <span class="section__number">05</span>
                <div>
                    <h2 class="section__title">改进建议</h2>
                    <p class="section__subtitle">基于用户反馈的产品优化方向</p>
                </div>
            </div>
            <div class="list-group">
                {% for suggestion in improvement_suggestions.improvement_suggestions %}
                <div class="list-item list-item--{{ suggestion.priority|lower }}">
                    <span class="list-item__priority list-item__priority--{{ suggestion.priority|lower }}">
                        {{ suggestion.priority }}优先级
                    </span>
                    <div class="list-item__title">{{ suggestion.suggestion }}</div>
                    <div class="list-item__meta">预期效果：{{ suggestion.expected_effect }}</div>
                </div>
                {% else %}
                <div class="empty-state">
                    <div class="empty-state__icon">💡</div>
                    <div class="empty-state__text">暂无改进建议</div>
                </div>
                {% endfor %}
            </div>
        </section>

        <!-- Competitor Analysis -->
        {% if improvement_suggestions.competitor_analysis and improvement_suggestions.competitor_analysis != "无法分析竞品信息" %}
        <section class="section">
            <div class="section__header">
                <span class="section__number">06</span>
                <div>
                    <h2 class="section__title">竞品亮点分析</h2>
                    <p class="section__subtitle">用户提及的竞争对手优势</p>
                </div>
            </div>
            <div class="analysis-box">
                <div class="analysis-box__content">{{ improvement_suggestions.competitor_analysis }}</div>
            </div>
        </section>
        {% endif %}

        <!-- Overall Evaluation -->
        {% if improvement_suggestions.overall_evaluation and improvement_suggestions.overall_evaluation != "无法生成整体评价" %}
        <section class="section">
            <div class="section__header">
                <span class="section__number">07</span>
                <div>
                    <h2 class="section__title">整体评价</h2>
                    <p class="section__subtitle">产品在 Reddit 上的口碑总结</p>
                </div>
            </div>
            <div class="analysis-box">
                <div class="analysis-box__content">{{ improvement_suggestions.overall_evaluation }}</div>
            </div>
        </section>
        {% endif %}

        <!-- Posts Section -->
        <section id="posts" class="section">
            <div class="section__header">
                <span class="section__number">08</span>
                <div>
                    <h2 class="section__title">热门帖子</h2>
                    <p class="section__subtitle">按分数排序的 Top 10 讨论</p>
                </div>
            </div>
            
            {% for post in posts %}
            <article class="post-card">
                <h3 class="post-card__title">
                    {% if post.url %}
                    <a href="{{ post.url }}" target="_blank" rel="noopener noreferrer" class="post-card__title-link">
                        {{ post.title }}
                    </a>
                    {% else %}
                    {{ post.title }}
                    {% endif %}
                </h3>
                
                <div class="post-card__meta">
                    <div class="post-card__meta-item">
                        <span class="post-card__meta-icon">👤</span>
                        <span>{{ post.author }}</span>
                    </div>
                    <div class="post-card__meta-item">
                        <span class="post-card__meta-icon">📍</span>
                        <span>r/{{ post.subreddit }}</span>
                    </div>
                    <div class="post-card__meta-item">
                        <span class="post-card__meta-icon">⬆️</span>
                        <span class="post-card__score">{{ post.score }} 分</span>
                    </div>
                    <div class="post-card__meta-item">
                        <span class="post-card__meta-icon">💬</span>
                        <span>{{ post.num_comments }} 条评论</span>
                    </div>
                    {% if post.created_utc %}
                    <div class="post-card__meta-item">
                        <span class="post-card__meta-icon">📅</span>
                        <span>{{ post.created_utc[:10] }}</span>
                    </div>
                    {% endif %}
                </div>

                {% if post.content %}
                <div class="post-card__content">
                    {{ post.content[:300] }}{% if post.content|length > 300 %}...{% endif %}
                </div>
                {% endif %}

                {% if post.url %}
                <a href="{{ post.url }}" target="_blank" rel="noopener noreferrer" class="post-card__link">
                    查看原文 →
                </a>
                {% endif %}

                {% if post.comments %}
                <div class="post-card__comments" style="margin-top: 20px;">
                    <div class="post-card__comments-title">精选评论</div>
                    {% for comment in post.comments[:3] %}
                    <div class="post-card__comment">
                        <span class="post-card__comment-author">{{ comment.author }}</span>
                        {{ comment.body[:150] }}{% if comment.body|length > 150 %}...{% endif %}
                    </div>
                    {% endfor %}
                </div>
                {% endif %}
            </article>
            {% else %}
            <div class="empty-state">
                <div class="empty-state__icon">📝</div>
                <div class="empty-state__text">暂无帖子数据</div>
            </div>
            {% endfor %}
        </section>

        <!-- Footer -->
        <footer class="footer">
            <div class="footer__content">
                <div class="footer__text">本报告由跨境电商竞品监控系统自动生成</div>
                <div class="footer__logo">Reddit Analysis</div>
            </div>
        </footer>
    </div>

    <script>
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animationPlayState = 'running';
                }
            });
        }, observerOptions);

        document.querySelectorAll('.section').forEach(section => {
            observer.observe(section);
        });
    </script>
</body>
</html>
"""
        return self.env.from_string(template).render(vars)


if __name__ == "__main__":
    generator = HTMLGenerator()
    print("HTML生成器初始化完成")
