from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'postCategory',
            # 'categoryType',
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 20:
            raise ValidationError({
                "text": _("The text of the post can not "
                          "be less than 20 characters.")
            })

        title = cleaned_data.get("title")
        if title == text:
            raise ValidationError(
                _("The title should not match the main text.")
            )
        return cleaned_data
