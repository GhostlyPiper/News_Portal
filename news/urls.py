from django.urls import path
# Импортируем созданное нами представление
from .views import (PostList,
                    PostDetail,
                    PostSearchView,
                    NewsCreate,
                    ArticlesCreate,
                    NewsEdit,
                    ArticlesEdit,
                    NewsDelete,
                    ArticlesDelete,
                    PostAuthorView,
                    CategoryList,
                    add_subscribe,

                    )


urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым,
    # чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', PostList.as_view(), name='posts_list'),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
    path('news/<int:pk>/edit', NewsEdit.as_view(), name='news_edit'),
    path('news/<int:pk>/delete', NewsDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/edit', ArticlesEdit.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete', ArticlesDelete.as_view(), name='articles_delete'),
    path('my_posts/', PostAuthorView.as_view(), name='post_author_view'),
    path('sub/', CategoryList.as_view(), name='categories'),
    path('add_sub/category/<int:pk>', add_subscribe, name='add_sub'),
]
