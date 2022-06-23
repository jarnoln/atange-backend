import logging

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from collective.models import UserGroup, Collective


class CollectiveAdmin(APIView):
    """List current user's permissions in collective"""

    def post(self, request, collective_name, username, format=None):
        logger = logging.getLogger(__name__)
        logger.debug("CollectiveAdmin:post {} {}".format(collective_name, username))
        collective = get_object_or_404(Collective, name=collective_name)
        permissions = collective.get_permissions(request.user)
        if not permissions["can_edit"]:
            return Response(
                {"detail": "No permission to edit"}, status=status.HTTP_401_UNAUTHORIZED
            )
        user = get_object_or_404(User, username=username)
        admin_group = collective.admin_group
        if not admin_group:
            admin_group_name = "{}_admins".format(collective.name)
            admin_group_title = "{} administrators".format(collective.name)
            admin_group = UserGroup.objects.create(
                name=admin_group_name, title=admin_group_title
            )
            collective.admin_group = admin_group
            collective.save()

        if admin_group.is_member(user):
            return Response(
                {"detail": "Already admin"}, status=status.HTTP_400_BAD_REQUEST
            )

        admin_group.add_member(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, collective_name, username, format=None):
        collective = get_object_or_404(Collective, name=collective_name)
        permissions = collective.get_permissions(request.user)
        if not permissions["can_edit"]:
            return Response(
                {"detail": "No permission to edit"}, status=status.HTTP_401_UNAUTHORIZED
            )
        user = get_object_or_404(User, username=username)
        admin_group = collective.admin_group
        if not admin_group:
            admin_group_name = "{}_admins".format(collective.name)
            admin_group_title = "{} administrators".format(collective.name)
            admin_group = UserGroup.objects.create(
                name=admin_group_name, title=admin_group_title
            )
            collective.admin_group = admin_group
            collective.save()

        if not admin_group.is_member(user):
            return Response({"detail": "Not admin"}, status=status.HTTP_400_BAD_REQUEST)

        admin_group.kick_member(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
