from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/user/<slug:username>/', views.UserInfo.as_view(), name='user_info'),
    path('api/collective/<slug:name>/questions/', views.CollectiveQuestions.as_view(), name='collective_questions'),
    path('api/collective/<slug:name>/', views.CollectiveDetail.as_view(), name='collective_detail'),
    path('api/collectives/', views.CollectiveList.as_view(), name='collective_list')
]
