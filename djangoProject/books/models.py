from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Book(models.Model):
    title = models.CharField('书名', max_length=200)
    author = models.CharField('作者', max_length=100)
    isbn = models.CharField('ISBN', max_length=20, unique=True)
    category = models.CharField('分类', max_length=50, default='综合')
    stock = models.IntegerField('库存', default=1)

    def __str__(self):
        return self.title

class BorrowRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField('借阅时间', auto_now_add=True)
    due_date = models.DateTimeField('应还日期', null=True, blank=True)
    return_date = models.DateTimeField('归还时间', null=True, blank=True)
    is_returned = models.BooleanField('是否已还', default=False)

    def save(self, *args, **kwargs):
        if not self.due_date:
            from django.utils import timezone
            from datetime import timedelta
            self.due_date = timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)