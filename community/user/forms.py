from django import forms

class loginForm(forms.Form):
    username = forms.CharField(max_length=32, label="사용자 이름")
    password = forms.CharField(widget=forms.PasswordInput, label="비밀번호")