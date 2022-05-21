from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Collective, QuestionnaireItem


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


class CollectiveListSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Collective
        fields = ['name', 'title', 'creator', 'created']


class QuestionListSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    parent = serializers.ReadOnlyField(source='parent.name')

    class Meta:
        model = QuestionnaireItem
        fields = ['name', 'title', 'description', 'item_type', 'parent', 'order', 'creator', 'created']
