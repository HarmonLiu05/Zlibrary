"""
直接测试构建索引流程
"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
django.setup()

from books.models import Book
from books.utils.rag import get_rag_assistant

print("="*60)
print("🧪 测试构建向量索引")
print("="*60 + "\n")

try:
    # 获取书籍数据
    books = Book.objects.all()
    print(f"📚 找到 {books.count()} 本书\n")
    
    for book in books:
        print(f"  - 《{book.title}》 by {book.author}")
    
    print("\n" + "-"*60)
    print("开始构建索引...\n")
    
    # 获取 RAG 助手
    rag = get_rag_assistant()
    
    # 构建索引
    rag.build_index(books)
    
    print("\n" + "="*60)
    print("✅ 测试完成！")
    print("="*60)
    
except KeyboardInterrupt:
    print("\n\n⚠️  用户中断")
    sys.exit(0)
    
except Exception as e:
    print(f"\n\n❌ 测试失败: {e}")
    import traceback
    print(f"\n详细错误:\n{traceback.format_exc()}")
    sys.exit(1)
