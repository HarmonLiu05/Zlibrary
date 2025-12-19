from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="请输入真实邮箱以接收激活链接")

    class Meta:
        model = User
        fields = ['username', 'email'] # 注册时显示用户名和邮箱