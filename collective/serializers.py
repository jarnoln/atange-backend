import logging

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Collective, GlobalSettings, QuestionnaireItem, Answer, UserGroup, UserDescription


class GlobalSettingsSerializer(serializers.ModelSerializer):
    """Editable user data (does not include username or password)"""

    class Meta:
        model = GlobalSettings
        fields = '__all__'


class UserInfoSerializer(serializers.ModelSerializer):
    """Editable user data (does not include username or password)"""

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]


class UserDetailSerializer(serializers.ModelSerializer):
    """User data shown to other users"""

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]


class UserDescriptionSerializer(serializers.ModelSerializer):
    """Editable user data (does not include username or password)"""

    class Meta:
        model = UserDescription
        fields = ["description", "home_page", "candidate_number"]


class UserGroupSerializer(serializers.ModelSerializer):
    """Editable user data (does not include username or password)"""

    class Meta:
        model = UserGroup
        fields = ["name", "title", "type"]


class CollectiveSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source="creator.username")

    class Meta:
        model = Collective
        fields = [
            "name",
            "title",
            "description",
            "is_visible",
            "creator",
            "created",
            "edited",
        ]


class CollectiveListSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source="creator.username")

    class Meta:
        model = Collective
        fields = ["name", "title", "description", "is_visible", "creator", "created"]


class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    question = serializers.ReadOnlyField(source="question.name")

    class Meta:
        model = Answer
        fields = ["question", "user", "vote", "comment"]


class QuestionSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source="creator.username")
    parent = serializers.ReadOnlyField(source="parent.name")
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = QuestionnaireItem
        fields = [
            "name",
            "title",
            "description",
            "item_type",
            "parent",
            "order",
            "creator",
            "created",
            "answers",
        ]


class QuestionListSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source="creator.username")
    parent = serializers.ReadOnlyField(source="parent.name")
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = QuestionnaireItem
        fields = [
            "name",
            "title",
            "item_type",
            "parent",
            "order",
            "description",
            "creator",
            "answers",
        ]


class CollectiveExportSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source="creator.username")
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Collective
        fields = [
            "name",
            "title",
            "description",
            "is_visible",
            "creator",
            "created",
            "edited",
            "questions",
        ]
