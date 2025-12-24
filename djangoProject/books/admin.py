from django.contrib import admin
from .models import Book, BorrowRecord

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publisher', 'stock')
    search_fields = ('title', 'author', 'isbn', 'publisher')
    fields = ('title', 'author', 'isbn', 'category', 'publisher', 'publish_date', 'stock', 'cover_image', 'description')

@admin.register(BorrowRecord)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date', 'is_returned')