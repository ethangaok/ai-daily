# AI Daily

每日AI新闻自动抓取和展示网站。

## 功能

- 📅 **日历视图** - 查看所有历史日期的AI新闻
- 📰 **新闻详情** - 按分类浏览每日AI新闻
- 🔄 **自动更新** - 每天自动抓取最新AI新闻
- 📱 **响应式设计** - 支持桌面和移动端

## 技术栈

- GitHub Pages - 静态网站托管
- GitHub Actions - 定时自动抓取
- Python + BeautifulSoup - 新闻抓取
- 纯前端JavaScript - 数据展示

## 本地开发

```bash
# 安装依赖
pip install requests beautifulsoup4

# 运行抓取脚本
python scripts/fetch_news.py

# 本地预览
python -m http.server 8000
```

## 部署

1. Fork 本仓库
2. 在 Settings > Pages 中启用 GitHub Pages
3. GitHub Actions 会自动每天抓取新闻

## 数据来源

- TechCrunch AI 分类

## License

MIT
