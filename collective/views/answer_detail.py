import logging

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from collective.serializers import (
    AnswerSerializer,
)
from collective.models import Collective, QuestionnaireItem, Answer, Statistics


class AnswerDetail(APIView):
    """Endpoint for answer operations"""

    def get(self, request, collective_name, question_name, username, format=None):
        collective = get_object_or_404(Collective, name=collective_name)
        question = get_object_or_404(
            QuestionnaireItem, collective=collective, name=question_name
        )
        user = get_object_or_404(User, username=username)
        answer = get_object_or_404(Answer, question=question, user=user)
        serializer = AnswerSerializer(answer)
        return Response(serializer.data)

    def put(self, request, collective_name, question_name, username, format=None):
        collective = get_object_or_404(Collective, name=collective_name)
        question = get_object_or_404(
            QuestionnaireItem, collective=collective, name=question_name
        )
        user = get_object_or_404(User, username=username)
        if request.user != user:
            return Response(
                {"detail": "Can edit only own answers"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # answer = get_object_or_404(Answer, question=question, user=user)
        answer, created = Answer.objects.get_or_create(question=question, user=user)
        serializer = AnswerSerializer(answer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            if created:
                statistics = Statistics.objects.create()
                statistics.update()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, collective_name, question_name, username, format=None):
        collective = get_object_or_404(Collective, name=collective_name)
        question = get_object_or_404(
            QuestionnaireItem, collective=collective, name=question_name
        )
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Need to be logged in"}, status=status.HTTP_401_UNAUTHORIZED
            )
        if request.user.username != username:
            return Response(
                {"detail": "Can add only own answers"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if Answer.objects.filter(question=question, user=request.user).count() != 0:
            return Response(
                {"detail": "Answer already exists"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(question=question, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, collective_name, question_name, username, format=None):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Need to be logged in"}, status=status.HTTP_401_UNAUTHORIZED
            )

        if request.user.username != username:
            return Response(
                {"detail": "Can delete only own answers"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        collective = get_object_or_404(Collective, name=collective_name)
        question = get_object_or_404(
            QuestionnaireItem, collective=collective, name=question_name
        )
        answer = get_object_or_404(Answer, question=question, user=request.user)
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
