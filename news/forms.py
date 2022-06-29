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
            'title',
            'text',
            'postCategory',
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 20:
            raise ValidationError({
                "text": "Текст поста не может быть менее 20 символов."
            })

        title = cleaned_data.get("title")
        if title == text:
            raise ValidationError(
                "Название не должно совпадать с основным текстом."
            )
        return cleaned_data
