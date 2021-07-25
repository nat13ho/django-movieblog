from django import forms


class ProfileForm(forms.Form):
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'user__image-input'
    }))
    username = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={
        'class': 'register__window-input',
        'placeholder': 'Имя пользователя'
    }))
    is_subscribed = forms.BooleanField(required=None)
