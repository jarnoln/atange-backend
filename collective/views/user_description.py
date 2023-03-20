import logging

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from collective.models import UserDescription
from collective.serializers import UserDescriptionSerializer


class UserDescriptionView(APIView):
    def get(self, request, username, format=None):
        user = get_object_or_404(User, username=username)
        description, created = UserDescription.objects.get_or_create(user=user)
        serializer = UserDescriptionSerializer(description)
        return Response(serializer.data)

    def put(self, request, username, format=None):
        logger = logging.getLogger(__name__)
        logger.info('PUT {}'.format(str(request.data)))
        user = get_object_or_404(User, username=username)
        description, created = UserDescription.objects.get_or_create(user=user)
        serializer = UserDescriptionSerializer(description, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            logger.warning('Invalid user data: {}'.format(str(serializer.errors)))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
