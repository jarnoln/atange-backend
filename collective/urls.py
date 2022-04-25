from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('collective/<slug:collective_name>/', views.collective, name='collective'),
    path('api/user/<slug:username>/', views.UserInfo.as_view(), name='user_info')
]
