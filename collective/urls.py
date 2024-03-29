from django.urls import path

from .views.index import index
from .views.answer_detail import AnswerDetail
from .views.collective_admins import CollectiveAdmins
from .views.collective_admin import CollectiveAdmin
from .views.collective_answers import CollectiveAnswers
from .views.collective_detail import CollectiveDetail
from .views.collective_export import CollectiveExport
from .views.collective_import import CollectiveImportFormView
from .views.collective_list import CollectiveList
from .views.collective_permissions import CollectivePermissions
from .views.collective_questions import CollectiveQuestions
from .views.global_settings import GlobalSettingsView
from .views.question_detail import QuestionDetail
from .views.user_description import UserDescriptionView
from .views.user_group_members import (
    UserGroupMembers,
    UserGroupMemberDetails,
    UserGroupMembersJoin,
    UserGroupMembersLeave,
)
from .views.user_groups import UserGroups, UserGroupsByType
from .views.user_info import UserInfo, UserMemberships


urlpatterns = [
    path(
        "api/collective/<slug:collective_name>/question/<slug:question_name>/answer/<slug:username>/",
        AnswerDetail.as_view(),
        name="answer",
    ),
    path(
        "api/collective/<slug:collective_name>/question/<slug:question_name>/",
        QuestionDetail.as_view(),
        name="question",
    ),
    path(
        "api/collective/<slug:name>/answers/",
        CollectiveAnswers.as_view(),
        name="answers",
    ),
    path(
        "api/collective/<slug:collective_name>/admin/<slug:username>/",
        CollectiveAdmin.as_view(),
        name="collective_admin",
    ),
    path(
        "api/collective/<slug:collective>/group/<slug:group>/members/",
        UserGroupMembers.as_view(),
        name="collective_user_group_members",
    ),
    path(
        "api/collective/<slug:collective>/group/<slug:group>/join/",
        UserGroupMembersJoin.as_view(),
        name="collective_user_group_join",
    ),
    path(
        "api/collective/<slug:collective>/group/<slug:group>/leave/",
        UserGroupMembersLeave.as_view(),
        name="collective_user_group_leave",
    ),
    path(
        "api/collective/<slug:collective>/user_groups/type/<type_name>/",
        UserGroupsByType.as_view(),
        name="collective_user_groups_by_type",
    ),
    path(
        "api/collective/<slug:collective>/user_groups/",
        UserGroups.as_view(),
        name="collective_user_groups",
    ),
    path(
        "api/collective/<slug:collective_name>/admins/",
        CollectiveAdmins.as_view(),
        name="collective_admins",
    ),
    path(
        "api/collective/<slug:name>/permissions/",
        CollectivePermissions.as_view(),
        name="collective_permissions",
    ),
    path(
        "api/collective/<slug:collective_name>/export/",
        CollectiveExport.as_view(),
        name="collective_export",
    ),
    path(
        "api/collective/<slug:name>/questions/",
        CollectiveQuestions.as_view(),
        name="questions",
    ),
    path(
        "api/collective/<slug:name>/",
        CollectiveDetail.as_view(),
        name="collective",
    ),
    path("api/collectives/", CollectiveList.as_view(), name="collectives"),
    path(
        "api/group/<slug:group>/members/",
        UserGroupMembers.as_view(),  # Returns list of usernames
        kwargs={"collective": None},
        name="user_group_members",
    ),
    path(
        "api/group/<slug:group>/member_details/",
        UserGroupMemberDetails.as_view(),  # Returns detailed member information
        kwargs={"collective": None},
        name="user_group_member_details",
    ),
    path(
        "api/group/<slug:group>/join/",
        UserGroupMembersJoin.as_view(),
        kwargs={"collective": None},
        name="user_group_join",
    ),
    path(
        "api/group/<slug:group>/leave/",
        UserGroupMembersLeave.as_view(),
        kwargs={"collective": None},
        name="user_group_leave",
    ),
    path(
        "api/user_groups/type/<type_name>/",
        UserGroupsByType.as_view(),
        kwargs={"collective": None},
        name="user_groups_by_type",
    ),
    path(
        "api/user_groups/",
        UserGroups.as_view(),
        kwargs={"collective": None},
        name="user_groups",
    ),
    path(
        "api/user/<slug:username>/memberships/",
        UserMemberships.as_view(),
        name="user_memberships",
    ),
    path("api/user/<slug:username>/description/", UserDescriptionView.as_view(), name="user_description"),
    path("api/user/<slug:username>/", UserInfo.as_view(), name="user_info"),
    path("api/settings/", GlobalSettingsView.as_view(), name="settings"),
    path("upload/", CollectiveImportFormView.as_view(), name="collective_import_form"),
    path("", index, name="index"),
]
