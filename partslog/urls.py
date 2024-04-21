from . import views
from django.urls import path

app_name = 'partslog'
urlpatterns = [
    path('', views.logs, name='logs'),
    path('form/', views.log_form, name='log_form'),
    path('approve/', views.approval, name='approval'),
    path('approve/approved/<int:item>', views.approve_item, name='approve_item'),
]
