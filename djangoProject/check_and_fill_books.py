"""
检查并填充书籍数据
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
django.setup()

from books.models import Book

# 查看现有书籍数据
books = Book.objects.all()
print(f"📚 找到 {books.count()} 本书\n")

for i, book in enumerate(books, 1):
    print(f"书籍 {i}:")
    print(f"  ID: {book.id}")
    print(f"  书名: {book.title}")
    print(f"  作者: {book.author}")
    print(f"  分类: {book.category}")
    print(f"  ISBN: {book.isbn}")
    print(f"  出版社: {book.publisher or '❌ 缺失'}")
    print(f"  出版日期: {book.publish_date or '❌ 缺失'}")
    print(f"  简介: {book.description[:50] if book.description else '❌ 缺失'}...")
    print()

# 智能填充缺失字段
print("\n" + "="*50)
print("🔧 开始智能填充缺失字段...")
print("="*50 + "\n")

# 根据书名智能推断信息
book_data = {
    "Python": {
        "publisher": "人民邮电出版社",
        "publish_date": "2023-01-01",
        "description": "这是一本关于Python编程的优秀教材，适合初学者和进阶学习者。书中详细介绍了Python语言的基础知识、数据结构、面向对象编程、常用库等内容。通过大量实例帮助读者快速掌握Python编程技能。"
    },
    "Java": {
        "publisher": "机械工业出版社",
        "publish_date": "2022-06-01",
        "description": "Java编程入门经典教程，涵盖Java基础语法、面向对象编程、集合框架、多线程、网络编程等核心内容。适合零基础读者学习，也可作为Java程序员的参考手册。"
    },
    "算法": {
        "publisher": "清华大学出版社",
        "publish_date": "2023-03-01",
        "description": "算法导论经典教材，深入讲解数据结构与算法设计。包括排序、查找、图论、动态规划等经典算法，配有详细的实现代码和案例分析，是计算机专业学生和程序员的必读书籍。"
    },
    "数据库": {
        "publisher": "电子工业出版社",
        "publish_date": "2022-09-01",
        "description": "数据库系统原理与应用教程，介绍关系型数据库的基本概念、SQL语言、数据库设计、事务处理、并发控制等内容。理论与实践相结合，适合数据库学习者和从业人员。"
    },
    "机器学习": {
        "publisher": "人民邮电出版社",
        "publish_date": "2023-05-01",
        "description": "机器学习入门到精通，涵盖监督学习、无监督学习、深度学习等核心内容。通过Python实战案例，帮助读者理解机器学习算法原理并掌握实际应用技能。适合AI方向的学习者。"
    },
    "Web": {
        "publisher": "机械工业出版社",
        "publish_date": "2023-02-01",
        "description": "Web开发全栈教程，讲解HTML、CSS、JavaScript前端技术，以及后端开发、数据库操作、API设计等内容。实战项目丰富，帮助读者快速成为全栈开发工程师。"
    },
}

updated_count = 0
for book in books:
    needs_update = False
    
    # 检查是否需要填充
    if not book.publisher or not book.publish_date or not book.description:
        # 根据书名关键词匹配
        matched_data = None
        for keyword, data in book_data.items():
            if keyword.lower() in book.title.lower():
                matched_data = data
                break
        
        # 如果没有匹配到，使用通用数据
        if not matched_data:
            matched_data = {
                "publisher": "综合出版社",
                "publish_date": "2023-01-01",
                "description": f"《{book.title}》是一本由{book.author}编写的{book.category}类书籍。本书内容丰富，结构清晰，适合相关领域的学习者和从业人员阅读参考。"
            }
        
        # 填充缺失字段
        if not book.publisher:
            book.publisher = matched_data["publisher"]
            needs_update = True
            print(f"✅ 为《{book.title}》填充出版社: {matched_data['publisher']}")
        
        if not book.publish_date:
            book.publish_date = matched_data["publish_date"]
            needs_update = True
            print(f"✅ 为《{book.title}》填充出版日期: {matched_data['publish_date']}")
        
        if not book.description:
            book.description = matched_data["description"]
            needs_update = True
            print(f"✅ 为《{book.title}》填充简介: {matched_data['description'][:50]}...")
        
        if needs_update:
            book.save()
            updated_count += 1
            print(f"💾 已保存《{book.title}》的更新\n")

print("\n" + "="*50)
print(f"🎉 完成！共更新了 {updated_count} 本书的信息")
print("="*50)

# 再次显示所有书籍
print("\n📚 更新后的书籍列表：\n")
for i, book in enumerate(Book.objects.all(), 1):
    print(f"{i}. 《{book.title}》")
    print(f"   作者: {book.author}")
    print(f"   出版社: {book.publisher}")
    print(f"   出版日期: {book.publish_date}")
    print(f"   简介: {book.description[:80]}...")
    print()
