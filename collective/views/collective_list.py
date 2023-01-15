import logging

from rest_framework.views import APIView
from rest_framework.response import Response

from collective.serializers import CollectiveListSerializer
from collective.models import Collective


class CollectiveList(APIView):
    """List of public collectives

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
        collective_list = Collective.objects.all()
        serializer = CollectiveListSerializer(collective_list, many=True)
        return Response(serializer.data)
