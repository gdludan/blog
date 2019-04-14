from django import forms


class PostForm(forms.Form):
    title = forms .CharField(label='文章标题')
    content = forms.CharField(label='文章内容')
    type = forms.TypedChoiceField(label='文章类型',
        choices=(
            ('原创','原创'),
            ('转载','转载'),
            ('杂谈','杂谈'),
        ),
    )

class UPfileForm(forms.Form):
    file = forms.FileField(label='文件')