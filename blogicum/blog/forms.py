from django import forms
from django.contrib.auth import get_user_model

from .models import Comment, Post


class UserForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email',)
        widgets = {
            'email': forms.EmailInput(attrs={'type': 'email'})
        }


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author', 'is_published',)
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
