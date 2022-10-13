from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
                    BaseRegisterView,
                    ProfileUpdateView,
                    log_in_author,
                    log_out_author
                    )

urlpatterns = [
    path('login/',
         LoginView.as_view(template_name='sign/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='sign/logout.html'),
         name='logout'),
    path('signup/',
         BaseRegisterView.as_view(template_name='sign/signup.html'),
         name='signup'),
    path('profile_update/',
         ProfileUpdateView.as_view(
             template_name='account/profile_update.html'
         ),
         name='profile_update'),
    path('upgrade/', log_in_author, name='upgrade'),
    path('log_out_author/', log_out_author, name='upgrade'),
]
