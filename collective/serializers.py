from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Collective


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
