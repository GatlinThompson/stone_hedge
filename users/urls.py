from . import views
from django.urls import path

app_name = 'users'
urlpatterns = [
    path('', views.users, name='users'),
    path('create/', views.create_user, name='create_user'),
]
