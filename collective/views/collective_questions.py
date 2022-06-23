from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from collective.serializers import QuestionListSerializer
from collective.models import Collective, QuestionnaireItem


class CollectiveQuestions(APIView):
    """List of questions (and headers) in collective"""

    def get(self, request, name, format=None):
        collective = get_object_or_404(Collective, name=name)
        question_list = QuestionnaireItem.objects.filter(
            collective=collective
        ).order_by("order")
        serializer = QuestionListSerializer(question_list, many=True)
        return Response(serializer.data)
