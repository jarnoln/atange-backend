from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from collective.serializers import (
    QuestionSerializer,
)
from collective.models import Collective, QuestionnaireItem, Statistics


class QuestionDetail(APIView):
    """Endpoint for question operations"""

    def get(self, request, collective_name, question_name, format=None):
        collective = get_object_or_404(Collective, name=collective_name)
        question = get_object_or_404(
            QuestionnaireItem, collective=collective, name=question_name
        )
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, collective_name, question_name, format=None):
        collective = get_object_or_404(Collective, name=collective_name)
        question = get_object_or_404(
            QuestionnaireItem, collective=collective, name=question_name
        )

        if request.user != question.creator:
            return Response(
                {"detail": "Only creator can edit"}, status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, collective_name, question_name, format=None):
        collective = get_object_or_404(Collective, name=collective_name)
        if (
            QuestionnaireItem.objects.filter(
                collective=collective, name=question_name
            ).count()
            != 0
        ):
            return Response(
                {"detail": "Question {} already exists".format(question_name)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Need to be logged in"}, status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(collective=collective, creator=request.user)
            statistics = Statistics.objects.create()
            statistics.update()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, collective_name, question_name, format=None):
        collective = get_object_or_404(Collective, name=collective_name)
        question = get_object_or_404(
            QuestionnaireItem, collective=collective, name=question_name
        )
        if request.user != question.creator:
            return Response(
                {"detail": "Only creator can delete"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        question.delete()
        statistics = Statistics.objects.create()
        statistics.update()
        return Response(status=status.HTTP_204_NO_CONTENT)
