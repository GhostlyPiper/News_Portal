# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  )

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.shortcuts import get_object_or_404, render
from django.core.cache import cache  # импортируем наш кэш
# импортируем функцию для перевода
from django.utils.translation import gettext as _

from datetime import datetime
from .models import Post, Author, Category
from .filters import PostFilter
from .forms import PostForm
from .tasks import notify_news_create
from NewsPaper.settings import DAILY_POST_LIMIT


class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news/posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    # вот так мы можем указать количество записей на странице:
    paginate_by = 5


class PostDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной новости
    model = Post
    # Используем другой шаблон — post.html
    template_name = 'news/post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'
    permission_required = (
        'news.view_post',
    )

    # переопределяем метод получения объекта
    def get_object(self, *args, **kwargs):
        # Кэш очень похож на словарь, и метод get действует так же.
        # Он забирает значение по ключу, если его нет, то забирает None.
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostSearchView(ListView):
    model = Post
    template_name = 'news/post_search.html'
    ordering = '-dateCreation'
    paginate_by = 5
    context_object_name = 'search_list'

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter(),
        }


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'
    permission_required = (
        'news.add_post',
    )
    success_url = "/news/my_posts/"
    error_message = _('No more than') + f' {DAILY_POST_LIMIT} ' + _(
        'posts a day, dude!')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.categoryType = 'NW'
        self.object.author = Author.objects.get(authorUser=self.request.user)
        self.object.save()

        cat = Category.objects.get(pk=self.request.POST['postCategory'])
        self.object.postCategory.add(cat)

        validated = super().form_valid(form)
        notify_news_create.apply_async(
            [self.object.pk],
            countdown=5,
            expires=100
        )

        return validated

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all()
        today_posts_count = 0
        limit = DAILY_POST_LIMIT

        for post in posts:
            time_delta = datetime.now().date() - post.dateCreation.date()
            if time_delta.total_seconds() < (60 * 60 * 24):
                today_posts_count += 1

        context['posts_limit'] = limit <= today_posts_count
        context['limit'] = limit
        return context


class NewsEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'
    permission_required = (
        'news.change_post',
    )

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        post.author = Author.objects.get(authorUser=self.request.user)
        return super().form_valid(form)


class NewsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('posts_list')


class ArticlesCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/articles_edit.html'
    permission_required = (
        'news.add_post',
    )
    success_url = "/news/my_posts/"
    error_message = _('No more than') + f' {DAILY_POST_LIMIT} ' + _(
        'posts a day, dude!')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = Author.objects.get(authorUser=self.request.user)
        self.object.save()

        cat = Category.objects.get(pk=self.request.POST['postCategory'])
        self.object.postCategory.add(cat)

        validated = super().form_valid(form)
        notify_news_create.apply_async(
            [self.object.pk],
            countdown=5,
            expires=100
        )

        return validated

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all()
        today_posts_count = 0
        limit = DAILY_POST_LIMIT

        for post in posts:
            time_delta = datetime.now().date() - post.dateCreation.date()
            if time_delta.total_seconds() < (60 * 60 * 24):
                today_posts_count += 1

        context['posts_limit'] = limit <= today_posts_count
        context['limit'] = limit
        return context


class ArticlesEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/articles_edit.html'
    permission_required = (
        'news.change_post',
    )

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Author.objects.get(authorUser=self.request.user)
        return super().form_valid(form)


class ArticlesDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/articles_delete.html'
    success_url = reverse_lazy('posts_list')


class PostAuthorView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news/post_author_view.html'
    paginate_by = 3
    context_object_name = 'author_posts'

    def get_queryset(self):
        my_post = Post.objects.filter(author__authorUser=self.request.user).order_by('-dateCreation')
        return my_post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class CategoryList(ListView):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'
    paginate_by = 3

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        quaryset = Post.objects.filter(postCategory=self.category).order_by('-dateCreation')
        return quaryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def sub_cat(request, pk):
    user = request.user
    cat = Category.objects.get(id=pk)
    is_subscribed = cat.subscribers.filter(id=user.id).exists()

    message = _('You have successfully subscribed to '
                'the newsletter of posts of the category')

    if not is_subscribed:
        cat.subscribers.add(user)

    return render(
        request,
        'news/subscribe.html',
        {'category': cat, 'message': message}
    )


@login_required
def un_sub_cat(request, pk):
    user = request.user
    cat = Category.objects.get(id=pk)
    is_subscribed = cat.subscribers.filter(id=user.id).exists()

    message = _('You have successfully unsubscribed '
                'from the mailing list of posts of the category')

    if is_subscribed:
        cat.subscribers.remove(user)

    return render(
        request,
        'news/un_subscribe.html',
        {'category': cat, 'message': message}
    )
