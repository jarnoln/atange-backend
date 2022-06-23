from django.urls import path

from .views import views
from .views.collective_admin_view import CollectiveAdmin


urlpatterns = [
    path(
        "api/collective/<slug:collective_name>/question/<slug:question_name>/answer/<slug:username>/",
        views.AnswerDetail.as_view(),
        name="answer",
    ),
    path(
        "api/collective/<slug:collective_name>/question/<slug:question_name>/",
        views.QuestionDetail.as_view(),
        name="question",
    ),
    path(
        "api/collective/<slug:name>/answers/",
        views.CollectiveAnswers.as_view(),
        name="answers",
    ),
    path(
        "api/collective/<slug:collective_name>/admin/<slug:username>/",
        CollectiveAdmin.as_view(),
        name="collective_admin",
    ),
    path(
        "api/collective/<slug:collective_name>/admins/",
        views.CollectiveAdmins.as_view(),
        name="collective_admins",
    ),
    path(
        "api/collective/<slug:name>/permissions/",
        views.CollectivePermissions.as_view(),
        name="collective_permissions",
    ),
    path(
        "api/collective/<slug:name>/questions/",
        views.CollectiveQuestions.as_view(),
        name="questions",
    ),
    path(
        "api/collective/<slug:name>/",
        views.CollectiveDetail.as_view(),
        name="collective",
    ),
    path("api/collectives/", views.CollectiveList.as_view(), name="collectives"),
    path("api/user/<slug:username>/", views.UserInfo.as_view(), name="user_info"),
    path("", views.index, name="index"),
]
