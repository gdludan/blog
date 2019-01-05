from django import forms
####
from captcha.fields import CaptchaField

class CaptchaLoginForm(forms.Form):
    username = forms.CharField(label='用户名或邮箱',error_messages={"invalid":u"用户名填写错误或不存在此用户"})
    password = forms.CharField(label='登录密码', widget=forms.PasswordInput,error_messages={"invalid":u"密码填写错误"})
    captcha = CaptchaField(label='验证码',error_messages={"invalid":u"验证码错误"})

class CaptchaRegistForm(forms.Form):
    username = forms.CharField(label='用户名',error_messages={"invalid":u"用户名已经注册过"})
    email = forms.EmailField(label='邮箱地址',error_messages={"invalid":u"邮箱已经注册过"})
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确定密码', widget=forms.PasswordInput)
    captcha = CaptchaField(label='验证码',error_messages={"invalid":u"验证码错误"})