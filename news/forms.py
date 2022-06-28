from django import forms
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# from django.forms import ModelForm

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'dateCreation',
            'postCategory',
            'rating',
            'text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        body = cleaned_data.get("body")
        if body is not None and len(body) < 20:
            raise ValidationError({
                "body": "Текст поста не может быть менее 20 символов."
            })

        title = cleaned_data.get("title")
        if title == body:
            raise ValidationError(
                "Название не должно совпадать с основным текстом."
            )
        return cleaned_data
