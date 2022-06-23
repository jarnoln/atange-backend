from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from collective.models import Collective


class CollectiveAdmins(APIView):
    """List of collective's administrator usernames"""

    def get(self, request, collective_name, format=None):
        collective = get_object_or_404(Collective, name=collective_name)
        admin_group = collective.admin_group
        admin_usernames = []
        if admin_group:
            admins = admin_group.members
            for admin in admins:
                admin_usernames.append(admin.username)
        return Response(admin_usernames)
