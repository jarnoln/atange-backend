from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from collective.serializers import AnswerSerializer
from collective.models import Collective, Answer


class CollectiveAnswers(APIView):
    """List of all answers in collective"""

    def get(self, request, name, format=None):
        collective = get_object_or_404(Collective, name=name)
        question_list = Answer.objects.filter(question__collective=collective).order_by(
            "question__order"
        )
        serializer = AnswerSerializer(question_list, many=True)
        return Response(serializer.data)
