from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Collective


def index(request):
    collectives = Collective.objects.all()
    context = {'collectives': collectives}
    return render(request, 'collective/index.html', context)


class UserInfoSerializer(serializers.ModelSerializer):
    """ Editable user data (does not include username or password) """
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class CollectiveSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    class Meta:
        model = Collective
        fields = ['name', 'title', 'description', 'is_visible', 'creator', 'created', 'edited']


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


class CollectiveDetail(APIView):
    def get(self, request, name, format=None):
        collective = get_object_or_404(Collective, name=name)
        serializer = CollectiveSerializer(collective)
        return Response(serializer.data)

    def put(self, request, name, format=None):
        collective = get_object_or_404(Collective, name=name)
        serializer = CollectiveSerializer(collective, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, name, format=None):
        if Collective.objects.filter(name=name).count() != 0:
            return Response({'detail': 'Collective {} already exists'.format(name)}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CollectiveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name, format=None):
        collective = get_object_or_404(Collective, name=name)
        if request.user != collective.creator:
            return Response({'detail': 'Only creator can delete'}, status=status.HTTP_401_UNAUTHORIZED)

        collective.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
