from django import forms

from posts.models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'post__comments-input',
                'placeholder': 'Оставить комментарий'
            })
        }
