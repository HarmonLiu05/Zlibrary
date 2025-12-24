"""
Django Management Command
用于生成书籍的向量索引
"""
from django.core.management.base import BaseCommand
from books.models import Book
from books.utils.rag import get_rag_assistant


class Command(BaseCommand):
    help = '为所有书籍生成向量索引，用于 RAG 问答系统'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('开始构建书籍向量索引...'))
        
        # 获取所有书籍
        books = Book.objects.all()
        book_count = books.count()
        
        if book_count == 0:
            self.stdout.write(self.style.WARNING('数据库中没有书籍，请先添加书籍数据'))
            return
        
        self.stdout.write(f'找到 {book_count} 本书籍')
        
        # 构建索引
        try:
            rag_assistant = get_rag_assistant()
            rag_assistant.build_index(books)
            self.stdout.write(self.style.SUCCESS(f'✅ 成功为 {book_count} 本书生成向量索引！'))
            self.stdout.write(self.style.SUCCESS('现在可以使用 AI 问答功能了'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ 构建索引失败: {e}'))
            self.stdout.write(self.style.WARNING('请检查 OPENAI_API_KEY 是否正确配置'))
