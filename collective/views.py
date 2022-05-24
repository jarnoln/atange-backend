# import logging

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import CollectiveSerializer, CollectiveListSerializer, UserInfoSerializer, QuestionListSerializer, \
    QuestionSerializer, AnswerSerializer
from .models import Collective, QuestionnaireItem, Answer


def index(request):
    collectives = Collective.objects.all()
    context = {'collectives': collectives}
    return render(request, 'collective/index.html', context)


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


class CollectiveList(APIView):
    """ List of public collectives

    Example response:
    -----------------

    ```
    [
        {
            "name":"jla",
            "title":"JLA",
            "created":"2022-03-07T06:39:58.410779Z"
        },
        {
            "name":"jsa",
            "title":"JSA",
            "created":"2022-03-07T07:58:41.012390Z"
        }
    ]
    ```
    """
    def get(self, request, format=None):
        collective_list = Collective.objects.filter(is_visible=True)
        serializer = CollectiveListSerializer(collective_list, many=True)
        return Response(serializer.data)


class CollectiveDetail(APIView):
    """ Endpoint for collective operations """
    def get(self, request, name, format=None):
        collective = get_object_or_404(Collective, name=name)
        serializer = CollectiveSerializer(collective)
        return Response(serializer.data)

    def put(self, request, name, format=None):
        collective = get_object_or_404(Collective, name=name)
        if request.user != collective.creator:
            return Response({'detail': 'Only creator can edit'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CollectiveSerializer(collective, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, name, format=None):
        if Collective.objects.filter(name=name).count() != 0:
            return Response({'detail': 'Collective {} already exists'.format(name)}, status=status.HTTP_400_BAD_REQUEST)
        if not request.user.is_authenticated:
            return Response({'detail': 'Need to be logged in'}, status=status.HTTP_401_UNAUTHORIZED)
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


class CollectiveQuestions(APIView):
    """ List of questions (and headers) in collective
    """
    def get(self, request, name, format=None):
        collective = get_object_or_404(Collective, name=name)
        question_list = QuestionnaireItem.objects.filter(collective=collective).order_by('order')
        serializer = QuestionListSerializer(question_list, many=True)
        return Response(serializer.data)


class QuestionDetail(APIView):
    """ Endpoint for question operations """
    def get(self, request, collective_name, question_name, format=None):
        collective = get_object_or_404(Collective, name=collective_name)
        question = get_object_or_404(QuestionnaireItem, collective=collective, name=question_name)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, collective_name, question_name, format=None):
        collective = get_object_or_404(Collective, name=collective_name)
        question = get_object_or_404(QuestionnaireItem, collective=collective, name=question_name)

        if request.user != question.creator:
            return Response({'detail': 'Only creator can edit'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, collective_name, question_name, format=None):
        collective = get_object_or_404(Collective, name=collective_name)
        if QuestionnaireItem.objects.filter(collective=collective, name=question_name).count() != 0:
            return Response({'detail': 'Question {} already exists'.format(question_name)}, status=status.HTTP_400_BAD_REQUEST)
        if not request.user.is_authenticated:
            return Response({'detail': 'Need to be logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(collective=collective, creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, collective_name, question_name, format=None):
        collective = get_object_or_404(Collective, name=collective_name)
        question = get_object_or_404(QuestionnaireItem, collective=collective, name=question_name)
        if request.user != question.creator:
            return Response({'detail': 'Only creator can delete'}, status=status.HTTP_401_UNAUTHORIZED)

        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerDetail(APIView):
    """ Endpoint for answer operations """
    def get(self, request, collective_name, question_name, username, format=None):
        collective = get_object_or_404(Collective, name=collective_name)
        question = get_object_or_404(QuestionnaireItem, collective=collective, name=question_name)
        user = get_object_or_404(User, username=username)
        answer = get_object_or_404(Answer, question=question, user=user)
        serializer = AnswerSerializer(answer)
        return Response(serializer.data)

    def put(self, request, collective_name, question_name, username, format=None):
        collective = get_object_or_404(Collective, name=collective_name)
        question = get_object_or_404(QuestionnaireItem, collective=collective, name=question_name)
        user = get_object_or_404(User, username=username)
        if request.user != user:
            return Response({'detail': 'Can edit only own answers'}, status=status.HTTP_401_UNAUTHORIZED)

        answer = get_object_or_404(Answer, question=question, user=user)
        serializer = AnswerSerializer(answer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, collective_name, question_name, username, format=None):
        collective = get_object_or_404(Collective, name=collective_name)
        question = get_object_or_404(QuestionnaireItem, collective=collective, name=question_name)
        if not request.user.is_authenticated:
            return Response({'detail': 'Need to be logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user.username != username:
            return Response({'detail': 'Can add only own answers'}, status=status.HTTP_401_UNAUTHORIZED)
        if Answer.objects.filter(question=question, user=request.user).count() != 0:
            return Response({'detail': 'Answer already exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(question=question, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, collective_name, question_name, username, format=None):
        if not request.user.is_authenticated:
            return Response({'detail': 'Need to be logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        if request.user.username != username:
            return Response({'detail': 'Can delete only own answers'}, status=status.HTTP_401_UNAUTHORIZED)

        collective = get_object_or_404(Collective, name=collective_name)
        question = get_object_or_404(QuestionnaireItem, collective=collective, name=question_name)
        answer = get_object_or_404(Answer, question=question, user=request.user)
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
