import logging

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from collective.serializers import (
    CollectiveSerializer,
)
from collective.models import UserGroup, Collective, Statistics


class CollectiveDetail(APIView):
    """Endpoint for collective operations"""

    def get(self, request, name, format=None):
        collective = get_object_or_404(Collective, name=name)
        serializer = CollectiveSerializer(collective)
        return Response(serializer.data)

    def put(self, request, name, format=None):
        collective = get_object_or_404(Collective, name=name)
        logger = logging.getLogger(__name__)
        logger.debug("CollectiveDetail:put collective_name:{}".format(name))
        logger.debug(" request.user:{}".format(request.user))
        permissions = collective.get_permissions(request.user)
        if not permissions["can_edit"]:
            return Response(
                {"detail": "No permission to edit"}, status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = CollectiveSerializer(collective, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, name, format=None):
        if Collective.objects.filter(name=name).count() != 0:
            return Response(
                {"detail": "Collective {} already exists".format(name)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Need to be logged in"}, status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = CollectiveSerializer(data=request.data)
        if serializer.is_valid():
            collective = serializer.save(creator=request.user)
            member_group_name = "{}_members".format(collective.name)
            member_group_title = "{} members".format(collective.name)
            admin_group_name = "{}_admins".format(collective.name)
            admin_group_title = "{} administrators".format(collective.name)
            member_group = UserGroup.objects.create(
                name=member_group_name, title=member_group_title
            )
            admin_group = UserGroup.objects.create(
                name=admin_group_name, title=admin_group_title
            )
            admin_group.add_member(request.user)
            collective.member_group = member_group
            collective.admin_group = admin_group
            collective.save()
            statistics = Statistics.objects.create()
            statistics.update()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name, format=None):
        collective = get_object_or_404(Collective, name=name)
        if request.user != collective.creator:
            return Response(
                {"detail": "Only creator can delete"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        collective.delete()
        statistics = Statistics.objects.create()
        statistics.update()
        return Response(status=status.HTTP_204_NO_CONTENT)
