from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<int:record_id>/', views.return_book, name='return_book'),
    path('profile/', views.profile, name='profile'),
    path('import/', views.bulk_import, name='bulk_import'),
    path('register/', views.register, name='register'),
    path('activate/<str:token>/', views.activate, name='activate'),
]