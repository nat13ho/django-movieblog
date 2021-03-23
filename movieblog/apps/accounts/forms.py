from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserLoginForm(auth_forms.AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'login__window-input',
            'placeholder': 'Имя пользователя',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'login__window-input',
            'placeholder': 'Пароль',
        })


class EmailForm(auth_forms.PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'register__window-input',
            'placeholder': 'Email',
        })


class NewPasswordForm(auth_forms.SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'class': 'register__window-input',
            'placeholder': 'Пароль'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'register__window-input',
            'placeholder': 'Потвердите пароль'
        })


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'register__window-input',
        'placeholder': 'Потвердите пароль'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'register__window-input',
                'placeholder': 'Имя пользователя'}),
            'email': forms.EmailInput(attrs={
                'class': 'register__window-input',
                'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={
                'class': 'register__window-input',
                'placeholder': 'Пароль'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.data.get('confirm_password')

        if confirm_password != password:
            raise ValueError('Пароли не совпадают')
        else:
            return password

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким адресом электронной почты уже существует')
        return email


class CustomPasswordChangeForm(auth_forms.PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'class': 'register__window-input',
            'placeholder': 'Текущий пароль'
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'register__window-input',
            'placeholder': 'Новый пароль'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'register__window-input',
            'placeholder': 'Потвердите пароль'
        })
