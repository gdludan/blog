from django import forms
class ProfileForm(forms.Form):
    interest = forms.CharField(label= '兴趣')
    aims = forms.CharField(label='最近目标')
    motto = forms.CharField(label='座右铭')
    self_reprot = forms.CharField(label='自我介绍')