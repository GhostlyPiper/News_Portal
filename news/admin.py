from django.contrib import admin

from .models import (
                    Author,
                    Category,
                    Post,
                    Comment,
                    CategorySubscribers,
                    PostCategory,
                    AuthorSubscribers
                    )


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(CategorySubscribers)
admin.site.register(PostCategory)
