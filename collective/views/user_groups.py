from rest_framework.views import APIView
from rest_framework.response import Response

from collective.models import UserGroup
from collective.serializers import UserGroupSerializer


class UserGroups(APIView):
    """List members of given user group (list of usenames)"""

    def get(self, request, collective, format=None):
        user_group_list = UserGroup.objects.filter(collective_name=collective).order_by('type', 'name')
        serializer = UserGroupSerializer(user_group_list, many=True)
        return Response(serializer.data)


class UserGroupsByType(APIView):
    """List members of given user group (list of usenames)"""

    def get(self, request, collective, type_name, format=None):
        user_group_list = UserGroup.objects.filter(collective_name=collective, type=type_name).order_by('name')
        serializer = UserGroupSerializer(user_group_list, many=True)
        return Response(serializer.data)
