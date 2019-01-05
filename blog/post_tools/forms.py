from django import forms


class PostForm(forms.Form):
    title = forms .CharField(label='文章标题')
    content = forms.CharField(label='文章内容')

class UPfileForm(forms.Form):
    file = forms.FileField(label='文件')