import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from books.models import Book  # 确保导入更新后的模型

class Command(BaseCommand):
    help = '从CSV文件批量导入图书数据'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='CSV文件路径')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        with open(csv_file, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            books_created = 0
            books_updated = 0
            
            for row_idx, row in enumerate(reader, 1):
                try:
                    # 解析出版日期
                    publish_date = None
                    if row.get('publish_date'):
                        try:
                            publish_date = datetime.strptime(row['publish_date'][:10], '%Y-%m-%d').date()
                        except ValueError:
                            pass  # 如果日期格式不正确则设为None
                            
                    # 转换页数
                    pages = None
                    if row.get('pages'):
                        try:
                            pages = int(row['pages'])
                        except ValueError:
                            pass  # 如果页数不是数字则设为None
                    
                    # 转换库存
                    stock = 1
                    if row.get('stock'):
                        try:
                            stock = int(row['stock'])
                        except ValueError:
                            pass  # 如果库存不是数字则设为默认值1
                    
                    book, created = Book.objects.update_or_create(
                        isbn=row['isbn'],
                        defaults={
                            'title': row.get('title', ''),
                            'author': row.get('author', ''),
                            'category': row.get('category', '综合'),
                            'cover_image_url': row.get('cover_image_url', ''),
                            'publisher': row.get('publisher', ''),
                            'publish_date': publish_date,
                            'pages': pages,
                            'description': row.get('description', ''),
                            'stock': stock
                        }
                    )
                    
                    if created:
                        books_created += 1
                    else:
                        books_updated += 1
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'第 {row_idx} 行数据处理错误: {e}')
                    )
                    continue
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'导入完成! 新增 {books_created} 本书, 更新 {books_updated} 本书'
                )
            )