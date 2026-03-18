#!/usr/bin/env python3
"""
AI Daily News Fetcher
抓取AI新闻并生成JSON数据和更新首页
"""

import json
import re
import os
from datetime import datetime, timedelta
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# 新闻源配置
NEWS_SOURCES = {
    'techcrunch': {
        'url': 'https://techcrunch.com/category/artificial-intelligence/',
        'name': 'TechCrunch'
    }
}

# 分类关键词
CATEGORIES = {
    'enterprise': ['enterprise', 'company', 'business', '收购', '合并', '融资', 'IPO', '五角大楼', '政府'],
    'product': ['launch', 'release', 'product', '发布', '推出', '上线', '开放'],
    'tool': ['tool', 'code', 'IDE', 'editor', '配置', 'setup', 'workflow'],
    'research': ['research', 'paper', 'study', '论文', '研究', '算法', '模型'],
    'policy': ['policy', 'regulation', 'law', '政策', '法规', '监管']
}

def fetch_techcrunch_news():
    """从TechCrunch抓取AI新闻"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(NEWS_SOURCES['techcrunch']['url'], headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        articles = []

        # TechCrunch文章选择器
        article_elements = soup.find_all('article', class_=re.compile('post-block'))[:15]

        for article in article_elements:
            try:
                # 提取标题
                title_elem = article.find('h2', class_=re.compile('post-block__title')) or \
                           article.find('a', class_=re.compile('post-block__title__link'))
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)

                # 提取链接
                link_elem = title_elem if title_elem.name == 'a' else title_elem.find('a')
                link = link_elem.get('href', '') if link_elem else ''

                # 提取摘要
                excerpt_elem = article.find('div', class_=re.compile('post-block__content')) or \
                              article.find('p', class_=re.compile('excerpt'))
                excerpt = excerpt_elem.get_text(strip=True) if excerpt_elem else ''

                # 提取时间
                time_elem = article.find('time')
                pub_date = time_elem.get('datetime', '') if time_elem else datetime.now().isoformat()

                if title and link:
                    articles.append({
                        'title': title,
                        'url': link,
                        'summary': excerpt[:200] + '...' if len(excerpt) > 200 else excerpt,
                        'source': 'TechCrunch',
                        'published': pub_date
                    })
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue

        return articles

    except Exception as e:
        print(f"Error fetching TechCrunch: {e}")
        return []

def categorize_news(title, summary):
    """根据标题和摘要分类新闻"""
    text = (title + ' ' + summary).lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in text:
                return category

    return 'other'

def generate_news_data():
    """生成当日新闻数据"""
    today = datetime.now().strftime('%Y-%m-%d')

    # 抓取新闻
    articles = fetch_techcrunch_news()

    # 处理新闻数据
    news_items = []
    for article in articles[:12]:  # 限制12条
        category = categorize_news(article['title'], article['summary'])

        # 生成中文摘要（简化版，实际可用AI翻译）
        summary = article['summary'] if article['summary'] else article['title']

        news_items.append({
            'id': f"{today}-{len(news_items)}",
            'title': article['title'],
            'summary': summary,
            'url': article['url'],
            'source': article['source'],
            'category': category,
            'published': article['published']
        })

    # 统计数据
    category_count = {}
    for item in news_items:
        cat = item['category']
        category_count[cat] = category_count.get(cat, 0) + 1

    data = {
        'date': today,
        'generated_at': datetime.now().isoformat(),
        'total': len(news_items),
        'categories': category_count,
        'news': news_items
    }

    return data

def save_news_data(data):
    """保存新闻数据到JSON文件"""
    date = data['date']
    filename = f"data/{date}.json"

    os.makedirs('data', exist_ok=True)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Saved news data to {filename}")
    return filename

def update_index_html():
    """更新首页日历视图"""
    # 获取所有数据文件
    data_files = []
    if os.path.exists('data'):
        for f in os.listdir('data'):
            if f.endswith('.json'):
                date_str = f.replace('.json', '')
                data_files.append(date_str)

    data_files.sort(reverse=True)

    # 生成日历HTML
    today = datetime.now()
    current_year = today.year
    current_month = today.month

    # 读取模板并更新
    # 实际实现会更新index.html中的日历部分
    print(f"Found {len(data_files)} days of news data")
    print(f"Latest: {data_files[0] if data_files else 'None'}")

def main():
    """主函数"""
    print("Fetching AI news...")

    # 生成新闻数据
    data = generate_news_data()

    # 保存数据
    save_news_data(data)

    # 更新首页
    update_index_html()

    print(f"Done! Generated {data['total']} news items for {data['date']}")

if __name__ == '__main__':
    main()
