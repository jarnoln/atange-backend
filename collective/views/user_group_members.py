import logging

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from collective.models import UserGroup


class UserGroupMembers(APIView):
    """List members of given user group (list of usenames)"""

    def get(self, request, collective, group, format=None):
        user_group = get_object_or_404(
            UserGroup, name=group, collective_name=collective
        )
        member_usernames = []
        for member in user_group.members:
            member_usernames.append(member.username)
        return Response(member_usernames)


class UserGroupMembersJoin(APIView):
    """Endpoint for collective operations"""

    def post(self, request, collective, group, format=None):
        user_group = get_object_or_404(
            UserGroup, name=group, collective_name=collective
        )
        logger = logging.getLogger(__name__)
        if not request.user.is_authenticated:
            logger.debug(
                "User {} failed to join group {}: Not logged in".format(
                    request.user, user_group.name
                )
            )
            return Response(
                {"detail": "Need to be logged in"}, status=status.HTTP_401_UNAUTHORIZED
            )
        success = user_group.add_member(request.user)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserGroupMembersLeave(APIView):
    """Endpoint for collective operations"""

    def post(self, request, collective, group, format=None):
        logger = logging.getLogger(__name__)
        logger.debug("User {} leaving group {}".format(request.user, group))
        user_group = get_object_or_404(
            UserGroup, name=group, collective_name=collective
        )
        if not request.user.is_authenticated:
            logger.debug(
                "User {} failed to leave group {}: Not logged in".format(
                    request.user, user_group.name
                )
            )
            return Response(
                {"detail": "Need to be logged in"}, status=status.HTTP_401_UNAUTHORIZED
            )
        user_group.kick_member(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
