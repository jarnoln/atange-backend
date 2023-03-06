import logging

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from collective.models import UserGroup
from collective.serializers import UserInfoSerializer, UserGroupSerializer


class UserInfo(APIView):
    def get(self, request, username, format=None):
        user = get_object_or_404(User, username=username)
        serializer = UserInfoSerializer(user)
        return Response(serializer.data)

    def put(self, request, username, format=None):
        user = get_object_or_404(User, username=username)
        serializer = UserInfoSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserMemberships(APIView):
    def get(self, request, username, format=None):
        user = get_object_or_404(User, username=username)
        groups = UserGroup.objects.filter(memberships__user=user)
        serializer = UserGroupSerializer(groups, many=True)
        return Response(serializer.data)
