from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from core import views
from core.views import CustomLoginView

urlpatterns = [
    path('', views.index, name='index'),
    path('user_info/', views.user_info, name='user_info'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),

    #administrator urls
    path('administrator/bejegyzes/', views.bejegyzes, name='bejegyzes'),
    path('administrator/csoport/', views.csoport, name='csoport'),
    path('administrator/komment/', views.komment, name='komment'),
    path('administrator/uzenet/', views.uzenet, name='uzenet'),
]