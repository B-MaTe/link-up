from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from core import views
from core.views import CustomLoginView


urlpatterns = [
    path('', views.index, name='index'),
    path('user_info/', views.user_info, name='user_info'),
    path('user_info/<int:user_id>/', views.user_info, name='user_info'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('connections/', views.connections, name='connections'),
    path('health/', views.health, name='health'),
    path('search_users/', views.search_users, name='search_users'),
    path('csoportok/', views.csoportok_view, name='csoportok'),
    path('message/all', views.all_message, name='all_messages'),
    path('message/new', views.new_message, name='new_message'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('kommentek', views.kommentek_for_bejegyzes, name='kommentek_for_bejegyzes'),
    path('csoportok/', views.csoportok_view, name='csoportok'),
    path('message/<int:group_id>/', views.message, name='message'),
]