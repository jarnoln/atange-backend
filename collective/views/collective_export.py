import logging

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from collective.serializers import CollectiveExportSerializer
from collective.models import Collective


class CollectiveExport(APIView):
    """Endpoint for exporting collective contents as JSON file"""

    def get(self, request, collective_name, format=None):
        logger = logging.getLogger(__name__)
        logger.debug("CollectiveExport:get collective_name:{}".format(collective_name))
        logger.debug(" request.user:{}".format(request.user))
        logger.debug(" format:{}".format(format))

        collective = get_object_or_404(Collective, name=collective_name)
        serializer = CollectiveExportSerializer(collective)
        response = Response(serializer.data, content_type="application/json")
        logger.debug("  serializer.data: {}".format(serializer.data))
        response.headers['Content-Disposition'] = 'attachment; filename={}.json'.format(collective_name)
        return response
