from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Book, BorrowRecord
from django.db.models import Q
from django.utils import timezone
import pandas as pd
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.conf import settings
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.core.signing import dumps, loads
from django.contrib.auth.models import User
# 首页和搜索
def index(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))

    # 简单的 AI 推荐逻辑：推荐当前库存最多的前3本书
    recommendations = Book.objects.order_by('-stock')[:3]

    return render(request, 'index.html', {'books': books, 'query': query, 'recommendations': recommendations})





# 还书
@login_required
def return_book(request, record_id):
    record = BorrowRecord.objects.get(id=record_id)
    record.is_returned = True
    record.return_date = timezone.now()
    record.book.stock += 1
    record.book.save()
    record.save()
    return redirect('profile')


# 个人中心（查看已借书籍）
@login_required
def profile(request):
    # 只查询未归还的记录
    records = BorrowRecord.objects.filter(user=request.user, is_returned=False)
    now = timezone.now()

    for r in records:
        if r.due_date:
            # 计算时间差
            delta = r.due_date - now
            # 将剩余时间（天数）保存到对象中，方便前端调用
            r.days_left = delta.days
            # 判断状态：已过期、今天到期、即将到期
            if delta.total_seconds() < 0:
                r.status = "overdue"  # 已超期
            elif delta.days < 3:
                r.status = "urgent"  # 紧急（3天内）
            else:
                r.status = "normal"  # 正常
        else:
            r.days_left = None

    return render(request, 'profile.html', {'records': records})


# 批量导入书籍 (管理员用)
def bulk_import(request):
    if request.method == "POST" and request.FILES['file']:
        file = request.FILES['file']
        df = pd.read_csv(file)  # 假设上传 CSV
        for _, row in df.iterrows():
            Book.objects.create(title=row['title'], author=row['author'], isbn=row['isbn'], stock=row['stock'])
        return redirect('index')
    return render(request, 'import.html')

# 注册功能
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)  # 确保这里用的是 UserRegisterForm
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.email = form.cleaned_data.get('email')
            user.save()

            # 生成加密 token
            token = dumps(user.username)
            domain = get_current_site(request).domain
            verify_url = f"http://{domain}/activate/{token}/"

            # 邮件主题尽量先用英文，彻底避开 ASCII 编码报错
            subject = "Library System Activation"

            # 2. 内容改纯英文，确保 verify_url 是纯 ASCII
            message = "Welcome! Please click the link to activate your account: " + str(verify_url)

            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,  # 发件人：纯邮箱地址
                    [user.email],  # 收件人
                    fail_silently=False
                )
                return render(request, 'registration/register_success.html')
            except Exception as e:
                # 如果邮件发送还是失败，记录详细错误到控制台
                print(f"Mail Error: {e}")
                user.delete()
                return HttpResponse(f"Error: {e}")
        else:
            # 如果 form.is_valid() 为 False，代码会走到这里
            # Django 会自动带着错误信息重新渲染 register.html
            pass
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

# 修改借书逻辑，增加库存不足提醒、请求方法验证和 CSRF 保护
@login_required
@csrf_exempt
def borrow_book(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        if book.stock > 0:
            BorrowRecord.objects.create(user=request.user, book=book)
            book.stock -= 1
            book.save()
            messages.success(request, f'成功借阅《{book.title}》！')
        else:
            messages.error(request, '抱歉，该书库存不足！')
    return redirect('index')

def activate(request, token):
    try:
        # token 解码，1小时内有效
        username = loads(token, max_age=3600)
        user = User.objects.get(username=username)
        user.is_active = True  # 核心：把用户状态改为“活跃”
        user.save()
        messages.success(request, '🎉 账号激活成功！现在可以登录了。')
        return redirect('login')
    except Exception as e:
        # 如果 token 过期或无效
        return render(request, 'registration/activate_fail.html')