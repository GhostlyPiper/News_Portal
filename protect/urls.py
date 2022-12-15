from django.urls import path
from .views import IndexView, set_timezone

urlpatterns = [
    path('', IndexView.as_view()),
    path('', set_timezone, name='set_timezone'),
]
