from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from collective.models import Collective


class CollectivePermissions(APIView):
    """List current user's permissions in collective"""

    def get(self, request, name, format=None):
        collective = get_object_or_404(Collective, name=name)
        return Response(collective.get_permissions(request.user))
