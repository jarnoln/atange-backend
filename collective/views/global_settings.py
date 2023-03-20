from rest_framework.views import APIView
from rest_framework.response import Response

from collective.models import GlobalSettings, Collective
from collective.serializers import GlobalSettingsSerializer


class GlobalSettingsView(APIView):
    def get(self, request, format=None):
        collectives = Collective.objects.count()
        collective_list = Collective.objects.all()
        gs_count = GlobalSettings.objects.count()
        if GlobalSettings.objects.count() == 0:
            gs = GlobalSettings.objects.create()
        else:
            gs = GlobalSettings.objects.first()

        serializer = GlobalSettingsSerializer(gs)
        return Response(serializer.data)
