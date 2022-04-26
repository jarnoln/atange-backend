from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/user/<slug:username>/', views.UserInfo.as_view(), name='user_info'),
    path('api/collective/<slug:name>/', views.CollectiveDetail.as_view(), name='collective_detail')
]
