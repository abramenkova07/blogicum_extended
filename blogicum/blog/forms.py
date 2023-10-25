from django import forms
from django.contrib.auth import get_user_model

from .models import Comment, Post
from .validators import validate_name


class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].validators.append(validate_name)
        self.fields['last_name'].validators.append(validate_name)

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email',)


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author', 'is_published',)
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
