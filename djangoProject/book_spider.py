import requests
import csv
import time
import random
from urllib.parse import quote
from bs4 import BeautifulSoup
import re

class ChineseBookSpider:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

    def search_books_on_jd(self, keyword, page=1):
        """从京东搜索图书"""
        books = []
        try:
            # 使用京东搜索
            encoded_keyword = quote(keyword)
            url = f'https://search.jd.com/Search?keyword={encoded_keyword}&page={page}'
            
            response = requests.get(url, headers=self.headers)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # 查找商品列表
                items = soup.find_all('div', class_='gl-i-wrap')
                
                for item in items[:10]:  # 限制每页最多10本书
                    book = self.parse_jd_item(item)
                    if book:
                        books.append(book)
                        
        except Exception as e:
            print(f"搜索 {keyword} 时出错: {e}")
            
        return books

    def parse_jd_item(self, item):
        """解析京东商品信息"""
        try:
            # 获取书名
            title_elem = item.find('div', class_='p-name')
            if title_elem:
                title_link = title_elem.find('a')
                if title_link:
                    title = title_link.get_text(strip=True)
                else:
                    title = "未知书名"
            else:
                title = "未知书名"

            # 获取价格（可能可以间接获得更多信息）
            price_elem = item.find('div', class_='p-price')
            if price_elem:
                price = price_elem.get_text(strip=True)
            else:
                price = ""

            # 获取图片
            img_elem = item.find('div', class_='p-img')
            if img_elem:
                img = img_elem.find('img')
                if img:
                    img_src = img.get('src') or img.get('data-lazy-img')
                    if img_src and not img_src.startswith('http'):
                        img_src = 'https:' + img_src
                else:
                    img_src = ""
            else:
                img_src = ""

            # 为模拟数据生成ISBN（实际使用时需要更复杂的逻辑获取真实ISBN）
            import uuid
            fake_isbn = f"978-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}-{random.randint(0, 9)}"
            
            return {
                'title': title[:200] if title != "未知书名" else f"图书_{int(time.time())}_{random.randint(1000, 9999)}",
                'author': f"作者_{random.randint(100, 999)}",
                'isbn': fake_isbn,
                'category': '计算机' if '编程' in title or 'Python' in title or '计算机' in title else 
                          '文学' if '文学' in title or '小说' in title else 
                          '经济' if '经济' in title or '金融' in title else 
                          '综合',
                'cover_image_url': img_src if img_src else "",
                'publisher': f"出版社_{random.randint(100, 999)}",
                'publish_date': f"{random.randint(2010, 2024)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                'pages': random.randint(100, 800),
                'description': f"关于{title}的详细介绍，这是一本非常优秀的图书。",
                'stock': random.randint(1, 10)
            }
        except Exception as e:
            print(f"解析商品信息时出错: {e}")
            return None

    def search_books_by_mock_data(self, keywords, count_per_keyword=5):
        """使用模拟数据生成图书（当真实API不可用时）"""
        books = []
        sample_authors = ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十']
        sample_publishers = ['人民邮电出版社', '机械工业出版社', '清华大学出版社', '电子工业出版社', '中信出版社']
        sample_categories = ['计算机', '文学', '经济', '历史', '心理学', '艺术', '科学', '教育']
        
        for keyword in keywords:
            for i in range(count_per_keyword):
                fake_isbn = f"978-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}-{random.randint(0, 9)}"
                
                book = {
                    'title': f"{keyword}实战指南 第{i+1}版" if '编程' in keyword or 'Python' in keyword else f"{keyword}精解",
                    'author': random.choice(sample_authors),
                    'isbn': fake_isbn,
                    'category': random.choice(sample_categories),
                    'cover_image_url': f"https://via.placeholder.com/200x280.png?text={quote(keyword[:10])}",
                    'publisher': random.choice(sample_publishers),
                    'publish_date': f"{random.randint(2018, 2024)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                    'pages': random.randint(150, 600),
                    'description': f"这是一本关于{keyword}的优秀图书，内容详实，适合学习和参考。",
                    'stock': random.randint(1, 15)
                }
                books.append(book)
                time.sleep(0.2)  # 减少请求频率
                
        return books

    def save_to_csv(self, books, filename='chinese_books.csv'):
        """保存数据到CSV文件"""
        if not books:
            print("没有数据可保存")
            return
            
        fieldnames = [
            'title', 'author', 'isbn', 'category',
            'cover_image_url', 'publisher', 'publish_date',
            'pages', 'description', 'stock'
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(books)
            
        print(f"成功保存 {len(books)} 本图书到 {filename}")

    def crawl_books(self, keywords=None):
        """爬取图书数据"""
        if keywords is None:
            keywords = ['Python编程', '数据科学', '人工智能', '机器学习', '经济学', '历史', '文学']
        
        print("由于API访问受限，使用模拟数据生成图书...")
        all_books = self.search_books_by_mock_data(keywords, count_per_keyword=8)
        
        # 去重
        seen_isbns = set()
        unique_books = []
        for book in all_books:
            if book['isbn'] not in seen_isbns:
                seen_isbns.add(book['isbn'])
                unique_books.append(book)
        
        return unique_books

if __name__ == "__main__":
    spider = ChineseBookSpider()
    
    print("开始获取中文图书数据...")
    all_books = spider.crawl_books(['Python编程', '数据科学', '人工智能', '机器学习', '经济学', '历史', '文学'])
    
    # 保存数据
    spider.save_to_csv(all_books, 'chinese_books.csv')
    print(f"总共生成了 {len(all_books)} 本不重复的图书数据")