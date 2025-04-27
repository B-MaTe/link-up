from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from core import views
from core.views import CustomLoginView


urlpatterns = [
    path('', views.index, name='index'),
    path('user_info/', views.user_info, name='user_info'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('health/', views.health, name='health'),
]