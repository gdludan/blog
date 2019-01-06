from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser
####
from captcha.fields import CaptchaField

class CaptchaLoginForm(forms.Form):
    username = forms.CharField(label='用户名或邮箱',error_messages={"invalid":u"用户名填写错误或不存在此用户"})
    password = forms.CharField(label='登录密码', widget=forms.PasswordInput,error_messages={"invalid":u"密码填写错误"})
    captcha = CaptchaField(label='验证码',error_messages={"invalid":u"验证码错误"})

class MyUserCreationForm(UserCreationForm):
    # 重写初始化函数，设置自定义字段password1和password2的样式和属性
    captcha = CaptchaField(label='验证码',error_messages={"invalid":u"验证码错误"})
    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder':'密码,8-16位数字/字母/特殊符号(空格除外)'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder':'重复密码'})
    class Meta(UserCreationForm.Meta):
        model = MyUser
        # 在注册界面添加模型字段：手机号码和密码
        fields = UserCreationForm.Meta.fields +('email',)
        # 设置模型字段的样式和属性
        widgets = {
            'email': forms.widgets.TextInput(attrs={'class': 'txt tabInput', 'placeholder':'邮箱'}),
            'username': forms.widgets.TextInput(attrs={'class': 'txt tabInput', 'placeholder':'用户名'}),
        }
