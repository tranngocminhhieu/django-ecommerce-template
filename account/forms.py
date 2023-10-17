import re

from django import forms
from django.contrib.auth.models import User

# Not in use
class SignUpForm(forms.Form):
    username = forms.CharField(max_length=255, label='Username', required=True)
    email = forms.EmailField(max_length=255, label='Email', required=True)
    password1 = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', required=True, widget=forms.PasswordInput)

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Confirm password is not match')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(pattern=r'^[A-Za-z0-9]+(?:[_-][A-Za-z0-9]+)*$', string=username):
            raise forms.ValidationError('Username only accepts letters, numbers, and _')
        try:
            User.objects.get(username=username)  # Kiểm tra username trong database
        except User.DoesNotExist:  # Nếu chưa có thì sẽ bị lỗi không tồn tại, vậy thì có thể signup được
            return username
        raise forms.ValidationError('Username is existed, try another username')  # Nếu không bị lỗi thì username đã tồn tại, phải raise lên

    def save(self):
        User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            # is_staff=True,
        )
